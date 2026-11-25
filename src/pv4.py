"""4교시 원리 애니메이션 — 웨이퍼 맵 (접두어 w4*). 실습 원시 CSV 에서 다이를 그대로 읽어 그린다."""
import csv
import math
import random

from anim import G, K, N, O, OK, R, S, W, _D, _box, _dot, _t
from pkit import LAB

RAW = LAB / "wafer-lab" / "data" / "raw"
TYPE_COL = {"none": "#B9E2C4", "crack": "#7B1FA2", "open_short": "#1565C0", "leakage": "#E65100", "vth_shift": "#C62828",
            "particle": "#00897B", "parametric": "#6D4C41"}
KO = {"none": "양품", "crack": "크랙", "open_short": "오픈·쇼트", "leakage": "누설전류", "vth_shift": "문턱전압 이탈",
      "particle": "파티클", "parametric": "기타 파라미터"}


def dies(w):
    with (RAW / f"wafer_test_{w}.csv").open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _cell(r, cx, cy, c):
    return cx + int(r["die_x"]) * c, cy - (int(r["die_y"]) + 1) * c


def _wafer_bg(cx, cy, c):
    return f'<circle cx="{cx}" cy="{cy}" r="{15 * c + 4}" fill="#EEF1F5" stroke="#9AA5B1" stroke-width="2"/>'


# ── 표와 맵 ─────────────────────────────────────────
def table_vs_map():
    """W07 의 crack 다이 25행 — 표로 내려 읽으면 숫자 목록 · 맵에 찍으면 대각선 한 줄. 12초."""
    d = _D("w4a", 12)
    rows = dies("W07")
    cr = [r for r in rows if r["fail_type"] == "crack"]
    s = ""
    # 왼쪽 표
    s += f'<rect x="10" y="20" width="420" height="44" rx="8" fill="{K}"/>'
    for j, h in enumerate(("die_x", "die_y", "fail_type")):
        s += _t(80 + j * 135, 42, h, "tw", extra='style="font-family:var(--mono,monospace);font-size:15px"')
    for i, r in enumerate(cr[:9]):
        y = 74 + i * 34
        s += (f'<g {d.show(2 + i * 3)}><rect x="10" y="{y}" width="420" height="30" rx="6" fill="{W}" stroke="{G}"/>'
              + _t(80, y + 15, r["die_x"], "tm") + _t(215, y + 15, r["die_y"], "tm") + _t(350, y + 15, "crack", "tm", extra=f'style="fill:#7B1FA2"')
              + "</g>")
    s += f'<g {d.show(30)}>' + _t(220, 400, f"… crack {len(cr)}행 · 위치는 숫자로만 보임", "tn") + "</g>"
    # 오른쪽 맵
    cx, cy, c = 830, 215, 12.5
    s += _wafer_bg(cx, cy, c)
    for r in rows:
        x, y = _cell(r, cx, cy, c)
        s += f'<rect x="{x:.1f}" y="{y:.1f}" width="{c - 1.2:.1f}" height="{c - 1.2:.1f}" fill="#C9D6E6"/>'
    order = sorted(cr, key=lambda r: int(r["die_x"]))
    for i, r in enumerate(order):
        x, y = _cell(r, cx, cy, c)
        s += f'<rect x="{x:.1f}" y="{y:.1f}" width="{c - 1.2:.1f}" height="{c - 1.2:.1f}" fill="#7B1FA2" {d.show(40 + i * 1.3)}/>'
    s += (f'<g {d.show(82)}><rect x="1010" y="30" width="146" height="70" rx="12" fill="#F3E5F5" stroke="#7B1FA2" stroke-width="2.5"/>'
          + _t(1083, 54, "대각선 한 줄", "tn", extra='style="fill:#7B1FA2"') + _t(1083, 80, "스크래치 후보", "ts") + "</g>")
    s += f'<g {d.show(36)}><path d="M450 215 H600" stroke="{O}" stroke-width="3.5" marker-end="url(#{d.id("o")})"/>' + _t(525, 198, "좌표대로 찍기", "to") + "</g>"
    return d.svg(1160, 420, s)


