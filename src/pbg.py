"""배경 장 그림 — 빅데이터의 등장 · 3V · 하루 간편결제 건수(한국은행) · 바이브코딩까지의 변화 · 데이터 분석과 엔지니어링의 변화 · Git 이전의 버전 관리.

언어 발전 · AI 코딩 도구 변화 · 파일 이름 버전 관리는 vibe-coding 강의(1-1 · 1-5)의 구성을 이 과정 예시로 옮긴 것.
장면 간격 2초 이상 · 한 번 재생 후 마지막 장면에 멈춤. CSS 접두어 pbg.
"""
import math

from anim import K, N, O, W, _D, _t
from hx import esc
import sk

GRAY = "#9AA5B1"

# ── 빅데이터의 등장 · 연표 ─────────────────────────────────────────
# 연도 · 사실은 원문에서 확인: Laney 노트 「3-D Data Management: Controlling Data Volume, Velocity and Variety」(META Group, 2001-02-06 · 본인 재게시)
# · Apache Hadoop 사이트(2006-02 코드 분리 · 2006-03-30 새 프로젝트) · Apple 보도자료(2007-01-09) · McKinsey Global Institute 보고서(2011)
# · OpenAI 「Introducing ChatGPT」(2022-11-30)
BIG = [  # (해, 분류, 이름, 설명 두 줄, 강조)
    (2001, "개념", "3V", ("전자상거래 데이터의", "양 · 속도 · 다양성"), False),
    (2006, "기술", "Hadoop", ("컴퓨터 여러 대에", "나눠 저장 · 처리"), False),
    (2007, "기기", "스마트폰", ("아이폰 공개", "위치 · 사진 · 결제 기록"), False),
    (2011, "확산", "빅데이터", ("McKinsey 보고서", "경쟁의 핵심 기반"), True),
    (2022, "AI", "생성형 AI", ("ChatGPT 공개", "대규모 데이터로 학습"), False),
]
LANEY = ("Laney 2001", "https://community.aiim.org/blogs/doug-laney/2012/08/25/deja-vvvu-gartners-original-volume-velocity-variety-definition-of-big-data")
BIG_SRC = [LANEY,
           ("Apache Hadoop 2006", "https://svn.apache.org/repos/asf/hadoop/common/tags/release-0.1.0/site/index.html"),
           ("Apple 2007", "https://www.apple.com/newsroom/2007/01/09Apple-Reinvents-the-Phone-with-iPhone/"),
           ("McKinsey 2011", "https://www.mckinsey.com/business-functions/mckinsey-digital/our-insights/big-data-the-next-frontier-for-innovation"),
           ("OpenAI 2022", "https://openai.com/index/chatgpt/")]


def bigdata_timeline():
    """2001 3V → 2006 Hadoop → 2007 스마트폰 → 2011 빅데이터 확산(강조) → 2022 생성형 AI. 칸이 2초 간격 · 기준선이 따라 이어짐. 12초."""
    d = _D("pbb", 12)
    pc = lambda t: t / 12 * 100  # noqa: E731
    Y, L0, L1 = 172, 30, 1130
    xs = [118 + i * 231 for i in range(len(BIG))]
    ts = [.5 + i * 2 for i in range(len(BIG))]
    draw = [(0, "stroke-dashoffset:1"), (pc(.3), "stroke-dashoffset:1")]
    draw += [(pc(t + .6), f"stroke-dashoffset:{1 - (x + 60 - L0) / (L1 - L0):.3f}") for x, t in zip(xs, ts)]
    draw += [(pc(ts[-1] + 1.2), "stroke-dashoffset:0"), (100, "stroke-dashoffset:0")]
    s = (f'<path d="M{L0} {Y} H{L1}" stroke="{N}" stroke-width="3" pathLength="1" stroke-dasharray="1" fill="none" {d.a(draw)}/>')
    for (yr, cat, name, sub, hi), x, t in zip(BIG, xs, ts):
        c = O if hi else K
        s += (f'<g {d.show(pc(t))}>'
              f'<rect x="{x - 36}" y="{Y - 140}" width="72" height="28" rx="14" fill="{"#FFF3E6" if hi else "#EEF1F4"}"/>'
              + _t(x, Y - 126, cat, "tn", extra=f'style="font-size:14px;fill:{c}"')
              + _t(x, Y - 66, yr, "tt", extra=f'style="font-size:32px;fill:{c}"')
              + f'<circle cx="{x}" cy="{Y}" r="12" fill="{c}" stroke="{W}" stroke-width="4"/>'
              + _t(x, Y + 46, name, "tt", extra=f'style="font-size:21px;fill:{c}"')
              + "".join(_t(x, Y + 82 + k * 24, ln, "ts", extra='style="font-size:15px"') for k, ln in enumerate(sub)) + "</g>")
    return d.svg(1160, 320, s)


# ── 빅데이터의 3V · 양 · 속도 · 다양성 (Laney 2001) ─────────────────────
V3 = [("양", "Volume", "기존 도구로 다루기 어려운 크기", "예 · 전국 결제 기록 · 검색 기록"),
      ("속도", "Velocity", "실시간으로 쉬지 않고 생김", "예 · 카드 결제 · 공장 센서"),
      ("다양성", "Variety", "형식이 서로 다른 데이터", "예 · 상품 리뷰 · 검사 사진")]


def _v_volume(d, pc, cx, t0):
    """엑셀 한 시트 틀 안을 줄이 채움 → 틀 위로 넘침."""
    s = (f'<g {d.show(pc(t0))}><rect x="{cx - 110}" y="150" width="220" height="130" rx="6" fill="none" stroke="{N}" stroke-width="2" stroke-dasharray="7 5"/>'
         + _t(cx, 298, "엑셀 한 시트", "ts", extra='style="font-size:14px"') + "</g>")
    s += f'<g {d.show(pc(t0 + 1))}>' + "".join(f'<rect x="{cx - 98}" y="{158 + k * 17}" width="196" height="10" rx="3" fill="{K}" fill-opacity=".75"/>' for k in range(7)) + "</g>"
    s += f'<g {d.show(pc(t0 + 2))}>' + "".join(f'<rect x="{cx - 98 + (k % 2) * 8}" y="{133 - k * 17}" width="196" height="10" rx="3" fill="{O}"/>' for k in range(3)) + "</g>"
    return s


