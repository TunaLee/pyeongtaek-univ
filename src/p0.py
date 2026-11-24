"""개요 — 데이터와 데이터 분석. 1교시 앞에 붙는다 (build.py).

도입(데이터의 정의 · 저장 형식의 변화 · 엑셀 · CSV · DB)
→ 설명(AI 이전의 처리 · 같은 질문 세 도구 · 분석 요청 경로 · 데이터→결정 · 분석 종류 · 흐름 · 분석과 엔지니어링)
→ 적용(사과 선별 데이터 · 행 · 열 · 변수 · 상품률).
숫자는 practice CSV · labs/ref.json 에서 계산한다.
"""
import pandas as pd

import pgen
import sk
import viz2
from deck import divider, light
from hx import code, esc
from pkit import REF, chat
from stats_hx import big

GEN = REF["general"]
P = pgen.P
TAG = "개요"

CSS = """
  .p0fm{display:grid; grid-template-columns:1fr 34px 1fr 34px 1fr 34px 1fr; align-items:start; margin-top:4px;}
  .p0fm > i{font-style:normal; color:#F28C28; font-weight:900; font-size:26px; text-align:center; margin-top:92px;}
  .p0f{display:flex; flex-direction:column; gap:6px; opacity:0; animation:p0In .5s var(--d) forwards;}
  .p0f > b{font-size:21px; color:#16233A; margin-top:8px;}
  .p0f > span{font-size:15px; color:#6B7785;}
  .p0v{height:200px; border-radius:12px; overflow:hidden; border:1.5px solid #D9DDE3; background:#fff; display:flex; flex-direction:column;}
  .p0v img{width:100%; height:100%; object-fit:cover;}
  .p0xl table{border-collapse:collapse; width:100%; font-size:12.5px; font-family:var(--sans);}
  .p0xl .bar{background:#1D6F42; color:#fff; font-size:11px; font-weight:700; padding:5px 8px;}
  .p0xl th{background:#F1F3F4; color:#5F6368; font-weight:600; border:1px solid #DADCE0; padding:3px 4px; font-size:11px;}
  .p0xl td{border:1px solid #E3E5E8; padding:5px 5px; color:#202124; white-space:nowrap;}
  .p0xl td.sel{outline:2px solid #1D6F42; outline-offset:-2px;}
  .p0csv{background:#1E1E2E;}
  .p0csv pre{margin:0; padding:14px 12px; color:#E6E6E6; font-family:var(--mono); font-size:11.5px; line-height:1.75; white-space:pre;}
  .p0db{background:#F7F9FC; padding:12px; gap:8px;}
  .p0db .q{font-family:var(--mono); font-size:11.5px; color:#1F3A5F; background:#fff; border:1px solid #D9DDE3; border-radius:6px; padding:7px 8px; line-height:1.5;}
  .p0db table{border-collapse:collapse; font-size:12.5px; width:100%;}
  .p0db th{background:#1F3A5F; color:#fff; font-weight:700; padding:4px 8px; text-align:left;}
  .p0db td{border-bottom:1px solid #E1E5EB; padding:4px 8px; background:#fff;}
  .p0tl{display:grid; grid-template-columns:minmax(0,1.2fr) minmax(0,1.45fr) minmax(0,1fr); gap:18px;}
  .p0t{border:1.5px solid #E1E5EB; border-top:5px solid #1F3A5F; border-radius:14px; background:#fff; padding:14px 18px; display:flex; flex-direction:column; gap:10px; opacity:0; animation:p0In .5s var(--d) forwards;}
  .p0t.on{border-top-color:#F28C28; background:#FFF8F1;}
  .p0t > b{font-size:21px; color:#16233A;}
  .p0t .code{margin:0; max-width:100%;}
  .p0t .code pre, .p0t .code code{font-size:12.5px !important; white-space:pre;}
  .p0t .v1chat{margin:0;}
  .p0t ol code{white-space:nowrap;}
  .p0t ol{margin:0; padding-left:20px; font-size:15px; color:#3B4756; line-height:1.7;}
  .p0t ol code{font-family:var(--mono); font-size:13px; background:#F4F6F9; border-radius:4px; padding:1px 5px;}
  .p0t .r{margin-top:auto; font-size:26px; font-weight:800; color:#E07A12; display:flex; align-items:baseline; justify-content:space-between; gap:8px;}
  .p0t .r small{font-size:15px; font-weight:700; color:#3B4756;}
  .p0tq{display:flex; align-items:baseline; gap:14px; margin-bottom:14px; padding:10px 18px; border-left:5px solid #F28C28; background:#FFF8F1; border-radius:8px; font-size:20px; font-weight:700; color:#16233A; opacity:0; animation:p0In .5s 0s forwards;}
  .p0tq b{font-size:15px; color:#E07A12;}
  .p0tq span{margin-left:auto; font-size:15px; font-weight:600; color:#6B7785;}
  .p0ph{display:inline-flex; gap:3px; margin-left:4px;}
  .p0ph i{font-style:normal; font-family:var(--sans); font-size:11px; font-weight:700; letter-spacing:0; padding:3px 8px; border-radius:6px; background:#EEF1F5; color:#9AA3AF;}
  .p0ph i.on{background:#F28C28; color:#fff;}
  .p0ev{display:flex; flex-direction:column; gap:12px;}
  .p0ev .code pre, .p0ev .code code{font-size:14px !important; line-height:1.6;}
  .p0er{display:grid; grid-template-columns:170px minmax(0,1fr); gap:18px; align-items:center; opacity:0; animation:p0In .5s var(--d) forwards;}
  .p0er > div:first-child b{display:block; font-size:24px; color:#16233A;}
  .p0er > div:first-child span{display:block; font-size:14.5px; color:#6B7785; line-height:1.5; margin-top:4px;}
  .p0er.on > div:first-child b{color:#E07A12;}
  .p0x{border:1.5px solid #D9DDE3; border-radius:10px; overflow:hidden; background:#fff; font-family:var(--sans);}
  .p0x .bar{background:#1D6F42; color:#fff; font-size:12px; font-weight:700; padding:6px 12px;}
  .p0x .fx{display:flex; gap:10px; align-items:center; font-size:12.5px; border-bottom:1px solid #DADCE0; padding:4px 10px; color:#3C4043;}
  .p0x .fx i{font-style:italic; color:#5F6368; border-right:1px solid #DADCE0; padding-right:10px;}
  .p0x .fx em{font-style:normal; font-weight:700; width:28px;}
  .p0x table{border-collapse:collapse; width:100%; font-size:13px;}
  .p0x th{background:#F1F3F4; color:#5F6368; font-weight:600; border:1px solid #DADCE0; padding:3px 6px; font-size:11.5px;}
  .p0x td{border:1px solid #E3E5E8; padding:5px 8px; color:#202124; white-space:nowrap;}
  .p0x td.n{text-align:right;}
  .p0x tr.h td{font-weight:700; background:#E8F0E9;}
  .p0x td.sel{outline:2px solid #1D6F42; outline-offset:-2px;}
  .p0x .tab{font-size:11.5px; color:#1D6F42; font-weight:700; padding:4px 12px; border-top:1px solid #DADCE0; background:#F8F9FA;}
  .p0er.on .code{border:2px solid #F28C28;}
  .p0tb{display:grid; grid-template-columns:minmax(0,1.3fr) minmax(0,1fr); gap:28px; align-items:center;}
  .p0tb .t{border:1.5px solid #D9DDE3; border-radius:12px; overflow:hidden; background:#fff;}
  .p0tb .t .nm{background:#1F3A5F; color:#fff; font-family:var(--mono); font-size:13px; font-weight:700; padding:7px 14px;}
  .p0tb table{border-collapse:collapse; width:100%; font-size:15px;}
  .p0tb th{background:#F4F6F9; color:#1F3A5F; font-family:var(--mono); font-size:13.5px; text-align:left; padding:8px 12px; border-bottom:1.5px solid #D9DDE3;}
  .p0tb td{padding:8px 12px; border-bottom:1px solid #EEF1F5; color:#16233A;}
  .p0tb td.more{color:#9AA3AF; font-size:13px;}
  .p0tb .k{color:#E07A12;}
  .p0tb tr.row td{animation:p0Row .5s 1s forwards;}
  .p0tb .col{animation:p0Col .5s 3s forwards;}
  .p0tb td.cell{animation:p0Cell .5s 5s forwards;}
  @keyframes p0Row{to{background:#FFF3E6;}}
  @keyframes p0Col{to{background:#E6EEF8;}}
  @keyframes p0Cell{to{background:#F28C28; color:#fff; font-weight:800;}}
  .p0lg{display:flex; flex-direction:column; gap:10px;}
  .p0lg div{display:grid; grid-template-columns:150px 1fr; gap:12px; align-items:center; border-radius:10px; padding:10px 14px; background:#fff; border:1.5px solid #E1E5EB; opacity:0; animation:p0In .5s var(--d) forwards;}
  .p0lg b{font-size:17px; color:#16233A;} .p0lg b small{display:block; font-size:12px; color:#6B7785; font-weight:600; font-family:var(--mono);}
  .p0lg span{font-size:15px; color:#3B4756;}
  .p0lg i{display:inline-block; width:12px; height:12px; border-radius:3px; margin-right:6px; vertical-align:-1px;}
  @media print{.p0tb tr.row td{background:#FFF3E6} .p0tb .col{background:#E6EEF8} .p0tb td.cell{background:#F28C28;color:#fff} .p0lg div{animation:none;opacity:1}}
  @keyframes p0In{from{opacity:0; transform:translateY(8px)} to{opacity:1; transform:none}}
  @media print{.p0f,.p0t{animation:none; opacity:1}}
"""


