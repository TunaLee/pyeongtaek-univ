"""사과 엑셀 집계 — 상품률 · 불량 사유별 · 구역별 시트 3장과 화면용 CSV.

실행: python scripts/apple_summary.py
결과: output/apple_summary.xlsx · output/apple_A07.csv
"""
from pathlib import Path

import pandas as pd

SRC = Path("data/apple_A07.xlsx")
OUT = Path("output")
REASON = {"bruise": "멍", "worm": "벌레 먹음", "light": "무게 미달", "low_sugar": "당도 미달"}
ZONES = ["안쪽", "중간", "가장자리"]

df = pd.read_excel(SRC)
total = len(df)
ok = int((df["grade"] == "상품").sum())

rate_sheet = pd.DataFrame({"항목": ["전체 사과", "상품", "불량", "상품률(%)"],
                           "값": [total, ok, total - ok, round(ok / total * 100, 2)]})

fails = df[df["grade"] == "불량"]
reason_sheet = fails["reason"].value_counts().rename_axis("사유").reset_index(name="개수")
reason_sheet.insert(1, "화면 이름", reason_sheet["사유"].map(REASON))
reason_sheet["불량 중 비율(%)"] = (reason_sheet["개수"] / len(fails) * 100).round(1)

zone_sheet = (df.groupby("zone")
              .agg(개수=("grade", "size"), 상품=("grade", lambda s: int((s == "상품").sum())))
              .reindex(ZONES).reset_index().rename(columns={"zone": "구역"}))
zone_sheet["상품률(%)"] = (zone_sheet["상품"] / zone_sheet["개수"] * 100).round(2)

OUT.mkdir(exist_ok=True)
with pd.ExcelWriter(OUT / "apple_summary.xlsx") as xw:
    rate_sheet.to_excel(xw, sheet_name="상품률", index=False)
    reason_sheet.to_excel(xw, sheet_name="사유별", index=False)
    zone_sheet.to_excel(xw, sheet_name="구역별", index=False)
df.to_csv(OUT / "apple_A07.csv", index=False)

print(f"전체 {total} · 상품 {ok} · 불량 {total - ok} · 상품률 {ok / total * 100:.2f}%")
