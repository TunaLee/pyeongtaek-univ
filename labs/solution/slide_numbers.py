"""6~8교시 슬라이드 숫자 — warehouse.duckdb 에서 뽑아 output/slide_numbers.json 에 저장 (덱은 이 파일만 읽는다).

실행: python scripts/run_all.py && python slide_numbers.py
"""
import json
from pathlib import Path

import duckdb

HERE = Path(__file__).resolve().parent
D = HERE / "data"
con = duckdb.connect(str(D / "warehouse.duckdb"), read_only=True)
q = lambda s: con.execute(s).fetchall()
YLD = "round(100.0 * avg(CASE WHEN pass_fail = 'PASS' THEN 1 ELSE 0 END), 2)"
out = {
    "eqp_yield": [dict(zip(("eqp", "wafers", "yield", "below"), (r[0], r[1], r[2], int(r[3])))) for r in q("SELECT * FROM eqp_yield")],
    "eqp_zone": {f"{e}|{z}": y for e, z, y in q(f"SELECT e.eqp_id, zone, {YLD} FROM dies d JOIN equipment e USING (wafer_id) GROUP BY 1, 2")},
    "eqp_fail": {f"{e}|{t}": n for e, t, n in q("SELECT eqp_id, fail_type, n FROM fail_pareto")},
    "wafer_zone": {f"{w}|{z}": y for w, z, y in q(f"SELECT wafer_id, zone, {YLD} FROM dies GROUP BY 1, 2")},
    "wafer_fail": {f"{w}|{t}": n for w, t, n in q("SELECT wafer_id, fail_type, count(*) FROM dies WHERE pass_fail <> 'PASS' GROUP BY 1, 2")},
    "chamber": {f"{e}|{c}": y for e, c, y in q(f"SELECT e.eqp_id, chamber, {YLD} FROM dies d JOIN equipment e USING (wafer_id) GROUP BY 1, 2")},
    "date": {str(t): [y, ", ".join(sorted(set(ws.split(","))))] for t, y, ws in q(f"SELECT test_date, {YLD}, string_agg(DISTINCT e.eqp_id, ',') FROM dies d JOIN equipment e USING (wafer_id) GROUP BY 1 ORDER BY 1")},
    "dies": q("SELECT count(*) FROM dies")[0][0],
    "csv_kb": round(sum(f.stat().st_size for f in (D / "raw").glob("*.csv")) / 1024),
    "parquet_kb": round(sum(f.stat().st_size for f in (D / "clean").glob("*.parquet")) / 1024),
    "w07_csv_kb": round((D / "raw" / "wafer_test_W07.csv").stat().st_size / 1024, 1),
    "w07_parquet_kb": round((D / "clean" / "wafer_test_W07.parquet").stat().st_size / 1024, 1),
}
(HERE / "output" / "slide_numbers.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print({k: v for k, v in out.items() if k in ("eqp_yield", "dies", "csv_kb", "parquet_kb", "w07_csv_kb", "w07_parquet_kb")})
