"""택배 엑셀 집계 — 정시율 · 실패 사유별 · 구역별 시트 3장과 화면용 CSV.

실행: python scripts/delivery_summary.py
결과: output/delivery_summary.xlsx · output/delivery_D07.csv
"""
from pathlib import Path

import pandas as pd

SRC = Path("data/delivery_D07.xlsx")
OUT = Path("output")
REASON = {"damaged": "파손", "addr_error": "주소 오류", "late": "지연", "absent": "부재"}
AREAS = ["도심", "중간", "외곽"]

df = pd.read_excel(SRC)
total = len(df)
ok = int((df["status"] == "ON_TIME").sum())

rate_sheet = pd.DataFrame({"항목": ["전체 배송", "정시", "실패", "정시율(%)"],
                           "값": [total, ok, total - ok, round(ok / total * 100, 2)]})

fails = df[df["status"] == "FAIL"]
reason_sheet = fails["reason"].value_counts().rename_axis("사유").reset_index(name="건수")
reason_sheet.insert(1, "화면 이름", reason_sheet["사유"].map(REASON))
reason_sheet["실패 중 비율(%)"] = (reason_sheet["건수"] / len(fails) * 100).round(1)

area_sheet = (df.groupby("area")
              .agg(건수=("status", "size"), 정시=("status", lambda s: int((s == "ON_TIME").sum())))
              .reindex(AREAS).reset_index().rename(columns={"area": "구역"}))
area_sheet["정시율(%)"] = (area_sheet["정시"] / area_sheet["건수"] * 100).round(2)

OUT.mkdir(exist_ok=True)
with pd.ExcelWriter(OUT / "delivery_summary.xlsx") as xw:
    rate_sheet.to_excel(xw, sheet_name="정시율", index=False)
    reason_sheet.to_excel(xw, sheet_name="사유별", index=False)
    area_sheet.to_excel(xw, sheet_name="구역별", index=False)
df.to_csv(OUT / "delivery_D07.csv", index=False)

print(f"전체 {total} · 정시 {ok} · 실패 {total - ok} · 정시율 {ok / total * 100:.2f}%")
