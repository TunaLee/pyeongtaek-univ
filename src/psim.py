"""시뮬레이터 과정 애니메이션 (접두어 sm*). 한 번 재생 → 마지막 장면에 멈춤 · 장면 간격 2초 이상.

- Claude 활용 개념 그림은 anim.py(vibe-coding 에서 복사)의 것을 쓰고 예시 문구만 시뮬레이터로 바꾼다.
- 데이터 그림은 sk.py 의 판정 함수로 숫자를 계산해 그린다.
"""
import anim
import sk
from anim import BG, G, K, N, O, OK, R, S, W, _D, _box, _t

MO = "#FFF3E6"


def _swap(svg, pairs):
    for a, b in pairs:
        assert a in svg, a
        svg = svg.replace(a, b)
    return svg


# ── Claude 활용 그림 (anim.py 예시 문구 교체) ─────────────────
def chat_vs_agent():
    return _swap(anim.chat_vs_agent(), [
        ("「11/10 회의록 정리해 줘」", "「W07 엑셀 요약해 줘」"),
        ("「회의록을 열어 할 일을 표로 정리하세요」", "「필터로 PASS 행 개수 확인」"),
        ("일은 사람 손으로", "사람이 직접 작업"),
        ("out/11-10_정리.md", "docs/데이터_요약.md"), (">하네스<", ">도구<")])


def agent_loop():
    """하네스는 8교시에 정의 → 1교시 그림에서는 Claude Code · 규칙으로."""
    return _swap(anim.agent_loop(), [(">하네스 · 요청 + 지금까지의 결과<", ">규칙 · 요청 + 지금까지의 결과<"),
                                     (">하네스<", ">Claude Code<"), (">하네스 · 조립 · 실행<", ">Claude Code · 조립 · 실행<")])


def context_fill():
    return _swap(anim.context_fill(), [("한도 가까우면 자동으로", "한도 근처 · 자동"), ("회의록 11-03", "W07 엑셀"), ("회의록 11-10", "simulator.html"), ("회의록 11-05", "기준표.md")])


def skill_trigger():
    return _swap(anim.skill_trigger(), [
        ("weekly-report · 주간 보고서를 쓸 때", "excel-summary · 엑셀 요약 문서를 쓸 때"),
        ("meeting-notes · 회의록을 할 일 · 결정으로 정리할 때", "sim-check · 시뮬레이터 숫자를 점검할 때"),
        ("mail-draft · 고객 메일 답장 초안을 쓸 때", "chart-style · 차트 색 · 글자를 맞출 때"),
        ("「11/10 회의록 정리해 줘」", "「조절 바 숫자 점검해 줘」"),
        ("SKILL.md 본문 · meeting-notes", "SKILL.md 본문 · sim-check"),
        ("1. 결정 · 할 일 · 열린 질문으로 나누기", "1. 조절 바 네 가지를 움직여 숫자 기록"),
        ("2. 형식은 양식.md · 다 쓰면 check.py 로 확인", "2. 기대 숫자는 정답표.md · check.py 로 대조"),
        ("양식.md · 읽어서 올림", "정답표.md · 읽어서 올림"), ("부속: 양식.md · check.py", "부속: 정답표.md · check.py")])


def hook_gate():
    return _hook()


def _hook():
    s = anim.hook_gate()
    for a, b in [(">원본/<", ">data/<"), (">회의록 3개<", ">원본 엑셀<"), (">out/<", ">output/<"), (">정리 결과<", ">시뮬레이터<"),
                 ("Edit 원본/11-03.md", "Edit data/W07.xlsx"), ("Write out/정리.md", "Write output/simulator.html"),
                 ("「원본/은 수정 금지 · out/ 에 쓰기」", "「data/ 는 수정 금지 · output/ 에 쓰기」")]:
        s = s.replace(a, b)
    return s


