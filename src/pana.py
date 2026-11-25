"""데이터 분석의 흐름 애니메이션 — 큰 흐름 → 2차원 → 차원 더하기 → 여러 날 → 특이점 → 원인 → 추세선 예측
→ 지도학습 · 비지도학습(정답 열 · 경계 찾기 · 무리 묶기 · 활용 예) → 기준 바꿔 보기 · 바이브코딩의 흐름.

사과 데이터(sk.D07 · 25일치 · labs/ref.json general)로 그린다. 숫자는 모두 코드로 계산. 장면 간격 2초 이상 · 한 번 재생. 접두어 pa.
"""
import numpy as np
import pandas as pd

import sk
from anim import K, N, O, OK, R, W, _D, _t
from p0 import _RH, _rows8, _sheet
from pkit import REF

GOOD, BAD = "#2BA84A", "#E8344E"
GRAY = "#9AA5B1"


def _axes(x0, y0, w, h, xr, yr, xticks, yticks, xlab, ylab, show):
    """좌표축 · 눈금 · 축 이름. fx · fy 변환 함수를 함께 돌려준다."""
    fx = lambda v: x0 + (v - xr[0]) / (xr[1] - xr[0]) * w  # noqa: E731
    fy = lambda v: y0 + h - (v - yr[0]) / (yr[1] - yr[0]) * h  # noqa: E731
    s = f'<g {show}><line x1="{x0}" y1="{y0 + h}" x2="{x0 + w}" y2="{y0 + h}" stroke="{N}" stroke-width="2"/>'
    s += f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0 + h}" stroke="{N}" stroke-width="2"/>'
    for v in xticks:
        s += f'<line x1="{fx(v):.1f}" y1="{y0 + h}" x2="{fx(v):.1f}" y2="{y0 + h + 6}" stroke="{N}" stroke-width="1.5"/>' + _t(fx(v), y0 + h + 22, f"{v:g}", "ts", extra='style="font-size:13px"')
    for v in yticks:
        s += f'<line x1="{x0 - 6}" y1="{fy(v):.1f}" x2="{x0}" y2="{fy(v):.1f}" stroke="{N}" stroke-width="1.5"/>' + _t(x0 - 10, fy(v), f"{v:g}", "ts", "end", 'style="font-size:13px"')
    s += _t(x0 + w, y0 + h + 44, xlab, "tn", "end", 'style="font-size:14px"') + _t(x0 - 8, y0 - 16, ylab, "tn", "start", 'style="font-size:14px"') + "</g>"
    return s, fx, fy


# ── 데이터 분석의 큰 흐름 · 다섯 단계 ─────────────────────────────
def roadmap():
    d = _D("par", 14)
    pc = lambda t: t / 14 * 100  # noqa: E731
    icons = [
        "".join(f'<rect x="{-44}" y="{-34 + i * 18}" width="88" height="12" rx="3" fill="{"#1D6F42" if i == 0 else "#E1E5EB"}"/>' for i in range(4)),
        "".join(f'<rect x="{-42 + i * 22}" y="{30 - h}" width="16" height="{h}" rx="2" fill="{K}"/>' for i, h in enumerate([22, 46, 60, 34])),
        "".join(f'<circle cx="{x}" cy="{y}" r="4" fill="{GRAY}"/>' for x, y in [(-36, 20), (-20, 8), (-6, 14), (8, -2), (22, 6), (34, -10)])
        + f'<circle cx="30" cy="22" r="5" fill="{BAD}"/><circle cx="30" cy="22" r="13" fill="none" stroke="{BAD}" stroke-width="2.5"/>',
        f'<circle cx="-6" cy="-6" r="22" fill="none" stroke="{K}" stroke-width="5"/><path d="M10 10 L34 34" stroke="{K}" stroke-width="7" stroke-linecap="round"/>',
        f'<path d="M-44 26 L-20 10 L0 16 L20 -4" fill="none" stroke="{K}" stroke-width="4"/><path d="M20 -4 L44 -24" fill="none" stroke="{O}" stroke-width="4" stroke-dasharray="6 5"/>',
    ]
    steps = [("기록 모으기", "사과 600개 · 25일"), ("그려 보기", "분포 · 산점도 · 지도"), ("특이점 찾기", "몰린 곳 · 튀는 날"),
             ("원인 짐작", "왜 그 위치 · 그날?"), ("예측 · 판단", "기준을 바꾸면?")]
    s = ""
    for i, ((h, ex), ic) in enumerate(zip(steps, icons)):
        x, t = 24 + i * 226, pc(.5 + i * 2.4)
        s += (f'<g {d.show(t)}><rect x="{x}" y="60" width="196" height="200" rx="16" fill="{"#FFF8F0" if i == 4 else W}" '
              f'stroke="{O if i == 4 else K}" stroke-width="2.5"/><g transform="translate({x + 98},128)">{ic}</g>'
              + _t(x + 98, 206, h, "tt", extra='style="font-size:20px"') + _t(x + 98, 236, ex, "ts", extra='style="font-size:14px"') + "</g>")
        if i:
            s += f'<g {d.show(t)}><path d="M{x - 26} 160 H{x - 6}" stroke="{O}" stroke-width="3" marker-end="url(#{d.id("o")})"/></g>'
    return d.svg(1160, 290, s)


