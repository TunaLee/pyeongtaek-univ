"""1교시 데이터 분석 첫걸음 · Claude Code 시작 (사과 데이터).

도입(사과 선별 데이터 · 데이터 분석의 흐름)
→ 설명(채팅과 에이전트 · 에이전트 루프 · 데이터 작업 고리 · 요청 구성
       · 테이블의 행과 열 · 수치형 변수와 분포 · 범주형 변수와 막대 · 위치 데이터와 지도 · 데이터 종류와 차트)
→ 적용(실습 폴더 · 환경 · 실습 1-1 사과 데이터 읽기 → 1-2 사과 차트 세 장 · 사과 차트에서 읽은 사실).
열 목록 · 열 묶음 표는 쓰지 않는다 — 데이터는 지도 · 차트로 직접 보며 이해한다. 웨이퍼는 2교시에 같은 순서로.
"""
import p0
import pbg
import psim
import pviz
import sk
import viz2
from deck import lab, light
from pkit import brief, tag
from stats_hx import src

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
        light("사과 선별 데이터", pbg.orchard_zones(), T),
        light("데이터 분석의 흐름", pbg.analysis_flow(), T),
        # ── 설명 · Claude Code 로 데이터 다루기
        light("채팅과 에이전트", psim.chat_vs_agent(), T),
        light("에이전트 루프", psim.agent_loop()
              + src(("Claude Code 문서 · How Claude Code works", "https://code.claude.com/docs/en/how-claude-code-works")), T),
        light("Claude Code 의 데이터 작업 고리", pviz.data_loop(), T),
        light("요청 구성", viz2.pair(
            "한 줄 요청", [("요청", "「사과 엑셀 요약해 줘」"), ("무엇을", "Claude 가 추측"), ("저장", "대화창에만 · 파일 없음")],
            "네 칸을 채운 요청", [("목표", "몇 행 · 몇 열 · 열마다 뜻 · 상품 · 불량 수"), ("입력", "data/apple_A07.xlsx"),
                             ("산출물", "docs/사과_요약.md"), ("하지 말 것", "원본 수정")]), T),
        # ── 설명 · 데이터 보는 법 (열의 종류 → 맞는 차트)
        light("테이블의 행과 열", p0.table_terms(df), T),
        light("수치형 변수와 분포", p0.num_anim(df), T),
        light("범주형 변수와 막대", p0.cat_anim(df), T),
        light("위치 데이터와 지도", p0.map_anim(df), T),
        light("데이터 종류와 차트", pbg.chart_types(), T),
        # ── 적용
        light("실습 폴더 sim-lab", viz2.maprows([
            ("data/", "apple_A07.xlsx · wafer_test_W07.xlsx", "읽기만"), ("templates/", "선별기준표 · 합격기준표 · 예시 HTML", "참고 자료"),
            ("docs/", "데이터 요약 · 실험 기록", "문서"), ("output/", "차트 · apple_sim.html · simulator.html", "교시마다 추가")], "폴더", "내용"), T),
        light("실습 환경", viz2.tiles([
            ("VS Code", "편집기 · 파일 탐색기 · 터미널"), ("Claude Code 확장", "VS Code 확장 · 교육용 계정 로그인"),
            ("Python", "pandas · openpyxl"), ("sim-lab 폴더", "파일 → 폴더 열기")], 2)
              + src(("Claude Code 문서 · VS Code", "https://code.claude.com/docs/en/vs-code")), T),
        lab("1-1", "사과 데이터 읽기", T, "apple_A07.xlsx 를 Claude Code 로 읽고 몇 행 · 몇 열 · 열마다 뜻 · 상품 · 불량 수를 요약 문서로 받는다",
            ["sim-lab 열기 · Claude Code 실행", "사과 엑셀 요약 요청", "숫자 열 · 글자 열 구분 요청", "엑셀 필터로 상품 수 대조"],
            [f"{DN['rows']}행 × {DN['cols']}열", f"상품 {DN['pass']} · 불량 {DN['fail']} · {DN['rate']}%", "docs/사과_요약.md"],
            files="data/apple_A07.xlsx"),
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
