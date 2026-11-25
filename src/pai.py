"""Ⅱ 추가 장 — AI 활용 방식의 변화(프롬프트 → 컨텍스트 → 에이전틱 AI → 하네스 엔지니어링 · METR 작업 길이) ·
컨텍스트 관리가 필요한 이유 · .claude 폴더(참고하는 것 · 폴더 구조 · 위치 · Sub Agent) · 부록 플러그인 마켓플레이스.

posco-dx · vibe-coding 3부 장을 이 과정 예시(사과 · 웨이퍼 · sim-lab)로 옮긴 것. 숫자는 sk(사과 · 웨이퍼) · METR 원문에서.
접두어 pq (CSS · 애니메이션). build.py 의 VIBE · APPENDIX 가 제목으로 골라 쓴다.
"""
import hx
import sk
import viz2
from anim import BG, K, N, O, OK, R, S, W, _D, _t
from deck import flow, light
from hx import code, esc, two
from stats_hx import src

T = "바이브코딩"
DN = sk.DN
FL = "#8FA3BF"

# ── 출처 (원문에서 확인 · 2026) ───────────────────────────
METR_11 = ("METR · Time Horizon 1.1 (2026.1)", "https://metr.org/blog/2026-1-29-time-horizon-1-1")
METR_TH = ("METR · Time Horizons (2026.9)", "https://metr.org/time-horizons/")
OAI_FC = ("OpenAI · Function calling (2023.6)", "https://openai.com/index/function-calling-and-other-api-updates/")
ANT_MCP = ("Anthropic · MCP (2024.11)", "https://www.anthropic.com/news/model-context-protocol")
OAI_HE = ("OpenAI · Harness engineering (2026.2)", "https://openai.com/index/harness-engineering/")
CC_HOW = ("Claude Code 문서 · How Claude Code works", "https://code.claude.com/docs/en/how-claude-code-works")
CC_BP = ("Claude Code 문서 · Best practices", "https://code.claude.com/docs/en/best-practices")
CC_DIR = ("Claude Code 문서 · .claude directory", "https://code.claude.com/docs/en/claude-directory")
CC_SUB = ("Claude Code 문서 · Subagents", "https://code.claude.com/docs/en/sub-agents")
CC_PLUG = ("Claude Code 문서 · Install plugins", "https://code.claude.com/docs/en/plugins/install")
CC_MKT = ("Claude Code 문서 · Anthropic's marketplaces", "https://code.claude.com/docs/en/plugins/anthropic-marketplaces")
GH_SP = ("GitHub · obra/superpowers", "https://github.com/obra/superpowers")
GH_GS = ("GitHub · garrytan/gstack", "https://github.com/garrytan/gstack")

# GitHub 별 수 (2026-11-26 gh api 로 확인)
SP_STARS, GS_STARS = 326441, 142637
# METR Time Horizon 1.1 (time-horizons 페이지 데이터) — Claude Opus 4.6 · 50% · 80% 작업 길이(분)
OPUS46_P50, OPUS46_P80 = 718.8, 69.9


