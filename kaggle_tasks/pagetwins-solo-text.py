# %% [markdown]
# # PageTwins: do AI graders notice when a landing page breaks?
#
# 10 original landing pages, each paired with 10 one-defect twins (100 pairs),
# plus 20 control pairs (10 identical, 10 with a harmless change).
# Data: CC BY 4.0. Code: MIT. Both by Prasenjit Nayak.

# %%
import glob
import json
import os
import re
from collections import Counter, defaultdict

import pandas as pd

import kaggle_benchmarks as kbench
from kaggle_benchmarks.content_types import images

LABELS = {
    "missing_cta": "There is no button or link to sign up, buy or start.",
    "hidden_price": "The page never says what the paid product or plans cost.",
    "contradiction": "Two parts of the page make claims that cannot both be true.",
    "vague_headline": "The main headline does not say what the product is or does.",
    "typos": "Misspelled words in prominent text such as the headline.",
    "placeholder_text": 'Leftover template text such as "Lorem ipsum" or "{{name}}" is visible.',
    "low_contrast": "Important text is very hard to read against its background.",
    "broken_image": "An image failed to load and shows an empty box or broken-image icon.",
    "blocking_popup": "A popup or overlay covers the main content when the page opens.",
    "cut_off_text": "Text is cut off or hidden by another element, so it cannot be fully read.",
}
LABEL_LIST = "\n".join(f"{k}: {v}" for k, v in LABELS.items())
MAX_TOKENS = int(os.environ.get("PAGETWINS_MAX_TOKENS", "8192"))
N_JOBS = int(os.environ.get("PAGETWINS_N_JOBS", "4"))
# Comma-separated base ids (e.g. "B01") restrict a run for quick local validation; unset means all 10 bases.
BASES = [b for b in os.environ.get("PAGETWINS_BASES", "").split(",") if b]


def find_data_root():
    """Locate the dataset folder (the one that contains pairs.csv)."""
    candidates = [os.environ.get("PAGETWINS_DATA", ""), "dataset", "../dataset"]
    candidates += sorted(glob.glob("/kaggle/input/**/pairs.csv", recursive=True))
    for c in candidates:
        if not c:
            continue
        path = c[: -len("pairs.csv")] if c.endswith("pairs.csv") else c
        if os.path.exists(os.path.join(path, "pairs.csv")):
            return os.path.abspath(path)
    raise FileNotFoundError("PageTwins dataset not found. Attach the dataset or set PAGETWINS_DATA.")


DATA_ROOT = find_data_root()

# %% [markdown]
# ## Prompts
# The same wording is used for every model. Screenshot and text modes differ
# only in the sentence that describes the input.

# %%
VISION_INPUT_PAIR = "The first image is Page A and the second image is Page B. Each image is a full-page screenshot."
TEXT_INPUT_PAIR = (
    "Each page is given as text: the visible text and the role of each element (heading, button, link, "
    "image alt text, dialog) in reading order. Styling, colors and layout are not included."
)
VISION_INPUT_SOLO = "The image is a full-page screenshot."
TEXT_INPUT_SOLO = (
    "The page is given as text: the visible text and the role of each element (heading, button, link, "
    "image alt text, dialog) in reading order. Styling, colors and layout are not included."
)

PAIR_PROMPT = """You are reviewing two versions of a landing page before launch. {input_note}

The two versions may be equally good. Or one version may have a problem that the other does not have, a problem that would hurt sign-ups, sales or trust.

Decide which version you would ship:
- "A" if Page A is better, because Page B has a problem that Page A does not have.
- "B" if Page B is better, because Page A has a problem that Page B does not have.
- "same" if neither version has such a problem, or the differences do not matter.

If you answer "A" or "B", label the main problem of the worse version with one of these labels:
{labels}
other: A different problem.
If you answer "same", use the label "none".

Reply with only a JSON object and nothing else:
{{"better": "A" or "B" or "same", "problem": "<label>", "evidence": "<one short sentence saying where you see the problem>"}}"""

SOLO_PROMPT = """You are reviewing a landing page before launch. {input_note}

Check the page for these problems:
{labels}

List every problem from this list that you can see on the page. Only list a problem if you can point to where it is. If none of these problems are present, return an empty list.
Then rate how ready the page is to launch, from 1 (not ready) to 10 (ready to launch).

Reply with only a JSON object and nothing else:
{{"problems": ["<label>", ...], "score": <integer from 1 to 10>, "evidence": "<one short sentence about the most serious problem, or none>"}}"""


