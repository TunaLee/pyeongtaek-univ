"""2교시 애니메이션 — 원시 파일 속 문제 · 정제 단계 · 단위 함정 · 검증 관문. anim._D · 접두어 p2a~p2d."""
from anim import G, K, N, O, OK, R, S, W, _D, _box, _t

MO = "#FFF3E6"
RB = "#FDECEA"
GB = "#E8F5E9"


def raw_issues(rows05, rows11, rows19):
    """원시 파일 세 장 · 문제 칸이 차례로 빨갛게. rowsXX = [(die_x, die_y, vth, ioff)] 앞 5줄. 12초."""
    d = _D("p2a", 12)
    s = ""
    panels = [("wafer_test_W05.csv", rows05, "같은 다이 두 번", "중복 12행", "dup"),
              ("wafer_test_W11.csv", rows11, "vth_v 가 460 · 431", "단위 mV", "unit"),
              ("wafer_test_W19.csv", rows19, "ioff_na 빈칸", "결측 9칸", "na")]
    for p, (name, rows, why, tagt, kind) in enumerate(panels):
        x = 10 + p * 385
        s += f'<g {d.show(1 + p * 4)}><rect x="{x}" y="20" width="365" height="300" rx="14" fill="{W}" stroke="{G}" stroke-width="2"/>'
        s += _t(x + 182, 46, name, "tm", extra='style="font-size:15px"')
        s += f'<rect x="{x + 12}" y="62" width="341" height="32" rx="6" fill="{K}"/>'
        for j, h in enumerate(("die_x", "die_y", "vth_v", "ioff_na")):
            s += _t(x + 54 + j * 85, 78, h, "tw", extra='style="font-family:var(--mono,monospace);font-size:13px"')
        for i, r in enumerate(rows):
            y = 102 + i * 38
            s += f'<rect x="{x + 12}" y="{y}" width="341" height="32" rx="6" fill="#F7F8FA"/>'
            for j, v in enumerate(r):
                s += _t(x + 54 + j * 85, y + 16, v if v != "" else "·", "tm", extra='style="font-size:14px"')
        s += "</g>"
        t = 34 + p * 18
        if kind == "dup":
            for i in (1, 3):
                y = 102 + i * 38
                s += f'<rect x="{x + 12}" y="{y}" width="341" height="32" rx="6" fill="none" stroke="{R}" stroke-width="3" {d.show(t)}/>'
        elif kind == "unit":
            for i in range(len(rows)):
                y = 102 + i * 38
                s += f'<rect x="{x + 182}" y="{y}" width="80" height="32" rx="6" fill="none" stroke="{R}" stroke-width="3" {d.show(t + i)}/>'
        else:
            for i, r in enumerate(rows):
                if r[3] == "":
                    y = 102 + i * 38
                    s += f'<rect x="{x + 267}" y="{y}" width="80" height="32" rx="6" fill="none" stroke="{R}" stroke-width="3" {d.show(t)}/>'
        s += (f'<g {d.show(t + 6)}><rect x="{x}" y="336" width="365" height="70" rx="12" fill="{RB}" stroke="{R}" stroke-width="2.5"/>'
              + _t(x + 182, 360, tagt, "tt", extra=f'style="fill:{R}"') + _t(x + 182, 386, why, "ts") + "</g>")
    return d.svg(1160, 420, s)


def clean_steps(n_raw, n_dup, n_na, n_clean):
    """원시 → 중복 제거 → 단위 통일 → 결측 표시 → 재판정 → 검증 → 정제본. 행 수가 바뀌는 곳에 숫자. 14초."""
    d = _D("p2b", 14)
    st = [("원시 파일", f"W05 {n_raw}행"), ("중복 제거", f"−{n_dup}행"), ("단위 통일", "mV → V"),
          ("결측 표시", f"{n_na}칸 → RETEST"), ("다시 판정", "spec.csv 기준"), ("검증", "규칙 5개")]
    s = ""
    for i, (h, sub) in enumerate(st):
        x = 10 + i * 190
        hl = i == 5
        s += f'<g {d.show(3 + i * 11)}>' + _box(x, 70, 166, 100, h, sub, fill=MO if hl else W, stroke=O if hl else K) + "</g>"
        if i:
            s += f'<g {d.show(2 + i * 11)}><path d="M{x - 22} 120 H{x - 4}" stroke="{G}" stroke-width="3" marker-end="url(#{d.id("k")})"/></g>'
    s += f'<g {d.show(70)}><path d="M1093 174 V236" stroke="{OK}" stroke-width="3.5" marker-end="url(#{d.id("g")})"/></g>'
    s += (f'<g {d.show(74)}><rect x="830" y="244" width="320" height="96" rx="14" fill="{GB}" stroke="{OK}" stroke-width="3"/>'
          + _t(990, 280, "정제본", "tt", extra=f'style="fill:{OK}"') + _t(990, 310, f"{n_clean}행 · 다이 좌표 하나에 한 줄", "tn") + "</g>")
    s += (f'<g {d.show(80)}><rect x="10" y="244" width="780" height="96" rx="14" fill="{W}" stroke="{G}" stroke-width="2"/>'
          + _t(400, 280, "원시 파일은 그대로 · 정제본은 output/clean/ 에 새로 저장", "tt", extra='style="font-size:18px"')
          + _t(400, 310, "같은 스크립트를 다시 돌리면 같은 결과", "ts") + "</g>")
    return d.svg(1160, 360, s)


