"""Validate a generated Kaggle task file end to end before pushing it.

Runs the file unchanged, with kbench.llm pointed at a Groq model (or at an
offline stand-in) and the data limited to one base page, then checks that a
*.run.json was written:

    python harness/validate_task.py kaggle_tasks/pagetwins-solo-textview.py --model openai/gpt-oss-20b
    python harness/validate_task.py kaggle_tasks/pagetwins-pairs-vision.py --offline 0.3

`--offline SHARE` answers every call with a fixed reply and makes that share of
first attempts fail with HTTP 503, which exercises the retry passes without
any API calls. `--offline-down` makes every call fail, which must end in the
partial-run refusal.
"""

import argparse
import hashlib
import json
import os
import random
import runpy
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def offline_llm(fail_share, always_fail=False):
    import httpx
    import openai
    from kaggle_benchmarks.actors.llms import OpenAI as KBenchOpenAI

    seen = set()

    def handler(request):
        text = json.dumps(json.loads(request.content)["messages"])
        key = hashlib.sha1(text.encode()).hexdigest()
        first = key not in seen
        seen.add(key)
        if always_fail or (first and random.random() < fail_share):
            return httpx.Response(503, json={"error": {"message": "offline stand-in: simulated outage"}})
        content = ('{"better": "same", "problem": "none", "evidence": "none"}' if "Page A" in text
                   else '{"problems": [], "score": 8, "evidence": "none"}')
        return httpx.Response(200, json={
            "id": "offline", "object": "chat.completion", "created": 0, "model": "offline/stand-in",
            "choices": [{"index": 0, "finish_reason": "stop", "message": {"role": "assistant", "content": content}}],
            "usage": {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15}})

    client = openai.OpenAI(api_key="offline", base_url="http://offline.invalid/v1", max_retries=0,
                           http_client=httpx.Client(transport=httpx.MockTransport(handler)))
    llm = KBenchOpenAI(client, "offline/stand-in", support_structured_outputs=False, support_temperature=False)
    llm.stream_responses = False
    return llm


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("task_file")
    ap.add_argument("--model", default="openai/gpt-oss-20b")
    ap.add_argument("--bases", default="B01")
    ap.add_argument("--offline", type=float, default=None, metavar="SHARE")
    ap.add_argument("--offline-down", action="store_true")
    args = ap.parse_args()

    os.environ["PAGETWINS_BASES"] = args.bases
    os.environ["PAGETWINS_N_JOBS"] = "1" if args.offline is None and not args.offline_down else "4"
    task_file = Path(args.task_file).resolve()
    work = Path(tempfile.mkdtemp(prefix="pagetwins_validate_"))
    os.environ["PAGETWINS_OUT"] = str(work)

    sys.argv = [sys.argv[0]]
    import run_local  # sets data path, console settings and the Groq client
    import kaggle_benchmarks as kbench

    if args.offline is not None or args.offline_down:
        kbench.llm = offline_llm(args.offline or 0.0, always_fail=args.offline_down)
    else:
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
