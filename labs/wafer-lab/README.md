# wafer-lab — 반도체 품질데이터 실습 폴더

이 폴더를 VS Code로 열고 Claude Code를 실행한다.

| 경로 | 내용 |
|---|---|
| data/wafer_test_W07.csv | 1교시 · 웨이퍼 한 장 (다이 616개) |
| data/raw/wafer_test_W01~W25.csv | 2·6교시 · 테스터 원시 파일 25장 (일부러 넣은 문제 포함) |
| data/spec.csv | 측정 항목별 스펙 (LSL · USL) |
| data/equipment.csv | 웨이퍼별 설비 · 챔버 · 테스트 날짜 |
| data/new/wafer_test_W26.csv | 7교시 · 나중에 들어오는 웨이퍼 (ETCH_03) — raw/ 로 옮겨 다시 실행 |
| data/practice/ | 교시마다 먼저 보는 일반 예 · 택배 배송 25일치 (D05 중복 · D11 g 단위 · D19 결측) |
| data/secom/secom.csv | 2교시 · 실제 공정 센서 데이터 (UCI SECOM) |

- 웨이퍼 데이터는 교육용 합성 데이터다 (labs/make_data.py · 시드 2611). 택배 데이터도 합성 (labs/make_general.py · 시드 1025).
- SECOM: McCann, M. & Johnston, A. (2008). SECOM [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C54305 · CC BY 4.0
