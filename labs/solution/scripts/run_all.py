"""한 번에 — 파이프라인 → 대시보드. 새 원시 파일을 data/raw/ 에 넣고 이것만 다시 실행한다.

사용: python scripts/run_all.py
"""
import runpy
from pathlib import Path

HERE = Path(__file__).resolve().parent
for s in ("pipeline.py", "dashboard.py"):
    print(f"── {s}")
    runpy.run_path(str(HERE / s), run_name="__main__")
