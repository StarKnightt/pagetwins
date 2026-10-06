"""Charts and summary facts for the Kaggle results (called from analyze.py)."""

import json

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

NAMES = {
    "gemini-3.7-flash": "Gemini 3.7 Flash",
    "gemini-3.5-flash-lite": "Gemini 3.5 Flash-Lite",
    "gemma-4-31b-it": "Gemma 4 31B",
    "claude-sonnet-5-5-default": "Claude Sonnet 5.5",
    "claude-haiku-4-5-20251001": "Claude Haiku 4.5",
    "gpt-6.1-sol": "GPT-6.1 Sol",
    "gpt-6-luna": "GPT-6 Luna",
    "grok-4.6": "Grok 4.6",
    "gpt-oss-120b": "gpt-oss-120b",
    "qwen3-235b-a22b-instruct-2507": "Qwen 3 235B",
    "deepseek-r1-0528": "DeepSeek-R1",
    "glm-5": "GLM-5",
}
TASKS = [("pairs", "vision"), ("solo", "vision"), ("pairs", "text"), ("solo", "text")]
TASK_LABEL = {("pairs", "vision"): "Pairs\nscreenshots", ("solo", "vision"): "Single page\nscreenshot",
              ("pairs", "text"): "Pairs\ntext", ("solo", "text"): "Single page\ntext"}
CAT_LABEL = {
    "missing_cta": "missing\nbutton", "hidden_price": "hidden\nprice", "contradiction": "contra-\ndiction",
    "vague_headline": "vague\nheadline", "typos": "typos", "placeholder_text": "placeholder\ntext",
    "blocking_popup": "blocking\npopup", "low_contrast": "low\ncontrast", "broken_image": "broken\nimage",
    "cut_off_text": "cut-off\ntext",
}
BLUE, ORANGE, GREY, RED = "#2f6db5", "#e08a2b", "#8a94a6", "#b03030"
plt.rcParams.update({"font.family": "DejaVu Sans", "axes.spines.top": False, "axes.spines.right": False})


def name(model):
    return NAMES.get(model, model)


def index(rows):
    return {(r["model"], r["task"], r["mode"]): r["metrics"] for r in rows}


def detection(m, task):
    return m["named_both_rate"] if task == "pairs" else m["strict_detection_rate"]


def cat_rate(m, task, cats):
    field = "named_both" if task == "pairs" else "strict"
    n = sum(m["per_category"].get(c, {}).get("n", 0) for c in cats)
    hit = sum(m["per_category"].get(c, {}).get(field, 0) for c in cats)
    return hit / n if n else np.nan


def model_order(rows):
    """Models sorted by their mean Kaggle score over the tasks they ran (vision-capable first)."""
    got = index(rows)
    models = sorted({r["model"] for r in rows})
    def key(mo):
        scores = [got[(mo, t, md)]["score"] for t, md in TASKS if (mo, t, md) in got]
        has_vision = any((mo, t, "vision") in got for t in ("pairs", "solo"))
        return (not has_vision, -np.mean(scores))
    return sorted(models, key=key)