def _tiles(items, cols=3):
    """viz2.tiles 와 같은 카드 · 둘째 칸이 여러 줄(<span> 여러 개)일 때."""
    t = "".join(f'<div class="v2tile" style="--d:{i * .08:.2f}s"><b>{h}</b>{x}</div>' for i, (h, x) in enumerate(items))
    return f'<div class="v2tiles c{cols}">{t}</div>'


def _d07():
    return sk.apple()


def formats():
    """종이 장부 → 엑셀 → CSV → 데이터베이스. 같은 사과 선별 기록을 형식마다."""
    df = _d07()
    h = df.head(3)[["date", "zone", "weight_g", "grade"]]
    rows = "".join(f'<tr><th>{i + 2}</th><td>{r.date[5:]}</td><td>{r.zone}</td><td{" class=sel" if i == 0 else ""}>{r.weight_g}</td><td>{r.grade}</td></tr>'
                   for i, r in enumerate(h.itertuples()))
    xl = (f'<div class="p0v p0xl"><div class="bar">apple_A07.xlsx</div><table><tr><th></th><th>A</th><th>B</th><th>C</th><th>D</th></tr>'
          f'<tr><th>1</th><td>date</td><td>zone</td><td>weight</td><td>grade</td></tr>{rows}</table></div>')
    csv = '<div class="p0v p0csv"><pre>' + esc(h.to_csv(index=False).strip()) + "</pre></div>"
    cnt = df.zone.value_counts()
    tb = "".join(f"<tr><td>{a}</td><td>{cnt[a]}</td></tr>" for a in sk.AREA)
    db = (f'<div class="p0v p0db"><div class="q">SELECT zone, count(*)<br/>FROM apple<br/>GROUP BY zone</div>'
          f'<table><tr><th>zone</th><th>count</th></tr>{tb}</table></div>')
    ledger = '<div class="p0v"><img src="img/p0_ledger.webp" alt="1906년 회계 장부"/></div>'
    cells = [(ledger, "종이 장부", "손으로 적고 손으로 더함"), (xl, "엑셀", "칸 · 수식 · 서식"),
             (csv, "CSV", "쉼표로 나눈 글자"), (db, "데이터베이스", "표 여러 개 · SQL 질의")]
    out = []
    for i, (v, b, s) in enumerate(cells):
        if i:
            out.append("<i>→</i>")
        out.append(f'<div class="p0f" style="--d:{i * .5:.1f}s">{v}<b>{b}</b><span>{s}</span></div>')
    from stats_hx import src
    return f'<div class="p0fm">{"".join(out)}</div>' + src(
        ("장부 사진 · Camp Chesterfield general account ledger (1906) · 퍼블릭 도메인",
         "https://commons.wikimedia.org/wiki/File:Camp_Chesterfield_hotel_ledger,_1940_and_general_account_ledger,_1905-1908_-_DPLA_-_74076597873e46852e851ab1bd511b35_(page_63).jpg"))