def unit_trap(vth_raw, n_vth_fail, y_fixed):
    """W11 을 단위 확인 없이 판정 → 전부 문턱전압 이탈 · 수율 0% / 단위를 V 로 고친 뒤 → 정상 수율. 12초."""
    d = _D("p2c", 12)
    s = ""
    # 스펙 축
    s += _t(290, 40, "스펙 vth_v 0.38~0.52 V", "tn")
    s += (f'<g {d.show(2)}><rect x="40" y="70" width="500" height="120" rx="14" fill="{W}" stroke="{K}" stroke-width="2.5"/>'
          + _t(290, 104, f"원시 값 vth_v = {vth_raw}", "tm", extra='style="font-size:19px"')
          + _t(290, 140, "0.38~0.52 와 비교 → 범위 밖", "ts") + "</g>")
    s += f'<g {d.show(14)}><path d="M290 194 V236" stroke="{R}" stroke-width="3.5" marker-end="url(#{d.id("r")})"/></g>'
    s += (f'<g {d.show(18)}><rect x="40" y="244" width="500" height="130" rx="14" fill="{RB}" stroke="{R}" stroke-width="3"/>'
          + _t(290, 280, f"문턱전압 이탈 {n_vth_fail}개", "tt", extra=f'style="fill:{R};font-size:22px"')
          + _t(290, 318, "수율 0%", "tt", extra=f'style="fill:{R};font-size:30px"') + "</g>")
    # 고친 쪽
    s += (f'<g {d.show(42)}><rect x="620" y="70" width="500" height="120" rx="14" fill="{W}" stroke="{K}" stroke-width="2.5"/>'
          + _t(870, 104, f"{vth_raw} ÷ 1000 = {vth_raw / 1000:.3f} V", "tm", extra='style="font-size:19px"')
          + _t(870, 140, "중앙값이 10 보다 크면 mV 로 보고 변환", "ts") + "</g>")
    s += f'<g {d.show(54)}><path d="M870 194 V236" stroke="{OK}" stroke-width="3.5" marker-end="url(#{d.id("g")})"/></g>'
    s += (f'<g {d.show(58)}><rect x="620" y="244" width="500" height="130" rx="14" fill="{GB}" stroke="{OK}" stroke-width="3"/>'
          + _t(870, 280, "단위 통일 후 다시 판정", "tt", extra=f'style="fill:{OK};font-size:20px"')
          + _t(870, 318, f"수율 {y_fixed:.2f}%", "tt", extra=f'style="fill:{OK};font-size:30px"') + "</g>")
    s += f'<line x1="580" y1="60" x2="580" y2="380" stroke="{G}" stroke-width="2" stroke-dasharray="6 6" {d.show(40)}/>'
    return d.svg(1160, 400, s)


def gate(rules):
    """검증 규칙이 하나씩 통과(✓) → 관문 열림 → 다음 단계. 규칙 하나가 실패하면 멈춤(아래 줄). 12초."""
    d = _D("p2d", 12)
    s = ""
    for i, r in enumerate(rules):
        y = 30 + i * 62
        s += (f'<g {d.show(2 + i * 8)}><rect x="20" y="{y}" width="560" height="50" rx="12" fill="{W}" stroke="{K}" stroke-width="2"/>'
              + _t(44, y + 26, f"assert  {r}", "tm", "start", 'style="font-size:15px"') + "</g>")
        s += (f'<g {d.show(6 + i * 8)}><circle cx="548" cy="{y + 25}" r="15" fill="{OK}"/>'
              + f'<path d="M541 {y + 25} l5 6 l10 -12" fill="none" stroke="{W}" stroke-width="3.5" stroke-linecap="round"/>' + "</g>")
    yb = 30 + len(rules) * 62
    s += f'<g {d.show(46)}><path d="M590 {30 + len(rules) * 31} H700" stroke="{OK}" stroke-width="3.5" marker-end="url(#{d.id("g")})"/></g>'
    s += (f'<g {d.show(50)}><rect x="706" y="{30 + len(rules) * 31 - 50}" width="430" height="100" rx="14" fill="{GB}" stroke="{OK}" stroke-width="3"/>'
          + _t(921, 30 + len(rules) * 31 - 14, "통과 → 정제본 저장", "tt", extra=f'style="fill:{OK}"')
          + _t(921, 30 + len(rules) * 31 + 16, "qc_W11.md 에 결과 기록", "ts") + "</g>")
    s += (f'<g {d.show(70)}><rect x="20" y="{yb + 10}" width="1116" height="56" rx="12" fill="{RB}" stroke="{R}" stroke-width="2.5"/>'
          + _t(578, yb + 39, "하나라도 False → AssertionError · 그 파일은 적재하지 않고 멈춤", "tt", extra=f'style="fill:{R};font-size:18px"') + "</g>")
    return d.svg(1160, yb + 80, s)
