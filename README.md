# PageTwins

A Kaggle benchmark that asks: when a landing page breaks in one specific way,
does an AI grader notice, name the problem, and leave a clean page alone?

10 original landing pages each get 10 "evil twins" with exactly one labeled
defect (missing call to action, hidden price, contradiction, vague headline,
typos, placeholder text, blocking popup, low contrast, broken image, cut-off
text), plus an identical copy and a harmlessly changed copy as controls.

## Layout

- `generator/`: builds the dataset (content, SVG art, HTML templates, defect injection, rendering and verification).
- `dataset/`: the generated dataset (CC BY 4.0), with its own data card.
- `harness/pagetwins_core.py`: the benchmark logic (prompts, parsing, per-item tasks, scoring) for the `kaggle-benchmarks` SDK.
- `harness/make_tasks.py`: writes the four self-contained Kaggle task files to `kaggle_tasks/`.
- `harness/validate_task.py`: runs a task file unchanged against a Groq model on a one-page subset and checks that a run file was written.
- `harness/run_local.py`: the local pilot runner (Groq, rate limited, resumable JSONL output).
- `harness/analyze.py`: metrics and charts from local or Kaggle results.

## Tasks

| Task | Input | Score |
|---|---|---|
| `pagetwins-pairs-vision` | two full-page screenshots, shown in both orders | 0.5 x defects picked and named in both orders + 0.5 x controls answered "same" in both orders |
| `pagetwins-pairs-text` | the same pairs as visible text with element roles | same |
| `pagetwins-solo-vision` | one screenshot | share of twins where the defect is flagged and the clean base page is not |
| `pagetwins-solo-text` | one page as text | same |

## Reproduce

```bash
uv venv --python 3.12 && source .venv/Scripts/activate
uv pip install kaggle-benchmarks==0.6.1 kaggle playwright pillow pandas matplotlib numpy
python -m playwright install chromium

python generator/build.py          # rebuild dataset/ and verify every twin
python harness/make_tasks.py       # write kaggle_tasks/*.py

# local pilot (needs GROQ_API_KEY)
python harness/run_local.py --model openai/gpt-oss-120b --task pairs --mode text
python harness/analyze.py

# Kaggle
kaggle b t push pagetwins-pairs-vision -f kaggle_tasks/pagetwins-pairs-vision.py -d <user>/pagetwins --wait
kaggle b t run pagetwins-pairs-vision -m gemini-3.5-flash --wait
```

## License

Code: MIT. Dataset: CC BY 4.0. Prasenjit Nayak, 2026.
