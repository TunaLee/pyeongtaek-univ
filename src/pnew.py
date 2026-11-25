"""새 장 — AI 전반(LLM · 도구) · CLAUDE.md · Skill · 하네스 개념, 실습(사과 집계 · 분석 Skill · 정적 · 동적 웹 ·
보고서 템플릿 · GitHub · Vercel 배포 · 마지막 프로젝트).

교시는 없다. build.py 의 OUTLINE 이 장 제목으로 골라 순서를 정하고, 꼬리표 · 실습 번호는 build.py 가 다시 붙인다
(여기 실습 번호 11-3 · 21-1 … 은 자리표). 숫자는 sk.DN · sk.WN 에서 계산한다. CSS 접두어 pn.
vibe-coding 1부(LLM · 배포) · 3부(CLAUDE.md · Skill · 하네스) 장을 이 과정 예시로 옮긴 것.
"""
import sk
import viz2
from anim import K, N, O, OK, R, W, _D, _t
from deck import flow, lab, light
from hx import code, esc
from pkit import brief, chat
from stats_hx import src

T = "실습"            # build.py 가 장마다 다시 붙임
DN, WN = sk.DN, sk.WN
GOOD, BAD = "#2BA84A", "#E8344E"


# ── AI 전반 ─────────────────────────────────────────────
def llm():
    """LLM — 이름 풀이 → 글(토큰)을 읽고 쓰기만 함 → 도구 없이 못 하는 일. vibe-coding 1-1 「LLM」."""
    name = "".join(f'<div class="pnlN" style="--d:{d}s"><i>{c}</i><b>{en} · {ko}</b><small>{x}</small></div>'
                   for c, en, ko, x, d in [("L", "Large", "큰", "인터넷 · 책 · 코드 등 아주 많은 글로 학습", .3),
                                           ("L", "Language", "언어", "사람의 말 · 글 · 프로그래밍 언어", 1.3),
                                           ("M", "Model", "모델", "다음에 올 글 조각(토큰)을 고르는 계산", 2.3)])
    head = ('<div class="pnlH" style="--d:3.6s"><span>글 (토큰)</span><i></i><b>LLM</b><i></i><span>글 (토큰)</span>'
            '<em>읽고 쓰기만 하는 모델 · Claude · GPT · Gemini</em></div>')
    ok = "".join(f'<li style="--d:{d}s">{t}</li>' for t, d in [("질문 읽기", 5.4), ("답 쓰기", 5.9), ("코드를 글로 쓰기", 6.4)])
    no = "".join(f'<li style="--d:{d}s">{t}</li>' for t, d in [("엑셀 파일 열기 · 저장", 8.0), ("코드 실행", 8.5), ("결과 화면 확인", 9.0)])
    return (f'<div class="pnlNs">{name}</div>' + head + f'<div class="pnlG"><div class="pnlC ok" style="--d:5.2s"><b>할 수 있는 일</b><ul>{ok}</ul></div>'
            f'<div class="pnlC no" style="--d:7.8s"><b>도구 없이 못 하는 일</b><ul>{no}</ul></div></div>')