# ── 좌표 → 사각형 ────────────────────────────────────
def coord_to_rect():
    """CSV 한 행의 die_x · die_y → 화면 x · y → 사각형 하나. 그다음 616행이 줄 단위로 채워짐. 14초."""
    d = _D("w4b", 14)
    rows = dies("W07")
    one = next(r for r in rows if r["die_x"] == "4" and r["die_y"] == "-3")
    cx, cy, c = 860, 215, 12.5
    s = _wafer_bg(cx, cy, c)
    # 축
    s += f'<line x1="{cx - 200}" y1="{cy}" x2="{cx + 200}" y2="{cy}" stroke="{G}" stroke-dasharray="4 4"/>'
    s += f'<line x1="{cx}" y1="{cy - 200}" x2="{cx}" y2="{cy + 200}" stroke="{G}" stroke-dasharray="4 4"/>'
    s += _t(cx + 206, cy, "x", "ts", "start") + _t(cx, cy - 206, "y", "ts")
    # 왼쪽: 한 행 → 계산
    s += (f'<g {d.show(1)}><rect x="10" y="30" width="520" height="56" rx="10" fill="{W}" stroke="{K}" stroke-width="2"/>'
          + _t(270, 58, f'die_x = {one["die_x"]}   die_y = {one["die_y"]}   fail_type = {one["fail_type"]}', "tm", extra='style="font-size:16px"') + "</g>")
    s += (f'<g {d.show(10)}><rect x="10" y="110" width="520" height="120" rx="10" fill="{K}"/>'
          + _t(270, 140, "x = 중심 + die_x × 칸 크기", "tw", extra='style="font-family:var(--mono,monospace);font-size:16px"')
          + _t(270, 172, "y = 중심 − (die_y + 1) × 칸 크기", "tw", extra='style="font-family:var(--mono,monospace);font-size:16px"')
          + _t(270, 204, "화면 y 는 아래로 커짐 → 부호 반대", "tw", extra='style="font-weight:500;fill:#C9D6E6;font-size:14px"') + "</g>")
    s += (f'<g {d.show(22)}><rect x="10" y="254" width="520" height="56" rx="10" fill="{"#FFF3E6"}" stroke="{O}" stroke-width="2.5"/>'
          + _t(270, 282, '&lt;rect x=… y=… width=칸 height=칸 fill=색&gt;', "tm", extra='style="font-size:16px;fill:#C76A12"') + "</g>")
    x, y = hx, hy = _cell(one, cx, cy, c)
    s += f'<g {d.show(24)}><path d="M534 282 C 640 282, {x - 60} {y + 6}, {x - 4} {y + 6}" fill="none" stroke="{O}" stroke-width="3" marker-end="url(#{d.id("o")})"/></g>'
    s += f'<rect x="{x:.1f}" y="{y:.1f}" width="{c - 1.2:.1f}" height="{c - 1.2:.1f}" fill="{O}" {d.show(28)}/>'
    # 줄 단위로 채움
    by_y = {}
    for r in rows:
        by_y.setdefault(int(r["die_y"]), []).append(r)
    ys = sorted(by_y, reverse=True)
    for k, yy in enumerate(ys):
        g = ""
        for r in by_y[yy]:
            x, y = _cell(r, cx, cy, c)
            g += f'<rect x="{x:.1f}" y="{y:.1f}" width="{c - 1.2:.1f}" height="{c - 1.2:.1f}" fill="{TYPE_COL[r["fail_type"]]}"/>'
        s += f'<g {d.show(40 + k * 1.5)}>{g}</g>'
    s += f'<rect x="{hx - 1:.1f}" y="{hy - 1:.1f}" width="{c + .8:.1f}" height="{c + .8:.1f}" fill="none" stroke="{O}" stroke-width="3" {d.show(28)}/>'
    s += (f'<g {d.show(88)}><rect x="10" y="340" width="520" height="56" rx="10" fill="#E8F5E9" stroke="{OK}" stroke-width="2.5"/>'
          + _t(270, 368, f"{len(rows)}행 → 사각형 {len(rows)}개 = 웨이퍼 맵", "tt", extra=f'style="fill:{OK};font-size:18px"') + "</g>")
    return d.svg(1160, 420, s)