def _v_velocity(d, pc, cx, t0):
    """시간 축 위로 기록 눈금이 왼쪽부터 차례로 촘촘히 찍힘."""
    s = (f'<g {d.show(pc(t0))}><line x1="{cx - 140}" y1="250" x2="{cx + 140}" y2="250" stroke="{N}" stroke-width="2" marker-end="url(#{d.id("k")})"/>'
         + _t(cx + 140, 274, "시간", "ts", "end", 'style="font-size:14px"') + "</g>")
    xs = [cx - 132 + k * 9.4 for k in range(29)]
    for g in range(4):
        grp = xs[g * 8:(g + 1) * 8]
        s += f'<g {d.show(pc(t0 + 1 + g * .6))}>' + "".join(
            f'<rect x="{x:.1f}" y="{208 + (k * 7) % 20}" width="4" height="{36 - (k * 7) % 20}" rx="2" fill="{O if g == 3 else K}"/>'
            for k, x in enumerate(grp)) + "</g>"
    return s


def _v_variety(d, pc, cx, t0):
    """표 · 글 · 사진 · 영상 · 센서 기록 — 모양이 다른 다섯 칸."""
    tw, th = 92, 66
    pos = [(cx - 150, 112), (cx - 46, 112), (cx + 58, 112), (cx - 98, 214), (cx + 6, 214)]
    def tile(k, x, y):
        g = f'<rect x="{x}" y="{y}" width="{tw}" height="{th}" rx="8" fill="{W}" stroke="{K}" stroke-width="2"/>'
        if k == 0:    # 표
            g += "".join(f'<line x1="{x + 10}" y1="{y + 14 + r * 13}" x2="{x + tw - 10}" y2="{y + 14 + r * 13}" stroke="{K}" stroke-width="1.5"/>' for r in range(4))
            g += "".join(f'<line x1="{x + 10 + c * 24}" y1="{y + 14}" x2="{x + 10 + c * 24}" y2="{y + 53}" stroke="{K}" stroke-width="1.5"/>' for c in range(4))
        elif k == 1:  # 글
            g += "".join(f'<rect x="{x + 12}" y="{y + 14 + r * 12}" width="{tw - 24 - (r == 3) * 26}" height="5" rx="2" fill="{GRAY}"/>' for r in range(4))
        elif k == 2:  # 사진
            g += (f'<circle cx="{x + 66}" cy="{y + 20}" r="7" fill="{O}"/>'
                  f'<path d="M{x + 10} {y + 56} L{x + 36} {y + 28} L{x + 54} {y + 46} L{x + 64} {y + 38} L{x + 82} {y + 56} Z" fill="{K}" fill-opacity=".7"/>')
        elif k == 3:  # 영상
            g += f'<path d="M{x + 38} {y + 20} L{x + 60} {y + 33} L{x + 38} {y + 46} Z" fill="{K}"/>'
        else:         # 센서 기록
            g += f'<polyline points="{x + 10},{y + 40} {x + 24},{y + 22} {x + 36},{y + 48} {x + 50},{y + 18} {x + 62},{y + 44} {x + 82},{y + 30}" fill="none" stroke="{O}" stroke-width="3"/>'
        return g
    names = ["표", "글", "사진", "영상", "센서 기록"]
    s = ""
    for k, (x, y) in enumerate(pos):
        s += f'<g {d.show(pc(t0 + 1 + (k > 2) * .8))}>' + tile(k, x, y) + _t(x + tw / 2, y + th + 15, names[k], "ts", extra='style="font-size:13px"') + "</g>"
    return s


def three_v():
    """양(엑셀 시트가 넘침) → 속도(시간 축에 기록이 촘촘히) → 다양성(표 · 글 · 사진 · 영상 · 센서). 카드 3.5초 간격 · 12초."""
    d = _D("pbv", 12)
    pc = lambda t: t / 12 * 100  # noqa: E731
    draw = [_v_volume, _v_velocity, _v_variety]
    s = ""
    for i, (ko, en, mean, ex) in enumerate(V3):
        x0, t0 = i * 395, .5 + i * 3.5
        cx = x0 + 182
        s += (f'<g {d.show(pc(t0))}><rect x="{x0}" y="0" width="365" height="372" rx="18" fill="{W}" stroke="#D9DDE3" stroke-width="2"/>'
              + _t(x0 + 24, 38, ko, "tt", "start", 'style="font-size:28px"') + _t(x0 + 24 + len(ko) * 28 + 10, 40, en, "ts", "start", 'style="font-size:16px"')
              + _t(x0 + 24, 76, mean, "tn", "start", 'style="font-size:17px"') + _t(x0 + 24, 344, ex, "ts", "start", 'style="font-size:15px"') + "</g>")
        s += draw[i](d, pc, cx, t0)
    return d.svg(1160, 376, s)


# ── 하루 간편결제 건수 · 한국은행 ─────────────────────────────────────
# 한국은행 보도자료 「2026년 상반기중 전자지급서비스 이용현황」(2026-09-18) 부록 「간편지급 서비스 이용 현황」 표
# (일평균 · 만 건 · 이용건수 합계 행) · 원문 PDF 에서 직접 확인
PAY = {"src": ("한국은행 · 2026년 상반기중 전자지급서비스 이용현황 (2026.9)",
               "https://www.bok.or.kr/portal/bbs/B0000502/view.do?nttId=11064870&menuNo=201265"),
       "count": [("24년 상", 2973.5), ("24년 하", 3177.8), ("25년 상", 3388.1), ("25년 하", 3758.3), ("26년 상", 3822.1)]}
