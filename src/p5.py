"""5교시 불합격 차트 · 나눠서 요청하기.

도입(맵과 차트) → 설명(막대 하나의 구성 · 사유별 막대 · 위치별 합격률 · 두 칸 배치 · 한 번에 요청 vs 나눠 요청 · 파일 이름 버전 관리 · Git 커밋 · 체크포인트)
→ 적용(실습 5-1 사과 차트 → 5-2 웨이퍼 차트).
"""
import pbg
import pv3
import sk
import viz2
from deck import lab, light
from pkit import brief, tag
from v3kit import phmap
from stats_hx import hbars, src

T = tag("5")
WN, DN = sk.WN, sk.DN
TOP = max(DN["reason"], key=DN["reason"].get)
TOPK = sk.D_KO[TOP]
CSS = ""


def slides():
    zr = WN["zone"]
    return [
        # ── 도입
        light("맵과 차트", viz2.pair(
            "웨이퍼 맵", [("보여 주는 정보", "어디에 있나 · 위치"), ("읽는 법", "색이 몰린 곳"), ("예", "가장자리 · 대각선")],
            "막대 차트", [("보여 주는 정보", "얼마나 많나 · 크기"), ("읽는 법", "막대 길이 비교"), ("예", "사유별 칩 수")]), T),
        # ── 설명
        light("막대 하나의 구성", viz2.tiles([
            ("이름", "사유 · 위치"), ("길이", "칩 수 · 합격률"), ("숫자", "막대 끝 값"), ("순서", "많은 순")], 4), T),
        light("사과 사유별 막대", pv3.pareto([(sk.D_KO[k], v) for k, v in sorted(DN["reason"].items(), key=lambda x: -x[1])], "사과 수"), T),
        light("칩 사유별 막대", pv3.pareto([(sk.KO[k], v) for k, v in sorted(WN["reason"].items(), key=lambda x: -x[1])], "칩 수"), T),
        light("위치별 합격률 막대", hbars([(a, DN["area"][a], a == "가장자리", f"{DN['area'][a]:.2f}%") for a in sk.AREA], top=100, title="사과 · 위치별 상품률")
              + hbars([(sk.ZONE_KO[z], zr[z], False, f"{zr[z]:.2f}%") for z in ("center", "mid", "edge")], top=100, title="칩 · 위치별 합격률"), T),
        light("두 칸 배치", viz2.maprows([
            ("위", "숫자 카드 4개", "한 줄"), ("왼쪽", "웨이퍼 맵", "넓게"), ("오른쪽 위", "사유별 막대", "많은 순"),
            ("오른쪽 아래", "위치별 합격률", "3개")], "자리", "내용"), T),
        # ── 설명 · Claude 활용
        light("한 번에 요청과 나눠 요청", viz2.pair(
            "한 번에", [("요청", "「차트 두 개 · 배치 · 색 다 해 줘」"), ("결과", "여러 곳이 동시에 바뀜"), ("틀리면", "어디서 틀렸는지 모름")],
            "나눠서", [("1", "사유별 막대 → 확인"), ("2", "위치별 막대 → 확인"), ("3", "배치 → 확인")]), T),
        light("파일 이름 버전 관리", pbg.versions(), T),
        light("Git 커밋", phmap("savepoint.webp", "세이브 포인트", "AI 생성 그림 · Z-Image Turbo (Apache 2.0)",
                                "https://huggingface.co/Tongyi-MAI/Z-Image-Turbo", viz2.maprows([
            ("세이브 포인트에서 저장", "커밋 · 지금 상태를 기록", "「지금 상태 커밋해 줘」"),
            ("저장 슬롯 이름", "커밋 메시지 · 무엇을 바꿨나", "「사유별 막대 추가」"),
            ("저장 목록", "기록 · 언제 · 무엇을", "「커밋 기록 보여 줘」"),
            ("불러오기", "되돌리기 · 저장 시점 복원", "「직전 커밋으로 되돌려 줘」")], "게임", "Git · 요청 예")), T),
        light("체크포인트", viz2.tiles([
            ("자동 저장", "Claude 가 파일을 고치기 전 상태"), ("되감기", "Esc 두 번 · /rewind"),
            ("Git 과 차이", "체크포인트는 이 대화 안 · Git 은 계속 남음")], 3)
              + src(("Claude Code 문서 · Checkpointing", "https://code.claude.com/docs/en/checkpointing")), T),
        # ── 적용
        lab("5-1", "사과 차트", T, "apple_sim.html 에 불량 사유별 막대 · 위치별 상품률 막대를 넣고 두 칸으로 배치한다",
            ["사유별 막대 → 확인 · 커밋", "위치별 막대 → 확인 · 커밋", "두 칸 배치 → 확인 · 커밋", "읽히는 사실 세 가지"],
            [f"{TOPK} {max(DN['reason'].values())}개 1위", f"가장자리 {DN['area']['가장자리']:.2f}% 최저"], files="output/apple_sim.html"),
        light("사과 차트 결과", sk.one("sim/apple_s5.webp", "사과 차트"), T),
        lab("5-2", "웨이퍼 차트", T, "simulator.html 에 불합격 사유별 막대 · 위치별 합격률 막대를 넣고 맵 왼쪽 · 차트 오른쪽으로 배치한다",
            ["사유별 막대 → 확인 · 커밋", "위치별 막대 → 확인 · 커밋", "두 칸 배치 → 확인 · 커밋", "읽히는 사실 세 가지"],
            [f"깨짐 · 긁힘 {WN['reason']['crack']}개 1위", f"중심 {zr['center']:.2f}% · 가장자리 {zr['edge']:.2f}%"], files="output/simulator.html"),
        brief("5-2", T,
              ["사유별 막대", "위치별 막대", "두 칸 배치", "읽히는 사실"],
              [("목표", "차트 2종 · 두 칸 배치"), ("입력", "fail_type · zone · pass_fail"),
               ("산출물", "simulator.html 맵 오른쪽"), ("하지 말 것", "맵 · 카드 지우기 · 한 번에 다 요청")],
              [], [f"막대 합계 {WN['fail']}", "커밋 3개"], ""),
        light("웨이퍼 차트 결과", sk.one("sim/wafer_s5.webp", "웨이퍼 차트"), T),
    ]
