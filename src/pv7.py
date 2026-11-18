"""7교시 애니메이션 — 새 파일 하나 → 명령 하나 · 원인 후보 좁히기 · 정기 실행. anim._D · 접두어 p7a · p7b · p7c."""
from anim import G, K, N, O, OK, R, S, W, _D, _box, _dot, _t

MO = "#FFF3E6"


def new_file(before, after):
    """W26 파일이 data/raw 에 들어옴 → run_all.py → 단계가 차례로 켜짐 → KPI 숫자가 바뀜. 14초.
    before · after = output/w26_rerun.json 의 값."""
    d = _D("p7a", 14)
    s = ""
    # 폴더
    s += f'<rect x="20" y="70" width="230" height="250" rx="14" fill="#F4F6F9" stroke="{G}" stroke-width="2"/>' + _t(135, 96, "data/raw/", "tm")
    for i, w in enumerate(("W23", "W24", "W25")):
        s += f'<rect x="44" y="{116 + i * 44}" width="182" height="36" rx="8" fill="{W}" stroke="{K}" stroke-width="1.5"/>' + _t(135, 134 + i * 44, f"wafer_test_{w}.csv", "tm", extra='style="font-size:13px"')
    s += (f'<g {d.a([(0, "transform:translate(0px,-120px);opacity:0"), (4, "transform:translate(0px,-120px);opacity:1"), (14, "transform:translate(0px,0px);opacity:1"), (100, "transform:translate(0px,0px);opacity:1")])}>'
          f'<rect x="44" y="248" width="182" height="36" rx="8" fill="{MO}" stroke="{O}" stroke-width="2.5"/>' + _t(135, 266, "wafer_test_W26.csv", "tm", extra=f'style="font-size:13px;fill:{O}"') + "</g>")
    s += f'<g {d.show(14)}>' + _t(135, 344, "새 파일 하나", "to") + "</g>"
    # 명령
    s += (f'<g {d.show(20)}><rect x="290" y="160" width="250" height="60" rx="30" fill="{N}"/>'
          + _t(415, 190, "python scripts/run_all.py", "tw", extra='style="font-family:var(--mono,monospace);font-size:14px"') + "</g>")
    s += f'<g {d.show(19)}><path d="M254 190 H286" stroke="{G}" stroke-width="3" marker-end="url(#{d.id("k")})"/></g>'
    for i, (h, sub) in enumerate((("정제", "clean"), ("적재", "DuckDB"), ("집계", "SQL 뷰"), ("그리기", "dashboard.html"))):
        x = 580 + i * 145
        s += f'<g {d.show(28 + i * 8)}>' + _box(x, 150, 130, 80, h, sub, fill=MO if i == 3 else W, stroke=O if i == 3 else K) + "</g>"
        if i:
            s += f'<g {d.show(27 + i * 8)}><path d="M{x - 14} 190 H{x - 2}" stroke="{G}" stroke-width="3" marker-end="url(#{d.id("k")})"/></g>'
    s += f'<g {d.show(26)}><path d="M544 190 H576" stroke="{G}" stroke-width="3" marker-end="url(#{d.id("k")})"/></g>'
    # KPI 전 → 후
    k = [("웨이퍼", f"{before['wafers']}장", f"{after['wafers']}장"), ("LOT 수율", f"{before['lot_yield']}%", f"{after['lot_yield']}%"),
         ("목표 미달", f"{before['below_target']}장", f"{after['below_target']}장")]
    for i, (lab, b, a) in enumerate(k):
        x = 300 + i * 280
        s += f'<rect x="{x}" y="280" width="250" height="110" rx="14" fill="{W}" stroke="{G}" stroke-width="2"/>' + _t(x + 125, 306, lab, "ts")
        s += f'<g {d.a([(0, "opacity:1"), (62, "opacity:1"), (66, "opacity:0"), (100, "opacity:0")])}>' + _t(x + 125, 350, b, "tt", extra='style="font-size:30px"') + "</g>"
        s += f'<g {d.show(64)}>' + _t(x + 125, 350, a, "tt", extra=f'style="font-size:30px;fill:{O}"') + "</g>"
    s += f'<g {d.show(80)}>' + _t(700, 420, "사람이 한 일 · 파일 넣기 + 명령 한 줄", "tn", extra='style="font-size:17px"') + "</g>"
    return d.svg(1160, 440, s)


