"""Build the four self-contained Kaggle task files in kaggle_tasks/.

Each file is pagetwins_core.py plus one main task that ends with
`.run(kbench.llm)`, in jupytext percent format, ready for
`kaggle b t push <slug> -f kaggle_tasks/<slug>.py -d <owner>/pagetwins`.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORE = (ROOT / "harness" / "pagetwins_core.py").read_text(encoding="utf-8").rstrip() + "\n"

TASKS = {
    ("pairs", "vision"): "Two full-page screenshots of the same landing page; one may carry a single defect. "
                         "Pick the version to ship and name the defect. Score: half defects found and named "
                         "in both orders, half controls answered 'same' in both orders.",
    ("pairs", "text"): "Same as the screenshot pairs, but each page is given as its visible text and element roles. "
                       "Three visual defect types are invisible in this view by construction.",
    ("solo", "vision"): "One full-page screenshot, no reference page. List problems from a fixed list and rate launch "
                        "readiness. Score: share of twins where the defect is flagged and the clean page is not.",
    ("solo", "text"): "Same as the screenshot solo task, but the page is given as its visible text and element roles.",
}

TEMPLATE = '''
# %% [markdown]
# ## Main task: {title}

# %%
@kbench.task(name="{slug}", description="{description}")
def {func}(llm) -> float:
    return _run_{task}(llm, "{mode}")


{func}.run(kbench.llm)
'''


def main():
    out = ROOT / "kaggle_tasks"
    out.mkdir(exist_ok=True)
    for (task, mode), description in TASKS.items():
        # the slug pagetwins-solo-text is taken by an empty task left by a failed push
        slug = "pagetwins-solo-textview" if (task, mode) == ("solo", "text") else f"pagetwins-{task}-{mode}"
        body = TEMPLATE.format(title=f"{task} ({mode})", slug=slug, description=description,
                               func=slug.replace("-", "_"), task=task, mode=mode)
        (out / f"{slug}.py").write_text(CORE + body, encoding="utf-8")
        print("wrote", out / f"{slug}.py")


if __name__ == "__main__":
    main()