# ── 도구가 필요한 이유 · 토큰을 확률로 골라 이어 씀 ─────────────────
def token_pick(a=48217, b=29356):
    """LLM 이 곱셈 답을 토큰 단위로 이어 씀 — 토큰마다 후보 셋 · 확률 막대(길이만 · 값은 예) → 셋째 토큰에서 강조 틀이
    후보 사이를 오가다 막대가 가장 길지 않은 후보에 멈춤 → 그럴듯한 틀린 답 · 오른쪽 계산 도구는 코드로 계산한 값.
    정답은 a*b 로 계산 · 틀린 토큰은 셋째 묶음 첫 자리만 바꾼 것. 20초 · 한 번 · 마지막 장면 = 셋째 토큰 후보 + 두 답."""
    d = _D("pnt", 20)
    pc = lambda t: t / 20 * 100  # noqa: E731
    ok = a * b
    g = f"{ok:,}".split(",")                                   # 1 · 415 · 458 · 252
    bad = ("7" if g[2][0] != "7" else "3") + g[2][1:]          # 758
    sw = lambda s, i, c: s[:i] + str(c) + s[i + 1:]  # noqa: E731
    # (후보 · 확률 예, 고른 번호, 창 시작, 고르는 때, 창 끝) — 막대 길이만 보이고 숫자는 적지 않음
    steps = [([(g[0] + ",", .86), (str(int(g[0]) + 1) + ",", .09), ("9", .05)], 0, .8, 3.0, 4.6),
             ([(g[1] + ",", .71), (sw(g[1], 2, (int(g[1][2]) - 1) % 10) + ",", .17),
               (sw(g[1], 2, (int(g[1][2]) + 1) % 10) + ",", .12)], 0, 4.6, 6.8, 8.4),
             ([(g[2] + ",", .38), (bad + ",", .34), (sw(g[2], 1, 1) + ",", .28)], 1, 8.4, 12.0, 14.0),
             ([(g[3], .80), (sw(g[3], 1, 6), .12), (sw(g[3], 0, 3), .08)], 0, 14.0, 15.6, 17.0)]
    toks = [st[0][st[1]][0] for st in steps]                   # 1, · 415, · 758, · 252
    cw = [30 + 16 * len(t) for t in toks]
    cx = [360 + sum(cw[:i]) + 10 * i for i in range(4)]
    ROW = [222, 286, 350]
    mono = 'style="font-size:{}px;fill:{}"'.format

    # 질문 줄 · 답 칸
    s = (f'<rect x="0" y="14" width="1160" height="80" rx="14" fill="#F4F6F9" stroke="#DDE3EA" stroke-width="1.5"/>'
         + _t(30, 54, f"{a:,} × {b:,} =", "tm", "start", mono(28, N)))
    for x, w in zip(cx, cw):
        s += f'<rect x="{x}" y="31" width="{w}" height="46" rx="10" fill="none" stroke="#C9CFD8" stroke-width="2" stroke-dasharray="5 5"/>'
    for i, (st, x, w) in enumerate(zip(steps, cx, cw)):
        s += (f'<g {d.show(pc(st[3] + .4))}><rect x="{x}" y="31" width="{w}" height="46" rx="10" fill="{W}" stroke="{K}" stroke-width="2"/>'
              + _t(x + w / 2, 55, toks[i], "tm", "middle", mono(26, N)) + "</g>")
    s += (f'<g {d.show(pc(17))}><rect x="{cx[2]}" y="31" width="{cw[2]}" height="46" rx="10" fill="#FDECEC" stroke="{R}" stroke-width="2.5"/>'
          + _t(cx[2] + cw[2] / 2, 55, toks[2], "tm", "middle", mono(26, R))
          + _t(cx[3] + cw[3] + 30, 55, "✕", "tt", "middle", f'style="font-size:30px;fill:{R}"') + "</g>")

    # 왼쪽 · LLM 이 토큰을 고르는 판
    s += (f'<rect x="0" y="110" width="748" height="310" rx="16" fill="{W}" stroke="#DDE3EA" stroke-width="1.5"/>'
          + _t(24, 142, "LLM · 다음 토큰을 확률로 골라 이어 씀", "tn", "start", 'style="font-size:17px"')
          + _t(724, 142, "후보 · 확률 막대는 예", "ts", "end", 'style="font-size:13.5px"'))

    def rows(k, cand, mark=None):
        """mark: {번호: (테두리 색, 칠, 막대 색, 꼬리표, 꼬리표 색)} — 강조할 줄."""
        r = _t(24, 180, f"토큰 {k + 1} / 4", "to", "start", 'style="font-size:15px"')
        for j, (tok, p) in enumerate(cand):
            y = ROW[j]
            m = (mark or {}).get(j)
            if m:
                r += f'<rect x="14" y="{y - 29}" width="720" height="58" rx="12" fill="{m[1]}" stroke="{m[0]}" stroke-width="3"/>'
            r += (_t(44, y, tok, "tm", "start", mono(26, N))
                  + f'<rect x="200" y="{y - 14}" width="{p * 480:.0f}" height="28" rx="6" fill="{m[2] if m else "#C9D3E0"}"/>')
            if m:
                r += _t(716, y, m[3], "to", "end", f'style="font-size:15px;fill:{m[4]}"')
        return r

    for k, (cand, pick, t0, tp, t1) in enumerate(steps):
        y = ROW[pick]
        body = f'<g {d.show(pc(tp))}><rect x="14" y="{y - 29}" width="720" height="58" rx="12" fill="#FFF3E6" stroke="{O}" stroke-width="3"/></g>'
        top = (f'<g {d.show(pc(tp))}><rect x="200" y="{y - 14}" width="{cand[pick][1] * 480:.0f}" height="28" rx="6" fill="{O}"/>'
               + _t(716, y, "고름", "to", "end") + "</g>")
        if k == 2:   # 셋째 토큰 · 강조 틀이 후보 사이를 오가다 멈춤 (확률로 뽑기)
            seq = [(9.6, 0), (10.0, 2), (10.4, 1), (10.8, 0), (11.2, 2), (11.6, 1)]
            st = [(0, "opacity:0;transform:translate(0px,0px)")]
            for (t, r_), nxt in zip(seq, seq[1:] + [(tp, None)]):
                dy = ROW[r_] - ROW[0]
                st += [(pc(t), f"opacity:1;transform:translate(0px,{dy}px)"),
                       (pc(nxt[0]) - .05, f"opacity:1;transform:translate(0px,{dy}px)")]
            st += [(pc(tp) + .3, f"opacity:0;transform:translate(0px,{ROW[1] - ROW[0]}px)"), (100, "opacity:0")]
            body = (f'<rect x="14" y="{ROW[0] - 29}" width="720" height="58" rx="12" fill="none" stroke="{O}" stroke-width="3" '
                    f'stroke-dasharray="8 5" {d.a(st)}/>' + body)
        s += f'<g {d.show(pc(t0), pc(t1))}>' + body + rows(k, cand) + top + "</g>"
    # 마지막 장면 · 셋째 토큰 후보를 다시 보여 줌 (뽑힌 758 · 막대가 가장 긴 458)
    s += (f'<g {d.show(pc(17))}>' + rows(2, steps[2][0], {
        0: ("#C9E7CC", "#F1F8F2", OK, "실제 값", OK),
        1: (R, "#FDECEC", R, "뽑힘 · 틀림", R)}) + "</g>")

    # 오른쪽 · 계산 도구
    s += (f'<g {d.show(pc(17.6))}><rect x="772" y="110" width="388" height="310" rx="16" fill="#F1F8F2" stroke="{OK}" stroke-width="2.5"/>'
          + _t(792, 142, "계산 도구 · 코드로 실제 계산", "tn", "start", f'style="font-size:17px;fill:{OK}"')
          + f'<rect x="792" y="172" width="348" height="58" rx="10" fill="{N}"/>'
          + _t(812, 201, f"{a} * {b}", "tm", "start", mono(24, W))
          + f'<path d="M966 240 V276" stroke="{OK}" stroke-width="3" marker-end="url(#{d.id("g")})"/></g>')
    s += (f'<g {d.show(pc(18.4))}>'
          + _t(966, 318, f'{g[0]},{g[1]},<tspan style="fill:{OK};text-decoration:underline">{g[2]}</tspan>,{g[3]}', "tm", "middle", mono(32, N))
          + _t(966, 372, "✓ 다시 해도 같은 답", "tn", "middle", f'style="font-size:16px;fill:{OK}"') + "</g>")
    return d.svg(1160, 430, s)


