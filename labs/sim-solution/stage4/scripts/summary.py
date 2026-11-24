"""웨이퍼 엑셀 집계 — 수율 · 불합격 사유별 · 위치별 시트 3장과 HTML 이 읽는 CSV.

실행: python scripts/summary.py
결과: output/yield_summary.xlsx · output/wafer_test_W07.csv
"""
from pathlib import Path

import pandas as pd

SRC = Path("data/wafer_test_W07.xlsx")
OUT = Path("output")
REASON = {"crack": "깨짐·긁힘", "open_short": "접촉저항 초과", "leakage": "누설전류 초과",
          "vth_shift": "문턱전압 범위 밖", "particle": "먼지 많음", "parametric": "기타 측정값"}
ZONE = {"center": "중심", "mid": "중간", "edge": "가장자리"}

df = pd.read_excel(SRC)
total = len(df)
ok = int((df["pass_fail"] == "PASS").sum())

yield_sheet = pd.DataFrame({"항목": ["전체 칩", "합격", "불합격", "수율(%)"],
                            "값": [total, ok, total - ok, round(ok / total * 100, 2)]})

fails = df[df["pass_fail"] == "FAIL"]
reason_sheet = (fails["fail_type"].value_counts().rename_axis("사유").reset_index(name="칩 수"))
reason_sheet.insert(1, "화면 이름", reason_sheet["사유"].map(REASON))
reason_sheet["불합격 중 비율(%)"] = (reason_sheet["칩 수"] / len(fails) * 100).round(1)

zone_sheet = (df.groupby("zone")
              .agg(칩수=("pass_fail", "size"), 합격=("pass_fail", lambda s: int((s == "PASS").sum())))
              .reindex(list(ZONE)).reset_index())
zone_sheet.insert(1, "위치", zone_sheet["zone"].map(ZONE))
zone_sheet["합격률(%)"] = (zone_sheet["합격"] / zone_sheet["칩수"] * 100).round(2)
zone_sheet = zone_sheet.rename(columns={"zone": "구역", "칩수": "칩 수"})

OUT.mkdir(exist_ok=True)
with pd.ExcelWriter(OUT / "yield_summary.xlsx") as xw:
    yield_sheet.to_excel(xw, sheet_name="수율", index=False)
    reason_sheet.to_excel(xw, sheet_name="사유별", index=False)
    zone_sheet.to_excel(xw, sheet_name="위치별", index=False)
df.to_csv(OUT / "wafer_test_W07.csv", index=False)

print(f"전체 {total} · 합격 {ok} · 불합격 {total - ok} · 수율 {ok / total * 100:.2f}%")
