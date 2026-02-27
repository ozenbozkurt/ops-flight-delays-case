# Ops Flight Delays Case — Executive Summary

## Goal
Analyze U.S. flight delay patterns and translate findings into operational actions: where delays concentrate, which routes are risky, which delay reasons dominate, and what to prioritize.

## Data & Approach
- Source: 2024 flight records (sampled across 12 months).
- Pipeline (one command): generates a multi-month sample and runs EDA + ops analysis + plots.

## Key Findings (from outputs)
1) **On-time performance:** ~**80.04%** overall (ON_TIME_OVERALL_PCT).
2) **Seasonality / worst month:** **2024-07** is the worst month:
   - EDA worst month metric: **22.67**
   - Ops late-rate worst month: **29.4% late rate**
3) **Top delay driver:** **late_aircraft_delay** is the dominant reason (~**41.98% share**).
4) **Highest-risk route:** **SFO–LAX**
   - late_rate_pct **28.77%**
   - avg_delay **15.93** minutes
5) Concentration indicators:
   - Top origin: **MIA** (22.2)
   - Top carrier: **AA** (20.44)

## Operational Recommendations (actionable)
### A) Attack the #1 delay driver: late_aircraft_delay
- Introduce tighter aircraft rotation buffers on critical turns (especially peak months).
- Pre-position spare aircraft / crews on high-risk hubs during summer peaks.
- Improve turnaround predictability: gate staffing, pushback coordination, ground services SLA.

### B) Seasonal playbook for July
- Treat July as “surge ops”: add buffer capacity, increase dispatch readiness, and prioritize on-time critical legs.
- Re-rank routes by late-rate for July and allocate contingency resources accordingly.

### C) Route-level risk management: SFO–LAX
- Flag SFO–LAX as a monitoring route: real-time late-rate tracking, proactive swaps, and tighter connection management.
- If constraints exist (slots, gate), adjust schedule padding for this lane only (avoid blanket padding everywhere).

## Artifacts Produced
- CSVs:
  - `outputs/by_month_metrics.csv`
  - `outputs/worst_origins.csv`
  - `outputs/worst_carriers.csv`
  - `outputs/top_risky_routes.csv`
  - `outputs/delay_reason_share.csv`
- Plots:
  - `outputs/avg_delay_by_month.png`
  - `outputs/late_rate_by_month.png`
  - `outputs/dep_delay_hist.png`
  - `outputs/avg_delay_by_dayofweek.png`

## How to Run
```powershell
powershell -ExecutionPolicy Bypass -File .\run.ps1