def find_pages_dir():
    """Folder that holds the per-page folders; uploaded archives can add a nesting level on Kaggle."""
    first = pd.read_csv(os.path.join(DATA_ROOT, "pages.csv")).page_id.iloc[0]
    if os.path.isdir(os.path.join(DATA_ROOT, "pages", first)):
        return os.path.join(DATA_ROOT, "pages")
    search_roots = [DATA_ROOT, os.path.dirname(DATA_ROOT)]
    for root in search_roots:
        hits = glob.glob(os.path.join(root, "**", first, "page.txt"), recursive=True)
        if hits:
            return os.path.dirname(os.path.dirname(hits[0]))
    raise FileNotFoundError(f"Page folders not found under {DATA_ROOT}")


PAGES_DIR = find_pages_dir()


def page_file(page_id, name):
    return os.path.join(PAGES_DIR, page_id, name)


def page_text(page_id):
    with open(page_file(page_id, "page.txt"), encoding="utf-8") as f:
        return f.read().strip()

# %% [markdown]
# ## Parsing
# Answers are parsed leniently (code fences, extra prose, single quotes), and
# anything that cannot be parsed is scored as wrong, never dropped.

# %%
def parse_json(text):
    if not isinstance(text, str):
        return None
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.S)
    text = re.sub(r"```(?:json)?", "", text)
    starts = [m.start() for m in re.finditer(r"\{", text)]
    for s in starts:
        depth = 0
        for i in range(s, len(text)):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
                if depth == 0:
                    chunk = text[s:i + 1]
                    for candidate in (chunk, chunk.replace("'", '"')):
                        try:
                            obj = json.loads(candidate)
                            if isinstance(obj, dict):
                                return obj
                        except json.JSONDecodeError:
                            pass
                    break
    if starts:  # an object cut off before its closing brace
        tail = text[starts[-1]:].rstrip()
        for suffix in ('"}', "}", '"]}', "]}"):
            try:
                obj = json.loads(tail + suffix)
                if isinstance(obj, dict):
                    return obj
            except json.JSONDecodeError:
                pass
    return None


def norm_label(x):
    if not isinstance(x, str):
        return "invalid"
    s = x.strip().lower().replace("-", "_").replace(" ", "_").strip("\"'.")
    if s in LABELS or s in ("other", "none"):
        return s
    for k in LABELS:
        if k in s:
            return k
    return "other" if s else "invalid"


def norm_better(x):
    if not isinstance(x, str):
        return "invalid"
    s = x.strip().strip("\"'.").lower()
    if s in ("a", "page a", "page_a"):
        return "A"
    if s in ("b", "page b", "page_b"):
        return "B"
    if s in ("same", "none", "equal", "neither", "tie", "either"):
        return "same"
    return "invalid"


def _usage(chat):
    try:
        u = chat.usage
        return u.input_tokens, u.output_tokens
    except Exception:
        return None, None

# %% [markdown]
# ## Per-item tasks
# Each comparison and each solo grade runs in its own isolated chat.

# %%
@kbench.task(name="pagetwins-pair-item", store_task=False)
def pair_item(llm, pair_id, kind, category, order, page_a, page_b, expected, mode) -> dict:
    if mode == "vision":
        kbench.user.send("Page A:")
        kbench.user.send(images.from_path(page_file(page_a, "screenshot.png")))
        kbench.user.send("Page B:")
        kbench.user.send(images.from_path(page_file(page_b, "screenshot.png")))
        prompt = PAIR_PROMPT.format(input_note=VISION_INPUT_PAIR, labels=LABEL_LIST)
    else:
        prompt = (
            f"Page A:\n<page>\n{page_text(page_a)}\n</page>\n\n"
            f"Page B:\n<page>\n{page_text(page_b)}\n</page>\n\n"
            + PAIR_PROMPT.format(input_note=TEXT_INPUT_PAIR, labels=LABEL_LIST)
        )
    raw = llm.prompt(prompt, extra_api_params={"max_tokens": MAX_TOKENS})
    ans = parse_json(raw) or {}
    better = norm_better(ans.get("better"))
    problem = norm_label(ans.get("problem")) if better in ("A", "B") else ("none" if better == "same" else "invalid")
    tin, tout = _usage(kbench.chats.get_current_chat())
    return {
        "pair_id": pair_id, "kind": kind, "category": category, "order": order, "expected": expected,
        "better": better, "problem": problem, "valid": better != "invalid",
        "evidence": str(ans.get("evidence", ""))[:300], "raw": str(raw)[:1500],
        "input_tokens": tin, "output_tokens": tout,
    }


