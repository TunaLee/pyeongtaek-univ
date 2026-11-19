"""평택대 원리 애니메이션 — 타임라인 SVG (anim._D) · 한 번 재생 후 마지막 장면에 멈춤.

함수마다 접두어를 따로 쓴다. 본문 폭 1160 기준.
"""
import math

from anim import G, K, N, O, OK, R, S, W, _D, _box, _dot, _t

MO = "#FFF3E6"


# ── 반도체가 만들어지는 흐름 ─────────────────────────────
def fab_flow():
    """웨이퍼 → FAB 공정 → CP 테스트 → 패키징 → 최종 테스트 → 출하. CP 테스트에서 데이터가 나온다. 12초.
    참고: 공정 순서는 SEMI · 업계 일반 구분 (웨이퍼 제조 → 전공정 → 웨이퍼 테스트 → 후공정)."""
    d = _D("ff", 12)
    st = [("웨이퍼", "실리콘 원판"), ("FAB 공정", "노광 · 식각 · 증착"), ("CP 테스트", "웨이퍼 상태 전기 검사"),
          ("패키징", "다이 자르기 · 포장"), ("최종 테스트", "포장된 칩 검사"), ("출하", "고객")]
    s = ""
    for i, (h, sub) in enumerate(st):
        x = 10 + i * 192
        hl = h == "CP 테스트"
        s += (f'<g {d.show(2 + i * 9)}>' + _box(x, 60, 170, 96, h, sub, fill=MO if hl else W, stroke=O if hl else K, sw=3 if hl else 2.5) + "</g>")
        if i:
            s += f'<g {d.show(1 + i * 9)}><path d="M{x - 20} 108 H{x - 4}" stroke="{G}" stroke-width="3" marker-end="url(#{d.id("k")})"/></g>'
    # CP 테스트에서 데이터가 떨어짐
    s += f'<g {d.show(60)}><path d="M479 160 V236" stroke="{O}" stroke-width="3.5" stroke-dasharray="6 5" marker-end="url(#{d.id("o")})"/></g>'
    s += (f'<g {d.show(66)}><rect x="330" y="244" width="300" height="120" rx="14" fill="{K}"/>'
          + _t(480, 278, "테스트 데이터", "tw", extra='style="font-size:21px"')
          + _t(480, 306, "다이마다 측정값 · Bin · 양불", "tw", extra='style="font-weight:500;fill:#C9D3E0;font-size:15px"')
          + _t(480, 334, "→ CSV 로 내려받음", "tw", extra='style="font-weight:600;fill:#F7C99A;font-size:15px"') + "</g>")
    s += (f'<g {d.show(78)}><rect x="680" y="256" width="460" height="96" rx="14" fill="{W}" stroke="{O}" stroke-width="2.5"/>'
          + _t(910, 290, "이 과정의 실습 데이터", "tt") + _t(910, 320, "CP 테스트 결과 · 웨이퍼 25장 × 다이 616개", "ts") + "</g>")
    return d.svg(1160, 380, s)


