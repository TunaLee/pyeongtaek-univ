"""6교시 데이터 파이프라인.

배경(매일 쌓이는 테스트 파일 · 업계 사례 테스트 데이터 레이크) → 비유(물류센터) → 다섯 단계 애니메이션 → 정제에서 잡은 문제
→ CSV 와 Parquet(열 저장 애니메이션 · 파일 크기) → DuckDB(SQL 한 줄 · 설비별 결과) → 다시 돌려도 같은 결과 → 기록 → 역할 → 실습 6.
숫자는 labs/ref.json · labs/solution/output(pipeline_log.md · slide_numbers.json)에서 읽는다.
"""
import json

import pv6
import viz2
from deck import lab, light
from hx import code, esc, note
from pkit import REF, SOL, brief, chat, codemap, tag
from stats_hx import big, hbars, src

T = tag("6")
NUM = json.loads((SOL / "output" / "slide_numbers.json").read_text(encoding="utf-8"))
LOG = (SOL / "output" / "pipeline_log.md").read_text(encoding="utf-8")
EQ = NUM["eqp_yield"]
E3 = next(e for e in EQ if e["eqp"] == "ETCH_03")


def _log_rows():
    """pipeline_log.md 의 표 행 → (파일, 원시 행, 정제 행, 문제)."""
    out = []
    for ln in LOG.splitlines():
        if ln.startswith("| wafer_test_"):
            f, a, b, iss, _ = [x.strip() for x in ln.strip("|").split("|")]
            out.append((f, int(a), int(b), iss))
    return out


ROWS = _log_rows()
ISSUES = [r for r in ROWS if r[3] != "-"]


def _log_excerpt():
    keep = [ln for ln in LOG.splitlines() if ln.startswith("| 파일") or ln.startswith("|---")]
    keep += [ln for ln in LOG.splitlines() if ln.startswith("| wafer_test_W0") and ("W04" in ln or "W05" in ln)]
    keep += [ln for ln in LOG.splitlines() if "W11" in ln or "W19" in ln]
    keep += [ln for ln in LOG.splitlines() if ln.startswith("- 적재")]
    return "\n".join(keep).replace(" — 해당 다이는 재측정(RETEST)으로 분류", "").replace(" — 1000으로 나눠 V로 변환", "")


SQL = [("SELECT eqp_id,", "설비마다"), ("  count(*) AS wafers,", "웨이퍼 수"), ("  round(avg(yield_pct), 2) AS yield_pct,", "평균 수율"),
       ("  sum(CASE WHEN yield_pct < 90", "목표 90% 미만인"), ("      THEN 1 ELSE 0 END) AS below_target", "웨이퍼 수"),
       ("FROM wafer_yield", "웨이퍼별 수율 뷰에서"), ("GROUP BY eqp_id", "설비별로 묶어")]


