"""실습 순서 장(단계마다 그대로 입력할 짧은 프롬프트) · Hook · Sub Agent 실습 장(원본 보호 Hook · 파일 4개 병렬 요약).

예전 「실습 N 순서 · 요청 항목」(목표 · 입력 · 산출물 · 하지 말 것)은 무엇을 입력할지 바로 보이지 않아 이 모듈의 「실습 N 순서」로 바꾼다.
build.py 가 v1kit.SKIP 에 PROMPTS 의 실습 번호를 넣어 예전 brief() 장을 만들지 않게 한다. 숫자는 sk 에서 계산. 접두어 plb.
"""
import json
from pathlib import Path

import sk
import viz2
from anim import K, N, O, OK, R, W, _D, _t
from deck import flow, lab, light
from hx import code, esc, two
from stats_hx import src

T = "실습"
DN, WN = sk.DN, sk.WN


def _nums():
    """병렬 요약 실습의 정답 — data/ 의 엑셀 4개 (행 · 합격(상품) · 비율)."""
    out = []
    for f, name in [("A07", "apple_A07"), ("A25", "apple_A25")]:
        df = sk.apple(f)
        n, g = len(df), int((df["등급"] == "상품").sum())
        out.append((name, n, g, round(g / n * 100, 2)))
    for f in ["W07", "W21"]:
        df = sk.wafer(f)
        g, rate = sk.yld(df)
        out.append((f"wafer_test_{f}", len(df), int(g), float(rate)))
    return out


FOUR = _nums()
CC_HOOK = ("Claude Code 문서 · Hooks", "https://code.claude.com/docs/en/hooks")
CC_SUB = ("Claude Code 문서 · Subagents", "https://code.claude.com/docs/en/sub-agents")
CC_BP = ("Claude Code 문서 · Best practices", "https://code.claude.com/docs/en/best-practices")


def _pct(x):
    return f"{x:.2f}%"


