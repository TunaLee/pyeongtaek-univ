"""3교시 애니메이션 — 불량 Pareto · Gross die 세기 · 결함 비 · 다이 크기별 수율 곡선. anim._D · 접두어 p3a~p3d."""
import math
import random

from anim import G, K, N, O, OK, R, S, W, _D, _t

MO = "#FFF3E6"
RB = "#FDECEA"


def pareto(rows):
    """rows = [(이름, 개수)] 많은 순 · 막대가 차례로 차오르고 누적 % 꺾은선이 따라 그려짐. 12초."""
    d = _D("p3a", 12)
    tot = sum(v for _, v in rows)
    x0, y0, w, h = 90, 360, 980, 300
    bw = w / len(rows)
    mx = rows[0][1] * 1.1
    s = f'<line x1="{x0}" y1="{y0}" x2="{x0 + w}" y2="{y0}" stroke="#9AA5B1" stroke-width="2"/>'
    s += _t(x0 - 12, y0 - h - 6, "다이 수", "ts", "end") + _t(x0 + w + 14, y0 - h - 6, "누적 %", "ts", "start")
    cum, pts = 0, []
    for i, (name, v) in enumerate(rows):
        bh = h * v / mx
        x = x0 + i * bw + bw * .18
        t = 4 + i * 9
        s += (f'<rect x="{x:.1f}" y="{y0 - bh:.1f}" width="{bw * .64:.1f}" height="{bh:.1f}" fill="{R if i == 0 else K}" '
              f'style="transform-box:fill-box;transform-origin:bottom" {d.a([(0, "transform:scaleY(0)"), (t, "transform:scaleY(0)"), (t + 6, "transform:scaleY(1)"), (100, "transform:scaleY(1)")])}/>')
        s += f'<g {d.show(t + 5)}>' + _t(x + bw * .32, y0 - bh - 14, f"{v}", "tn") + "</g>"
        s += _t(x + bw * .32, y0 + 20, name, "tn", extra='style="font-size:15px"')
        cum += v
        pts.append((x + bw * .32, y0 - h * cum / tot, cum / tot * 100))
    path = " ".join(f"{'M' if i == 0 else 'L'}{x:.1f} {y:.1f}" for i, (x, y, _) in enumerate(pts))
    L = 1400
    s += (f'<path d="{path}" fill="none" stroke="{O}" stroke-width="3.5" stroke-dasharray="{L}" '
          f'{d.a([(0, f"stroke-dashoffset:{L}"), (62, f"stroke-dashoffset:{L}"), (85, "stroke-dashoffset:0"), (100, "stroke-dashoffset:0")])}/>')
    for i, (x, y, p) in enumerate(pts):
        s += f'<g {d.show(64 + i * 3.5)}><circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="{O}"/>' + _t(x, y - 18, f"{p:.0f}%", "to") + "</g>"
    return d.svg(1160, 400, s)


