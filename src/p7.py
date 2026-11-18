"""7교시 자동화 · 대시보드.

배경(매일 들어오는 파일 · 자동화의 조건) → 비유(자동 세차장) → 새 파일 하나 · 명령 하나 애니메이션 → run_all.py
→ 대시보드 구성 · 차트 고르는 기준 · 목표선과 색 → 원인 후보 좁히기 애니메이션 → W26 반영 → 정기 실행(claude -p) → 점검 → 실습 7.
숫자는 labs/solution/output(slide_numbers.json · w26_rerun.json)에서 읽는다.
"""
import json

import pv7
import viz2
from deck import lab, light
from hx import checks, code, esc, note
from pkit import SOL, brief, chat, codemap, shot, tag
from stats_hx import src

T = tag("7")
NUM = json.loads((SOL / "output" / "slide_numbers.json").read_text(encoding="utf-8"))
RE = json.loads((SOL / "output" / "w26_rerun.json").read_text(encoding="utf-8"))
B, A = RE["before"], RE["after"]
EQ = NUM["eqp_yield"]
EDGE = [(e["eqp"], NUM["eqp_zone"][f"{e['eqp']}|edge"]) for e in EQ]
F = NUM["eqp_fail"]


def _fails():
    """불량 유형별 ETCH_03 개수 vs 나머지 두 설비 평균 — 차이가 큰 두 유형."""
    out = []
    for t, ko in (("leakage", "누설전류"), ("vth_shift", "문턱전압 이탈")):
        other = round((F.get(f"ETCH_01|{t}", 0) + F.get(f"ETCH_02|{t}", 0)) / 2)
        out.append((ko, F[f"ETCH_03|{t}"], other))
    return out


RUN = [('for s in ("pipeline.py", "dashboard.py"):', "pipeline → dashboard 순서"),
       ('    print(f"── {s}")', "지금 단계를 화면에 표시"),
       ('    runpy.run_path(HERE / s, run_name="__main__")', "그 스크립트를 실행")]

CLAUDE_P = 'claude -p "output/pipeline_log.md 를 읽고\n  검증 실패한 파일과 이유를 세 줄로 요약해 줘"'


