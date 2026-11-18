"""5교시 원리 애니메이션 — 분포 · Cpk · 반경 경향 · 산점도 (접두어 s5*). 수치는 실습 원시 CSV 에서 계산."""
import csv
import math
import statistics as st

from anim import G, K, N, O, OK, R, S, W, _D, _box, _t
from pkit import LAB

RAW = LAB / "wafer-lab" / "data" / "raw"
LSL, USL = 0.38, 0.52


def dies(w):
    """원시 CSV → 정제한 dict 목록 (중복 좌표 제거 · mV → V)."""
    with (RAW / f"wafer_test_{w}.csv").open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    seen, out = set(), []
    for r in rows:
        k = (r["die_x"], r["die_y"])
        if k in seen:
            continue
        seen.add(k)
        v = float(r["vth_v"])
        r["vth"] = v / 1000 if v > 10 else v
        r["idsat"] = float(r["idsat_ma"])
        r["rad"] = float(r["radius_mm"])
        out.append(r)
    return out


def cpk(vals, lsl=LSL, usl=USL):
    mu, sd = st.mean(vals), st.stdev(vals)
    return round(min(usl - mu, mu - lsl) / (3 * sd), 2), round((usl - lsl) / (6 * sd), 2), mu, sd


# ── 히스토그램이 쌓이는 과정 ─────────────────────────────
def hist_build(w="W07"):
    """다이 616개의 vth 를 0.005 V 칸에 쌓음 → LSL · USL 선 → 스펙 밖 칸 빨강. 12초."""
    d = _D("s5a", 12)
    v = [r["vth"] for r in dies(w)]
    lo, step, nb = 0.38 - 0.02, 0.005, 50
    cnt = [0] * nb
    for x in v:
        cnt[max(0, min(nb - 1, int((x - lo) / step)))] += 1
    X = lambda x: 60 + (x - lo) / (step * nb) * 1060
    top = max(cnt)
    Y0, H = 360, 290
    s = f'<line x1="50" y1="{Y0}" x2="1130" y2="{Y0}" stroke="#9AA5B1" stroke-width="2"/>'
    for i, k in enumerate(cnt):
        if not k:
            continue
        x0 = lo + i * step
        h = H * k / top
        out = not (LSL <= x0 + step / 2 <= USL)
        grow = d.a([(0, "transform:scaleY(0)"), (4 + i * .9, "transform:scaleY(0)"), (10 + i * .9, "transform:scaleY(1)"), (100, "transform:scaleY(1)")],
                   extra="transform-box:fill-box;transform-origin:bottom")
        s += f'<rect x="{X(x0) + 1:.1f}" y="{Y0 - h:.1f}" width="{X(x0 + step) - X(x0) - 2:.1f}" height="{h:.1f}" fill="{K}" {grow}/>'
        if out:
            s += f'<rect x="{X(x0) + 1:.1f}" y="{Y0 - h:.1f}" width="{X(x0 + step) - X(x0) - 2:.1f}" height="{h:.1f}" fill="{R}" {d.show(78)}/>'
    for x in (0.38, 0.42, 0.46, 0.50, 0.54, 0.58):
        s += _t(X(x), Y0 + 20, f"{x:.2f}", "ts", extra='style="font-size:13px"')
    s += _t(1130, Y0 + 40, "vth_v (V)", "ts", "end")
    for lim, lab in ((LSL, "LSL 0.38"), (USL, "USL 0.52")):
        s += (f'<g {d.show(62)}><line x1="{X(lim):.1f}" y1="40" x2="{X(lim):.1f}" y2="{Y0}" stroke="{R}" stroke-width="2.5" stroke-dasharray="7 5"/>'
              + _t(X(lim), 28, lab, "tn", extra=f'style="fill:{R}"') + "</g>")
    k, cp, mu, sd = cpk(v)
    nout = sum(not (LSL <= x <= USL) for x in v)
    s += (f'<g {d.show(84)}><rect x="820" y="60" width="300" height="104" rx="12" fill="{W}" stroke="{G}" stroke-width="2"/>'
          + _t(970, 88, f"평균 {mu:.3f} V · σ {sd:.4f}", "tn") + _t(970, 116, f"스펙 밖 {nout}개 (빨강)", "tn", extra=f'style="fill:{R}"')
          + _t(970, 144, f"Cp {cp} · Cpk {k}", "tt", extra='style="font-size:18px"') + "</g>")
    return d.svg(1160, 400, s)


