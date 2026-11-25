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
    """같은 요청 「사과 엑셀 요약해 줘」 — 왼쪽 채팅: AI 는 브라우저 창 안 · 붙여 넣기 · 코드 옮겨 실행 · 저장은 사람(빨간 화살표).
    오른쪽 에이전트: Claude Code 가 내 컴퓨터 폴더 안에서 읽기 · 실행 · 저장 · 결과 보고(주황 화살표). 14초.
    참고: Claude Code 문서 「How Claude Code works」(파일 읽기 · 명령 실행 · 파일 수정 도구)."""
    d = _D("smc", 14)
    pc = lambda t: t / 14 * 100  # noqa: E731
    DN = sk.DN
    AI_C, AI_F = O, MO

    def chip(x, y, name, t, w=158):
        return (f'<g {d.show(pc(t))}><rect x="{x}" y="{y}" width="{w}" height="44" rx="9" fill="{W}" stroke="{K}" stroke-width="2"/>'
                + _t(x + w / 2, y + 22, name, "tm", extra='style="font-size:13px"') + "</g>")

    def label(x, y, num, who, what, c, t, anchor="start"):
        return f'<g {d.show(pc(t))}>' + _t(x, y, f"{num} {who} · {what}", "tn", anchor, f'style="font-size:14px;fill:{c}"') + "</g>"

    def arrow(path, c, t, dash=False):
        mk = d.id("r" if c == R else "o")
        da = ' stroke-dasharray="7 5"' if dash else ""
        return f'<g {d.show(pc(t))}><path d="{path}" fill="none" stroke="{c}" stroke-width="3"{da} marker-end="url(#{mk})"/></g>'

    # ── 왼쪽 · 채팅 ──
    s = (_t(10, 20, "채팅", "tt", "start", 'style="font-size:22px"') + _t(78, 22, "AI 는 브라우저 창 안 · 파일 작업은 사람", "ts", "start", 'style="font-size:15px"'))
    s += (f'<g {d.show(pc(.3))}><rect x="300" y="40" width="250" height="132" rx="12" fill="{W}" stroke="{K}" stroke-width="2"/>'
          f'<path d="M300 64 V52 Q300 40 312 40 H538 Q550 40 550 52 V64 Z" fill="{N}"/>'
          + _t(425, 52, "채팅 창 · 브라우저", "tw", extra='style="font-size:13px"')
          + f'<rect x="376" y="72" width="164" height="28" rx="10" fill="{N}"/>' + _t(458, 86, "「사과 엑셀 요약해 줘」", "tw", extra='style="font-size:12px"') + "</g>")
    s += (f'<g {d.show(pc(3))}><rect x="310" y="108" width="230" height="56" rx="10" fill="#F1F3F6"/>'
          + _t(320, 122, "② AI · 글 · 코드로 답함", "tn", "start", f'style="font-size:12.5px;fill:{AI_C}"')
          + f'<rect x="320" y="134" width="210" height="22" rx="4" fill="#1E2433"/>'
          + "".join(f'<rect x="{330 + k * 62}" y="142" width="{50 - k * 8}" height="6" rx="3" fill="#8FA3BF"/>' for k in range(3)) + "</g>")
    s += (f'<g {d.show(pc(.3))}><rect x="10" y="214" width="540" height="194" rx="16" fill="#F7F8FA" stroke="#C9CFD8" stroke-width="2" stroke-dasharray="7 5"/>'
          + _t(26, 236, "내 컴퓨터", "tn", "start", 'style="font-size:15px"') + "</g>")
    s += chip(26, 262, "apple_A07.xlsx", .3) + chip(201, 262, "summary.py", 4.5) + chip(376, 262, "사과_요약.md", 6)
    s += arrow("M105 260 V86 H370", R, 1.5, True) + label(115, 72, "①", "사람", "엑셀 내용 붙여 넣기", R, 1.5)
    s += arrow("M420 174 V196 H280 V256", R, 4.5, True) + label(410, 184, "③", "사람", "코드 옮겨 실행", R, 4.5, "end")
    s += arrow("M361 284 H370", R, 6, True) + label(376, 330, "④", "사람", "결과 저장", R, 6)

    # ── 오른쪽 · 에이전트 ──
    X = 600
    s += (f'<g {d.show(pc(7))}>' + _t(X + 10, 20, "에이전트", "tt", "start", 'style="font-size:22px"')
          + _t(X + 108, 22, "AI 가 내 컴퓨터 폴더 안에서 작업", "ts", "start", 'style="font-size:15px"') + "</g>")
    s += (f'<g {d.show(pc(7))}><rect x="{X + 10}" y="120" width="540" height="288" rx="16" fill="#F7F8FA" stroke="#C9CFD8" stroke-width="2" stroke-dasharray="7 5"/>'
          + _t(X + 26, 142, "내 컴퓨터 · 프로젝트 폴더", "tn", "start", 'style="font-size:15px"')
          + f'<rect x="{X + 190}" y="152" width="180" height="52" rx="14" fill="{AI_F}" stroke="{AI_C}" stroke-width="2.5"/>'
          + _t(X + 280, 178, "Claude Code", "tt", extra='style="font-size:18px"') + "</g>")
    s += (f'<g {d.show(pc(7.5))}><rect x="{X + 155}" y="40" width="250" height="38" rx="19" fill="{N}"/>'
          + _t(X + 280, 59, "「사과 엑셀 요약해 줘」", "tw", extra='style="font-size:14px"')
          + f'<path d="M{X + 280} 80 V146" stroke="{N}" stroke-width="3" marker-end="url(#{d.id("k")})"/>'
          + _t(X + 292, 104, "① 사람 · 요청", "tn", "start", f'style="font-size:14px;fill:{N}"') + "</g>")
    s += chip(X + 26, 286, "apple_A07.xlsx", 7) + chip(X + 201, 286, "summary.py", 10.5) + chip(X + 376, 286, "사과_요약.md", 12)
    s += arrow(f"M{X + 188} 178 H{X + 105} V280", AI_C, 9) + label(X + 115, 238, "②", "AI", "파일 읽기", AI_C, 9)
    s += arrow(f"M{X + 280} 206 V280", AI_C, 10.5) + label(X + 290, 250, "③", "AI", "작성 · 실행", AI_C, 10.5)
    s += arrow(f"M{X + 372} 178 H{X + 455} V280", AI_C, 12) + label(X + 465, 238, "④", "AI", "저장", AI_C, 12)
    s += (f'<g {d.show(pc(13))}><rect x="{X + 26}" y="346" width="508" height="46" rx="12" fill="#E8F5E9" stroke="{OK}" stroke-width="2"/>'
          + _t(X + 280, 369, f"⑤ AI · 결과 보고 · {DN['rows']}행 · 상품 {DN['pass']} · 상품률 {DN['rate']:.2f}%", "tn",
               extra=f'style="font-size:15px;fill:{OK}"') + "</g>")
    s += f'<line x1="575" y1="10" x2="575" y2="410" stroke="{G}" stroke-width="2" stroke-dasharray="6 6"/>'
    return d.svg(1160, 420, s)