# ── 엑셀 한 행 = 맵 한 칸 = 칩 한 개 ───────────────────────
def row_to_cell():
    """왼쪽 엑셀 행 셋이 차례로 강조 → 오른쪽 맵의 같은 칸이 칠해짐 → 616칸 전체가 판정 색으로. 14초 · 한 번."""
    d = _D("smr", 14)
    df = sk.W07
    pick = [df[df.pass_fail == "PASS"].iloc[40], df[df.fail_type == "crack"].iloc[3], df[df.pass_fail == "PASS"].iloc[300]]
    cols = ["die_x", "die_y", "ioff_na", "pass_fail"]
    s = ""
    # 엑셀 표
    s += f'<rect x="10" y="40" width="500" height="40" fill="#1D6F42"/>' + _t(24, 60, "wafer_test_W07.xlsx · 616행", "tw", "start", 'style="font-size:15px"')
    xs = [70, 170, 280, 410]
    s += f'<rect x="10" y="80" width="500" height="36" fill="#F1F3F4" stroke="#DADCE0"/>'
    for x, c in zip(xs, cols):
        s += _t(x, 98, c, "tm")
    for i, r in enumerate(pick):
        y = 116 + i * 52
        t = 8 + i * 22
        s += f'<rect x="10" y="{y}" width="500" height="52" fill="{W}" stroke="#E3E5E8"/>'
        s += f'<rect x="10" y="{y}" width="500" height="52" fill="{MO}" stroke="{O}" stroke-width="3" {d.show(t)}/>'
        for x, c in zip(xs, cols):
            v = r[c]
            col = (OK if v == "PASS" else R) if c == "pass_fail" else N
            s += _t(x, y + 26, v, "tm", extra=f'style="fill:{col};font-size:16px"')
    s += _t(260, 290, "⋮", "ts", extra='style="font-size:22px"')
    # 웨이퍼 맵
    cx, cy, c = 830, 225, 12.5
    s += f'<circle cx="{cx}" cy="{cy}" r="{15 * c + 6}" fill="#EEF1F5" stroke="#9AA5B1" stroke-width="2"/>'
    allc = ""
    for r in df.itertuples():
        x, y = cx + r.die_x * c, cy - (r.die_y + 1) * c
        allc += f'<rect x="{x:.1f}" y="{y:.1f}" width="{c - 1.5}" height="{c - 1.5}" fill="{"#B9E2C4" if r.pass_fail == "PASS" else "#E8344E"}"/>'
        s += f'<rect x="{x:.1f}" y="{y:.1f}" width="{c - 1.5}" height="{c - 1.5}" fill="#D5DAE1"/>'
    for i, r in enumerate(pick):
        t = 8 + i * 22
        x, y = cx + r.die_x * c, cy - (r.die_y + 1) * c
        col = OK if r.pass_fail == "PASS" else R
        s += (f'<g {d.show(t + 6)}><path d="M512 {142 + i * 52} C 600 {142 + i * 52}, {x - 60:.0f} {y + 6:.0f}, {x - 3:.0f} {y + 6:.0f}" fill="none" '
              f'stroke="{O}" stroke-width="2.5" stroke-dasharray="6 5"/><rect x="{x - 3:.1f}" y="{y - 3:.1f}" width="{c + 4:.1f}" height="{c + 4:.1f}" '
              f'fill="{col}" stroke="{N}" stroke-width="2"/></g>')
    s += f'<g {d.show(78)}>{allc}</g>'
    s += (f'<g {d.show(84)}>' + _t(830, 438, f"합격 {sk.WN['pass']} · 불합격 {sk.WN['fail']}", "tn", extra='style="font-size:16px"') + "</g>")
    s += (f'<g {d.show(4)}>' + _t(260, 20, "엑셀 한 행", "tt") + _t(830, 20, "맵 한 칸 = 칩 한 개", "tt") + "</g>")
    return d.svg(1160, 450, s)


