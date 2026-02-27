import os
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

DATA = Path("data") / "sample_multi_month.csv"
OUT = Path("outputs")
OUT.mkdir(exist_ok=True)

MIN_N = 500  # noise filtre

df = pd.read_csv(DATA, low_memory=False)

# types
df["fl_date"] = pd.to_datetime(df["fl_date"], errors="coerce")
df["dep_delay"] = pd.to_numeric(df["dep_delay"], errors="coerce")

df = df.dropna(subset=["dep_delay", "fl_date"])

# --- Metrics ---
on_time_overall = (df["dep_delay"] <= 15).mean()

by_month = (
    df.assign(month=df["fl_date"].dt.to_period("M").astype(str))
      .groupby("month")
      .agg(
          n=("dep_delay", "size"),
          avg_dep_delay=("dep_delay", "mean"),
          on_time_rate=("dep_delay", lambda s: (s <= 15).mean()),
      )
      .sort_index()
)

# worst origins / carriers (avg delay) with min n
worst_origins = (
    df.groupby("origin")
      .agg(n=("dep_delay", "size"), avg_dep_delay=("dep_delay", "mean"))
      .query("n >= @MIN_N")
      .sort_values("avg_dep_delay", ascending=False)
      .head(15)
)

worst_carriers = (
    df.groupby("op_unique_carrier")
      .agg(n=("dep_delay", "size"), avg_dep_delay=("dep_delay", "mean"))
      .query("n >= @MIN_N")
      .sort_values("avg_dep_delay", ascending=False)
      .head(15)
)

# --- Save tables ---
by_month.to_csv(OUT / "by_month_metrics.csv")
worst_origins.to_csv(OUT / "worst_origins.csv")
worst_carriers.to_csv(OUT / "worst_carriers.csv")

# --- Plot avg delay by month ---
plt.figure()
plt.plot(by_month.index, by_month["avg_dep_delay"], marker="o")
plt.xticks(rotation=45, ha="right")
plt.xlabel("Month")
plt.ylabel("Avg dep_delay (min)")
plt.title("Average Departure Delay by Month (Sample)")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(OUT / "avg_delay_by_month.png", dpi=150)
plt.close()

# --- Print key summary for README ---
top_origin = worst_origins.index[0]
top_origin_delay = float(worst_origins.iloc[0]["avg_dep_delay"])
top_carrier = worst_carriers.index[0]
top_carrier_delay = float(worst_carriers.iloc[0]["avg_dep_delay"])

worst_month = by_month["avg_dep_delay"].idxmax()
worst_month_delay = float(by_month.loc[worst_month, "avg_dep_delay"])

print("ON_TIME_OVERALL_PCT", round(on_time_overall * 100, 2))
print("TOP_ORIGIN", top_origin, round(top_origin_delay, 2))
print("TOP_CARRIER", top_carrier, round(top_carrier_delay, 2))
print("WORST_MONTH", worst_month, round(worst_month_delay, 2))
print("Saved:",
      "outputs/by_month_metrics.csv, outputs/worst_origins.csv, outputs/worst_carriers.csv, outputs/avg_delay_by_month.png")