# ── 2차원 · 무게와 당도 ───────────────────────────────────────
def scatter_2d(df):
    """엑셀 두 열(무게 · 당도) → 8행이 평면 위 점으로 → 600개. 18초."""
    d = _D("pa2", 18)
    rows = _rows8(df)
    scol = [("사과번호", 100, False), ("무게", 78, True), ("당도", 78, True)]
    sh, cells, W_ = _sheet(d, rows, len(df), "무게", 6, scol)
    x2, _, w2 = cells[(0, "당도")]
    sh += f'<rect x="{x2}" y="44" width="{w2}" height="{26 + 8 * _RH}" fill="none" stroke="{O}" stroke-width="3" {d.show(6)}/>'
    ax, fx, fy = _axes(W_ + 110, 70, 1120 - (W_ + 110), 280, (200, 380), (9, 17), range(200, 381, 40), range(9, 18, 2),
                       "무게 (g)", "당도 (brix)", d.show(12))
    s = sh + ax
    for i, (_, r) in enumerate(rows.iterrows()):
        t = 20 + i * 3.5
        for c in ("무게", "당도"):
            cx, cy, w = cells[(i, c)]
            s += f'<rect x="{cx}" y="{cy}" width="{w}" height="{_RH}" fill="{O}" fill-opacity=".22" {d.show(t)}/>'
        s += f'<circle cx="{fx(r["무게"]):.1f}" cy="{fy(r["당도"]):.1f}" r="7" fill="{O}" stroke="{N}" stroke-width="1.5" {d.show(t)}/>'
    dots = "".join(f'<circle cx="{fx(a):.1f}" cy="{fy(b):.1f}" r="3.2" fill="{K}" fill-opacity=".45"/>' for a, b in zip(df["무게"], df["당도"]))
    s += f'<g {d.show(56)}>{dots}</g>'
    s += f'<g {d.show(70)}>' + _t(W_ + 110, 14, f"점 하나 = 사과 한 개 · 가로 무게 · 세로 당도 · {len(df)}개", "to", "start", 'style="font-size:16px"') + "</g>"
    return d.svg(1160, 410, s)


# ── 3차원 · 등급 색까지 ───────────────────────────────────────
def scatter_3d(df):
    """600개 점에 등급 색 → 기준선(무게 · 당도) → 불량이 몰린 곳 · 흩어진 곳. 12초."""
    d = _D("pa3", 12)
    pc = lambda t: t / 12 * 100  # noqa: E731
    ax, fx, fy = _axes(110, 40, 760, 320, (200, 380), (9, 17), range(200, 381, 40), range(9, 18, 2), "무게 (g)", "당도 (brix)", d.show(0))
    s = ax + "".join(f'<circle cx="{fx(a):.1f}" cy="{fy(b):.1f}" r="3.4" fill="{GRAY}" fill-opacity=".6"/>' for a, b in zip(df["무게"], df["당도"]))
    col = "".join(f'<circle cx="{fx(r["무게"]):.1f}" cy="{fy(r["당도"]):.1f}" r="3.6" fill="{GOOD if r["등급"] == "상품" else BAD}"/>'
                  for _, r in df.iterrows())
    s += f'<g {d.show(pc(2))}>{col}</g>'
    s += (f'<g {d.show(pc(2))}><circle cx="910" cy="56" r="6" fill="{GOOD}"/>' + _t(924, 56, "상품", "tn", "start")
          + f'<circle cx="990" cy="56" r="6" fill="{BAD}"/>' + _t(1004, 56, "불량 · 색 = 등급", "tn", "start") + "</g>")
    w0, b0 = sk.MIN_W, sk.MIN_SUGAR
    s += (f'<g {d.show(pc(5))}><line x1="{fx(w0):.1f}" y1="40" x2="{fx(w0):.1f}" y2="360" stroke="{N}" stroke-width="2" stroke-dasharray="7 5"/>'
          f'<line x1="110" y1="{fy(b0):.1f}" x2="870" y2="{fy(b0):.1f}" stroke="{N}" stroke-width="2" stroke-dasharray="7 5"/>'
          + _t(fx(w0) + 6, 50, f"무게 {w0}g", "tn", "start", 'style="font-size:13px"') + _t(866, fy(b0) - 10, f"당도 {b0:g}", "tn", "end", 'style="font-size:13px"') + "</g>")
    rs = sk.DN["reason"]
    s += (f'<g {d.show(pc(8))}><rect x="900" y="110" width="250" height="100" rx="12" fill="#FDECEA" stroke="{BAD}" stroke-width="2"/>'
          + _t(916, 136, "왼쪽 · 아래에 몰림", "tn", "start", 'style="font-size:16px"')
          + _t(916, 164, f"무게 미달 {rs['무게 미달']} · 당도 미달 {rs['당도 미달']}", "ts", "start") + _t(916, 188, "기준선 바깥", "ts", "start") + "</g>")
    s += (f'<g {d.show(pc(10))}><rect x="900" y="228" width="250" height="100" rx="12" fill="{W}" stroke="{BAD}" stroke-width="2" stroke-dasharray="6 4"/>'
          + _t(916, 254, "곳곳에 흩어짐", "tn", "start", 'style="font-size:16px"')
          + _t(916, 282, f"멍 {rs['멍']} · 벌레 먹음 {rs['벌레 먹음']}", "ts", "start") + _t(916, 306, "무게 · 당도와 상관없음", "ts", "start") + "</g>")
    return d.svg(1160, 410, s)