# ── 조절 바 · 합격선이 움직이면 ─────────────────────────────
def slider(vals, stages, lo, hi, bins, unit, name, label, rate_word, prefix, low=False, ticks=5):
    """한쪽 합격선(low=True 면 하한 · 선 왼쪽이 불합격) · stages=[(선 값, 합격 수, 비율)] 를 차례로. 상한이면 선 오른쪽 칸, 하한이면 왼쪽 칸이 빨강. 장면마다 3초 이상. 길이 = 4 + 4×장면 초."""
    dur = 4 + 4 * len(stages)
    d = _D(prefix, dur)
    X0, X1, Y0, H = 70, 1090, 330, 240
    step = (hi - lo) / bins
    cnt = [0] * bins
    over = 0
    for v in vals:
        if v >= hi:
            over += 1
            cnt[-1] += 1
        else:
            cnt[max(0, int((v - lo) / step))] += 1
    mx = max(cnt) * 1.08
    sx = lambda v: X0 + (X1 - X0) * (v - lo) / (hi - lo)  # noqa: E731
    s = f'<line x1="{X0}" y1="{Y0}" x2="{X1}" y2="{Y0}" stroke="{N}" stroke-width="2"/>'
    for k in range(0, ticks + 1):
        v = lo + (hi - lo) * k / ticks
        s += _t(sx(v), Y0 + 22, f"{v:g}", "ts")
    s += _t(X1 + 10, Y0 + 22, unit, "ts", "start")
    s += _t(X0, 24, f"{name} · {len(vals)}개", "tn", "start")
    seg = [(4 + 4 * i) / dur * 100 for i in range(len(stages))] + [100]
    for i in range(bins):
        a, b = lo + i * step, lo + (i + 1) * step
        h = H * cnt[i] / mx
        if not cnt[i]:
            continue
        x, w = sx(a) + 1, sx(b) - sx(a) - 2
        s += f'<rect x="{x:.1f}" y="{Y0 - h:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{K}"/>'
        for k, (thr, *_r) in enumerate(stages):
            if (b <= thr + 1e-9) if low else (a >= thr):
                s += f'<rect x="{x:.1f}" y="{Y0 - h:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{R}" {d.show(seg[k] + 2, seg[k + 1] if k + 1 < len(stages) else None)}/>'
    if over:
        s += _t(sx(hi) - 4, Y0 - H * cnt[-1] / mx - 14, f"{hi:g} 이상 {over}개 포함", "ts", "end", 'style="font-size:13px"')
    # 합격선 · 숫자 카드
    for k, (thr, n, rate) in enumerate(stages):
        a, b = seg[k], (seg[k + 1] if k + 1 < len(stages) else None)
        s += (f'<g {d.show(a, b)}><line x1="{sx(thr):.1f}" y1="{Y0 - H - 20}" x2="{sx(thr):.1f}" y2="{Y0 + 6}" stroke="{O}" stroke-width="4"/>'
              + _t(sx(thr), Y0 - H - 34, f"{label} {thr:g}{unit}", "to", extra='style="font-size:17px"') + "</g>")
        s += (f'<g {d.show(a + 1, b)}><rect x="{X1 - 300}" y="{Y0 + 46}" width="300" height="70" rx="14" fill="{W}" stroke="{N}" stroke-width="2.5"/>'
              + _t(X1 - 150, Y0 + 70, f"{rate_word} {rate:.2f}%", "tt", extra='style="font-size:22px"')
              + _t(X1 - 150, Y0 + 98, f"{n} / {len(vals)}", "ts") + "</g>")
        # 조절 바
        s += (f'<g {d.show(a, b)}><line x1="{X0}" y1="{Y0 + 80}" x2="{X0 + 560}" y2="{Y0 + 80}" stroke="{G}" stroke-width="8" stroke-linecap="round"/>'
              f'<circle cx="{X0 + 560 * (thr - lo) / (hi - lo):.1f}" cy="{Y0 + 80}" r="14" fill="{O}" stroke="{W}" stroke-width="3"/>'
              + _t(X0, Y0 + 112, "조절 바", "ts", "start") + "</g>")
    return d.svg(1160, 450, s)


def wafer_slider():
    v = list(sk.W07.ioff_na)
    st = [(t, *sk.yld(sk.W07, ioff_na=(None, t))) for t in (10, 5, 20)]
    return slider(v, st, 0, 25, 25, " nA", "누설전류 ioff_na", "합격선", "수율", "sms")


def apple_slider():
    v = list(sk.D07["당도"])
    st = [(t, *sk.d_rate(sk.D07, sugar=t)) for t in (sk.MIN_SUGAR, 10.0, 12.0)]
    return slider(v, st, 9, 17, 16, " brix", "당도", "하한", "상품률", "smd", low=True, ticks=8)


# ── 조절 바 한 번 → 네 곳이 함께 ──────────────────────────
def four_updates():
    """조절 바 → 판정 다시 → 숫자 카드 · 맵 · 차트 · 분포 네 곳이 차례로 다시 그려짐. 12초 · 한 번."""
    d = _D("smf", 12)
    s = f'<g {d.show(2)}>' + _box(20, 160, 200, 90, "조절 바", "값이 바뀜", fill=MO, stroke=O) + "</g>"
    s += f'<g {d.show(12)}><path d="M224 205 H286" stroke="{K}" stroke-width="3" marker-end="url(#{d.id("k")})"/></g>'
    s += f'<g {d.show(14)}>' + _box(292, 160, 220, 90, "판정 다시", "616행 전부 · 기준표 순서") + "</g>"
    outs = [("숫자 카드", "합격 · 불합격 · 수율"), ("웨이퍼 맵", "칸 색"), ("사유별 차트", "막대 길이"), ("분포", "합격선 위치")]
    for i, (h, sub) in enumerate(outs):
        y = 20 + i * 100
        t = 30 + i * 14
        s += f'<g {d.show(t)}><path d="M516 205 C 560 205, 560 {y + 40}, 610 {y + 40}" fill="none" stroke="{K}" stroke-width="2.5" marker-end="url(#{d.id("k")})"/></g>'
        s += f'<g {d.show(t + 2)}>' + _box(616, y, 260, 80, h, sub) + "</g>"
        s += f'<g {d.show(t + 6)}><circle cx="910" cy="{y + 40}" r="14" fill="{OK}"/><path d="M903 {y + 40} l5 5 l9 -10" fill="none" stroke="{W}" stroke-width="3"/></g>'
    s += f'<g {d.show(92)}>' + _t(940, 420, "한 곳이라도 그대로면 → 다시 요청", "to", "start", 'style="font-size:15px"') + "</g>"
    return d.svg(1160, 430, s)
