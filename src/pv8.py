"""8교시 애니메이션 — 분석 요약 네 칸 조립 · 날짜와 설비가 겹칠 때. anim._D · 접두어 p8a · p8b."""
from anim import G, K, N, O, OK, R, S, W, _D, _box, _t

MO = "#FFF3E6"


def summary(blocks):
    """분석 요약 네 칸이 위에서부터 차례로 채워짐 · 칸마다 근거 숫자 한 줄. blocks = [(칸, 한 줄)] 4개. 12초."""
    d = _D("p8a", 12)
    s = _t(580, 24, "analysis_summary.md", "tm", extra='style="font-size:16px"')
    for i, (h, line) in enumerate(blocks):
        y = 50 + i * 96
        col = O if i == 1 else K
        s += (f'<g {d.show(4 + i * 20)}><rect x="40" y="{y}" width="1080" height="80" rx="14" fill="{MO if i == 1 else W}" stroke="{col}" stroke-width="2.5"/>'
              f'<rect x="40" y="{y}" width="170" height="80" rx="14" fill="{col}"/>'
              + _t(125, y + 40, h, "tw", extra='style="font-size:20px"') + _t(240, y + 40, line, "tn", "start", 'style="font-size:17px"') + "</g>")
    return d.svg(1160, 440, s)


def confound(rows):
    """날짜별 수율만 보면 11-07 이 낮다 → 같은 날(11-06) 안에서 설비별로 나누면 ETCH_03 만 낮다. 14초.
    rows = [(날짜, 수율, 설비 목록)] · 마지막 두 단계 숫자는 같은 날 웨이퍼별 수율."""
    d = _D("p8b", 14)
    s = _t(300, 24, "① 날짜별 수율", "to", extra='style="font-size:17px"')
    mx, mn = 96, 84
    for i, (day, y, eq) in enumerate(rows):
        x = 40 + i * 106
        h = (y - mn) / (mx - mn) * 220
        bad = y < 90
        s += (f'<g {d.show(2 + i * 4)}><rect x="{x}" y="{280 - h:.0f}" width="80" height="{h:.0f}" rx="6" fill="{R if bad else K}"/>'
              + _t(x + 40, 268 - h, f"{y}%", "tn", extra='style="font-size:14px"') + _t(x + 40, 300, day[5:], "tm", extra='style="font-size:13px"')
              + _t(x + 40, 324, eq.replace("ETCH_", "E"), "ts", extra='style="font-size:12px"') + "</g>")
    s += f'<line x1="30" y1="{280 - (90 - mn) / (mx - mn) * 220:.0f}" x2="580" y2="{280 - (90 - mn) / (mx - mn) * 220:.0f}" stroke="{R}" stroke-dasharray="5 4" stroke-width="2"/>'
    s += f'<g {d.show(28)}>' + _t(300, 370, "날짜 · 설비가 겹침", "tt", extra=f'style="fill:{R};font-size:18px"') + "</g>"
    s += f'<line x1="610" y1="20" x2="610" y2="420" stroke="{G}" stroke-width="2" stroke-dasharray="6 6"/>'
    return d, s


def confound_svg(rows, same_day):
    """confound() + 오른쪽 · 같은 날 안에서 설비별로 나눈 웨이퍼 수율. same_day = [(웨이퍼, 설비, 수율)]."""
    d, s = confound(rows)
    s += f'<g {d.show(40)}>' + _t(880, 24, "② 같은 날 2026-11-06 · 설비별", "to", extra='style="font-size:17px"') + "</g>"
    for i, (w, e, y) in enumerate(same_day):
        yy = 60 + i * 60
        bad = y < 90
        wd = (y - 80) / 16 * 330
        s += (f'<g {d.show(46 + i * 6)}>' + _t(640, yy + 22, f"{w}", "tn", "start") + _t(700, yy + 22, e, "ts", "start", 'style="font-size:13px"')
              + f'<rect x="780" y="{yy + 6}" width="{wd:.0f}" height="32" rx="6" fill="{R if bad else OK}"/>' + _t(790 + wd, yy + 22, f"{y}%", "tn", "start") + "</g>")
    s += f'<g {d.show(84)}>' + _t(880, 400, "같은 날에도 ETCH_03 만 낮음 → 설비 쪽", "tt", extra=f'style="fill:{OK};font-size:18px"') + "</g>"
    return d.svg(1160, 430, s)
