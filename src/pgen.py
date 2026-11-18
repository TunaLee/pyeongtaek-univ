"""일반 예 → 반도체 적용 — 교시마다 맨 앞에 붙는 장 (build.py 가 과정 지도 다음에 넣는다).

일반 예제 = 택배 배송 데이터 (labs/make_general.py · labs/wafer-lab/data/practice). 같은 방법을 익숙한 데이터에 먼저 쓰고,
바로 다음 장에서 반도체 데이터의 무엇에 해당하는지 짝을 지어 보인다. 숫자는 practice CSV 에서 계산한다.
"""
import pandas as pd

import viz2
from anim import G, K, N, O, OK, R, W, _D, _box, _t
from deck import light
from hx import code, esc, note
from pkit import LAB, REF, tag
from stats_hx import big, hbars

P = LAB / "wafer-lab" / "data" / "practice"
GEN = REF["general"]
KO = {"late": "지연", "absent": "부재", "addr_error": "주소 오류", "damaged": "파손", "retest": "재확인"}


def _all():
    return pd.concat([pd.read_csv(f) for f in sorted((P / "raw").glob("delivery_D*.csv"))], ignore_index=True)


def _d07():
    return pd.read_csv(P / "delivery_D07.csv")


def _pair(rows, t):
    """택배 ↔ 반도체 대응표."""
    return light("반도체 적용", viz2.maprows(rows, "택배", "반도체"), t)


# ── 1교시 · 데이터 분석의 흐름 ───────────────────────────
def flow_anim():
    """질문 → 읽기 → 정제 → 집계 → 시각화 → 해석 → 자동화. 단계마다 택배 예가 아래에 붙는다. 12초."""
    d = _D("gf", 12)
    st = [("질문", "외곽 배송이 왜 늦나"), ("읽기", "열 · 행 · 단위"), ("정제", "중복 · 단위 · 결측"), ("집계", "구역별 정시율"),
          ("시각화", "구역 지도 · 막대"), ("해석", "원인 후보 · 근거"), ("자동화", "매일 같은 결과")]
    s = ""
    for i, (h, ex) in enumerate(st):
        x = 8 + i * 164
        s += f'<g {d.show(2 + i * 9)}>' + _box(x, 70, 146, 70, h, "", fill="#FFF3E6" if i == 0 else W, stroke=O if i == 0 else K) + "</g>"
        if i:
            s += f'<g {d.show(1 + i * 9)}><path d="M{x - 16} 105 H{x - 3}" stroke="{G}" stroke-width="3" marker-end="url(#{d.id("k")})"/></g>'
        s += (f'<g {d.show(5 + i * 9)}><rect x="{x}" y="160" width="146" height="64" rx="10" fill="#F4F6F9"/>'
              + _t(x + 73, 192, ex, "tn", extra='style="font-size:14px"') + "</g>")
    s += _t(8, 192, "", "ts")
    s += (f'<g {d.show(72)}><rect x="8" y="262" width="1144" height="70" rx="14" fill="{K}"/>'
          + _t(580, 297, "같은 일곱 단계 · 택배 데이터에서 먼저 → 반도체 테스트 데이터에 그대로", "tw", extra='style="font-size:19px"') + "</g>")
    s += f'<g {d.show(1)}>' + _t(8, 40, "택배 예", "to", "start", 'style="font-size:15px"') + "</g>"
    return d.svg(1160, 350, s)


