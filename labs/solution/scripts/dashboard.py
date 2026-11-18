"""대시보드 — data/warehouse.duckdb → output/dashboard.html

사용: python scripts/dashboard.py   (pipeline.py 다음)
"""
import duckdb

from common import DATA, KO, OUT
from svg import bars, line, page, wafer_map

con = duckdb.connect(str(DATA / "warehouse.duckdb"), read_only=True)
wy = con.execute("SELECT * FROM wafer_yield").df()
ey = con.execute("SELECT * FROM eqp_yield").df()
worst = wy.sort_values("yield_pct").iloc[0]
dies = con.execute("SELECT * FROM dies WHERE wafer_id = ?", [worst.wafer_id]).df()
par = con.execute("""SELECT fail_type, sum(n) AS n FROM fail_pareto GROUP BY fail_type ORDER BY n DESC""").df()
eq = dict(zip(wy.wafer_id, wy.eqp_id))
EQC = {"ETCH_01": "#1F3A5F", "ETCH_02": "#5C8DC9", "ETCH_03": "#E07A12"}
lot = wy["pass"].sum() / wy.dies.sum() * 100
kpi = (f"<div class='kpi'><div><span>LOT 수율</span><b>{lot:.2f}%</b></div><div><span>웨이퍼</span><b>{len(wy)}장</b></div>"
       f"<div><span>목표 90% 미달</span><b>{int((wy.yield_pct < 90).sum())}장</b></div>"
       f"<div><span>최저 웨이퍼</span><b>{worst.wafer_id} · {worst.yield_pct}%</b></div></div>")
body = (kpi + "<div class='card'><h3>웨이퍼별 수율 · 점 색 = 설비 (남 ETCH_01 · 하늘 ETCH_02 · 주황 ETCH_03)</h3>"
        + line(list(zip(wy.wafer_id, wy.yield_pct)), w=1100, unit="%", target=90, ymin=84, ymax=97, color_of=lambda k: EQC[eq[k]])
        + "</div><div class='grid' style='margin-top:16px'>"
        + f"<div class='card'><h3>설비별 평균 수율</h3>{bars(list(zip(ey.eqp_id, ey.yield_pct)), unit='%', target=90, ymin=80, ymax=97)}</div>"
        + f"<div class='card'><h3>불량 유형 Pareto (LOT 전체)</h3>{bars([(KO[t], int(n)) for t, n in zip(par.fail_type, par.n)], color='#C62828')}</div>"
        + f"<div class='card'><h3>최저 수율 웨이퍼 {worst.wafer_id} ({worst.eqp_id})</h3>{wafer_map(dies, 400)}</div></div>")
(OUT / "dashboard.html").write_text(page("웨이퍼 테스트 대시보드 · LOT2611-07", body), encoding="utf-8")
print("dashboard.html", f"LOT {lot:.2f}%", worst.wafer_id)
