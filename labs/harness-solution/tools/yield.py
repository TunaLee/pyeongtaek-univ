"""수율 계산 도구 — 엑셀 파일마다 행 수 · 합격(상품) · 불합격(불량) · 수율(상품률)을 출력한다.

실습 「수율 계산 도구 만들기」 완성본. 실행: python3 tools/yield.py data/wafer_test_W07.xlsx (여러 개 가능)
CLAUDE.md 한 줄: 수율은 tools/yield.py 로 계산한다. 웨이퍼는 pass_fail 이 PASS, 사과는 등급이 상품이면 합격.
"""
import sys
import pandas as pd

for path in sys.argv[1:]:
    df = pd.read_excel(path)
    n = len(df)
    ok = int((df["pass_fail"] == "PASS").sum()) if "pass_fail" in df else int((df["등급"] == "상품").sum())
    print(f"{path} · 행 {n} · 합격 {ok} · 불합격 {n - ok} · 수율 {ok / n * 100:.2f}%")