def u1():
    df = _d07()
    head = df.head(4)[["date", "zone_x", "zone_y", "area", "truck_id", "delivery_min", "reason", "status"]]
    t = tag("1")
    return [
        light("데이터 분석의 흐름", flow_anim(), t),
        light("일반 예 · 택배 배송 데이터", code("delivery_D07.csv · 앞 4줄", esc(head.to_csv(index=False).strip()))
              + viz2.tiles([("한 행", "배송 1건"), ("하루 파일", f"{GEN['rows_per_day']}행 · 25일치"),
                            ("판정", f"약속 120분 안 · 파손 · 주소 · 부재 없음 → ON_TIME")], 3), t),
        light("일반 예 · 정시 도착률", big([
            (f"{GEN['D07']['on_time']}", "건", "정시 도착 (10월 7일)"), (f"{GEN['D07']['rows']}", "건", "전체 배송"),
            (f"{GEN['D07']['rate']}", "%", "정시 도착률 = 정시 ÷ 전체", True)], 3), t),
        _pair([("배송 1건 = 1행", "다이 1개 = 1행", "wafer_test_W07.csv"), ("하루 파일 25개", "웨이퍼 파일 25개", "LOT 하나"),
               ("구역 좌표 · 거리", "die_x · die_y · radius_mm", "위치"), ("정시 도착률", "수율", "양품 ÷ 전체")], t),
    ]


# ── 2교시 · 정제 ──────────────────────────────────────
def u2():
    t = tag("2")
    d05 = pd.read_csv(P / "raw" / "delivery_D05.csv")
    d11 = pd.read_csv(P / "raw" / "delivery_D11.csv")
    d19 = pd.read_csv(P / "raw" / "delivery_D19.csv")
    dup = int(d05.duplicated(subset=["order_id"]).sum())
    return [
        light("일반 예 · 택배 원시 파일의 문제", viz2.tiles([
            ("D05 · 중복", f"{len(d05)}행 중 같은 송장 번호 {dup}행"),
            ("D11 · 단위", f"weight_kg 중앙값 {d11.weight_kg.median():,.0f} — g 로 기록됨"),
            ("D19 · 결측", f"delivery_min 빈칸 {int(d19.delivery_min.isna().sum())}개")], 3)
              + note("그대로 집계하면", f"D11 평균 무게 {d11.weight_kg.mean():,.0f} kg · g → kg 로 고치면 {d11.weight_kg.mean() / 1000:.2f} kg"), t),
        _pair([("송장 번호 중복", "다이 좌표 중복", "W05 · 12행"), ("무게 g ↔ kg", "vth mV ↔ V", "W11 · 단위"),
               ("배송 시간 결측", "ioff_na 결측", "W19 · 9칸"), ("결측 = 재확인", "결측 = 재측정 (RETEST)", "판정 보류")], t),
    ]


# ── 3교시 · 집계 ──────────────────────────────────────
def u3():
    t = tag("3")
    a = GEN["area"]
    rs = GEN["reason"]
    tot = sum(rs.values())
    return [
        light("일반 예 · 구역별 정시 도착률", hbars([(k, v, k == "외곽") for k, v in a.items()], unit="%", top=100)
              + note("25일 전체", f"정시 도착률 {GEN['on_time']}%"), t),
        light("일반 예 · 실패 사유 Pareto", hbars([(KO[k], v, i == 0, f"{v:,}건 · {v / tot * 100:.0f}%") for i, (k, v) in enumerate(rs.items())]), t),
        _pair([("구역 (도심 · 중간 · 외곽)", "존 (center · mid · edge)", "groupby"), ("실패 사유 Pareto", "불량 유형 Pareto", "많은 순"),
               ("정시 도착률", "수율", "비율 집계"), ("엑셀 피벗", "엑셀 피벗 · 3시트", "yield_summary.xlsx")], t),
    ]


# ── 4교시 · 지도 ──────────────────────────────────────
def city_map():
    """구역 15×15 격자 · 칸 색 = 그 구역 정시 도착률 (25일). 외곽 고리가 붉다."""
    df = _all()
    g = df.groupby(["zone_x", "zone_y"]).status.apply(lambda s: (s == "ON_TIME").mean() * 100)
    s = '<svg viewBox="0 0 520 520" style="width:100%;max-height:430px;display:block;margin:0 auto">'
    for (x, y), v in g.items():
        c = "#2BA84A" if v >= 90 else ("#F2C94C" if v >= 75 else "#C62828")
        s += f'<rect x="{(x + 7) * 34 + 6}" y="{(7 - y) * 34 + 6}" width="32" height="32" rx="3" fill="{c}" opacity=".85"><title>({x},{y}) {v:.0f}%</title></rect>'
    s += '<circle cx="260" cy="260" r="10" fill="#16233A"/><text x="260" y="246" text-anchor="middle" font-size="13" font-weight="800" fill="#16233A">물류센터</text></svg>'
    return s