# ── 정적 웹과 동적 웹 ─────────────────────────────────────
def static_dynamic():
    """위 줄 정적 웹(브라우저 ↔ 서버 · 만들어 둔 파일 그대로) → 아래 줄 동적 웹(서버가 DB 를 읽어 요청마다 만듦). 12초."""
    d = _D("pnw", 12)
    pc = lambda t: t / 12 * 100  # noqa: E731

    def box(x, y, w, h, title, sub, t, fill=W, stroke=K):
        return (f'<g {d.show(pc(t))}><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="{stroke}" stroke-width="2.5"/>'
                + _t(x + w / 2, y + h / 2 - 10, title, "tt", extra='style="font-size:17px"') + _t(x + w / 2, y + h / 2 + 14, sub, "ts", extra='style="font-size:13px"') + "</g>")

    def arrow(x1, x2, y, label, t, c=O, up=True):
        mk = d.id("o") if c == O else d.id("k")
        ly = y - 12 if up else y + 16
        return (f'<g {d.show(pc(t))}><path d="M{x1} {y} H{x2}" stroke="{c}" stroke-width="3" marker-end="url(#{mk})"/>'
                + _t((x1 + x2) / 2, ly, label, "tn", extra=f'style="font-size:13px;fill:{c}"') + "</g>")

    def card(y, title, rows, t, c):
        s = f'<g {d.show(pc(t))}><rect x="760" y="{y}" width="390" height="150" rx="14" fill="{W}" stroke="{c}" stroke-width="2.5"/>'
        s += _t(782, y + 30, title, "tt", "start", f'style="font-size:20px;fill:{c}"')
        for i, (k, v) in enumerate(rows):
            s += _t(782, y + 64 + i * 28, k, "ts", "start", 'style="font-size:13px"') + _t(872, y + 64 + i * 28, v, "tn", "start", 'style="font-size:14px"')
        return s + "</g>"

    s = _t(20, 16, "정적 웹", "tt", "start", 'style="font-size:19px"')
    s += box(20, 40, 170, 76, "브라우저", "주소 입력", .5) + box(330, 40, 190, 76, "서버", "HTML 파일 보관", .5)
    s += arrow(192, 326, 66, "① 주소 요청", 1.5, K) + arrow(328, 194, 96, "② 만들어 둔 파일 그대로", 3, O, up=False)
    s += card(10, "정적 웹", [("받는 내용", "누가 열어도 같은 파일"), ("예", "회사 소개 · 강의 자료 · 보고서 템플릿"),
                              ("배포 위치", "Vercel · GitHub Pages")], 4.5, K)
    s += f'<line x1="20" y1="186" x2="1150" y2="186" stroke="#D9DDE3" stroke-width="2" stroke-dasharray="6 6"/>'
    s += f'<g {d.show(pc(6))}>' + _t(20, 214, "동적 웹", "tt", "start", 'style="font-size:19px"') + "</g>"
    s += box(20, 238, 170, 76, "브라우저", "로그인 · 장바구니", 6) + box(330, 238, 190, 76, "서버 프로그램", "요청마다 HTML 생성", 6)
    s += (f'<g {d.show(pc(6))}><path d="M590 248 V304 A44 11 0 0 0 678 304 V248" fill="#EEF3FA" stroke="{K}" stroke-width="2.5"/>'
          f'<ellipse cx="634" cy="248" rx="44" ry="11" fill="#EEF3FA" stroke="{K}" stroke-width="2.5"/>' + _t(634, 282, "DB", "tt", extra='style="font-size:17px"') + "</g>")
    s += arrow(192, 326, 264, "① 요청", 7, K) + arrow(522, 586, 264, "② 조회", 8, K) + arrow(586, 522, 294, "③ 데이터", 9, O, up=False)
    s += arrow(328, 194, 294, "④ 요청마다 만든 HTML", 10, O, up=False)
    s += card(208, "동적 웹", [("받는 내용", "사람마다 다른 화면"), ("예", "쇼핑몰 · 은행 · 게시판"), ("필요 요소", "서버 프로그램 · DB")], 11, O)
    return d.svg(1160, 370, s)


