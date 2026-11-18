"""4교시 웨이퍼 맵과 불량 패턴.

배경(지도에서 보이는 것 · 표와 맵) → 원리(좌표 → 사각형 · HTML/SVG 한 파일) → 공개 데이터(WM-811K · 패턴 9종 · 비율 · 원인 후보)
→ 우리 LOT(W07 스크래치 · W12 중심 · W21 가장자리 링) → 보기 전환 · 툴팁 · 검증 → 실습 4.
맵 그림은 labs/wafer-lab/data/raw 의 실제 다이로 그린다(pv4). 캡처는 labs/solution/scripts/wafer_map.py 결과.
"""
import pv4
import viz2
from deck import lab, light
from hx import note
from pkit import REF, W, brief, chat, shot, tag
from stats_hx import big, hbars, src
from v3kit import phmap

T = tag("4")
WM811K = ("Wu · Jang · Chen, IEEE TSM 28(1) 2015 · WM-811K", "https://doi.org/10.1109/TSM.2014.2364237")
LABELED = 172950


def _fails(w):
    x = W(w)
    return sum(x[k] for k in ("crack", "open_short", "leakage", "vth_shift", "particle", "parametric"))


def _zone_fail(w):
    cnt = {"center": 0, "mid": 0, "edge": 0}
    for r in pv4.dies(w):
        if r["pass_fail"] != "PASS":
            cnt[r["zone"]] += 1
    return cnt