# ── 1. AI 활용 방식의 변화 · 겹겹이 넓어지는 설계 범위 ──────────────
def shift():
    """가운데 모델 → 질문(프롬프트) → 자료(컨텍스트) → 도구 · 반복(에이전틱 AI) → 규칙 · 권한 · 확인(하네스).
    고리가 하나씩 생기고 오른쪽 줄이 함께 나타남. 12초."""
    d = _D("pqs", 12)
    pc = lambda t: t / 12 * 100  # noqa: E731
    cx, cy = 236, 214
    rings = [(200, "#FFF3E6", O, 2.5, "규칙 · 권한 · 확인", 9), (164, "#EEF2F7", K, 1.5, "도구 · 반복", 6.5),
             (124, "#DCE5F0", K, 1.5, "자료", 4), (84, "#C9D6E6", K, 1.5, "질문", 1.5)]
    s = ""
    inner = [164, 124, 84, 44]
    for (r, fill, st, sw, lab, t), r_in in zip(rings, inner):
        s += (f'<g {d.show(pc(t))}><circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{st}" stroke-width="{sw}"/>'
              + _t(cx, cy - (r + r_in) / 2, lab, "tn", extra=f'style="font-size:13.5px;fill:{O if st == O else N}"') + "</g>")
    s += (f'<g {d.show(pc(.3))}><circle cx="{cx}" cy="{cy}" r="44" fill="{N}"/>'
          + _t(cx, cy, "모델", "tw", extra='style="font-size:17px"') + "</g>")
    rows = [("프롬프트 엔지니어링", "질문 한 번을 잘 쓰기", "역할 · 형식을 넣은 질문", 1.5, K),
            ("컨텍스트 엔지니어링", "보여 줄 자료 고르기", "사과 엑셀 · 선별 기준표", 4, K),
            ("에이전틱 AI", "AI 가 도구로 직접 실행 · 반복", "읽기 · 실행 · 저장 · 확인", 6.5, K),
            ("하네스 엔지니어링", "일하는 환경 전체를 설계", "CLAUDE.md · Skill · Hook", 9, O)]
    for i, (name, what, ex, t, c) in enumerate(rows):
        y = 22 + i * 100
        hl = c == O
        s += (f'<g {d.show(pc(t))}><rect x="490" y="{y}" width="660" height="84" rx="14" fill="{"#FFF8F1" if hl else W}" '
              f'stroke="{O if hl else "#C9CFD8"}" stroke-width="{2.5 if hl else 2}"/>'
              f'<circle cx="524" cy="{y + 42}" r="17" fill="{c}"/>' + _t(524, y + 42, i + 1, "tw", extra='style="font-size:16px"')
              + _t(556, y + 28, name, "tt", "start", f'style="font-size:20px;fill:{"#EF6C00" if hl else N}"')
              + _t(556, y + 60, what, "ts", "start", 'style="font-size:15px"')
              + _t(1130, y + 42, ex, "tn", "end", f'style="font-size:14.5px;fill:{"#EF6C00" if hl else K}"') + "</g>")
    return d.svg(1160, 430, s)


# ── 2. 하네스 = 모델을 감싼 나머지 전부 ─────────────────────────
def anatomy():
    """가운데 모델 · 둘레에 하네스 부품이 하나씩 붙고 · 바깥 테두리가 에이전트. 10초.
    참고: Claude Code 「How Claude Code works」(모델을 감싼 층 = agentic harness)."""
    d = _D("pqh", 10)
    s = (f'<g {d.show(78)}><rect x="16" y="8" width="1128" height="414" rx="22" fill="none" stroke="{N}" stroke-width="3" stroke-dasharray="9 7"/>'
         + _t(40, 34, "에이전트 = 모델 + 하네스", "tt", "start", 'style="font-size:21px"') + "</g>")
    s += (f'<g {d.show(12)}><rect x="60" y="56" width="1040" height="346" rx="18" fill="#EEF2F7" stroke="{K}" stroke-width="2.5"/>'
          + _t(1080, 80, "하네스 · 모델을 감싼 나머지 전부", "tn", "end", f'style="fill:{K}"') + "</g>")
    parts = [(110, 110, "내장 도구", "파일 읽기 · 실행 · 저장"), (110, 210, "규칙", "CLAUDE.md"), (110, 310, "절차", "Skill"),
             (820, 110, "컨텍스트 관리", "자동 요약 · /clear"), (820, 210, "통제", "권한 · Hook"), (820, 310, "확인", "정답 숫자 · Sub Agent")]
    for i, (x, y, h, sub) in enumerate(parts):
        t = 22 + i * 8
        ex = x + 230 if x < 500 else x
        s += (f'<g {d.show(t)}><path d="M{ex} {y + 33} L580 230" stroke="#C9CFD8" stroke-width="2" stroke-dasharray="5 5"/>'
              f'<rect x="{x}" y="{y}" width="230" height="66" rx="12" fill="{W}" stroke="{K}" stroke-width="2.2"/>'
              + _t(x + 115, y + 23, h, "tn", extra='style="font-size:17px"') + _t(x + 115, y + 47, sub, "ts", extra='style="font-size:13.5px"') + "</g>")
    s += (f'<g {d.show(2)}><rect x="470" y="180" width="220" height="100" rx="16" fill="#FFF3E6" stroke="{O}" stroke-width="3"/>'
          + _t(580, 218, "모델", "tt", extra='style="font-size:22px"') + _t(580, 250, "판단 · 작성", "ts") + "</g>")
    return d.svg(1160, 430, s)