def three_tools():
    """같은 질문 「가장자리 사과 상품률」 — 엑셀 · 파이썬 · Claude Code. 세 칸 모두 같은 값."""
    df = _d07()
    o = df[df.zone == "가장자리"]
    n, k = len(o), int((o.grade == "상품").sum())
    rate = round(k / n * 100, 2)
    py = ('import pandas as pd\ndf = pd.read_csv("apple_A07.csv")\nedge = df[df.zone == "가장자리"]\n'
          'rate = (edge.grade == "상품").mean() * 100\nprint(round(rate, 2))')
    xl = ('<ol><li>파일 열기 · 열 필터</li><li><code>=COUNTIFS(F:F,"가장자리",N:N,"상품")</code></li>'
          '<li><code>=COUNTIF(F:F,"가장자리")</code> 로 나누기</li><li>파일 25개면 25번 반복</li></ol>')
    cc = chat([("me", "apple_A07.csv 에서 가장자리 상품률 알려 줘"), ("ai", f"가장자리 {n}개 중 상품 {k}개 · {rate}%")], "Claude Code")
    cols = [("엑셀", xl, "사람이 수식 입력", False), ("파이썬", code("edge_rate.py", esc(py)), "분석가가 코드 작성", False),
            ("Claude Code", cc, "요청 한 문장 · 코드는 Claude 가 작성", True)]
    t = "".join(f'<div class="p0t{" on" if on else ""}" style="--d:{i * .4 + .4:.1f}s"><b>{h}</b>{body}'
                f'<div class="r"><small>상품 {k} / {n}</small>{rate}%</div>'
                f'<span style="font-size:14px;color:#6B7785">{who}</span></div>' for i, (h, body, who, on) in enumerate(cols))
    q = (f'<div class="p0tq"><b>질문</b>과수원 가장자리 나무의 사과 {n}개 중 상품 비율'
         f'<span>상품률 = 상품 개수 ÷ 전체 개수</span></div>')
    return f'{q}<div class="p0tl">{t}</div>'


def table_terms(df):
    """DB 테이블 한 장 — 행(1초) · 열(3초) · 값(5초) 차례로 강조 · 한 번 재생."""
    cols = ["apple_id", "zone", "variety", "weight_g", "grade"]
    h = df.head(5)[cols]
    hc = cols.index("weight_g")
    th = "".join(f'<th class="{"col" if j == hc else ""}">{c}</th>' for j, c in enumerate(cols))
    trs = ""
    for r, (_, row) in enumerate(h.iterrows()):
        tds = "".join(f'<td class="{"col" if j == hc else ""}{" cell" if (r == 1 and j == hc) else ""}{" k" if j == 0 else ""}">{row[c]}</td>'
                      for j, c in enumerate(cols))
        trs += f'<tr class="{"row" if r == 1 else ""}">{tds}</tr>'
    trs += f'<tr><td class="more" colspan="{len(cols)}">… {len(df)}행</td></tr>'
    v = h.iloc[1]
    lg = [("테이블", "table", "apple · 사과 선별 기록을 모은 표", ""),
          ("행", "row · 레코드", f"사과 1개 · {v.apple_id}", "#FFF3E6"),
          ("열", "column · 필드", "같은 종류의 값 · weight_g", "#E6EEF8"),
          ("값", "cell", f"행과 열이 만나는 칸 · {v.weight_g}", "#F28C28"),
          ("기본 키", "primary key", "행마다 겹치지 않는 열 · apple_id", "")]
    leg = "".join(f'<div style="--d:{0.6 + i * 1.0:.1f}s"><b>{"<i style=background:%s></i>" % c if c else ""}{a}<small>{e}</small></b><span>{x}</span></div>'
                  for i, (a, e, x, c) in enumerate(lg))
    return (f'<div class="p0tb"><div class="t"><div class="nm">TABLE apple</div><table><tr>{th}</tr>{trs}</table></div>'
            f'<div class="p0lg">{leg}</div></div>')


