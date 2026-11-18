"""집계 — 정제본 한 장 → output/yield_summary.xlsx (시트 3장: 요약 · 존별 · 불량 유형)

사용: python scripts/aggregate.py output/clean/W07.csv
"""
import sys

import pandas as pd

from common import KO, OUT

df = pd.read_csv(sys.argv[1])
ok = df.pass_fail == "PASS"
summary = pd.DataFrame({"항목": ["총 다이", "양품", "불량", "수율(%)"],
                        "값": [len(df), int(ok.sum()), int((~ok).sum()), round(ok.mean() * 100, 2)]})
zone = (df.assign(ok=ok).groupby("zone").agg(다이=("ok", "size"), 양품=("ok", "sum"))
        .reindex(["center", "mid", "edge"]).assign(**{"수율(%)": lambda t: (t.양품 / t.다이 * 100).round(2)}))
fail = (df[~ok].fail_type.value_counts().rename_axis("불량 유형").reset_index(name="다이 수")
        .assign(**{"이름": lambda t: t["불량 유형"].map(KO), "누적(%)": lambda t: (t["다이 수"].cumsum() / t["다이 수"].sum() * 100).round(1)}))
with pd.ExcelWriter(OUT / "yield_summary.xlsx") as xw:
    summary.to_excel(xw, sheet_name="요약", index=False)
    zone.to_excel(xw, sheet_name="존별")
    fail.to_excel(xw, sheet_name="불량 유형", index=False)
print(summary.to_string(index=False)); print(zone); print(fail.to_string(index=False))
