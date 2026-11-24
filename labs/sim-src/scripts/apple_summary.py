"""사과 엑셀 집계 — 상품률 · 불량 사유별 · 위치별 시트 3장과 HTML 이 읽는 CSV.

실행: python scripts/apple_summary.py
결과: output/apple_summary.xlsx · output/apple_A07.csv
"""
from pathlib import Path

import pandas as pd

SRC = Path("data/apple_A07.xlsx")
OUT = Path("output")
ZONES = ["안쪽", "중간", "가장자리"]

df = pd.read_excel(SRC)
total = len(df)
ok = int((df["등급"] == "상품").sum())

rate_sheet = pd.DataFrame({"항목": ["전체 사과", "상품", "불량", "상품률(%)"],
                           "값": [total, ok, total - ok, round(ok / total * 100, 2)]})

fails = df[df["등급"] == "불량"]
reason_sheet = fails["불량사유"].value_counts().rename_axis("불량사유").reset_index(name="개수")
reason_sheet["불량 중 비율(%)"] = (reason_sheet["개수"] / len(fails) * 100).round(1)

zone_sheet = (df.groupby("위치")
              .agg(개수=("등급", "size"), 상품=("등급", lambda s: int((s == "상품").sum())))
              .reindex(ZONES).reset_index())
zone_sheet["상품률(%)"] = (zone_sheet["상품"] / zone_sheet["개수"] * 100).round(2)

OUT.mkdir(exist_ok=True)
with pd.ExcelWriter(OUT / "apple_summary.xlsx") as xw:
    rate_sheet.to_excel(xw, sheet_name="상품률", index=False)
    reason_sheet.to_excel(xw, sheet_name="사유별", index=False)
    zone_sheet.to_excel(xw, sheet_name="위치별", index=False)
df.to_csv(OUT / "apple_A07.csv", index=False)

print(f"전체 {total} · 상품 {ok} · 불량 {total - ok} · 상품률 {ok / total * 100:.2f}%")