# ── 여러 날 · 25일치 상품률 ──────────────────────────────────
def daily_line():
    """25일 상품률이 선으로 그려짐 → 25일 평균 → 가장 낮은 날 표시. 12초."""
    d = _D("pad", 12)
    pc = lambda t: t / 12 * 100  # noqa: E731
    days = REF["general"]["days"]
    vals = [days[f"A{k:02d}"] for k in range(1, 26)]
    ax, fx, fy = _axes(110, 40, 900, 300, (1, 25), (50, 85), [1, 5, 10, 15, 20, 25], range(50, 86, 10), "10월 · 일", "상품률 (%)", d.show(0))
    pts = " ".join(f"{fx(k + 1):.1f},{fy(v):.1f}" for k, v in enumerate(vals))
    draw = [(0, "stroke-dashoffset:1"), (pc(.5), "stroke-dashoffset:1"), (pc(4), "stroke-dashoffset:0"), (100, "stroke-dashoffset:0")]
    s = ax + f'<polyline points="{pts}" fill="none" stroke="{K}" stroke-width="3" pathLength="1" stroke-dasharray="1" {d.a(draw)}/>'
    s += f'<g {d.show(pc(4))}>' + "".join(f'<circle cx="{fx(k + 1):.1f}" cy="{fy(v):.1f}" r="5" fill="{K}"/>' for k, v in enumerate(vals)) + "</g>"
    avg = sum(vals) / len(vals)
    s += (f'<g {d.show(pc(6))}><line x1="110" y1="{fy(avg):.1f}" x2="1010" y2="{fy(avg):.1f}" stroke="{GRAY}" stroke-width="2" stroke-dasharray="7 5"/>'
          + _t(1022, fy(avg) - 10, "25일 평균", "ts", "start", 'style="font-size:14px"') + _t(1022, fy(avg) + 12, f"{avg:.2f}%", "tn", "start", 'style="font-size:15px"') + "</g>")
    k = min(range(25), key=lambda i: vals[i])
    s += (f'<g {d.show(pc(8))}><circle cx="{fx(k + 1):.1f}" cy="{fy(vals[k]):.1f}" r="16" fill="none" stroke="{BAD}" stroke-width="3"/>'
          + _t(fx(k + 1), fy(vals[k]) + 34, f"{k + 1}일 · {vals[k]:.2f}%", "to", extra=f'style="font-size:17px;fill:{BAD}"') + "</g>")
    return d.svg(1160, 400, s)


# ── 특이한 날 · 불량 사유 비교 ───────────────────────────────
def odd_day():
    """평소 하루 평균과 특이한 날의 불량 사유별 개수 → 멍이 크게 늘어남 → 원인 짐작. 12초."""
    d = _D("pao", 12)
    pc = lambda t: t / 12 * 100  # noqa: E731
    od = REF["general"]["odd_day"]
    reasons = sk.D_ORDER
    usual, odd = od["reason_avg_other"], od["reason"]
    mx = max(max(usual.values()), max(odd.values())) * 1.1
    X0, Y0, H, GW = 120, 50, 280, 150
    s = f'<line x1="{X0 - 20}" y1="{Y0 + H}" x2="{X0 + 4 * GW + 10}" y2="{Y0 + H}" stroke="{N}" stroke-width="2"/>'
    grow = "transform-box:fill-box;transform-origin:50% 100%"
    for i, r in enumerate(reasons):
        gx = X0 + i * GW
        for j, (v, col, t0) in enumerate([(usual[r], GRAY, 1), (odd[r], BAD if r == "멍" else "#F2A0AC", 4)]):
            h = H * v / mx
            st = [(0, "transform:scaleY(0)"), (pc(t0), "transform:scaleY(0)"), (pc(t0 + 1), "transform:scaleY(1)"), (100, "transform:scaleY(1)")]
            x = gx + j * 54
            s += f'<rect x="{x}" y="{Y0 + H - h:.1f}" width="46" height="{h:.1f}" rx="4" fill="{col}" {d.a(st, "ease-out", grow)}/>'
            s += f'<g {d.show(pc(t0 + 1))}>' + _t(x + 23, Y0 + H - h - 12, f"{v:g}", "tn", extra='style="font-size:14px"') + "</g>"
        s += _t(gx + 50, Y0 + H + 22, sk.D_KO[r], "tn")
    day = int(od["day"][1:])
    s += (f'<g {d.show(pc(1))}><rect x="{X0}" y="8" width="14" height="14" rx="3" fill="{GRAY}"/>' + _t(X0 + 20, 15, "평소 하루 평균", "ts", "start")
          + "</g>" + f'<g {d.show(pc(4))}><rect x="{X0 + 160}" y="8" width="14" height="14" rx="3" fill="{BAD}"/>'
          + _t(X0 + 180, 15, f"{day}일", "ts", "start") + "</g>")
    ratio = odd["멍"] / usual["멍"]
    s += (f'<g {d.show(pc(7))}><rect x="780" y="70" width="360" height="96" rx="14" fill="#FDECEA" stroke="{BAD}" stroke-width="2.5"/>'
          + _t(960, 104, f"멍 {odd['멍']}개 · 평소 {usual['멍']:g}개", "tt", extra=f'style="fill:{BAD};font-size:19px"')
          + _t(960, 136, f"약 {ratio:.0f}배 · 상품률 {od['rate']:.2f}%", "ts") + "</g>")
    s += (f'<g {d.show(pc(9.5))}><rect x="780" y="190" width="360" height="110" rx="14" fill="{W}" stroke="{N}" stroke-width="2" stroke-dasharray="7 5"/>'
          + _t(800, 222, "원인 짐작", "to", "start", 'style="font-size:16px"') + _t(800, 252, "수확 · 운반 중 충격?", "tn", "start", 'style="font-size:16px"')
          + _t(800, 280, "그날 작업 기록으로 확인", "ts", "start") + "</g>")
    return d.svg(1160, 370, s)