def u4():
    t = tag("4")
    leg = viz2.tiles([("초록", "정시 90% 이상"), ("노랑", "75~90%"), ("빨강", "75% 미만")], 1)
    return [
        light("일반 예 · 구역 지도", f'<div class="twocol w"><div>{city_map()}</div><div>{leg}</div></div>', t),
        _pair([("구역 격자 한 칸", "다이 한 칸", "좌표 → 사각형"), ("물류센터에서 먼 고리", "웨이퍼 가장자리 링", "Edge-Ring"),
               ("칸 색 = 정시율", "칸 색 = 불량 유형", "보기 전환"), ("표로는 안 보이는 위치", "표로는 안 보이는 패턴", "지도의 이유")], t),
    ]


# ── 5교시 · 분포와 한계 ────────────────────────────────
def _hist(vals, usl, w=560, h=280, bins=24):
    """배송 시간 히스토그램 · 약속 시간(한쪽 한계) 선 하나 · 넘는 칸은 빨강."""
    lo, hi = min(vals), max(vals)
    step = (hi - lo) / bins
    cnt = [0] * bins
    for v in vals:
        cnt[min(int((v - lo) / step), bins - 1)] += 1
    pl, pb, pt = 20, 30, 24
    sx = lambda v: pl + (w - pl - 34) * (v - lo) / (hi - lo)
    sy = lambda c: pt + (h - pt - pb) * (1 - c / (max(cnt) * 1.1))
    s = f'<svg viewBox="0 0 {w} {h}" style="width:100%;display:block">'
    for i, c in enumerate(cnt):
        x0 = lo + i * step
        s += (f'<rect x="{sx(x0):.1f}" y="{sy(c):.1f}" width="{sx(x0 + step) - sx(x0) - 1:.1f}" height="{h - pb - sy(c):.1f}" '
              f'fill="{"#C62828" if x0 + step / 2 > usl else "#1F3A5F"}"/>')
    s += (f'<line x1="{sx(usl):.1f}" y1="{pt}" x2="{sx(usl):.1f}" y2="{h - pb}" stroke="#C62828" stroke-width="2" stroke-dasharray="5 4"/>'
          f'<text x="{sx(usl):.1f}" y="{pt - 8}" font-size="14" font-weight="800" fill="#C62828" text-anchor="middle">약속 {usl}분</text>')
    for k in range(5):
        v = lo + (hi - lo) * k / 4
        s += f'<text x="{sx(v):.1f}" y="{h - 8}" font-size="13" fill="#6B7785" text-anchor="middle">{v:.0f}분</text>'
    return s + "</svg>"


def u5():
    t = tag("5")
    df = _d07()
    mu, sd = GEN["D07"]["mean_min"], GEN["D07"]["std_min"]
    cpk = (120 - mu) / (3 * sd)
    late = int((df.delivery_min > 120).sum())
    return [
        light("일반 예 · 배송 시간 분포", f'<div class="twocol w"><div>{_hist(df.delivery_min.tolist(), 120)}</div><div>'
              + viz2.tiles([("약속 시간", f"120분 · 넘은 배송 {late}건"), ("평균 · 표준편차", f"{mu}분 · {sd}분"),
                            ("Cpk (한쪽 한계)", f"(120 − {mu}) ÷ (3 × {sd}) = {cpk:.2f}")], 1) + "</div></div>", t),
        _pair([("약속 시간 120분", "USL · LSL", "spec.csv"), ("배송 시간 분포", "vth 분포", "히스토그램"),
               (f"Cpk {cpk:.2f} · 자주 늦음", "W07 vth 의 Cpk", "클수록 한계까지 여유"), ("늦은 건 목록", "스펙 밖 다이 목록", "outliers.csv")], t),
    ]