# ── WM-811K 패턴 9종 (다시 그림) ───────────────────────
PATTERNS = [("none", "없음", 147431), ("Edge-Ring", "가장자리 링", 9680), ("Edge-Loc", "가장자리 국부", 5189),
            ("Center", "중심", 4294), ("Loc", "국부", 3593), ("Scratch", "스크래치", 1193), ("Random", "랜덤", 866),
            ("Donut", "도넛", 555), ("Near-full", "거의 전체", 149)]


def _pat_fail(name, x, y, rr, rnd):
    a = math.atan2(y, x)
    if name == "none": return rnd.random() < .03
    if name == "Edge-Ring": return rr > .82 and rnd.random() < .85
    if name == "Edge-Loc": return rr > .7 and -2.4 < a < -1.2 and rnd.random() < .85
    if name == "Center": return rr < .32 and rnd.random() < .9
    if name == "Loc": return math.hypot(x - 3, y - 3) < 2.6 and rnd.random() < .85
    if name == "Scratch": return abs(y - (-.8 * x + 1)) < .7 and abs(x) < 7
    if name == "Random": return rnd.random() < .2
    if name == "Donut": return .38 < rr < .62 and rnd.random() < .85
    if name == "Near-full": return rnd.random() < .85
    return False


def patterns():
    """WM-811K 패턴 9종을 격자로 다시 그림 · 하나씩 나타남. 10초. 원본 파일은 쓰지 않는다."""
    d = _D("w4c", 10)
    s = ""
    n, c = 9, 8.6
    for k, (name, ko, cnt) in enumerate(PATTERNS):
        col, row = k % 5, k // 5
        cx = 115 + col * 232 + (116 if row else 0)
        cy = 100 + row * 236
        rnd = random.Random(k + 7)
        g = f'<circle cx="{cx}" cy="{cy}" r="{n * c + 6}" fill="#EEF1F5" stroke="#9AA5B1" stroke-width="1.5"/>'
        for gy in range(-n, n):
            for gx in range(-n, n):
                rr = math.hypot(gx + .5, gy + .5) / n
                if rr > .98:
                    continue
                f = _pat_fail(name, gx + .5, gy + .5, rr, rnd)
                g += f'<rect x="{cx + gx * c:.1f}" y="{cy + gy * c:.1f}" width="{c - 1:.1f}" height="{c - 1:.1f}" fill="{R if f else "#B9E2C4"}"/>'
        g += _t(cx, cy + n * c + 26, name, "tt", extra='style="font-size:17px"') + _t(cx, cy + n * c + 48, f"{ko} · {cnt:,}", "ts", extra='style="font-size:14px"')
        s += f'<g {d.show(2 + k * 8)}>{g}</g>'
    return d.svg(1160, 470, s)