def narrow(lot, eqp, zone, fails):
    """원인 후보 좁히기 — LOT → 설비 → 존 → 불량 유형. 단계마다 남는 범위가 줄어듦. 14초.
    lot = LOT 수율 · eqp = [(설비, 수율)] · zone = [(설비, edge 수율)] · fails = [(유형, ETCH_03, 나머지 평균)]."""
    d = _D("p7b", 14)
    s = ""
    steps = [("LOT", f"수율 {lot}% · 웨이퍼 25장"), ("설비", " · ".join(f"{e} {y}%" for e, y in eqp)),
             ("존 (edge)", " · ".join(f"{e} {y}%" for e, y in zone)), ("불량 유형", " · ".join(f"{t} {a} vs {b}" for t, a, b in fails))]
    for i, (h, txt) in enumerate(steps):
        y = 30 + i * 100
        w = 1100 - i * 150
        x = (1160 - w) / 2
        last = i == 3
        s += (f'<g {d.show(4 + i * 20)}><rect x="{x}" y="{y}" width="{w}" height="80" rx="14" fill="{MO if last else W}" stroke="{O if last else K}" stroke-width="{3 if last else 2.5}"/>'
              + _t(x + 24, y + 28, h, "to", "start", 'style="font-size:16px"') + _t(580, y + 54, txt, "tt", extra='style="font-size:18px"') + "</g>")
    s += f'<g {d.show(88)}>' + _t(580, 440, "남은 후보 · ETCH_03 가장자리의 누설전류 · 문턱전압 이탈", "tt", extra=f'style="fill:{O};font-size:19px"') + "</g>"
    return d.svg(1160, 460, s)


def schedule():
    """정기 실행 — 매일 아침 run_all → 검증 통과면 대시보드 갱신 · 실패면 claude -p 가 기록을 읽고 요약 → 담당자 확인. 14초."""
    d = _D("p7c", 14)
    s = ""
    s += f'<g {d.show(1)}><rect x="20" y="170" width="170" height="70" rx="35" fill="{N}"/>' + _t(105, 205, "매일 아침", "tw", extra='style="font-size:18px"') + "</g>"
    s += f'<g {d.show(8)}>' + _box(240, 160, 220, 90, "run_all.py", "정제 · 적재 · 집계", fill=W, stroke=K) + "</g>"
    s += f'<g {d.show(7)}><path d="M194 205 H236" stroke="{G}" stroke-width="3" marker-end="url(#{d.id("k")})"/></g>'
    s += (f'<g {d.show(18)}><path d="M510 160 L580 205 L510 250 L440 205 Z" transform="translate(70 0)" fill="{W}" stroke="{O}" stroke-width="3"/>'
          + _t(580, 205, "검증 통과?", "tn", extra='style="font-size:15px"') + "</g>")
    s += f'<g {d.show(17)}><path d="M464 205 H504" stroke="{G}" stroke-width="3" marker-end="url(#{d.id("k")})"/></g>'
    s += (f'<g {d.show(30)}><path d="M652 205 H720" stroke="{OK}" stroke-width="3" marker-end="url(#{d.id("g")})"/>' + _t(686, 190, "예", "tn", extra=f'style="fill:{OK}"')
          + _box(726, 160, 400, 90, "dashboard.html 갱신", "출근 전에 새 숫자", fill="#E8F5E9", stroke=OK) + "</g>")
    s += (f'<g {d.show(48)}><path d="M580 252 V330" stroke="{R}" stroke-width="3" marker-end="url(#{d.id("r")})"/>' + _t(596, 290, "아니오", "tn", "start", f'style="fill:{R}"')
          + f'<rect x="380" y="336" width="400" height="90" rx="14" fill="#FDECEA" stroke="{R}" stroke-width="2.5"/>'
          + _t(580, 368, 'claude -p "pipeline_log 요약"', "tm", extra=f'style="fill:{R};font-size:15px"') + _t(580, 400, "실패한 파일 · 이유를 글로 정리", "ts") + "</g>")
    s += (f'<g {d.show(66)}><path d="M784 381 H836" stroke="{G}" stroke-width="3" marker-end="url(#{d.id("k")})"/>'
          + _box(842, 336, 284, 90, "담당자 확인", "고칠지 · 다시 측정할지", fill=W, stroke=K) + "</g>")
    s += f'<g {d.show(80)}>' + _t(580, 60, "사람이 정하는 것 · 검증 규칙 · 판정 기준 · 최종 판단", "tt", extra='style="font-size:19px"') + "</g>"
    return d.svg(1160, 450, s)