# ── 추세선과 예측 · 무게로 지름 짐작 ────────────────────────────
def trend_predict(df):
    """무게 × 지름 점 → 추세선 → 무게 320g 사과의 지름 예측. 12초."""
    d = _D("pat", 12)
    pc = lambda t: t / 12 * 100  # noqa: E731
    xs, ys = df["무게"].to_numpy(float), df["지름"].to_numpy(float)
    a, b = np.polyfit(xs, ys, 1)
    lo, hi = float(np.floor(ys.min() - 1)), float(np.ceil(ys.max() + 1))
    ax, fx, fy = _axes(110, 40, 760, 310, (200, 380), (lo, hi), range(200, 381, 40), range(int(lo) + (int(lo) % 2), int(hi) + 1, 4),
                       "무게 (g)", "지름 (mm)", d.show(0))
    s = ax + f'<g {d.show(pc(.5))}>' + "".join(f'<circle cx="{fx(x):.1f}" cy="{fy(y):.1f}" r="3.2" fill="{K}" fill-opacity=".4"/>' for x, y in zip(xs, ys)) + "</g>"
    draw = [(0, "stroke-dashoffset:1"), (pc(3), "stroke-dashoffset:1"), (pc(5), "stroke-dashoffset:0"), (100, "stroke-dashoffset:0")]
    s += f'<line x1="{fx(200):.1f}" y1="{fy(a * 200 + b):.1f}" x2="{fx(380):.1f}" y2="{fy(a * 380 + b):.1f}" stroke="{O}" stroke-width="4" pathLength="1" stroke-dasharray="1" {d.a(draw)}/>'
    s += f'<g {d.show(pc(5))}>' + _t(fx(380) - 4, fy(a * 380 + b) - 16, "추세선", "to", "end", 'style="font-size:15px"') + "</g>"
    xq = 320
    yq = a * xq + b
    s += f'<g {d.show(pc(6.5))}><line x1="{fx(xq):.1f}" y1="350" x2="{fx(xq):.1f}" y2="{fy(yq):.1f}" stroke="{BAD}" stroke-width="2.5" stroke-dasharray="6 4"/><circle cx="{fx(xq):.1f}" cy="{fy(yq):.1f}" r="7" fill="{BAD}"/></g>'
    s += f'<g {d.show(pc(8))}><line x1="{fx(xq):.1f}" y1="{fy(yq):.1f}" x2="110" y2="{fy(yq):.1f}" stroke="{BAD}" stroke-width="2.5" stroke-dasharray="6 4"/></g>'
    s += (f'<g {d.show(pc(9.5))}><rect x="900" y="110" width="250" height="110" rx="14" fill="#FDECEA" stroke="{BAD}" stroke-width="2.5"/>'
          + _t(1025, 142, f"무게 {xq}g 사과", "tn", extra='style="font-size:16px"') + _t(1025, 176, f"지름 약 {yq:.1f}mm", "tt", extra=f'style="fill:{BAD};font-size:21px"')
          + _t(1025, 204, f"무게 10g ↑ · 지름 약 {a * 10:.1f}mm ↑", "ts") + "</g>")
    return d.svg(1160, 410, s)


# ── 지도학습 · 비지도학습 ─────────────────────────────────────
BLUE = "#4A86E8"


def _boundary(df):
    """정답(등급)만 보고 「무게 ≥ a 이고 당도 ≥ b → 상품」 경계를 찾는다 — 맞힌 사과가 가장 많은 a · b."""
    w, s = df["무게"].to_numpy(float), df["당도"].to_numpy(float)
    y = (df["등급"] == "상품").to_numpy(np.int64)
    uw, us = np.unique(w), np.unique(s)
    cw, cs = (uw[:-1] + uw[1:]) / 2, (us[:-1] + us[1:]) / 2
    a = (w[None] >= cw[:, None]).astype(np.int64)
    b = (s[None] >= cs[:, None]).astype(np.int64)
    hit = 2 * ((a * y) @ b.T) - a @ b.T + int((1 - y).sum())      # 맞힌 수 = 상품 맞힘 + 불량 맞힘
    i, j = np.unravel_index(hit.argmax(), hit.shape)
    return float(cw[i]), float(cs[j]), int(hit[i, j])


_TREES = []


def _trees():
    """25일치를 나무(가로칸 · 세로칸)별로 평균 → 무게 · 당도만으로 두 무리(k-평균). 위치 열은 묶을 때 쓰지 않는다."""
    if _TREES:
        return _TREES[0]
    al = pd.concat([sk.apple(f"A{k:02d}") for k in range(1, 26)])
    g = al.groupby(["가로칸", "세로칸"]).agg(무게=("무게", "mean"), 당도=("당도", "mean"), 위치=("위치", "first")).reset_index()
    z = np.c_[(g["무게"] - g["무게"].mean()) / g["무게"].std(), (g["당도"] - g["당도"].mean()) / g["당도"].std()]
    c = z[[z.sum(1).argmin(), z.sum(1).argmax()]]
    for _ in range(100):
        lab = ((z[:, None] - c[None]) ** 2).sum(2).argmin(1)
        c2 = np.array([z[lab == k].mean(0) for k in range(2)])
        if np.allclose(c2, c):
            break
        c = c2
    small = int((lab == 1).sum() < (lab == 0).sum())
    g["무리"] = np.where(lab == small, 2, 1)                        # 작은 무리 = 무리 2
    _TREES.append(g)
    return g