def slides():
    w07, w12, w21 = W("W07"), W("W12"), W("W21")
    z21 = _zone_fail("W21")
    return [
        # ── 배경
        light("지도에서 보이는 것", phmap(
            "p4_snow_map.webp", "1854 런던 콜레라 지도 · 검은 막대 = 사망자", "지도 · John Snow (1854) · 퍼블릭 도메인",
            "https://commons.wikimedia.org/wiki/File:Snow-cholera-map-1.jpg",
            viz2.maprows([("기록", "사망자 주소 목록", "표"), ("지도", "주소마다 막대", "위치"), ("보인 것", "한 펌프 주변에 몰림", "원인 후보"),
                          ("웨이퍼", "불량 다이 좌표", "웨이퍼 맵")], "1854 런던", "같은 원리")), T),
        light("표와 맵", pv4.table_vs_map(), T),
        light("웨이퍼 맵", viz2.tiles([
            ("한 칸", f"다이 하나 · 웨이퍼 한 장 = {REF['gross_die']}칸"), ("색", "양불 또는 불량 유형"),
            ("모양", "불량이 모인 위치 · 공정 문제의 단서")], 3), T),
        # ── 원리
        light("좌표에서 사각형까지", pv4.coord_to_rect(), T),
        light("HTML · SVG 한 파일", viz2.maprows([
            ("SVG", "그림을 글자로 적는 형식", "&lt;rect&gt; · &lt;circle&gt;"), ("rect 하나", "다이 하나", f"{REF['gross_die']}개"),
            ("&lt;title&gt;", "마우스를 올리면 뜨는 풍선", "툴팁"), ("HTML 한 파일", "브라우저로 열림 · 메일로 공유", "설치 없음")], "요소", "역할"), T),
        # ── 공개 데이터 · 패턴
        light("WM-811K 공개 데이터셋", big([
            ("811,457", "장", "실제 공장 웨이퍼 맵", True), ("46,393", "LOT", "수집 단위"), (f"{LABELED:,}", "장", "패턴 라벨이 붙은 맵")], 3)
              + src(WM811K), T),
        light("불량 패턴 9종", pv4.patterns() + src(WM811K), T),
        light("패턴 비율", hbars([(f"{n} · {ko}", c, n == "none", f"{c:,} · {c / LABELED * 100:.1f}%")
                               for n, ko, c in pv4.PATTERNS], top=pv4.PATTERNS[0][2])
              + src(WM811K), T),
        light("패턴과 원인 후보", viz2.maprows([
            ("Edge-Ring · 가장자리 링", "식각 · 증착의 가장자리 균일도", "설비 · 챔버"),
            ("Scratch · 스크래치", "웨이퍼 이송 · 연마(CMP) 접촉", "핸들링"),
            ("Center · 중심", "회전 도포 · 가스 흐름의 중심부", "공정 조건"),
            ("Random · 랜덤", "파티클 · 공정 환경", "청정도")], "패턴", "원인 후보"), T),
        # ── 우리 LOT
        light("W07 · 대각선 스크래치", shot("p4_wm_W07.webp", "W07 웨이퍼 맵 · wafer_map.py 결과", [
            ("수율", f"{w07['yield']}% · 양품 {w07['pass']}"), ("크랙", f"{w07['crack']}개 · 대각선 한 줄"),
            ("설비", f"{w07['eqp']} · 같은 설비 다른 웨이퍼는 크랙 0"), ("후보", "이송 · 핸들링")]), T),
        light("W12 · 중심 클러스터", shot("p4_wm_W12.webp", "W12 웨이퍼 맵 · wafer_map.py 결과", [
            ("수율", f"{w12['yield']}% · 양품 {w12['pass']}"), ("오픈 · 쇼트", f"{w12['open_short']}개 · 중심에 몰림"),
            ("설비", w12["eqp"]), ("후보", "중심부 공정 조건")]), T),
        light("W21 · 가장자리 링", shot("p4_wm_W21.webp", "W21 웨이퍼 맵 · wafer_map.py 결과", [
            ("수율", f"{w21['yield']}% · LOT 최저"), ("불량 위치", f"edge {z21['edge']} · mid {z21['mid']} · center {z21['center']}"),
            ("유형", f"누설전류 {w21['leakage']} · 문턱전압 이탈 {w21['vth_shift']}"), ("설비", f"{w21['eqp']} · 같은 설비 9장 모두 링")]), T),
        light("보기 전환과 존", pv4.view_toggle(), T),
        light("툴팁", pv4.tooltip(), T),
        light("맵 검증", viz2.tiles([
            ("칸 수", f"사각형 {REF['gross_die']}개 = CSV {REF['gross_die']}행"), ("색별 개수", f"범례 숫자 = 불량 유형 집계 (W07 불량 {_fails('W07')})"),
            ("방향", "die_y 가 큰 다이가 위쪽"), ("툴팁 값", "다이 하나를 골라 CSV 행과 대조")], 2), T),
        # ── 실습
        lab("4", "웨이퍼 맵 HTML", T, "W07 웨이퍼 맵을 HTML 한 파일로 만들고 툴팁 · 보기 전환을 넣은 뒤 W21 로 다시 그려 비교한다",
            ["W07 웨이퍼 맵 요청", "범례 · 수율 숫자 확인", "툴팁 · 보기 전환 요청", "W21 로 다시 그리기", "두 맵 비교 한 줄"],
            [f"사각형 {REF['gross_die']}개 · 범례 합계 일치", "툴팁 값 = CSV 행", "W07 대각선 · W21 가장자리 링이 보임"],
            files="data/wafer_test_W07.csv · data/raw/wafer_test_W21.csv"),
        brief("4", T,
              ["W07 맵 요청 (양불 색 · 범례 · 수율)", "브라우저로 열어 확인", "툴팁 · 보기 전환 요청", "같은 스크립트로 W21", "두 맵의 차이 한 줄 기록"],
              [("목표", "다이 위치별 양불 · 불량 유형이 보이는 맵"), ("입력", "웨이퍼 CSV 한 장 (파일 이름만 바꿔 재사용)"),
               ("산출물", "output/wafer_map_W07.html · W21.html"), ("하지 말 것", "외부 라이브러리 · 인터넷 연결 필요한 파일")],
              [], [f"범례 숫자 합 = {REF['gross_die']}", "다이 하나의 툴팁 = CSV 행"], ""),
        light("실습 4 확인", chat([
            ("me", "W07 웨이퍼 맵을 HTML 한 파일로 만들어 줘. 불량 유형별 색과 범례, 수율을 넣고 다이에 마우스를 올리면 측정값이 보이게."),
            ("ai", f"output/wafer_map_W07.html 을 만들었다.\n다이 {REF['gross_die']}개 · 양품 {w07['pass']} · 수율 {w07['yield']}%\n"
                   f"크랙 {w07['crack']}개가 왼쪽 위에서 오른쪽 아래로 이어짐")], "맵 요청 대화 예"), T),
    ]
