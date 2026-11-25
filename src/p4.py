"""4교시 웨이퍼 맵 · 화면 보고 고치기.

도입(칩 좌표와 맵 칸) → 설명(색과 범례 · 칩 정보 툴팁)
→ 적용(실습 4-1 과수원 지도 → 4-2 웨이퍼 맵).
"""
import pv4
import sk
import viz2
from deck import lab, light
from pkit import brief, tag

T = tag("4")
WN, DN = sk.WN, sk.DN
CSS = ""


def slides():
    return [
        # ── 도입
        light("칩 좌표와 맵 칸", pv4.coord_to_rect(), T),
        # ── 설명
        light("색과 범례", viz2.tiles([
            ("합격", f"초록 #2BA84A · {WN['pass']}칸"), ("불합격", f"빨강 #E8344E · {WN['fail']}칸"),
            ("범례", "색 · 이름 · 개수 · 맵 옆")], 3), T),
        light("칩 정보 툴팁", pv4.tooltip(), T),
        # ── 설명 · Claude 활용
        light("캡처 첨부 전후", viz2.pair(
            "글로만 설명", [("요청", "「맵이 이상해 · 고쳐 줘」"), ("Claude", "코드만 읽고 원인 추측"), ("결과", "다른 곳이 바뀌기도 함")],
            "캡처 + 한 줄", [("첨부", "맵 화면 캡처"), ("한 줄", "「위아래가 뒤집혀 보임」"),
                          ("Claude", "화면과 코드를 함께 보고 고침")]), T),
        light("캡처 첨부 방법", viz2.tiles([
            ("캡처", "Windows · Win + Shift + S / Mac · Cmd + Shift + 4"), ("붙여 넣기", "Claude Code 입력창에 Ctrl + V"),
            ("한 줄 덧붙임", "어디가 · 어떻게 달라야 하는지"), ("확인", "고친 뒤 새로 고침 · 다시 캡처")], 2), T),
        # ── 적용
        lab("4-1", "과수원 지도", T, "apple_sim.html 카드 아래에 나무 30 × 20 칸 지도를 그리고 색 · 범례 · 툴팁을 넣는다",
            ["나무 칸 그리기 요청", "상품 · 불량 색 · 범례 요청", "툴팁 요청"],
            [f"초록 {DN['pass']}칸 · 빨강 {DN['fail']}칸", f"가장자리 상품률 {DN['area']['가장자리']:.2f}%"], files="output/apple_sim.html"),
        light("과수원 지도 결과", sk.one("sim/apple_s4.webp", "과수원 지도"), T),
        lab("4-2", "웨이퍼 맵", T, "simulator.html 카드 아래에 칩 616칸 맵을 그리고 합격 · 불합격 색 · 범례 · 툴팁을 넣는다",
            ["회색 칸 616개 요청", "합격 · 불합격 색 · 범례 요청", "칩 정보 툴팁 요청"],
            [f"초록 {WN['pass']} · 빨강 {WN['fail']}", "툴팁 값 = 엑셀 그 행"], files="output/simulator.html"),
        brief("4-2", T,
              ["회색 칸 616개", "색 · 범례", "툴팁", "캡처로 고치기"],
              [("목표", "칩 616칸 웨이퍼 맵 · 색 · 범례 · 툴팁"), ("입력", "die_x · die_y · pass_fail"),
               ("산출물", "simulator.html 카드 아래"), ("하지 말 것", "숫자 카드 지우기 · 외부 라이브러리")],
              [], [f"범례 합계 {WN['rows']}", "툴팁 값 = 엑셀 행"], ""),
        light("웨이퍼 맵 결과", sk.one("sim/wafer_s4.webp", "웨이퍼 맵"), T),
    ]
