import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

csv_path = Path("data") / "sample_multi_month.csv"
if not csv_path.exists():
   raise FileNotFoundError("data/sample_multi_month.csv yok. Önce analysis.py ile multi-month sample üretmelisin.")

print("Kullanılan dosya:", csv_path)
df = pd.read_csv(csv_path)

print("Satır:", len(df), "Sütun:", len(df.columns))
print(df.head())

Path("outputs").mkdir(exist_ok=True)

# 1) dep_delay histogram
series = pd.to_numeric(df["dep_delay"], errors="coerce").dropna()
plt.figure()
plt.hist(series, bins=60)
plt.title("Departure delay distribution (dep_delay)")
plt.xlabel("Minutes")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig(Path("outputs") / "dep_delay_hist.png")
print("Kaydedildi: outputs/dep_delay_hist.png")

# 2) ortalama gecikme - haftanın günü
group = df.groupby("day_of_week")["dep_delay"].mean()
plt.figure()
plt.plot(group.index, group.values, marker="o")
plt.title("Average dep_delay by day_of_week")
plt.xlabel("day_of_week (1=Mon ... 7=Sun)")
plt.ylabel("Avg dep_delay (min)")
plt.tight_layout()
plt.savefig(Path("outputs") / "avg_delay_by_dayofweek.png")
print("Kaydedildi: outputs/avg_delay_by_dayofweek.png")