def excel_vs_csv(head):
    """같은 사과 기록 4줄 — 엑셀 화면과 CSV 글자. 1~8교시는 CSV 를 다룬다."""
    cols = list(head.columns)
    letters = "ABCDEFGHIJ"
    num = {c for c in cols if str(head[c].dtype) != "object"}
    th = "<tr><th></th>" + "".join(f"<th>{letters[i]}</th>" for i in range(len(cols))) + "</tr>"
    hr = '<tr class="h"><th>1</th>' + "".join(f"<td>{c}</td>" for c in cols) + "</tr>"
    sel = cols.index("weight_g")
    body = "".join("<tr><th>%d</th>" % (r + 2) + "".join(
        f'<td class="{"n" if c in num else ""}{" sel" if (r == 0 and j == sel) else ""}">{v}</td>' for j, (c, v) in enumerate(row.items()))
        + "</tr>" for r, (_, row) in enumerate(head.iterrows()))
    first = head.iloc[0]["weight_g"]
    xl = (f'<div class="p0x"><div class="bar">apple_A07.xlsx</div>'
          f'<div class="fx"><em>{letters[sel]}2</em><i>fx</i>{first}</div><table>{th}{hr}{body}</table>'
          f'<div class="tab">Sheet1</div></div>')
    cv = code("apple_A07.csv", esc(head.to_csv(index=False).strip()))
    rows = [("엑셀", "사람이 보는 화면<br/>칸 · 서식 · 시트", xl, False),
            ("CSV", "1~8교시에서 다루는 형식<br/>쉼표로 나눈 글자", cv, True)]
    return '<div class="p0ev">' + "".join(
        f'<div class="p0er{" on" if on else ""}" style="--d:{i * .8:.1f}s"><div><b>{h}</b><span>{sub}</span></div>{v}</div>'
        for i, (h, sub, v, on) in enumerate(rows)) + "</div>"


def slides():
    df = _d07()
    head = df.head(4)[["date", "tree_x", "tree_y", "zone", "variety", "weight_g", "sugar_brix", "grade"]]

    dd = [
        light("데이터의 정의", viz2.maprows([
            ("편의점 결제", "시각 · 품목 · 금액", "영수증 한 장 = 한 줄"), ("출석", "날짜 · 이름 · 출결", "출석부 한 칸"),
            ("사과 선별", "무게 · 당도 · 흠", "사과 1개 = 한 줄"), ("반도체 테스트", "다이 좌표 · 전압 · 양불", "다이 1개 = 한 줄")],
            "기록 대상", "남는 값"), TAG),
        light("데이터 저장 형식의 변화", formats(), TAG),
        light("엑셀 · CSV · 데이터베이스", _tiles([
            ("엑셀 .xlsx", "<span>사람이 보고 고치는 표 · 수식 · 차트</span><span>시트당 최대 1,048,576행</span>"
                          '<span style="color:#E07A12;font-weight:700">1교시 · 웨이퍼 테스트 엑셀</span>'),
            ("CSV .csv", "<span>쉼표로 나눈 글자 · 서식 없음</span><span>어느 프로그램이나 읽음</span>"
                        '<span style="color:#E07A12;font-weight:700">2교시 · 화면용 CSV</span>'),
            ("데이터베이스", "<span>표 여러 개를 키로 연결 · 여러 사람이 동시에</span><span>SQL 로 질의</span>")], 3), TAG),
    ]
    ex = [
        light("AI 이전의 데이터 처리", _tiles([
            ("손 계산", "<span>장부 · 계산기 · 그래프 용지</span><span>담당자가 한 줄씩 더함</span>"),
            ("스프레드시트", "<span>엑셀 수식 · 필터 · 피벗 · 차트</span><span>실무자가 파일마다 반복</span>"),
            ("코드", "<span>SQL · 파이썬 · 통계 도구</span><span>분석가 · 개발자가 작성</span>")], 3), TAG),
        light("같은 질문, 세 가지 도구", three_tools(), TAG),
        light("분석 요청 경로", viz2.pair(
            "AI 이전", [("질문", "현업 담당자"), ("요청", "분석가에게 전달 · 순서 대기"), ("작업", "분석가가 SQL · 파이썬 작성"), ("결과", "보고서 · 엑셀 파일")],
            "Claude Code", [("질문", "현업 담당자"), ("요청", "요청 한 문장 · 바로 실행"), ("작업", "Claude 가 코드 작성 · 실행 · 오류 수정"), ("결과", "파일 + 사람이 숫자 확인")]), TAG),
        light("기존 코딩과 바이브코딩", viz2.pair(
            "기존 코딩", [("만드는 사람", "코드를 직접 씀"), ("배우는 것", "문법 · 라이브러리"), ("수정", "코드를 찾아 고침")],
            "바이브코딩", [("만드는 사람", "말로 요청 · Claude 가 코드 작성"), ("배우는 것", "요청 · 확인 · 되돌리기"),
                         ("수정", "화면을 보고 다시 요청")]), TAG),
        light("테이블의 행과 열", table_terms(df), TAG),
    ]
    ap = [
        light("사과 선별 데이터", excel_vs_csv(head), TAG),
        light("변수 종류", viz2.maprows([
            ("수치형 변수", "weight_g · sugar_brix · diameter_mm", "평균 · 합계 · 분포"), ("범주형 변수", "zone · variety · grade", "개수 · 비율 · 묶어 세기"),
            ("판정 열 grade", "상품 · 불량", f"멍 · 벌레 없음 · 무게 {sk.MIN_W}g 이상 · 당도 {sk.MIN_SUGAR:g} 이상"),
            ("파일 규모", f"{len(df)}행 × {df.shape[1]}열", "하루 한 파일 · 25일치")], "변수", "apple_A07.csv"), TAG),
        light("수치형 변수", num_anim(df), TAG),
        light("범주형 변수", cat_anim(df), TAG),
        light("상품률", big([
            (f"{GEN['A07']['good']}", "개", "상품 (10월 7일 수확)"), (f"{GEN['A07']['rows']}", "개", "전체 사과"),
            (f"{GEN['A07']['rate']}", "%", "상품률 = 상품 ÷ 전체", True)], 3), TAG),
    ]
    div = divider("0", "데이터와 바이브코딩", "").replace('<div class="kick">0</div>', f'<div class="kick">{TAG}</div>')
    return div, {"도입": dd, "설명": ex, "적용": ap}


