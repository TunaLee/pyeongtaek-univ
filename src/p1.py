"""1교시 엑셀 데이터 구조 · Claude Code 시작.

도입(완성 시뮬레이터 · 웨이퍼와 칩 · 엑셀 행과 맵 칸) → 설명(열 네 묶음 · 판정 조건(사과 → 칩) · 채팅과 에이전트 · 에이전트 루프 · 작업 고리 · 요청 구성)
→ 적용(실습 폴더 · 환경 · 실습 1-1 사과 엑셀 요약 → 1-2 웨이퍼 엑셀 요약).
반도체 용어는 칩 · 합격/불합격 · 수율 세 개만. 측정값 이름은 「몰라도 됨」.
"""
import p0
import psim
import pviz
import sk
import viz2
from deck import lab, light
from hx import photo
from pkit import brief, chat, tag
from stats_hx import src

T = tag("1")
WN, DN = sk.WN, sk.DN
CSS = ""


def slides():
    return [
        # ── 도입
        light("완성 시뮬레이터", sk.duo("sim/apple_s8.webp", "sim/wafer_s8.webp", "사과 상품률 시뮬레이터", "웨이퍼 수율 시뮬레이터"), T),
        light("웨이퍼와 칩", f'<div class="phmap v3ph">{photo("wafer_photo.webp", "웨이퍼")}' + viz2.maprows([
            ("칩", "웨이퍼 위 네모 한 칸", f"한 장에 {WN['rows']}개"), ("합격 · 불합격", "칩마다 검사 결과", "PASS · FAIL"),
            ("수율", "합격 칩 ÷ 전체 칩", f"W07 · {WN['yield']}%")], "용어", "뜻") + "</div>", T),
        light("엑셀 행과 맵 칸", psim.row_to_cell(), T),
        # ── 설명 · 데이터
        light("열 18개 네 묶음", sk.groups([
            ("이름표", ["lot_id", "wafer_id"], "어느 웨이퍼", ""),
            ("위치", ["die_x · die_y", "center_x_mm · center_y_mm", "radius_mm · zone"], "맵의 어느 칸", "k"),
            ("측정값", ["vth_v · idsat_ma · ioff_na", "rc_ohm · ox_thk_nm", "crack · particle_cnt"], "뜻은 몰라도 됨 · 기준표만", "dim"),
            ("판정", ["bin", "fail_type", "pass_fail"], "합격 · 불합격 · 사유", "k")]), T),
        light("사과 판정 조건", p0.judge_apple(), T),
        light("칩 판정 조건", p0.judge_wafer(), T),
        # ── 설명 · Claude Code
        light("채팅과 에이전트", psim.chat_vs_agent(), T),
        light("에이전트 루프", psim.agent_loop()
              + src(("Claude Code 문서 · How Claude Code works", "https://code.claude.com/docs/en/how-claude-code-works")), T),
        light("Claude Code 의 데이터 작업 고리", pviz.data_loop(), T),
        light("요청 구성", viz2.pair(
            "한 줄 요청", [("요청", "「사과 엑셀 요약해 줘」"), ("무엇을", "Claude 가 추측"), ("저장", "대화창에만 · 파일 없음")],
            "네 칸을 채운 요청", [("목표", "줄 수 · 열 묶음 · 상품 · 불량 수"), ("입력", "data/apple_A07.xlsx"),
                             ("산출물", "docs/사과_요약.md"), ("하지 말 것", "원본 수정")]), T),
        # ── 적용
        light("실습 폴더 sim-lab", viz2.maprows([
            ("data/", "wafer_test_W07.xlsx · apple_A07.xlsx", "읽기만"), ("templates/", "합격기준표 · 선별기준표 · 예시 HTML", "참고 자료"),
            ("docs/", "데이터 요약 · 실험 기록", "문서"), ("output/", "simulator.html · apple_sim.html", "교시마다 기능 추가")], "폴더", "내용"), T),
        light("실습 환경", viz2.tiles([
            ("VS Code", "편집기 · 파일 탐색기 · 터미널"), ("Claude Code 확장", "VS Code 확장 · 교육용 계정 로그인"),
            ("Python", "pandas · openpyxl"), ("sim-lab 폴더", "파일 → 폴더 열기")], 2)
              + src(("Claude Code 문서 · VS Code", "https://code.claude.com/docs/en/vs-code")), T),
        lab("1-1", "사과 엑셀 요약", T, "apple_A07.xlsx 를 Claude Code 로 읽고 줄 수 · 열 묶음 · 상품 · 불량 수를 보고받는다",
            ["sim-lab 열기 · Claude Code 실행", "사과 엑셀 요약 요청", "선별기준표로 판정 다시 요청", "grade 열과 대조"],
            [f"{DN['rows']}행 × {DN['cols']}열", f"상품 {DN['pass']} · 불량 {DN['fail']} · {DN['rate']}%"],
            files="data/apple_A07.xlsx · templates/선별기준표.md"),
        lab("1-2", "웨이퍼 엑셀 요약", T, "wafer_test_W07.xlsx 를 읽고 요약 문서를 만든다",
            ["W07 요약 요청", "합격기준표로 판정 다시 요청", "요약 문서 저장 요청", "엑셀 필터로 합격 수 대조"],
            [f"{WN['rows']}행 × {WN['cols']}열", f"합격 {WN['pass']} · 불합격 {WN['fail']} · 수율 {WN['yield']}%", "docs/데이터_요약.md"],
            files="data/wafer_test_W07.xlsx · templates/합격기준표.md"),
        brief("1-2", T,
              ["W07 요약 요청", "합격기준표로 판정 다시 요청", "요약 문서 저장 요청", "엑셀 필터로 합격 수 대조"],
              [("목표", "W07 의 줄 수 · 열 묶음 · 합격 · 불합격 수"), ("입력", "wafer_test_W07.xlsx · 합격기준표.md"),
               ("산출물", "docs/데이터_요약.md"), ("하지 말 것", "data/ 원본 수정 · 측정값 뜻 설명")],
              [], [f"합격 {WN['pass']} · 불합격 {WN['fail']}", "열 네 묶음"], ""),
        light("실습 1-2 확인", chat([
            ("me", "data/wafer_test_W07.xlsx 를 요약해 줘. 줄 수, 열 묶음, 합격 · 불합격 수만."),
            ("ai", f"{WN['rows']}행 × {WN['cols']}열\n이름표 2 · 위치 6 · 측정값 7 · 판정 3\n"
                   f"합격 {WN['pass']} · 불합격 {WN['fail']} · 수율 {WN['yield']}%\n불합격 1위 깨짐 · 긁힘 {WN['reason']['crack']}개")], "요약 대화 예"), T),
    ]
