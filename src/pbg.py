"""배경 장 그림 — 바이브코딩까지의 변화 · 데이터 분석과 엔지니어링의 변화 · Git 이전의 버전 관리.

언어 발전 · AI 코딩 도구 변화 · 파일 이름 버전 관리는 vibe-coding 강의(1-1 · 1-5)의 구성을 이 과정 예시로 옮긴 것.
장면 간격 2초 이상 · 한 번 재생 후 마지막 장면에 멈춤. CSS 접두어 pbg.
"""
from anim import K, N, O, W, _D, _t
from hx import esc
import sk

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
  @media print{.pbgA,.pbgL,.pbgLine,.pbgE,.pbgR,.pbgF,.pbgP,.pbgPh,.pbgHm{animation:none; opacity:1}
    .pbgM.sim .num .a{animation:none; opacity:0} .pbgM.sim .num .b{animation:none; opacity:1} .pbgM.sim .sl b{animation:none; left:32%}}
"""
