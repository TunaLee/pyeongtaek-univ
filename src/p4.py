"""4교시 웨이퍼 맵 · 화면 보고 고치기.

도입(표와 맵) → 설명(좌표에서 사각형까지 · 택배 구역 지도 · 색과 범례 · 칩 정보 풍선 · 흐린 요청과 구체적 요청 · 화면 캡처 첨부)
→ 적용(실습 4-1 택배 구역 지도 → 4-2 웨이퍼 맵).
"""
import pgen
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
        light("표와 맵", pv4.table_vs_map(), T),
        # ── 설명
        light("좌표에서 사각형까지", pv4.coord_to_rect(), T),
        light("택배 구역 지도", f'<div class="twocol w"><div>{pgen.city_map()}</div><div>'
              + viz2.tiles([("칸", "구역 하나 · zone_x · zone_y"), ("색", "정시율 · 초록 90% 이상 · 노랑 75~90% · 빨강 75% 미만"),
                            ("가운데", "물류센터")], 1) + "</div></div>", T),
        light("색과 범례", viz2.tiles([
            ("합격", f"초록 #2BA84A · {WN['pass']}칸"), ("불합격", f"빨강 #E8344E · {WN['fail']}칸"),
            ("범례", "색 · 이름 · 개수 · 맵 옆")], 3), T),
        light("칩 정보 풍선", pv4.tooltip(), T),
        # ── 설명 · Claude 활용
        light("흐린 요청과 구체적 요청", viz2.pair(
            "흐린 요청", [("요청", "「맵이 이상해 · 고쳐 줘」"), ("Claude", "어디가 이상한지 추측"), ("결과", "다른 곳이 바뀜")],
            "구체적 요청", [("본 것", "「맵이 위아래로 뒤집혀 보임」"), ("기대", "「die_y 가 클수록 위쪽」"),
                          ("범위", "「맵만 고치고 카드는 그대로」")]), T),
        light("화면 캡처 첨부", viz2.tiles([
            ("캡처", "Windows · Win + Shift + S / Mac · Cmd + Shift + 4"), ("붙여 넣기", "Claude Code 입력창에 Ctrl + V"),
            ("한 줄 덧붙임", "어디가 · 어떻게 달라야 하는지"), ("확인", "고친 뒤 새로 고침 · 다시 캡처")], 2), T),
        # ── 적용
        lab("4-1", "택배 구역 지도", T, "delivery_sim.html 카드 아래에 구역 격자 지도를 그리고 색 · 범례 · 풍선을 넣는다",
            ["구역 칸 그리기 요청", "정시율 색 · 범례 요청", "풍선 요청", "캡처 첨부로 고치기"],
            [f"외곽 정시율 {DN['area']['외곽']}%", "가운데에서 먼 칸일수록 빨강"], files="output/delivery_sim.html"),
        light("택배 구역 지도 결과", sk.one("sim/delivery_s4.webp", "택배 구역 지도"), T),
        lab("4-2", "웨이퍼 맵", T, "simulator.html 카드 아래에 칩 616칸 맵을 그리고 합격 · 불합격 색 · 범례 · 풍선을 넣는다",
            ["회색 칸 616개 요청", "합격 · 불합격 색 · 범례 요청", "칩 정보 풍선 요청", "캡처 첨부로 고치기"],
            [f"초록 {WN['pass']} · 빨강 {WN['fail']}", "풍선 값 = 엑셀 그 행"], files="output/simulator.html"),
        brief("4-2", T,
              ["회색 칸 616개", "색 · 범례", "풍선", "캡처로 고치기"],
              [("목표", "칩 616칸 웨이퍼 맵 · 색 · 범례 · 풍선"), ("입력", "die_x · die_y · pass_fail"),
               ("산출물", "simulator.html 카드 아래"), ("하지 말 것", "숫자 카드 지우기 · 외부 라이브러리")],
              [], [f"범례 합계 {WN['rows']}", "풍선 값 = 엑셀 행"], ""),
        light("웨이퍼 맵 결과", sk.one("sim/wafer_s4.webp", "웨이퍼 맵"), T),
    ]