# ── 실습마다 단계 · 그대로 입력할 프롬프트 · 확인 숫자 ──────────────────
# 프롬프트 앞에 「!」 가 있으면 입력이 아니라 손으로 하는 일(브라우저 · 단축키)
def prompts():
    a07, w07 = DN, WN
    f = {n: (r, g, p) for n, r, g, p in FOUR}
    return {
        "1-1": ([("폴더 만들기", "!새 폴더 sim-lab → VS Code 로 열기 → 받은 sim-data.zip 을 폴더에 넣기"),
                 ("압축 풀기", "sim-data.zip 을 이 폴더에 풀어 줘"),
                 ("CLAUDE.md", "data/ 는 읽기만 하고 결과는 output/ 에 저장하는 CLAUDE.md 를 만들어 줘"),
                 ("사과 엑셀 요약", "data/apple_A07.xlsx 를 요약해 줘"),
                 ("열 나누기", "열을 수치형과 범주형으로 나눠 줘"),
                 ("저장", "요약을 docs/사과_요약.md 로 저장해 줘")],
                ["data/ 엑셀 4개 · templates/ 3개", f"{a07['rows']}행 × {a07['cols']}열",
                 f"상품 {a07['pass']} · 불량 {a07['fail']} · {_pct(a07['rate'])}"]),
        "11-3": ([("집계", "불량 사유별 · 위치별로 집계해서 엑셀 시트로 저장해 줘"),
                  ("CSV", "apple_A07 을 CSV 로도 저장해 줘"),
                  ("대조", "사유별 합계가 불량 수와 같은지 확인해 줘"),
                  ("엑셀 필터", "!엑셀에서 등급 열을 「상품」으로 걸러 개수 세기 · 보고와 비교")],
                 [f"상품 {a07['pass']} · 불량 {a07['fail']}", f"사유별 합 {sum(a07['reason'].values())}"]),
        "21-1": ([("순서 정리", "지금까지 사과 분석에서 한 순서를 정리해 줘"),
                  ("Skill 만들기", "그 순서를 data-report 라는 Skill 로 만들어 줘"),
                  ("내용 확인", "SKILL.md 의 description 과 단계를 보여 줘"),
                  ("새 대화 · /clear", "data-report 로 사과 A07 분석해 줘")],
                 [f"{a07['rows']}행 · 상품 {a07['pass']} · {_pct(a07['rate'])}", "앞 실습과 같은 형식"]),
        "21-2": ([("웨이퍼 분석", "data-report 로 wafer_test_W07 분석해 줘"),
                  ("결과 위치", "요약 · 집계 파일이 어디 있는지 알려 줘"),
                  ("숫자 대조", "합격 수와 수율을 다시 계산해서 맞는지 봐 줘"),
                  ("Skill 보완", "빠진 단계가 있으면 data-report 에 추가해 줘")],
                 [f"{w07['rows']}행 · 합격 {w07['pass']} · 수율 {_pct(w07['yield'])}"]),
        "22-1": ([("Hook 만들기", "data/ 파일은 고치거나 지우지 못하게 Hook 을 만들어 줘"),
                  ("설정 보기", "만든 Hook 설정과 스크립트를 보여 줘"),
                  ("막히는지 보기", "data/apple_A07.xlsx 의 당도를 반올림해서 그 파일에 저장해 줘"),
                  ("허용 확인", "같은 결과를 output/ 에 새 파일로 저장해 줘")],
                 ["3 → 막힘 · 이유 한 줄", "4 → output/ 에 저장", "data/ 원본 그대로"]),
        "22-2": ([("Agent 만들기", "엑셀 하나를 요약하는 file-summary Agent 를 만들어 줘"),
                  ("파일 보기", "만든 Agent 파일을 보여 줘"),
                  ("동시에 맡기기", "data/ 엑셀 4개를 file-summary 4개로 동시에 요약해 줘"),
                  ("표로 모으기", "결과를 표 하나로 모아 output/ 에 저장해 줘")],
                 [f"A07 {_pct(f['apple_A07'][2])} · A25 {_pct(f['apple_A25'][2])}",
                  f"W07 {_pct(f['wafer_test_W07'][2])} · W21 {_pct(f['wafer_test_W21'][2])}"]),
        "22-3": ([("도구 만들기", "data/ 엑셀의 수율을 계산하는 MCP 도구를 만들어 이 프로젝트에 연결해 줘"),
                  ("다시 열기", "!Claude Code 다시 열기 → 서버 사용 승인 → /mcp 에서 yield-tools 확인"),
                  ("도구로 계산", "yield 도구로 data/ 엑셀 4개의 수율을 알려 줘"),
                  ("호출 확인", "!답 위에 yield_of 호출 표시가 있는지 보기")],
                 [f"A07 {_pct(f['apple_A07'][2])} · A25 {_pct(f['apple_A25'][2])}",
                  f"W07 {_pct(f['wafer_test_W07'][2])} · W21 {_pct(f['wafer_test_W21'][2])}", "/mcp · yield-tools 도구 1개"]),
        "3-2": ([("계획 · Plan Mode", "!Shift+Tab 으로 Plan Mode → 「W07 숫자 카드 4개 화면 계획 세워 줘」"),
                 ("뼈대", "계획대로 만들어 줘. 꾸밈 없이 숫자만"),
                 ("꾸밈", "숫자 4개를 카드 모양으로 꾸며 줘"),
                 ("바꾸기", "수율 카드만 주황색으로 크게 해 줘")],
                [f"{w07['rows']} · {w07['pass']} · {w07['fail']} · {_pct(w07['yield'])}"]),
        "4-2": ([("칸 그리기", "카드 아래에 칩 616개를 die_x · die_y 위치대로 회색 칸으로 그려 줘"),
                 ("색 · 범례", "합격은 초록, 불합격은 빨강으로 칠하고 범례를 붙여 줘"),
                 ("툴팁", "칸에 마우스를 올리면 그 칩 정보를 보여 줘"),
                 ("캡처로 고치기", "!화면 캡처를 붙이고 「이 부분이 겹쳐 보여. 고쳐 줘」")],
                [f"초록 {w07['pass']} · 빨강 {w07['fail']}", "툴팁 값 = 엑셀 그 행"]),
        "5-2": ([("사유별 막대", "불합격 사유별 개수를 막대그래프로 넣어 줘"),
                 ("위치별 막대", "위치별 합격률 막대도 넣어 줘"),
                 ("배치", "맵은 왼쪽, 차트는 오른쪽으로 놓아 줘"),
                 ("읽히는 사실", "차트에서 읽히는 사실 세 가지를 적어 줘")],
                [f"막대 합계 {w07['fail']}", f"깨짐 · 긁힘 {max(w07['reason'].values())}개 1위"]),
        "6-2": ([("분포 · 합격선", "누설전류 분포를 그리고 합격선을 표시해 줘"),
                 ("조절 바", "합격선을 조절 바로 바꾸면 카드 · 맵 · 차트가 다시 계산되게 해 줘"),
                 ("숫자 보고", "상한 5 · 10 · 20 일 때 수율과 불합격 수를 알려 줘"),
                 ("다시 지시", "!안 바뀐 곳이 있으면 「맵도 같이 바뀌게 해 줘」")],
                ["상한 10 → " + _pct(w07['yield']), "카드 · 맵 · 차트 · 분포가 함께 바뀜"]),
        "7-2": ([("설계표", "합격기준표.md 기준마다 조절 바 설계표를 만들어 줘"),
                 ("조절 바 8개", "설계표대로 조절 바 8개를 만들어 줘"),
                 ("배치", "조절 바는 왼쪽, 결과는 오른쪽에 놓아 줘"),
                 ("처음 값", "처음 값 버튼과 원본 대비 차이를 넣어 줘"),
                 ("점검", "점검할 숫자 네 가지가 맞는지 확인해 줘")],
                ["처음 값 → " + _pct(w07['yield']), "점검 숫자 네 가지 일치"]),
        "31-1": ([("올리기", "엑셀이나 CSV 를 올리면 그 파일로 다시 분석하게 해 줘"),
                  ("다른 파일", "!브라우저에서 wafer_test_W21.xlsx 올리기 · 숫자가 바뀌는지 보기"),
                  ("내려받기", "판정 결과를 CSV 로 내려받는 버튼을 넣어 줘"),
                  ("한 파일 정리", "index.html 한 파일로 정리해 줘")],
                 [f"W07 → {_pct(w07['yield'])}", f"W21 → {_pct(f['wafer_test_W21'][2])}"]),
        "31-2": ([("GitHub 로그인", "GitHub 에 로그인해 줘"),
                  ("올리기 전 점검", "올리기 전에 키나 개인 정보가 있는지 확인해 줘"),
                  ("저장소 올리기", "이 폴더를 GitHub 저장소로 만들어 올려 줘"),
                  ("Vercel 배포", "!vercel.com → Add New → Project → 저장소 Import → Deploy")],
                 [f"배포 주소에서 W07 수율 {_pct(w07['yield'])}", "고친 뒤 같은 주소에 반영"]),
        "41-1": ([("주제", "내 엑셀로 만들 수 있는 화면 세 가지만 제안해 줘"),
                  ("규칙", "이 프로젝트용 CLAUDE.md 를 만들어 줘"),
                  ("계획 · Plan Mode", "만들 화면 계획 세워 줘"),
                  ("만들기", "첫 화면부터 하나씩 만들어 줘"),
                  ("배포", "GitHub 저장소로 올려 줘")],
                 ["배포 주소가 열림", "입력을 바꾸면 결과가 바뀜"]),
    }


