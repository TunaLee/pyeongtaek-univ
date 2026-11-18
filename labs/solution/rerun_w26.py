"""7교시 슬라이드 숫자 — W26 을 넣기 전 · 후의 대시보드 숫자를 임시 폴더에서 다시 계산해 output/w26_rerun.json 에 저장.

실행: python make_w26.py && python rerun_w26.py   (data/ 원본은 건드리지 않는다)
"""
import json
import runpy
import shutil
import sys
import tempfile
from pathlib import Path

import duckdb

HERE = Path(__file__).resolve().parent


def numbers(root):
    con = duckdb.connect(str(root / "data" / "warehouse.duckdb"), read_only=True)
    wy = con.execute("SELECT * FROM wafer_yield").df()
    ey = con.execute("SELECT * FROM eqp_yield").df()
    con.close()
    return {"wafers": len(wy), "lot_yield": round(float(wy["pass"].sum() / wy.dies.sum() * 100), 2),
            "below_target": int((wy.yield_pct < 90).sum()),
            "etch03": {"wafers": int(ey[ey.eqp_id == "ETCH_03"].wafers.iloc[0]), "yield": float(ey[ey.eqp_id == "ETCH_03"].yield_pct.iloc[0])}}


def run(root):
    sys.path.insert(0, str(root / "scripts"))
    for s in ("pipeline.py", "dashboard.py"):
        runpy.run_path(str(root / "scripts" / s), run_name="__main__")
    sys.path.pop(0)
    for m in ("common", "clean", "svg"):
        sys.modules.pop(m, None)


out = {}
for tag, add in (("before", False), ("after", True)):
    tmp = Path(tempfile.mkdtemp())
    shutil.copytree(HERE / "scripts", tmp / "scripts")
    shutil.copytree(HERE / "data", tmp / "data", ignore=shutil.ignore_patterns("clean", "warehouse.duckdb"))
    if add:
        shutil.copy(HERE / "extra" / "wafer_test_W26.csv", tmp / "data" / "raw")
        eq = tmp / "data" / "equipment.csv"
        lines = [x for x in eq.read_text().replace("\r\n", "\n").split("\n") if x] + ["W26,ETCH_03,CHA,2026-11-08"]
        eq.write_text("\n".join(lines) + "\n")
    run(tmp)
    out[tag] = numbers(tmp)
    if add:
        shutil.copy(tmp / "output" / "dashboard.html", HERE / "output" / "dashboard_W26.html")
    shutil.rmtree(tmp)
(HERE / "output" / "w26_rerun.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print(out)
