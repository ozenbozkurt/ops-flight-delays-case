@"
# Ops Flight Delays Case (2024)

A reproducible ops analytics case study on U.S. flight delays: multi-month sampling + EDA + operational risk insights + actionable recommendations.

## Quick Demo (Windows, one command)

Run the full pipeline:

    powershell -ExecutionPolicy Bypass -File .\run.ps1

After it finishes, open:
- `REPORT.md` — executive summary + operational recommendations
- `outputs/` — generated CSVs + charts

Fast mode (skip sample generation):

    powershell -ExecutionPolicy Bypass -File .\run.ps1 -SkipSampleGen

## What the pipeline does

`run.ps1` will:
1. Create `.venv` if missing
2. Install `requirements.txt`
3. Generate `data/sample_multi_month.csv` (if `ops-bigdata/flight_data_2024.csv` exists)
4. Run:
   - `analysis_eda.py`
   - `analysis_ops.py`
   - `main.py`
5. Write artifacts to `outputs/`

## Key Outputs

### CSVs
- `outputs/by_month_metrics.csv`
- `outputs/worst_origins.csv`
- `outputs/worst_carriers.csv`
- `outputs/top_risky_routes.csv`
- `outputs/delay_reason_share.csv`

### Charts (generated)
- `outputs/avg_delay_by_month.png`
- `outputs/late_rate_by_month.png`
- `outputs/dep_delay_hist.png`
- `outputs/avg_delay_by_dayofweek.png`

## Notes
- If `data/sample_multi_month.csv` is missing and the big dataset is not present under `ops-bigdata/`, the pipeline will fail fast with a clear error.
- Recommended entry point for reviewers: `REPORT.md`.
"@ | Set-Content -Encoding UTF8 README.md