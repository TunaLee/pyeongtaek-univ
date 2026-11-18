"""웨이퍼 맵 — 정제본 한 장 → output/wafer_map_W07.html

사용: python scripts/wafer_map.py output/clean/W07.csv
"""
import sys

import pandas as pd

from common import OUT
from svg import page, wafer_map

df = pd.read_csv(sys.argv[1])
wid = df.wafer_id.iloc[0]
y = (df.pass_fail == "PASS").mean() * 100
body = (f"<div class='kpi'><div><span>총 다이</span><b>{len(df)}</b></div><div><span>양품</span><b>{(df.pass_fail == 'PASS').sum()}</b></div>"
        f"<div><span>수율</span><b>{y:.2f}%</b></div></div><div class='card'>{wafer_map(df, 520)}</div>")
(OUT / f"wafer_map_{wid}.html").write_text(page(f"웨이퍼 맵 · {wid}", body), encoding="utf-8")
print(wid, f"{y:.2f}%")
