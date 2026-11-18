"""6교시 애니메이션 — 파이프라인 단계 · 행 저장과 열 저장 · 다시 돌려도 같은 결과. anim._D · 접두어 p6a · p6b · p6c."""
from anim import G, K, N, O, OK, R, S, W, _D, _box, _dot, _t

MO = "#FFF3E6"


def pipeline(n_raw=25, issues=3, dies=15400, views=("wafer_yield", "eqp_yield", "fail_pareto")):
    """원시 CSV 25장 → 정제 → Parquet → DuckDB → SQL 뷰. 단계마다 상자가 켜지고 점이 지나감. 16초."""
    d = _D("p6a", 16)
    s = ""
    # 1 수집 — 파일 더미
    for i in range(6):
        s += f'<g {d.show(1 + i)}><rect x="{20 + i * 6}" y="{120 - i * 6}" width="120" height="150" rx="10" fill="{W}" stroke="{K}" stroke-width="2"/></g>'
    s += f'<g {d.show(8)}>' + _t(110, 300, f"원시 CSV {n_raw}장", "tt") + _t(110, 324, "data/raw/", "tm") + "</g>"
    s += _t(110, 60, "① 수집", "to", extra='style="font-size:17px"')
    # 2 정제
    s += f'<g {d.show(14)}>' + _box(230, 120, 200, 150, "정제", "clean.py", fill=MO, stroke=O) + "</g>"
    s += _t(330, 60, "② 정제", "to", extra='style="font-size:17px"')
    for i, lab in enumerate(("중복 12행 삭제", "mV → V", "결측 → RETEST")[:issues]):
        s += f'<g {d.show(24 + i * 4)}><rect x="240" y="{290 + i * 34}" width="180" height="28" rx="14" fill="#FDECEA"/>' + _t(330, 304 + i * 34, lab, "tn", extra=f'style="fill:{R};font-size:14px"') + "</g>"
    # 3 저장 — parquet
    s += _t(560, 60, "③ 저장", "to", extra='style="font-size:17px"')
    for i in range(4):
        s += f'<g {d.show(38 + i * 2)}><rect x="{480 + i * 4}" y="{140 - i * 4}" width="150" height="110" rx="8" fill="#EAF0F7" stroke="{K}" stroke-width="2"/></g>'
    s += f'<g {d.show(44)}>' + _t(565, 196, ".parquet", "tm", extra='style="font-size:17px"') + _t(565, 290, "data/clean/", "tm") + "</g>"
    # 4 적재 — DuckDB 원통
    s += _t(790, 60, "④ 적재", "to", extra='style="font-size:17px"')
    s += (f'<g {d.show(52)}><path d="M710 120 v130 a80 22 0 0 0 160 0 v-130" fill="{K}"/><ellipse cx="790" cy="120" rx="80" ry="22" fill="#2C4C75"/>'
          + _t(790, 190, "DuckDB", "tw", extra='style="font-size:20px"') + _t(790, 218, f"dies {dies:,}행", "tw", extra='style="font-weight:500;fill:#C9D3E0;font-size:14px"') + "</g>")
    s += f'<g {d.show(56)}>' + _t(790, 300, "warehouse.duckdb", "tm") + "</g>"
    # 5 집계 — 뷰
    s += _t(1030, 60, "⑤ 집계", "to", extra='style="font-size:17px"')
    for i, v in enumerate(views):
        s += f'<g {d.show(64 + i * 5)}><rect x="930" y="{110 + i * 56}" width="210" height="44" rx="10" fill="{W}" stroke="{OK}" stroke-width="2.5"/>' + _t(1035, 132 + i * 56, v, "tm", extra=f'style="fill:{OK}"') + "</g>"
    s += f'<g {d.show(80)}>' + _t(1035, 300, "SQL 뷰 → 대시보드", "tn") + "</g>"
    # 화살표
    for x1, x2, t in ((150, 226, 12), (434, 476, 36), (636, 706, 50), (874, 926, 62)):
        s += f'<g {d.show(t)}><path d="M{x1} 195 H{x2}" stroke="{G}" stroke-width="3.5" marker-end="url(#{d.id("k")})"/></g>'
    # 지나가는 점
    pts = [(0, 80, 195, 0), (10, 80, 195, 1), (16, 330, 195, 1), (34, 330, 195, 1), (40, 560, 195, 1), (50, 560, 195, 1),
           (56, 790, 195, 1), (62, 790, 195, 1), (68, 1035, 195, 1), (70, 1035, 195, 0), (100, 1035, 195, 0)]
    s += _dot(d, pts, r=10)
    s += (f'<g {d.show(86)}><rect x="230" y="400" width="700" height="50" rx="12" fill="{MO}" stroke="{O}" stroke-width="2"/>'
          + _t(580, 426, "명령 하나 · python scripts/pipeline.py", "tt", extra='style="font-family:var(--mono,monospace);font-size:17px"') + "</g>")
    return d.svg(1160, 460, s)