def slides():
    return [
        # ── 배경
        light("매일 쌓이는 테스트 파일", viz2.tiles([
            ("웨이퍼 한 장", f"파일 하나 · {REF['gross_die']}행"), ("LOT 하나", f"파일 25개 · {NUM['dies']:,}행"),
            ("설비 · 날짜", "LOT 가 들어올 때마다 같은 파일 묶음")], 3), T),
        light("업계 사례 · 테스트 데이터 레이크", viz2.maprows([
            ("테스트 장비", "STDF 파일", "웨이퍼 · 다이마다 결과"), ("수집", "게이트웨이", "장비에서 파일을 모음"),
            ("적재", "데이터 레이크", "한곳에 형식을 맞춰 저장"), ("분석", "대시보드 · 질의", "수율 · 불량 추적")], "단계", "AWS 반도체 사례")
              + src(("AWS 블로그 · Faster post-silicon analysis with an AWS data lake",
                     "https://aws.amazon.com/blogs/industries/faster-post-silicon-analysis-with-an-aws-data-lake")), T),
        light("비유 · 물류센터", viz2.maprows([
            ("입고", "트럭에서 상자를 내림", "수집 · data/raw/"), ("검수", "파손 · 수량 확인 · 반품", "정제 · clean.py"),
            ("선반 보관", "품목별 자리에 정리", "저장 · Parquet · DuckDB"), ("출고", "주문대로 꺼내 배송", "집계 · SQL 뷰 · 대시보드")], "물류센터", "파이프라인"), T),
        light("파이프라인 다섯 단계", pv6.pipeline(len(ROWS), len(ISSUES), NUM["dies"]), T),
        light("정제 단계에서 잡은 문제", viz2.tiles([(f[11:14], f"원시 {a}행 → 정제 {b}행 · {iss.split(' — ')[0].split(' · ')[0]}") for f, a, b, iss in ISSUES], 3), T),
        # ── 저장 형식
        light("CSV 와 Parquet", pv6.row_vs_col()
              + src(("Apache Parquet · Overview", "https://parquet.apache.org/docs/overview/")), T),
        light("같은 데이터의 파일 크기", big([
            (f"{NUM['csv_kb']:,}", "KB", f"원시 CSV {len(ROWS)}장"), (f"{NUM['parquet_kb']:,}", "KB", f"Parquet {len(ROWS)}장", True),
            (f"{round(NUM['parquet_kb'] / NUM['csv_kb'] * 100)}", "%", "CSV 대비 크기")], 3), T),
        light("DuckDB", viz2.tiles([
            ("서버 없음", "설치 · 계정 없이 파이썬 안에서 실행"), ("파일 하나", "warehouse.duckdb"),
            ("SQL 로 바로 읽기", "SELECT * FROM 'file.csv' · Parquet 도 같음"), ("라이선스", "MIT · 무료")], 2)
              + src(("DuckDB · Why DuckDB", "https://duckdb.org/why_duckdb"), ("DuckDB · CSV import", "https://duckdb.org/docs/stable/data/csv/overview")), T),
        light("SQL 한 덩어리 읽기", codemap(SQL, ask="설비별 평균 수율과 목표 미달 웨이퍼 수", title="eqp_yield 뷰"), T),
        light("설비별 수율 · SQL 결과", hbars([(e["eqp"], e["yield"], e["eqp"] == "ETCH_03", f"{e['yield']}% · {e['wafers']}장 · 미달 {e['below']}") for e in EQ],
                                         top=100, title="평균 수율 · 웨이퍼 수 · 목표 90% 미달"), T),
        light("다시 돌려도 같은 결과", pv6.rerun(NUM["dies"]), T),
        light("파이프라인 기록", code("output/pipeline_log.md · 일부", esc(_log_excerpt())), T),
        light("맡길 것과 정할 것", viz2.pair(
            "Claude Code", [("작성", "pipeline.py · SQL 뷰"), ("실행", "25장 처리 · 오류 고침"), ("기록", "pipeline_log.md")],
            "사람", [("정제 규칙", "중복 기준 · 단위 판단 · 결측 처리"), ("검증 규칙", "다이 616 · 값 범위"), ("대조", "설비별 수율을 원본에서 다시 셈")], hl="r"), T),
        # ── 실습
        lab("6", "파이프라인", T, "원시 CSV 25장을 정제해 Parquet · DuckDB 에 적재하고 설비별 수율을 SQL 로 뽑는다",
            ["clean.py 재사용 확인", "pipeline.py 요청 (정제 → Parquet → DuckDB)", "SQL 뷰 세 개 요청", "두 번 실행해 행 수 비교",
             "pipeline_log.md 확인"],
            [f"dies {NUM['dies']:,}행", f"ETCH_03 평균 {E3['yield']}% · 미달 {E3['below']}장", "두 번 돌려도 같은 행 수"],
            files="data/raw/*.csv · data/equipment.csv"),
        brief("6", T,
              ["clean.py 가 있는지 확인", "파이프라인 요청", "SQL 뷰 요청 (웨이퍼 · 설비 · 불량 유형)", "한 번 더 실행", "기록 · 숫자 대조"],
              [("목표", "원시 25장 → 정제 → 적재 → 집계를 명령 하나로"), ("입력", "data/raw/ · equipment.csv"),
               ("산출물", "pipeline.py · warehouse.duckdb · pipeline_log.md"), ("하지 말 것", "data/raw/ 수정 · 실행마다 행이 늘어나는 적재")],
              [], [f"dies {NUM['dies']:,}행", "문제 있던 3장이 기록에 남음"], ""),
        light("실습 6 확인", chat([
            ("me", "설비별 평균 수율과 목표 미달 웨이퍼 수를 SQL 로 보여 줘."),
            ("ai", "\n".join(f"{e['eqp']} · {e['wafers']}장 · {e['yield']}% · 미달 {e['below']}장" for e in EQ))], "SQL 대화 예"), T),
    ]