@kbench.task(name="pagetwins-solo-item", store_task=False)
def solo_item(llm, page_id, base_id, role, category, mode) -> dict:
    if mode == "vision":
        prompt = SOLO_PROMPT.format(input_note=VISION_INPUT_SOLO, labels=LABEL_LIST)
        raw = llm.prompt(prompt, image=images.from_path(page_file(page_id, "screenshot.png")),
                         extra_api_params={"max_tokens": MAX_TOKENS})
    else:
        prompt = (f"<page>\n{page_text(page_id)}\n</page>\n\n"
                  + SOLO_PROMPT.format(input_note=TEXT_INPUT_SOLO, labels=LABEL_LIST))
        raw = llm.prompt(prompt, extra_api_params={"max_tokens": MAX_TOKENS})
    ans = parse_json(raw)
    valid = isinstance(ans, dict) and isinstance(ans.get("problems"), list)
    problems = sorted({norm_label(p) for p in ans.get("problems", [])} - {"none", "invalid"}) if valid else []
    try:
        score = int(round(float(ans.get("score")))) if valid else None
        score = score if score is not None and 1 <= score <= 10 else None
    except (TypeError, ValueError):
        score = None
    tin, tout = _usage(kbench.chats.get_current_chat())
    return {
        "page_id": page_id, "base_id": base_id, "role": role, "category": category,
        "problems": problems, "score": score, "valid": valid,
        "evidence": str((ans or {}).get("evidence", ""))[:300], "raw": str(raw)[:1500],
        "input_tokens": tin, "output_tokens": tout,
    }

# %% [markdown]
# ## Evaluation rows
# Every pair is shown twice, once in each order, so position bias cancels out
# and can be measured.

# %%
def pair_rows(mode):
    pairs = pd.read_csv(os.path.join(DATA_ROOT, "pairs.csv"))
    rows = []
    for p in pairs.itertuples():
        for order in ("clean_first", "clean_second"):
            a, b = (p.clean_page_id, p.other_page_id) if order == "clean_first" else (p.other_page_id, p.clean_page_id)
            if p.kind == "control":
                expected = "same"
            else:
                expected = "A" if order == "clean_first" else "B"
            rows.append(dict(pair_id=p.pair_id, kind=p.kind, category=p.category, order=order,
                             page_a=a, page_b=b, expected=expected, mode=mode))
    df = pd.DataFrame(rows)
    return df[df.pair_id.str.split("-").str[0].isin(BASES)] if BASES else df


def solo_rows(mode):
    pages = pd.read_csv(os.path.join(DATA_ROOT, "pages.csv"))
    df = pd.DataFrame([dict(page_id=p.page_id, base_id=p.base_id, role=p.role, category=p.category, mode=mode)
                       for p in pages.itertuples()])
    return df[df.base_id.isin(BASES)] if BASES else df


def collect(runs, df, key_cols):
    """Turn evaluate() runs into records, keeping failed runs as invalid answers."""
    done = {}
    for run in runs.runs:
        res = run.result
        if isinstance(res, dict):
            done[tuple(res[k] for k in key_cols)] = res
    records = []
    for row in df.to_dict("records"):
        k = tuple(row[c] for c in key_cols)
        if k in done:
            records.append(done[k])
        else:
            r = {c: row[c] for c in row if c != "mode"}
            r.update(valid=False, better="invalid", problem="invalid", problems=[], score=None,
                     evidence="", raw="ERROR: no answer (API error or timeout)")
            records.append(r)
    return records

# %% [markdown]
# ## Scoring

