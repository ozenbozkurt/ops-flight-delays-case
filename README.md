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