# ── 보고서 템플릿 ──────────────────────────────────────────
def report_template():
    """엑셀 파일 칩이 브라우저 창으로 들어감 → 카드 · 맵 · 차트가 채워짐 → 결과 파일이 나옴 · 서버 · DB 없음. 12초."""
    d = _D("pnr", 12)
    pc = lambda t: t / 12 * 100  # noqa: E731
    s = ""
    # 입력 · 엑셀 파일
    s += (f'<g {d.show(pc(.5))}><rect x="10" y="130" width="190" height="64" rx="10" fill="#E8F5EC" stroke="#1D6F42" stroke-width="2.5"/>'
          + _t(105, 154, "wafer_test_W26.xlsx", "tm", extra='style="font-size:12.5px"') + _t(105, 176, "① 엑셀 올리기", "tn", extra='style="font-size:14px;fill:#1D6F42"') + "</g>")
    s += f'<g {d.show(pc(2))}><path d="M204 162 H262" stroke="{O}" stroke-width="3" marker-end="url(#{d.id("o")})"/></g>'
    # 브라우저 창 · index.html
    s += (f'<g {d.show(pc(2))}><rect x="270" y="40" width="560" height="300" rx="12" fill="{W}" stroke="{K}" stroke-width="2.5"/>'
          f'<path d="M270 70 V52 Q270 40 282 40 H818 Q830 40 830 52 V70 Z" fill="#EEF1F4"/>'
          + "".join(f'<circle cx="{288 + i * 16}" cy="55" r="5" fill="#C9CFD8"/>' for i in range(3))
          + _t(350, 55, "이름.vercel.app · index.html", "tm", "start", 'style="font-size:12px"')
          + _t(550, 92, "② 브라우저 JS 가 읽고 판정 · 집계", "tn", extra=f'style="font-size:14px;fill:{O}"') + "</g>")
    # 보고서 화면 — 카드 · 맵 · 차트 · 조절 바
    cards = [("전체", "", 290), ("합격", "", 420), ("수율", "", 550), ("불합격", "", 680)]
    s += f'<g {d.show(pc(4))}>' + "".join(
        f'<rect x="{x}" y="110" width="122" height="52" rx="8" fill="{W}" stroke="#D9DDE3" stroke-width="1.5"/>'
        + _t(x + 61, 126, lab_, "ts", extra='style="font-size:11px"') + f'<rect x="{x + 22}" y="138" width="78" height="12" rx="4" fill="{K}"/>'
        for lab_, _, x in cards) + "</g>"
    grid = "".join(f'<rect x="{292 + (i % 12) * 13}" y="{180 + (i // 12) * 13}" width="11" height="11" rx="2" fill="{BAD if (i * 7) % 23 == 0 else GOOD}"/>'
                   for i in range(12 * 10))
    s += f'<g {d.show(pc(5.5))}>{grid}' + _t(370, 322, "맵", "ts", extra='style="font-size:12px"') + "</g>"
    bars = "".join(f'<rect x="{470 + i * 30}" y="{310 - h}" width="22" height="{h}" rx="3" fill="{BAD if i < 2 else "#F2A0AC"}"/>' for i, h in enumerate([110, 74, 50, 34, 22]))
    s += f'<g {d.show(pc(6.5))}>{bars}' + _t(530, 322, "사유별 막대", "ts", extra='style="font-size:12px"') + "</g>"
    s += (f'<g {d.show(pc(7.5))}>' + _t(700, 196, "누설전류 상한", "ts", extra='style="font-size:12px"')
          + f'<rect x="640" y="214" width="120" height="6" rx="3" fill="#F6C99A"/><circle cx="690" cy="217" r="9" fill="{W}" stroke="{O}" stroke-width="3"/>'
          + _t(700, 246, "조절 바", "ts", extra='style="font-size:12px"') + "</g>")
    # 출력 · 결과 내려받기
    s += f'<g {d.show(pc(9))}><path d="M834 190 H892" stroke="{O}" stroke-width="3" marker-end="url(#{d.id("o")})"/></g>'
    s += (f'<g {d.show(pc(9))}><rect x="900" y="158" width="250" height="64" rx="10" fill="#FFF8F0" stroke="{O}" stroke-width="2.5"/>'
          + _t(1025, 182, "판정결과.csv", "tm", extra='style="font-size:13px"') + _t(1025, 204, "③ 결과 내려받기", "tn", extra=f'style="font-size:14px;fill:{O}"') + "</g>")
    s += (f'<g {d.show(pc(10.5))}><rect x="270" y="352" width="560" height="34" rx="17" fill="#EEF1F4"/>'
          + _t(550, 369, "서버 · DB 없음 · HTML 한 파일 · 올린 파일은 내 PC 브라우저 안에서만 읽음", "tn", extra='style="font-size:13.5px"') + "</g>")
    return d.svg(1160, 392, s)


