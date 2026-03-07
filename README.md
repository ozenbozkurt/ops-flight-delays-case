# Flight Delay Operations Intelligence

A reproducible aviation analytics case study that identifies operational delay patterns, route risk, carrier volatility, and actionable mitigation priorities using U.S. 2024 flight data.

## Why this project matters

Flight delays are not just passenger inconvenience metrics. They are operational signals tied to route fragility, carrier performance variability, airport congestion, and downstream disruption risk.

This project turns raw delay data into decision-oriented insights for operations, performance, and planning teams.

## Key questions

- Which months show the highest operational delay burden?
- Which origins and carriers underperform consistently?
- Which routes show elevated disruption risk?
- What proportion of delay burden comes from each delay reason?
- Which interventions would likely reduce late departures most effectively?

## Tools used

- Python
- pandas
- matplotlib
- PowerShell
- CSV-based reproducible pipeline

## Run locally

Run the full pipeline:

```powershell
powershell -ExecutionPolicy Bypass -File .\run.ps1
