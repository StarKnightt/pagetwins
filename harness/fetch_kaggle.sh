#!/usr/bin/env bash
# Download completed Kaggle runs for the four PageTwins tasks and keep only the
# records CSV and the main result file of each run (full runs embed every
# screenshot and are about 85 MB each).
cd "$(dirname "$0")/.." && source .venv/Scripts/activate
export PYTHONIOENCODING=utf-8 PYTHONUTF8=1
for t in pagetwins-solo-vision pagetwins-pairs-vision pagetwins-pairs-text pagetwins-solo-textview; do
  kaggle b t download "$t" -o results/kaggle_raw 2>&1 | grep -E "Done|Skipp|rror" | tail -2
  find results/kaggle_raw/"$t" -type f ! -name "*_records.csv" ! -name "pagetwins-*-run_id_*.result.json" -delete 2>/dev/null
  find results/kaggle_raw/"$t" -type f -name "pagetwins-*-item-*" -delete 2>/dev/null
done
du -sh results/kaggle_raw
