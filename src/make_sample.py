"""Export a small cleaned CSV the deployed dashboard can read.

Run once locally:
    python src/make_sample.py
Creates data/processed/transactions_sample.csv (committed to git).
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))
from data_prep import clean_transactions  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "online_retail_II.xlsx"
OUT = ROOT / "data" / "processed" / "transactions_sample.csv"

raw = pd.read_excel(RAW, sheet_name=None)
df = clean_transactions(pd.concat(raw.values(), ignore_index=True))

# Sample to keep the file small & fast for the cloud (keeps every customer's rows
# light while staying representative). Adjust frac if you want more/less.
sample = df.sample(frac=0.15, random_state=42).sort_values("invoice_date")
OUT.parent.mkdir(parents=True, exist_ok=True)
sample.to_csv(OUT, index=False)
print(f"Wrote {len(sample):,} rows to {OUT} ({OUT.stat().st_size/1e6:.1f} MB)")
