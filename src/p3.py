"""3교시 수율 집계 · 엑셀 자동화.

수율 집계(엑셀 피벗이 하던 일 · 존별 · 불량 Pareto(애니) · 엑셀 세 시트) → 웨이퍼 25장 한 번에 → 결과 대조 → 실습 3.
숫자는 W07 · 원시 25장을 직접 계산해 얻는다.
"""
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
from svg import line  # noqa: E402

T = tag("3")
W07 = W("W07")
DF = pd.read_csv(LAB / "wafer-lab" / "data" / "wafer_test_W07.csv")
OK = DF.pass_fail == "PASS"
ZONE = (DF.assign(ok=OK).groupby("zone").ok.agg(["size", "sum"]).reindex(["center", "mid", "edge"]))
ZONE["y"] = (ZONE["sum"] / ZONE["size"] * 100).round(2)
FAIL = DF[~OK].fail_type.value_counts()
TOP = FAIL.index[0]
TOP_PCT = FAIL.iloc[0] / FAIL.sum() * 100
RAW = LAB / "wafer-lab" / "data" / "raw"
WY = [(w, v["yield"], v["eqp"]) for w, v in REF["wafers"].items()]   # 테스터 판정 기준 웨이퍼별 수율
LOW = [w for w, y, _ in WY if y < 90]
XL_PASS = int(OK.sum())


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
        # ── 결함 밀도 · 수율 모델
        # ── 실습
        light("웨이퍼 25장 한 번에", line([(w, y) for w, y, _ in WY], w=1160, h=330, unit="%", target=90, ymin=84, ymax=97,
                                       color_of=lambda w: "#C62828" if REF["wafers"][w]["yield"] < 90 else "#1F3A5F"), T),
        light("집계 결과 대조", viz2.maprows([
            ("양품 수", f"스크립트 {XL_PASS}", f"엑셀 필터 PASS {XL_PASS}"), ("존별 다이 수", " · ".join(str(int(v)) for v in ZONE["size"]), "합계 616"),
            ("불량 유형 합", f"{int(FAIL.sum())}", "불량 다이 수와 같음"), ("25장 수율", f"90% 미만 {len(LOW)}장", ", ".join(LOW[:5]) + " …")], "항목", "결과"), T),
        lab("3", "수율 집계 · 엑셀 자동화", T, "W07 을 존별 · 불량 유형으로 집계해 엑셀에 저장하고, 원시 25장의 웨이퍼별 수율 표를 만든다",
            ["존별 · 불량 유형 집계 요청", "엑셀 세 시트 저장", "엑셀 필터로 대조", "25장 웨이퍼별 수율 표 요청", "90% 미만 웨이퍼 확인"],
            [f"존별 수율 center {ZONE['y']['center']}%", f"25장 중 90% 미만 {len(LOW)}장", "yield_summary.xlsx · wafer_yield.csv"],
            files="data/wafer_test_W07.csv · data/raw/*.csv"),
        brief("3", T,
              ["집계 요청 (존별 · 불량 유형)", "엑셀 저장 · 필터로 대조", "25장 수율 표 요청", "90% 미만 웨이퍼 확인", "결과 파일 열어 보기"],
              [("목표", "W07 집계 엑셀 + 웨이퍼 25장 수율 표"), ("입력", "wafer_test_W07.csv · data/raw/"),
               ("산출물", "output/yield_summary.xlsx · output/wafer_yield.csv"), ("하지 말 것", "수율 숫자를 손으로 적기")],
              [], [f"PASS {XL_PASS} · 엑셀과 같음", f"90% 미만 {len(LOW)}장"], ""),
        light("실습 3 확인", chat([
            ("me", "data/raw 의 25장 웨이퍼별 수율 표를 만들어 줘. 90% 미만인 웨이퍼만 따로 알려 줘."),
            ("ai", f"output/wafer_yield.csv 저장 · 25행\n90% 미만 {len(LOW)}장 · {', '.join(LOW)}")], "집계 대화 예"), T),
    ]
