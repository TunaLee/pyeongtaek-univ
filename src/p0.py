"""개요 — 데이터와 데이터 분석. 1교시 앞에 붙는다 (build.py).

도입(데이터의 정의 · 저장 형식의 변화 · 엑셀 · CSV · DB)
→ 설명(AI 이전의 처리 · 같은 질문 세 도구 · 분석 요청 경로 · 데이터→결정 · 분석 종류 · 흐름 · 분석과 엔지니어링)
→ 적용(택배 데이터 · 행 · 열 · 변수 · 정시율 · 분석 기법 · 반도체 연결).
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
    return pd.read_csv(P / "delivery_D07.csv")


def formats():
    """종이 장부 → 엑셀 → CSV → 데이터베이스. 같은 택배 기록을 형식마다."""
    df = _d07()
    h = df.head(3)[["date", "area", "delivery_min", "status"]]
    rows = "".join(f'<tr><th>{i + 2}</th><td>{r.date[5:]}</td><td>{r.area}</td><td{" class=sel" if i == 0 else ""}>{r.delivery_min}</td><td>{r.status}</td></tr>'
                   for i, r in enumerate(h.itertuples()))
    xl = (f'<div class="p0v p0xl"><div class="bar">delivery_D07.xlsx</div><table><tr><th></th><th>A</th><th>B</th><th>C</th><th>D</th></tr>'
          f'<tr><th>1</th><td>date</td><td>area</td><td>min</td><td>status</td></tr>{rows}</table></div>')
    csv = '<div class="p0v p0csv"><pre>' + esc(h.to_csv(index=False).strip()) + "</pre></div>"
    cnt = df.area.value_counts()
    tb = "".join(f"<tr><td>{a}</td><td>{cnt[a]}</td></tr>" for a in ("도심", "중간", "외곽"))
    db = (f'<div class="p0v p0db"><div class="q">SELECT area, count(*)<br/>FROM delivery<br/>GROUP BY area</div>'
          f'<table><tr><th>area</th><th>count</th></tr>{tb}</table></div>')
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
    """같은 질문 「10월 7일 외곽 정시율」 — 엑셀 · 파이썬 · Claude Code. 세 칸 모두 같은 값."""
    df = _d07()
    o = df[df.area == "외곽"]
    n, k = len(o), int((o.status == "ON_TIME").sum())
    rate = round(k / n * 100, 2)
    py = ('import pandas as pd\ndf = pd.read_csv("delivery_D07.csv")\nouter = df[df.area == "외곽"]\n'
          'rate = (outer.status == "ON_TIME").mean() * 100\nprint(round(rate, 2))')
    xl = ('<ol><li>파일 열기 · 열 필터</li><li><code>=COUNTIFS(F:F,"외곽",N:N,"ON_TIME")</code></li>'
          '<li><code>=COUNTIF(F:F,"외곽")</code> 로 나누기</li><li>파일 25개면 25번 반복</li></ol>')
    cc = chat([("me", "delivery_D07.csv 에서 외곽 정시율 알려 줘"), ("ai", f"외곽 {n}건 중 정시 {k}건 · {rate}%")], "Claude Code")
    cols = [("엑셀", xl, "사람이 수식 입력", False), ("파이썬", code("outer_rate.py", esc(py)), "분석가가 코드 작성", False),
            ("Claude Code", cc, "요청 한 문장 · 코드는 Claude 가 작성", True)]
    t = "".join(f'<div class="p0t{" on" if on else ""}" style="--d:{i * .4 + .4:.1f}s"><b>{h}</b>{body}'
                f'<div class="r"><small>외곽 정시율 · {k} / {n}</small>{rate}%</div>'
                f'<span style="font-size:14px;color:#6B7785">{who}</span></div>' for i, (h, body, who, on) in enumerate(cols))
    q = (f'<div class="p0tq"><b>질문</b>외곽 구역 배송 {n}건 중 약속 시간({sk.PROMISE}분) 안에 도착한 비율'
         f'<span>정시율 = 정시 건수 ÷ 전체 건수</span></div>')
    return f'{q}<div class="p0tl">{t}</div>'


def table_terms(df):
    """DB 테이블 한 장 — 행(1초) · 열(3초) · 값(5초) 차례로 강조 · 한 번 재생."""
    cols = ["order_id", "area", "truck_id", "delivery_min", "status"]
    h = df.head(5)[cols]
    hc = cols.index("delivery_min")
    th = "".join(f'<th class="{"col" if j == hc else ""}">{c}</th>' for j, c in enumerate(cols))
    trs = ""
    for r, (_, row) in enumerate(h.iterrows()):
        tds = "".join(f'<td class="{"col" if j == hc else ""}{" cell" if (r == 1 and j == hc) else ""}{" k" if j == 0 else ""}">{row[c]}</td>'
                      for j, c in enumerate(cols))
        trs += f'<tr class="{"row" if r == 1 else ""}">{tds}</tr>'
    trs += f'<tr><td class="more" colspan="{len(cols)}">… {len(df)}행</td></tr>'
    v = h.iloc[1]
    lg = [("테이블", "table", f"delivery · 배송 기록을 모은 표", ""),
          ("행", "row · 레코드", f"배송 1건 · {v.order_id}", "#FFF3E6"),
          ("열", "column · 필드", "같은 종류의 값 · delivery_min", "#E6EEF8"),
          ("값", "cell", f"행과 열이 만나는 칸 · {v.delivery_min}", "#F28C28"),
          ("기본 키", "primary key", "행마다 겹치지 않는 열 · order_id", "")]
    leg = "".join(f'<div style="--d:{0.6 + i * 1.0:.1f}s"><b>{"<i style=background:%s></i>" % c if c else ""}{a}<small>{e}</small></b><span>{x}</span></div>'
                  for i, (a, e, x, c) in enumerate(lg))
    return (f'<div class="p0tb"><div class="t"><div class="nm">TABLE delivery</div><table><tr>{th}</tr>{trs}</table></div>'
            f'<div class="p0lg">{leg}</div></div>')


def excel_vs_csv(head):
    """같은 택배 기록 4줄 — 엑셀 화면과 CSV 글자. 1~8교시는 CSV 를 다룬다."""
    cols = list(head.columns)
    letters = "ABCDEFGHIJ"
    num = {c for c in cols if str(head[c].dtype) != "object"}
    th = "<tr><th></th>" + "".join(f"<th>{letters[i]}</th>" for i in range(len(cols))) + "</tr>"
    hr = '<tr class="h"><th>1</th>' + "".join(f"<td>{c}</td>" for c in cols) + "</tr>"
    sel = cols.index("delivery_min")
    body = "".join("<tr><th>%d</th>" % (r + 2) + "".join(
        f'<td class="{"n" if c in num else ""}{" sel" if (r == 0 and j == sel) else ""}">{v}</td>' for j, (c, v) in enumerate(row.items()))
        + "</tr>" for r, (_, row) in enumerate(head.iterrows()))
    first = head.iloc[0]["delivery_min"]
    xl = (f'<div class="p0x"><div class="bar">delivery_D07.xlsx</div>'
          f'<div class="fx"><em>{letters[sel]}2</em><i>fx</i>{first}</div><table>{th}{hr}{body}</table>'
          f'<div class="tab">Sheet1</div></div>')
    cv = code("delivery_D07.csv", esc(head.to_csv(index=False).strip()))
    rows = [("엑셀", "사람이 보는 화면<br/>칸 · 서식 · 시트", xl, False),
            ("CSV", "1~8교시에서 다루는 형식<br/>쉼표로 나눈 글자", cv, True)]
    return '<div class="p0ev">' + "".join(
        f'<div class="p0er{" on" if on else ""}" style="--d:{i * .8:.1f}s"><div><b>{h}</b><span>{sub}</span></div>{v}</div>'
        for i, (h, sub, v, on) in enumerate(rows)) + "</div>"


def slides():
    df = _d07()
    head = df.head(4)[["date", "zone_x", "zone_y", "area", "truck_id", "delivery_min", "reason", "status"]]
    o = df[df.area == "외곽"]
    oc = o[o.truck_id == "TRUCK_C"]
    rate = lambda s: round((s.status == "ON_TIME").mean() * 100, 2)  # noqa: E731
    by = {a: rate(df[df.area == a]) for a in ("도심", "외곽")}
    tr, rs = GEN["truck"], GEN["reason"]
    late = round(rs["late"] / sum(rs.values()) * 100)
    d05 = pd.read_csv(P / "raw" / "delivery_D05.csv")
    dup = int(d05.duplicated(subset=["order_id"]).sum())

    dd = [
        light("데이터의 정의", viz2.maprows([
            ("편의점 결제", "시각 · 품목 · 금액", "영수증 한 장 = 한 줄"), ("출석", "날짜 · 이름 · 출결", "출석부 한 칸"),
            ("택배 배송", "송장 · 구역 · 걸린 시간", "배송 1건 = 한 줄"), ("반도체 테스트", "다이 좌표 · 전압 · 양불", "다이 1개 = 한 줄")],
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
        light("택배 배송 데이터", excel_vs_csv(head), TAG),
        light("변수 종류", viz2.maprows([
            ("수치형 변수", "delivery_min · dist_km", "평균 · 합계 · 분포"), ("범주형 변수", "area · truck_id · status", "개수 · 비율 · 묶어 세기"),
            ("판정 열 status", "ON_TIME · 그 외", "약속 120분 안 · 파손 · 주소 · 부재 없음"),
            ("파일 규모", f"{len(df)}행 × {df.shape[1]}열", "하루 한 파일 · 25일치")], "변수", "delivery_D07.csv"), TAG),
        light("수치형 변수", num_anim(df), TAG),
        light("범주형 변수", cat_anim(df), TAG),
        light("정시 도착률", big([
            (f"{GEN['D07']['on_time']}", "건", "정시 도착 (10월 7일)"), (f"{GEN['D07']['rows']}", "건", "전체 배송"),
            (f"{GEN['D07']['rate']}", "%", "정시 도착률 = 정시 ÷ 전체", True)], 3), TAG),
    ]
    div = divider("0", "데이터와 바이브코딩", "").replace('<div class="kick">0</div>', f'<div class="kick">{TAG}</div>')
    return div, {"도입": dd, "설명": ex, "적용": ap}


CSS += "  .v2tile .p0hl{color:#E07A12; font-weight:700;}\n"


# ── 변수 종류 애니메이션 · 택배 D07 ─────────────────────
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


def num_anim(df):
    """수치형 — 값 8개가 수직선 위에 점으로 → 600건 전체 → 평균 · 표준편차. 16초 · 한 번."""
    d = _D("vn", 16)
    v8 = df.delivery_min.head(8).tolist()
    m, sd = df.delivery_min.mean(), df.delivery_min.std()
    c, xs = _chips(d, v8)
    s = c + f'<g {d.show(0)}>' + _t(150 - 54, 4, "delivery_min · 첫 8행", "to", "start") + "</g>"
    # 수직선
    s += f'<g {d.show(14)}><line x1="{_X0}" y1="250" x2="{_X1}" y2="250" stroke="{N}" stroke-width="2.5"/>'
    for t in range(40, 171, 10):
        s += f'<line x1="{_vx(t):.1f}" y1="250" x2="{_vx(t):.1f}" y2="{258 if t % 50 else 264}" stroke="{N}" stroke-width="1.5"/>'
        if t % 20 == 0:
            s += _t(_vx(t), 280, t, "ts", extra='style="font-size:13px"')
    s += _t(_X1 + 8, 280, "분", "ts", "start") + "</g>"
    # 8개 점이 수직선 위 제자리에 차례로 (움직이지 않고 나타남)
    for i, v in enumerate(v8):
        s += f'<circle cx="{_vx(v):.1f}" cy="236" r="9" fill="{O}" {d.show(22 + i * 2.5)}/>'
    # 600건 전체 · 점 띠
    rng = __import__("random").Random(7)
    dots = "".join(f'<circle cx="{_vx(v):.1f}" cy="{316 + rng.random() * 50:.1f}" r="3" fill="{K}" fill-opacity=".35"/>' for v in df.delivery_min)
    s += f'<g {d.show(48)}>{dots}' + _t(_X0 - 10, 341, f"{len(df)}건", "tn", "end") + "</g>"
    # 평균 · 표준편차
    s += (f'<g {d.show(64)}><line x1="{_vx(m):.1f}" y1="206" x2="{_vx(m):.1f}" y2="380" stroke="{O}" stroke-width="3" stroke-dasharray="7 5"/>'
          + _t(_vx(m), 192, f"평균 {m:.1f}분", "to", extra='style="font-size:17px"') + "</g>")
    a, b = _vx(m - sd), _vx(m + sd)
    s += (f'<g {d.show(80)}><path d="M{a:.1f} 392 V404 H{b:.1f} V392" fill="none" stroke="{K}" stroke-width="2.5"/>'
          + _t((a + b) / 2, 426, f"표준편차 {sd:.1f}분 · 평균 ± 1σ", "tn", extra='style="font-size:16px"')
          + _t(_vx(df.delivery_min.min()), 426, f"최솟값 {df.delivery_min.min()}", "ts")
          + _t(_vx(df.delivery_min.max()), 426, f"최댓값 {df.delivery_min.max()}", "ts") + "</g>")
    return d.svg(1160, 440, s)


def cat_anim(df):
    """범주형 — 첫 8행 구역 칩(색 = 범주) → 구역별 건수 막대 → 정시 비율. 16초 · 한 번."""
    d = _D("vc", 16)
    names = sk.AREA
    col = {"도심": "#2F6DB5", "중간": "#2BA38F", "외곽": "#E07A12"}
    tint = {"도심": "#E6EEF8", "중간": "#E3F4F0", "외곽": "#FFF1E3"}
    pick = sorted(sum((df.index[df.area == a][:k].tolist() for a, k in (("도심", 2), ("중간", 3), ("외곽", 3))), []))
    v8 = df.area.loc[pick].tolist()
    cnt = df.area.value_counts()
    on = df[df.status == "ON_TIME"].area.value_counts()
    bx = {n: 250 + i * 330 for i, n in enumerate(names)}
    base, H = 388, 200
    s = f'<g {d.show(0)}>' + _t(150 - 54, 4, "area · 기록 8건", "to", "start") + "</g>"
    for i, v in enumerate(v8):
        x = 150 + i * 123
        s += (f'<g {d.show(1 + i * 1.5)}><rect x="{x - 54}" y="26" width="108" height="40" rx="8" fill="{tint[v]}" stroke="{col[v]}" stroke-width="2"/>'
              + _t(x, 47, v, "tm", extra=f'style="font-size:16px;fill:{col[v]};font-weight:700"') + "</g>")
    s += f'<line x1="70" y1="{base}" x2="1090" y2="{base}" stroke="{N}" stroke-width="2.5" {d.show(14)}/>'
    for n in names:
        s += f'<g {d.show(14)}>' + _t(bx[n], base + 28, n, "tt", extra=f'style="font-size:19px;fill:{col[n]}"') + "</g>"
    c8 = pd.Series(v8).value_counts()
    for i, n in enumerate(names):
        s += f'<g {d.show(22 + i * 8, 46)}>' + _t(bx[n], base - 40, f"8건 중 {c8.get(n, 0)}건", "to", extra='style="font-size:18px"') + "</g>"
    mx = cnt.max()
    for n in names:
        h = cnt[n] / mx * H
        ho = on.get(n, 0) / mx * H
        grow = "transform-box:fill-box;transform-origin:50% 100%"
        st = [(0, "transform:scaleY(0)"), (50, "transform:scaleY(0)"), (60, "transform:scaleY(1)"), (100, "transform:scaleY(1)")]
        s += f'<rect x="{bx[n] - 60}" y="{base - h:.1f}" width="120" height="{h:.1f}" fill="{tint[n]}" stroke="{col[n]}" stroke-width="2" {d.a(st, "ease-out", grow)}/>'
        s += f'<g {d.show(60)}>' + _t(bx[n], base - h - 18, f"{cnt[n]}건", "tt", extra='style="font-size:18px"') + "</g>"
        s += f'<rect x="{bx[n] - 60}" y="{base - ho:.1f}" width="120" height="{ho:.1f}" fill="{col[n]}" {d.show(76)}/>'
        s += (f'<g {d.show(80)}>' + _t(bx[n] + 72, base - ho / 2, f"정시 {on.get(n, 0) / cnt[n] * 100:.2f}%", "to", "start",
                                         'style="font-size:16px"') + "</g>")
    return d.svg(1160, 440, s)


# ── 판정 조건 쌓기 · 택배(1교시 앞) · 웨이퍼(판정 순서 뒤) 공통 ─────────
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


def judge_delivery():
    """택배 D07 · 파손 → 주소 오류 → 지연 → 부재 → 정시 (labs/make_general.py judge 순서). 사유마다 한 건 + 정시 둘."""
    df = _d07()
    prom = 120
    steps = [("파손", "damaged = 1", "", lambda r: ["damaged"] if r.damaged else []),
             ("주소 오류", "addr_error = 1", "", lambda r: ["addr_error"] if r.addr_error else []),
             ("지연", f"delivery_min &gt; {prom}", f"약속 {prom}분", lambda r: ["delivery_min"] if r.delivery_min > prom else []),
             ("부재", "absent = 1", "", lambda r: ["absent"] if r.absent else [])]
    cols = ["damaged", "addr_error", "delivery_min", "absent"]
    n = df.damaged + df.addr_error + (df.delivery_min > prom) + df.absent
    df = df.assign(n=n)
    pick = [df[df.reason == "none"].iloc[i] for i in (0, 1)]
    for rs in ("damaged", "addr_error", "late", "absent"):
        pick.append(df[df.reason == rs].sort_values("n", ascending=False).iloc[0])
    pick = pd.DataFrame(pick).sort_values("order_id")
    return judge_build(pick, ("order_id", lambda r: r.order_id), cols, steps, ("남은 행", "ON_TIME", "", "정시"))


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
