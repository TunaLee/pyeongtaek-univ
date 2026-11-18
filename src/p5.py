"""5교시 파라미터 분포 · SPC.

배경(평균은 같고 퍼짐이 다름) → 분포 · 스펙 한계 → 히스토그램 → 비유(차선과 차) → Cp · Cpk 공식 → Cpk 세 장면
→ 우리 데이터(설비별 Cpk · 반경 경향 · 산점도 · 이상 다이 목록 · 완성 화면) → 실습 5.
수치는 pv5 가 실습 원시 CSV 에서 계산한다(중복 제거 · mV → V). 공식은 NIST/SEMATECH e-Handbook.
"""
import pv5
import viz2
from deck import lab, light
from hx import code, esc, note
from pkit import SOL, brief, chat, shot, tag
from stats_hx import big, src

T = tag("5")
NIST = ("NIST/SEMATECH e-Handbook · Process capability indices", "https://www.itl.nist.gov/div898/handbook/pmc/section1/pmc16.htm")
EQP = {"ETCH_01": range(1, 9), "ETCH_02": range(9, 17), "ETCH_03": range(17, 26)}


def _eqp_stats():
    out = {}
    for e, ws in EQP.items():
        v = [r["vth"] for w in ws for r in pv5.dies(f"W{w:02d}")]
        k, cp, mu, sd = pv5.cpk(v)
        out[e] = (k, cp, mu, sd)
    return out


def _outliers():
    t = (SOL / "output" / "outliers_W07.csv").read_text(encoding="utf-8").strip().split("\n")
    cols = t[0].split(",")
    keep = [cols.index(c) for c in ("die_x", "die_y", "zone", "vth_v", "idsat_ma", "fail_type")]
    rows = [",".join(r.split(",")[i] for i in keep) for r in t[:7]]
    return "\n".join(rows), len(t) - 1