def label_or_not(df):
    """같은 사과 시트 둘 — 왼쪽은 등급 열이 정답(라벨) → 새 사과 등급 예측 / 오른쪽은 등급 열을 가림 → 비슷한 사과 묶기 · 튀는 값 찾기. 14초."""
    d = _D("pal", 14)
    pc = lambda t: t / 14 * 100  # noqa: E731
    rows = _rows8(df)
    scol = [("사과번호", 92, False), ("무게", 70, True), ("당도", 70, True), ("등급", 70, False)]
    Y, BH = 58, 26 + 8 * _RH
    side = [(0, "지도학습", .5, "정답 (라벨)", "정답을 보고 학습", ["새 사과", "등급 예측"]),
            (600, "비지도학습", 7, "정답 없음", "정답 없이 학습", ["비슷한 사과 묶기", "튀는 값 찾기"])]
    s = ""
    for k, (x0, name, t0, tag, sub, job) in enumerate(side):
        sh, cells, W_ = _sheet(d, rows, len(df), None if k else "등급", pc(t0 + 2), scol)
        gx, _, gw = cells[(0, "등급")]
        if k:                                                    # 등급 열을 가림
            sh += (f'<g {d.show(pc(t0 + 2))}><rect x="{gx}" y="44" width="{gw}" height="{BH}" fill="#EEF1F4"/>'
                   f'<rect x="{gx}" y="44" width="{gw}" height="{BH}" fill="none" stroke="{O}" stroke-width="3" stroke-dasharray="7 5"/>'
                   + _t(gx + gw / 2, 44 + BH / 2, "없음", "ts") + "</g>")
        s += (f'<g {d.show(pc(t0))}>' + _t(x0, 24, name, "tt", "start", 'style="font-size:22px"')
              + f'<g transform="translate({x0},{Y})">{sh}</g></g>')
        s += f'<g {d.show(pc(t0 + 2))}>' + _t(x0 + gx + gw / 2, Y - 14, tag, "to", extra='style="font-size:15px"') + "</g>"
        bx = x0 + W_ + 44
        bw, by = x0 + 560 - bx, Y + 98
        s += (f'<g {d.show(pc(t0 + 4))}><path d="M{x0 + W_ + 8} {by + 70} H{bx - 6}" stroke="{N}" stroke-width="2.5" marker-end="url(#{d.id("k")})"/>'
              f'<rect x="{bx}" y="{by}" width="{bw}" height="140" rx="14" fill="{W}" stroke="{K}" stroke-width="2.5"/>'
              + _t(bx + bw / 2, by + 30, sub, "ts", extra='style="font-size:14px"')
              + "".join(_t(bx + bw / 2, by + 72 + i * 34, j, "tt", extra='style="font-size:18px"') for i, j in enumerate(job)) + "</g>")
    return d.svg(1160, 400, s)


def supervised(df):
    """정답(등급 색)이 붙은 사과 → 맞힌 수가 가장 많은 경계를 찾음 → 새 사과 셋이 경계 안 · 밖에 따라 상품 · 불량으로 예측. 14초."""
    d = _D("pas", 14)
    pc = lambda t: t / 14 * 100  # noqa: E731
    ax, fx, fy = _axes(110, 40, 760, 320, (200, 380), (9, 17), range(200, 381, 40), range(9, 18, 2), "무게 (g)", "당도 (brix)", d.show(0))
    tw, ts, _ = _boundary(df)
    s = ax + f'<rect x="{fx(tw):.1f}" y="40" width="{870 - fx(tw):.1f}" height="{fy(ts) - 40:.1f}" fill="{GOOD}" fill-opacity=".10" {d.show(pc(3))}/>'
    s += (f'<g {d.show(pc(.5))}>' + "".join(f'<circle cx="{fx(r["무게"]):.1f}" cy="{fy(r["당도"]):.1f}" r="3.6" fill="{GOOD if r["등급"] == "상품" else BAD}"/>'
                                            for _, r in df.iterrows())
          + _t(900, 56, "정답", "to", "start") + f'<circle cx="952" cy="56" r="6" fill="{GOOD}"/>' + _t(966, 56, "상품", "tn", "start")
          + f'<circle cx="1022" cy="56" r="6" fill="{BAD}"/>' + _t(1036, 56, "불량", "tn", "start") + "</g>")
    s += (f'<g {d.show(pc(3))}><path d="M{fx(tw):.1f} 40 V{fy(ts):.1f} H870" fill="none" stroke="{O}" stroke-width="3.5"/>'
          + _t(fx(tw) + 8, 54, "찾아낸 경계", "to", "start") + "</g>")
    s += (f'<g {d.show(pc(3))}><rect x="900" y="90" width="250" height="128" rx="14" fill="#FFF8F0" stroke="{O}" stroke-width="2.5"/>'
          + _t(1025, 116, f"정답 {len(df)}개로 찾은 경계", "to")
          + _t(1025, 150, f"무게 약 {tw:.0f}g", "tt", extra='style="font-size:20px"') + _t(1025, 178, f"당도 약 {ts:.0f}", "tt", extra='style="font-size:20px"')
          + _t(1025, 202, "선별 기준과 거의 같음", "ts", extra='style="font-size:14px"') + "</g>")
    for w_, b_ in [(335, 13.8), (228, 12.9), (305, 10.0)]:            # 새 사과 — 정답(등급)을 모르는 입력
        cx, cy = fx(w_), fy(b_)
        c = GOOD if w_ >= tw and b_ >= ts else BAD
        s += (f'<g {d.show(pc(6))}><circle cx="{cx:.1f}" cy="{cy:.1f}" r="11" fill="{W}" stroke="{N}" stroke-width="2.5"/>'
              + _t(cx, cy + 1, "?", "tn", extra='style="font-size:14px"') + "</g>")
        s += (f'<g {d.show(pc(8.5))}><circle cx="{cx:.1f}" cy="{cy:.1f}" r="11" fill="{c}" stroke="{N}" stroke-width="2.5"/>'
              + _t(cx + 18, cy, "상품" if c == GOOD else "불량", "tn", "start",
                   f'style="font-size:16px;fill:{c};paint-order:stroke;stroke:#fff;stroke-width:5px"') + "</g>")
    s += (f'<g {d.show(pc(8.5))}><rect x="900" y="240" width="250" height="96" rx="14" fill="{W}" stroke="{N}" stroke-width="2.5"/>'
          + _t(1025, 272, "새 사과 등급 예측", "tn", extra='style="font-size:16px"') + _t(1025, 304, "경계 안 상품 · 밖 불량", "ts") + "</g>")
    return d.svg(1160, 410, s)