CSS += "  .v2tile .p0hl{color:#E07A12; font-weight:700;}\n"


# ── 변수 종류 애니메이션 · 사과 A07 ─────────────────────
from anim import _D, _t, N, O, W, K  # noqa: E402

_X0, _X1, _V0, _V1 = 90, 1070, 40, 170          # 수직선 화면 x · 값 범위(분)


def _vx(v):
    return _X0 + (v - _V0) / (_V1 - _V0) * (_X1 - _X0)


def _chips(d, vals, y=46):
    """첫 8행의 값을 위에 칩으로. 칩 중심 x 목록을 돌려준다."""
    s, xs = "", []
    for i, v in enumerate(vals):
        x = 150 + i * 123
        xs.append(x)
        s += (f'<g {d.show(1 + i * 1.5)}><rect x="{x - 54}" y="{y - 20}" width="108" height="40" rx="8" fill="{W}" stroke="{K}" stroke-width="2"/>'
              + _t(x, y + 1, v, "tm", extra='style="font-size:15px"') + "</g>")
    return s, xs


_SCOL = [("apple_id", 96, False), ("zone", 76, False), ("variety", 70, False), ("weight_g", 84, True),
         ("sugar_brix", 96, True), ("grade", 64, False)]
_ACOL = {"안쪽": "#2F6DB5", "중간": "#2BA38F", "가장자리": "#E07A12"}
_ATINT = {"안쪽": "#E6EEF8", "중간": "#E3F4F0", "가장자리": "#FFF1E3"}
_RH, _SY = 30, 70                                   # 시트 행 높이 · 첫 데이터 행 y


def _rows8(df):
    """시트에 보일 실제 기록 8건 — 세 구역이 모두 섞이게 (원래 순서 유지)."""
    pick = sorted(sum((df.index[df.zone == a][:k].tolist() for a, k in (("안쪽", 2), ("중간", 3), ("가장자리", 3))), []))
    return df.loc[pick]


def _sheet(d, rows, n, hi, hi_t):
    """SVG 엑셀 시트 · 열 hi 를 hi_t% 에 강조. 칸 좌표 {(행, 열): (x, y, w)} 를 돌려준다."""
    x0, rn = 0, 30
    xs, x = {}, x0 + rn
    for c, w, _ in _SCOL:
        xs[c] = (x, w)
        x += w
    W_ = x - x0
    s = (f'<rect x="{x0}" y="0" width="{W_}" height="24" fill="#1D6F42"/>'
         + _t(x0 + 10, 12, "apple_A07.xlsx", "ts", "start", 'style="font-size:12px;fill:#fff;font-weight:700"'))
    y = 24
    s += f'<rect x="{x0}" y="{y}" width="{W_}" height="20" fill="#F1F3F4" stroke="#DADCE0"/>'
    for i, (c, w, _) in enumerate(_SCOL):
        cx = xs[c][0]
        s += f'<line x1="{cx}" y1="{y}" x2="{cx}" y2="{y + 20}" stroke="#DADCE0"/>' + _t(cx + w / 2, y + 10, "ABCDEF"[i], "ts", extra='style="font-size:11px"')
    y = 44
    hx_, hw = xs[hi]
    cells = {}
    allrows = [("hdr", None)] + [(r, row) for r, (_, row) in enumerate(rows.iterrows())]
    for k, (r, row) in enumerate(allrows):
        yy = y + k * _RH if k == 0 else y + 26 + (k - 1) * _RH
        h = 26 if k == 0 else _RH
        fill = "#E8F0E9" if k == 0 else "#fff"
        s += f'<rect x="{x0}" y="{yy}" width="{W_}" height="{h}" fill="{fill}" stroke="#E3E5E8"/>'
        s += f'<rect x="{x0}" y="{yy}" width="{rn}" height="{h}" fill="#F1F3F4" stroke="#DADCE0"/>' + _t(x0 + rn / 2, yy + h / 2, k + 1, "ts", extra='style="font-size:11px"')
        for c, w, num in _SCOL:
            cx = xs[c][0]
            s += f'<line x1="{cx}" y1="{yy}" x2="{cx}" y2="{yy + h}" stroke="#E3E5E8"/>'
            v = c if k == 0 else row[c]
            st = 'style="font-size:13px;font-weight:700;fill:#202124"' if k == 0 else 'style="font-size:14px;fill:#202124"'
            if num and k:
                s += _t(cx + w - 8, yy + h / 2, v, "ts", "end", st)
            else:
                s += _t(cx + 8, yy + h / 2, v, "ts", "start", st)
            if k:
                cells[(r, c)] = (cx, yy, w)
    ye = y + 26 + 8 * _RH
    s += f'<rect x="{x0}" y="{ye}" width="{W_}" height="26" fill="#F8F9FA" stroke="#E3E5E8"/>' + _t(x0 + W_ / 2, ye + 13, f"… {n}행", "ts", extra='style="font-size:13px"')
    # 열 강조 (나타남)
    s += f'<rect x="{hx_}" y="44" width="{hw}" height="{ye - 44}" fill="none" stroke="{O}" stroke-width="3" {d.show(hi_t)}/>'
    return s, cells, W_


