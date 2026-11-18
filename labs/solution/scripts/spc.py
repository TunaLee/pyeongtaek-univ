"""파라미터 분포 · Cpk · 이상 다이 — 정제본 한 장 → output/spc_W07.html · output/outliers_W07.csv

Cpk = min(USL − μ, μ − LSL) / 3σ  (NIST/SEMATECH e-Handbook)
"""
import sys

import pandas as pd

from common import COLOR, OUT
from svg import hist, page, scatter

SPEC = {"vth_v": (0.38, 0.52), "ox_thk_nm": (2.85, 3.15)}


def cpk(s, lsl, usl):
    mu, sd = s.mean(), s.std()
    return min(usl - mu, mu - lsl) / (3 * sd)


df = pd.read_csv(sys.argv[1])
wid = df.wafer_id.iloc[0]
rows = [{"param": p, "mean": round(df[p].mean(), 4), "std": round(df[p].std(), 4), "lsl": l, "usl": u,
         "cpk": round(cpk(df[p], l, u), 2)} for p, (l, u) in SPEC.items()]
print(pd.DataFrame(rows).to_string(index=False))
out = df[(~df.vth_v.between(.38, .52)) | (df.idsat_ma < .92)]
out.to_csv(OUT / f"outliers_{wid}.csv", index=False)
print("스펙 밖 다이", len(out))
body = ("<div class='grid'>"
        f"<div class='card'><h3>문턱전압 분포 (Cpk {rows[0]['cpk']})</h3>{hist(df.vth_v.tolist(), .38, .52, unit=' V')}</div>"
        f"<div class='card'><h3>문턱전압 · 포화전류</h3>"
        f"{scatter(df.vth_v.tolist(), df.idsat_ma.tolist(), [COLOR['none'] if p == 'PASS' else '#C62828' for p in df.pass_fail], (.38, .52, .92), xl='vth_v (V)', yl='idsat_ma (mA)')}</div>"
        "</div>")
(OUT / f"spc_{wid}.html").write_text(page(f"파라미터 분포 · {wid}", body), encoding="utf-8")