# ── Cpk 가 바뀌는 세 장면 ──────────────────────────────
def _curve(mu, sd, X, Y0, H, peak):
    pts = []
    for i in range(121):
        x = 0.32 + i * 0.0021
        y = math.exp(-((x - mu) / sd) ** 2 / 2)
        pts.append(f"{X(x):.1f},{Y0 - H * y * peak:.1f}")
    return "M" + " L".join(pts)


def _tail(mu, sd, X, Y0, H, peak, a, b):
    pts = [f"{X(a):.1f},{Y0}"]
    n = 30
    for i in range(n + 1):
        x = a + (b - a) * i / n
        pts.append(f"{X(x):.1f},{Y0 - H * peak * math.exp(-((x - mu) / sd) ** 2 / 2):.1f}")
    pts.append(f"{X(b):.1f},{Y0}")
    return "M" + " L".join(pts) + " Z"


SCENES = [(0.45, 0.015, "가운데 · 좁음"), (0.49, 0.015, "USL 쪽으로 치우침"), (0.45, 0.030, "가운데 · 넓게 퍼짐")]


def cpk_shift():
    """같은 스펙 폭에서 분포만 바꿈 — 가운데 좁음(Cpk 높음) → 한쪽 치우침(Cpk 낮음) → 넓게 퍼짐(Cp · Cpk 낮음). 15초."""
    d = _D("s5b", 15)
    X = lambda x: 60 + (x - 0.32) / 0.26 * 700
    Y0, H = 340, 260
    s = f'<line x1="50" y1="{Y0}" x2="780" y2="{Y0}" stroke="#9AA5B1" stroke-width="2"/>'
    s += f'<rect x="{X(LSL):.1f}" y="40" width="{X(USL) - X(LSL):.1f}" height="{Y0 - 40}" fill="{OK}" opacity=".06"/>'
    for lim, lab in ((LSL, "LSL"), (USL, "USL")):
        s += (f'<line x1="{X(lim):.1f}" y1="40" x2="{X(lim):.1f}" y2="{Y0}" stroke="{R}" stroke-width="2.5" stroke-dasharray="7 5"/>'
              + _t(X(lim), 28, f"{lab} {lim}", "tn", extra=f'style="fill:{R}"'))
    for x in (0.34, 0.40, 0.46, 0.52, 0.58):
        s += _t(X(x), Y0 + 20, f"{x:.2f}", "ts", extra='style="font-size:13px"')
    spans = [(2, 33), (35, 66), (68, None)]
    for i, ((mu, sd, lab), (t0, t1)) in enumerate(zip(SCENES, spans)):
        peak = 0.015 / sd
        cp = (USL - LSL) / (6 * sd)
        k = min(USL - mu, mu - LSL) / (3 * sd)
        g = f'<path d="{_curve(mu, sd, X, Y0, H, peak)}" fill="none" stroke="{K}" stroke-width="3.5"/>'
        g += f'<path d="{_tail(mu, sd, X, Y0, H, peak, USL, 0.58)}" fill="{R}" opacity=".55"/>'
        g += f'<path d="{_tail(mu, sd, X, Y0, H, peak, 0.32, LSL)}" fill="{R}" opacity=".55"/>'
        g += f'<line x1="{X(mu):.1f}" y1="{Y0}" x2="{X(mu):.1f}" y2="{Y0 - H * peak - 6:.1f}" stroke="{O}" stroke-width="2" stroke-dasharray="4 4"/>'
        s += f'<g {d.show(t0, t1)}>{g}</g>'
        y = 40 + i * 116
        s += (f'<g {d.show(t0)}><rect x="810" y="{y}" width="340" height="100" rx="14" fill="{"#FFF3E6" if i else W}" '
              f'stroke="{O if i else K}" stroke-width="2.5"/>' + _t(980, y + 28, f"{i + 1}. {lab}", "tt", extra='style="font-size:18px"')
              + _t(980, y + 58, f"μ {mu} · σ {sd}", "tm") + _t(980, y + 84, f"Cp {cp:.2f} · Cpk {k:.2f}", "tn", extra=f'style="fill:{R if k < 1 else OK}"')
              + "</g>")
    s += (f'<g {d.show(86)}>' + _t(420, 384, "Cpk = min(USL − μ, μ − LSL) ÷ 3σ · 1 미만이면 ±3σ 가 스펙을 넘음", "tn", extra='style="font-size:16px"') + "</g>")
    return d.svg(1160, 400, s)