def num_anim(df):
    """수치형 — 엑셀 시트의 weight_g 열 → 8칸이 수직선 위 점으로 → 600건 → 평균 · 표준편차. 18초 · 한 번."""
    d = _D("vn", 18)
    rows = _rows8(df)
    sh, cells, W_ = _sheet(d, rows, len(df), "weight_g", 6)
    m, sd = df.weight_g.mean(), df.weight_g.std()
    X0, X1, V0, V1 = W_ + 70, 1150, 200, 380
    vx = lambda v: X0 + (v - V0) / (V1 - V0) * (X1 - X0)  # noqa: E731
    ay = 210
    s = sh + f'<g {d.show(6)}>' + _t(X0, 20, "weight_g · 사과 무게(g) · 수치형", "to", "start", 'style="font-size:17px"') + "</g>"
    s += f'<g {d.show(14)}><line x1="{X0}" y1="{ay}" x2="{X1}" y2="{ay}" stroke="{N}" stroke-width="2.5"/>'
    for t in range(200, 381, 10):
        s += f'<line x1="{vx(t):.1f}" y1="{ay}" x2="{vx(t):.1f}" y2="{ay + (6 if t % 40 else 12)}" stroke="{N}" stroke-width="1.5"/>'
        if t % 40 == 0:
            s += _t(vx(t), ay + 28, t, "ts", extra='style="font-size:13px"')
    s += _t(X1, ay + 48, "g", "ts", "end") + "</g>"
    lv, last = {}, []
    for i in sorted(range(len(rows)), key=lambda j: rows.weight_g.iloc[j]):
        x = vx(rows.weight_g.iloc[i])
        k = next((k for k, lx in enumerate(last) if x - lx > 60), len(last))
        last[k:k + 1] = [x]
        lv[i] = k
    for i, (_, row) in enumerate(rows.iterrows()):
        t = 20 + i * 3.2
        cx, cy, w = cells[(i, "weight_g")]
        v = row.weight_g
        s += f'<rect x="{cx}" y="{cy}" width="{w}" height="{_RH}" fill="{O}" fill-opacity=".22" {d.show(t)}/>'
        s += f'<g {d.show(t)}><circle cx="{vx(v):.1f}" cy="{ay - 14 - lv[i] * 24}" r="9" fill="{O}"/>' \
             f'{_t(vx(v) + 13, ay - 14 - lv[i] * 24, v, "ts", "start", "style=font-size:13px")}</g>'
    rng = __import__("random").Random(7)
    dots = "".join(f'<circle cx="{vx(v):.1f}" cy="{ay + 66 + rng.random() * 56:.1f}" r="3" fill="{K}" fill-opacity=".35"/>' for v in df.weight_g)
    s += f'<g {d.show(52)}>{dots}' + _t(X0 - 8, ay + 94, f"{len(df)}개", "tn", "end") + "</g>"
    s += (f'<g {d.show(66)}><line x1="{vx(m):.1f}" y1="{ay - 104}" x2="{vx(m):.1f}" y2="{ay + 130}" stroke="{O}" stroke-width="3" stroke-dasharray="7 5"/>'
          + _t(vx(m), ay - 120, f"평균 {m:.1f}g", "to", extra='style="font-size:17px"') + "</g>")
    a_, b_ = vx(m - sd), vx(m + sd)
    s += (f'<g {d.show(80)}><path d="M{a_:.1f} {ay + 140} V{ay + 152} H{b_:.1f} V{ay + 140}" fill="none" stroke="{K}" stroke-width="2.5"/>'
          + _t((a_ + b_) / 2, ay + 174, f"표준편차 {sd:.1f}g · 평균 ± 1σ", "tn", extra='style="font-size:16px"')
          + _t(vx(df.weight_g.min()), ay + 200, f"최솟값 {df.weight_g.min()}", "ts")
          + _t(vx(df.weight_g.max()), ay + 200, f"최댓값 {df.weight_g.max()}", "ts") + "</g>")
    return d.svg(1160, 420, s)


