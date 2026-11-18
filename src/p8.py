"""8교시 분석 리포트 · 발표.

배경(차트에서 결정까지) → 분석 요약 네 칸 애니메이션 → 결과 → 원인 후보 3건(웨이퍼 맵 · 숫자) → 근거 묶기
→ 상관과 원인(날짜와 설비가 겹침 애니메이션) → 추가 확인 → Git 기록 · README → 발표 2분 → 사람이 정할 것 → 내 데이터 적용 → 실습 8.
숫자는 labs/ref.json · labs/solution/output(slide_numbers.json · git_log_example.txt) · docs/analysis_summary.md 에서 읽는다.
"""
import json

import pv8
import viz2
from deck import flow, lab, light
from hx import code, esc, note
from pkit import REF, SOL, brief, chat, shot, tag
from stats_hx import big, src

T = tag("8")
NUM = json.loads((SOL / "output" / "slide_numbers.json").read_text(encoding="utf-8"))
EQ = {e["eqp"]: e for e in NUM["eqp_yield"]}
E3 = EQ["ETCH_03"]
Z = NUM["eqp_zone"]
F = NUM["eqp_fail"]
WF = NUM["wafer_fail"]
LOT_Y = json.loads((SOL / "output" / "w26_rerun.json").read_text(encoding="utf-8"))["before"]["lot_yield"]  # 정제 뒤 LOT 수율
GITLOG = (SOL / "output" / "git_log_example.txt").read_text(encoding="utf-8").strip()
README = (SOL / "README.md").read_text(encoding="utf-8")

OS_OTHERS = [v for k, v in WF.items() if k.endswith("|open_short") and not k.startswith("W12")]
CRACK_WAFERS = sorted({k.split("|")[0] for k in WF if k.endswith("|crack")})
def _clean_yield(w):
    """정제 뒤 수율 — DuckDB 결과와 같은 기준 (W19 재측정 9개 반영)."""
    import sys
    import pandas as pd
    sys.path.insert(0, str(SOL / "scripts"))
    from clean import clean
    df, _ = clean(pd.read_csv(SOL.parent / "wafer-lab" / "data" / "raw" / f"wafer_test_{w}.csv"))
    return round((df.pass_fail == "PASS").mean() * 100, 2)


SAME_DAY = [(w, REF["wafers"][w]["eqp"], _clean_yield(w)) for w in ("W16", "W17", "W18", "W19", "W20")]
DATE_ROWS = [(d, v[0], v[1]) for d, v in sorted(NUM["date"].items())]
E1_OTHERS = [v["yield"] for w, v in REF["wafers"].items() if v["eqp"] == "ETCH_01" and w != "W07"]
CH3 = (NUM["chamber"]["ETCH_03|CHA"], NUM["chamber"]["ETCH_03|CHB"])


def _readme():
    """README 의 실행 표 → 「교시 · 명령」 두 칸만 (한 줄이 화면 폭을 넘지 않게)."""
    out = ["# 웨이퍼 테스트 분석", "", "## 실행"]
    for ln in README.splitlines():
        if ln.startswith("| ") and "python" in ln:
            c = [x.strip().strip("`") for x in ln.strip("|").split("|")]
            out.append(f"{c[0]:>5}교시  {c[1].split(' · ')[0].strip('`')}")
    return "\n".join(out[:10])


