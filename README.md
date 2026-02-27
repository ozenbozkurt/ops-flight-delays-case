# Flight Delay Ops Case

## Goal
Quick exploratory analysis of flight departure delays.

## What's inside
- `main.py`: loads `data/sample.csv` and generates charts
- `outputs/dep_delay_hist.png`: departure delay distribution
- `outputs/avg_delay_by_dayofweek.png`: avg dep_delay by day of week

## How to run (Windows)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install pandas matplotlib scikit-learn
python main.py
```
## Notes
- Dataset is sampled (200k rows) for fast iteration.
## Findings (Sample - 200k rows, Jan 1–12 only)
- This sample covers **only January 1–12** (not full-year), so no seasonality claims.
- Next step: sample across multiple months or stratified sampling to compare month-to-month delays.
## Findings (Sample - 200k rows)
- On-time rate (dep_delay <= 15): **X%**
- Worst origins (n>=200): **TOP_ORIGIN** had avg dep_delay **Y min**
- Worst carriers (n>=200): **TOP_CARRIER** had avg dep_delay **Z min**
- Seasonality: month with highest avg dep_delay was **M**