"""SVG 차트 — 외부 라이브러리 없이 HTML 한 파일에 넣는다."""
import math

from common import COLOR, KO

F = "font-family='Pretendard,Apple SD Gothic Neo,sans-serif'"


def page(title, body):
    return (f"<!doctype html><html lang='ko'><meta charset='utf-8'><title>{title}</title>"
            "<style>body{font-family:Pretendard,'Apple SD Gothic Neo',sans-serif;background:#F5F6F8;margin:24px;color:#16233A}"
            ".grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(420px,1fr));gap:16px}"
            ".card{background:#fff;border-radius:12px;padding:16px 18px;box-shadow:0 1px 3px #0001}"
            ".card h3{margin:0 0 8px;font-size:16px}.kpi{display:flex;gap:12px;margin-bottom:16px}"
            ".kpi div{flex:1;background:#fff;border-radius:12px;padding:14px 18px}.kpi b{display:block;font-size:28px}"
            ".kpi span{font-size:13px;color:#6B7785}</style>"
            f"<h2>{title}</h2>{body}</html>")


def wafer_map(df, size=420, title=""):
    """다이 한 개 = 사각형 한 개 · 색은 불량 유형."""
    R = 150.0
    s = size / (2 * R + 10)
    c = size / 2
    out = [f"<svg viewBox='0 0 {size} {size + 40}' width='{size}' {F}>",
           f"<circle cx='{c}' cy='{c}' r='{R * s}' fill='#F2F4F7' stroke='#9AA5B1'/>"]
    for r in df.itertuples():
        x = c + (r.die_x * 10) * s
        y = c - ((r.die_y + 1) * 10) * s
        tip = f"({r.die_x},{r.die_y}) {KO[r.fail_type]} · vth {r.vth_v} V · ioff {r.ioff_na} nA"
        out.append(f"<rect x='{x:.1f}' y='{y:.1f}' width='{10 * s - .8:.1f}' height='{10 * s - .8:.1f}' "
                   f"fill='{COLOR[r.fail_type]}' opacity='{.35 if r.fail_type == 'none' else 1}'><title>{tip}</title></rect>")
    cnt = df.fail_type.value_counts()
    lx = 6
    for t in ["none", "crack", "open_short", "leakage", "vth_shift", "particle", "parametric", "retest"]:
        if t in cnt:
            out.append(f"<rect x='{lx}' y='{size + 14}' width='10' height='10' fill='{COLOR[t]}'/>"
                       f"<text x='{lx + 14}' y='{size + 23}' font-size='11'>{KO[t]} {cnt[t]}</text>")
            lx += 14 + 11 * (len(KO[t]) + len(str(cnt[t])) + 1) * .62 + 10
    out.append("</svg>")
    return "".join(out)


def bars(items, w=440, h=240, unit="", target=None, color="#1F3A5F", ymax=None, ymin=0):
    """items: [(이름, 값)] 세로 막대."""
    pad_l, pad_b, pad_t = 40, 34, 14
    ymax = ymax or max(v for _, v in items) * 1.15
    bw = (w - pad_l - 10) / len(items)
    sy = lambda v: pad_t + (h - pad_t - pad_b) * (1 - (v - ymin) / (ymax - ymin))
    out = [f"<svg viewBox='0 0 {w} {h}' width='{w}' {F}>",
           f"<line x1='{pad_l}' y1='{h - pad_b}' x2='{w}' y2='{h - pad_b}' stroke='#9AA5B1'/>"]
    for i, (k, v) in enumerate(items):
        x = pad_l + i * bw + bw * .15
        out.append(f"<rect x='{x:.1f}' y='{sy(v):.1f}' width='{bw * .7:.1f}' height='{h - pad_b - sy(v):.1f}' fill='{color}'/>"
                   f"<text x='{x + bw * .35:.1f}' y='{sy(v) - 4:.1f}' font-size='11' text-anchor='middle'>{v:g}{unit}</text>"
                   f"<text x='{x + bw * .35:.1f}' y='{h - pad_b + 15}' font-size='11' text-anchor='middle'>{k}</text>")
    if target is not None:
        out.append(f"<line x1='{pad_l}' y1='{sy(target):.1f}' x2='{w}' y2='{sy(target):.1f}' stroke='#C62828' stroke-dasharray='5 4'/>"
                   f"<text x='{w - 4}' y='{sy(target) - 4:.1f}' font-size='11' fill='#C62828' text-anchor='end'>목표 {target:g}{unit}</text>")
    out.append("</svg>")
    return "".join(out)