# ── 3. METR 작업 길이 그래프 + 카드 ──────────────────────────────
def metr():
    chart = hx.metr_chart().replace("</svg>", '<text x="70" y="8" font-size="13" font-weight="700" fill="#5B6573">작업 길이 · 사람이 하면 걸리는 시간</text></svg>')
    cards = [("hl", '89<small>일</small>', "2024년 이후 · 작업 길이가 2배 되는 기간"),
             ("", '약 7<small>개월</small>', "2019년 이후 전체 추세 · 196일"),
             ("", f'{OPUS46_P50 / 60:.0f}<small>시간</small> · {OPUS46_P80:.0f}<small>분</small>', "Claude Opus 4.6 · 절반 성공 · 80% 성공")]
    c = "".join(f'<div class="bn {k}" style="--d:{.4 + i * .3:.2f}s"><div class="bv">{v}</div><div class="bl">{lab}</div></div>' for i, (k, v, lab) in enumerate(cards))
    return f'<div class="mwrap">{chart}<div class="mcards">{c}</div></div>'


# ── 4. 컨텍스트 관리가 필요한 이유 ──────────────────────────────
def ctx_why():
    """사과 요약 → 차트 → 집계 → 웨이퍼 분석 → 고침 두 번 → 자동 요약. 요청마다 처음부터 끝까지 다시 읽음(주황 훑기).
    웨이퍼 요청에서 사과 기록은 관계없는 기록 · 고침 두 번은 실패한 시도 · 자동 요약에서 초반 지시가 빠짐. 16초.
    참고: Claude Code 문서 Best practices(요청마다 대화 전체 전송 · 집중된 컨텍스트 · 실패한 시도 · /clear) · How Claude Code works(요약 때 초반 지시)."""
    d = _D("pqc", 16)
    pc = lambda t: t / 16 * 100  # noqa: E731
    X0, Y, H = 30, 66, 66
    TC, TE = 12.4, 13.2                               # 자동 요약 시작 · 끝
    s = ('<defs><pattern id="pqhatch" width="9" height="9" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
         '<rect width="9" height="9" fill="#fff" fill-opacity=".45"/><line x1="0" y1="0" x2="0" y2="9" stroke="#5B6573" stroke-width="3" stroke-opacity=".55"/></pattern></defs>')
    s += _t(X0, 28, "대화 기록 · 요청할 때마다 처음부터 다시 읽음", "tt", "start", 'style="font-size:18px"')
    s += _t(1130, 28, "창 크기 · 대부분 100만 토큰", "ts", "end", 'style="font-size:14px"')
    s += f'<rect x="{X0}" y="{Y}" width="1100" height="{H}" rx="10" fill="{BG}" stroke="{N}" stroke-width="2.5"/>'
    blocks = [("CLAUDE.md", 86, N, .3, False), ("「원본은 고치지 마」", 150, "#9AA5B1", .9, True), ("사과 요약", 150, FL, 1.8, True),
              ("사과 차트", 150, FL, 3.4, True), ("사과 집계", 150, FL, 5.0, True), ("웨이퍼 분석", 150, O, 6.8, True),
              ("고침 ✕", 95, R, 9.0, True), ("고침 ✕", 95, R, 10.2, True)]
    x, ends = X0, []
    for name, w, col, t, gone in blocks:
        if gone:
            st = [(0, "width:0px"), (pc(t), "width:0px"), (pc(t + .6), f"width:{w}px"), (pc(TC), f"width:{w}px"), (pc(TE), "width:0px"), (100, "width:0px")]
        else:
            st = [(0, "width:0px"), (pc(t), "width:0px"), (pc(t + .6), f"width:{w}px"), (100, f"width:{w}px")]
        s += f'<rect x="{x}" y="{Y}" height="{H}" fill="{col}" stroke="{W}" stroke-width="2" {d.a(st)}/>'
        lab = _t(x + w / 2, Y + H / 2, name, "tw", extra=f'style="font-size:{12.5 if len(name) > 6 else 14.5}px"')
        s += f'<g {d.show(pc(t + .5), pc(TC) if gone else None)}>{lab}</g>'
        x += w
        ends.append(x)
    # 요청마다 처음부터 다시 읽기 — 주황 훑기
    for i in (2, 3, 4, 5, 6, 7):
        t, wd = blocks[i][3], ends[i] - X0
        st = [(0, "width:0px;opacity:0"), (pc(t + .6), "width:0px;opacity:1"), (pc(t + 1.3), f"width:{wd}px;opacity:1"),
              (pc(t + 1.8), f"width:{wd}px;opacity:0"), (100, f"width:{wd}px;opacity:0")]
        s += f'<rect x="{X0}" y="{Y - 6}" height="{H + 12}" rx="8" fill="{O}" fill-opacity=".22" {d.a(st)}/>'
    # 관계없는 기록 — 사과 기록 세 칸
    ax0, ax1 = ends[1], ends[4]
    s += (f'<g {d.show(pc(7.6), pc(TC))}><rect x="{ax0}" y="{Y}" width="{ax1 - ax0}" height="{H}" fill="url(#pqhatch)"/>'
          f'<path d="M{ax0 + 4} {Y + H + 10} V{Y + H + 18} H{ax1 - 4} V{Y + H + 10}" fill="none" stroke="{S}" stroke-width="2"/>'
          + _t((ax0 + ax1) / 2, Y + H + 34, "웨이퍼 작업과 관계없는 기록", "tn", extra=f'style="font-size:14px;fill:{S}"') + "</g>")
    # 실패한 시도
    fx0, fx1 = ends[5], ends[7]
    s += (f'<g {d.show(pc(10.8), pc(TC))}><path d="M{fx0 + 4} {Y + H + 10} V{Y + H + 18} H{fx1 - 4} V{Y + H + 10}" fill="none" stroke="{R}" stroke-width="2"/>'
          + _t((fx0 + fx1) / 2, Y + H + 34, "실패한 시도", "tn", extra=f'style="font-size:14px;fill:{R}"') + "</g>")
    # 자동 요약
    sx, sw = ends[0], 130
    s += f'<g {d.show(pc(TC - .3))}>' + _t(1130, Y + H + 34, "한도 근처 · 자동 요약", "tn", "end", f'style="font-size:14px;fill:{OK}"') + "</g>"
    s += (f'<rect x="{sx}" y="{Y}" height="{H}" fill="{OK}" stroke="{W}" stroke-width="2" '
          + d.a([(0, "width:0px"), (pc(TE), "width:0px"), (pc(TE + .6), f"width:{sw}px"), (100, f"width:{sw}px")]) + "/>")
    s += f'<g {d.show(pc(TE + .5))}>' + _t(sx + sw / 2, Y + H / 2, "요약", "tw", extra='style="font-size:14.5px"') + "</g>"
    s += (f'<g {d.show(pc(TE + .8))}><rect x="{sx + sw + 14}" y="{Y + 16}" width="250" height="34" rx="17" fill="#FDECEA" stroke="{R}" stroke-width="2" stroke-dasharray="6 4"/>'
          + _t(sx + sw + 139, Y + 33, "「원본은 고치지 마」 빠질 수 있음", "tn", extra=f'style="font-size:13.5px;fill:{R}"') + "</g>")
    # 이유 카드 네 장
    cards = [("1", O, "매번 다시 읽음", "요청마다 대화 전체를 보냄", "쓰지 않는 기록에도 비용", 2.6),
             ("2", S, "관계없는 기록", "웨이퍼 작업에 사과 기록 3개", "집중된 기록일수록 좋은 답", 7.8),
             ("3", R, "실패한 시도", "틀린 시도 두 번도 매번 읽음", "세 번째 고침은 기록만 늘림", 11.0),
             ("4", OK, "자동 요약", "요청 · 핵심 코드는 남음", "초반 지시가 빠질 수 있음", 14.0)]
    cw, gap = 262, (1100 - 4 * 262) / 3
    for i, (n, c, h, l1, l2, t) in enumerate(cards):
        x0, y0 = X0 + i * (cw + gap), 196
        s += (f'<g {d.show(pc(t))}><rect x="{x0}" y="{y0}" width="{cw}" height="150" rx="16" fill="{W}" stroke="{c}" stroke-width="2.5"/>'
              f'<circle cx="{x0 + 32}" cy="{y0 + 36}" r="15" fill="{c}"/>' + _t(x0 + 32, y0 + 36, n, "tw", extra='style="font-size:15px"')
              + _t(x0 + 58, y0 + 37, h, "tn", "start", 'style="font-size:18px"')
              + _t(x0 + 22, y0 + 86, l1, "ts", "start", 'style="font-size:14.5px"') + _t(x0 + 22, y0 + 118, l2, "ts", "start", 'style="font-size:14.5px"') + "</g>")
    return d.svg(1160, 356, s)