def agent_loop():
    """Claude Code 문서 「How Claude Code works」의 고리 — 요청 → 맥락 모으기 → 작업 → 결과 확인 → (틀리면 다시) → 완료 · 보고.
    고리를 먼저 그린 뒤 두 바퀴: 1바퀴 확인에서 「틀림 → 다시」 · 2바퀴 「맞음 → 완료」. 사람은 언제든 멈추고 방향을 바꿈.
    다른 장보다 천천히(장면 간격 코드 3초 → 화면 약 1.2초). 34초. 하네스라는 말은 8교시에 정의하므로 쓰지 않는다."""
    d = _D("sml", 34)
    pc = lambda t: t / 34 * 100  # noqa: E731
    DN = sk.DN
    BAD, GOOD = "#E8344E", "#2BA84A"
    nodes = {"맥락": (300, 168, "맥락 모으기", "파일 찾기 · 열 이름 읽기"), "작업": (475, 40, "작업", "요약 코드 작성 · 실행"),
             "확인": (650, 168, "결과 확인", f"상품 + 불량 = {DN['rows']} 점검")}
    NW, NH = 176, 74

    def node(key, t):
        x, y, h, sub = nodes[key]
        return (f'<g {d.show(pc(t))}><rect x="{x}" y="{y}" width="{NW}" height="{NH}" rx="16" fill="{MO}" stroke="{O}" stroke-width="2.5"/>'
                + _t(x + NW / 2, y + 28, h, "tt", extra='style="font-size:19px"') + _t(x + NW / 2, y + 54, sub, "ts", extra='style="font-size:13px"') + "</g>")

    def glow(key, t0, t1, c):
        x, y, *_ = nodes[key]
        return f'<rect x="{x - 5}" y="{y - 5}" width="{NW + 10}" height="{NH + 10}" rx="20" fill="none" stroke="{c}" stroke-width="5" {d.show(pc(t0), pc(t1))}/>'

    s = (f'<g {d.show(pc(.5))}><rect x="10" y="182" width="230" height="46" rx="23" fill="{N}"/>'
         + _t(125, 205, "「사과 엑셀 요약해 줘」", "tw", extra='style="font-size:14px"') + "</g>")
    s += f'<g {d.show(pc(3))}><path d="M242 205 H294" stroke="{N}" stroke-width="3" marker-end="url(#{d.id("k")})"/></g>' + node("맥락", 3)
    s += f'<g {d.show(pc(6))}><path d="M420 166 C 440 120, 455 100, 470 92" fill="none" stroke="{O}" stroke-width="3" marker-end="url(#{d.id("o")})"/></g>' + node("작업", 6)
    s += f'<g {d.show(pc(9))}><path d="M652 92 C 668 100, 690 120, 706 164" fill="none" stroke="{O}" stroke-width="3" marker-end="url(#{d.id("o")})"/></g>' + node("확인", 9)
    s += (f'<g {d.show(pc(12))}><path d="M738 246 C 738 338, 388 338, 388 248" fill="none" stroke="{O}" stroke-width="3" stroke-dasharray="7 5" marker-end="url(#{d.id("o")})"/>'
          + _t(563, 334, "틀리면 다시", "to", extra='style="font-size:15px"') + _t(563, 196, "완료될 때까지 반복", "tn", extra='style="font-size:15px"') + "</g>")
    # 두 바퀴 — 지금 단계가 빛남
    p1 = [("맥락", 14), ("작업", 16.5), ("확인", 19)]
    p2 = [("맥락", 22.5), ("작업", 25), ("확인", 27.5)]
    for key, t in p1 + p2:
        c = BAD if (key, t) == ("확인", 19) else GOOD if (key, t) == ("확인", 27.5) else O
        s += glow(key, t, t + 2.3, c)
    s += f'<g {d.show(pc(14), pc(22.3))}>' + _t(563, 222, "1바퀴", "to", extra='style="font-size:16px"') + "</g>"
    s += f'<g {d.show(pc(22.5), pc(31))}>' + _t(563, 222, "2바퀴", "to", extra='style="font-size:16px"') + "</g>"
    s += f'<g {d.show(pc(19.5), pc(22.3))}>' + _t(836, 262, "틀림 · 다시", "tn", "start", f'style="font-size:15px;fill:{BAD}"') + "</g>"
    s += f'<g {d.show(pc(28))}>' + _t(836, 262, "맞음", "tn", "start", f'style="font-size:15px;fill:{GOOD}"') + "</g>"
    s += f'<path d="M738 246 C 738 338, 388 338, 388 248" fill="none" stroke="{BAD}" stroke-width="4" stroke-dasharray="7 5" {d.show(pc(21), pc(22.6))}/>'
    # 완료 · 보고
    s += (f'<g {d.show(pc(30))}><path d="M830 205 H892" stroke="{GOOD}" stroke-width="3.5" marker-end="url(#{d.id("g")})"/>'
          + _t(861, 190, "맞으면", "tn", extra=f'style="font-size:13px;fill:{GOOD}"')
          + f'<rect x="898" y="150" width="252" height="112" rx="16" fill="#E8F5E9" stroke="{GOOD}" stroke-width="2.5"/>'
          + _t(1024, 180, "완료 · 보고", "tt", extra=f'style="font-size:19px;fill:{GOOD}"')
          + _t(1024, 210, "docs/사과_요약.md", "tm", extra='style="font-size:13px"')
          + _t(1024, 238, f"{DN['rows']}행 · 상품 {DN['pass']} · {DN['rate']:.2f}%", "tn", extra='style="font-size:14px"') + "</g>")
    s += (f'<g {d.show(pc(32))}><rect x="898" y="292" width="252" height="58" rx="14" fill="{W}" stroke="{N}" stroke-width="2" stroke-dasharray="6 4"/>'
          + _t(1024, 313, "사람 · 언제든 끼어듦", "tn", extra='style="font-size:14px"') + _t(1024, 335, "Esc 로 멈춤 · 고칠 점 입력", "ts", extra='style="font-size:13px"') + "</g>")
    return d.svg(1160, 360, s)