def unsupervised():
    """정답 없는 점(나무 600그루 · 25일 평균 무게 · 당도) → 두 무리로 묶임 → 지도에 칠하면 무리 2 가 가장자리 띠. 14초."""
    d = _D("pau", 14)
    pc = lambda t: t / 14 * 100  # noqa: E731
    g = _trees()
    col = {1: BLUE, 2: O}
    ax, fx, fy = _axes(100, 50, 440, 300, (255, 315), (10.8, 13.4), range(260, 311, 10), [11, 12, 13],
                       "25일 평균 무게 (g)", "25일 평균 당도 (brix)", d.show(0))
    s = ax + (f'<g {d.show(pc(.5))}>' + "".join(f'<circle cx="{fx(r["무게"]):.1f}" cy="{fy(r["당도"]):.1f}" r="3.2" fill="{GRAY}" fill-opacity=".7"/>'
                                                for _, r in g.iterrows())
              + _t(100, 12, f"점 하나 = 나무 한 그루 · {len(g)}그루 · 정답 없음", "to", "start", 'style="font-size:16px"') + "</g>")
    s += f'<g {d.show(pc(3))}>' + "".join(f'<circle cx="{fx(r["무게"]):.1f}" cy="{fy(r["당도"]):.1f}" r="3.4" fill="{col[r["무리"]]}"/>'
                                          for _, r in g.iterrows())
    for k in (1, 2):
        m = g[g["무리"] == k]
        lx, ly = (m["무게"].mean() + 8, m["당도"].min() - .3) if k == 1 else (m["무게"].mean() - 6, m["당도"].max() + .3)
        s += _t(fx(lx), fy(ly), f"무리 {k} · {len(m)}그루", "tn", extra=f'style="font-size:16px;fill:{col[k]}"')
    s += "</g>"
    C, X0, Y0 = 15, 630, 50
    nx, ny = int(g["가로칸"].max()), int(g["세로칸"].max())
    gx = lambda x: X0 + (x - 1) * C  # noqa: E731
    gy = lambda y: Y0 + (ny - y) * C  # noqa: E731
    cell = lambda r, f: f'<rect x="{gx(r["가로칸"])}" y="{gy(r["세로칸"])}" width="{C - 2}" height="{C - 2}" rx="2" fill="{f}"/>'  # noqa: E731
    s += (f'<g {d.show(pc(6))}>' + _t(X0, 26, "과수원 지도", "tn", "start", 'style="font-size:16px"')
          + "".join(cell(r, "#E1E5EB") for _, r in g.iterrows()) + "</g>")
    s += f'<g {d.show(pc(8))}>' + "".join(cell(r, col[r["무리"]]) for _, r in g.iterrows()) + "</g>"
    edge = g["위치"] == "가장자리"
    n2 = int((g["무리"] == 2).sum())
    assert n2 == int(((g["무리"] == 2) & edge).sum()) == int(edge.sum()), "무리 2 와 가장자리가 어긋남 — 문구를 고친다"
    s += (f'<g {d.show(pc(10.5))}><rect x="{X0}" y="366" width="{nx * C - 2}" height="58" rx="12" fill="#FFF8F0" stroke="{O}" stroke-width="2.5"/>'
          + _t(X0 + nx * C / 2, 386, f"무리 2 = 가장자리 나무 {n2}그루", "to", extra='style="font-size:17px"')
          + _t(X0 + nx * C / 2, 410, "묶을 때 쓴 열 · 무게 · 당도", "ts", extra='style="font-size:14px"') + "</g>")
    return d.svg(1160, 430, s)