# ── 5. Claude 가 작업할 때 참고하는 것 (hx.arch 를 이 과정 말로) ─────────
def arch():
    ctx = [("Claude Code 기본 지침", "항상"), ("도구 정의", "항상"), ("CLAUDE.md", "항상"), ("Skill 목록", "이름 · 설명만"),
           ("Sub Agent 목록", "이름 · 설명만"), ("대화 · 도구 결과", "쌓임"), ("새 요청", "이번 요청")]
    left = "".join(f'<div class="ar-it"><b>{a}</b><em>{b}</em></div>' for a, b in ctx)
    acts = ["답하기", "도구 쓰기 · 읽기 · 실행 · 저장", "Skill 본문 불러오기", "Sub Agent 에게 맡기기"]
    mid = "".join(f'<div class="ar-act">{a}</div>' for a in acts)
    gate = [("권한", "settings.json · 허용 · 거부 · 확인"), ("Hook", "실행 전후 검사 · 차단"), ("실행", "파일 · 명령")]
    right = "".join(f'<div class="ar-g"><b>{a}</b><em>{b}</em></div>' for a, b in gate)
    return (f'<div class="arch"><div class="ar-col ar-ctx"><div class="ar-h">① 모델이 읽는 것 · 컨텍스트</div>{left}</div>'
            f'<div class="ar-arrow">→</div>'
            f'<div class="ar-col ar-model"><div class="ar-h">② Claude 가 고르는 것</div>{mid}</div>'
            f'<div class="ar-arrow">→</div>'
            f'<div class="ar-col ar-gate"><div class="ar-h">③ 모델 밖에서 작동 · 코드</div>{right}</div></div>'
            f'<div class="ar-loop">↺ 실행 결과는 다시 ①로 쌓이고, 끝날 때까지 반복</div>')