def cat_anim(df):
    """범주형 — 엑셀 시트의 zone 열 → 8칸이 위치 색으로 칠해지며 위치별로 한 칸씩 쌓임 → 600개 막대 → 상품 비율. 18초 · 한 번."""
    d = _D("vc", 18)
    rows = _rows8(df)
    sh, cells, W_ = _sheet(d, rows, len(df), "zone", 6)
    names = sk.AREA
    cnt = df.zone.value_counts()
    on = df[df.grade == "상품"].zone.value_counts()
    L = W_ + 60
    bx = {n: L + 80 + i * 200 for i, n in enumerate(names)}
    base, H = 360, 230
    s = sh + f'<g {d.show(6)}>' + _t(L, 20, "zone · 나무 위치 · 범주형", "to", "start", 'style="font-size:17px"') + "</g>"
    s += f'<line x1="{L}" y1="{base}" x2="1150" y2="{base}" stroke="{N}" stroke-width="2.5" {d.show(14)}/>'
    for n in names:
        s += f'<g {d.show(14)}>' + _t(bx[n], base + 26, n, "tt", extra=f'style="font-size:19px;fill:{_ACOL[n]}"') + "</g>"
    seen = {n: 0 for n in names}
    for i, (_, row) in enumerate(rows.iterrows()):
        t = 20 + i * 3.2
        a = row.zone
        cx, cy, w = cells[(i, "zone")]
        s += f'<rect x="{cx}" y="{cy}" width="{w}" height="{_RH}" fill="{_ACOL[a]}" fill-opacity=".3" {d.show(t)}/>'
        k = seen[a]
        seen[a] += 1
        s += f'<rect x="{bx[a] - 22}" y="{base - 34 - k * 36}" width="44" height="30" rx="5" fill="{_ATINT[a]}" stroke="{_ACOL[a]}" stroke-width="2" {d.show(t, 50)}/>'
    for n in names:
        s += f'<g {d.show(47, 50)}>' + _t(bx[n], base - 34 - seen[n] * 36 - 4, f"{seen[n]}개", "to", extra='style="font-size:17px"') + "</g>"
    mx = cnt.max()
    for n in names:
        h = cnt[n] / mx * H
        ho = on.get(n, 0) / mx * H
        grow = "transform-box:fill-box;transform-origin:50% 100%"
        st = [(0, "transform:scaleY(0)"), (54, "transform:scaleY(0)"), (64, "transform:scaleY(1)"), (100, "transform:scaleY(1)")]
        s += f'<rect x="{bx[n] - 55}" y="{base - h:.1f}" width="110" height="{h:.1f}" fill="{_ATINT[n]}" stroke="{_ACOL[n]}" stroke-width="2" {d.a(st, "ease-out", grow)}/>'
        s += f'<g {d.show(64)}>' + _t(bx[n], base - h - 16, f"{cnt[n]}개", "tt", extra='style="font-size:18px"') + "</g>"
        s += f'<rect x="{bx[n] - 55}" y="{base - ho:.1f}" width="110" height="{ho:.1f}" fill="{_ACOL[n]}" {d.show(78)}/>'
        s += (f'<g {d.show(82)}>' + _t(bx[n], base + 54, f"상품 {on.get(n, 0) / cnt[n] * 100:.2f}%", "to",
                                         extra=f'style="font-size:16px;fill:{_ACOL[n]}"') + "</g>")
    return d.svg(1160, 420, s)


# ── 판정 조건 쌓기 · 사과(1교시 앞) · 웨이퍼(판정 순서 뒤) 공통 ─────────
CSS += """
  .p0j{display:grid; grid-template-columns:minmax(0,1fr) 320px; gap:22px; align-items:start; margin-top:4px;}
  .p0j table{border-collapse:collapse; width:100%; font-size:14.5px; background:#fff; border:1.5px solid #D9DDE3;}
  .p0j th{background:#F4F6F9; color:#1F3A5F; font-family:var(--mono); font-size:12.5px; font-weight:700; padding:8px 7px; border-bottom:1.5px solid #D9DDE3; text-align:right;}
  .p0j td{font-family:var(--mono); padding:8px 7px; border-bottom:1px solid #EEF1F5; text-align:right; color:#16233A;}
  .p0j th:first-child, .p0j td:first-child{text-align:left;}
  .p0j td.r{width:118px; text-align:center; font-family:var(--sans); font-weight:800;}
  .p0j td.r span{opacity:0; animation:p0Op .4s var(--d) forwards;}
  .p0j tr.f td{animation:p0Bad .4s var(--d) forwards;}
  .p0j tr.f td.hit{animation:p0Hit .4s var(--d) forwards;}
  .p0j tr.f td.r span{color:#C62828;}
  .p0j tr.ok td{animation:p0Ok .4s var(--d) forwards;}
  .p0j tr.ok td.r span{color:#2E7D32;}
  .p0j ol{list-style:none; margin:0; padding:0; display:flex; flex-direction:column; gap:8px;}
  .p0j li{border:1.5px solid #E1E5EB; border-left:5px solid #1F3A5F; border-radius:10px; background:#fff; padding:8px 12px; opacity:0; animation:p0Op .4s var(--d) forwards;}
  .p0j li b{display:block; font-size:16px; color:#16233A;}
  .p0j li code{font-family:var(--mono); font-size:13px; color:#C62828;}
  .p0j li em{font-style:normal; float:right; font-size:13px; color:#6B7785; font-weight:700;}
  .p0j li.ok{border-left-color:#2E7D32;} .p0j li.ok code{color:#2E7D32;}
  @keyframes p0Op{to{opacity:1}}
  @keyframes p0Bad{to{background:#FDECEA; color:#9AA3AF}}
  @keyframes p0Hit{to{background:#C62828; color:#fff; font-weight:800}}
  @keyframes p0Ok{to{background:#E8F5E9}}
  @media print{.p0j *{animation:none!important; opacity:1!important} .p0j tr.f td{background:#FDECEA} .p0j tr.f td.hit{background:#C62828;color:#fff} .p0j tr.ok td{background:#E8F5E9}}
"""