def slides():
    return [
        # ── 배경
        light("차트에서 결정까지", viz2.tiles([
            ("읽는 사람", "팀장 · 공정 엔지니어 · 설비 담당"), ("필요한 것", "무엇이 문제 · 왜 그렇게 보나 · 다음에 할 일"),
            ("대시보드만 보내면", "차트 해석이 사람마다 다름")], 3), T),
        light("분석 요약 네 칸", pv8.summary([
            ("결과", f"LOT 수율 {LOT_Y}% · 목표 미달 {E3['below']}장"),
            ("원인 후보", "ETCH_03 가장자리 · W07 스크래치 · W12 중심 오픈·쇼트"),
            ("근거", "SQL 뷰 숫자 · 설비별 · 존별 수율 · 웨이퍼 맵"),
            ("추가 확인", "날짜 · 챔버 영향 · 장비 이력")]), T),
        light("결과", big([
            (f"{LOT_Y}", "%", "LOT 수율 · 웨이퍼 25장"), (f"{E3['below']}", "장", "목표 90% 미달", True),
            (f"{E3['yield']}", "%", "ETCH_03 평균 · 나머지 두 설비 93%대")], 3), T),
        light("원인 후보 1 · ETCH_03 가장자리", shot("p8_wafer_map_W21.webp", "W21 (ETCH_03) · 수율 최저", [
            ("edge 존 수율", f"ETCH_03 {Z['ETCH_03|edge']}% · ETCH_01 {Z['ETCH_01|edge']}% · ETCH_02 {Z['ETCH_02|edge']}%"),
            ("누설전류", f"ETCH_03 {F['ETCH_03|leakage']}개 · 나머지 {F['ETCH_01|leakage']} · {F['ETCH_02|leakage']}개"),
            ("문턱전압 이탈", f"ETCH_03 {F['ETCH_03|vth_shift']}개 · 나머지 {F['ETCH_01|vth_shift']} · {F['ETCH_02|vth_shift']}개")]), T),
        light("원인 후보 2 · W07 스크래치", shot("sol_wafer_map_W07.webp", "W07 (ETCH_01) · 크랙이 대각선 한 줄", [
            ("크랙", f"{REF['wafers']['W07']['crack']}개 · LOT 에서 {', '.join(CRACK_WAFERS)} 에만"),
            ("모양", "대각선 한 줄로 이어짐 · 무작위 분포와 다름"),
            ("수율", f"{REF['wafers']['W07']['yield']}% · 같은 설비 다른 웨이퍼 {min(E1_OTHERS):.0f}~{max(E1_OTHERS):.0f}%")]), T),
        light("원인 후보 3 · W12 중심 오픈·쇼트", shot("p8_wafer_map_W12.webp", "W12 (ETCH_02) · 중심에 오픈·쇼트 묶음", [
            ("오픈·쇼트", f"{WF['W12|open_short']}개 · 다른 웨이퍼 {min(OS_OTHERS)}~{max(OS_OTHERS)}개"),
            ("center 존 수율", f"{NUM['wafer_zone']['W12|center']}% · 같은 웨이퍼 mid {NUM['wafer_zone']['W12|mid']}%"),
            ("모양", "중심 근처에 뭉침 · 무작위 분포와 다름")]), T),
        light("근거 묶기", viz2.maprows([
            ("주장", "ETCH_03 가장자리 불량", "한 문장"), ("숫자", f"edge {Z['ETCH_03|edge']}% vs {Z['ETCH_01|edge']}%", "SQL 결과 그대로"),
            ("차트", "존별 수율 · W21 웨이퍼 맵", "숫자를 눈으로 확인"), ("출처", "warehouse.duckdb · eqp_zone 질의", "다시 뽑을 수 있게")], "칸", "예"), T),
        light("상관과 원인", pv8.confound_svg(DATE_ROWS, SAME_DAY), T),
        light("추가 확인", viz2.tiles([
            ("챔버", f"ETCH_03 CHA {CH3[0]}% · CHB {CH3[1]}% · 차이 작음 → 후보 제외"),
            ("장비 이력", "식각 균일도 · 정비(PM) 기록 · 이 데이터에는 없음"),
            ("다음 LOT", "ETCH_03 가장자리 수율이 반복되는지")], 3), T),
        # ── 기록 · 공유
        light("Git 커밋 기록", code("git log --oneline · 과정 프로젝트 예", esc(GITLOG)), T),
        light("README", code("README.md · 일부", esc(_readme())), T),
        light("발표 2분", flow([("결과", "20초 · KPI 세 개"), ("원인 후보", "60초 · 후보 3건"), ("근거", "30초 · 맵 · 차트 한 장씩"),
                              ("추가 확인", "10초 · 다음에 볼 것")], hl=1), T),
        light("사람이 정할 것", viz2.pair(
            "Claude Code", [("숫자 뽑기", "SQL · 집계"), ("차트 · 맵", "근거 그림"), ("초안", "analysis_summary.md")],
            "사람", [("판정 · 지표 정의", "스펙 · 수율 계산 방식"), ("원인 판단", "상관과 원인 구분"), ("다음 행동", "점검 · 재측정 결정")], hl="r")
              + src(("Claude 블로그 · How Anthropic enables self-service data analytics",
                     "https://claude.com/blog/how-anthropic-enables-self-service-data-analytics-with-claude")), T),
        light("내 데이터에 적용", flow([("데이터 사전", "열 · 단위 · 기준"), ("정제 규칙", "중복 · 단위 · 결측"), ("파이프라인", "명령 하나"),
                                    ("대시보드", "목표선 · 비교"), ("분석 요약", "근거 숫자")], hl=0), T),
        # ── 실습
        lab("8", "분석 요약 · 발표", T, "원인 후보 3건을 근거 숫자 · 차트와 묶은 분석 요약을 쓰고 2분 발표한다",
            ["원인 후보 숫자 요청 (설비 · 존 · 웨이퍼)", "분석 요약 초안 요청", "숫자 · 출처 대조", "README · 커밋", "짝꿍 발표 · 질문"],
            ["네 칸 모두 숫자 포함", "후보마다 차트 하나", "발표 2분 이내"],
            files="warehouse.duckdb · output/dashboard.html"),
        brief("8", T,
              ["후보 숫자 요청", "분석 요약 초안", "숫자 · 출처 대조", "README · 커밋", "2분 발표"],
              [("목표", "결과 · 원인 후보 · 근거 · 추가 확인 한 장"), ("입력", "SQL 뷰 · 대시보드 · 웨이퍼 맵"),
               ("산출물", "docs/analysis_summary.md · README.md"), ("하지 말 것", "숫자 없는 단정 · 원인 확정 표현")],
              [], ["후보마다 숫자 · 차트", "출처 질의를 다시 돌릴 수 있음"], ""),
        light("실습 8 확인", chat([
            ("me", "ETCH_03 가장자리 불량을 원인 후보로 쓰려고 해. 근거 숫자를 설비별로 비교해 줘."),
            ("ai", f"edge 존 수율 · ETCH_01 {Z['ETCH_01|edge']}% · ETCH_02 {Z['ETCH_02|edge']}% · ETCH_03 {Z['ETCH_03|edge']}%\n"
                   f"누설전류 · {F['ETCH_01|leakage']} · {F['ETCH_02|leakage']} · {F['ETCH_03|leakage']}개\n"
                   "출처 · warehouse.duckdb (dies × equipment)")], "근거 대화 예"), T),
    ]

