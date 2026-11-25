"""8교시 시뮬레이터 완성 · 하네스 · 발표.

도입(남은 기능) → 설명(다른 파일 불러오기 · 목표 수율 · 내려받기 · 실험 기록 · 프롬프트 · 컨텍스트 · 하네스 · 마구와 하네스 · 교시별 하네스 부품 · Hook)
→ 적용(실습 8-1 사과 완성 → 8-2 웨이퍼 완성 · 발표 · 제출물).
"""
import pbg
import psim
import sk
import viz2
from deck import lab, light
from pkit import brief, tag
from hx import C_OAI_HE, PH_HARNESS, PH_WILD
from stats_hx import src

T = tag("8")
WN, DN = sk.WN, sk.DN
CSS = ""
WS, DS = sk.SIM["wafer"], sk.SIM["apple"]
TARGET = WS["s8_target"]["target"]


def slides():
    w21, d25 = WS["s8_alt"], DS["s8_alt"]
    wp, dp = WS["s8_target"]["pick"], DS["s8_target"]["pick"]
    combo = lambda p: " · ".join(f"{x['label']} {x['display']}" for x in p["set"])  # noqa: E731
    return [
        # ── 도입
        light("남은 기능", viz2.tiles([
            ("불러오기", "다른 엑셀 · CSV 를 골라 화면 전체를 다시"), ("목표 수율", f"목표 {TARGET}% · 달성 여부 표시"),
            ("내려받기", "판정 결과 · 기준값 CSV")], 3), T),
        # ── 설명
        light("다른 파일 불러오기", viz2.maprows([
            ("W07 (처음)", f"수율 {WN['yield']}%", f"합격 {WN['pass']} / {WN['rows']}"),
            ("W21 불러옴", f"수율 {w21['rate']:.2f}%", f"합격 {w21['pass']} / {w21['total']} · 가장자리 {w21['zones']['가장자리']['rate']:.2f}%"),
            ("A07 → A25 (사과)", f"상품률 {DN['rate']}% → {d25['rate']:.2f}%", f"상품 {d25['pass']} / {d25['total']}")], "파일", "결과"), T),
        light("목표 수율 표시", sk.duo("sim/wafer_s8_loaded.webp", "sim/wafer_s8_target.webp",
                                       f"W21 · {w21['rate']:.2f}% · 목표 {TARGET}% 미달", f"{combo(wp)} → {wp['rate']:.2f}%"), T),
        light("판정 결과 내려받기", viz2.maprows([
            ("판정 결과 CSV", "칩마다 · 새 판정 · 사유", f"{WN['rows']}행"), ("기준값 CSV", "조절 바 8개 값", "실험 조건"),
            ("파일 이름", "날짜 · 시각 포함", "덮어쓰지 않음")], "파일", "내용"), T),
        light("실험 기록", viz2.maprows([
            ("실험 1", f"W21 · 누설전류 상한 30", f"{sk.yld(sk.wafer('W21'), ioff_na=(None, 30))[1]}%"),
            ("실험 2", "W21 · 문턱전압 상한 0.55", f"{sk.yld(sk.wafer('W21'), vth_v=(0.38, 0.55))[1]}%"),
            ("실험 3", combo(wp), f"{wp['rate']:.2f}% · 목표 {TARGET}% 달성")], "실험", "조건 · 수율"), T),
        # ── 설명 · 하네스 (배경 → 비유 → 이 과정의 부품)
        light("프롬프트 · 컨텍스트 · 하네스", pbg.prompt_to_harness()
              + src(("Anthropic · Effective context engineering 2025.9", "https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents"),
                    C_OAI_HE), T),
        light("마구와 하네스", pbg.harness_photo() + src(PH_WILD, PH_HARNESS), T),
        light("지금까지 쓴 하네스", viz2.tiles([
            ("CLAUDE.md · 2교시", "프로젝트 규칙 · 정답 숫자"), ("Plan Mode · 권한 · 3교시", "계획 먼저 · 확인 받기"),
            ("Git · 체크포인트 · 5교시", "되돌릴 지점"), ("검증 · 6교시", "기대 숫자 · 화면 증거"),
            ("Skill · 7교시", "반복 절차 · sim-check"), ("Hook · 8교시", "원본 보호 · 자동 차단")], 3), T),
        light("부탁과 Hook", viz2.pair(
            "CLAUDE.md 부탁", [("규칙", "「data/ 는 수정 금지」"), ("지킴", "대부분"), ("어길 때", "막을 장치 없음")],
            "Hook", [("규칙", "data/ 쓰기 직전 검사"), ("지킴", "매번 · 자동"), ("어길 때", "실행 전에 차단 · 이유를 Claude 에게")]), T),
        light("Hook 이 끼어드는 시점", psim.hook_gate()
              + src(("Claude Code 문서 · Hooks", "https://code.claude.com/docs/en/hooks")), T),
        # ── 적용
        lab("8-1", "사과 시뮬레이터 완성", T, f"다른 사과 파일 불러오기 · 목표 상품률 {TARGET}% · 결과 내려받기를 넣고 실험을 기록한다",
            ["불러오기 요청 · A25 로 확인", "목표 상품률 표시", "내려받기", "실험 세 가지 기록"],
            [f"A25 → 상품률 {d25['rate']:.2f}%", f"A07 · {combo(dp)} → {dp['rate']:.2f}%", "docs/실험기록.md"], files="output/apple_sim.html · data/apple_A25.xlsx"),
        light("사과 시뮬레이터 완성", sk.one("sim/apple_s8.webp", "사과 시뮬레이터 완성"), T),
        lab("8-2", "수율 시뮬레이터 완성", T, "불러오기 · 목표 수율 · 내려받기를 넣고 목표 수율을 맞춘 조합을 기록해 1분 발표한다",
            ["불러오기 · W21 로 확인", "목표 수율 · 내려받기", f"W21 에서 목표 {TARGET}% 조합 찾기 · 기록", "1분 발표", "폴더 제출"],
            [f"W21 → 수율 {w21['rate']:.2f}%", f"목표 {TARGET}% 조합 예 · {wp['rate']:.2f}%", "simulator.html · 실험기록.md · 내려받은 CSV"],
            files="output/simulator.html · data/wafer_test_W21.xlsx"),
        brief("8-2", T,
              ["불러오기", "목표 수율 · 내려받기", "조합 찾기 · 기록", "발표"],
              [("목표", "완성 시뮬레이터 · 실험 기록"), ("입력", "W07 · W21 엑셀"),
               ("산출물", "simulator.html · docs/실험기록.md · CSV"), ("하지 말 것", "data/ 원본 수정 · 기존 기능 지우기")],
              [], [f"W21 수율 {w21['rate']:.2f}%", f"목표 {TARGET}% 달성 조합 하나"], ""),
        light("웨이퍼 시뮬레이터 완성", sk.one("sim/wafer_s8.webp", "수율 시뮬레이터 완성"), T),
        light("1분 발표", viz2.maprows([
            ("화면", "시뮬레이터 띄우기", "10초"), ("실험", "조절 바 세 가지 · 수율 변화", "30초"),
            ("결과", f"목표 {TARGET}% 를 맞춘 조합", "10초"), ("다음", "내 엑셀로 해 볼 실험", "10초")], "순서", "내용"), T),
        light("제출물", viz2.tiles([
            ("output/", "charts/ 차트 · apple_sim.html · simulator.html · 내려받은 CSV"), ("docs/", "사과_요약.md · 데이터_요약.md · 실험기록.md"),
            ("CLAUDE.md · .claude/", "규칙 · Skill · Hook")], 3), T),
    ]
