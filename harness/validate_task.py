"""Validate a generated Kaggle task file end to end before pushing it.

Runs the file unchanged, with kbench.llm pointed at a Groq model and the data
limited to one base page, then checks that a *.run.json was written:

    python harness/validate_task.py kaggle_tasks/pagetwins-solo-text.py --model openai/gpt-oss-20b
"""

import argparse
import os
import runpy
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("task_file")
    ap.add_argument("--model", default="openai/gpt-oss-20b")
    ap.add_argument("--bases", default="B01")
    args = ap.parse_args()

    os.environ["PAGETWINS_BASES"] = args.bases
    os.environ["PAGETWINS_N_JOBS"] = "1"
    task_file = Path(args.task_file).resolve()
    work = Path(tempfile.mkdtemp(prefix="pagetwins_validate_"))
    os.environ["PAGETWINS_OUT"] = str(work)

    sys.argv = [sys.argv[0]]
    import run_local  # sets data path, console settings and the Groq client
    import kaggle_benchmarks as kbench

    mode = "vision" if "vision" in task_file.name else "text"
    task = "pairs" if "pairs" in task_file.name else "solo"
    need = {("pairs", "vision"): 3200, ("pairs", "text"): 4500,
            ("solo", "vision"): 2200, ("solo", "text"): 2800}[(task, mode)]
    kbench.llm, _ = run_local.make_llm(args.model, need)

    os.chdir(work)
    runpy.run_path(str(task_file), run_name="__main__")
    produced = sorted(p.name for p in work.glob("*.run.json"))
    main_runs = [p for p in produced if p.startswith(task_file.stem)]
    print(f"run files in {work}: {len(produced)} total, main task: {main_runs}")
    if not main_runs:
        raise SystemExit("FAIL: no run file for the main task")
    print("OK")


if __name__ == "__main__":
    main()