EXCEL_ROWS = 1_048_576   # 엑셀 한 시트 최대 행 수 — Microsoft 「Excel specifications and limits」 1,048,576 rows by 16,384 columns
EXCEL_SRC = ("Microsoft · Excel 사양 및 제한", "https://support.microsoft.com/en-us/office/excel-specifications-and-limits-1672b34d-7043-467e-8e27-269d656771c3")


def payments():
    """반기별 간편결제 하루 평균 건수 막대가 자람 → 마지막 막대 강조 · 1년 전 대비 → 1초 · 엑셀 시트로 환산. 12초."""
    d = _D("pbp", 12)
    pc = lambda t: t / 12 * 100  # noqa: E731
    cnt = PAY["count"]
    mx = max(v for _, v in cnt)
    base, top, bw, gap, x0 = 340, 250, 84, 44, 60
    grow = "transform-box:fill-box;transform-origin:50% 100%"
    s = (_t(40, 20, "간편결제 · 하루 평균 건수", "tn", "start", 'style="font-size:16px"')
         + f'<line x1="40" y1="{base}" x2="{x0 + len(cnt) * (bw + gap)}" y2="{base}" stroke="{N}" stroke-width="2"/>')
    st = [(0, "transform:scaleY(0)"), (pc(.5), "transform:scaleY(0)"), (pc(2), "transform:scaleY(1)"), (100, "transform:scaleY(1)")]
    for i, (lab, v) in enumerate(cnt):
        x, h = x0 + i * (bw + gap), top * v / mx
        last = i == len(cnt) - 1
        s += f'<rect x="{x}" y="{base - h:.1f}" width="{bw}" height="{h:.1f}" rx="5" fill="{K}" {d.a(st, "ease-out", grow)}/>'
        if last:
            s += f'<rect x="{x}" y="{base - h:.1f}" width="{bw}" height="{h:.1f}" rx="5" fill="{O}" {d.show(pc(4))}/>'
        s += (f'<g {d.show(pc(2))}>' + _t(x + bw / 2, base - h - 16, f"{v:,.0f}만", "tn", extra='style="font-size:15px"')
              + _t(x + bw / 2, base + 22, lab, "ts", extra='style="font-size:15px"') + "</g>")
    (pl, pv), (ll, lv) = cnt[-3], cnt[-1]                               # 1년 전 같은 반기와 비교
    s += (f'<g {d.show(pc(4))}><rect x="720" y="50" width="420" height="140" rx="16" fill="#FFF8F0" stroke="{O}" stroke-width="2.5"/>'
          + _t(930, 82, f"20{ll[:2]}년 상반기 · 하루 평균", "ts", extra='style="font-size:15px"')
          + _t(930, 122, f"{lv:,.0f}만 건", "tt", extra=f'style="font-size:30px;fill:{O}"')
          + _t(930, 162, f"1년 전보다 {(lv / pv - 1) * 100:.1f}% 증가", "tn", extra='style="font-size:16px"') + "</g>")
    n = lv * 1e4                                                        # 만 건 → 건
    s += (f'<g {d.show(pc(7))}><rect x="720" y="210" width="420" height="130" rx="16" fill="{W}" stroke="{K}" stroke-width="2.5"/>'
          + _t(930, 248, f"1초에 약 {n / 86400:,.0f}건", "tt", extra='style="font-size:26px"')
          + _t(930, 288, f"하루치 엑셀 시트 {math.ceil(n / EXCEL_ROWS)}장 분량", "tn", extra='style="font-size:18px"')
          + _t(930, 318, f"시트 한 장 최대 {EXCEL_ROWS:,}행", "ts", extra='style="font-size:14px"') + "</g>")
    return d.svg(1160, 400, s)

# ── 프로그래밍 언어의 발전 · 같은 계산(1부터 100까지 합) ──────────────
LANGS = [  # (시기, 이름, 예, 특징, 요리 비유)
    ("1940년대 말 ~", "어셈블리", "mov  x1, #0\nadd  x1, x1, x2\n… 38줄", "CPU 명령 하나씩", "재료 손질부터 직접"),
    ("1957 FORTRAN · 1991 Python", "고급 언어", "for n in range(1, 101):\n    total += n", "영어 단어 · 수식", "밀키트"),
    ("2025 ~", "자연어", "「1부터 100까지 더해\n화면에 보여 줘」", "우리말 요청 → AI 가 코드 작성", "식당에서 주문"),
]


def langs():
    """어셈블리 → 고급 언어 → 자연어 — 칸이 2초 간격으로 나타남."""
    c = ""
    for i, (when, name, ex, feat, cook) in enumerate(LANGS):
        c += (f'<div class="pbgL" style="--d:{.3 + i * 2:.1f}s"><div class="y">{when}</div><b>{name}</b>'
              f'<pre class="{"nl" if i == 2 else ""}">{esc(ex)}</pre><div class="f">{feat}</div>'
              f'<div class="k"><span>요리</span>{cook}</div></div>')
        if i < 2:
            c += f'<i class="pbgA" style="--d:{1.3 + i * 2:.1f}s">→</i>'
    return (f'<div class="pbgLs">{c}</div>'
            '<div class="pbgLine" style="--d:5.5s"><span>기계에 가까운 말</span><b></b><span>사람에 가까운 말</span></div>')


# ── AI 코딩 도구의 변화 · 사람이 하는 일이 줄어듦 (막대는 모양만 · 측정값 아님) ──
ERAS = [  # (해, 이름, 도구, 사람 비중 %, AI 가 하는 일, 사람이 하는 일, AI 가 파악하는 것)
    ("2021", "자동완성", "GitHub Copilot", 85, "다음 줄 · 함수 제안", "위치 · 구조 결정 · 작성 · 실행", "앞뒤 코드"),
    ("2022", "대화형", "ChatGPT", 55, "요청한 코드 작성", "붙일 위치 찾기 · 붙여 넣기 · 실행", "요청 문장"),
    ("2025", "위임형", "Claude Code", 15, "파일 찾기 · 수정 · 실행 · 확인", "목표 · 결과 판단", "목표"),
]