# ── 보기 전환 · 존 ───────────────────────────────────
def view_toggle():
    """W21 (ETCH_03) — 양불 보기 → 불량 유형 보기 → 존 경계(50 · 110 mm). 14초."""
    d = _D("w4d", 14)
    rows = dies("W21")
    cx, cy, c = 330, 215, 12.8
    s = _wafer_bg(cx, cy, c)
    pf, ty = "", ""
    for r in rows:
        x, y = _cell(r, cx, cy, c)
        wh = f'x="{x:.1f}" y="{y:.1f}" width="{c - 1.2:.1f}" height="{c - 1.2:.1f}"'
        pf += f'<rect {wh} fill="{"#B9E2C4" if r["pass_fail"] == "PASS" else R}"/>'
        ty += f'<rect {wh} fill="{TYPE_COL[r["fail_type"]]}"/>'
    s += f'<g {d.show(0, 36)}>{pf}</g><g {d.show(36)}>{ty}</g>'
    # 존 경계: 반지름 50 · 110 mm → 1 mm = c/10
    for rad, lab in ((50, "center | mid · 50 mm"), (110, "mid | edge · 110 mm")):
        s += f'<g {d.show(66)}><circle cx="{cx}" cy="{cy}" r="{rad * c / 10:.1f}" fill="none" stroke="{N}" stroke-width="2.5" stroke-dasharray="7 5"/></g>'
    # 오른쪽 설명 단계
    steps = [(2, "① 양불 보기", "초록 PASS · 빨강 FAIL · 가장자리에 몰림"), (38, "② 불량 유형 보기", "주황 누설전류 · 빨강 문턱전압 이탈"),
             (68, "③ 존 경계", "edge 존에 불량 집중 → 가장자리 링")]
    for i, (t, h, sub) in enumerate(steps):
        y = 60 + i * 112
        s += (f'<g {d.show(t)}><rect x="640" y="{y}" width="500" height="92" rx="14" fill="{"#FFF3E6" if i == 2 else W}" '
              f'stroke="{O if i == 2 else K}" stroke-width="2.5"/>' + _t(890, y + 32, h, "tt") + _t(890, y + 62, sub, "ts") + "</g>")
    cnt = {}
    for r in rows:
        if r["pass_fail"] != "PASS":
            cnt[r["zone"]] = cnt.get(r["zone"], 0) + 1
    s += f'<g {d.show(80)}>' + _t(890, 410, f'불량 다이 · center {cnt.get("center", 0)} · mid {cnt.get("mid", 0)} · edge {cnt.get("edge", 0)}', "tn") + "</g>"
    return d.svg(1160, 430, s)


# ── 툴팁 ─────────────────────────────────────────────
def tooltip():
    """W07 맵 위에서 커서가 크랙 다이 · 양품 다이로 이동 → 그 다이의 CSV 값이 툴팁에. 10초."""
    d = _D("w4e", 10)
    rows = dies("W07")
    cx, cy, c = 300, 215, 12.8
    s = _wafer_bg(cx, cy, c)
    for r in rows:
        x, y = _cell(r, cx, cy, c)
        s += f'<rect x="{x:.1f}" y="{y:.1f}" width="{c - 1.2:.1f}" height="{c - 1.2:.1f}" fill="{TYPE_COL[r["fail_type"]]}"/>'
    a = next(r for r in rows if r["fail_type"] == "crack" and r["die_x"] == "0")
    b = next(r for r in rows if r["fail_type"] == "leakage")
    pts = [(0, cx, cy + 260, 0)]
    for t0, r in ((8, a), (52, b)):
        x, y = _cell(r, cx, cy, c)
        pts += [(t0, x + 6, y + 6, 1), (t0 + 36, x + 6, y + 6, 1)]
        tip = (f'({r["die_x"]}, {r["die_y"]}) · {KO[r["fail_type"]]}', f'vth {r["vth_v"]} V · idsat {r["idsat_ma"]} mA',
               f'ioff {r["ioff_na"]} nA · rc {r["rc_ohm"]} Ω', f'bin {r["bin"]} · {r["pass_fail"]}')
        g = f'<rect x="620" y="{90 if t0 < 50 else 230}" width="500" height="130" rx="12" fill="{N}"/>'
        for i, line in enumerate(tip):
            g += _t(640, (90 if t0 < 50 else 230) + 26 + i * 27, line, "tw", "start", 'style="font-weight:600;font-size:16px"')
        g += f'<path d="M{x + 14} {y + 6} L616 {(90 if t0 < 50 else 230) + 20}" stroke="{O}" stroke-width="2" stroke-dasharray="4 4"/>'
        s += f'<g {d.show(t0 + 4)}>{g}</g>'
    pts += [(100, *pts[-1][1:3], 1)]
    s += _dot(d, pts, color=O, r=7)
    return d.svg(1160, 430, s)