def slides():
    es = _eqp_stats()
    v07 = [r["vth"] for r in pv5.dies("W07")]
    k07, cp07, mu07, sd07 = pv5.cpk(v07)
    ol, nol = _outliers()
    rm07, rm21 = pv5.radius_means("W07"), pv5.radius_means("W21")
    return [
        # ── 배경
        light("평균은 같고 퍼짐이 다름", big([
            (f"{es['ETCH_01'][2]:.3f}", "V", "ETCH_01 · vth 평균"), (f"{es['ETCH_03'][2]:.3f}", "V", "ETCH_03 · vth 평균"),
            (f"{es['ETCH_01'][3]:.4f}", "", "ETCH_01 · 표준편차 σ"), (f"{es['ETCH_03'][3]:.4f}", "", "ETCH_03 · 표준편차 σ", True)], 4)
              + note("평균만 보면", "두 설비 차이 0.003 V · 퍼짐은 ETCH_03 이 약 1.2배"), T),
        light("분포와 스펙 한계", viz2.tiles([
            ("분포", "값이 어디에 얼마나 모였나"), ("σ · 표준편차", "평균에서 퍼진 정도"),
            ("LSL · USL", "스펙 하한 · 상한 (data/spec.csv)"), ("vth_v 스펙", "LSL 0.38 V · USL 0.52 V")], 2), T),
        light("히스토그램", pv5.hist_build("W07"), T),
        light("비유 · 차선과 차", pv5.lane(), T),
        light("Cp 와 Cpk", '<div class="twocol w"><div>' + code("공정 능력 지수", esc(
            "Cp  = (USL − LSL) / 6σ\n"
            "Cpk = min(USL − μ, μ − LSL) / 3σ\n\n"
            f"W07 vth : μ {mu07:.4f} · σ {sd07:.4f}\n"
            f"Cp  = 0.14 / {6 * sd07:.4f} = {cp07}\n"
            f"Cpk = {0.52 - mu07:.4f} / {3 * sd07:.4f} = {k07}")) + "</div><div>"
              + viz2.tiles([("Cp", "스펙 폭 ÷ 분포 폭 · 위치 무시"), ("Cpk", "가까운 쪽 스펙까지 여유 · 치우침 반영"),
                            ("1 미만", "±3σ 범위가 스펙 밖으로 나감")], 1) + "</div></div>" + src(NIST), T),
        light("분포 모양과 Cpk", pv5.cpk_shift() + src(NIST), T),
        # ── 우리 데이터
        light("설비별 vth Cpk", big([
            (f"{es['ETCH_01'][0]}", "", f"ETCH_01 · Cp {es['ETCH_01'][1]}"), (f"{es['ETCH_02'][0]}", "", f"ETCH_02 · Cp {es['ETCH_02'][1]}"),
            (f"{es['ETCH_03'][0]}", "", f"ETCH_03 · Cp {es['ETCH_03'][1]}", True)], 3)
              + note("ETCH_03", "평균은 비슷 · σ 가 커서 Cp · Cpk 모두 낮음 → 가장자리 vth 이탈과 같은 설비"), T),
        light("반경과 문턱전압", pv5.radius_trend()
              + note("경향", f"W07 중심 {rm07[0][1]:.3f} → 가장자리 {rm07[-1][1]:.3f} V · W21 가장자리 {rm21[-1][1]:.3f} V"), T),
        light("산점도와 규격 영역", pv5.scatter_spec("W07"), T),
        light("이상 다이 목록", '<div class="twocol w"><div>' + code(f"output/outliers_W07.csv · {nol}행 중 6행", esc(ol)) + "</div><div>"
              + viz2.tiles([("뽑는 조건", "vth 스펙 밖 · idsat < 0.92"), ("쓰는 곳", "맵 위치 확인 · 재측정 목록"),
                            ("대조", f"엑셀 필터 개수 = {nol}")], 1) + "</div></div>", T),
        light("완성 화면", shot("p5_spc_W07.webp", "spc_W07.html · spc.py 결과", [
            ("왼쪽", f"vth 히스토그램 · LSL · USL · Cpk {k07}"), ("오른쪽", "vth × idsat 산점도 · 규격 영역"),
            ("색", "양품 초록 · 불량 빨강"), ("파일", "HTML 한 파일 · 외부 라이브러리 없음")]), T),
        # ── 실습
        lab("5", "분포 · Cpk · 이상 다이", T, "W07 의 vth 분포와 Cpk 를 구하고, 산점도와 이상 다이 목록을 만든다",
            ["vth 히스토그램 요청 (LSL · USL 선)", "Cp · Cpk 계산 요청", "vth × idsat 산점도 요청", "이상 다이 CSV 저장", "설비별 Cpk 비교"],
            [f"W07 vth Cpk {k07}", f"이상 다이 {nol}행 · 엑셀 개수와 같음", f"ETCH_03 Cpk 가 가장 낮음 ({es['ETCH_03'][0]})"],
            files="output/clean/W07.csv · data/spec.csv"),
        brief("5", T,
              ["히스토그램 요청", "Cp · Cpk 숫자 확인", "산점도 요청", "이상 다이 CSV 요청", "설비별 Cpk 요청"],
              [("목표", "vth 퍼짐 · 스펙 여유를 숫자와 그림으로"), ("입력", "W07 정제본 · spec.csv"),
               ("산출물", "output/spc_W07.html · outliers_W07.csv"), ("하지 말 것", "스펙 숫자를 코드에 직접 적기 · spec.csv 를 읽게")],
              [], [f"Cpk {k07} · Cp {cp07}", f"이상 다이 {nol}개"], ""),
        light("실습 5 확인", chat([
            ("me", "W07 vth 의 Cp, Cpk 를 spec.csv 기준으로 계산하고 식에 들어간 값도 보여 줘."),
            ("ai", f"μ {mu07:.4f} · σ {sd07:.4f} · LSL 0.38 · USL 0.52\nCp {cp07} · Cpk {k07}\n"
                   "USL 쪽 여유가 더 작음 — 가장자리 다이의 vth 가 높음")], "Cpk 요청 대화 예")
              + note("대조", "엑셀 AVERAGE · STDEV 로 μ · σ 를 구해 같은지"), T),
    ]