def eras():
    c = ""
    for i, (y, name, tool, h, ai, me, grasp) in enumerate(ERAS):
        c += (f'<div class="pbgE" style="--d:{.3 + i * 2:.1f}s; margin-top:{(2 - i) * 34}px">'
              f'<div class="y">{y}</div><b>{name}</b><span class="t">{tool}</span>'
              f'<div class="bar"><i class="me" style="width:{h}%"></i><i class="ai" style="width:{100 - h}%"></i></div>'
              f'<div class="r"><em class="me">사람</em><small>{me}</small></div>'
              f'<div class="r"><em class="ai">AI</em><small>{ai}</small></div>'
              f'<div class="g">AI 가 파악 · <b>{grasp}</b></div></div>')
    return f'<div class="pbgEs">{c}</div>'


# ── 데이터 분석의 흐름 · AI 이전 → AI 에이전트 (사과 예) ─────────────────
FLOW = [("질문", "가장자리 사과는\n왜 불량이 많나"), ("읽기", "열 · 행 · 단위"), ("정제", "빈칸 · 중복 · 단위"),
        ("집계", "위치별 상품률"), ("시각화", "과수원 지도 · 막대"), ("해석", "원인 후보 · 근거"), ("결정", "선별 기준 · 관리")]


def analysis_flow():
    """일곱 단계가 2초 간격으로 → 「AI 이전 · 분석가가 코드」 띠 → 「Claude Code 가 코드 작성 · 실행」 띠로 바뀜 → 사람이 맡는 단계. 22초."""
    d = _D("pbf", 22)
    pc = lambda s: s / 22 * 100  # noqa: E731
    s = f'<g {d.show(1)}>' + _t(8, 26, "사과 예", "to", "start", 'style="font-size:15px"') + "</g>"
    X = [8 + i * 164 for i in range(len(FLOW))]
    for i, (h, ex) in enumerate(FLOW):
        x, t = X[i], pc(.5 + i * 2)
        s += (f'<g {d.show(t)}><rect x="{x}" y="50" width="146" height="62" rx="14" fill="{"#FFF3E6" if i == 0 else W}" '
              f'stroke="{O if i == 0 else K}" stroke-width="2.5"/>' + _t(x + 73, 82, h, "tt") + "</g>")
        if i:
            s += f'<g {d.show(t)}><path d="M{x - 16} 81 H{x - 3}" stroke="#D9DDE3" stroke-width="3" marker-end="url(#{d.id("k")})"/></g>'
        lines = ex.split("\n")
        y0 = 152 - (len(lines) - 1) * 10
        s += (f'<g {d.show(t)}><rect x="{x}" y="126" width="146" height="54" rx="10" fill="#F4F6F9"/>'
              + "".join(_t(x + 73, y0 + j * 20, ln, "tn", extra='style="font-size:14px"') for j, ln in enumerate(lines)) + "</g>")
    xa, xb = X[1], X[4] + 146          # 읽기 ~ 시각화
    # AI 이전 · 분석가가 코드로 (14.5초에 나타나 18.5초에 사라짐)
    s += (f'<g {d.show(pc(14.5), pc(18.5))}><rect x="{xa}" y="200" width="{xb - xa}" height="50" rx="12" fill="#EEF1F5" stroke="#9AA5B1" stroke-width="2"/>'
          + _t((xa + xb) / 2, 225, "AI 이전 · 분석가가 SQL · 파이썬 코드를 직접 작성", "tn", extra='style="font-size:16px"') + "</g>")
    # AI 에이전트 · Claude Code (18.5초)
    s += (f'<g {d.show(pc(18.5))}><rect x="{xa}" y="200" width="{xb - xa}" height="50" rx="12" fill="#FFF3E6" stroke="{O}" stroke-width="2.5"/>'
          + _t((xa + xb) / 2, 225, "Claude Code · 코드 작성 · 실행 · 결과 보고", "to", extra='style="font-size:17px"') + "</g>")
    # 사람이 맡는 단계 (20초)
    for x0, x1, lab in [(X[0], X[0] + 146, "사람 · 질문"), (X[5], X[6] + 146, "사람 · 판단 · 결정")]:
        s += (f'<g {d.show(pc(20))}><rect x="{x0}" y="200" width="{x1 - x0}" height="50" rx="12" fill="{N}"/>'
              + _t((x0 + x1) / 2, 225, lab, "tw", extra='style="font-size:16px"') + "</g>")
    return d.svg(1160, 262, s)


# ── 분석 결과물의 변화 · 보고서 → 대시보드 → 시뮬레이터 ─────────────────
def results_change():
    """세 카드가 2초 간격 · 시뮬레이터 카드에서 조절 바가 움직이면 숫자가 바뀜(당도 하한 11 → 10)."""
    base, moved = sk.d_rate(sk.D07)[1], sk.d_rate(sk.D07, sugar=10.0)[1]
    rep = ('<div class="pbgM rep"><i class="h"></i><i></i><i></i><i class="s"></i>'
           '<div class="tb"><span></span><span></span><span></span><span></span><span></span><span></span></div><i></i><i class="s"></i></div>')
    rs = sorted(sk.DN["reason"].values(), reverse=True)
    bars = "".join(f'<i style="height:{v / rs[0] * 85:.0f}%"></i>' for v in rs)
    dash = (f'<div class="pbgM dash"><div class="kp"><span>{sk.DN["rows"]}</span><span>{sk.DN["pass"]}</span><span>{sk.DN["rate"]:.0f}%</span></div>'
            f'<div class="bars">{bars}</div></div>')
    sim = (f'<div class="pbgM sim"><div class="num"><span class="a">{base:.2f}%</span><span class="b">{moved:.2f}%</span></div>'
           '<div class="lb">당도 하한</div><div class="sl"><i></i><b></b></div></div>')
    cards = [("보고서", rep, [("형태", "정해진 숫자 · 표 · 그림"), ("갱신", "다시 쓸 때만"), ("읽는 사람", "읽기")]),
             ("대시보드", dash, [("형태", "정해진 화면 · 차트"), ("갱신", "매일 · 자동"), ("읽는 사람", "보기 · 고르기")]),
             ("시뮬레이터", sim, [("형태", "기준을 바꾸는 화면"), ("갱신", "조절 바를 움직일 때마다"), ("읽는 사람", "직접 실험")])]
    c = ""
    for i, (h, mock, rows) in enumerate(cards):
        r = "".join(f'<div class="rw"><span>{a}</span><b>{b}</b></div>' for a, b in rows)
        c += f'<div class="pbgR{" on" if i == 2 else ""}" style="--d:{.3 + i * 2:.1f}s"><b class="h">{h}</b>{mock}{r}</div>'
        if i < 2:
            c += f'<i class="pbgA" style="--d:{1.3 + i * 2:.1f}s">→</i>'
    return f'<div class="pbgRs">{c}</div>'