def chart_scores(rows, path):
    got = index(rows)
    models = model_order(rows)
    mat = np.array([[got[(mo, t, md)]["score"] if (mo, t, md) in got else np.nan for t, md in TASKS] for mo in models])
    fig, ax = plt.subplots(figsize=(7.6, 0.42 * len(models) + 1.6))
    ax.imshow(mat, cmap="RdYlGn", vmin=0, vmax=1, aspect="auto")
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            v = mat[i, j]
            ax.text(j, i, "not run" if np.isnan(v) else f"{v:.2f}", ha="center", va="center",
                    fontsize=9, color=GREY if np.isnan(v) else "black")
    ax.set_xticks(range(len(TASKS)), [TASK_LABEL[t] for t in TASKS], fontsize=9)
    ax.xaxis.tick_top()
    ax.set_yticks(range(len(models)), [name(m) for m in models], fontsize=10)
    ax.tick_params(length=0)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_title("Kaggle task scores (0 to 1). Text-only models ran the two text tasks.", fontsize=10, pad=34)
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def chart_categories(rows, path, mode, cats, text_visible):
    """Defects caught per category: single-page task and pairs task side by side."""
    got = index(rows)
    models = [m for m in model_order(rows) if (m, "solo", mode) in got or (m, "pairs", mode) in got]
    fig, axes = plt.subplots(1, 2, figsize=(14, 0.42 * len(models) + 2.0), sharey=True)
    for ax, task, title in zip(axes, ("solo", "pairs"),
                               ("Single page: defect flagged on the twin, not on the original",
                                "Pairs: defect picked and named in both orders")):
        field = "named_both" if task == "pairs" else "strict"
        mat = np.array([[got[(mo, task, mode)]["per_category"][c][field] / got[(mo, task, mode)]["per_category"][c]["n"]
                         if (mo, task, mode) in got else np.nan for c in cats] for mo in models])
        ax.imshow(mat, cmap="RdYlGn", vmin=0, vmax=1, aspect="auto")
        for i in range(mat.shape[0]):
            for j in range(mat.shape[1]):
                v = mat[i, j]
                ax.text(j, i, "" if np.isnan(v) else f"{round(v * 10)}", ha="center", va="center", fontsize=9)
        ax.set_xticks(range(len(cats)), [CAT_LABEL[c] for c in cats], fontsize=8.5)
        for j, c in enumerate(cats):
            if c not in text_visible:
                ax.get_xticklabels()[j].set_color(RED)
        ax.set_yticks(range(len(models)), [name(m) for m in models], fontsize=10)
        ax.tick_params(length=0)
        for s in ax.spines.values():
            s.set_visible(False)
        ax.set_title(title, fontsize=10)
    view = "screenshots" if mode == "vision" else "text view"
    fig.suptitle(f"Defects caught out of 10 per category, {view}"
                 + (" (red: not visible in the text view)" if mode == "vision" else
                    " (red: invisible in the text view by construction)"), fontsize=11)
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def chart_dumbbell(rows, path, pairs_of, labels, title, xlabel):
    """One row per model, two dots (for example screenshot vs text) joined by a line."""
    data = []
    for mo in model_order(rows):
        a, b = pairs_of(mo)
        if a is not None and b is not None and not (np.isnan(a) or np.isnan(b)):
            data.append((mo, a, b))
    if not data:
        return
    fig, ax = plt.subplots(figsize=(7.4, 0.42 * len(data) + 1.5))
    for i, (mo, a, b) in enumerate(data):
        ax.plot([a, b], [i, i], color="#c9ced8", lw=3, zorder=1)
        ax.scatter([a], [i], color=BLUE, s=60, zorder=2, label=labels[0] if i == 0 else None)
        ax.scatter([b], [i], color=ORANGE, s=60, zorder=2, label=labels[1] if i == 0 else None)
        ax.text(a, i + 0.32, f"{a:.0%}", ha="center", fontsize=8, color=BLUE)
        ax.text(b, i - 0.42, f"{b:.0%}", ha="center", fontsize=8, color=ORANGE)
    ax.set_yticks(range(len(data)), [name(d[0]) for d in data], fontsize=10)
    ax.set_ylim(-0.8, len(data) - 0.3)
    ax.invert_yaxis()
    ax.set_xlim(-0.03, 1.03)
    ax.xaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))
    ax.set_xlabel(xlabel, fontsize=9)
    ax.set_title(title, fontsize=10)
    ax.legend(fontsize=8, loc="lower center", bbox_to_anchor=(0.5, 1.02 + 0.6 / max(len(data), 1)), ncol=2, frameon=False)
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def chart_false_alarms(rows, path):
    got = index(rows)
    fig, ax = plt.subplots(figsize=(7.6, 5.2))
    for mode, color, marker in (("vision", BLUE, "o"), ("text", ORANGE, "s")):
        for mo in model_order(rows):
            m = got.get((mo, "solo", mode))
            if not m:
                continue
            x, y = m["strict_detection_rate"], m["clean_pages_with_any_flag"]
            ax.scatter([x], [y], color=color, marker=marker, s=55, zorder=2)
            ax.annotate(name(mo), (x, y), textcoords="offset points", xytext=(5, 4), fontsize=7.5, color=color)
    ax.scatter([], [], color=BLUE, marker="o", label="screenshot")
    ax.scatter([], [], color=ORANGE, marker="s", label="text view")
    ax.set_xlim(-0.03, 1.03)
    ax.set_ylim(-0.03, 1.03)
    ax.xaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))
    ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))
    ax.set_xlabel("Twins caught (defect flagged, original not flagged for it)", fontsize=9)
    ax.set_ylabel("Clean pages flagged with at least one problem", fontsize=9)
    ax.set_title("Single-page task: catching defects vs crying wolf (bottom right is best)", fontsize=10)
    ax.legend(fontsize=8, frameon=False)
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def facts(rows, cats, text_visible):
    """Numbers quoted in the write-up, computed in one place."""
    got = index(rows)
    visual = [c for c in cats if c not in text_visible]
    tv = [c for c in cats if c in text_visible]
    out = {"models": {}, "categories": {}}
    for mo in model_order(rows):
        d = {"name": name(mo)}
        for task, mode in TASKS:
            m = got.get((mo, task, mode))
            if not m:
                continue
            k = f"{task}_{mode}"
            d[k] = {"score": m["score"], "caught": round(detection(m, task), 4),
                    "caught_text_visible": round(cat_rate(m, task, tv), 4),
                    "caught_visual_only": round(cat_rate(m, task, visual), 4), "invalid": m["invalid_answers"]}
            if task == "pairs":
                d[k].update(controls=m["control_pass_rate"], identical=m["identical_pass_rate"],
                            harmless=m["harmless_pass_rate"], share_A=m["share_of_picks_for_A"],
                            picked_both=m["picked_both_rate"], one_order_only=m["picked_one_order_only_rate"],
                            said_same_both=m["said_same_both_rate"], wrong_labels=m["wrong_label_counts"])
            else:
                d[k].update(clean_flagged=m["clean_pages_with_any_flag"], flagged=m["flagged_rate"],
                            score_drop=m["score_drop_rate"], mean_score_clean=m["mean_score_clean"],
                            mean_score_twin=m["mean_score_twin"], false_flags=m["false_flags_on_clean_pages"])
        out["models"][mo] = d
    for task, mode in TASKS:
        field = "named_both" if task == "pairs" else "strict"
        per = {}
        for c in cats:
            ms = [got[k] for k in got if k[1] == task and k[2] == mode]
            n = sum(m["per_category"][c]["n"] for m in ms)
            per[c] = {"caught": sum(m["per_category"][c][field] for m in ms), "of": n, "models": len(ms)}
        out["categories"][f"{task}_{mode}"] = per
    return out