PROMPTS = prompts()


def order(no):
    rows, checks = PROMPTS[no]
    r = ""
    for i, (lab_, p) in enumerate(rows):
        hand = p.startswith("!")
        q = f'<q class="nb">{p[1:]}</q>' if hand else f"<q>{p}</q>"
        r += f'<div class="plbr" style="--d:{i * .35:.2f}s"><em>{i + 1}</em><b>{lab_}</b>{q}</div>'
    ck = "".join(f"<span>{c}</span>" for c in checks)
    return light(f"실습 {no} 순서", f'<div class="plbs">{r}</div><div class="plbk"><b>확인</b>{ck}</div>', T)


# ── Hook · Sub Agent 실습 장 ─────────────────────────────────────
def hook_agent():
    """왼쪽: data/ 에 저장하려는 도구 호출 → Hook(guard.py) 이 막고 이유를 돌려줌 → output/ 에 저장.
    오른쪽: 메인 Claude 가 file-summary 4개에 파일을 하나씩 동시에 맡김 → 결과 4줄이 표로. 14초."""
    d = _D("plh", 14)
    pc = lambda t: t / 14 * 100  # noqa: E731
    s = _t(10, 20, "Hook · 원본 보호", "tt", "start", 'style="font-size:20px"')
    s += (f'<g {d.show(pc(.4))}><rect x="10" y="42" width="540" height="40" rx="20" fill="{N}"/>'
          + _t(280, 62, "「apple_A07 당도를 반올림해서 그 파일에 저장해 줘」", "tw", extra='style="font-size:14px"') + "</g>")
    s += (f'<g {d.show(pc(1.4))}><path d="M280 84 V104" stroke="{N}" stroke-width="2.5" marker-end="url(#{d.id("k")})"/>'
          f'<rect x="200" y="108" width="160" height="42" rx="12" fill="#FFF3E6" stroke="{O}" stroke-width="2.5"/>'
          + _t(280, 129, "Claude", "tt", extra='style="font-size:17px"') + "</g>")
    s += (f'<g {d.show(pc(2.6))}><path d="M280 152 V172" stroke="{O}" stroke-width="2.5" marker-end="url(#{d.id("o")})"/>'
          f'<rect x="90" y="176" width="380" height="38" rx="10" fill="{W}" stroke="{K}" stroke-width="2"/>'
          + _t(280, 195, "도구 호출 · data/apple_A07.xlsx 에 저장", "tm", extra='style="font-size:13.5px"') + "</g>")
    s += (f'<g {d.show(pc(3.8))}><path d="M280 216 V234" stroke="{K}" stroke-width="2.5" marker-end="url(#{d.id("k")})"/>'
          f'<rect x="150" y="238" width="260" height="40" rx="10" fill="{N}"/>'
          + _t(280, 258, "Hook · guard.py 검사", "tw", extra='style="font-size:14.5px"') + "</g>")
    s += (f'<g {d.show(pc(5.2))}><rect x="10" y="296" width="540" height="40" rx="10" fill="#FDECEA" stroke="{R}" stroke-width="2.5"/>'
          + _t(28, 316, "✕ 차단", "tn", "start", f'style="font-size:15px;fill:{R}"')
          + _t(300, 316, "data/ 원본은 고치지 않는다 · 결과는 output/ 에", "tn", extra=f'style="font-size:14px;fill:{R}"') + "</g>")
    s += (f'<g {d.show(pc(6.6))}><rect x="10" y="350" width="540" height="40" rx="10" fill="#E8F5E9" stroke="{OK}" stroke-width="2.5"/>'
          + _t(28, 370, "✓ 다시", "tn", "start", f'style="font-size:15px;fill:{OK}"')
          + _t(300, 370, "output/ 에 새 파일로 저장 · data/ 그대로", "tn", extra=f'style="font-size:14px;fill:{OK}"') + "</g>")
    # 오른쪽 · Sub Agent 4개 동시
    X = 600
    s += f'<line x1="575" y1="6" x2="575" y2="404" stroke="#D9DDE3" stroke-width="2" stroke-dasharray="6 6"/>'
    s += f'<g {d.show(pc(7.6))}>' + _t(X + 10, 20, "Sub Agent · 동시에 4개", "tt", "start", 'style="font-size:20px"') + "</g>"
    s += (f'<g {d.show(pc(7.8))}><rect x="{X + 170}" y="42" width="210" height="40" rx="12" fill="#FFF3E6" stroke="{O}" stroke-width="2.5"/>'
          + _t(X + 275, 62, "메인 Claude", "tt", extra='style="font-size:16px"') + "</g>")
    for i, (name, n, g, p) in enumerate(FOUR):
        x0 = X + 6 + i * 138
        s += (f'<g {d.show(pc(8.6))}><path d="M{X + 275} 84 L{x0 + 63} 124" stroke="{O}" stroke-width="2"/>'
              f'<rect x="{x0}" y="126" width="126" height="84" rx="10" fill="#FFF8F1" stroke="{O}" stroke-width="2" stroke-dasharray="6 4"/>'
              + _t(x0 + 63, 146, "file-summary", "tn", extra='style="font-size:13px"')
              + _t(x0 + 63, 168, name, "tm", extra='style="font-size:11.5px"')
              + f'<rect x="{x0 + 12}" y="186" width="102" height="10" rx="5" fill="#F4E3D0"/></g>')
        s += (f'<rect x="{x0 + 12}" y="186" height="10" rx="5" fill="{O}" '
              + d.a([(0, "width:0px"), (pc(8.9), "width:0px"), (pc(10.6), "width:102px"), (100, "width:102px")]) + "/>")
    s += (f'<g {d.show(pc(11.2))}><rect x="{X + 6}" y="232" width="546" height="160" rx="12" fill="{W}" stroke="{K}" stroke-width="2"/>'
          + "".join(_t(X + x_, 254, h, "ts", a_, 'style="font-size:13.5px"') for x_, h, a_ in [(24, "파일", "start"), (330, "행", "end"), (430, "합격 · 상품", "end"), (530, "비율", "end")])
          + "</g>")
    for i, (name, n, g, p) in enumerate(FOUR):
        y = 284 + i * 28
        s += (f'<g {d.show(pc(11.6 + i * .4))}>' + _t(X + 24, y, name, "tm", "start", 'style="font-size:13.5px"')
              + _t(X + 330, y, n, "tn", "end") + _t(X + 430, y, g, "tn", "end") + _t(X + 530, y, _pct(p), "tn", "end", f'style="fill:{O}"') + "</g>")
    return d.svg(1160, 400, s)