# ── 파일 이름 버전 관리 · Git 이전 ─────────────────────────────────
FILES = [("simulator.html", "11월 3일"), ("simulator_v2.html", "11월 5일"), ("simulator_최종.html", "11월 8일"),
         ("simulator_최종_수정.html", "11월 9일"), ("simulator_진짜최종.html", "11월 10일")]


def versions():
    """폴더 창에 사본이 2초 간격으로 늘어남 → 생기는 문제 세 가지가 2초 간격."""
    rows = "".join(f'<div class="pbgF" style="--d:{.3 + i * 2:.1f}s"><i>H</i><b>{n}</b><small>{d}</small></div>'
                   for i, (n, d) in enumerate(FILES))
    d0 = .3 + len(FILES) * 2
    probs = "".join(f'<div class="pbgP" style="--d:{d0 + i * 2:.1f}s"><b>{h}</b><span>{t}</span></div>' for i, (h, t) in enumerate([
        ("어느 게 최신", "날짜 · 파일을 열어 봐야 앎"), ("무엇이 바뀌었나", "두 파일을 나란히 놓고 비교"),
        ("이전 상태 복구", "사본을 지웠으면 불가")]))
    return (f'<div class="pbgFw"><div class="pbgFd"><div class="hd">sim-lab › output</div>{rows}</div>'
            f'<div class="pbgPs">{probs}</div></div>')


# ── 프롬프트 · 컨텍스트 · 하네스 · AI 를 쓰는 방법의 변화 ─────────────────
ENG = [("프롬프트", "요청 문장 한 번", "「수율 화면 만들어 줘」를 다듬기", "이번 답 한 번"),
       ("컨텍스트", "보여 줄 자료 고르기", "기준표 · CSV · 화면 캡처를 함께", "이번 대화"),
       ("하네스", "일하는 환경 전체", "CLAUDE.md · Plan Mode · Git · 검증 · Skill · Hook", "폴더에 남아 매번")]


def prompt_to_harness():
    c = ""
    for i, (h, what, ex, keep) in enumerate(ENG):
        rows = "".join(f'<div class="rw"><span>{a}</span><b>{b}</b></div>' for a, b in [("손대는 곳", what), ("이 과정 예", ex), ("남는 범위", keep)])
        c += f'<div class="pbgR{" on" if i == 2 else ""}" style="--d:{.3 + i * 2:.1f}s"><b class="h">{h}</b>{rows}</div>'
        if i < 2:
            c += f'<i class="pbgA" style="--d:{1.3 + i * 2:.1f}s">→</i>'
    return f'<div class="pbgRs">{c}</div>'


# ── 마구와 하네스 · 사진 두 장 → 대응 세 줄 ─────────────────────────
def harness_photo():
    pics = "".join(f'<figure class="pbgPh" style="--d:{.3 + i * 2:.1f}s"><img src="img/{f}" alt="{t}"/><b>{t}</b><span>{x}</span></figure>'
                   for i, (f, t, x) in enumerate([("horse_wild.webp", "마구 없는 말", "힘은 세지만 갈 곳 · 멈출 때를 모름"),
                                                  ("horse_harness.webp", "마구를 찬 말", "같은 힘이 수레를 끌고 마부가 방향을 잡음")]))
    rows = "".join(f'<div class="pbgHm" style="--d:{4.5 + i * 2:.1f}s"><b>{a}</b><i>→</i><span>{b}</span><small>{c}</small></div>'
                   for i, (a, b, c) in enumerate([("말", "모델 · Claude", "힘 · 지능"), ("마구", "하네스", "모델을 감싼 규칙 · 도구 · 절차 · 확인"),
                                                  ("마부", "사람", "방향 · 최종 판단")]))
    return f'<div class="pbgHs">{pics}</div><div class="pbgHr">{rows}</div>'


# ── 과수원과 사과 데이터 · 위치 열(안쪽 · 중간 · 가장자리)의 뜻 ─────────────
ZCOL = {"안쪽": "#2F6DB5", "중간": "#2BA38F", "가장자리": "#E07A12"}


