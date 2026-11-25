"""1교시 데이터 분석 첫걸음 · Claude Code 시작 (사과 데이터 · 실습 중심).

개요(데이터 분석 → 바이브코딩)에서 본 그림을 Claude Code 로 직접 그려 본다.
도입(실습 환경 · 실습 폴더 sim-lab) → 설명(요청 쓰는 법 · 차트 종류는 개요 「데이터 시각화 방법」 · Claude Code 의 동작은 개요 「에이전트 루프」)
→ 적용(실습 폴더 · 환경 · 실습 1-1 사과 데이터 읽기 → 1-2 사과 차트 세 장 · 결과 · 사과 차트에서 읽은 사실).
"""
import sk
import viz2
from deck import lab, light
from pkit import brief, tag
from stats_hx import src

DATA_URL = "tunalee.github.io/pyeongtaek-univ/sim-data.zip"   # labs/make_sim.py make_zip() 이 docs/ 에 만듦

T = tag("1")
DN = sk.DN
CSS = ""


def slides():
    df = sk.D07
    w = df["무게"]
    zr = DN["area"]
    low = min(zr, key=zr.get)
    rest = " · ".join(f"{z} {zr[z]:.2f}%" for z in sk.AREA if z != low)
    under = int((w < sk.MIN_W).sum())
    edge = df[df["위치"] == "가장자리"]
    e_bad, e_n = int((edge["등급"] != "상품").sum()), len(edge)
    return [
        # ── 도입
        light("실습 환경", viz2.tiles([
            ("VS Code", "편집기 · 파일 탐색기 · 터미널"), ("Claude Code 확장", "VS Code 확장 · 교육용 계정 로그인"),
            ("Python", "pandas · openpyxl"), ("실습 데이터", "sim-data.zip · 엑셀 4개 · 기준표 2장 · 예시 HTML")], 2)
              + src(("Claude Code 문서 · VS Code", "https://code.claude.com/docs/en/vs-code")), T),
        light("실습 폴더 만들기", viz2.tiles([("실습 데이터 받기", DATA_URL)], 1) + viz2.maprows([
            ("sim-lab/", "새 폴더 · VS Code 로 열기", "직접 만듦"),
            ("data/", "엑셀 4개 · 사과 A07 · A25 · 웨이퍼 W07 · W21", "sim-data.zip · 읽기만"),
            ("templates/", "선별기준표 · 합격기준표 · 예시 HTML", "sim-data.zip · 참고 자료"),
            ("CLAUDE.md", "폴더 규칙 · 계산 방법", "Claude 가 만듦"),
            ("docs/ · output/", "요약 · 집계 엑셀 · simulator.html · index.html", "실습마다 추가")], "폴더", "내용"), T),
        # ── 설명
        light("요청 쓰는 법", viz2.pair(
            "한 줄 요청", [("요청", "「사과 엑셀 요약해 줘」"), ("무엇을", "Claude 가 추측"), ("저장", "대화창에만 · 파일 없음")],
            "네 칸을 채운 요청", [("목표", "몇 행 · 몇 열 · 열마다 뜻 · 상품 · 불량 수"), ("입력", "data/apple_A07.xlsx"),
                             ("산출물", "docs/사과_요약.md"), ("금지 사항", "원본 수정")]), T),
        # ── 적용
        lab("1-1", "사과 데이터 읽기", T, "sim-lab 폴더를 만들고 데이터를 풀어 apple_A07.xlsx 를 요약 문서로 받는다",
            ["sim-lab 폴더 만들기 · sim-data.zip 받기", "압축 풀기 · CLAUDE.md 만들기", "사과 엑셀 요약 요청",
             "수치형 · 범주형 열 구분 요청", "엑셀 필터로 상품 수 대조"],
            ["data/ 엑셀 4개 · templates/ 3개 · CLAUDE.md", f"{DN['rows']}행 × {DN['cols']}열",
             f"상품 {DN['pass']} · 불량 {DN['fail']} · {DN['rate']}%", "docs/사과_요약.md"],
            files="sim-data.zip · data/apple_A07.xlsx"),
        lab("1-2", "사과 차트 세 장", T, "무게 분포 · 위치별 상품률 · 과수원 지도를 Claude Code 로 그리고 차트마다 읽히는 사실을 한 줄씩 적는다",
            ["무게 분포 요청", "위치별 상품률 막대 요청", "과수원 지도 요청", "차트마다 읽히는 사실 한 줄"],
            [f"무게 평균 {w.mean():.1f}g", f"{low} 상품률 {zr[low]:.2f}% 최저", "output/charts/ HTML 세 장"], files="data/apple_A07.xlsx"),
        brief("1-2", T,
              ["무게 분포", "위치별 상품률", "과수원 지도", "읽히는 사실"],
              [("목표", "차트 세 장 · 차트마다 사실 한 줄"), ("입력", "apple_A07.xlsx · 무게 · 위치 · 가로칸 · 세로칸 · 등급"),
               ("산출물", "output/charts/ HTML 세 장"), ("하지 말 것", "data/ 원본 수정 · 외부 라이브러리")],
              [], [f"무게 평균 {w.mean():.1f}g", f"{low} {zr[low]:.2f}%"], ""),
        light("사과 차트 결과", sk.trio([("sim/chart_apple_hist.webp", "무게 분포"), ("sim/chart_apple_zone.webp", "위치별 상품률"),
                                       ("sim/chart_apple_map.webp", "과수원 지도")]), T),
        light("사과 차트에서 읽은 사실", viz2.tiles([
            ("무게 분포", f"평균 {w.mean():.1f}g 근처에 몰림 · {sk.MIN_W}g 미만 {under}개"),
            ("위치별 상품률", f"{low} {zr[low]:.2f}% 최저 · {rest}"),
            ("과수원 지도", f"빨간 칸이 바깥 줄에 몰림 · 가장자리 불량 {e_bad} / {e_n}")], 3), T),
    ]
