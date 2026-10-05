"""Run the PageTwins tasks locally against Groq models, through the same
kaggle-benchmarks task functions that run on Kaggle.

    python harness/run_local.py --model openai/gpt-oss-120b --task pairs --mode text
    python harness/run_local.py --model qwen/qwen3.8-27b --task solo --mode vision --bases B01,B05

Answers are appended to results/local/<model>/<task>_<mode>.jsonl as they
arrive, so an interrupted run resumes where it stopped. The API key is read
from GROQ_API_KEY or from an env file and is never printed.
"""

import argparse
import json
import os
import re
import sys
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
os.environ.setdefault("PAGETWINS_DATA", str(ROOT / "dataset"))
os.environ.setdefault("BENCHMARK_CONSOLE_QUIET", "true")
os.environ.setdefault("BENCHMARK_CONSOLE_COLOR", "false")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, str(Path(__file__).resolve().parent))

import httpx  # noqa: E402
import kaggle_benchmarks as kbench  # noqa: E402
import openai  # noqa: E402
from kaggle_benchmarks.actors.llms import OpenAI as KBenchOpenAI  # noqa: E402

import pagetwins_core as core  # noqa: E402

if kbench.config.ui_handler is not None:  # the terminal transcript printer echoes every prompt
    kbench.events.manager.unbind(kbench.config.ui_handler)
    kbench.config.ui_handler = None

ENV_FILE = Path(r"C:\Code\hackathon\paypal\shipgrade\.env.local")
GROQ_URL = "https://api.groq.com/openai/v1"


def groq_key():
    if os.environ.get("GROQ_API_KEY"):
        return os.environ["GROQ_API_KEY"]
    for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        if line.strip().startswith("GROQ_API_KEY="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("GROQ_API_KEY not found")


def _seconds(s):
    """Parse Groq reset strings like '7.66s', '1m2.5s' or '120ms'."""
    if not s:
        return 0.0
    total = 0.0
    for num, unit in re.findall(r"([\d.]+)(ms|h|m|s)", s):
        total += float(num) * {"ms": 0.001, "s": 1, "m": 60, "h": 3600}[unit]
    return total


class Limiter:
    """Waits before a request when the per-minute token budget is nearly spent."""

    def __init__(self, need_tokens):
        self.need = need_tokens
        self.next_ok = 0.0
        self.remaining_requests = None
        self.lock = threading.Lock()

    def before(self, request):
        wait = self.next_ok - time.time()
        if wait > 0:
            time.sleep(wait)

    def after(self, response):
        h = response.headers
        with self.lock:
            if h.get("x-ratelimit-remaining-requests"):
                self.remaining_requests = int(h["x-ratelimit-remaining-requests"])
            rem = h.get("x-ratelimit-remaining-tokens")
            if rem is not None and int(rem) < self.need:
                self.next_ok = time.time() + _seconds(h.get("x-ratelimit-reset-tokens")) + 0.5
            if response.status_code == 429:
                self.next_ok = time.time() + float(h.get("retry-after", "10")) + 1


def make_llm(model, need_tokens):
    limiter = Limiter(need_tokens)
    http = httpx.Client(timeout=180, event_hooks={"request": [limiter.before], "response": [limiter.after]})
    client = openai.OpenAI(api_key=groq_key(), base_url=GROQ_URL, max_retries=8, http_client=http)
    # Mirrors how Kaggle's Model Proxy wraps OpenAI-compatible models:
    # no native structured outputs, provider-default temperature.
    llm = KBenchOpenAI(client, model, support_structured_outputs=False, support_temperature=False)
    llm.stream_responses = False
    return llm, limiter


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--task", choices=["pairs", "solo"], required=True)
    ap.add_argument("--mode", choices=["vision", "text"], required=True)
    ap.add_argument("--bases", default="", help="comma-separated base ids to limit the run, e.g. B01,B05")
    ap.add_argument("--out", default=str(ROOT / "results" / "local"))
    ap.add_argument("--tag", default="", help="suffix for the output file, e.g. a prompt version")
    args = ap.parse_args()

    need = {("pairs", "vision"): 3200, ("pairs", "text"): 4500,
            ("solo", "vision"): 2200, ("solo", "text"): 2800}[(args.task, args.mode)]
    llm, limiter = make_llm(args.model, need)

    if args.task == "pairs":
        df = core.pair_rows(args.mode)
        key_cols, item = ["pair_id", "order"], core.pair_item
        if args.bases:
            df = df[df.pair_id.str.split("-").str[0].isin(args.bases.split(","))]
    else:
        df = core.solo_rows(args.mode)
        key_cols, item = ["page_id"], core.solo_item
        if args.bases:
            df = df[df.base_id.isin(args.bases.split(","))]
    object.__setattr__(item, "store_run", False)  # JSONL below is the local record; run files embed the screenshots

    out_dir = Path(args.out) / args.model.replace("/", "__")
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{args.task}_{args.mode}{args.tag}.jsonl"
    done = set()
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            r = json.loads(line)
            if r.get("valid") or not str(r.get("raw", "")).startswith("ERROR"):
                done.add(tuple(r[k] for k in key_cols))

    todo = [r for r in df.to_dict("records") if tuple(r[k] for k in key_cols) not in done]
    print(f"{args.model} {args.task}/{args.mode}: {len(df)} items, {len(todo)} to run -> {path}", flush=True)
    t0 = time.time()
    with open(path, "a", encoding="utf-8") as f:
        for i, row in enumerate(todo):
            if limiter.remaining_requests is not None and limiter.remaining_requests < 5:
                print("Daily request limit nearly reached; stopping. Re-run later to resume.", flush=True)
                break
            start = time.time()
            try:
                while True:
                    try:
                        run = item.run(llm=llm, **row)
                        break
                    except openai.RateLimitError as e:
                        m = re.search(r"per day.*?try again in ([\dhms.]+)", str(e), re.S)
                        if not m:
                            raise
                        wait = _seconds(m.group(1)) + 5
                        print(f"  daily token limit reached; waiting {wait / 60:.1f} min", flush=True)
                        time.sleep(wait)
                        start = time.time()
                res = run.result if isinstance(run.result, dict) else None
                if res is None:
                    raise RuntimeError(getattr(run, "error_message", "task failed"))
            except Exception as e:  # recorded, and retried on the next invocation
                res = {k: row[k] for k in row if k != "mode"}
                res.update(valid=False, better="invalid", problem="invalid", problems=[], score=None,
                           evidence="", raw=f"ERROR: {type(e).__name__}: {str(e)[:300]}")
            res["model"] = args.model
            res["mode"] = args.mode
            res["latency_s"] = round(time.time() - start, 2)
            f.write(json.dumps(res) + "\n")
            f.flush()
            if (i + 1) % 10 == 0 or i == len(todo) - 1:
                el = time.time() - t0
                print(f"  {i + 1}/{len(todo)} in {el / 60:.1f} min, requests left today: "
                      f"{limiter.remaining_requests}", flush=True)


if __name__ == "__main__":
    main()