def row_vs_col():
    """같은 표 · CSV 는 행 단위로 붙어 있고 Parquet 은 열 단위로 붙어 있음. vth_v 평균 한 번에 읽는 칸 수 비교. 12초."""
    d = _D("p6b", 12)
    cols = ["wafer_id", "die_x", "vth_v", "ioff_na", "pass_fail"]
    rows = 6
    s = ""
    for k, (x0, title, sub) in enumerate(((20, "CSV · 행 단위 저장", "한 줄 = 다이 한 개의 모든 열"), (600, "Parquet · 열 단위 저장", "한 묶음 = 열 하나의 모든 다이"))):
        s += _t(x0 + 270, 30, title, "tt", extra='style="font-size:20px"') + _t(x0 + 270, 58, sub, "ts")
        for j, c in enumerate(cols):
            s += _t(x0 + 46 + j * 104, 92, c, "tm", extra='style="font-size:13px"')
        for i in range(rows):
            for j in range(len(cols)):
                x, y = x0 + j * 104, 110 + i * 40
                hl = j == 2
                # CSV: 행 전체를 차례로 읽음 · Parquet: vth_v 열만 읽음
                if k == 0:
                    st = d.a([(0, f"fill:{W}"), (8 + i * 9, f"fill:{W}"), (10 + i * 9, f"fill:{'#F7C99A' if hl else '#E3E8EF'}"), (100, f"fill:{'#F7C99A' if hl else '#E3E8EF'}")])
                else:
                    st = d.a([(0, f"fill:{W}"), (8, f"fill:{W}"), (12, f"fill:{'#F7C99A' if hl else W}"), (100, f"fill:{'#F7C99A' if hl else W}")])
                s += f'<rect x="{x}" y="{y}" width="96" height="32" rx="6" stroke="{G}" stroke-width="1.5" {st}/>'
        if k == 0:
            for i in range(rows):
                s += f'<rect x="{x0 - 6}" y="{106 + i * 40}" width="532" height="40" rx="8" fill="none" stroke="{K}" stroke-width="2" {d.show(8 + i * 9, 10 + i * 9 + 6)}/>'
        else:
            s += f'<rect x="{x0 + 2 * 104 - 6}" y="104" width="108" height="{rows * 40 + 6}" rx="8" fill="none" stroke="{O}" stroke-width="3" {d.show(8)}/>'
    s += f'<line x1="580" y1="20" x2="580" y2="360" stroke="{G}" stroke-width="2" stroke-dasharray="6 6"/>'
    s += f'<g {d.show(66)}>' + _t(290, 380, "vth_v 평균 → 다섯 열 모두 읽음", "tn", extra=f'style="fill:{R}"') + "</g>"
    s += f'<g {d.show(70)}>' + _t(870, 380, "vth_v 평균 → vth_v 열만 읽음", "tn", extra=f'style="fill:{OK}"') + "</g>"
    return d.svg(1160, 400, s)


def rerun(dies=15400):
    """다시 돌렸을 때 · 덧붙이기(INSERT) 는 두 배로 쌓이고 · 바꿔 쓰기(CREATE OR REPLACE) 는 그대로. 12초."""
    d = _D("p6c", 12)
    s = ""
    for k, (y, title, cmd, col, end) in enumerate(((40, "덧붙이기", "INSERT INTO dies …", R, dies * 2),
                                                     (230, "바꿔 쓰기", "CREATE OR REPLACE TABLE dies …", OK, dies))):
        s += _t(20, y + 20, title, "tt", "start", 'style="font-size:21px"') + _t(20, y + 50, cmd, "tm", "start")
        for r in range(3):
            x = 380 + r * 250
            t = 8 + r * 26
            n = (dies * (r + 1)) if k == 0 else dies
            s += (f'<g {d.show(t)}><rect x="{x}" y="{y}" width="220" height="110" rx="14" fill="{W}" stroke="{col if r else K}" stroke-width="2.5"/>'
                  + _t(x + 110, y + 34, f"{r + 1}번째 실행", "tn") + _t(x + 110, y + 72, f"{n:,}행", "tt", extra=f'style="font-size:26px;fill:{col if r else N}"') + "</g>")
            if r:
                s += f'<g {d.show(t - 2)}><path d="M{x - 26} {y + 55} H{x - 4}" stroke="{G}" stroke-width="3" marker-end="url(#{d.id("k")})"/></g>'
    s += (f'<g {d.show(86)}><rect x="380" y="380" width="720" height="50" rx="12" fill="#E8F5E9" stroke="{OK}" stroke-width="2"/>'
          + _t(740, 406, f"몇 번을 돌려도 dies = {dies:,}행 · 같은 결과", "tt", extra=f'style="fill:{OK};font-size:18px"') + "</g>")
    return d.svg(1160, 440, s)
