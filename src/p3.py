"""3교시 수율 집계와 수율 모델.

수율 집계(엑셀 피벗이 하던 일 · 존별 · 불량 Pareto(애니) · 엑셀 세 시트) → Gross die(배경 · 세기(애니) · 근사식)
→ 결함 밀도(비유 · 결함 비(애니)) → Poisson · Negative binomial → 다이 크기별 수율(애니) · 양품 수 → 실습 3.
숫자는 labs/solution/scripts(yield_model.py) 와 W07 정제본을 직접 계산해 얻는다.
"""
import math
import sys

import pandas as pd

import pv3
import viz2
from deck import flow, lab, light
from hx import note
from pkit import LAB, REF, SOL, W, brief, chat, codemap, tag
from stats_hx import big, hbars, src

sys.path.insert(0, str(SOL / "scripts"))
from common import KO  # noqa: E402
from yield_model import gross_die_count, gross_die_formula, negbin, poisson  # noqa: E402

T = tag("3")
W07 = W("W07")
DF = pd.read_csv(LAB / "wafer-lab" / "data" / "wafer_test_W07.csv")
OK = DF.pass_fail == "PASS"
ZONE = (DF.assign(ok=OK).groupby("zone").ok.agg(["size", "sum"]).reindex(["center", "mid", "edge"]))
ZONE["y"] = (ZONE["sum"] / ZONE["size"] * 100).round(2)
FAIL = DF[~OK].fail_type.value_counts()
TOP = FAIL.index[0]
TOP_PCT = FAIL.iloc[0] / FAIL.sum() * 100
G616 = gross_die_count()
F300 = gross_die_formula(300, 10)
F294 = gross_die_formula(294, 10)
Y = W07["yield"] / 100
D0 = -math.log(Y) / 1.0                          # 다이 10×10 mm = 1 cm²
SIZES = (5, 8, 10, 12, 15, 20, 25)
ROWS = [(s, round(poisson(s * s / 100, D0) * 100, 1), round(negbin(s * s / 100, D0) * 100, 1)) for s in SIZES]
GOOD = [(s, round(gross_die_count(die=s) * poisson(s * s / 100, D0))) for s in SIZES]
RAIN, RAIN_RES, RAIN_N = pv3.rain(D0)

D_DEVRIES = ("de Vries · IEEE TSM 18(1) 2005 · doi:10.1109/TSM.2004.836656", "https://doi.org/10.1109/TSM.2004.836656")
D_CUNN = ("Cunningham · IEEE TSM 3(2) 1990 · doi:10.1109/66.53188", "https://doi.org/10.1109/66.53188")
D_STAPPER = ("Stapper · IBM J. Res. Dev. 30(3) 1986 · doi:10.1147/rd.303.0326", "https://doi.org/10.1147/rd.303.0326")

CSS = """
  .p3eq{font-size:40px; font-weight:800; color:#16233A; text-align:center; margin:18px 0 22px; letter-spacing:-.01em;}
  .p3eq em{font-style:normal; color:#F28C28;}
  .p3eq small{display:block; font-size:16px; font-weight:600; color:#6B7785; margin-top:10px;}
"""