def judge_build(rows, key, cols, steps, ok, gap=2.5):
    """표 위에 조건을 하나씩 더한다 — 조건마다 처음 걸린 행이 빨갛게 빠지고, 마지막에 남은 행이 통과.
    steps: [(이름, 조건 html, 오른쪽 작은 글씨, 걸림 판단 fn(row)->[걸린 열])] · ok: (이름, 조건 html, 작은 글씨, 판정 글자)."""
    t0 = 1.0
    t_ok = t0 + len(steps) * gap
    th = f"<tr><th>{key[0]}</th>" + "".join(f"<th>{c}</th>" for c in cols) + "<th>판정</th></tr>"
    trs = ""
    for _, r in rows.iterrows():
        k, hit = None, []
        for i, (*_, fn) in enumerate(steps):
            hit = fn(r)
            if hit:
                k = i
                break
        d = (t0 + k * gap if k is not None else t_ok) + .4
        cells = "".join(f'<td class="{"hit" if c in hit else ""}">{r[c]:g}</td>' if not isinstance(r[c], str) else f"<td>{r[c]}</td>"
                        for c in cols)
        res = steps[k][0] if k is not None else ok[3]
        trs += (f'<tr class="{"f" if k is not None else "ok"}" style="--d:{d:.1f}s"><td>{key[1](r)}</td>{cells}'
                f'<td class="r"><span>{res}</span></td></tr>')
    li = "".join(f'<li style="--d:{t0 + i * gap:.1f}s"><b>{i + 1}. {h}<em>{sm}</em></b><code>{c}</code></li>'
                 for i, (h, c, sm, _) in enumerate(steps))
    li += f'<li class="ok" style="--d:{t_ok:.1f}s"><b>{ok[0]}<em>{ok[2]}</em></b><code>{ok[1]}</code></li>'
    return f'<div class="p0j"><div><table>{th}{trs}</table></div><ol>{li}</ol></div>'


def judge_apple():
    """사과 A07 · 멍 → 벌레 → 무게 미달 → 당도 미달 → 상품 (labs/make_apple.py judge 순서). 사유마다 한 개 + 상품 둘."""
    df = _d07()
    w, b = sk.MIN_W, sk.MIN_SUGAR
    steps = [("멍", "bruise = 1", "", lambda r: ["bruise"] if r.bruise else []),
             ("벌레 먹음", "worm = 1", "", lambda r: ["worm"] if r.worm else []),
             ("무게 미달", f"weight_g &lt; {w}", f"{w}g", lambda r: ["weight_g"] if r.weight_g < w else []),
             ("당도 미달", f"sugar_brix &lt; {b:g}", f"{b:g} brix", lambda r: ["sugar_brix"] if r.sugar_brix < b else [])]
    cols = ["bruise", "worm", "weight_g", "sugar_brix"]
    n = df.bruise + df.worm + (df.weight_g < w) + (df.sugar_brix < b)
    df = df.assign(n=n)
    pick = [df[df.reason == "none"].iloc[i] for i in (0, 1)]
    for rs in sk.D_ORDER:
        pick.append(df[df.reason == rs].sort_values("n", ascending=False).iloc[0])
    pick = pd.DataFrame(pick).sort_values("apple_id")
    return judge_build(pick, ("apple_id", lambda r: r.apple_id), cols, steps, ("남은 행", "상품", "", "상품"))


def judge_wafer():
    """W07 · spec.csv 조건을 판정 순서대로. 유형마다 다이 하나 + 양품 둘 (크랙 다이는 다른 조건에도 걸리는 것)."""
    dd = P.parent
    df = pd.read_csv(dd / "raw" / "wafer_test_W07.csv")
    spec = pd.read_csv(dd / "spec.csv")
    import sk
    ko = {k: sk.KO[k] for k in sk.ORDER}

    def bad(r, p):
        s = spec[spec.param == p].iloc[0]
        return bool((pd.notna(s.lsl) and r[p] < s.lsl) or (pd.notna(s.usl) and r[p] > s.usl))

    def txt(p):
        s = spec[spec.param == p].iloc[0]
        if pd.notna(s.lsl) and pd.notna(s.usl):
            return f"{p} {s.lsl:g}~{s.usl:g} 밖"
        return f"{p} &gt; {s.usl:g}" if pd.notna(s.usl) else f"{p} &lt; {s.lsl:g}"

    par = {ft: list(spec[spec.fail_type == ft].param) for ft in ko}
    binno = df.groupby("fail_type").bin.first()
    steps = [(ko[ft], " · ".join(txt(p) for p in par[ft]), f"bin {binno[ft]}",
              (lambda ps: lambda r: [p for p in ps if bad(r, p)])(par[ft])) for ft in ko]
    df = df.assign(n=df.apply(lambda r: sum(any(bad(r, p) for p in par[ft]) for ft in ko), axis=1))
    pick = [df[df.fail_type == "none"].iloc[i] for i in (0, 1)]
    for ft in ko:
        pick.append(df[df.fail_type == ft].sort_values("n", ascending=False).iloc[0])
    pick = pd.DataFrame(pick).sort_values(["die_y", "die_x"])
    cols = ["crack", "rc_ohm", "ioff_na", "vth_v", "particle_cnt", "idsat_ma", "ox_thk_nm"]
    return judge_build(pick, ("die", lambda r: f"({int(r.die_x)}, {int(r.die_y)})"), cols, steps,
                       ("남은 행", "PASS", f"bin {binno['none']}", "합격"))
