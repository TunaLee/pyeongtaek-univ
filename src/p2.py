"""2교시 엑셀 집계 자동화 · CLAUDE.md.

도입(손 집계와 요청) → 설명(수율 계산 · 택배 집계 · 칩 집계 · 엑셀 시트 세 장 · CSV 저장 · CLAUDE.md · 확인할 수 있는 문장 · 숫자 대조)
→ 적용(실습 2-1 택배 집계 → 2-2 웨이퍼 yield_summary.xlsx).
"""
import pv3
import sk
import viz2
from deck import lab, light
from hx import code, esc
from pkit import LAB, brief, chat, tag
from stats_hx import hbars

T = tag("2")
WN, DN = sk.WN, sk.DN
CSS = """
  .p2eq{font-size:40px; font-weight:800; color:#16233A; text-align:center; margin:30px 0 26px;}
  .p2eq em{font-style:normal; color:#F28C28;}
"""


def _claude_md():
    """sim-lab/CLAUDE.md 에서 10줄 — 제목 · 만드는 것 · 작업 규칙 셋 · 정답 숫자."""
    t = [x for x in (LAB / "sim-lab" / "CLAUDE.md").read_text(encoding="utf-8").split("\n") if x.strip()]
    i = t.index("## 작업 규칙")
    j = t.index(next(x for x in t if x.startswith("## 정답 숫자")))
    return "\n".join([t[0], t[1], t[2], t[i], t[i + 1], t[i + 3], t[i + 5], t[j], t[j + 1], t[j + 2]])


