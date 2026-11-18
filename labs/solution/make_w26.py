"""7교시 · 새로 들어온 웨이퍼 한 장 — W26 (ETCH_03) 원시 파일을 만든다.

실행: python make_w26.py  → extra/wafer_test_W26.csv
실습: 이 파일을 data/raw/ 에 넣고 python scripts/run_all.py 를 다시 실행 → 대시보드에 26장째가 붙는다.
make_data.py 의 웨이퍼 생성기를 그대로 쓴다 (시드 2626).
"""
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import make_data as md  # noqa: E402

rows = md.wafer(26, np.random.default_rng(2626), md.dies())
(HERE / "extra").mkdir(exist_ok=True)
md.write(HERE / "extra" / "wafer_test_W26.csv", md.HEADER, rows)
eq = (HERE / "data" / "equipment.csv")
npass = sum(r[-1] == "PASS" for r in rows)
print("W26", md.eqp_of(26), npass, f"{npass / len(rows) * 100:.2f}%")
