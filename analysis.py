import pandas as pd

PATH = "data/sample.csv"

df = pd.read_csv(PATH, low_memory=False)
print("Rows, Cols:", df.shape)

print("\nMissing values (top 10):")
print(df.isna().sum().sort_values(ascending=False).head(10))

df["fl_date"] = pd.to_datetime(df["fl_date"], errors="coerce")
df["dep_delay"] = pd.to_numeric(df["dep_delay"], errors="coerce")
df = df.dropna(subset=["dep_delay"])

on_time_rate = (df["dep_delay"] <= 15).mean()
print("\nOn-time rate (dep_delay <= 15):", round(on_time_rate * 100, 2), "%")

origin_stats = (
    df.groupby("origin")
      .agg(n=("dep_delay", "size"), avg_dep_delay=("dep_delay", "mean"))
      .query("n >= 200")
      .sort_values("avg_dep_delay", ascending=False)
      .head(10)
)
print("\nWorst origins (avg dep_delay, n>=200):")
print(origin_stats)

carrier_stats = (
    df.groupby("op_unique_carrier")
      .agg(n=("dep_delay", "size"), avg_dep_delay=("dep_delay", "mean"))
      .query("n >= 200")
      .sort_values("avg_dep_delay", ascending=False)
      .head(10)
)
print("\nWorst carriers (avg dep_delay, n>=200):")
print(carrier_stats)

monthly = (
    df.groupby(df["fl_date"].dt.month)["dep_delay"]
      .mean()
      .rename("avg_dep_delay")
)
print("\nAvg dep_delay by month:")
print(monthly)