def parallel():
    """한 대화에서 하나씩(파일 4개) vs Sub Agent 4개 동시 — 메인 대화에 남는 기록 차이. 숫자 없이 모양만. 10초."""
    d = _D("plq", 10)
    pc = lambda t: t / 10 * 100  # noqa: E731
    names = [n for n, *_ in FOUR]
    s = _t(20, 40, "한 대화에서 하나씩", "tn", "start", 'style="font-size:17px"') + _t(20, 196, "Sub Agent 4개 동시", "tn", "start", 'style="font-size:17px;fill:#EF6C00"')
    for i, nm in enumerate(names):                                  # 차례로 — 한 줄에 이어서
        x0, t0 = 220 + i * 222, .4 + i * 2
        s += f'<rect x="{x0}" y="22" width="214" height="36" rx="8" fill="#EEF1F5" stroke="#C9CFD8"/>'
        s += (f'<rect x="{x0}" y="22" height="36" rx="8" fill="{K}" '
              + d.a([(0, "width:0px"), (pc(t0), "width:0px"), (pc(t0 + 1.8), "width:214px"), (100, "width:214px")]) + "/>")
        s += f'<g {d.show(pc(t0 + .2))}>' + _t(x0 + 107, 40, nm, "tw", extra='style="font-size:12.5px;font-family:var(--mono,monospace)"') + "</g>"
    for i, nm in enumerate(names):                                  # 동시에 — 네 줄
        y = 170 + i * 44
        s += f'<rect x="220" y="{y}" width="214" height="36" rx="8" fill="#FFF3E6" stroke="#F2C58F"/>'
        s += (f'<rect x="220" y="{y}" height="36" rx="8" fill="{O}" '
              + d.a([(0, "width:0px"), (pc(.4), "width:0px"), (pc(2.2), "width:214px"), (100, "width:214px")]) + "/>")
        s += f'<g {d.show(pc(.6))}>' + _t(327, y + 18, nm, "tw", extra='style="font-size:12.5px;font-family:var(--mono,monospace)"') + "</g>"
    s += (f'<g {d.show(pc(2.6))}><path d="M450 188 H490" stroke="{O}" stroke-width="2.5" marker-end="url(#{d.id("o")})"/>'
          f'<rect x="500" y="200" width="420" height="96" rx="14" fill="{W}" stroke="{O}" stroke-width="2.5"/>'
          + _t(710, 232, "메인 대화에는 결과 4줄만", "tn", extra='style="font-size:17px"')
          + _t(710, 264, "파일 읽기 · 계산은 각자 자기 컨텍스트에서", "ts", extra='style="font-size:14.5px"') + "</g>")
    s += (f'<g {d.show(pc(8.6))}>' + _t(1106, 84, "메인 대화에 파일 4개 기록이 다 쌓임", "tn", "end", f'style="font-size:15px;fill:{K}"') + "</g>")
    s += (f'<g {d.show(pc(9.2))}><rect x="500" y="320" width="420" height="40" rx="20" fill="#F4F6F9"/>'
          + _t(710, 340, "Agent 마다 따로 요청 · 토큰은 더 듦", "ts", extra='style="font-size:14.5px"') + "</g>")
    return d.svg(1160, 372, s)