def _grid(die, r_use=147.0):
    """좌상단 기준 격자에서 네 모서리가 모두 원 안인 다이 (labs/solution/scripts/yield_model.py 와 같은 규칙)."""
    n = int(r_use // die) + 2
    full, part = [], []
    for y in range(-n, n):
        for x in range(-n, n):
            ins = [((x + a) * die) ** 2 + ((y + b) * die) ** 2 <= r_use ** 2 for a in (0, 1) for b in (0, 1)]
            if all(ins):
                full.append((x, y))
            elif any(ins):
                part.append((x, y))
    return full, part


def gross(dies=(10, 20)):
    """같은 300 mm 웨이퍼에 다이 10 mm · 20 mm 격자 · 가장자리 걸친 칸은 회색으로 빠짐 · 세어진 수. 12초."""
    d = _D("p3b", 12)
    s = ""
    sc = 1.15
    for k, die in enumerate(dies):
        cx, cy = 230 + k * 560, 200
        full, part = _grid(die)
        t = 4 + k * 40
        s += f'<g {d.show(t)}><circle cx="{cx}" cy="{cy}" r="{150 * sc:.1f}" fill="#EEF1F5" stroke="#9AA5B1" stroke-width="2"/>'
        s += f'<circle cx="{cx}" cy="{cy}" r="{147 * sc:.1f}" fill="none" stroke="{R}" stroke-width="1.5" stroke-dasharray="4 4"/></g>'
        for (x, y) in part:
            s += (f'<rect x="{cx + x * die * sc:.1f}" y="{cy + y * die * sc:.1f}" width="{die * sc - 1:.1f}" height="{die * sc - 1:.1f}" '
                  f'fill="#C7CDD6" {d.show(t + 8)}/>')
        for (x, y) in full:
            s += (f'<rect x="{cx + x * die * sc:.1f}" y="{cy + y * die * sc:.1f}" width="{die * sc - 1:.1f}" height="{die * sc - 1:.1f}" '
                  f'fill="{K}" opacity=".85" {d.show(t + 14)}/>')
        s += (f'<g {d.show(t + 22)}><rect x="{cx + 190}" y="{cy - 50}" width="150" height="100" rx="14" fill="{MO}" stroke="{O}" stroke-width="2.5"/>'
              + _t(cx + 265, cy - 18, f"다이 {die} mm", "tn") + _t(cx + 265, cy + 18, f"{len(full)}개", "tt", extra='style="font-size:28px"') + "</g>")
    s += (f'<g {d.show(88)}>' + _t(580, 392, "남색 = 세는 다이 · 회색 = 가장자리에 걸려 버리는 칸 · 빨간 점선 = 가장자리 제외 3 mm", "ts") + "</g>")
    return d.svg(1160, 410, s)


def rain(d0_cm2, seed=7):
    """같은 결함(점) 분포를 다이 10 mm · 20 mm 격자에 떨어뜨림 · 결함이 닿은 다이 = 불량. 수율은 그림의 점으로 센 값. 14초."""
    d = _D("p3c", 14)
    rnd = random.Random(seed)
    area = math.pi * 14.7 ** 2                      # cm² · 쓰는 원
    n = round(area * d0_cm2)
    pts = []
    while len(pts) < n:
        x, y = rnd.uniform(-147, 147), rnd.uniform(-147, 147)
        if x * x + y * y < 147 ** 2:
            pts.append((x, y))
    s = ""
    sc = 1.1
    res = []
    for k, die in enumerate((10, 20)):
        cx, cy = 210 + k * 560, 190
        full, _ = _grid(die)
        hit = {(math.floor(x / die), math.floor(y / die)) for x, y in pts}
        bad = [c for c in full if c in hit]
        res.append((die, len(full), len(bad)))
        s += f'<circle cx="{cx}" cy="{cy}" r="{150 * sc:.1f}" fill="#EEF1F5" stroke="#9AA5B1" stroke-width="2"/>'
        for c in full:
            s += f'<rect x="{cx + c[0] * die * sc:.1f}" y="{cy + c[1] * die * sc:.1f}" width="{die * sc - 1:.1f}" height="{die * sc - 1:.1f}" fill="#2BA84A" opacity=".45"/>'
        for c in bad:
            s += (f'<rect x="{cx + c[0] * die * sc:.1f}" y="{cy + c[1] * die * sc:.1f}" width="{die * sc - 1:.1f}" height="{die * sc - 1:.1f}" '
                  f'fill="{R}" {d.show(50)}/>')
        for i, (x, y) in enumerate(pts):
            s += (f'<circle cx="{cx + x * sc:.1f}" cy="{cy + y * sc:.1f}" r="3.2" fill="{N}" '
                  f'{d.a([(0, "opacity:0;transform:translateY(-30px)"), (6 + i * 40 / n, "opacity:0;transform:translateY(-30px)"), (9 + i * 40 / n, "opacity:1;transform:none"), (100, "opacity:1;transform:none")])}/>')
        y = (len(full) - len(bad)) / len(full) * 100
        s += (f'<g {d.show(60 + k * 8)}><rect x="{cx + 180}" y="{cy - 64}" width="170" height="128" rx="14" fill="{W}" stroke="{K}" stroke-width="2.5"/>'
              + _t(cx + 265, cy - 36, f"다이 {die} mm", "tn") + _t(cx + 265, cy - 6, f"불량 {len(bad)} / {len(full)}", "ts")
              + _t(cx + 265, cy + 30, f"{y:.1f}%", "tt", extra=f'style="font-size:28px;fill:{OK if die == 10 else R}"') + "</g>")
    s += (f'<g {d.show(84)}>' + _t(580, 392, f"결함 {n}개 · 같은 위치 · D0 {d0_cm2:.3f}/cm²", "tn") + "</g>")
    return d.svg(1160, 410, s), res, n


def curve(rows):
    """rows = [(die_mm, poisson%, negbin%)] · 다이 크기별 예상 수율 곡선 두 개가 차례로 그려짐. 12초."""
    d = _D("p3d", 12)
    x0, y0, w, h = 100, 340, 900, 290
    xs = [r[0] for r in rows]
    X = lambda v: x0 + w * (v - xs[0]) / (xs[-1] - xs[0])
    Y = lambda v: y0 - h * (v - 40) / 60
    s = f'<line x1="{x0}" y1="{y0}" x2="{x0 + w}" y2="{y0}" stroke="#9AA5B1" stroke-width="2"/><line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0 - h}" stroke="#9AA5B1" stroke-width="2"/>'
    for v in (40, 60, 80, 100):
        s += _t(x0 - 10, Y(v), f"{v}%", "ts", "end") + f'<line x1="{x0}" y1="{Y(v):.1f}" x2="{x0 + w}" y2="{Y(v):.1f}" stroke="#EEF1F5"/>'
    for v in xs:
        s += _t(X(v), y0 + 20, f"{v} mm", "ts")
    s += _t(x0 + w / 2, y0 + 46, "다이 한 변 길이", "tn")
    for k, (col, lab) in enumerate(((K, "Poisson"), (O, "Negative binomial (α=2)"))):
        path = " ".join(f"{'M' if i == 0 else 'L'}{X(r[0]):.1f} {Y(r[1 + k]):.1f}" for i, r in enumerate(rows))
        L = 1300
        t = 6 + k * 34
        s += (f'<path d="{path}" fill="none" stroke="{col}" stroke-width="4" stroke-dasharray="{L}" '
              f'{d.a([(0, f"stroke-dashoffset:{L}"), (t, f"stroke-dashoffset:{L}"), (t + 26, "stroke-dashoffset:0"), (100, "stroke-dashoffset:0")])}/>')
        last = rows[-1]
        s += f'<g {d.show(t + 26)}>' + _t(X(last[0]) - 6, Y(last[1 + k]) + (22 if k == 0 else -46), f"{lab} {last[1 + k]}%", "tn", "end", f'style="fill:{col}"') + "</g>"
    ten = [r for r in rows if r[0] == 10][0]
    s += (f'<g {d.show(80)}><circle cx="{X(10):.1f}" cy="{Y(ten[1]):.1f}" r="8" fill="{R}"/>'
          + _t(X(10) + 14, Y(ten[1]) - 22, f"W07 다이 10 mm · {ten[1]}%", "tn", "start", f'style="fill:{R}"') + "</g>")
    return d.svg(1160, 400, s)