# ── 비유 · 차선과 차 ─────────────────────────────────
def lane():
    """차선(스펙) 안의 차(분포) — 가운데 좁은 차 → 한쪽 차선에 붙은 차 → 넓은 트럭. cpk_shift 와 같은 세 장면. 15초."""
    d = _D("s5c", 15)
    s = f'<rect x="40" y="60" width="740" height="300" fill="#5B6573"/>'
    s += f'<line x1="140" y1="60" x2="140" y2="360" stroke="#fff" stroke-width="6"/><line x1="680" y1="60" x2="680" y2="360" stroke="#fff" stroke-width="6"/>'
    s += _t(140, 44, "LSL 차선", "tn", extra=f'style="fill:{R}"') + _t(680, 44, "USL 차선", "tn", extra=f'style="fill:{R}"')
    cars = [(410, 140, "#2E7D32"), (565, 140, "#E07A12"), (410, 470, "#C62828")]
    spans = [(2, 33), (35, 66), (68, None)]
    labs = [("가운데 · 좁은 차", "양쪽 여유 큼"), ("한쪽에 붙은 차", "가까운 쪽 여유 작음"), ("넓은 트럭", "양쪽 다 여유 작음")]
    for i, ((cx, w, col), (t0, t1), (h, sub)) in enumerate(zip(cars, spans, labs)):
        g = f'<rect x="{cx - w / 2:.0f}" y="150" width="{w}" height="130" rx="18" fill="{col}"/>'
        g += f'<rect x="{cx - w / 2 + 14:.0f}" y="166" width="{w - 28}" height="40" rx="8" fill="#fff" opacity=".35"/>'
        g += f'<line x1="140" y1="320" x2="{cx - w / 2:.0f}" y2="320" stroke="#FFE082" stroke-width="3" marker-end="url(#{d.id("o")})"/>'
        g += f'<line x1="680" y1="330" x2="{cx + w / 2:.0f}" y2="330" stroke="#FFE082" stroke-width="3" marker-end="url(#{d.id("o")})"/>'
        s += f'<g {d.show(t0, t1)}>{g}</g>'
        y = 40 + i * 116
        s += (f'<g {d.show(t0)}><rect x="810" y="{y}" width="340" height="100" rx="14" fill="{W}" stroke="{col}" stroke-width="2.5"/>'
              + _t(980, y + 36, f"{i + 1}. {h}", "tt", extra='style="font-size:18px"') + _t(980, y + 68, sub, "ts") + "</g>")
    s += f'<g {d.show(86)}>' + _t(410, 388, "Cpk = 가까운 차선까지 여유 ÷ 차 반폭(3σ)", "tn", extra='style="font-size:16px"') + "</g>"
    return d.svg(1160, 400, s)


# ── 반경 경향 ────────────────────────────────────────
BINS = [(0, 30), (30, 60), (60, 90), (90, 120), (120, 150)]


def radius_means(w):
    rows = dies(w)
    out = []
    for a, b in BINS:
        v = [r["vth"] for r in rows if a < r["rad"] <= b]
        out.append((f"{a}~{b}", round(st.mean(v), 4), len(v)))
    return out


