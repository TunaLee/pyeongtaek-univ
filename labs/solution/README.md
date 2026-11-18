# solution — 교시별 완성본

실행 전: `cp -r ../wafer-lab/data ./data` (data/ 는 저장소에 넣지 않는다)

| 교시 | 실행 | 결과 |
|---|---|---|
| 2 | `python scripts/clean.py data/raw/wafer_test_W11.csv` | output/clean/W11.csv · output/qc_W11.md |
| 3 | `python scripts/aggregate.py output/clean/W07.csv` · `python scripts/yield_model.py` | yield_summary.xlsx · die_size_yield.csv |
| 4 | `python scripts/wafer_map.py output/clean/W07.csv` | wafer_map_W07.html |
| 5 | `python scripts/spc.py output/clean/W07.csv` | spc_W07.html · outliers_W07.csv |
| 6 · 7 | `python scripts/run_all.py` | data/warehouse.duckdb · pipeline_log.md · dashboard.html |

패키지: pandas · openpyxl · duckdb · pyarrow
