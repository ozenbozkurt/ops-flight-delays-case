import pandas as pd
from pathlib import Path

DATA_DIR = Path("data")

csv_files = list(DATA_DIR.glob("*.csv"))
if not csv_files:
    raise FileNotFoundError("data klasöründe .csv yok.")

big_csv = csv_files[0]
print("Büyük dosya:", big_csv)

# Büyük CSV'yi parça parça okuyup ilk 200,000 satırı alıyoruz
chunks = pd.read_csv(big_csv, chunksize=200_000)
df = next(chunks)

out_path = DATA_DIR / "sample.csv"
df.to_csv(out_path, index=False)

print("Sample yazıldı:", out_path, "satır:", len(df))
print("Sütun sayısı:", len(df.columns))
print("Sütun örnekleri:", list(df.columns)[:20])