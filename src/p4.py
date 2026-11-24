"""4교시 웨이퍼 맵 · 화면 보고 고치기.

도입(표와 맵) → 설명(좌표에서 사각형까지 · 과수원 지도 · 색과 범례 · 칩 정보 풍선 · 흐린 요청과 구체적 요청 · 화면 캡처 첨부)
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


def orchard_map():
    """과수원 나무 30 × 20 · 칸 하나 = 사과 하나 · 상품 초록 · 불량 빨강."""
    df = sk.D07
    s = '<svg viewBox="0 0 612 412" style="width:100%;max-height:430px;display:block;margin:0 auto">'
    for r in df.itertuples():
        c = "#2BA84A" if r.grade == "상품" else "#E8344E"
        s += (f'<rect x="{(r.tree_x - 1) * 20 + 6}" y="{(20 - r.tree_y) * 20 + 6}" width="18" height="18" rx="3" fill="{c}">'
              f'<title>{r.apple_id} {r.grade}</title></rect>')
    return s + "</svg>"


def slides():
    return [
        # ── 도입
        light("표와 맵", pv4.table_vs_map(), T),
        # ── 설명
        light("좌표에서 사각형까지", pv4.coord_to_rect(), T),
        light("과수원 지도", f'<div class="twocol w"><div>{orchard_map()}</div><div>'
              + viz2.tiles([("칸", "나무 한 그루 · tree_x · tree_y"), ("색", f"상품 초록 {DN['pass']}칸 · 불량 빨강 {DN['fail']}칸"),
                            ("가장자리", f"상품률 {DN['area']['가장자리']}% · 안쪽 {DN['area']['안쪽']}%")], 1) + "</div></div>", T),
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
        lab("4-1", "과수원 지도", T, "apple_sim.html 카드 아래에 나무 30 × 20 칸 지도를 그리고 색 · 범례 · 풍선을 넣는다",
            ["나무 칸 그리기 요청", "상품 · 불량 색 · 범례 요청", "풍선 요청", "캡처 첨부로 고치기"],
            [f"초록 {DN['pass']}칸 · 빨강 {DN['fail']}칸", f"가장자리 상품률 {DN['area']['가장자리']}%"], files="output/apple_sim.html"),
        light("과수원 지도 결과", sk.one("sim/apple_s4.webp", "과수원 지도"), T),
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