# ── 수율 도구 (MCP) — 완성본 labs/harness-solution · MCP 공식 클라이언트로 시험함(엑셀 4개 = FOUR)
SOL = Path(__file__).resolve().parent.parent / "labs" / "harness-solution"
CC_MCP = ("Claude Code 문서 · MCP", "https://code.claude.com/docs/en/mcp")


def _tool_code():
    """완성본 tools/yield_server.py 의 핵심 부분(server = … return …) — 화면 코드 = 시험한 파일."""
    t = (SOL / "tools" / "yield_server.py").read_text(encoding="utf-8").split("\n")
    i = next(k for k, x in enumerate(t) if x.startswith("server = "))
    j = next(k for k, x in enumerate(t) if x.strip().startswith("return "))
    body = [x for x in t[i:j + 1] if x.strip()]
    return "\n".join(body)


def _mcp_json():
    """완성본 .mcp.json 의 서버 이름 → 실행 명령 한 줄."""
    cfg = json.loads((SOL / ".mcp.json").read_text(encoding="utf-8"))["mcpServers"]
    name, v = next(iter(cfg.items()))
    return f"{name} → {v['command']} {' '.join(v['args'])}"


def mcp_flow():
    """MCP 도구 흐름 — Claude Code ↔ MCP 서버(yield-tools) ↔ data/ 엑셀.
    ① 시작할 때 도구 목록을 받아 Claude Code 의 도구 목록(컨텍스트)에 yield_of 가 더해짐 → ② 「W07 수율 알려 줘」 → yield_of 호출
    → ③ 서버가 엑셀을 읽어 계산 → ④ 결과 → ⑤ 답. 숫자는 FOUR(데이터에서 계산). 11초 · 한 번."""
    D = 11
    d = _D("plm", D)
    pc = lambda t: t / D * 100  # noqa: E731
    _, rows, ok, rate = next(x for x in FOUR if x[0].endswith("W07"))
    mono = 'style="font-size:{}px;fill:{}"'.format
    # Claude Code · 도구 목록
    s = (f'<rect x="0" y="8" width="340" height="414" rx="18" fill="#F4F6F9" stroke="{K}" stroke-width="2.5"/>'
         + _t(20, 36, "Claude Code", "tt", "start")
         + f'<rect x="14" y="56" width="312" height="196" rx="12" fill="{W}" stroke="#C9CFD8" stroke-width="1.5"/>'
         + _t(28, 78, "컨텍스트 · 쓸 수 있는 도구 목록", "ts", "start", 'style="font-size:13.5px;font-weight:700"'))
    for i, (n, x) in enumerate([("Read", "파일 읽기"), ("Edit", "파일 고치기"), ("Bash", "명령 실행")]):
        y = 106 + i * 32
        s += _t(30, y, n, "tm", "start", mono(15, N)) + _t(118, y, x, "ts", "start", 'style="font-size:14px"')
    s += (f'<g {d.show(pc(2.4))}><rect x="22" y="187" width="296" height="38" rx="8" fill="#FFF3E6" stroke="{O}" stroke-width="2"/>'
          + _t(30, 206, "yield_of", "tm", "start", mono(15, "#EF6C00")) + _t(118, 206, "엑셀 수율 · yield-tools", "ts", "start", 'style="font-size:14px"')
          + "</g>")
    s += (f'<g {d.show(pc(3.6))}><rect x="14" y="268" width="312" height="52" rx="12" fill="#EEF4FD" stroke="#4A86E8" stroke-width="2"/>'
          + _t(28, 294, "사용자 「W07 수율 알려 줘」", "tn", "start", 'style="font-size:15px"') + "</g>")
    s += (f'<g {d.show(pc(8.2))}><rect x="14" y="336" width="312" height="70" rx="12" fill="{W}" stroke="{OK}" stroke-width="2.5"/>'
          + _t(28, 360, f"「W07 수율 {rate:.2f}%」", "tn", "start", f'style="font-size:17px;fill:{OK}"')
          + _t(28, 388, "yield_of 결과로 답", "ts", "start", 'style="font-size:13.5px"') + "</g>")
    # MCP 서버
    s += (f'<rect x="500" y="110" width="270" height="200" rx="16" fill="{W}" stroke="{K}" stroke-width="2.5"/>'
          + _t(520, 140, "MCP 서버", "tt", "start") + _t(520, 170, "yield-tools", "tm", "start", mono(15, N))
          + _t(520, 196, "tools/yield_server.py", "ts", "start", 'style="font-size:13px"')
          + _t(520, 218, "내 PC 에서 실행", "ts", "start", 'style="font-size:13px"')
          + f'<rect x="516" y="242" width="238" height="38" rx="9" fill="#FFF3E6" stroke="{O}" stroke-width="2"/>'
          + _t(635, 261, "yield_of(file)", "tm", "middle", mono(15, "#EF6C00")))
    # data/
    s += (f'<rect x="880" y="110" width="280" height="200" rx="16" fill="{W}" stroke="#C9CFD8" stroke-width="2"/>'
          + _t(900, 140, "data/", "tt", "start"))
    files = [n for n, *_ in FOUR]
    for i, f in enumerate(files):
        y = 176 + i * 32
        if f.endswith("W07"):
            s += f'<rect x="892" y="{y - 14}" width="256" height="28" rx="6" fill="#FFF3E6" stroke="{O}" stroke-width="2" {d.show(pc(5.8))}/>'
        s += _t(904, y, f + ".xlsx", "tm", "start", mono(14, N))
    # 화살표 · ① ~ ④
    arrows = [(1.0, "M344 138 H494", "① 도구 목록 요청", 420, 122, K),
              (1.8, "M496 174 H346", "도구 이름 · 설명 · 입력", 420, 192, K),
              (4.6, "M344 252 H494", "② yield_of(file=W07)", 420, 236, O),
              (5.8, "M774 210 H874", "③ 엑셀 읽기 · 계산", 825, 194, O),
              (7.0, "M496 290 H346", f"④ {rows}행 · 합격 {ok} · {rate:.2f}%", 420, 310, OK)]
    for t, path, lab_, lx, ly, c in arrows:
        mk = {K: "k", O: "o", OK: "g"}[c]
        s += (f'<g {d.show(pc(t))}><path d="{path}" stroke="{c}" stroke-width="3" marker-end="url(#{d.id(mk)})"/>'
              + _t(lx, ly, lab_, "tn", "middle", f'style="font-size:13.5px;fill:{c if c != K else N}"') + "</g>")
    return d.svg(1160, 430, s)