def slides():
    return [
        # ── 수율 집계
        light("수율 집계 세 가지", viz2.tiles([
            ("전체 수율", f"양품 ÷ 전체 · W07 {W07['yield']}%"), ("존별 수율", "center · mid · edge 구역마다"),
            ("불량 유형별 개수", "어떤 불량이 많은가 · Pareto")], 3), T),
        light("피벗 테이블과 요청", viz2.maprows([
            ("행", "zone", "「존별로」"), ("값", "pass_fail 이 PASS 인 개수", "「양품 수와 수율」"),
            ("정렬", "개수 큰 순", "「많은 순으로」"), ("저장", "시트 하나", "「엑셀 시트로」")], "피벗 설정", "요청에 들어갈 말"), T),
        light("존별 수율 · W07", hbars([
            (f"center · 중심 {ZONE['size']['center']}개", ZONE["y"]["center"], True, f"{ZONE['y']['center']}%"),
            (f"mid · 중간 {ZONE['size']['mid']}개", ZONE["y"]["mid"], False, f"{ZONE['y']['mid']}%"),
            (f"edge · 가장자리 {ZONE['size']['edge']}개", ZONE["y"]["edge"], False, f"{ZONE['y']['edge']}%")], top=100), T),
        light("불량 유형 Pareto · W07", pv3.pareto([(KO[t], int(v)) for t, v in FAIL.items()]), T),
        light("엑셀 세 시트", viz2.tiles([
            ("요약", f"총 다이 {len(DF)} · 양품 {int(OK.sum())} · 불량 {int((~OK).sum())} · 수율 {W07['yield']}%"),
            ("존별", "구역 · 다이 수 · 양품 · 수율"), ("불량 유형", "유형 · 개수 · 누적 %")], 3), T),
        # ── Gross die
        light("Gross die", viz2.tiles([
            ("뜻", "웨이퍼 한 장에서 나오는 다이 수 (양불 전)"), ("정하는 것", "웨이퍼 지름 · 다이 크기 · 가장자리 제외"),
            ("쓰는 곳", "칩 원가 = 웨이퍼 값 ÷ 양품 다이 수")], 3), T),
        light("격자에 놓고 세기", pv3.gross(), T),
        light("Gross die 근사식", '<div class="p3eq">DPW = <em>π·d²</em> / 4S − <em>π·d</em> / √(2S)'
              '<small>d 웨이퍼 지름 · S 다이 면적</small></div>'
              + big([(f"{G616}", "개", "격자에 놓고 직접 센 수", True), (f"{F300:.0f}", "개", "근사식 · d = 300 mm"),
                     (f"{F294:.0f}", "개", "근사식 · d = 294 mm (가장자리 3 mm 제외)")], 3)
              + src(D_DEVRIES), T),
        # ── 결함 밀도 · 수율 모델
        light("비유 · 빗방울과 타일", viz2.maprows([
            ("빗방울", "결함 (파티클 · 결정 결함)", "웨이퍼 위 무작위 위치"), ("타일", "다이", "크기가 다이 면적"),
            ("한 방울이라도 맞은 타일", "불량 다이", "결함 하나면 불량"), ("비의 세기", "결함 밀도 D0", "cm² 당 결함 수")], "비", "웨이퍼"), T),
        light("같은 결함 · 다른 다이 크기", RAIN, T),
        light("Poisson 수율 모델", '<div class="p3eq">Y = e<sup>−A·D0</sup>'
              '<small>Y = 수율 · A = 다이 면적 (cm²) · D0 = 결함 밀도 (개/cm²)</small></div>'
              + flow([("W07 수율", f"Y = {W07['yield']}%"), ("다이 면적", "A = 1 cm²"),
                      ("D0 = −ln(Y) ÷ A", f"{D0:.3f} 개/cm²"), ("다른 다이 크기", "같은 D0 로 예상")], hl=2)
              + src(D_CUNN), T),
        light("Negative binomial 모델", '<div class="p3eq">Y = (1 + A·D0 / <em>α</em>)<sup>−α</sup>'
              '<small>α 작을수록 결함이 뭉침 · α → ∞ 이면 Poisson</small></div>'
              + viz2.pair("Poisson", [("결함", "웨이퍼 전체에 고르게"), ("큰 다이", "수율을 낮게 봄")],
                          "Negative binomial", [("결함", "한 곳에 뭉침 (클러스터)"), ("큰 다이", "Poisson 보다 높게 봄")])
              + src(D_STAPPER), T),
        light("다이 크기별 예상 수율", pv3.curve(ROWS), T),
        light("다이 크기와 양품 수", hbars([(f"{s} mm", g, s == 10, f"{g:,}개") for s, g in GOOD]), T),
        light("Claude Code 에 계산 맡기기", codemap([
            ("gross_die_count(d=300, edge=3, die=10)", f"격자로 센 Gross die · {G616}"),
            ("d0 = -math.log(0.9042) / 1.0", f"W07 수율에서 D0 · {D0:.3f}"),
            ("math.exp(-a * d0)", "Poisson 예상 수율"),
            ("(1 + a * d0 / alpha) ** (-alpha)", "Negative binomial 예상 수율")],
            ask="다이 크기별 Gross die 와 예상 수율 표를 만들어 줘", title="yield_model.py"), T),
        # ── 실습
        lab("3", "수율 집계 · 수율 모델", T, "W07 의 수율을 집계해 엑셀로 저장하고 다이 크기별 예상 수율 표를 만든다",
            ["존별 · 불량 유형 집계 요청", "엑셀 세 시트 저장", "Gross die 함수 요청 · 616 확인", "D0 · Poisson · NB 계산 요청",
             "다이 크기별 표 저장"],
            [f"존별 수율 center {ZONE['y']['center']}%", f"Gross die {G616} · D0 {D0:.3f}", "yield_summary.xlsx · die_size_yield.csv"],
            files="output/clean/W07.csv 또는 data/wafer_test_W07.csv"),
        brief("3", T,
              ["집계 요청 (존별 · 불량 유형)", "엑셀 저장 · 필터로 대조", "Gross die 세기 요청", "수율 모델 계산 요청", "다이 크기별 표 저장"],
              [("목표", "W07 수율 집계 + 다이 크기별 예상 수율"), ("입력", "W07 정제본 · 웨이퍼 300 mm · 다이 10 mm · 제외 3 mm"),
               ("산출물", "output/yield_summary.xlsx · output/die_size_yield.csv"), ("하지 말 것", "수율 숫자를 손으로 적기")],
              [], [f"Gross die {G616}", f"다이 20 mm 예상 수율 {[r for r in ROWS if r[0] == 20][0][1]}%"], ""),
        light("실습 3 확인", chat([
            ("me", "다이 크기 5~25 mm 의 Gross die 와 Poisson · NB 예상 수율 표를 만들어 줘. W07 수율로 D0 를 구해서."),
            ("ai", f"D0 = {D0:.3f}/cm² (W07 {W07['yield']}%)\n"
                   + "\n".join(f"{s} mm · Gross die {gross_die_count(die=s)} · Poisson {p}% · NB {n}%" for s, p, n in ROWS if s in (10, 20, 25))
                   + "\n저장: output/die_size_yield.csv")], "계산 대화 예"), T),
    ]