def slides():
    a07 = f"{DN['rows']}행 · 상품 {DN['pass']} · {DN['rate']}%"
    w07 = f"{WN['rows']}행 · 합격 {WN['pass']} · 수율 {WN['yield']}%"
    return [
        # ── Ⅱ AI 전반
        light("LLM", llm(), T),
        light("도구가 필요한 이유", token_pick(), T),
        # ── Ⅱ CLAUDE.md
        light("CLAUDE.md에 적을 내용", viz2.tiles([
            ("같은 실수가 두 번", "원본 엑셀을 고쳐 저장"), ("같은 설명을 또 함", "「결과는 output/ 에 저장」"),
            ("새로 온 사람도 알아야 함", "data/ 는 읽기만")], 3)
              + viz2.maprows([
                  ("「원본은 고치지 마」", "data/ 는 읽기만 · 결과는 output/ 에", ""),
                  ("「쉬운 말로 써 줘」", "반도체 용어를 새로 꺼내지 않는다", ""),
                  ("「숫자 다시 확인해 줘」", "계산한 코드 · 행 수를 함께 보고", "")], "또 한 말", "CLAUDE.md 한 줄"), T),
        # ── Ⅱ Skill
        light("Skill의 정의", flow([("한 번 써 둠", "절차 · 형식 · 기준"), ("요청", "「사과 엑셀 요약해 줘」"),
                                  ("Claude 가 꺼냄", "설명(description)과 맞으면"), ("같은 결과", "매번 같은 절차 · 형식")], hl=2)
              + viz2.tiles([("폴더 하나", "SKILL.md + 참고 파일"), ("마크다운 글", "코드를 몰라도 작성"), ("다시 쓰는 지시서", "대화가 바뀌어도 그대로")], 3), T),
        light("SKILL.md 예", '<div class="twocol w"><div>' + code(".claude/skills/excel-summary/SKILL.md", esc(
            "---\nname: excel-summary\ndescription: 엑셀 · CSV 파일을 요약 문서로 정리할 때\n---\n"
            "1. 몇 행 · 몇 열 · 열마다 뜻\n2. 수치형 열 · 평균 · 최솟값 · 최댓값\n3. 범주형 열 · 값별 개수\n"
            "4. docs/요약.md 에 저장 · 원본은 고치지 않음")) + "</div><div>"
              + viz2.tiles([("위치", ".claude/skills/이름/SKILL.md"), ("맨 위 두 줄", "name · description · Claude 가 고르는 기준"),
                            ("본문", "절차 · 형식 · 기준")], 1) + "</div></div>"
              + src(("Claude Code 문서 · Skills", "https://code.claude.com/docs/en/skills")), T),
        light("CLAUDE.md vs Skill", viz2.pair(
            "CLAUDE.md", [("불러오는 시점", "대화를 시작할 때마다"), ("내용", "지킬 규칙 · 폴더 · 계산 방법"), ("예", "「data/ 는 읽기만」")],
            "Skill", [("불러오는 시점", "요청이 설명과 맞을 때만"), ("내용", "일의 절차 · 형식 · 기준"), ("예", "「엑셀 요약 순서」")]), T),
        # ── Ⅱ 하네스
        light("Claude Code = 기본 하네스", viz2.pair(
            "처음부터 있는 부품", [("내장 도구", "파일 읽기 · 검색 · 실행 · 웹"), ("컨텍스트 관리", "한도 근처에서 자동 요약"),
                               ("권한 모드", "수정 · 명령 전에 확인")],
            "직접 더하는 부품", [("CLAUDE.md", "규칙"), ("Skill", "절차"), ("Hook", "꼭 지킬 규칙 · 자동 차단")])
              + src(("Claude Code 문서 · How Claude Code works", "https://code.claude.com/docs/en/how-claude-code-works")), T),

        # ── 실습 · 사과 집계 (사유별 합계 · 엑셀 필터로 확인)
        lab("11-3", "사과 집계 엑셀 · CSV", T, "사과를 사유별 · 위치별로 집계해 엑셀 시트 세 장과 CSV 로 저장하고 엑셀 필터로 센 숫자와 맞춘다",
            ["사과 집계 · CSV 요청", "사유별 합계 대조", "엑셀 필터로 상품 수 세기"],
            [f"상품률 {DN['rate']}%", "apple_summary.xlsx (시트 3장)", "apple_A07.csv"], files="data/apple_A07.xlsx"),
        brief("11-3", T,
              ["사과 집계 · CSV", "사유별 합계 대조", "엑셀 필터로 대조"],
              [("목표", "요약 · 사유별 · 위치별 집계"), ("입력", "apple_A07.xlsx"),
               ("산출물", "apple_summary.xlsx(시트 3장) · apple_A07.csv"), ("하지 말 것", "data/ 원본 수정")],
              [], [f"상품 {DN['pass']} · 불량 {DN['fail']}", "사유별 합 = 불량 수"], ""),
        light("실습 11-3 확인", chat([
            ("me", "apple_summary.xlsx 의 사유별 시트 합계가 불량 수와 같은지 확인해 줘."),
            ("ai", f"사유별 합계 {sum(DN['reason'].values())} · 불량 {DN['fail']} · 같음\n"
                   + " · ".join(f"{sk.D_KO[k]} {v}" for k, v in DN["reason"].items()))], "확인 대화 예"), T),

        # ── 실습 · Skill 로 반도체 분석
        light("분석 Skill 흐름", flow([("사과로 한 번", "요약 · 집계 · 대조"), ("Skill 만들기", "data-report · SKILL.md"),
                                    ("웨이퍼에 적용", "「data-report 로 W07 분석해 줘」"), ("같은 형식의 결과", "요약 문서 · 집계 엑셀")], hl=1)
              + viz2.pair("사과 · apple_A07", [("한 행", "사과 한 개"), ("판정", "상품 · 불량"), ("결과", a07)],
                          "웨이퍼 · W07", [("한 행", "칩 한 개"), ("판정", "합격 · 불합격"), ("결과", w07)]), T),
        lab("21-1", "사과 분석 Skill 만들기", T, "사과 분석에서 한 순서(요약 · 집계 · 대조)를 data-report Skill 하나로 만든다",
            ["지금까지 한 요청 · 결과 정리 요청", "SKILL.md 초안 요청", "설명 · 절차 · 산출물 확인", "사과 파일로 다시 돌려 보기"],
            [".claude/skills/data-report/SKILL.md", f"다시 돌린 사과 결과 · {a07}", "결과 형식이 앞 실습과 같음"], files="docs/ · output/"),
        brief("21-1", T,
              ["지금까지 한 요청 · 결과 정리", "SKILL.md 초안", "설명 · 절차 · 산출물 확인", "사과로 다시 돌려 보기"],
              [("목표", "앞 실습 순서를 Skill 하나로"), ("입력", "사과 요약 · 집계 결과"),
               ("산출물", ".claude/skills/data-report/SKILL.md"), ("하지 말 것", "사과 열 이름을 절차에 박아 넣기")],
              [], ["설명(description)에 「엑셀 분석」", "사과로 다시 돌려 같은 숫자"], ""),
        lab("21-2", "Skill 로 웨이퍼 분석", T, "data-report Skill 로 W07 을 사과와 같은 형식으로 분석하고 숫자를 대조한다",
            ["「data-report 로 W07 분석해 줘」", "요약 · 집계 확인", "엑셀 필터로 숫자 대조", "Skill 에 빠진 단계 보완"],
            [w07, "웨이퍼 요약 문서", "yield_summary.xlsx (시트 3장)"], files="data/wafer_test_W07.xlsx"),
        brief("21-2", T,
              ["data-report 로 W07 분석", "요약 · 집계 확인", "엑셀 필터로 대조", "Skill 보완"],
              [("목표", "같은 Skill · 다른 데이터"), ("입력", "wafer_test_W07.xlsx · data-report Skill"),
               ("산출물", "웨이퍼 요약 · 집계 엑셀"), ("하지 말 것", "Skill 없이 처음부터 다시 설명")],
              [], [f"수율 {WN['yield']}%", f"사유별 합 = 불합격 {WN['fail']}"], ""),

        # ── 실습 · 화면
        light("정적 웹과 동적 웹", static_dynamic(), T),

        # ── 실습 · 보고서 템플릿
        light("보고서 템플릿", report_template(), T),
        lab("31-1", "보고서 템플릿", T, "simulator.html 에 엑셀 올리기 · 결과 내려받기를 넣어 어떤 웨이퍼 파일이든 분석하는 보고서로 만든다",
            ["엑셀 · CSV 올리기 요청", "다른 웨이퍼 파일로 확인", "결과 내려받기 요청", "index.html 한 파일로 정리"],
            [f"W07 을 올리면 수율 {WN['yield']}%", "다른 파일을 올리면 카드 · 맵 · 차트 · 조절 바가 다시 계산", "판정 결과 CSV 내려받기"],
            files="output/simulator.html · data/new/"),
        brief("31-1", T,
              ["엑셀 · CSV 올리기", "다른 웨이퍼 파일로 확인", "결과 내려받기", "index.html 한 파일"],
              [("목표", "엑셀을 올리면 다시 분석하는 보고서"), ("입력", "simulator.html · data/new/ 의 웨이퍼 파일"),
               ("산출물", "index.html 한 파일"), ("하지 말 것", "서버 · DB · data/ 원본 수정")],
              [], [f"W07 수율 {WN['yield']}%", "다른 파일이면 숫자가 바뀜"], ""),

        # ── 실습 · GitHub · Vercel 배포
        light("배포 흐름", flow([("내 폴더", "index.html · 커밋"), ("GitHub", "저장소 · 파일 보관"), ("Vercel", "저장소를 가져와 공개"),
                               ("주소", "이름.vercel.app"), ("누구나", "주소로 열고 엑셀 올리기")], hl=2)
              + viz2.tiles([("연결 ① Claude Code → GitHub", "gh 로 저장소 만들기 · 올리기 · 요청 한 줄"),
                            ("연결 ② GitHub → Vercel", "한 번 연결하면 이후 자동")], 2), T),
        light("GitHub · Vercel 준비", viz2.tiles([
            ("GitHub", "github.com · 이메일로 가입 · 저장소 보관"), ("Vercel", "vercel.com · GitHub 계정으로 가입 · Hobby 무료"),
            ("Git", "버전 기록 도구 · 「Git 설치돼 있는지 확인해 줘」")], 3)
              + src(("GitHub", "https://github.com/signup"), ("Vercel", "https://vercel.com/signup"), ("GitHub CLI", "https://cli.github.com/")), T),
        light("수정과 재배포", '<div class="twocol"><div>'
              + chat([("me", "판정 결과 버튼 색을 주황으로 바꿔 줘"), ("ai", "index.html 의 버튼 색 변경 완료"),
                      ("me", "커밋하고 GitHub 에 올려 줘"), ("ai", "커밋 「버튼 색 변경」 → push 완료 · Vercel 새 배포 시작")], "Claude Code 대화")
              + "</div><div>"
              + viz2.tiles([("① 수정 요청", "Claude Code"), ("② 내 PC 에서 확인", "index.html 열기"), ("③ 커밋 · push", "올리기 요청"),
                            ("④ Vercel 자동 배포", "push 감지 · 1~2분"), ("⑤ 같은 주소에 반영", "새 링크 없음")], 1)
              + "</div></div>" + src(("Vercel · Git", "https://vercel.com/docs/git")), T),
        light("배포 전 점검", viz2.tiles([
            ("키 · 비밀번호", "코드 · 파일에 들어 있지 않은지"), ("데이터 파일", "저장소에 올리지 않음 · 보고서는 올린 파일만 읽음"),
            ("배포 주소는 공개", "주소를 아는 누구나 열람"), ("Hobby 는 개인 · 비상업", "회사 서비스는 Pro 이상")], 2)
              + src(("Vercel · Hobby", "https://vercel.com/docs/plans/hobby")), T),
        lab("31-2", "GitHub · Vercel 배포", T, "보고서 템플릿을 GitHub 저장소에 올리고 Vercel 로 배포해 주소를 공유한다",
            ["GitHub 로그인 (gh)", "올리기 전 점검 요청", "저장소 만들고 올리기 요청", "Vercel 가져오기 · Deploy"],
            ["저장소 주소 · github.com/내계정/이름", "배포 주소 · 이름.vercel.app", "다른 PC 에서 엑셀 올려 분석"], files="index.html"),
        brief("31-2", T,
              ["gh 로그인 (브라우저 승인)", "올리기 전 점검", "저장소 만들고 올리기", "Vercel 가져오기 · Deploy"],
              [("목표", "보고서를 인터넷 주소에 공개"), ("입력", "index.html · GitHub · Vercel 계정"),
               ("산출물", "저장소 주소 · 배포 주소"), ("하지 말 것", "데이터 파일 · 개인 정보 올리기")],
              [], [f"배포 주소에서 W07 수율 {WN['yield']}%", "고친 뒤 같은 주소에 반영"], ""),

        # ── 실습 · 마지막 프로젝트
        light("프로젝트 주제", viz2.tiles([
            ("내 데이터", "전공 실험 · 동아리 · 아르바이트 기록 엑셀"), ("공개 데이터", "공공데이터포털 · 기관 통계 엑셀 · CSV"),
            ("자유 주제", "만들고 싶은 웹 도구 · 계산기 · 기록장")], 3)
              + viz2.tiles([("조건", "엑셀 · CSV 를 올리거나 값을 입력 → 화면에서 결과"), ("배포", "Vercel 주소 하나")], 2)
              + src(("공공데이터포털", "https://www.data.go.kr/")), T),
        light("프로젝트 진행 순서", flow([("주제 · 데이터", "하나 고르기"), ("CLAUDE.md · 계획", "규칙 · Plan Mode"),
                                       ("만들기 · 확인", "나눠서 요청"), ("배포", "GitHub · Vercel 주소")], hl=2), T),
        lab("41-1", "마지막 프로젝트", T, "고른 데이터나 주제로 웹을 만들어 Vercel 에 배포한다",
            ["주제 · 데이터 고르기", "CLAUDE.md 만들기", "Plan Mode 로 계획", "나눠서 만들기 · 확인", "GitHub · Vercel 배포"],
            ["배포 주소가 열림", "입력을 바꾸면 결과가 바뀜", "CLAUDE.md · (필요하면) Skill"], files="내 폴더"),
        brief("41-1", T,
              ["주제 · 데이터", "요청 항목 · CLAUDE.md", "Plan Mode 계획", "나눠서 만들기", "배포 · 발표"],
              [("목표", "한 문장 · 누가 · 무엇을"), ("입력", "엑셀 · CSV · 직접 입력"), ("산출물", "index.html · 배포 주소"),
               ("하지 말 것", "개인정보 · 키 올리기 · 한 번에 다 요청")],
              [], ["배포 주소가 열림", "입력을 바꾸면 결과가 바뀜"], ""),
    ]


