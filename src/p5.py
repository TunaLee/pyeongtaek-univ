"""5교시 불합격 차트 · 나눠서 요청하기.

도입(맵과 차트) → 설명(막대 하나의 구성 · 사유별 막대 · 위치별 합격률 · 두 칸 배치 · 한 번에 요청 vs 나눠 요청 · Git 커밋 · 되돌리기)
→ 적용(실습 5-1 택배 차트 → 5-2 웨이퍼 차트).
"""
import pv3
import sk
import viz2
from deck import lab, light
from pkit import brief, tag
from stats_hx import hbars, src

T = tag("5")
WN, DN = sk.WN, sk.DN
CSS = ""


def slides():
    zr = WN["zone"]
    return [
        # ── 도입
        light("맵과 차트", viz2.pair(
            "웨이퍼 맵", [("보여 주는 것", "어디에 있나 · 위치"), ("읽는 법", "색이 몰린 곳"), ("예", "가장자리 · 대각선")],
            "막대 차트", [("보여 주는 것", "얼마나 많나 · 크기"), ("읽는 법", "막대 길이 비교"), ("예", "사유별 칩 수")]), T),
        # ── 설명
        light("막대 하나의 구성", viz2.tiles([
            ("이름", "사유 · 구역"), ("길이", "칩 수 · 합격률"), ("숫자", "막대 끝 값"), ("순서", "많은 순")], 4), T),
        light("택배 사유별 막대", pv3.pareto([(sk.D_KO[k], v) for k, v in sorted(DN["reason"].items(), key=lambda x: -x[1])]), T),
        light("칩 사유별 막대", pv3.pareto([(sk.KO[k], v) for k, v in sorted(WN["reason"].items(), key=lambda x: -x[1])]), T),
        light("위치별 합격률 막대", '<div class="twocol w"><div>'
              + hbars([(a, DN["area"][a], a == "외곽", f"{DN['area'][a]}%") for a in sk.AREA], top=100, title="택배 · 구역별 정시율")
              + "</div><div>"
              + hbars([(sk.ZONE_KO[z], zr[z], False, f"{zr[z]}%") for z in ("center", "mid", "edge")], top=100, title="칩 · 위치별 합격률")
              + "</div></div>", T),
        light("두 칸 배치", viz2.maprows([
            ("위", "숫자 카드 4개", "한 줄"), ("왼쪽", "웨이퍼 맵", "넓게"), ("오른쪽 위", "사유별 막대", "많은 순"),
            ("오른쪽 아래", "위치별 합격률", "3개")], "자리", "내용"), T),
        # ── 설명 · Claude 활용
        light("한 번에 요청과 나눠 요청", viz2.pair(
            "한 번에", [("요청", "「차트 두 개 · 배치 · 색 다 해 줘」"), ("결과", "여러 곳이 동시에 바뀜"), ("틀리면", "어디서 틀렸는지 모름")],
            "나눠서", [("1", "사유별 막대 → 확인"), ("2", "위치별 막대 → 확인"), ("3", "배치 → 확인")]), T),
        light("Git 커밋", viz2.maprows([
            ("커밋", "지금 상태를 저장 지점으로", "「지금 상태 커밋해 줘」"), ("기록", "언제 · 무엇을 바꿨나", "「커밋 기록 보여 줘」"),
            ("되돌리기", "저장 지점으로 돌아감", "「직전 커밋으로 되돌려 줘」")], "말", "요청 예"), T),
        light("체크포인트", viz2.tiles([
            ("자동 저장", "Claude 가 파일을 고치기 전 상태"), ("되감기", "Esc 두 번 · /rewind"),
            ("Git 과 차이", "체크포인트는 이 대화 안 · Git 은 계속 남음")], 3)
              + src(("Claude Code 문서 · Checkpointing", "https://code.claude.com/docs/en/checkpointing")), T),
        # ── 적용
        lab("5-1", "택배 차트", T, "delivery_sim.html 에 실패 사유별 막대 · 구역별 정시율 막대를 넣고 두 칸으로 배치한다",
            ["사유별 막대 → 확인 · 커밋", "구역별 막대 → 확인 · 커밋", "두 칸 배치 → 확인 · 커밋", "읽히는 사실 세 가지"],
            [f"지연 {DN['reason']['late']}건 1위", f"외곽 {DN['area']['외곽']}% 최저"], files="output/delivery_sim.html"),
        light("택배 차트 결과", sk.one("sim/delivery_s5.webp", "택배 차트"), T),
        lab("5-2", "웨이퍼 차트", T, "simulator.html 에 불합격 사유별 막대 · 위치별 합격률 막대를 넣고 맵 왼쪽 · 차트 오른쪽으로 배치한다",
            ["사유별 막대 → 확인 · 커밋", "위치별 막대 → 확인 · 커밋", "두 칸 배치 → 확인 · 커밋", "읽히는 사실 세 가지"],
            [f"깨짐 · 긁힘 {WN['reason']['crack']}개 1위", f"중심 {zr['center']}% · 가장자리 {zr['edge']}%"], files="output/simulator.html"),
        brief("5-2", T,
              ["사유별 막대", "위치별 막대", "두 칸 배치", "읽히는 사실"],
              [("목표", "차트 2종 · 두 칸 배치"), ("입력", "fail_type · zone · pass_fail"),
               ("산출물", "simulator.html 맵 오른쪽"), ("하지 말 것", "맵 · 카드 지우기 · 한 번에 다 요청")],
              [], [f"막대 합계 {WN['fail']}", "커밋 3개"], ""),
        light("웨이퍼 차트 결과", sk.one("sim/wafer_s5.webp", "웨이퍼 차트"), T),
    ]