# ── 테스트 한 번 → CSV 한 줄 ─────────────────────────────
def test_to_csv():
    """프로브 바늘이 다이에 닿음 → 측정값 → 판정(Bin) → CSV 한 줄 추가. 다이 세 개를 차례로. 14초."""
    d = _D("tc", 14)
    s = ""
    # 웨이퍼 (작은 격자)
    cx, cy, r = 170, 210, 150
    s += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#EEF1F5" stroke="#9AA5B1" stroke-width="2"/>'
    cells = []
    for gy in range(-5, 5):
        for gx in range(-5, 5):
            x0, y0 = cx + gx * 26, cy + gy * 26
            if all((x0 + a - cx) ** 2 + (y0 + b - cy) ** 2 <= (r - 6) ** 2 for a in (0, 26) for b in (0, 26)):
                cells.append((x0, y0))
                s += f'<rect x="{x0 + 1}" y="{y0 + 1}" width="24" height="24" fill="#C9D6E6"/>'
    s += _t(cx, 384, "웨이퍼 · 다이 격자", "ts")
    picks = [cells[3], cells[20], cells[41]]
    vals = [("0.452", "1.06", "1.9", "PASS", "1", OK), ("0.448", "1.04", "34.2", "FAIL", "3", R), ("0.466", "1.08", "2.3", "PASS", "1", OK)]
    # 프로브 (위에서 내려오는 바늘)
    stops = [(0, "transform:translate(0px,-40px);opacity:0")]
    for i, (x0, y0) in enumerate(picks):
        t = 6 + i * 28
        stops += [(t, f"transform:translate({x0 + 12 - 170}px,{y0 - 120 - 40}px);opacity:1"),
                  (t + 5, f"transform:translate({x0 + 12 - 170}px,{y0 - 120}px);opacity:1"),
                  (t + 16, f"transform:translate({x0 + 12 - 170}px,{y0 - 120 - 40}px);opacity:1")]
    stops += [(96, "transform:translate(0px,-40px);opacity:0"), (100, "transform:translate(0px,-40px);opacity:0")]
    s += (f'<g {d.a(stops)}><rect x="140" y="60" width="60" height="26" rx="6" fill="{N}"/>'
          f'<path d="M170 86 L170 120" stroke="{O}" stroke-width="4"/>' + _t(170, 50, "프로브", "to") + "</g>")
    # 측정 → 판정 → CSV
    head = ["vth_v", "idsat_ma", "ioff_na", "pass_fail", "bin"]
    s += (f'<rect x="380" y="40" width="760" height="56" rx="10" fill="{K}"/>'
          + "".join(_t(470 + j * 148, 68, h, "tw", extra='style="font-family:var(--mono,monospace);font-size:15px"') for j, h in enumerate(head)))
    s += _t(760, 22, "wafer_test.csv", "tm")
    for i, ((x0, y0), v) in enumerate(zip(picks, vals)):
        t = 6 + i * 28
        col = v[5]
        s += f'<rect x="{x0 + 1}" y="{y0 + 1}" width="24" height="24" fill="{col}" {d.show(t + 6)}/>'
        y = 108 + i * 64
        s += (f'<g {d.show(t + 8)}><rect x="380" y="{y}" width="760" height="54" rx="10" fill="{W}" stroke="{G}" stroke-width="2"/>'
              + "".join(_t(470 + j * 148, y + 28, v[j], "tm", extra=(f'style="fill:{col};font-size:16px"' if j >= 3 else 'style="font-size:16px"'))
                        for j in range(5)) + "</g>")
        s += f'<path d="M{x0 + 26} {y0 + 12} C 330 {y0 + 12}, 330 {y + 27}, 376 {y + 27}" fill="none" stroke="{O}" stroke-width="2.5" stroke-dasharray="5 4" {d.show(t + 7, t + 20)}/>'
    s += (f'<g {d.show(90)}><rect x="380" y="316" width="760" height="64" rx="12" fill="{MO}" stroke="{O}" stroke-width="2.5"/>'
          + _t(760, 348, "다이 616개 = CSV 616줄 · 웨이퍼 한 장 = 파일 하나", "tt") + "</g>")
    return d.svg(1160, 400, s)


# ── 판정 순서 ────────────────────────────────────────
JUDGE = [("crack", "크랙 있음", "crack ≠ 0"), ("open_short", "오픈 · 쇼트", "rc_ohm > 15"), ("leakage", "누설전류", "ioff_na > 10"),
         ("vth_shift", "문턱전압 이탈", "vth_v 0.38~0.52 밖"), ("particle", "파티클", "particle_cnt ≥ 5"),
         ("parametric", "기타 파라미터", "idsat < 0.92 · ox 밖")]


def sieve():
    """다이 하나가 판정 6단계를 위에서부터 통과 · 처음 걸린 단계가 불량 유형. 다이 셋(양품 · 누설 · 크랙). 14초."""
    d = _D("sv", 14)
    s = ""
    for i, (ft, ko, cond) in enumerate(JUDGE):
        x = 30 + i * 182
        s += (f'<g {d.show(1 + i * 2)}><rect x="{x}" y="120" width="166" height="96" rx="14" fill="{W}" stroke="{K}" stroke-width="2.5"/>'
              + _t(x + 83, 148, f"{i + 1}. {ko}", "tt", extra='style="font-size:17px"') + _t(x + 83, 176, cond, "tm", extra='style="font-size:13px"')
              + _t(x + 83, 200, f"bin {[5, 4, 3, 2, 6, 7][i]}", "ts", extra='style="font-size:13px"') + "</g>")
    s += (f'<g {d.show(14)}><rect x="1120" y="120" width="30" height="96" rx="8" fill="#E8F5E9" stroke="{OK}" stroke-width="2.5"/></g>')
    s += _t(580, 60, "위에서부터 차례로 검사 · 처음 걸린 단계에서 멈춤", "tn", extra='style="font-size:17px"')
    s += f'<path d="M20 168 H1150" stroke="{G}" stroke-width="2" stroke-dasharray="4 6"/>'
    # 다이 세 개: 양품(끝까지) · 누설(3단계) · 크랙(1단계)
    dies = [("다이 A", 6, OK, "양품 · bin 1", 18), ("다이 B", 2, R, "누설전류 · bin 3", 46), ("다이 C", 0, R, "크랙 · bin 5", 72)]
    for k, (name, stop, col, res, t0) in enumerate(dies):
        xs = [113 + i * 182 for i in range(stop + 1)] if stop < 6 else [113 + i * 182 for i in range(6)] + [1135]
        pts = [(0, 40, 168, 0), (t0, 40, 168, 1)]
        for j, x in enumerate(xs):
            pts.append((t0 + 2 + j * 2.4, x, 168, 1))
        tl = t0 + 2 + (len(xs) - 1) * 2.4
        ex = xs[-1]
        pts += [(tl + 3, ex, 268 + k * 46, 1), (100, ex, 268 + k * 46, 1)]
        s += _dot(d, pts, color=col, r=12)
        lx, anc = (ex - 20, "end") if ex > 800 else (ex + 20, "start")
        s += f'<g {d.show(tl + 4)}>' + _t(lx, 268 + k * 46, f"{name} → {res}", "tn", anc, f'style="fill:{col};font-size:17px"') + "</g>"
    return d.svg(1160, 420, s)