def _mini(x, y, w, h, kind, df):
    """활용 예 카드의 작은 그림 — 앞 장면의 사과 데이터를 축 숫자 없이 줄여 그린다."""
    s = (f'<line x1="{x}" y1="{y + h}" x2="{x + w}" y2="{y + h}" stroke="{N}" stroke-width="1.5"/>'
         f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y + h}" stroke="{N}" stroke-width="1.5"/>')

    def sc(xr, yr):
        return (lambda v: x + 6 + (v - xr[0]) / (xr[1] - xr[0]) * (w - 12)), (lambda v: y + h - 6 - (v - yr[0]) / (yr[1] - yr[0]) * (h - 12))
    dot = lambda fx, fy, a, b, c, r=2.2: f'<circle cx="{fx(a):.1f}" cy="{fy(b):.1f}" r="{r}" fill="{c}"/>'  # noqa: E731
    if kind == "분류":
        fx, fy = sc((200, 380), (9, 17))
        tw, ts, _ = _boundary(df)
        sub = df.iloc[::3]
        s += "".join(dot(fx, fy, a, b, GOOD if g == "상품" else BAD) for a, b, g in zip(sub["무게"], sub["당도"], sub["등급"]))
        s += f'<path d="M{fx(tw):.1f} {y} V{fy(ts):.1f} H{x + w}" fill="none" stroke="{O}" stroke-width="2.5"/>'
    elif kind == "회귀":
        xs, ys = df["무게"].to_numpy(float), df["지름"].to_numpy(float)
        a, b = np.polyfit(xs, ys, 1)
        fx, fy = sc((200, 380), (ys.min() - 1, ys.max() + 1))
        s += "".join(dot(fx, fy, p, q, K) for p, q in zip(xs[::3], ys[::3])).replace(f'fill="{K}"', f'fill="{K}" fill-opacity=".45"')
        s += f'<line x1="{fx(200):.1f}" y1="{fy(a * 200 + b):.1f}" x2="{fx(380):.1f}" y2="{fy(a * 380 + b):.1f}" stroke="{O}" stroke-width="3"/>'
    elif kind == "군집":
        g = _trees().iloc[::2]
        fx, fy = sc((255, 315), (10.8, 13.4))
        s += "".join(dot(fx, fy, a, b, BLUE if k == 1 else O) for a, b, k in zip(g["무게"], g["당도"], g["무리"]))
    else:
        days = REF["general"]["days"]
        vals = [days[f"A{k:02d}"] for k in range(1, 26)]
        fx, fy = sc((1, 25), (min(vals) - 4, max(vals) + 2))
        s += f'<polyline points="{" ".join(f"{fx(k + 1):.1f},{fy(v):.1f}" for k, v in enumerate(vals))}" fill="none" stroke="{K}" stroke-width="2.5"/>'
        k = min(range(25), key=lambda i: vals[i])
        s += f'<circle cx="{fx(k + 1):.1f}" cy="{fy(vals[k]):.1f}" r="9" fill="none" stroke="{BAD}" stroke-width="2.5"/>'
    return s


def ml_uses(df):
    """지도학습(분류 · 회귀) · 비지도학습(군집 · 이상 탐지) — 카드마다 덱에서 본 사과 그림을 줄여 붙이고 일상 예 · 사과 예. 카드 2초 간격 · 10초."""
    d = _D("pam", 10)
    pc = lambda t: t / 10 * 100  # noqa: E731
    day = int(REF["general"]["odd_day"]["day"][1:])
    cards = [("분류", "정답이 범주", ["스팸 메일 거르기", "사과 상품 · 불량 예측"]),
             ("회귀", "정답이 숫자", ["집값 예측", "무게로 지름 예측"]),
             ("군집", "비슷한 데이터끼리 묶기", ["고객 그룹 나누기", "가장자리 나무 무리"]),
             ("이상 탐지", "무리에서 튀는 값 찾기", ["카드 이상 결제 찾기", f"특이한 날 {day}일"])]
    s = ""
    for x0, h, sub, t in [(0, "지도학습", "정답 있음", .5), (596, "비지도학습", "정답 없음", 4.5)]:
        s += f'<g {d.show(pc(t))}>' + _t(x0, 20, h, "tt", "start", 'style="font-size:20px"') + _t(x0 + len(h) * 20 + 12, 20, sub, "ts", "start") + "</g>"
    for i, (name, mean, ex) in enumerate(cards):
        x0, y0, t = (0 if i < 2 else 596), (46 if i % 2 == 0 else 226), .5 + i * 2
        s += (f'<g {d.show(pc(t))}><rect x="{x0}" y="{y0}" width="564" height="165" rx="16" fill="{W}" stroke="{K}" stroke-width="2"/>'
              + _mini(x0 + 24, y0 + 22, 170, 121, name, df)
              + _t(x0 + 222, y0 + 38, name, "tt", "start", 'style="font-size:21px"') + _t(x0 + 222, y0 + 68, mean, "ts", "start")
              + "".join(f'<circle cx="{x0 + 228}" cy="{y0 + 104 + k * 30}" r="3.5" fill="{O}"/>'
                        + _t(x0 + 240, y0 + 104 + k * 30, e, "tn", "start", 'style="font-size:16px"') for k, e in enumerate(ex)) + "</g>")
    return d.svg(1160, 400, s)