def radius_trend(ws=("W07", "W21")):
    """반경 구간별 vth 평균 막대 — W07(ETCH_01) 다음 W21(ETCH_03). 바깥으로 갈수록 오름 · W21 가장자리가 더 높음. 12초."""
    d = _D("s5d", 12)
    lo, hi = 0.440, 0.490
    Y0, H = 330, 260
    Y = lambda v: Y0 - H * (v - lo) / (hi - lo)
    s = f'<line x1="70" y1="{Y0}" x2="1120" y2="{Y0}" stroke="#9AA5B1" stroke-width="2"/>'
    for v in (0.44, 0.45, 0.46, 0.47, 0.48, 0.49):
        s += f'<line x1="70" y1="{Y(v):.1f}" x2="1120" y2="{Y(v):.1f}" stroke="#EEF1F5"/>' + _t(62, Y(v), f"{v:.2f}", "ts", "end", 'style="font-size:13px"')
    cols = {"W07": K, "W21": O}
    for j, w in enumerate(ws):
        for i, (lab, m, n) in enumerate(radius_means(w)):
            x = 110 + i * 205 + j * 78
            grow = d.a([(0, "transform:scaleY(0)"), (4 + j * 40 + i * 4, "transform:scaleY(0)"), (10 + j * 40 + i * 4, "transform:scaleY(1)"), (100, "transform:scaleY(1)")],
                       extra="transform-box:fill-box;transform-origin:bottom")
            s += f'<rect x="{x}" y="{Y(m):.1f}" width="70" height="{Y0 - Y(m):.1f}" fill="{cols[w]}" {grow}/>'
            s += f'<g {d.show(10 + j * 40 + i * 4)}>' + _t(x + 35, Y(m) - 12, f"{m:.3f}", "tm", extra='style="font-size:13px"') + "</g>"
            if j == 0:
                s += _t(x + 74, Y0 + 22, f"{lab} mm", "ts", extra='style="font-size:14px"')
    s += (_t(120, 30, "W07 · ETCH_01", "tn", "start", f'style="fill:{K}"') + f'<g {d.show(42)}>'
          + _t(300, 30, "W21 · ETCH_03", "tn", "start", f'style="fill:{O}"') + "</g>")
    s += _t(600, Y0 + 50, "중심에서 거리 (radius_mm) · 막대 = 구간 평균 vth_v (V)", "ts")
    return d.svg(1160, 400, s)


# ── 산점도와 규격 영역 ────────────────────────────────
def scatter_spec(w="W07"):
    """vth × idsat 점 616개 → 규격 영역(vth 0.38~0.52 · idsat ≥ 0.92) → 밖의 점 빨강. 12초."""
    d = _D("s5e", 12)
    rows = dies(w)
    x0, x1, y0, y1 = 0.37, 0.61, 0.80, 1.20
    X = lambda v: 80 + (v - x0) / (x1 - x0) * 700
    Y = lambda v: 370 - (v - y0) / (y1 - y0) * 340
    s = f'<line x1="80" y1="370" x2="790" y2="370" stroke="#9AA5B1" stroke-width="2"/><line x1="80" y1="20" x2="80" y2="370" stroke="#9AA5B1" stroke-width="2"/>'
    for v in (0.40, 0.45, 0.50, 0.55, 0.60):
        s += _t(X(v), 388, f"{v:.2f}", "ts", extra='style="font-size:13px"')
    for v in (0.85, 0.95, 1.05, 1.15):
        s += _t(72, Y(v), f"{v:.2f}", "ts", "end", 'style="font-size:13px"')
    s += _t(800, 388, "vth_v (V)", "ts", "start") + _t(80, 10, "idsat_ma (mA)", "ts", "start")
    pts_in, pts_out = "", ""
    nout = 0
    for r in rows:
        out = not (LSL <= r["vth"] <= USL) or r["idsat"] < 0.92
        c = f'<circle cx="{X(r["vth"]):.1f}" cy="{Y(min(r["idsat"], 1.19)):.1f}" r="3.2"'
        pts_in += c + f' fill="{K}" opacity=".55"/>'
        if out:
            nout += 1
            pts_out += c + f' fill="{R}" r="5"/>'
    s += f'<g {d.show(2)}>{pts_in}</g>'
    s += (f'<g {d.show(30)}><rect x="{X(LSL):.1f}" y="20" width="{X(USL) - X(LSL):.1f}" height="{Y(0.92) - 20:.1f}" fill="{OK}" fill-opacity=".08" '
          f'stroke="{OK}" stroke-width="2.5" stroke-dasharray="7 5"/></g>')
    s += f'<g {d.show(56)}>{pts_out}</g>'
    s += (f'<g {d.show(70)}><rect x="830" y="60" width="320" height="150" rx="14" fill="{W}" stroke="{G}" stroke-width="2"/>'
          + _t(990, 92, "초록 상자 = 두 스펙을 함께 만족", "tn") + _t(990, 126, f"밖의 점 {nout}개", "tt", extra=f'style="fill:{R}"')
          + _t(990, 160, "오른쪽 덩어리 · vth 만 높음", "ts") + _t(990, 186, "아래 덩어리 · idsat 만 낮음", "ts") + "</g>")
    return d.svg(1160, 400, s)