# ── Claude Code 의 데이터 작업 고리 ─────────────────────
def data_loop():
    """요청 → CSV 읽기 → 파이썬 작성 → 실행 → 결과 확인 → (틀리면 고침) → 보고. 단계가 차례로 나타남 · 움직이는 점 없음. 14초.
    참고: Claude Code 문서 「How Claude Code works」 — 맥락 모으기 → 행동 → 결과 확인 반복."""
    d = _D("dl", 14)
    s = ""
    s += f'<g {d.show(1)}><rect x="10" y="150" width="170" height="64" rx="32" fill="{N}"/>' + _t(95, 182, "「W07 수율 알려 줘」", "tw", extra='style="font-size:15px"') + "</g>"
    st = [("CSV 읽기", "Read · 앞 5줄 · 열 이름"), ("파이썬 작성", "Write · yield.py"), ("실행", "Bash · python yield.py"), ("결과 확인", "616 · 557 · 90.42%")]
    xy = [(230, 60), (500, 60), (500, 250), (230, 250)]
    for i, ((h, sub), (x, y)) in enumerate(zip(st, xy)):
        s += f'<g {d.show(4 + i * 6)}>' + _box(x, y, 220, 96, h, sub, fill=MO if i == 3 else W, stroke=O if i == 3 else K) + "</g>"
    s += f'<g {d.show(3)}><path d="M184 182 C 205 182, 205 108, 226 108" fill="none" stroke="{N}" stroke-width="3" marker-end="url(#{d.id("k")})"/></g>'
    s += f'<g {d.show(9)}><path d="M454 108 H496" stroke="{K}" stroke-width="3" marker-end="url(#{d.id("k")})"/></g>'
    s += f'<g {d.show(15)}><path d="M610 160 V246" stroke="{K}" stroke-width="3" marker-end="url(#{d.id("k")})"/></g>'
    s += f'<g {d.show(21)}><path d="M496 298 H454" stroke="{K}" stroke-width="3" marker-end="url(#{d.id("k")})"/></g>'
    # 고침 (오류 → 다시 작성)
    s += (f'<g {d.show(40, 62)}><rect x="760" y="250" width="380" height="96" rx="14" fill="#FDECEA" stroke="{R}" stroke-width="2.5"/>'
          + _t(950, 284, "오류 · KeyError \'passfail\'", "tm", extra=f'style="fill:{R};font-size:15px"') + _t(950, 314, "열 이름 확인 → 코드 고침 → 다시 실행", "ts") + "</g>")
    s += f'<g {d.show(42, 62)}><path d="M340 246 C 340 200, 560 200, 560 164" fill="none" stroke="{R}" stroke-width="3" stroke-dasharray="6 5" marker-end="url(#{d.id("r")})"/></g>'
    # 보고
    s += f'<g {d.show(70)}><path d="M340 350 V380 H760" fill="none" stroke="{OK}" stroke-width="3" marker-end="url(#{d.id("g")})"/></g>'
    s += (f'<g {d.show(74)}><rect x="766" y="350" width="374" height="64" rx="14" fill="#E8F5E9" stroke="{OK}" stroke-width="3"/>'
          + _t(953, 382, "보고 · 수율 90.42% (557 / 616)", "tt", extra=f'style="fill:{OK};font-size:18px"') + "</g>")
    return d.svg(1160, 430, s)