# ── 6교시 · 파이프라인 ─────────────────────────────────
def u6():
    t = tag("6")
    tr = GEN["truck"]
    sql = ("SELECT truck_id,\n  round(avg(CASE WHEN status = 'ON_TIME' THEN 100.0 ELSE 0 END), 2) AS on_time\n"
           "FROM read_csv('practice/clean/*.csv') GROUP BY truck_id")
    return [
        light("일반 예 · 매일 쌓이는 배송 파일", viz2.maprows([
            ("수집", "delivery_D01 ~ D25.csv", "하루 한 파일"), ("정제", "중복 · g 단위 · 결측", "D05 · D11 · D19"),
            ("적재", f"한 표 · {GEN['rows_per_day'] * 25:,}행", "Parquet · DuckDB"), ("집계", "차량별 정시율 SQL", "매일 같은 쿼리")], "단계", "택배"), t),
        light("일반 예 · 차량별 정시율", code("SQL", esc(sql))
              + hbars([(k, v, k == "TRUCK_C") for k, v in tr.items()], unit="%", top=100), t),
        _pair([("하루 파일", "웨이퍼 파일", "data/raw/"), ("차량 TRUCK_A/B/C", "설비 ETCH_01/02/03", "equipment.csv"),
               ("TRUCK_C 정시율 낮음", "ETCH_03 수율 낮음", "같은 SQL 모양"), ("배송 DB", "warehouse.duckdb", "다시 돌려도 같은 결과")], t),
    ]


# ── 7교시 · 현황판 ────────────────────────────────────
def u7():
    t = tag("7")
    tr = GEN["truck"]
    worst = min(tr, key=tr.get)
    return [
        light("일반 예 · 배송 현황판", big([
            (f"{GEN['on_time']}", "%", "25일 정시 도착률"), (f"{GEN['area']['외곽']}", "%", "외곽 구역", True),
            (f"{tr[worst]}", "%", f"최저 차량 {worst}", True), ("25", "일", "하루 한 파일 · 명령 하나로 갱신")], 4), t),
        _pair([("현황판 KPI", "대시보드 KPI", "LOT 수율 · 미달 장 수"), ("새 날짜 파일", "새 웨이퍼 W26", "data/new → raw"),
               ("명령 하나로 갱신", "run_all.py", "파이프라인 → 대시보드"), ("매일 아침 실행", "claude -p · 예약 실행", "정기 실행")], t),
    ]


# ── 8교시 · 원인 ──────────────────────────────────────
def u8():
    t = tag("8")
    df = _all()
    df = df[df.status.notna()]
    outer = df[df.area == "외곽"]
    by = outer.groupby("truck_id").status.apply(lambda s: round((s == "ON_TIME").mean() * 100, 1))
    return [
        light("일반 예 · 외곽 지연의 원인 후보", hbars([(k, v, k == "TRUCK_C", f"{v}%") for k, v in by.items()], unit="%", top=100,
                                                title="같은 외곽 구역 안 · 차량별 정시율")
              + note("겹침 풀기", "외곽 탓 · 차량 탓이 섞임 → 같은 구역 안에서 차량끼리 비교"), t),
        _pair([("외곽 · TRUCK_C 겹침", "가장자리 · ETCH_03 겹침", "상관 ≠ 원인"), ("같은 구역 안 비교", "같은 날 · 같은 존 안 비교", "조건 맞추기"),
               ("원인 후보 + 근거 숫자", "원인 후보 + 근거 차트", "분석 요약"), ("추가 확인 · 차량 점검", "추가 확인 · 장비 이력", "다음 행동")], t),
    ]


def slides_for(u):
    return {"1": u1, "2": u2, "3": u3, "4": u4, "5": u5, "6": u6, "7": u7, "8": u8}[u]()