def slides():
    zr = WN["zone"]
    return [
        # ── 도입
        light("손 집계와 요청", viz2.pair(
            "엑셀 손 작업", [("수율", "필터 · 개수 세기 · 나누기"), ("사유별", "피벗 테이블 · 정렬"), ("다음 파일", "처음부터 다시")],
            "Claude Code 요청", [("수율", "「합격 수와 수율」"), ("사유별", "「사유별 칩 수 · 많은 순」"), ("다음 파일", "같은 요청 · 파일 이름만 바꿈")]), T),
        # ── 설명
        light("수율 계산", f'<div class="p2eq">수율 = <em>합격 {WN["pass"]}</em> ÷ 전체 {WN["rows"]} = <em>{WN["yield"]}%</em></div>'
              + viz2.tiles([("택배 정시율", f"정시 {DN['pass']} ÷ 전체 {DN['rows']} = {DN['rate']}%"),
                            ("같은 계산", "조건에 맞는 행 수 ÷ 전체 행 수")], 2), T),
        light("택배 집계 표", '<div class="twocol w"><div>' + hbars(
            [(f"{sk.D_KO[k]}", v, k == "late", f"{v}건") for k, v in sorted(DN["reason"].items(), key=lambda x: -x[1])], title="실패 사유별")
              + "</div><div>" + hbars([(a, DN["area"][a], a == "외곽", f"{DN['area'][a]}%") for a in sk.AREA], top=100, title="구역별 정시율")
              + "</div></div>", T),
        light("칩 사유별 개수", pv3.pareto([(sk.KO[k], v) for k, v in sorted(WN["reason"].items(), key=lambda x: -x[1])]), T),
        light("위치별 합격률", hbars([(f"{sk.ZONE_KO[z]} · {z}", zr[z], False, f"{zr[z]}%") for z in ("center", "mid", "edge")], top=100), T),
        light("엑셀 시트 세 장", viz2.tiles([
            ("요약", f"전체 {WN['rows']} · 합격 {WN['pass']} · 불합격 {WN['fail']} · 수율 {WN['yield']}%"),
            ("사유별", "사유 · 칩 수 · 많은 순"), ("위치별", "중심 · 중간 · 가장자리 · 합격률")], 3), T),
        light("화면용 CSV", viz2.maprows([
            ("엑셀 .xlsx", "칸 · 서식 · 시트 · 압축 파일", "사람이 보는 파일"), ("CSV .csv", "쉼표로 나눈 글자", "HTML 화면이 읽는 파일"),
            ("이 과정", "엑셀 → CSV 저장 → HTML 안에 넣음", "3교시부터")], "형식", "특징"), T),
        # ── 설명 · CLAUDE.md
        light("CLAUDE.md", '<div class="twocol w"><div>' + code("sim-lab/CLAUDE.md", esc(_claude_md())) + "</div><div>"
              + viz2.tiles([("읽는 때", "Claude Code 시작마다 자동"), ("담는 것", "만드는 것 · 폴더 · 데이터 · 작업 규칙 · 정답 숫자"),
                            ("고치는 때", "같은 말을 두 번 하게 될 때")], 1) + "</div></div>", T),
        light("확인할 수 있는 문장", viz2.pair(
            "흐린 규칙", [("말투", "「친절하게 답해」"), ("결과", "「깔끔하게 만들어」"), ("숫자", "「정확하게 계산해」")],
            "확인할 수 있는 규칙", [("말투", "「반도체 용어를 새로 꺼내지 않는다」"), ("결과", "「output/simulator.html 한 파일」"),
                              ("숫자", f"「정답은 {WN['rows']} · {WN['pass']} · {WN['fail']} · {WN['yield']}%」")]), T),
        light("숫자 대조", viz2.maprows([
            ("Claude 보고", f"합격 {WN['pass']}", "요청 결과"), ("엑셀 필터", f"pass_fail = PASS · {WN['pass']}행", "사람이 직접"),
            ("다르면", "어느 쪽이 맞는지 행 단위로 확인 요청", "그대로 넘어가지 않음")], "확인", "W07"), T),
        # ── 적용
        lab("2-1", "택배 집계 엑셀", T, "택배 엑셀을 실패 사유별 · 구역별로 집계해 엑셀 시트 세 장과 CSV 로 저장한다",
            ["CLAUDE.md 에 택배 정답 숫자 추가", "집계 요청 (요약 · 사유별 · 구역별)", "CSV 저장 요청", "엑셀 필터로 대조"],
            [f"정시 {DN['pass']} · {DN['rate']}%", f"지연 {DN['reason']['late']}건 1위 · 외곽 {DN['area']['외곽']}%",
             "output/delivery_summary.xlsx · delivery_D07.csv"], files="data/delivery_D07.xlsx"),
        lab("2-2", "수율 집계 엑셀", T, "W07 을 사유별 · 위치별로 집계해 yield_summary.xlsx 와 화면용 CSV 를 만든다",
            ["CLAUDE.md 정답 숫자 확인", "집계 요청 (요약 · 사유별 · 위치별)", "CSV 저장 요청", "엑셀 필터로 대조"],
            [f"수율 {WN['yield']}% · 깨짐 · 긁힘 {WN['reason']['crack']}개 1위", "output/yield_summary.xlsx (시트 3장)",
             "output/wafer_test_W07.csv"], files="data/wafer_test_W07.xlsx"),
        brief("2-2", T,
              ["CLAUDE.md 정답 숫자 확인", "집계 요청", "CSV 저장 요청", "엑셀 필터로 대조"],
              [("목표", "수율 · 사유별 · 위치별 집계"), ("입력", "wafer_test_W07.xlsx"),
               ("산출물", "yield_summary.xlsx 시트 3장 · CSV"), ("하지 말 것", "data/ 원본 수정")],
              [], [f"합격 {WN['pass']} · 수율 {WN['yield']}%", "사유 6가지 합 = 불합격 수"], ""),
        light("실습 2-2 확인", chat([
            ("me", "yield_summary.xlsx 의 사유별 시트 합계가 불합격 수와 같은지 확인해 줘."),
            ("ai", f"사유별 합계 {sum(WN['reason'].values())} · 불합격 {WN['fail']} · 같음\n"
                   + " · ".join(f"{sk.KO[k]} {v}" for k, v in WN["reason"].items()))], "확인 대화 예"), T),
    ]