def orchard_zones():
    """과수원 30 × 20 칸(나무 한 그루 = 사과 한 개) → 가장자리 · 중간 · 안쪽이 2초 간격으로 칠해짐 → 엑셀 한 행 ↔ 지도 한 칸. 14초 · 한 번.
    줄 수 · 그루 수는 데이터에서 계산 (바깥에서 몇 번째 줄인지)."""
    df = sk.D07
    d = _D("pbo", 14)
    pc = lambda t: t / 14 * 100  # noqa: E731
    nx, ny = int(df["가로칸"].max()), int(df["세로칸"].max())
    ring = df.apply(lambda r: min(r["가로칸"] - 1, nx - r["가로칸"], r["세로칸"] - 1, ny - r["세로칸"]) + 1, axis=1)
    C, X0, Y0 = 15, 20, 52
    cx = lambda x: X0 + (x - 1) * C  # noqa: E731
    cy = lambda y: Y0 + (ny - y) * C  # noqa: E731
    s = f'<g {d.show(0)}>' + _t(X0, 26, f"과수원 · 나무 {nx} × {ny} 그루 · 칸 하나 = 사과 하나", "tn", "start", 'style="font-size:16px"') + "</g>"
    s += f'<g {d.show(0)}>' + "".join(f'<rect x="{cx(r["가로칸"])}" y="{cy(r["세로칸"])}" width="{C - 2}" height="{C - 2}" rx="2" fill="#E1E5EB"/>'
                                    for _, r in df.iterrows()) + "</g>"
    cards = ""
    for k, (z, t) in enumerate([("가장자리", 2), ("중간", 4), ("안쪽", 6)]):
        m = df["위치"] == z
        lo, hi = int(ring[m].min()), int(ring[m].max())
        where = f"바깥에서 {lo}~{hi}번째 줄" if k < 2 else f"바깥에서 {lo}번째 줄부터"
        s += f'<g {d.show(pc(t))}>' + "".join(
            f'<rect x="{cx(r["가로칸"])}" y="{cy(r["세로칸"])}" width="{C - 2}" height="{C - 2}" rx="2" fill="{ZCOL[z]}" fill-opacity=".85"/>'
            for _, r in df[m].iterrows()) + "</g>"
        y = 60 + k * 74
        cards += (f'<g {d.show(pc(t))}><rect x="520" y="{y}" width="300" height="62" rx="12" fill="{W}" stroke="{ZCOL[z]}" stroke-width="2.5"/>'
                  f'<rect x="520" y="{y}" width="8" height="62" rx="3" fill="{ZCOL[z]}"/>'
                  + _t(544, y + 22, z, "tt", "start", f'style="fill:{ZCOL[z]}"') + _t(544, y + 46, f"{where} · {int(m.sum())}그루", "ts", "start")
                  + "</g>")
    s += cards
    # 엑셀 한 행 ↔ 지도 한 칸 (8초)
    r0 = df.iloc[0]
    hx, hy = cx(r0["가로칸"]), cy(r0["세로칸"])
    cols = ["사과번호", "가로칸", "세로칸", "위치", "무게", "당도", "등급"]
    ws = [96, 62, 62, 82, 60, 60, 60]
    tx, ty = 520, 322
    head = body = ""
    x = tx
    for c, w in zip(cols, ws):
        hl = c in ("가로칸", "세로칸", "위치")
        head += f'<rect x="{x}" y="{ty}" width="{w}" height="30" fill="#E8F0E9" stroke="#DADCE0"/>' + _t(x + w / 2, ty + 15, c, "tn", extra='style="font-size:13px"')
        body += (f'<rect x="{x}" y="{ty + 30}" width="{w}" height="34" fill="{"#FFF3E6" if hl else W}" stroke="#DADCE0"/>'
                 + _t(x + w / 2, ty + 47, r0[c], "tn", extra=f'style="font-size:14px{";fill:#C25E00" if hl else ""}"'))
        x += w
    s += (f'<g {d.show(pc(8.5))}><rect x="{tx}" y="{ty - 26}" width="{x - tx}" height="22" fill="#1D6F42"/>'
          + _t(tx + 8, ty - 15, "apple_A07.xlsx · 한 행", "tw", "start", 'style="font-size:12px"') + head + body + "</g>")
    s += (f'<g {d.show(pc(8.5))}><rect x="{hx - 3}" y="{hy - 3}" width="{C + 4}" height="{C + 4}" rx="4" fill="none" stroke="{N}" stroke-width="3"/>'
          f'<path d="M{hx + C + 2} {hy + 2} C 300 {hy + 40}, 420 {ty + 80}, {tx - 6} {ty + 47}" fill="none" stroke="{N}" stroke-width="2" stroke-dasharray="5 4" marker-end="url(#{d.id("k")})"/></g>')
    s += f'<g {d.show(pc(10.5))}>' + _t(tx, ty + 92, "엑셀 한 행 = 사과 한 개 = 지도 한 칸(나무 한 그루)", "to", "start", 'style="font-size:16px"') + "</g>"
    return d.svg(1160, 430, s)


# ── 데이터 종류와 차트 · 실제 사과 데이터로 그린 작은 그림 세 장 ─────────────
def chart_types():
    """숫자 열 → 분포 · 글자 열 → 막대 · 위치 열 → 지도. 카드 셋이 2초 간격."""
    df = sk.D07
    w = df["무게"]
    cnt = [int(((w >= lo) & (w < lo + 10)).sum()) for lo in range(200, 380, 10)]
    hist = '<div class="pbgTh">' + "".join(f'<i style="height:{c / max(cnt) * 100:.0f}%"></i>' for c in cnt) + "</div>"
    zr = sk.DN["area"]
    bars = '<div class="pbgTb">' + "".join(
        f'<div><span>{z}</span><b style="width:{zr[z]:.0f}%;background:{ZCOL[z]}"></b><em>{zr[z]:.2f}%</em></div>' for z in sk.AREA) + "</div>"
    nx = int(df["가로칸"].max())
    cells = sorted(((int(r["세로칸"]), int(r["가로칸"]), r["등급"]) for _, r in df.iterrows()), key=lambda t: (-t[0], t[1]))
    grid = (f'<div class="pbgTg" style="grid-template-columns:repeat({nx},1fr)">'
            + "".join(f'<i style="background:{"#2BA84A" if g == "상품" else "#E8344E"}"></i>' for *_, g in cells) + "</div>")
    cards = [("숫자 열", "무게 · 당도 · 지름", hist, "분포 · 평균 · 퍼짐"),
             ("글자 열", "위치 · 품종 · 등급", bars, "막대 · 개수 · 비율"),
             ("위치 열", "가로칸 · 세로칸", grid, "지도 · 몰린 곳")]
    c = "".join(f'<div class="pbgTc" style="--d:{.3 + i * 2:.1f}s"><b>{h}</b><span>{cols}</span><div class="m">{mock}</div>'
                f'<div class="u"><i>→</i>{use}</div></div>' for i, (h, cols, mock, use) in enumerate(cards))
    return f'<div class="pbgTs">{c}</div>'