HOOK_CFG = ('{\n  "hooks": {\n    "PreToolUse": [{\n      "matcher": "Edit|Write|Bash",\n'
            '      "hooks": [{ "type": "command",\n                  "command": "python3 .claude/hooks/guard.py" }]\n    }]\n  }\n}')
AGENT_MD = ("---\nname: file-summary\ndescription: 엑셀 파일 하나를 요약할 때. 파일은 고치지 않음\ntools: Read, Bash\n---\n"
            "파일 하나만 읽고 행 수 · 합격(상품) 수 · 비율을 계산한다.\n보고 형식: 파일 · 행 수 · 합격 수 · 비율 한 줄")


def slides():
    out = [order(no) for no in PROMPTS]
    out += [
        light("Hook 차단과 Agent 병렬", hook_agent(), T),
        light("Hook 설정 · settings.json", code(".claude/settings.json · hooks 부분 예", esc(HOOK_CFG))
              + flow([("도구 호출 직전", "Edit · Write · Bash"), ("guard.py 검사", "data/ 에 쓰는가"),
                      ("exit 2 · 차단", "이유를 Claude 에게"), ("exit 0 · 통과", "그대로 실행")], hl=2)
              + src(CC_HOOK), T),
        light("Sub Agent 정의 파일", two(
            code(".claude/agents/file-summary.md · 예", esc(AGENT_MD)),
            viz2.tiles([("name · description", "이름 · Claude 가 맡길 때 고르는 기준"), ("tools", "쓸 수 있는 도구 · 줄이면 권한도 줄어듦"),
                        ("본문", "할 일 · 보고 형식"), ("자기 컨텍스트", "결과만 메인 대화에 전달")], 1))
              + src(CC_SUB), T),
        light("병렬로 맡기기", parallel() + src(CC_SUB, CC_BP), T),
        lab("22-1", "원본 보호 Hook", T, "data/ 원본을 고치거나 지우는 도구 호출을 Hook 으로 막고, 실제로 막히는지 확인한다",
            ["Hook 만들기 요청", "설정 · 스크립트 확인", "data/ 에 저장 요청 → 막힘", "output/ 에 저장 → 됨"],
            ["data/ 저장 요청 → 차단 · 이유 한 줄", "output/ 새 파일 저장", "data/apple_A07.xlsx 그대로"], files=".claude/settings.json · .claude/hooks/"),
        lab("22-2", "Sub Agent 병렬 요약", T, "엑셀 하나를 요약하는 Sub Agent 를 만들고 data/ 의 엑셀 4개를 동시에 맡겨 표 하나로 모은다",
            ["file-summary Agent 만들기", "Agent 파일 확인", "엑셀 4개 동시에 맡기기", "표 하나로 모으기"],
            [" · ".join(f"{n.split('_')[-1]} {_pct(p)}" for n, _, _, p in FOUR[:2]), " · ".join(f"{n.split('_')[-1]} {_pct(p)}" for n, _, _, p in FOUR[2:]),
             "output/ 요약 표"], files=".claude/agents/file-summary.md"),
        light("MCP 도구 흐름", mcp_flow() + src(CC_MCP), T),
        light("도구 코드 · .mcp.json", code("tools/yield_server.py · 핵심 부분", esc(_tool_code()))
              + viz2.tiles([(".mcp.json", _mcp_json()), ("docstring", "도구 설명 · Claude 가 고르는 기준"),
                            ("/mcp", "연결 상태 · 서버별 도구 개수")], 3) + src(CC_MCP), T),
        lab("22-3", "수율 도구 만들기", T, "data/ 엑셀의 수율을 계산하는 MCP 도구를 만들어 연결하고, 그 도구로 엑셀 4개의 수율을 받는다",
            ["수율 도구 요청", "다시 열기 · 승인 · /mcp 확인", "도구로 엑셀 4개 수율 요청", "답 위 yield_of 호출 확인"],
            ["tools/yield_server.py · .mcp.json",
             " · ".join(f"{n.split('_')[-1]} {_pct(p)}" for n, _, _, p in FOUR[:2]),
             " · ".join(f"{n.split('_')[-1]} {_pct(p)}" for n, _, _, p in FOUR[2:])], files="data/ 엑셀 4개"),
    ]
    return out


