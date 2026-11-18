# 데이터 사전 · wafer_test_W07.csv

다이 1개 = 1행 · 616행 · 열 18개 · 결측 0

| 열 | 뜻 | 단위 · 값 | 스펙 |
|---|---|---|---|
| lot_id · wafer_id | LOT · 웨이퍼 번호 | LOT2611-07 · W07 | |
| die_x · die_y | 다이 격자 좌표 | 정수 −15~14 | |
| center_x_mm · center_y_mm | 다이 중심 좌표 | mm · 웨이퍼 중심 (0, 0) | |
| radius_mm · zone | 중심 거리 · 구역 | mm · center <50 · mid 50~110 · edge >110 | |
| vth_v | 문턱전압 | V | 0.38~0.52 |
| idsat_ma | 포화전류 | mA | 0.92 이상 |
| ioff_na | 누설전류 | nA | 10 이하 |
| rc_ohm | 접촉저항 | Ω | 15 이하 |
| ox_thk_nm | 산화막 두께 | nm | 2.85~3.15 |
| crack · particle_cnt | 크랙 여부 · 파티클 수 | 0/1 · 개 | 0 · 4 이하 |
| bin · fail_type · pass_fail | 판정 | 1 양품 · 2~7 불량 | |

기준 숫자: 다이 616 · 양품 557 · 불량 59 · 수율 90.42%