def context_fill():
    return _swap(anim.context_fill(), [("한도 가까우면 자동으로", "한도 근처 · 자동"), ("회의록 11-03", "apple_A07.xlsx"), ("회의록 11-10", "사과_요약.md"), ("회의록 11-05", "선별기준표.md")])


def skill_trigger():
    return _swap(anim.skill_trigger(), [
        ("weekly-report · 주간 보고서를 쓸 때", "slide-make · 발표 자료 초안을 만들 때"),
        ("meeting-notes · 회의록을 할 일 · 결정으로 정리할 때", "excel-summary · 엑셀 · CSV 를 요약 문서로 정리할 때"),
        ("mail-draft · 고객 메일 답장 초안을 쓸 때", "chart-style · 차트 색 · 글자를 맞출 때"),
        ("「11/10 회의록 정리해 줘」", "「사과 엑셀 요약해 줘」"),
        ("SKILL.md 본문 · meeting-notes", "SKILL.md 본문 · excel-summary"),
        ("1. 결정 · 할 일 · 열린 질문으로 나누기", "1. 행 · 열 · 열마다 뜻 · 수치형 · 범주형"),
        ("2. 형식은 양식.md · 다 쓰면 check.py 로 확인", "2. 형식은 양식.md · 다 쓰면 check.py 로 숫자 대조"),
        ])


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
