"""Score PageTwins results and draw the charts.

    python harness/analyze.py                       # local Groq pilot (results/local)
    python harness/analyze.py --kaggle results/kaggle_raw

Raw answers are re-parsed with the current parser, so every model is scored by
the same code, and only items present for every model in a group are compared.
Writes results/summary.json, results/summary.md and charts/*.png.
"""

import argparse
import ast
import json
import os
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
os.environ.setdefault("PAGETWINS_DATA", str(ROOT / "dataset"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, str(Path(__file__).resolve().parent))

import matplotlib  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402

import pagetwins_core as core  # noqa: E402

CATS = list(core.LABELS)
CHARTS = ROOT / "charts"


def reparse_pair(r):
    raw = str(r.get("raw", ""))
    if raw.startswith("ERROR"):
        return r
    ans = core.parse_json(raw) or {}
    better = core.norm_better(ans.get("better"))
    r["better"] = better
    r["problem"] = core.norm_label(ans.get("problem")) if better in ("A", "B") else ("none" if better == "same" else "invalid")
    r["valid"] = better != "invalid"
    return r


def reparse_solo(r):
    raw = str(r.get("raw", ""))
    if raw.startswith("ERROR"):
        r["problems"] = []
        return r
    ans = core.parse_json(raw)
    valid = isinstance(ans, dict) and isinstance(ans.get("problems"), list)
    r["valid"] = valid
    r["problems"] = sorted({core.norm_label(p) for p in ans.get("problems", [])} - {"none", "invalid"}) if valid else []
    try:
        s = int(round(float(ans.get("score")))) if valid else None
        r["score"] = s if s is not None and 1 <= s <= 10 else None
    except (TypeError, ValueError):
        r["score"] = None
    return r


def load_local(root):
    """{(model, task, mode): [records]} from results/local/<model>/<task>_<mode>.jsonl, last answer per item wins."""
    groups = {}
    for f in sorted(Path(root).glob("*/*.jsonl")):
        task, mode = f.stem.split("_")[:2]
        model = f.parent.name.replace("__", "/")
        key_cols = ["pair_id", "order"] if task == "pairs" else ["page_id"]
        best = {}
        for line in f.read_text(encoding="utf-8").splitlines():
            r = json.loads(line)
            k = tuple(r[c] for c in key_cols)
            if k not in best or not str(r.get("raw", "")).startswith("ERROR"):
                best[k] = r
        fix = reparse_pair if task == "pairs" else reparse_solo
        groups[(model, task, mode)] = [fix(r) for r in best.values()]
    return groups


def load_kaggle(root):
    """Records CSVs written by the Kaggle tasks, found under `kaggle b t download` output."""
    groups = {}
    for f in sorted(Path(root).rglob("pagetwins_*_records.csv")):
        task, mode = f.stem.split("_")[1:3]
        model = f.relative_to(root).parts[2] if len(f.relative_to(root).parts) > 3 else f.parent.name
        df = pd.read_csv(f)
        recs = df.where(df.notna(), None).to_dict("records")
        for r in recs:
            if task == "solo" and isinstance(r.get("problems"), str):
                r["problems"] = ast.literal_eval(r["problems"])
        fix = reparse_pair if task == "pairs" else reparse_solo
        groups[(model, task, mode)] = [fix(r) for r in recs]
    return groups


def common_subset(groups):
    """Keep only the base pages answered by every model, per task and mode."""
    out = {}
    for task in ("pairs", "solo"):
        for mode in ("vision", "text"):
            keys = [k for k in groups if k[1] == task and k[2] == mode]
            if not keys:
                continue
            base_sets = []
            for k in keys:
                bases = defaultdict(set)
                for r in groups[k]:
                    b = (r["pair_id"].split("-")[0]) if task == "pairs" else r["base_id"]
                    bases[b].add((r.get("pair_id"), r.get("order")) if task == "pairs" else r["page_id"])
                full = 24 if task == "pairs" else 12
                base_sets.append({b for b, s in bases.items() if len(s) == full})
            shared = set.intersection(*base_sets)
            for k in keys:
                out[k] = [r for r in groups[k]
                          if ((r["pair_id"].split("-")[0]) if task == "pairs" else r["base_id"]) in shared]
    return out


def summarize(groups):
    rows = []
    for (model, task, mode), recs in sorted(groups.items()):
        if not recs:
            continue
        m = core.score_pairs(recs) if task == "pairs" else core.score_solo(recs)
        bases = sorted({(r["pair_id"].split("-")[0]) if task == "pairs" else r["base_id"] for r in recs})
        rows.append(dict(model=model, task=task, mode=mode, bases=",".join(bases), items=len(recs), metrics=m))
    return rows


def text_visible_rate(m, field):
    vis = [c for c in CATS if c in core_text_visible()]
    n = sum(m["per_category"].get(c, {}).get("n", 0) for c in vis)
    hit = sum(m["per_category"].get(c, {}).get(field, 0) for c in vis)
    return hit / n if n else float("nan")


def core_text_visible():
    return set(json.load(open(ROOT / "dataset" / "categories.json", encoding="utf-8"))["text_visible"])


def write_tables(rows, out_dir, title):
    lines = [f"# {title}", ""]
    lines.append("| Model | Task | Input | Bases | Score | Defects found and named | Controls passed | Picks for A | Text-visible defects | Invalid |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|")
    for r in rows:
        m = r["metrics"]
        if r["task"] == "pairs":
            found, ctrl, a = m["named_both_rate"], f"{m['control_pass_rate']:.0%}", f"{m['share_of_picks_for_A']:.0%}"
            tv = text_visible_rate(m, "named_both")
        else:
            found, ctrl, a = m["strict_detection_rate"], f"{1 - m['clean_pages_with_any_flag']:.0%} clean pages unflagged", ""
            tv = text_visible_rate(m, "strict")
        lines.append(f"| {r['model']} | {r['task']} | {r['mode']} | {r['bases']} | {m['score']:.2f} | {found:.0%} | "
                     f"{ctrl} | {a} | {tv:.0%} | {m['invalid_answers']} |")
    lines += ["", "## Per category (defects found and named in both orders for pairs; strict detection for solo)", ""]
    lines.append("| Model | Task | Input | " + " | ".join(CATS) + " |")
    lines.append("|---|---|---|" + "---|" * len(CATS))
    for r in rows:
        pc = r["metrics"]["per_category"]
        field = "named_both" if r["task"] == "pairs" else "strict"
        cells = [f"{pc[c][field]}/{pc[c]['n']}" if c in pc else "" for c in CATS]
        lines.append(f"| {r['model']} | {r['task']} | {r['mode']} | " + " | ".join(cells) + " |")
    (out_dir / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (out_dir / "summary.json").write_text(json.dumps(rows, indent=1), encoding="utf-8")


def short(model):
    return model.split("/")[-1]


def chart_heatmap(rows, path):
    rows = [r for r in rows]
    if not rows:
        return
    mat = []
    labels = []
    for r in rows:
        pc = r["metrics"]["per_category"]
        field = "named_both" if r["task"] == "pairs" else "strict"
        mat.append([pc[c][field] / pc[c]["n"] if c in pc and pc[c]["n"] else np.nan for c in CATS])
        labels.append(f"{short(r['model'])}  {r['task']} / {r['mode']}")
    mat = np.array(mat)
    fig, ax = plt.subplots(figsize=(12, 0.55 * len(rows) + 2.2))
    im = ax.imshow(mat, cmap="RdYlGn", vmin=0, vmax=1, aspect="auto")
    ax.set_xticks(range(len(CATS)), [c.replace("_", "\n") for c in CATS], fontsize=9)
    ax.set_yticks(range(len(labels)), labels, fontsize=9)
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            if not np.isnan(mat[i, j]):
                ax.text(j, i, f"{mat[i, j]:.0%}", ha="center", va="center", fontsize=8)
    for j, c in enumerate(CATS):
        if c not in core_text_visible():
            ax.get_xticklabels()[j].set_color("#b03030")
    ax.set_title("Share of defects caught, by category (red labels: invisible in the text view)", fontsize=11)
    fig.colorbar(im, ax=ax, fraction=0.025)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def chart_pairs_vs_solo(rows, path):
    combos = sorted({(r["model"], r["mode"]) for r in rows})
    if not combos:
        return
    get = {(r["model"], r["mode"], r["task"]): r["metrics"] for r in rows}
    x = np.arange(len(combos))
    pair_v = [get.get((m, mo, "pairs"), {}).get("named_both_rate", np.nan) for m, mo in combos]
    solo_v = [get.get((m, mo, "solo"), {}).get("strict_detection_rate", np.nan) for m, mo in combos]
    fig, ax = plt.subplots(figsize=(max(6, 1.6 * len(combos)), 4.2))
    ax.bar(x - 0.2, pair_v, 0.4, label="With the clean twin to compare (pairs)", color="#3b6fb6")
    ax.bar(x + 0.2, solo_v, 0.4, label="Page alone (solo)", color="#e0913a")
    for xi, v in zip(x - 0.2, pair_v):
        if not np.isnan(v):
            ax.text(xi, v + 0.01, f"{v:.0%}", ha="center", fontsize=8)
    for xi, v in zip(x + 0.2, solo_v):
        if not np.isnan(v):
            ax.text(xi, v + 0.01, f"{v:.0%}", ha="center", fontsize=8)
    ax.set_xticks(x, [f"{short(m)}\n{mo}" for m, mo in combos], fontsize=9)
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("Defects caught")
    ax.set_title("Comparing against a reference vs judging a page alone", fontsize=11)
    ax.legend(fontsize=8, loc="upper right")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def contact_sheet(path, categories=("low_contrast", "broken_image", "cut_off_text", "blocking_popup",
                                    "hidden_price", "placeholder_text"), base="B01"):
    pairs = pd.read_csv(ROOT / "dataset" / "pairs.csv")
    sel = [pairs[(pairs.base_id == base) & (pairs.category == c)].iloc[0] for c in categories]
    tiles = []
    for p in sel:
        x0, y0, x1, y1 = json.loads(p.pixel_diff_box)
        w, h = 760, 420
        cx = (x0 + x1) // 2 if x1 - x0 < w else (x0 + w // 2)
        box = (max(0, min(1280 - w, cx - w // 2)), max(0, y0 - 60))
        box = (box[0], box[1], box[0] + w, box[1] + h)
        pair_imgs = []
        for pid in (p.clean_page_id, p.other_page_id):
            im = Image.open(ROOT / "dataset" / "pages" / pid / "screenshot.png").convert("RGB")
            pair_imgs.append(im.crop(box).resize((w // 2, h // 2)))
        tiles.append((p.category, pair_imgs))
    tw, th, pad, head = 380, 210, 14, 26
    sheet = Image.new("RGB", (pad + 2 * (tw + pad), head + len(tiles) * (th + head + pad)), "white")
    d = ImageDraw.Draw(sheet)
    d.text((pad, 6), "Clean page", fill="black")
    d.text((pad * 2 + tw, 6), "Twin with one defect", fill="black")
    y = head
    for cat, (a, b) in tiles:
        d.text((pad, y + 4), cat.replace("_", " "), fill="#b03030")
        sheet.paste(a, (pad, y + head))
        sheet.paste(b, (2 * pad + tw, y + head))
        y += th + head + pad
    sheet.save(path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--local", default=str(ROOT / "results" / "local"))
    ap.add_argument("--kaggle", default="")
    args = ap.parse_args()
    CHARTS.mkdir(exist_ok=True)

    if args.kaggle:
        groups, tag, title = load_kaggle(args.kaggle), "kaggle", "PageTwins results on Kaggle"
    else:
        groups, tag, title = load_local(args.local), "local", "PageTwins local pilot (Groq)"
    groups = common_subset(groups)
    rows = summarize(groups)
    out_dir = ROOT / "results" / tag
    out_dir.mkdir(parents=True, exist_ok=True)
    write_tables(rows, out_dir, title)
    chart_heatmap(rows, CHARTS / f"{tag}_per_category.png")
    chart_pairs_vs_solo(rows, CHARTS / f"{tag}_pairs_vs_solo.png")
    contact_sheet(CHARTS / "examples.png")
    print((out_dir / "summary.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