TREE = ("sim-lab/\n"
        "├── CLAUDE.md                        규칙 · 정답 숫자\n"
        "├── data/ · output/                  원본(읽기만) · 결과\n"
        "└── .claude/\n"
        "    ├── settings.json                권한 · Hook 등록 · 팀 공유\n"
        "    ├── settings.local.json          내 PC 전용 · git 제외\n"
        "    ├── skills/data-report/SKILL.md  분석 절차\n"
        "    ├── agents/file-summary.md       Sub Agent 하나 = 파일 하나\n"
        "    └── hooks/guard.py               Hook 스크립트")


def scopes():
    """하네스 위치 — 전역 · 프로젝트 · 내 PC만 (viz2.scopes 를 이 과정 범위로 · MCP 는 다루지 않음)."""
    cols = [("전역", "~/.claude/", "내 모든 프로젝트 · 설정 우선 ③", "", [("CLAUDE.md", "~/.claude/CLAUDE.md"), ("Skill · Agent", "~/.claude/skills/ · agents/"),
                                                                  ("권한 · Hook", "~/.claude/settings.json"), ("플러그인", "~/.claude/plugins/")]),
            ("프로젝트", "./.claude/", "git 으로 팀 공유 · 설정 우선 ②", "on", [("CLAUDE.md", "./CLAUDE.md"), ("Skill · Agent", "./.claude/skills/ · agents/"),
                                                                    ("권한 · Hook", "./.claude/settings.json")]),
            ("내 PC만", "이 프로젝트 · 나만", "git 에 안 올림 · 설정 우선 ①", "", [("권한 · Hook", "./.claude/settings.local.json"),
                                                                   ("나만 보는 규칙", "./CLAUDE.local.md")])]
    out = []
    for i, (h, path, sub, cls, rows) in enumerate(cols):
        r = "".join(f'<div class="scp-r"><b>{a}</b><code>{b}</code></div>' for a, b in rows)
        out.append(f'<div class="scp-c {cls}" style="--d:{i * .25:.2f}s"><div class="scp-h"><b>{h}</b><code>{path}</code><span>{sub}</span></div>{r}</div>')
    return f'<div class="scp">{"".join(out)}</div>'