def line(items, w=880, h=260, unit="", target=None, ymin=None, ymax=None, color_of=None):
    """items: [(이름, 값)] 꺾은선 + 점. color_of(이름) 으로 점 색."""
    pad_l, pad_b, pad_t = 40, 30, 14
    vs = [v for _, v in items]
    ymin = ymin if ymin is not None else min(vs) - 2
    ymax = ymax if ymax is not None else max(vs) + 2
    sx = lambda i: pad_l + 10 + i * (w - pad_l - 20) / (len(items) - 1)
    sy = lambda v: pad_t + (h - pad_t - pad_b) * (1 - (v - ymin) / (ymax - ymin))
    pts = " ".join(f"{sx(i):.1f},{sy(v):.1f}" for i, (_, v) in enumerate(items))
    out = [f"<svg viewBox='0 0 {w} {h}' width='{w}' {F}>",
           f"<line x1='{pad_l}' y1='{h - pad_b}' x2='{w}' y2='{h - pad_b}' stroke='#9AA5B1'/>",
           f"<polyline points='{pts}' fill='none' stroke='#9AA5B1'/>"]
    for v in range(math.ceil(ymin), int(ymax) + 1, 2):
        out.append(f"<text x='{pad_l - 6}' y='{sy(v) + 4:.1f}' font-size='10' text-anchor='end'>{v}{unit}</text>")
    for i, (k, v) in enumerate(items):
        col = color_of(k) if color_of else "#1F3A5F"
        out.append(f"<circle cx='{sx(i):.1f}' cy='{sy(v):.1f}' r='4.5' fill='{col}'><title>{k} {v}{unit}</title></circle>"
                   f"<text x='{sx(i):.1f}' y='{h - pad_b + 14}' font-size='10' text-anchor='middle'>{k}</text>")
    if target is not None:
        out.append(f"<line x1='{pad_l}' y1='{sy(target):.1f}' x2='{w}' y2='{sy(target):.1f}' stroke='#C62828' stroke-dasharray='5 4'/>"
                   f"<text x='{w - 4}' y='{sy(target) - 4:.1f}' font-size='11' fill='#C62828' text-anchor='end'>목표 {target:g}{unit}</text>")
    out.append("</svg>")
    return "".join(out)


def hist(vals, lsl, usl, w=440, h=240, bins=30, unit=""):
    lo, hi = min(min(vals), lsl) - .01, max(max(vals), usl) + .01
    step = (hi - lo) / bins
    cnt = [0] * bins
    for v in vals:
        cnt[min(int((v - lo) / step), bins - 1)] += 1
    pad_l, pad_b, pad_t = 30, 30, 14
    sx = lambda v: pad_l + (w - pad_l - 10) * (v - lo) / (hi - lo)
    sy = lambda c: pad_t + (h - pad_t - pad_b) * (1 - c / (max(cnt) * 1.1))
    out = [f"<svg viewBox='0 0 {w} {h}' width='{w}' {F}>"]
    for i, c in enumerate(cnt):
        x0 = lo + i * step
        out.append(f"<rect x='{sx(x0):.1f}' y='{sy(c):.1f}' width='{sx(x0 + step) - sx(x0) - 1:.1f}' height='{h - pad_b - sy(c):.1f}' "
                   f"fill='{'#1F3A5F' if lsl <= x0 + step / 2 <= usl else '#C62828'}'/>")
    for v, lab in ((lsl, "LSL"), (usl, "USL")):
        out.append(f"<line x1='{sx(v):.1f}' y1='{pad_t}' x2='{sx(v):.1f}' y2='{h - pad_b}' stroke='#C62828' stroke-dasharray='5 4'/>"
                   f"<text x='{sx(v):.1f}' y='{pad_t - 2}' font-size='11' fill='#C62828' text-anchor='middle'>{lab} {v}</text>")
    for k in range(5):
        v = lo + (hi - lo) * k / 4
        out.append(f"<text x='{sx(v):.1f}' y='{h - pad_b + 15}' font-size='10' text-anchor='middle'>{v:.2f}{unit}</text>")
    out.append("</svg>")
    return "".join(out)


def scatter(xs, ys, cols, box, w=440, h=260, xl="", yl=""):
    """box = (x_lo, x_hi, y_lo) 규격 영역."""
    pad_l, pad_b, pad_t = 44, 36, 12
    x0, x1, y0, y1 = min(xs) - .01, max(xs) + .01, min(ys) - .01, max(ys) + .01
    sx = lambda v: pad_l + (w - pad_l - 10) * (v - x0) / (x1 - x0)
    sy = lambda v: pad_t + (h - pad_t - pad_b) * (1 - (v - y0) / (y1 - y0))
    bx0, bx1, by0 = box
    out = [f"<svg viewBox='0 0 {w} {h}' width='{w}' {F}>",
           f"<rect x='{sx(bx0):.1f}' y='{pad_t}' width='{sx(bx1) - sx(bx0):.1f}' height='{sy(by0) - pad_t:.1f}' fill='#2BA84A' opacity='.08' stroke='#2BA84A' stroke-dasharray='4 3'/>"]
    for x, y, c in zip(xs, ys, cols):
        out.append(f"<circle cx='{sx(x):.1f}' cy='{sy(y):.1f}' r='2.4' fill='{c}' opacity='.75'/>")
    out.append(f"<text x='{w / 2}' y='{h - 4}' font-size='11' text-anchor='middle'>{xl}</text>"
               f"<text x='12' y='{h / 2}' font-size='11' text-anchor='middle' transform='rotate(-90 12 {h / 2})'>{yl}</text></svg>")
    return "".join(out)