CSS = r"""
  .plbs{display:flex; flex-direction:column; gap:12px; margin:2px 0 16px;}
  .plbr{display:grid; grid-template-columns:40px 190px 1fr; align-items:center; gap:16px; opacity:0; animation:plbIn .4s var(--d) forwards;}
  .plbr em{width:38px; height:38px; border-radius:50%; background:#16233A; color:#fff; font-style:normal; font-weight:800; font-size:18px;
    display:flex; align-items:center; justify-content:center;}
  .plbr b{font-size:19px; color:#16233A; line-height:1.3; word-break:keep-all;}
  .plbr q{quotes:"「" "」"; display:block; background:#FFF7EE; border:2px solid #F2C58F; border-radius:14px; padding:12px 18px;
    font-size:21px; font-weight:700; color:#16233A; line-height:1.35; word-break:keep-all;}
  .plbr q.nb{quotes:none; background:#F4F6F9; border-color:#D9DDE3; font-weight:600; color:#3A4657; font-size:19px;}
  .plbk{display:flex; gap:12px; align-items:center; flex-wrap:wrap;}
  .plbk b{font-size:16px; color:#C76A12; margin-right:4px;}
  .plbk span{background:#E8F5E9; color:#2E7D32; border-radius:999px; padding:6px 16px; font-size:17px; font-weight:700;}
  @keyframes plbIn{from{opacity:0; transform:translateY(8px)} to{opacity:1; transform:none}}
  @media print{.plbr{opacity:1; animation:none}}
"""
