"""개요 — 데이터와 데이터 분석. 1교시 앞에 붙는다 (build.py).

도입(데이터의 정의 · 저장 형식의 변화 · 엑셀 · CSV · DB)
→ 설명(AI 이전의 처리 · 같은 질문 세 도구 · 분석 요청 경로 · 데이터→결정 · 분석 종류 · 흐름 · 분석과 엔지니어링)
→ 적용(택배 데이터 · 행 · 열 · 변수 · 정시율 · 분석 기법 · 반도체 연결).
숫자는 practice CSV · labs/ref.json 에서 계산한다.
"""
import pandas as pd

import pgen
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
  .p0t .r{margin-top:auto; font-size:17px; font-weight:800; color:#E07A12;}
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
    t = "".join(f'<div class="p0t{" on" if on else ""}" style="--d:{i * .4:.1f}s"><b>{h}</b>{body}<div class="r">{rate}%</div>'
                f'<span style="font-size:14px;color:#6B7785">{who}</span></div>' for i, (h, body, who, on) in enumerate(cols))
    return f'<div class="p0tl">{t}</div>'


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
    on = '<span style="color:#E07A12;font-weight:800">이 과정 1~8교시</span>'
    off = "<span>이 과정 밖</span>"

    dd = [
        light("데이터의 정의", viz2.maprows([
            ("편의점 결제", "시각 · 품목 · 금액", "영수증 한 장 = 한 줄"), ("출석", "날짜 · 이름 · 출결", "출석부 한 칸"),
            ("택배 배송", "송장 · 구역 · 걸린 시간", "배송 1건 = 한 줄"), ("반도체 테스트", "다이 좌표 · 전압 · 양불", "다이 1개 = 한 줄")],
            "기록 대상", "남는 값"), TAG),
        light("데이터 저장 형식의 변화", formats(), TAG),
        light("엑셀 · CSV · 데이터베이스", _tiles([
            ("엑셀 .xlsx", "<span>사람이 보고 고치는 표 · 수식 · 차트</span><span>시트당 최대 1,048,576행</span>"
                          '<span style="color:#E07A12;font-weight:700">3교시 · 수율 요약 엑셀</span>'),
            ("CSV .csv", "<span>쉼표로 나눈 글자 · 서식 없음</span><span>어느 프로그램이나 읽음</span>"
                        '<span style="color:#E07A12;font-weight:700">1교시 · 웨이퍼 테스트 결과</span>'),
            ("데이터베이스", "<span>표 여러 개를 키로 연결 · 여러 사람이 동시에</span><span>SQL 로 질의</span>"
                           '<span style="color:#E07A12;font-weight:700">6교시 · DuckDB</span>')], 3), TAG),
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
        light("데이터 · 정보 · 인사이트 · 결정", viz2.maprows([
            ("데이터", f"배송 기록 {len(df)}행", f"delivery_D07.csv · 열 {df.shape[1]}개"),
            ("정보", f"외곽 정시율 {by['외곽']}%", f"{int((o.status == 'ON_TIME').sum())} ÷ {len(o)} · 도심 {by['도심']}%"),
            ("인사이트", "외곽 지연은 TRUCK_C 쪽", f"외곽 {len(oc)}건 · 정시율 {rate(oc)}%"),
            ("결정", "외곽 배차 조정", "사람이 정함")], "단계", "택배 예 · 10월 7일"), TAG),
        light("분석의 네 종류", _tiles([
            ("기술", f"<span>무엇이 일어났나</span><span>정시율 {GEN['D07']['rate']}%</span>{on}"),
            ("진단", f"<span>왜 일어났나</span><span>외곽 · TRUCK_C 지연</span>{on}"),
            ("예측", f"<span>무엇이 일어날까</span><span>11월 지연 건수 추정</span>{off}"),
            ("처방", f"<span>무엇을 할까</span><span>배차 조정안</span>{off}")], 4), TAG),
        light("데이터 분석의 흐름", pgen.flow_anim(), TAG),
        light("분석과 엔지니어링", viz2.pair(
            "데이터 분석", [("질문", "외곽 배송은 왜 늦나"), ("결과", "차트 · 원인 후보 · 요약"), ("주기", "질문이 생길 때 한 번")],
            "데이터 엔지니어링", [("질문", "매일 정시율 집계 자동화"), ("결과", "정제 · 적재 · 집계 스크립트"), ("주기", "파일이 들어올 때마다")]), TAG),
        light("테이블의 행과 열", table_terms(df), TAG),
    ]
    ap = [
        light("택배 배송 데이터", excel_vs_csv(head), TAG),
        light("변수 종류", viz2.maprows([
            ("수치형 변수", "delivery_min · dist_km", "평균 · 합계 · 분포"), ("범주형 변수", "area · truck_id · status", "개수 · 비율 · 묶어 세기"),
            ("판정 열 status", "ON_TIME · 그 외", "약속 120분 안 · 파손 · 주소 · 부재 없음"),
            ("파일 규모", f"{len(df)}행 × {df.shape[1]}열", "하루 한 파일 · 25일치")], "변수", "delivery_D07.csv"), TAG),
        light("정시 도착률", big([
            (f"{GEN['D07']['on_time']}", "건", "정시 도착 (10월 7일)"), (f"{GEN['D07']['rows']}", "건", "전체 배송"),
            (f"{GEN['D07']['rate']}", "%", "정시 도착률 = 정시 ÷ 전체", True)], 3), TAG),
        light("택배 데이터의 분석 기법", _tiles([
            ("정제", f'<span>중복 · 단위 · 결측</span><span class="p0hl">D05 송장 중복 {dup}행 · D11 무게 g 기록</span>'),
            ("집계 · Pareto", f'<span>구역별 정시율 · 실패 사유 순위</span><span class="p0hl">외곽 {GEN["area"]["외곽"]}% · 지연이 실패의 {late}%</span>'),
            ("지도", '<span>좌표별 정시율</span><span class="p0hl">물류센터에서 먼 고리일수록 낮음</span>'),
            ("분포", f'<span>배송 시간의 퍼짐</span><span class="p0hl">평균 {GEN["D07"]["mean_min"]}분 · 표준편차 {GEN["D07"]["std_min"]}분 (D07)</span>'),
            ("그룹 비교", f'<span>차량별 정시율 SQL</span><span class="p0hl">TRUCK_C {tr["TRUCK_C"]}%</span>'),
            ("자동화", '<span>매일 같은 집계</span><span class="p0hl">25일 파일 · 명령 하나로 갱신</span>')], 3), TAG),
        light("기법별 반도체 적용", viz2.maprows([
            ("정제", "다이 좌표 중복 · vth 단위 · 결측", "2교시"), ("집계 · Pareto", "존별 수율 · 불량 유형 순위", "3교시"),
            ("지도", "웨이퍼 맵 · 불량 패턴", "4교시"), ("분포", "vth 분포 · Cpk", "5교시"),
            ("그룹 비교", "설비별 수율 · ETCH_03", "6교시"), ("자동화", "대시보드 · run_all.py", "7교시")], "택배에서 쓴 기법", "반도체 데이터"), TAG),
    ]
    div = divider("0", "데이터와 데이터 분석", "").replace('<div class="kick">0</div>', f'<div class="kick">{TAG}</div>')
    return div, {"도입": dd, "설명": ex, "적용": ap}


CSS += "  .v2tile .p0hl{color:#E07A12; font-weight:700;}\n"