# ── 6. 부록 · 플러그인 = 하네스 묶음 ─────────────────────────────
def plugin_pack():
    """마켓플레이스의 플러그인 하나 = Skill · Agent · Hook · MCP 서버 묶음 → /plugin install 한 번 → 내 Claude Code 에 그대로. 10초."""
    d = _D("pqp", 10)
    pc = lambda t: t / 10 * 100  # noqa: E731
    chips = [("skills/", "Skill · 절차"), ("agents/", "Sub Agent · 역할"), ("hooks/", "Hook · 자동 검사"), (".mcp.json", "MCP 서버 · 외부 연결")]
    s = (f'<g {d.show(pc(.2))}><rect x="30" y="30" width="380" height="340" rx="16" fill="#FFF8F1" stroke="{O}" stroke-width="2.5"/>'
         + _t(56, 64, "플러그인", "tt", "start", 'style="font-size:22px"') + _t(56, 94, "하네스 묶음 · 마켓플레이스에서 받음", "ts", "start") + "</g>")
    s += (f'<g {d.show(pc(.2))}><rect x="660" y="30" width="470" height="340" rx="16" fill="{W}" stroke="{K}" stroke-width="2.5"/>'
          + _t(686, 64, "내 Claude Code", "tt", "start", 'style="font-size:22px"') + _t(686, 94, "~/.claude/plugins/", "tm", "start") + "</g>")
    for i, (a, b) in enumerate(chips):
        y = 118 + i * 60
        for x0, w, t in [(56, 330, .6 + i * .6), (686, 420, 4.6 + i * .5)]:
            s += (f'<g {d.show(pc(t))}><rect x="{x0}" y="{y}" width="{w}" height="46" rx="10" fill="{W}" stroke="{K}" stroke-width="2"/>'
                  + _t(x0 + 16, y + 23, a, "tm", "start", 'style="font-size:15px"') + _t(x0 + w - 16, y + 23, b, "ts", "end", 'style="font-size:14.5px"') + "</g>")
    s += (f'<g {d.show(pc(3.6))}><path d="M424 200 H640" stroke="{O}" stroke-width="4" marker-end="url(#{d.id("o")})"/>'
          + _t(532, 178, "/plugin install", "tm", extra=f'style="font-size:15px;fill:#EF6C00"') + _t(532, 224, "한 번에 설치", "ts") + "</g>")
    s += (f'<g {d.show(pc(7.4))}><rect x="300" y="388" width="560" height="38" rx="19" fill="{N}"/>'
          + _t(580, 407, "「/플러그인:Skill」 로 호출 · 예 /commit-commands:commit", "tw", extra='style="font-size:14.5px"') + "</g>")
    return d.svg(1160, 432, s)


