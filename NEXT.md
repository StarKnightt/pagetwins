# PageTwins: next steps

Deadline: Mon Oct 12, 2026, 12:29 PM IST. Target: benchmark live on Kaggle and post drafted by Sat Oct 10.

## Status

- Dataset built and verified: 120 pages, 100 one-defect pairs across 10 categories, 20 controls (`dataset/`, CC BY 4.0, with data card).
- Four Kaggle task files generated in `kaggle_tasks/` (`pagetwins-pairs-vision`, `pagetwins-pairs-text`, `pagetwins-solo-vision`, `pagetwins-solo-text`). Two were validated end to end per Kaggle's official skill (run the file, confirm a `.run.json` with a numeric result and assertions); the other two share the same code path.
- Local pilot on Groq running in the background on 3 of the 10 bases (Groq's free tier allows about 200,000 tokens per model per day): gpt-oss-120b and gpt-oss-20b (text), Qwen 3.8 27B (screenshots and text).
- Kaggle CLI 2.2.4 is installed in `.venv`, but it has no credentials yet.

## What the owner needs to do

1. **Create a Kaggle API token** (the CLI needs it to upload the dataset and push and run tasks):
   - kaggle.com, profile picture, **Settings**, section **API**, click **Create New Token**.
   - A file `kaggle.json` downloads. Move it to `C:\Users\prase\.kaggle\kaggle.json` (create the `.kaggle` folder if needed).
   - Do not paste the token into chat. I will only check that the file exists and run `kaggle` commands.
2. **Tell me your Kaggle username** (it goes into the dataset id `<username>/pagetwins`).
3. **Approve the Kaggle plan below with one "go"**. Kaggle's official benchmark skill asks for one confirmation before chaining push, run and publish steps. You can also approve only part of it, for example "go, but keep everything private".
4. **Later approvals** (I will ask when we get there):
   - making the dataset, the four tasks and the benchmark public (required for the DEV post link),
   - creating the public GitHub repo `StarKnightt/pagetwins` and pushing this folder,
   - publishing the DEV post (only needed if a placeholder remains).

## What I will do after "go"

Each step's output is checked before the next one starts; on an error I stop and report.

1. Put the username into `dataset/dataset-metadata.json`, then `kaggle d create -p dataset -r zip` (private at first; `-r zip` is needed or the `pages/` folder is skipped), then `kaggle d status <user>/pagetwins` until ready, and `kaggle d files` to confirm all 120 page folders arrived.
2. `kaggle b init -y` in a scratch folder outside the repo (it writes a short-lived Model Proxy key to `.env`, which is gitignored and never printed).
3. Validate against Kaggle's proxy on one base page: `PAGETWINS_BASES=B01 python kaggle_tasks/pagetwins-solo-text.py` and confirm the `.run.json`.
4. Push the four tasks, each with the dataset attached:
   `kaggle b t push pagetwins-pairs-vision -f kaggle_tasks/pagetwins-pairs-vision.py -d <user>/pagetwins --wait` (and the same for the other three).
5. Smoke run one task on one model: `kaggle b t run pagetwins-solo-text -m gemini-3.5-flash --wait`, then `kaggle b t status` and `kaggle b t log`.
6. Full runs: `kaggle b t models` to get the exact list, then run the screenshot tasks on every vision model and the text tasks on every model (repeated `-m` flags), polling `status`.
7. `kaggle b t download <task> -o results/kaggle_raw` for each task, then `python harness/analyze.py --kaggle results/kaggle_raw` for tables and charts.
8. In a **new tab** of your Chrome (through the `user-chrome` MCP DOM tools, never your existing tabs and never screen control): create the benchmark "PageTwins" at kaggle.com/benchmarks, add the four tasks and the models, and copy the public link for the post. The CLI cannot create benchmarks.
9. After your OK on publishing: `kaggle b t publish <task>` for the four tasks, and make the dataset public.

If you would rather not create an API token, I can do steps 1, 4 and 8 through the Kaggle web UI in a new Chrome tab instead (upload `dataset/` as a zip, create each task as a task notebook by pasting the generated file). Running across many models is slower that way.

## Then

- Fill `POST.md` (exact challenge template) with the Kaggle numbers and charts, and keep the Groq pilot as a secondary section.
- Final check: no em dashes, no placeholders, every number traceable to `results/*/summary.json`.