def draw_all(rows, charts_dir, cats, text_visible, results_dir):
    cats = [c for c in cats if c in text_visible] + [c for c in cats if c not in text_visible]
    chart_scores(rows, charts_dir / "kaggle_scores.png")
    chart_categories(rows, charts_dir / "kaggle_categories_vision.png", "vision", cats, text_visible)
    chart_categories(rows, charts_dir / "kaggle_categories_text.png", "text", cats, text_visible)
    got = index(rows)
    tv = [c for c in cats if c in text_visible]

    def seeing_vs_reading(mo):
        a, b = got.get((mo, "solo", "vision")), got.get((mo, "solo", "text"))
        return (cat_rate(a, "solo", tv) if a else None, cat_rate(b, "solo", tv) if b else None)

    chart_dumbbell(rows, charts_dir / "kaggle_seeing_vs_reading.png", seeing_vs_reading,
                   ("screenshot", "text view"),
                   "Single page, the 7 defects that are visible in both views:\nscreenshot vs text view",
                   "Twins caught")

    def pairs_vs_solo(mo):
        a, b = got.get((mo, "pairs", "vision")), got.get((mo, "solo", "vision"))
        return (detection(a, "pairs") if a else None, detection(b, "solo") if b else None)

    chart_dumbbell(rows, charts_dir / "kaggle_pairs_vs_solo.png", pairs_vs_solo,
                   ("with the original to compare (pairs)", "page alone (single page)"),
                   "Screenshots, all 10 defects: comparing two versions vs judging one page",
                   "Defects caught")
    chart_false_alarms(rows, charts_dir / "kaggle_false_alarms.png")
    f = facts(rows, cats, text_visible)
    (results_dir / "facts.json").write_text(json.dumps(f, indent=1), encoding="utf-8")
    return f