CSS = """
  @keyframes pbgIn{from{opacity:0; transform:translateY(10px)} to{opacity:1; transform:none}}
  .pbgA{font-style:normal; align-self:center; text-align:center; font-size:28px; font-weight:800; color:#F28C28; opacity:0; animation:pbgIn .5s var(--d) forwards;}
  /* 언어 */
  .pbgLs{display:grid; grid-template-columns:minmax(0,1fr) 36px minmax(0,1fr) 36px minmax(0,1fr); align-items:stretch; margin-top:4px;}
  .pbgL{border:2px solid #D9DDE3; border-radius:16px; background:#fff; padding:16px 18px; display:flex; flex-direction:column; opacity:0; animation:pbgIn .6s var(--d) forwards;}
  .pbgL:last-of-type{border-color:#F28C28; background:#FFF8F0;}
  .pbgL .y{font-family:var(--mono); font-size:13.5px; font-weight:800; color:#F28C28;}
  .pbgL b{font-size:23px; color:#16233A; margin:2px 0 10px;}
  .pbgL pre{margin:0; overflow:hidden; background:#1E2433; color:#E6EDF7; border-radius:10px; padding:12px 14px; font-family:var(--mono); font-size:16px; white-space:pre; min-height:62px; font-variant-ligatures:none;}
  .pbgL pre.nl{background:#fff; color:#16233A; border:1.5px solid #F7C99A; font-family:inherit; font-weight:700; white-space:pre-wrap;}
  .pbgL .f{font-size:15.5px; color:#3A4657; margin:10px 0 8px;}
  .pbgL .k{margin-top:auto; padding:8px 12px; border-radius:10px; background:#F4F6F9; font-size:15.5px; color:#16233A; font-weight:700;}
  .pbgL .k span{font-size:12.5px; font-weight:800; color:#E07A12; margin-right:8px;}
  .pbgLine{display:flex; align-items:center; gap:12px; margin-top:16px; font-size:14px; font-weight:800; color:#6B7785; opacity:0; animation:pbgIn .5s var(--d) forwards;}
  .pbgLine b{flex:1; height:4px; border-radius:2px; background:linear-gradient(90deg,#1F3A5F,#F28C28);}
  /* AI 코딩 도구 */
  .pbgEs{display:grid; grid-template-columns:repeat(3,1fr); gap:20px; align-items:start; margin-top:4px;}
  .pbgE{border:2px solid #D9DDE3; border-radius:16px; background:#fff; padding:18px 20px; opacity:0; animation:pbgIn .6s var(--d) forwards;}
  .pbgE:last-child{border-color:#F28C28; background:#FFF8F0;}
  .pbgE .y{font-family:var(--mono); font-size:15px; font-weight:800; color:#F28C28;}
  .pbgE > b{display:block; font-size:24px; color:#16233A; margin-top:2px;} .pbgE .t{font-size:15px; color:#6B7785;}
  .pbgE .bar{display:flex; height:14px; border-radius:7px; overflow:hidden; margin:14px 0 10px;}
  .pbgE .bar .me{background:#1F3A5F;} .pbgE .bar .ai{background:#F28C28;}
  .pbgE .r{display:flex; gap:10px; align-items:baseline; margin-top:6px;}
  .pbgE em{font-style:normal; font-size:13px; font-weight:800; min-width:30px;} .pbgE em.me{color:#1F3A5F;} .pbgE em.ai{color:#E07A12;}
  .pbgE small{font-size:15px; color:#3A4657; line-height:1.4;}
  .pbgE .g{margin-top:12px; padding-top:10px; border-top:1px dashed #D9DDE3; font-size:15px; color:#6B7785;} .pbgE .g b{font-size:17px; color:#E07A12;}
  /* 분석 결과물 */
  .pbgRs{display:grid; grid-template-columns:minmax(0,1fr) 36px minmax(0,1fr) 36px minmax(0,1fr); align-items:stretch; margin-top:4px;}
  .pbgR{border:2px solid #D9DDE3; border-radius:16px; background:#fff; padding:16px 18px; display:flex; flex-direction:column; gap:8px; opacity:0; animation:pbgIn .6s var(--d) forwards;}
  .pbgR.on{border-color:#F28C28; background:#FFF8F0;}
  .pbgR .h{font-size:23px; color:#16233A;}
  .pbgR .rw{display:grid; grid-template-columns:78px 1fr; gap:8px; align-items:baseline; font-size:15.5px;}
  .pbgR .rw span{font-size:13px; font-weight:800; color:#6B7785;} .pbgR .rw b{color:#16233A; font-weight:700; word-break:keep-all;}
  .pbgR.on .rw b{color:#C25E00;}
  .pbgM{height:150px; border:1.5px solid #D9DDE3; border-radius:12px; background:#fff; padding:14px 16px; margin-bottom:6px; display:flex; flex-direction:column; gap:8px;}
  .pbgM.rep i{display:block; height:8px; border-radius:4px; background:#E1E5EB;} .pbgM.rep i.h{height:12px; width:55%; background:#1F3A5F;}
  .pbgM.rep i.s{width:70%;}
  .pbgM.rep .tb{display:grid; grid-template-columns:repeat(3,1fr); gap:4px;} .pbgM.rep .tb span{height:14px; background:#F4F6F9; border:1px solid #E1E5EB;}
  .pbgM.dash .kp{display:grid; grid-template-columns:repeat(3,1fr); gap:6px;}
  .pbgM.dash .kp span{border:1px solid #E1E5EB; border-radius:6px; text-align:center; font-weight:800; font-size:15px; color:#1F3A5F; padding:4px 0;}
  .pbgM.dash .bars{flex:1; display:flex; align-items:flex-end; gap:12px; padding:0 8px; border-bottom:2px solid #9AA5B1;}
  .pbgM.dash .bars i{flex:1; background:#E8344E; border-radius:4px 4px 0 0;}
  .pbgM.sim .num{position:relative; height:44px;}
  .pbgM.sim .num span{position:absolute; left:0; top:0; font-size:34px; font-weight:800; color:#E07A12; font-variant-numeric:tabular-nums;}
  .pbgM.sim .num .b{opacity:0; animation:pbgShow .4s 7.5s forwards;} .pbgM.sim .num .a{animation:pbgHide .4s 7.5s forwards;}
  .pbgM.sim .lb{font-size:13px; font-weight:800; color:#6B7785;}
  .pbgM.sim .sl{position:relative; height:24px;}
  .pbgM.sim .sl i{position:absolute; left:0; right:0; top:9px; height:6px; border-radius:3px; background:#D9DDE3;}
  .pbgM.sim .sl b{position:absolute; top:0; left:50%; width:24px; height:24px; margin-left:-12px; border-radius:50%; background:#F28C28; border:3px solid #fff; box-shadow:0 1px 4px rgba(0,0,0,.25); animation:pbgSlide 1.2s 6.3s ease-in-out forwards;}
  @keyframes pbgSlide{to{left:32%}}
  @keyframes pbgShow{to{opacity:1}} @keyframes pbgHide{to{opacity:0}}
  /* 파일 이름 버전 */
  .pbgFw{display:grid; grid-template-columns:1.25fr 1fr; gap:30px; align-items:center; margin-top:14px;}
  .pbgFd{border:1.5px solid #D9DDE3; border-radius:14px; background:#fff; overflow:hidden;}
  .pbgFd .hd{background:#F2F4F7; padding:10px 18px; font-size:15px; font-weight:800; color:#6B7785; border-bottom:1.5px solid #D9DDE3;}
  .pbgF{display:grid; grid-template-columns:34px 1fr auto; gap:12px; align-items:center; padding:11px 18px; border-bottom:1px solid #EEF0F3; opacity:0; animation:pbgIn .45s var(--d) forwards;}
  .pbgF:last-child{border-bottom:none; background:#FFF8F0;}
  .pbgF i{display:inline-flex; width:30px; height:36px; border-radius:4px; background:#E44D26; color:#fff; font-style:normal; font-weight:900; font-size:14px; align-items:center; justify-content:center;}
  .pbgF b{font-size:19px; color:#16233A; font-weight:700;} .pbgF small{font-size:14px; color:#6B7785;}
  .pbgPs{display:flex; flex-direction:column; gap:14px;}
  .pbgP{border-left:5px solid #F28C28; background:#FFF1E2; border-radius:10px; padding:14px 18px; opacity:0; animation:pbgIn .45s var(--d) forwards;}
  .pbgP b{display:block; font-size:21px; color:#16233A; margin-bottom:4px;} .pbgP span{font-size:16px; color:#4A5563;}
  /* 마구와 하네스 */
  .pbgHs{display:grid; grid-template-columns:1fr 1fr; gap:20px;}
  .pbgPh{margin:0; border:1.5px solid #D9DDE3; border-radius:14px; overflow:hidden; background:#fff; opacity:0; animation:pbgIn .6s var(--d) forwards;}
  .pbgPh img{display:block; width:100%; height:200px; object-fit:cover;}
  .pbgPh b{display:block; padding:10px 16px 0; font-size:19px; color:#16233A;} .pbgPh span{display:block; padding:2px 16px 12px; font-size:15px; color:#6B7785;}
  .pbgHr{display:grid; grid-template-columns:repeat(3,1fr); gap:14px; margin-top:16px;}
  .pbgHm{display:grid; grid-template-columns:auto auto 1fr; gap:6px 10px; align-items:baseline; border:1.5px solid #E1E5EB; border-left:5px solid #F28C28; border-radius:10px; background:#fff; padding:10px 14px; opacity:0; animation:pbgIn .45s var(--d) forwards;}
  .pbgHm b{font-size:19px; color:#16233A;} .pbgHm i{font-style:normal; color:#F28C28; font-weight:800;} .pbgHm span{font-size:19px; font-weight:800; color:#C25E00;}
  .pbgHm small{grid-column:1 / -1; font-size:14.5px; color:#4A5563;}
  /* 데이터 종류와 차트 */
  .pbgTs{display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:22px; margin-top:6px;}
  .pbgTc{border:2px solid #D9DDE3; border-radius:16px; background:#fff; padding:18px 20px; display:flex; flex-direction:column; gap:6px; opacity:0; animation:pbgIn .6s var(--d) forwards;}
  .pbgTc > b{font-size:24px; color:#16233A;} .pbgTc > span{font-size:15px; color:#6B7785;}
  .pbgTc .m{height:170px; border:1.5px solid #E1E5EB; border-radius:12px; padding:14px; margin:8px 0; display:flex; align-items:center; justify-content:center;}
  .pbgTc .u{font-size:19px; font-weight:800; color:#C25E00;} .pbgTc .u i{font-style:normal; margin-right:8px;}
  .pbgTh{width:100%; height:100%; display:flex; align-items:flex-end; gap:2px; border-bottom:2px solid #9AA5B1;}
  .pbgTh i{flex:1; background:#1F3A5F; opacity:.85; border-radius:2px 2px 0 0;}
  .pbgTb{width:100%; display:flex; flex-direction:column; gap:12px;}
  .pbgTb div{display:grid; grid-template-columns:64px 1fr 62px; gap:8px; align-items:center; font-size:13.5px; font-weight:700; color:#16233A;}
  .pbgTb b{display:block; height:18px; border-radius:4px;} .pbgTb em{font-style:normal; font-size:13px; color:#3A4657; text-align:right;}
  .pbgTg{display:grid; gap:1px; width:213px; height:142px;}
  .pbgTg i{display:block; border-radius:1px;}
  @media print{.pbgA,.pbgL,.pbgLine,.pbgE,.pbgR,.pbgF,.pbgP,.pbgPh,.pbgHm,.pbgTc{animation:none; opacity:1}
    .pbgM.sim .num .a{animation:none; opacity:0} .pbgM.sim .num .b{animation:none; opacity:1} .pbgM.sim .sl b{animation:none; left:32%}}
"""
