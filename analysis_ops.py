import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

DATA = Path("data") / "sample_multi_month.csv"
OUT = Path("outputs")
OUT.mkdir(exist_ok=True)

MIN_N_ROUTE = 300   # route bazında noise filtresi
LATE_THRESHOLD = 15 # dep_delay > 15 => late

df = pd.read_csv(DATA, low_memory=False)

df["fl_date"] = pd.to_datetime(df["fl_date"], errors="coerce")
df["dep_delay"] = pd.to_numeric(df["dep_delay"], errors="coerce")

reason_cols = ["carrier_delay", "weather_delay", "nas_delay", "security_delay", "late_aircraft_delay"]
for c in reason_cols:
    if c in df.columns:
        df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)
    else:
        df[c] = 0

df = df.dropna(subset=["fl_date", "dep_delay", "origin", "dest"])

df["late_flag"] = (df["dep_delay"] > LATE_THRESHOLD).astype(int)

df["route"] = df["origin"].astype(str) + "-" + df["dest"].astype(str)

routes = (
    df.groupby("route")
      .agg(
          n=("late_flag", "size"),
          late_rate=("late_flag", "mean"),
          avg_dep_delay=("dep_delay", "mean"),
          p90_dep_delay=("dep_delay", lambda s: s.quantile(0.90)),
      )
      .query("n >= @MIN_N_ROUTE")
      .sort_values(["late_rate", "avg_dep_delay"], ascending=False)
      .head(20)
)

routes.to_csv(OUT / "top_risky_routes.csv")

delayed = df[df["dep_delay"] > 0].copy()
reason_totals = delayed[reason_cols].sum()
reason_share = (reason_totals / reason_totals.sum()).rename("share").to_frame()
reason_share["minutes_total"] = reason_totals
reason_share = reason_share.sort_values("share", ascending=False)
reason_share.to_csv(OUT / "delay_reason_share.csv")

by_month = (
    df.assign(month=df["fl_date"].dt.to_period("M").astype(str))
      .groupby("month")
      .agg(n=("late_flag", "size"), late_rate=("late_flag", "mean"))
      .sort_index()
)

plt.figure()
plt.plot(by_month.index, by_month["late_rate"] * 100, marker="o")
plt.xticks(rotation=45, ha="right")
plt.xlabel("Month")
plt.ylabel("Late rate (%)  (dep_delay > 15)")
plt.title("Late Rate by Month (Sample)")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(OUT / "late_rate_by_month.png", dpi=150)
plt.close()

top_route = routes.index[0]
top_route_late = float(routes.iloc[0]["late_rate"]) * 100
top_route_avg = float(routes.iloc[0]["avg_dep_delay"])

top_reason = reason_share.index[0]
top_reason_share = float(reason_share.iloc[0]["share"]) * 100

worst_month = by_month["late_rate"].idxmax()
worst_month_late = float(by_month.loc[worst_month, "late_rate"]) * 100

print("TOP_ROUTE", top_route, "late_rate_pct", round(top_route_late, 2), "avg_delay", round(top_route_avg, 2))
print("TOP_REASON", top_reason, "share_pct", round(top_reason_share, 2))
print("WORST_MONTH_LATE", worst_month, "late_rate_pct", round(worst_month_late, 2))
print("Saved: outputs/top_risky_routes.csv, outputs/delay_reason_share.csv, outputs/late_rate_by_month.png")
