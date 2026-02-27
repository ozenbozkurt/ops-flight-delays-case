import os
from pathlib import Path
import numpy as np
import pandas as pd

# ---------- Config ----------
RNG_SEED = 42
TARGET_PER_MONTH = 20000  # 12 * 20k = 240k rows approx
DATE_COL = "fl_date"

# Büyük dosya için olası path'ler (senin durumuna göre)
CANDIDATES = [
    Path("ops-bigdata") / "flight_data_2024.csv",                 # repo içinde olsaydı (ama değil)
    Path.home() / "Desktop" / "ops-bigdata" / "flight_data_2024.csv",
    Path.home() / "Masaüstü" / "ops-bigdata" / "flight_data_2024.csv",
]

def find_big_csv() -> Path:
    for p in CANDIDATES:
        if p.exists():
            return p
    raise FileNotFoundError(
        "flight_data_2024.csv bulunamadı. ops-bigdata klasörünün içinde olduğundan emin ol."
    )

def month_key_from_series(dt: pd.Series) -> pd.Series:
    # YYYY-MM format
    return dt.dt.to_period("M").astype(str)

def pass1_count_by_month(csv_path: Path, chunksize: int = 500_000) -> dict:
    counts = {}
    for chunk in pd.read_csv(csv_path, chunksize=chunksize, low_memory=False):
        if DATE_COL not in chunk.columns:
            raise KeyError(f"CSV içinde '{DATE_COL}' kolonu yok.")
        dt = pd.to_datetime(chunk[DATE_COL], errors="coerce")
        m = month_key_from_series(dt)
        vc = m.value_counts(dropna=True)
        for k, v in vc.items():
            counts[k] = counts.get(k, 0) + int(v)
    # "NaT" gibi bozukları istemiyoruz
    counts = {k: v for k, v in counts.items() if k != "NaT"}
    return counts

def pass2_sample(csv_path: Path, month_counts: dict, out_path: Path, chunksize: int = 300_000):
    rng = np.random.default_rng(RNG_SEED)

    # Her ay için hedef ve sampling olasılığı
    months = sorted(month_counts.keys())
    probs = {}
    for m in months:
        total = month_counts[m]
        # hedef/total oranı; 1'den büyük olamaz
        probs[m] = min(1.0, TARGET_PER_MONTH / max(1, total))

    buffers = {m: [] for m in months}

    for chunk in pd.read_csv(csv_path, chunksize=chunksize, low_memory=False):
        dt = pd.to_datetime(chunk[DATE_COL], errors="coerce")
        chunk = chunk.copy()
        chunk[DATE_COL] = dt
        chunk = chunk.dropna(subset=[DATE_COL])
        chunk["_month"] = month_key_from_series(chunk[DATE_COL])

        for m in months:
            sub = chunk[chunk["_month"] == m]
            if sub.empty:
                continue
            p = probs[m]
            # Bernoulli sample
            mask = rng.random(len(sub)) < p
            pick = sub.loc[mask].drop(columns=["_month"])
            if not pick.empty:
                buffers[m].append(pick)

    # Birleştir, her ayı TARGET_PER_MONTH’e kırp
    out_parts = []
    for m in months:
        if buffers[m]:
            dfm = pd.concat(buffers[m], ignore_index=True)
            if len(dfm) > TARGET_PER_MONTH:
                dfm = dfm.sample(n=TARGET_PER_MONTH, random_state=RNG_SEED)
            dfm["sample_month"] = m
            out_parts.append(dfm)

    if not out_parts:
        raise RuntimeError("Sample üretilemedi. CSV kolon adını ve tarih formatını kontrol et.")

    out_df = pd.concat(out_parts, ignore_index=True)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_df.to_csv(out_path, index=False)
    return out_df

def main():
    csv_path = find_big_csv()
    print(f"[OK] Big CSV: {csv_path}")

    month_counts = pass1_count_by_month(csv_path)
    print("[INFO] Month counts (top 5):", dict(list(sorted(month_counts.items()))[:5]))
    print("[INFO] Months found:", len(month_counts))

    out_path = Path("data") / "sample_multi_month.csv"
    out_df = pass2_sample(csv_path, month_counts, out_path)

    print(f"[DONE] Wrote: {out_path} rows={len(out_df)} months={out_df['sample_month'].nunique()}")
    print(out_df["sample_month"].value_counts().sort_index())

if __name__ == "__main__":
    main()