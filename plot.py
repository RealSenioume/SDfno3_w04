# /// script
# requires-python = ">=3.10"
# dependencies = ["pandas", "matplotlib"]
# ///

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# 函数：把 YEAR + MO + DY 合成日期
def add_date_column(df):
    """NASA POWER 用 YEAR + MO + DY 表示时间，合成一个 date 列。"""
    dates = []
    for _, row in df.iterrows():
        date = pd.to_datetime(
            f"{int(row['YEAR'])}-{int(row['MO'])}-{int(row['DY'])}",
            format="%Y-%m-%d",
        )
        dates.append(date)
    df = df.copy()
    df["date"] = dates
    return df

# 函数：计算滑动平均（不用 pandas.rolling）
def rolling_mean(values, window=7):
    result = []
    for i in range(len(values)):
        start = max(0, i - window // 2)
        end = min(len(values), i + window // 2 + 1)
        result.append(sum(values[start:end]) / (end - start))
    return result

# --- READ ---
DATA = "data/nasa_power_hongkong_202601t06.csv" # !!!file name!!!
df = pd.read_csv(DATA, skiprows=20)   # ← 改成数出来的行数 = (行数-1)
print("Columns:", df.columns.tolist())
print("Rows:", len(df))
print(df.head())

# 过滤掉 NASA 用 -999 表示的缺失值
df = df[df["ALLSKY_SFC_SW_DWN"] > -900].reset_index(drop=True)

df = add_date_column(df)

# --- 循环：对每一天算 7 天滑动平均 ---
df["radiation_smooth"] = rolling_mean(df["ALLSKY_SFC_SW_DWN"].tolist(), window=7)

# --- DRAW ---
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(df["date"], df["ALLSKY_SFC_SW_DWN"],
        alpha=0.35, linewidth=1, label="Daily")
ax.plot(df["date"], df["radiation_smooth"],
        linewidth=2.5, label="7-day average")
ax.set_xlabel("Date (2026)")
ax.set_ylabel("Solar radiation (kWh/m²/day)")
ax.set_title("Daily solar radiation — Hong Kong, 2026 Jan2Jun") # !!!Changing title name!!!
ax.legend()
ax.grid(True, alpha=0.3)

out = Path("out")
out.mkdir(exist_ok=True)
plt.savefig(out / "HK_solar_radiation_2026Jan2Jun.png", dpi=300, bbox_inches="tight")
print(f"Saved to {out / 'HK_solar_radiation_2026Jan2Jun.png'}")