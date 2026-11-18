"""데이터 파이프라인 — 원시 CSV 25장 → 정제 → Parquet → DuckDB 적재 → SQL 집계

사용: python scripts/pipeline.py
  수집  data/raw/*.csv           (테스터가 내려 준 원시 파일)
  정제  clean.clean()            (중복 · 단위 · 결측 · 재판정)
  적재  data/clean/*.parquet  →  data/warehouse.duckdb  (표 dies · equipment)
  집계  SQL 뷰 wafer_yield · eqp_yield · fail_pareto
  기록  output/pipeline_log.md   (파일마다 행 수 · 발견한 문제)
"""
import duckdb
import pandas as pd

from clean import clean, validate
from common import DATA, OUT

CLEAN = DATA / "clean"
DB = DATA / "warehouse.duckdb"


def run():
    CLEAN.mkdir(exist_ok=True)
    OUT.mkdir(exist_ok=True)
    log = ["# 파이프라인 기록", "", "| 파일 | 원시 행 | 정제 행 | 발견한 문제 | 검증 |", "|---|---|---|---|---|"]
    for f in sorted((DATA / "raw").glob("wafer_test_*.csv")):
        raw = pd.read_csv(f)
        df, issues = clean(raw)
        ok = all(v for _, v in validate(df))
        df.to_parquet(CLEAN / f"{f.stem}.parquet", index=False)
        log.append(f"| {f.name} | {len(raw)} | {len(df)} | {' · '.join(issues) or '-'} | {'통과' if ok else '실패'} |")
    con = duckdb.connect(str(DB))
    con.execute(f"CREATE OR REPLACE TABLE dies AS SELECT * FROM read_parquet('{CLEAN}/*.parquet')")
    con.execute(f"CREATE OR REPLACE TABLE equipment AS SELECT * FROM read_csv_auto('{DATA}/equipment.csv')")
    con.execute("""CREATE OR REPLACE VIEW wafer_yield AS
        SELECT d.wafer_id, e.eqp_id, count(*) AS dies,
               sum(CASE WHEN pass_fail = 'PASS' THEN 1 ELSE 0 END) AS pass,
               round(100.0 * sum(CASE WHEN pass_fail = 'PASS' THEN 1 ELSE 0 END) / count(*), 2) AS yield_pct
        FROM dies d JOIN equipment e USING (wafer_id) GROUP BY d.wafer_id, e.eqp_id ORDER BY d.wafer_id""")
    con.execute("""CREATE OR REPLACE VIEW eqp_yield AS
        SELECT eqp_id, count(*) AS wafers, round(avg(yield_pct), 2) AS yield_pct,
               sum(CASE WHEN yield_pct < 90 THEN 1 ELSE 0 END) AS below_target
        FROM wafer_yield GROUP BY eqp_id ORDER BY eqp_id""")
    con.execute("""CREATE OR REPLACE VIEW fail_pareto AS
        SELECT e.eqp_id, fail_type, count(*) AS n FROM dies d JOIN equipment e USING (wafer_id)
        WHERE pass_fail <> 'PASS' GROUP BY e.eqp_id, fail_type ORDER BY e.eqp_id, n DESC""")
    n = con.execute("SELECT count(*) FROM dies").fetchone()[0]
    log += ["", f"- 적재 다이 {n}개 · 웨이퍼 {n // 616}장"]
    (OUT / "pipeline_log.md").write_text("\n".join(log) + "\n", encoding="utf-8")
    print("\n".join(log))
    print(con.execute("SELECT * FROM eqp_yield").df().to_string(index=False))
    con.close()


if __name__ == "__main__":
    run()