CSS = """
  /* LLM · 읽고 쓰기 (pnl) */
  .pnlNs{display:grid; grid-template-columns:repeat(3,1fr); gap:14px; margin-bottom:16px;}
  .pnlN{display:grid; grid-template-columns:auto 1fr; column-gap:12px; align-items:center; background:#fff; border:2px solid #D9DDE3; border-radius:14px; padding:10px 16px;
    opacity:0; animation:pnIn .6s var(--d) forwards;}
  .pnlN i{grid-row:span 2; font-style:normal; font-size:34px; font-weight:900; color:#F28C28; width:34px; text-align:center;}
  .pnlN b{font-size:20px; color:#16233A;}
  .pnlN small{font-size:15px; color:#3A4657;}
  .pnlH{display:flex; align-items:center; gap:14px; background:#16233A; color:#fff; border-radius:14px; padding:12px 22px; margin-bottom:16px; opacity:0; animation:pnIn .6s var(--d) forwards;}
  .pnlH span{font-size:20px; font-weight:800; background:#2C4466; border-radius:8px; padding:6px 14px;}
  .pnlH b{font-size:28px; background:#F28C28; border-radius:10px; padding:6px 20px;}
  .pnlH i{width:30px; height:3px; background:#8FA3BC;}
  .pnlH em{font-style:normal; font-size:20px; color:#D6DEEA; margin-left:16px;}
  .pnlG{display:grid; grid-template-columns:1fr 1fr; gap:20px;}
  .pnlC{border-radius:14px; padding:18px 22px; border:2px solid #9FC5A8; background:#F4FBF6; opacity:0; animation:pnIn .6s var(--d) forwards;}
  .pnlC.no{border-color:#E6B0AA; background:#FFFAFA;}
  .pnlC b{font-size:22px; color:#1E7B45;} .pnlC.no b{color:#A93226;}
  .pnlC ul{list-style:none; margin:12px 0 0; padding:0; display:flex; flex-direction:column; gap:10px;}
  .pnlC li{font-size:21px; font-weight:700; color:#16233A; opacity:0; animation:pnIn .5s var(--d) forwards;}
  .pnlC.ok li:before{content:"✓ "; color:#1E7B45;} .pnlC.no li:before{content:"✕ "; color:#C0392B;}
  @keyframes pnIn{from{opacity:0} to{opacity:1}}
  .flow .fs b, .flow .fs span{word-break:keep-all;}
  @media print{.pnlN,.pnlH,.pnlC,.pnlC li{opacity:1; animation:none}}
"""