def slides():
    return [
        # ── 배경
        light("매일 들어오는 파일", viz2.tiles([
            ("새 LOT", "웨이퍼 25장이 한꺼번에"), ("재측정", "같은 웨이퍼 파일이 다시"), ("새 설비", "equipment.csv 에 한 줄 추가")], 3)
              + note("손으로 다시 만들면", "차트마다 숫자가 어긋남 · 어느 파일까지 반영했는지 모름"), T),
        light("자동화의 조건", viz2.tiles([
            ("입력 위치 고정", "새 파일은 data/raw/ 에만"), ("명령 하나", "python scripts/run_all.py"),
            ("검증 실패면 멈춤", "틀린 숫자를 그리지 않음"), ("결과 위치 고정", "output/dashboard.html")], 2), T),
        light("비유 · 자동 세차장", viz2.maprows([
            ("차를 넣음", "입구에 차 한 대", "data/raw/ 에 파일 하나"), ("버튼 하나", "시작 버튼", "run_all.py"),
            ("정해진 순서", "세척 → 헹굼 → 건조", "정제 → 적재 → 집계 → 그리기"), ("나오는 차", "몇 대를 넣어도 같은 상태", "dashboard.html")],
            "세차장", "파이프라인"), T),
        light("새 파일 하나 · 명령 하나", pv7.new_file(B, A), T),
        light("run_all.py", codemap(RUN, ask="파이프라인과 대시보드를 명령 하나로", title="scripts/run_all.py · 핵심 세 줄"), T),
        # ── 대시보드
        light("대시보드 구성", shot("p7_dash_mid.webp", "output/dashboard.html · 가운데 줄", [
            ("위 · KPI", f"LOT 수율 {B['lot_yield']}% · 미달 {B['below_target']}장"), ("위 · 웨이퍼별 수율", "목표선 90% · 점 색 = 설비"),
            ("가운데 · 설비별 · Pareto", "평균 수율 · 불량 유형 순위"), ("아래 · 웨이퍼 맵", "최저 수율 웨이퍼")]), T),
        light("차트 고르는 기준", viz2.tiles([
            ("비교", "막대 · 설비별 평균 수율"), ("순서 · 추이", "선 · 웨이퍼 번호순 수율"),
            ("순위", "Pareto · 많은 불량 유형부터"), ("위치", "웨이퍼 맵 · 다이 좌표")], 2)
              + note("분포", "히스토그램 · 측정값이 스펙 안에 얼마나 들어오나"), T),
        light("목표선과 색", shot("p7_dash_top.webp", "웨이퍼별 수율 · 목표 90%", [
            ("목표선", "90% 빨간 점선 · 아래가 미달"), ("점 색", "남 ETCH_01 · 하늘 ETCH_02 · 주황 ETCH_03"),
            ("읽히는 것", f"주황 점 {B['etch03']['wafers']}장이 모두 선 아래")]), T),
        light("원인 후보 좁히기", pv7.narrow(B["lot_yield"], [(e["eqp"], e["yield"]) for e in EQ], EDGE, _fails()), T),
        light("W26 반영", shot("p7_dash26_top.webp", "W26 을 넣고 run_all.py 한 번", [
            ("웨이퍼", f"{B['wafers']}장 → {A['wafers']}장"), ("LOT 수율", f"{B['lot_yield']}% → {A['lot_yield']}%"),
            ("목표 미달", f"{B['below_target']}장 → {A['below_target']}장 · W26 도 ETCH_03")]), T),
        # ── 정기 실행
        light("정기 실행", pv7.schedule(), T),
        light("claude -p", code("터미널 · 대화 없이 한 번 실행", esc(CLAUDE_P))
              + viz2.tiles([("-p", "질문 하나 → 답 출력 → 종료"), ("쓰는 곳", "예약 작업 · 스크립트 안"),
                            ("결과", "글 요약 · 사람이 읽고 판단")], 3)
              + src(("Claude Code 문서 · Overview", "https://code.claude.com/docs/en/overview")), T),
        light("대시보드 점검", checks([
            ("KPI 숫자가 SQL 결과와 같은가", f"LOT {B['lot_yield']}%"), ("목표선이 90% 에 있는가", "축 눈금과 대조"),
            ("점 색과 범례가 맞는가", "설비 세 개"), ("새 파일 뒤 웨이퍼 수가 늘었나", f"{B['wafers']} → {A['wafers']}")],
            "넷 다 「예」 → 공유 · 하나라도 「아니오」 → 숫자부터 다시"), T),
        # ── 실습
        lab("7", "자동화 · 대시보드", T, "명령 하나로 파이프라인과 대시보드를 다시 만들고 새 웨이퍼 파일로 확인한다",
            ["run_all.py 요청", "대시보드 요청 (KPI · 수율 선 · 설비 · Pareto · 맵)", "점검 네 가지", "data/new/ 의 W26 을 raw/ 로 옮기고 다시 실행",
             "원인 후보 한 줄 쓰기"],
            [f"웨이퍼 {A['wafers']}장 · LOT {A['lot_yield']}%", "목표선 · 범례 · 축 단위", "원인 후보 한 줄"],
            files="data/raw/ · data/new/wafer_test_W26.csv"),
        brief("7", T,
              ["run_all.py 요청", "대시보드 요청", "점검 네 가지", "W26 넣고 다시 실행", "원인 후보 한 줄"],
              [("목표", "새 파일이 들어와도 명령 하나로 같은 대시보드"), ("입력", "warehouse.duckdb 의 SQL 뷰"),
               ("산출물", "run_all.py · output/dashboard.html"), ("하지 말 것", "차트 숫자를 손으로 입력 · 외부 차트 라이브러리")],
              [], [f"W26 뒤 웨이퍼 {A['wafers']}장", f"미달 {B['below_target']} → {A['below_target']}장"], ""),
        light("실습 7 확인", chat([
            ("me", "W26 파일을 넣었어. 대시보드를 다시 만들고 바뀐 숫자만 알려 줘."),
            ("ai", f"웨이퍼 {B['wafers']} → {A['wafers']}장\nLOT 수율 {B['lot_yield']}% → {A['lot_yield']}%\n"
                   f"목표 미달 {B['below_target']} → {A['below_target']}장 (W26 · ETCH_03)")], "다시 실행 대화 예")
              + note("대조", "dashboard.html 을 새로 고침 · 웨이퍼별 수율 선 끝에 W26"), T),
    ]
