# 웨이퍼 테스트 데이터 프로젝트

## 목적
CP 테스트 CSV를 정제 · 적재 · 집계해 수율 대시보드와 분석 요약을 만든다.

## 폴더
- data/raw/   테스터 원시 CSV — 읽기만 한다. 고치지 않는다.
- data/       spec.csv · equipment.csv · 정제본 · DB
- docs/       데이터 사전 · 검증 보고서 · 분석 요약
- scripts/    파이썬 스크립트 (python scripts/파일.py 로 실행)
- output/     엑셀 · HTML · CSV 결과

## 데이터
- 다이 1개 = 1행 · 웨이퍼 1장 = 616행 · 열 18개 (docs/data_dictionary.md)
- 300 mm 웨이퍼 · 다이 10×10 mm · 가장자리 제외 3 mm

## 판정 규칙 (위에서부터 처음 걸린 유형)
crack → open_short(rc_ohm>15) → leakage(ioff_na>10) → vth_shift(vth_v 0.38~0.52 밖)
→ particle(particle_cnt≥5) → parametric(idsat_ma<0.92 · ox_thk_nm 2.85~3.15 밖) → none(PASS)

## 작업 규칙
- 답과 주석은 한국어
- CSV 전체를 출력하지 않는다 — 앞 5줄과 요약만
- 숫자를 보고할 때 원본에서 다시 센 값을 함께 적는다
- 차트는 축 제목 · 단위 · 범례를 넣는다 · 양품 #2BA84A · 불량 #C62828
