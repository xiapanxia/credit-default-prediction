"""W1 · 数据初探：确认数据能读、看清结构、找出脏数据。

运行：
    .venv/Scripts/python.exe src/peek_data.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"
TRAIN = DATA_DIR / "cs-training.csv"


def main() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    # index_col=0：第 1 列是行号；na_values="NA"：让 pandas 把 NA 识别为缺失
    df = pd.read_csv(TRAIN, index_col=0, na_values="NA")

    print(f"训练集形状：{df.shape[0]:,} 行 x {df.shape[1]} 列")
    print(f"内存占用：{df.memory_usage(deep=True).sum() / 1024 ** 2:.1f} MB")

    print("\n== 各字段非空数量 ==")
    print(df.notna().sum().to_string())

    print("\n== 缺失率（仅显示有缺失的字段）==")
    miss = (df.isna().mean() * 100).sort_values(ascending=False)
    for col, pct in miss.items():
        if pct > 0:
            print(f"{col}: {pct:.2f}%")

    print("\n== 标签分布 ==")
    for k, v in df["SeriousDlqin2yrs"].value_counts().sort_index().items():
        print(f"{int(k)}: {v:,} ({v / len(df):.2%})")

    print("\n== 数值范围速览（min / 中位数 / max）==")
    print(df.describe().T[["min", "50%", "max"]].round(2).to_string())

    print("\n== 逾期字段的特殊编码 96 / 98 ==")
    for col in (
        "NumberOfTime30-59DaysPastDueNotWorse",
        "NumberOfTime60-89DaysPastDueNotWorse",
        "NumberOfTimes90DaysLate",
    ):
        s = df[col]
        print(f"{col}: 96 -> {int((s == 96).sum())} 条, 98 -> {int((s == 98).sum())} 条")

    print("\n下一步：W2 做清洗 + 逻辑回归 baseline（记录 AUC）")


if __name__ == "__main__":
    main()