def slides():
    prompt = ("너는 데이터 분석 담당이다.\n"
              "아래 사과 선별 기록에서\n"
              "상품 · 불량 개수와 상품률을\n"
              "표로 정리해 줘.\n\n"
              "(엑셀 내용을 여기에 붙여 넣기)")
    answer = (f"| 구분   | 개수   |\n"
              f"| 상품   | {DN['pass']:<6} |\n"
              f"| 불량   | {DN['fail']:<6} |\n"
              f"| 상품률 | {DN['rate']}% |\n\n"
              "→ 표는 대화창에만 · 저장 · 다음 날 반복은 사람")
    plug = ("/plugin                                    # Discover 탭 · 둘러보기 · 검색\n"
            "/plugin install superpowers@claude-plugins-official\n"
            "                                           # 상세 확인 → 범위 선택 → 설치\n"
            "/plugin marketplace add anthropics/claude-plugins-community\n"
            "                                           # 다른 마켓 추가 · @claude-community 로 설치")
    return [
        # ── Ⅱ 도입 · AI 활용 방식의 변화
        light("AI 활용 방식의 변화", shift(), T),
        light("프롬프트 엔지니어링", two(code("채팅창에 보내는 요청 한 번", esc(prompt)), code("채팅 답 예", esc(answer)))
              + viz2.tiles([("손대는 곳", "질문 문장 · 역할 · 형식"), ("효과", "이번 답 한 번")], 2), T),
        light("프롬프트만의 한계", viz2.tiles([
            ("매번 붙여 넣기", "엑셀을 열어 복사 · 대화창에 붙임"), ("매번 같은 설명", "기준 · 형식을 대화마다 다시"),
            ("빠진 자료는 모름", "붙이지 않은 기준은 추측")], 3)
              + flow([("엑셀 열기", "사람"), ("복사 · 붙여 넣기", "사람"), ("기준 다시 설명", "사람"), ("답 받기", "모델"),
                      ("표 옮겨 저장", "사람")], hl=3), T),
        light("컨텍스트 엔지니어링", viz2.pair(
            "보여 줄 것", [("사과 엑셀", f"apple_A07.xlsx · {DN['rows']}행"), ("선별 기준표", f"멍 · 벌레 · 무게 {sk.MIN_W}g · 당도 {sk.MIN_SUGAR:g}"),
                         ("지난 요약", "형식 · 숫자 예")],
            "뺄 것", [("다른 날 파일", "A01 ~ A25 중 24개"), ("관계없는 대화", "앞서 한 다른 일")], hl="l")
              + viz2.tiles([("손대는 곳", "모델이 읽는 자료 · 넣을 것과 뺄 것")], 1), T),
        light("컨텍스트만의 한계", viz2.tiles([
            ("글로만 답함", "파일 저장 · 코드 실행은 사람"), ("긴 일은 나눠서", "단계마다 사람이 다음 요청"),
            ("확인도 사람", "숫자 대조 · 빠진 것 찾기")], 3)
              + flow([("자료 고르기", "사람"), ("답 · 코드", "모델"), ("코드 실행 · 저장", "사람"), ("결과 확인", "사람"),
                      ("다음 요청", "사람")], hl=1), T),
        light("에이전틱 AI", flow([("도구 호출", "2023.06 · 부를 함수 · 값을 모델이 고름"), ("긴 작업", "작업 길이 · 89일마다 2배"),
                                  ("연결 표준", "2024.11 · MCP"), ("에이전틱 AI", "목표를 받아 직접 실행 · 확인 반복")], hl=3)
              + viz2.tiles([("목표", "「사과 엑셀 요약해 줘」"), ("스스로 고름", "읽을 파일 · 쓸 도구"), ("반복", "결과를 보고 다음 행동")], 3)
              + src(OAI_FC, ANT_MCP, METR_11), T),
        light("AI가 맡을 수 있는 작업 길이", metr() + src(METR_11, METR_TH), T),
        light("에이전트만의 한계", flow([("지시 한 번", "사람"), ("도구 수십 번", "AI · 사람은 안 봄"), ("결과 보고", "AI"), ("최종 확인", "사람")], hl=1)
              + viz2.tiles([("규칙을 놓침", "대화로만 한 「원본은 고치지 마」"), ("위험한 실행", "원본 엑셀 덮어쓰기 · 파일 삭제"),
                            ("덜 된 결과", "숫자 대조 없이 「다 했다」")], 3), T),
        light("하네스 엔지니어링", anatomy() + src(CC_HOW, OAI_HE), T),
        # ── Ⅱ 설명 · 컨텍스트 관리
        light("컨텍스트 관리가 필요한 이유", ctx_why() + src(CC_BP, CC_HOW), T),
        # ── Ⅱ 설명 · .claude
        light("Claude가 작업할 때 참고하는 것", arch() + src(CC_HOW, CC_DIR), T),
        light("프로젝트 폴더 구조 · .claude/", two(
            '<div class="ctree">' + code("폴더 구조 예 · sim-lab", esc(TREE)) + "</div>",
            viz2.tiles([("CLAUDE.md", "대화 시작 때 항상"), ("skills/", "요청이 설명과 맞을 때"),
                        ("agents/", "Claude 가 맡길 때 · 따로 일함"), ("settings.json", "권한 · Hook · 항상 적용")], 1))
              + src(CC_DIR), T),
        light("전역 · 프로젝트 하네스 위치", scopes() + src(CC_DIR), T),
        light("Sub Agent의 흐름", viz2.subagent_flow(
            ask="「파일 4개 요약해 줘」", name="file-summary", tools=("Read", "Bash"),
            files=("apple_A07.xlsx", "apple_A25.xlsx", "wafer_test_W07.xlsx", "wafer_test_W21.xlsx"),
            back="파일마다 행 수 · 비율 한 줄", fw=172, ffs=12.5) + src(CC_SUB), T),
        # ── 부록 · 플러그인 마켓플레이스
        light("플러그인", plugin_pack() + src(CC_PLUG), T),
        light("마켓플레이스", flow([("마켓플레이스", "플러그인 목록 · GitHub 저장소"), ("플러그인", "Skill · Agent · Hook 묶음"),
                                   ("설치", "/plugin install 이름@마켓")], hl=0)
              + viz2.tiles([("claude-plugins-official", "Anthropic 공식 · 처음 실행 때 자동 추가 · 자동 업데이트"),
                            ("claude-community", "작성자가 제출한 플러그인 · 직접 추가"),
                            ("다른 저장소", "회사 · 개인 GitHub · /plugin marketplace add"),
                            ("둘러보기", "/plugin Discover 탭 · claude.com/marketplace")], 2)
              + src(CC_MKT), T),
        light("플러그인 설치 순서", code("Claude Code", esc(plug))
              + viz2.tiles([("나 · 모든 프로젝트", "user · ~/.claude/settings.json"), ("이 저장소 · 모두", "project · .claude/settings.json"),
                            ("이 저장소 · 나만", "local · .claude/settings.local.json")], 3)
              + src(CC_PLUG), T),
        light("많이 쓰는 공개 하네스", viz2.tiles([
            ("Superpowers", f"GitHub ★ {SP_STARS / 1e4:.1f}만 · 설계 → 계획 → 테스트 → 리뷰 순서"),
            ("gstack", f"GitHub ★ {GS_STARS / 1e4:.1f}만 · 기획 · 디자인 · 리뷰 · QA 역할 명령"),
            ("공식 마켓 플러그인", "commit-commands · code-review · feature-dev")], 3)
              + code("설치 · 각 저장소 README", esc(
                  "/plugin install superpowers@claude-plugins-official        # Superpowers · 공식 마켓\n"
                  "git clone --single-branch --depth 1 https://github.com/garrytan/gstack.git \\\n"
                  "  ~/.claude/skills/gstack && cd ~/.claude/skills/gstack && ./setup   # gstack"))
              + src(GH_SP, GH_GS, CC_MKT), T),
        light("설치 전 점검", viz2.tiles([
            ("실행하는 것", "Hook · MCP 서버가 내 PC 에서 실행"), ("컨텍스트 비용", "매 요청 · 호출 때 늘어나는 토큰"),
            ("출처", "공식 · 커뮤니티 · 개인 저장소 · 개인 저장소는 검토 없음"), ("필요한 것만", "안 쓰는 플러그인은 끄기 · 지우기")], 2)
              + src(CC_PLUG, CC_MKT), T),
    ]