# %%
def score_pairs(records):
    by = defaultdict(dict)
    for r in records:
        by[r["pair_id"]][r["order"]] = r
    defect, control = [], []
    a_votes = b_votes = 0
    for pid, d in by.items():
        r1, r2 = d.get("clean_first"), d.get("clean_second")
        if not r1 or not r2:
            continue
        for r in (r1, r2):
            if r["better"] == "A":
                a_votes += 1
            elif r["better"] == "B":
                b_votes += 1
        if r1["kind"] == "defect":
            cat = r1["category"]
            pick1, pick2 = r1["better"] == "A", r2["better"] == "B"
            defect.append(dict(
                pair_id=pid, category=cat,
                picked_both=pick1 and pick2,
                picked_one=pick1 != pick2,
                named_both=pick1 and pick2 and r1["problem"] == cat and r2["problem"] == cat,
                said_same_both=r1["better"] == "same" and r2["better"] == "same",
                same_letter=r1["better"] in ("A", "B") and r1["better"] == r2["better"],
                wrong_labels=[r["problem"] for r, ok in ((r1, pick1), (r2, pick2)) if ok and r["problem"] != cat],
            ))
        else:
            control.append(dict(pair_id=pid, category=r1["category"],
                                passed=r1["better"] == "same" and r2["better"] == "same",
                                false_alarms=int(r1["better"] != "same") + int(r2["better"] != "same")))
    n_d, n_c = len(defect), len(control)
    named = sum(x["named_both"] for x in defect) / max(n_d, 1)
    ctrl = sum(x["passed"] for x in control) / max(n_c, 1)
    per_cat = defaultdict(lambda: {"n": 0, "picked_both": 0, "named_both": 0})
    for x in defect:
        c = per_cat[x["category"]]
        c["n"] += 1
        c["picked_both"] += x["picked_both"]
        c["named_both"] += x["named_both"]
    ident = [x for x in control if x["category"] == "identical"]
    harm = [x for x in control if x["category"] != "identical"]
    return {
        "score": round(0.5 * named + 0.5 * ctrl, 4),
        "defect_pairs": n_d, "control_pairs": n_c,
        "named_both_rate": round(named, 4),
        "picked_both_rate": round(sum(x["picked_both"] for x in defect) / max(n_d, 1), 4),
        "picked_one_order_only_rate": round(sum(x["picked_one"] for x in defect) / max(n_d, 1), 4),
        "said_same_both_rate": round(sum(x["said_same_both"] for x in defect) / max(n_d, 1), 4),
        "same_letter_both_orders_rate": round(sum(x["same_letter"] for x in defect) / max(n_d, 1), 4),
        "control_pass_rate": round(ctrl, 4),
        "identical_pass_rate": round(sum(x["passed"] for x in ident) / max(len(ident), 1), 4),
        "harmless_pass_rate": round(sum(x["passed"] for x in harm) / max(len(harm), 1), 4),
        "share_of_picks_for_A": round(a_votes / max(a_votes + b_votes, 1), 4),
        "invalid_answers": sum(1 for r in records if not r["valid"]),
        "per_category": {k: dict(v) for k, v in sorted(per_cat.items())},
        "wrong_label_counts": dict(Counter(l for x in defect for l in x["wrong_labels"])),
    }


def score_solo(records):
    clean = {r["base_id"]: r for r in records if r["role"] == "clean"}
    twins = [r for r in records if r["role"] == "twin"]
    cleans = [r for r in records if r["role"] in ("clean", "variant")]
    per_cat = defaultdict(lambda: {"n": 0, "flagged": 0, "strict": 0, "score_drop": 0})
    strict_total = flagged_total = drops = drop_n = 0
    for t in twins:
        c = clean.get(t["base_id"])
        cat = t["category"]
        flagged = t["valid"] and cat in t["problems"]
        clean_ok = c is not None and c["valid"] and cat not in c["problems"]
        strict = flagged and clean_ok
        drop = (t["score"] is not None and c is not None and c["score"] is not None and t["score"] < c["score"])
        if t["score"] is not None and c is not None and c["score"] is not None:
            drop_n += 1
        pc = per_cat[cat]
        pc["n"] += 1
        pc["flagged"] += flagged
        pc["strict"] += strict
        pc["score_drop"] += drop
        strict_total += strict
        flagged_total += flagged
        drops += drop
    fp_labels = Counter(l for r in cleans if r["valid"] for l in r["problems"])
    n_t = max(len(twins), 1)
    clean_scores = [r["score"] for r in cleans if r["score"] is not None]
    twin_scores = [r["score"] for r in twins if r["score"] is not None]
    return {
        "score": round(strict_total / n_t, 4),
        "twins": len(twins), "clean_pages": len(cleans),
        "strict_detection_rate": round(strict_total / n_t, 4),
        "flagged_rate": round(flagged_total / n_t, 4),
        "score_drop_rate": round(drops / max(drop_n, 1), 4),
        "clean_pages_with_any_flag": round(sum(1 for r in cleans if r["valid"] and r["problems"]) / max(len(cleans), 1), 4),
        "mean_score_clean": round(sum(clean_scores) / max(len(clean_scores), 1), 3),
        "mean_score_twin": round(sum(twin_scores) / max(len(twin_scores), 1), 3),
        "invalid_answers": sum(1 for r in records if not r["valid"]),
        "per_category": {k: dict(v) for k, v in sorted(per_cat.items())},
        "false_flags_on_clean_pages": dict(fp_labels),
    }