# ── 기준 바꿔 보기 · 규칙으로 미리 보기 (시뮬레이터의 원리) ─────────────
def rule_whatif(df):
    """무게 · 당도 점에 등급 색 · 기준선 → 당도 하한 11 → 12 로 올리면 바뀌는 점이 빨갛게 · 상품률이 바뀜. 12초."""
    d = _D("paw", 12)
    pc = lambda t: t / 12 * 100  # noqa: E731
    ax, fx, fy = _axes(110, 40, 760, 320, (200, 380), (9, 17), range(200, 381, 40), range(9, 18, 2), "무게 (g)", "당도 (brix)", d.show(0))
    w0, b0, b1 = sk.MIN_W, sk.MIN_SUGAR, 12.0
    ok0 = sk.d_judge(df, sugar=b0) == "없음"
    ok1 = sk.d_judge(df, sugar=b1) == "없음"
    s = ax
    s += f'<rect x="{fx(w0):.1f}" y="40" width="{870 - fx(w0):.1f}" height="{fy(b0) - 40:.1f}" fill="{GOOD}" fill-opacity=".08" {d.show(0, pc(6))}/>'
    s += f'<rect x="{fx(w0):.1f}" y="40" width="{870 - fx(w0):.1f}" height="{fy(b1) - 40:.1f}" fill="{GOOD}" fill-opacity=".08" {d.show(pc(6))}/>'
    s += "".join(f'<circle cx="{fx(r["무게"]):.1f}" cy="{fy(r["당도"]):.1f}" r="3.6" fill="{GOOD if ok0[i] else BAD}"/>' for i, r in df.iterrows())
    flip = df[ok0 & ~ok1]
    s += f'<g {d.show(pc(6))}>' + "".join(f'<circle cx="{fx(r["무게"]):.1f}" cy="{fy(r["당도"]):.1f}" r="4.2" fill="{BAD}" stroke="{N}" stroke-width="1"/>'
                                         for _, r in flip.iterrows()) + "</g>"
    s += f'<line x1="{fx(w0):.1f}" y1="40" x2="{fx(w0):.1f}" y2="360" stroke="{N}" stroke-width="2" stroke-dasharray="7 5"/>' + _t(fx(w0) + 6, 50, f"무게 {w0}g", "tn", "start", 'style="font-size:13px"')
    for b, a_, z_ in [(b0, 0, pc(6)), (b1, pc(6), None)]:
        s += (f'<g {d.show(a_, z_) if z_ else d.show(a_)}><line x1="110" y1="{fy(b):.1f}" x2="870" y2="{fy(b):.1f}" stroke="{O}" stroke-width="3"/>'
              + _t(866, fy(b) - 12, f"당도 하한 {b:g}", "to", "end", 'style="font-size:15px"') + "</g>")
    r0, r1 = sk.d_rate(df, sugar=b0), sk.d_rate(df, sugar=b1)
    for (n, rate), a_, z_ in [(r0, 0, pc(6)), (r1, pc(6), None)]:
        s += (f'<g {d.show(a_, z_) if z_ else d.show(a_)}><rect x="900" y="90" width="250" height="100" rx="14" fill="{W}" stroke="{N}" stroke-width="2.5"/>'
              + _t(1025, 128, f"상품률 {rate:.2f}%", "tt", extra='style="font-size:24px"') + _t(1025, 160, f"상품 {n} / {len(df)}", "ts") + "</g>")
    s += (f'<g {d.show(pc(9))}><rect x="900" y="214" width="250" height="96" rx="14" fill="#FFF8F0" stroke="{O}" stroke-width="2.5"/>'
          + _t(1025, 246, f"하한 {b1:g} · 새로 불량 {len(flip)}개", "tn", extra='style="font-size:15px"') + _t(1025, 278, "기준만 바꿔 결과를 미리 봄", "to", extra='style="font-size:15px"') + "</g>")
    return d.svg(1160, 410, s)


# ── 바이브코딩의 흐름 · 기존 코딩과 두 줄 비교 ────────────────────────
def vibe_flow():
    """위 줄 기존 코딩(사람이 모두) → 아래 줄 바이브코딩(말로 요청 · AI 작성 · 실행 · 사람 확인). 장면 2초 간격 · 26초."""
    d = _D("pav", 26)
    pc = lambda t: t / 26 * 100  # noqa: E731
    lanes = [("기존 코딩", 70, [("설계", 0), ("문법 공부 · 코드 작성", 0), ("실행", 0), ("오류 · 코드 찾아 수정", 0), ("완성", 0)], 1, 3),
             ("바이브코딩", 250, [("말로 요청", 0), ("코드 작성 · 실행", 1), ("화면 확인", 0), ("고칠 점 다시 요청", 0), ("완성", 0)], 1, 3)]
    s = ""
    t = .5
    for name, y, steps, back_to, back_from in lanes:
        s += f'<g {d.show(pc(t))}>' + _t(20, y - 22, name, "tt", "start", 'style="font-size:20px"') + "</g>"
        xs = []
        for i, (h, ai) in enumerate(steps):
            x = 20 + i * 228
            xs.append(x)
            s += (f'<g {d.show(pc(t))}><rect x="{x}" y="{y}" width="196" height="64" rx="12" fill="{"#FFF3E6" if ai else W}" '
                  f'stroke="{O if ai else K}" stroke-width="2.5"/>' + _t(x + 98, y + 33, h, "tn", extra='style="font-size:15px"') + "</g>")
            if i:
                s += f'<g {d.show(pc(t))}><path d="M{x - 28} {y + 32} H{x - 6}" stroke="{N}" stroke-width="2.5" marker-end="url(#{d.id("k")})"/></g>'
            t += 2 if i < len(steps) - 1 else 0
        xa, xb = xs[back_to] + 98, xs[back_from] + 98
        t += 2
        s += f'<g {d.show(pc(t))}><path d="M{xb} {y + 66} C {xb} {y + 104}, {xa} {y + 104}, {xa} {y + 70}" fill="none" stroke="{BAD if name == "기존 코딩" else O}" stroke-width="2.5" stroke-dasharray="6 4" marker-end="url(#{d.id("r" if name == "기존 코딩" else "o")})"/>' \
             + _t((xa + xb) / 2, y + 112, "다시", "ts", extra='style="font-size:13px"') + "</g>"
        t += 2
    s += (f'<g {d.show(pc(t))}><rect x="840" y="12" width="16" height="16" rx="3" fill="{W}" stroke="{K}" stroke-width="2"/>' + _t(862, 20, "사람", "ts", "start")
          + f'<rect x="920" y="12" width="16" height="16" rx="3" fill="#FFF3E6" stroke="{O}" stroke-width="2"/>' + _t(942, 20, "AI · Claude Code", "ts", "start") + "</g>")
    return d.svg(1160, 400, s)