def report(metrics, title):
    print(f"== {title}")
    print(json.dumps(metrics, indent=1))


def save_records(records, name):
    out = os.environ.get("PAGETWINS_OUT", "/kaggle/working" if os.path.exists("/kaggle/working") else ".")
    path = os.path.join(out, name)
    pd.DataFrame(records).to_csv(path, index=False)
    return path

# %% [markdown]
# ## Benchmark tasks

# %%
def _run_pairs(llm, mode):
    df = pair_rows(mode)
    with kbench.client.enable_cache():
        runs = pair_item.evaluate(llm=[llm], evaluation_data=df, n_jobs=N_JOBS, max_attempts=3,
                                  retry_delay=10, on_failure="continue", timeout=600)
    records = collect(runs, df, ["pair_id", "order"])
    m = score_pairs(records)
    save_records(records, f"pagetwins_pairs_{mode}_records.csv")
    report(m, f"PageTwins pairs ({mode})")
    kbench.assertions.assert_true(m["invalid_answers"] <= 0.05 * len(records),
                                  expectation=f"At most 5% unreadable answers (got {m['invalid_answers']} of {len(records)}).")
    kbench.assertions.assert_true(m["identical_pass_rate"] == 1.0,
                                  expectation=f"Says 'same' for every identical pair in both orders (got {m['identical_pass_rate']:.0%}).")
    kbench.assertions.assert_true(m["named_both_rate"] >= 0.5,
                                  expectation=f"Finds and names at least half of the {m['defect_pairs']} defects in both orders (got {m['named_both_rate']:.0%}).")
    return m["score"]


def _run_solo(llm, mode):
    df = solo_rows(mode)
    with kbench.client.enable_cache():
        runs = solo_item.evaluate(llm=[llm], evaluation_data=df, n_jobs=N_JOBS, max_attempts=3,
                                  retry_delay=10, on_failure="continue", timeout=600)
    records = collect(runs, df, ["page_id"])
    m = score_solo(records)
    save_records(records, f"pagetwins_solo_{mode}_records.csv")
    report(m, f"PageTwins solo ({mode})")
    kbench.assertions.assert_true(m["invalid_answers"] <= 0.05 * len(records),
                                  expectation=f"At most 5% unreadable answers (got {m['invalid_answers']} of {len(records)}).")
    kbench.assertions.assert_true(m["clean_pages_with_any_flag"] <= 0.25,
                                  expectation=f"Flags a problem on at most a quarter of the {m['clean_pages']} clean pages (got {m['clean_pages_with_any_flag']:.0%}).")
    kbench.assertions.assert_true(m["strict_detection_rate"] >= 0.5,
                                  expectation=f"Flags the defect on the twin but not on its clean page for at least half of the {m['twins']} twins (got {m['strict_detection_rate']:.0%}).")
    return m["score"]

# %% [markdown]
# ## Main task: solo (text)

# %%
@kbench.task(name="pagetwins-solo-text", description="Same as the screenshot solo task, but the page is given as its visible text and element roles.")
def pagetwins_solo_text(llm) -> float:
    return _run_solo(llm, "text")


pagetwins_solo_text.run(kbench.llm)
