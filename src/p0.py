"""개요 — 데이터와 데이터 분석. 1교시 앞에 붙는다 (build.py).

도입(데이터의 정의 · 저장 형식의 변화 · 엑셀 · CSV · DB)
→ 설명(AI 이전의 처리 · 같은 질문 세 도구 · 분석 요청 경로 · 데이터→결정 · 분석 종류 · 흐름 · 분석과 엔지니어링)
→ 적용(사과 선별 데이터 · 행 · 열 · 변수 · 상품률).
숫자는 practice CSV · labs/ref.json 에서 계산한다.
"""
import pandas as pd

import pbg
import sk
import viz2
from deck import divider, light
from hx import code, esc
from pkit import chat
from stats_hx import quote, src

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
  .p0tb .t .nm{background:#1D6F42; color:#fff; font-size:13px; font-weight:700; padding:7px 14px;}
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


SALES = [("R-0001", "삼각김밥", 1500), ("R-0002", "우유", 1800), ("R-0003", "삼각김밥", 1500)]  # 저장 형식 설명용 예


def formats():
    """종이 장부 → 엑셀 → CSV → 데이터베이스. 같은 편의점 결제 기록 세 줄을 형식마다 (개요 · 사과 데이터는 1교시에)."""
    h = pd.DataFrame(SALES, columns=["영수증", "품목", "금액"])
    rows = "".join(f'<tr><th>{i + 2}</th><td>{r["영수증"]}</td><td>{r["품목"]}</td><td{" class=sel" if i == 0 else ""}>{r["금액"]:,}</td></tr>'
                   for i, (_, r) in enumerate(h.iterrows()))
    xl = (f'<div class="p0v p0xl"><div class="bar">결제_10월7일.xlsx</div><table><tr><th></th><th>A</th><th>B</th><th>C</th></tr>'
          f'<tr><th>1</th><td>영수증</td><td>품목</td><td>금액</td></tr>{rows}</table></div>')
    csv = '<div class="p0v p0csv"><pre>' + esc(h.to_csv(index=False).strip()) + "</pre></div>"
    tot = h.groupby("품목", sort=False)["금액"].sum()
    tb = "".join(f"<tr><td>{k}</td><td>{v:,}</td></tr>" for k, v in tot.items())
    db = (f'<div class="p0v p0db"><div class="q">SELECT 품목, sum(금액) AS 합계<br/>FROM 결제<br/>GROUP BY 품목</div>'
          f'<table><tr><th>품목</th><th>합계</th></tr>{tb}</table></div>')
    ledger = '<div class="p0v"><img src="img/p0_ledger.webp" alt="1906년 회계 장부"/></div>'
    cells = [(ledger, "종이 장부", "손으로 적고 손으로 더함"), (xl, "엑셀", "칸 · 수식 · 서식"),
             (csv, "CSV", "쉼표로 나눈 글자"), (db, "데이터베이스", "표 여러 개 · SQL 질의")]
    out = []
    for i, (v, b, s_) in enumerate(cells):
        if i:
            out.append("<i>→</i>")
        out.append(f'<div class="p0f" style="--d:{i * .5:.1f}s">{v}<b>{b}</b><span>{s_}</span></div>')
    from stats_hx import src
    return f'<div class="p0fm">{"".join(out)}</div>' + src(
        ("장부 사진 · Camp Chesterfield general account ledger (1906) · 퍼블릭 도메인",
         "https://commons.wikimedia.org/wiki/File:Camp_Chesterfield_hotel_ledger,_1940_and_general_account_ledger,_1905-1908_-_DPLA_-_74076597873e46852e851ab1bd511b35_(page_63).jpg"))


def three_tools():
    """같은 질문 「가장자리 사과 상품률」 — 엑셀 · 파이썬 · Claude Code. 세 칸 모두 같은 값."""
    df = _d07()
    o = df[df["위치"] == "가장자리"]
    n, k = len(o), int((o["등급"] == "상품").sum())
    rate = round(k / n * 100, 2)
    py = ('import pandas as pd\ndf = pd.read_csv("apple_A07.csv")\nedge = df[df["위치"] == "가장자리"]\n'
          'rate = (edge["등급"] == "상품").mean() * 100\nprint(round(rate, 2))')
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
    """엑셀 시트 한 장 = 테이블 — 행(1초) · 열(3초) · 값(5초) 차례로 강조 · 한 번 재생."""
    cols = ["사과번호", "위치", "품종", "무게", "등급"]
    h = df.head(5)[cols]
    hc = cols.index("무게")
    th = "".join(f'<th class="{"col" if j == hc else ""}">{c}</th>' for j, c in enumerate(cols))
    trs = ""
    for r, (_, row) in enumerate(h.iterrows()):
        tds = "".join(f'<td class="{"col" if j == hc else ""}{" cell" if (r == 1 and j == hc) else ""}{" k" if j == 0 else ""}">{row[c]}</td>'
                      for j, c in enumerate(cols))
        trs += f'<tr class="{"row" if r == 1 else ""}">{tds}</tr>'
    trs += f'<tr><td class="more" colspan="{len(cols)}">… {len(df)}행</td></tr>'
    v = h.iloc[1]
    lg = [("테이블", "table", f"시트 한 장 · 사과 선별 기록 {len(df)}행", ""),
          ("행", "row · 레코드", f"사과 1개 · {v['사과번호']}", "#FFF3E6"),
          ("열", "column · 필드", "같은 종류의 값 · 무게", "#E6EEF8"),
          ("값", "cell", f"행과 열이 만나는 칸 · {v['무게']}", "#F28C28")]
    leg = "".join(f'<div style="--d:{0.6 + i * 1.0:.1f}s"><b>{"<i style=background:%s></i>" % c if c else ""}{a}<small>{e}</small></b><span>{x}</span></div>'
                  for i, (a, e, x, c) in enumerate(lg))
    return (f'<div class="p0tb"><div class="t"><div class="nm">apple_A07.xlsx</div><table><tr>{th}</tr>{trs}</table></div>'
            f'<div class="p0lg">{leg}</div></div>')


def _letters(cols, full):
    """보여 줄 열의 실제 엑셀 열 글자 — 숨긴 열이 있으면 글자가 건너뜀 (A B C D F …)."""
    return [chr(65 + list(full).index(c)) for c in cols]


def excel_vs_csv(head, sel="무게", name="apple_A07",
                 subs=("사람이 보는 파일<br/>칸 · 서식 · 시트", "HTML 화면이 읽는 파일<br/>쉼표로 나눈 글자"), full=None):
    """같은 기록 4줄 — 엑셀 화면과 CSV 글자 (2교시 엑셀과 CSV). 열 글자는 원본 파일 기준."""
    cols = list(head.columns)
    letters = _letters(cols, full if full is not None else cols)
    num = {c for c in cols if str(head[c].dtype) != "object"}
    th = "<tr><th></th>" + "".join(f"<th>{letters[i]}</th>" for i in range(len(cols))) + "</tr>"
    hr = '<tr class="h"><th>1</th>' + "".join(f"<td>{c}</td>" for c in cols) + "</tr>"
    first = head.iloc[0][sel]
    sel = cols.index(sel)
    body = "".join("<tr><th>%d</th>" % (r + 2) + "".join(
        f'<td class="{"n" if c in num else ""}{" sel" if (r == 0 and j == sel) else ""}">{v}</td>' for j, (c, v) in enumerate(row.items()))
        + "</tr>" for r, (_, row) in enumerate(head.iterrows()))
    xl = (f'<div class="p0x"><div class="bar">{name}.xlsx</div>'
          f'<div class="fx"><em>{letters[sel]}2</em><i>fx</i>{first}</div><table>{th}{hr}{body}</table>'
          f'<div class="tab">Sheet1</div></div>')
    cv = code(f"{name}.csv", esc(head.to_csv(index=False).strip()))
    rows = [("엑셀", subs[0], xl, False), ("CSV", subs[1], cv, True)]
    return '<div class="p0ev">' + "".join(
        f'<div class="p0er{" on" if on else ""}" style="--d:{i * .8:.1f}s"><div><b>{h}</b><span>{sub}</span></div>{v}</div>'
        for i, (h, sub, v, on) in enumerate(rows)) + "</div>"


def _steps(items, cols, step=2.0):
    """변화 카드 — 2초 간격으로 한 칸씩 · 마지막 칸 강조."""
    t = "".join(f'<div class="v2tile{" p0on" if i == len(items) - 1 else ""}" style="--d:{.3 + i * step:.1f}s"><b>{h}</b>{x}</div>'
                for i, (h, x) in enumerate(items))
    return f'<div class="v2tiles c{cols}">{t}</div>'


def history():
    """개요 1 · 바이브코딩까지 — 유래 · 사례 → 언어 발전 · AI 코딩 도구 변화 → 기존 코딩과 바이브코딩."""
    dd = [
        light("바이브코딩의 유래", quote(
            "내가 <mark>「바이브코딩」</mark>이라고 부르는 새로운 코딩 방식이 있다. 느낌(vibe)에 완전히 몸을 맡기고, "
            "AI의 빠른 발전을 받아들이고, 코드가 있다는 사실조차 잊는 방식이다.",
            "Andrej Karpathy · X · 2025-02-02 · 원문 「There's a new kind of coding I call “vibe coding”…」")
              + viz2.tiles([("2023-01 · Karpathy", "「가장 인기 있는 새 프로그래밍 언어는 영어」"),
                            ("2025-02 · Karpathy", "「바이브코딩」 처음 사용"),
                            ("2025-11 · Collins 사전", "올해의 단어 선정")], 3)
              + src(("Karpathy · 2023-01-24", "https://x.com/karpathy/status/1617979122625712128"),
                    ("Karpathy · 2025-02-02", "https://x.com/karpathy/status/1886192184808149383"),
                    ("Collins · 2025-11-06", "https://blog.collinsdictionary.com/language-lovers/collins-word-of-the-year-2025-ai-meets-authenticity-as-society-shifts/")), TAG),
        light("바이브코딩 사례", viz2.tiles([
            ("브라우저 3D 비행 게임", "fly.pieter.com · 개발자 1명 + AI"),
            ("메뉴판 사진 → 음식 그림", "MenuGen · Karpathy"),
            ("수율 시뮬레이터", "엑셀 데이터 → 조절 바 화면 · 이 과정 8교시")], 3)
              + src(("levelsio · X", "https://x.com/levelsio/status/1899596115210891751"),
                    ("Karpathy · MenuGen", "https://karpathy.bearblog.dev/vibe-coding-menugen/")), TAG),
    ]
    ex = [
        light("프로그래밍 언어의 발전", pbg.langs()
              + src(("IBM · FORTRAN", "https://www.ibm.com/history/fortran"), ("Python · History", "https://docs.python.org/3/license.html")), TAG),
        light("AI 코딩 도구의 변화", pbg.eras()
              + src(("GitHub · 2021-06-29", "https://github.blog/2021-06-29-introducing-github-copilot-ai-pair-programmer/"),
                    ("OpenAI · 2022-11-30", "https://openai.com/index/chatgpt/"),
                    ("Anthropic · 2025-05-22", "https://www.anthropic.com/news/claude-4")), TAG),
    ]
    ap = [
        light("기존 코딩과 바이브코딩", viz2.pair(
            "기존 코딩", [("만드는 사람", "코드를 직접 씀"), ("익힐 내용", "문법 · 라이브러리"), ("수정", "코드를 찾아 고침")],
            "바이브코딩", [("만드는 사람", "말로 요청 · Claude 가 코드 작성"), ("익힐 내용", "요청 · 확인 · 되돌리기"),
                         ("수정", "화면을 보고 다시 요청")]), TAG),
    ]
    return _div("바이브코딩까지"), {"도입": dd, "설명": ex, "적용": ap}


def data_change():
    """개요 2 · 데이터 분석과 엔지니어링 — 데이터 · 저장 형식 → 처리 방법 · 요청 경로 · 분석과 엔지니어링 · 엔지니어링의 변화 → 결과물의 변화.
    일반 예(편의점 결제)만 쓴다. 사과 · 웨이퍼 데이터와 데이터 보는 법은 1 · 2교시 실습 단계에서."""
    dd = [
        light("데이터의 정의", viz2.maprows([
            ("편의점 결제", "시각 · 품목 · 금액", "영수증 한 장 = 한 줄"), ("출석", "날짜 · 이름 · 출결", "출석부 한 칸"),
            ("사과 선별", "무게 · 당도 · 흠", "사과 1개 = 한 줄"), ("반도체 검사", "칩 위치 · 측정값 · 합격 · 불합격", "칩 1개 = 한 줄")],
            "기록 대상", "남는 값"), TAG),
        light("데이터 저장 형식의 변화", formats(), TAG),
    ]
    ex = [
        light("데이터 처리 방법의 변화", _steps([
            ("손 계산", "<span>장부 · 계산기 · 그래프 용지</span><span>담당자가 한 줄씩 더함</span>"),
            ("스프레드시트", "<span>엑셀 수식 · 필터 · 피벗 · 차트</span><span>실무자가 파일마다 반복</span>"),
            ("코드", "<span>SQL · 파이썬 · 통계 도구</span><span>분석가 · 개발자가 작성</span>"),
            ("AI 에이전트", "<span>요청 한 문장 · Claude Code</span><span>담당자가 요청 · 결과 확인</span>")], 4), TAG),
        light("분석 요청 경로", viz2.pair(
            "AI 이전", [("질문", "현업 담당자"), ("요청", "분석가에게 전달 · 순서 대기"), ("작업", "분석가가 SQL · 파이썬 작성"), ("결과", "보고서 · 엑셀 파일")],
            "Claude Code", [("질문", "현업 담당자"), ("요청", "요청 한 문장 · 바로 실행"), ("작업", "Claude 가 코드 작성 · 실행 · 오류 수정"), ("결과", "파일 + 사람이 숫자 확인")]), TAG),
        light("분석과 엔지니어링", viz2.pair(
            "데이터 분석", [("질문", "「어느 품목이 많이 팔리나」"), ("결과", "차트 · 원인 후보 · 요약"), ("주기", "질문이 생길 때 한 번")],
            "데이터 엔지니어링", [("질문", "「매일 결제 파일을 같은 기준으로 집계」"), ("결과", "읽기 · 정제 · 집계 스크립트"), ("주기", "파일이 들어올 때마다")]), TAG),
        light("엔지니어링 작업의 변화", viz2.pair(
            "AI 이전", [("작성", "엔지니어가 스크립트 코드 작성"), ("오류", "로그를 읽고 사람이 수정"), ("반복", "같은 코드를 정해진 시각에 실행"),
                       ("규칙", "문서 · 담당자 기억")],
            "AI 에이전트", [("작성", "요청 → Claude 가 작성 · 실행"), ("오류", "Claude 가 오류를 읽고 고침 · 사람은 결과 확인"),
                          ("반복", "같은 요청 · 저장해 둔 절차"), ("규칙", "규칙 파일 · 자동 차단 장치")]), TAG),
    ]
    ap = [
        light("분석 결과물의 변화", pbg.results_change(), TAG),
    ]
    return _div("데이터 분석과 엔지니어링"), {"도입": dd, "설명": ex, "적용": ap}


def _div(title):
    return divider("0", title, "").replace('<div class="kick">0</div>', f'<div class="kick">{TAG}</div>')


def slides():
    """개요 두 부분 — [(간지, {도입 · 설명 · 적용})]."""
    return [history(), data_change()]


CSS += "  .v2tile .p0hl{color:#E07A12; font-weight:700;}\n  .v2tile.p0on{border-color:#F28C28; background:#FFF8F0;}\n"


# ── 변수 종류 애니메이션 · 사과 A07 ─────────────────────
from anim import _D, _t, N, O, W, K  # noqa: E402

_SCOL = [("사과번호", 100, False), ("위치", 80, False), ("품종", 66, False), ("무게", 76, True),
         ("당도", 76, True), ("등급", 66, False)]
_ACOL = {"안쪽": "#2F6DB5", "중간": "#2BA38F", "가장자리": "#E07A12"}
_ATINT = {"안쪽": "#E6EEF8", "중간": "#E3F4F0", "가장자리": "#FFF1E3"}
_RH, _SY = 30, 70                                   # 시트 행 높이 · 첫 데이터 행 y


def _rows8(df):
    """시트에 보일 실제 기록 8건 — 세 구역이 모두 섞이게 (원래 순서 유지)."""
    pick = sorted(sum((df.index[df["위치"] == a][:k].tolist() for a, k in (("안쪽", 2), ("중간", 3), ("가장자리", 3))), []))
    return df.loc[pick]


def _sheet(d, rows, n, hi, hi_t, scol=None):
    """SVG 엑셀 시트 · 열 hi 를 hi_t% 에 강조. 칸 좌표 {(행, 열): (x, y, w)} 를 돌려준다. scol 로 보여 줄 열을 바꿈."""
    scol = scol or _SCOL
    x0, rn = 0, 30
    xs, x = {}, x0 + rn
    for c, w, _ in scol:
        xs[c] = (x, w)
        x += w
    W_ = x - x0
    s = (f'<rect x="{x0}" y="0" width="{W_}" height="24" fill="#1D6F42"/>'
         + _t(x0 + 10, 12, "apple_A07.xlsx", "ts", "start", 'style="font-size:12px;fill:#fff;font-weight:700"'))
    y = 24
    s += f'<rect x="{x0}" y="{y}" width="{W_}" height="20" fill="#F1F3F4" stroke="#DADCE0"/>'
    lts = _letters([c for c, *_ in scol], rows.columns)            # 원본 파일의 열 글자 (숨긴 열은 건너뜀)
    for i, (c, w, _) in enumerate(scol):
        cx = xs[c][0]
        s += f'<line x1="{cx}" y1="{y}" x2="{cx}" y2="{y + 20}" stroke="#DADCE0"/>' + _t(cx + w / 2, y + 10, lts[i], "ts", extra='style="font-size:11px"')
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
        for c, w, num in scol:
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
    """수치형 — 엑셀 시트의 무게 열 → 8칸이 수직선 위 점으로 → 600개를 10g 구간별 개수 막대(히스토그램)로 → 평균 · 퍼짐. 20초 · 한 번."""
    d = _D("vn", 20)
    rows = _rows8(df)
    sh, cells, W_ = _sheet(d, rows, len(df), "무게", 6)
    v_all = df["무게"]
    m, sd = v_all.mean(), v_all.std()
    X0, X1, V0, V1, STEP = W_ + 70, 1150, 200, 380, 10
    vx = lambda v: X0 + (v - V0) / (V1 - V0) * (X1 - X0)  # noqa: E731
    ay, H = 300, 200
    s = sh + f'<g {d.show(6)}>' + _t(X0, 20, "무게 · 단위 g · 수치형", "to", "start", 'style="font-size:17px"') + "</g>"
    s += f'<g {d.show(14)}><line x1="{X0}" y1="{ay}" x2="{X1}" y2="{ay}" stroke="{N}" stroke-width="2.5"/>'
    for t in range(V0, V1 + 1, STEP):
        s += f'<line x1="{vx(t):.1f}" y1="{ay}" x2="{vx(t):.1f}" y2="{ay + (6 if t % 40 else 12)}" stroke="{N}" stroke-width="1.5"/>'
        if t % 40 == 0:
            s += _t(vx(t), ay + 26, t, "ts", extra='style="font-size:13px"')
    s += _t(X1, ay + 26, "g", "ts", "start", 'style="font-size:13px"') + "</g>"
    # 1) 첫 8칸 → 점 (구간 막대가 나오면 사라짐)
    lv, last = {}, []
    for i in sorted(range(len(rows)), key=lambda j: rows["무게"].iloc[j]):
        x = vx(rows["무게"].iloc[i])
        k = next((k for k, lx in enumerate(last) if x - lx > 60), len(last))
        last[k:k + 1] = [x]
        lv[i] = k
    for i, (_, row) in enumerate(rows.iterrows()):
        t = 20 + i * 3.2
        cx, cy, w = cells[(i, "무게")]
        v = row["무게"]
        s += f'<rect x="{cx}" y="{cy}" width="{w}" height="{_RH}" fill="{O}" fill-opacity=".22" {d.show(t)}/>'
        s += f'<g {d.show(t, 49)}><circle cx="{vx(v):.1f}" cy="{ay - 14 - lv[i] * 24}" r="9" fill="{O}"/>' \
             f'{_t(vx(v) + 13, ay - 14 - lv[i] * 24, v, "ts", "start", "style=font-size:13px")}</g>'
    # 2) 600개 → 10g 구간별 개수 막대
    edges = list(range(V0, V1 + STEP, STEP))
    cnt = [int(((v_all >= lo) & (v_all < lo + STEP)).sum()) for lo in edges[:-1]]
    mx = max(cnt)
    grow = "transform-box:fill-box;transform-origin:50% 100%"
    st = [(0, "transform:scaleY(0)"), (52, "transform:scaleY(0)"), (60, "transform:scaleY(1)"), (100, "transform:scaleY(1)")]
    for lo, c in zip(edges[:-1], cnt):
        if not c:
            continue
        h = H * c / mx
        s += f'<rect x="{vx(lo) + 1:.1f}" y="{ay - h:.1f}" width="{vx(lo + STEP) - vx(lo) - 2:.1f}" height="{h:.1f}" fill="{K}" fill-opacity=".8" {d.a(st, "ease-out", grow)}/>'
    s += (f'<g {d.show(56)}>' + _t(X0, ay - H - 18, f"{len(df)}개 · {STEP}g 구간마다 개수", "tn", "start", 'style="font-size:15px"') + "</g>")
    # 3) 평균 · 퍼짐
    s += (f'<g {d.show(66)}><line x1="{vx(m):.1f}" y1="{ay - H - 8}" x2="{vx(m):.1f}" y2="{ay + 4}" stroke="{O}" stroke-width="3" stroke-dasharray="7 5"/>'
          + _t(vx(m) + 8, ay - H - 18, f"평균 {m:.1f}g", "to", "start", 'style="font-size:17px"') + "</g>")
    a_, b_ = vx(m - sd), vx(m + sd)
    s += (f'<g {d.show(80)}><path d="M{a_:.1f} {ay + 44} V{ay + 56} H{b_:.1f} V{ay + 44}" fill="none" stroke="{K}" stroke-width="2.5"/>'
          + _t((a_ + b_) / 2, ay + 78, f"퍼짐 · 표준편차 {sd:.1f}g", "tn", extra='style="font-size:16px"')
          + _t(vx(v_all.min()), ay + 104, f"최솟값 {v_all.min()}", "ts")
          + _t(vx(v_all.max()), ay + 104, f"최댓값 {v_all.max()}", "ts") + "</g>")
    return d.svg(1160, 420, s)


def cat_anim(df):
    """범주형 — 엑셀 시트의 위치 열 → 8칸이 위치 색으로 칠해지며 위치별로 한 칸씩 쌓임 → 600개 막대 → 상품 비율. 18초 · 한 번."""
    d = _D("vc", 18)
    rows = _rows8(df)
    sh, cells, W_ = _sheet(d, rows, len(df), "위치", 6)
    names = sk.AREA
    cnt = df["위치"].value_counts()
    on = df[df["등급"] == "상품"]["위치"].value_counts()
    L = W_ + 60
    bx = {n: L + 80 + i * 200 for i, n in enumerate(names)}
    base, H = 360, 230
    s = sh + f'<g {d.show(6)}>' + _t(L, 20, "위치 · 과수원 구역 · 범주형", "to", "start", 'style="font-size:17px"') + "</g>"
    s += f'<line x1="{L}" y1="{base}" x2="1150" y2="{base}" stroke="{N}" stroke-width="2.5" {d.show(14)}/>'
    for n in names:
        s += f'<g {d.show(14)}>' + _t(bx[n], base + 26, n, "tt", extra=f'style="font-size:19px;fill:{_ACOL[n]}"') + "</g>"
    seen = {n: 0 for n in names}
    for i, (_, row) in enumerate(rows.iterrows()):
        t = 20 + i * 3.2
        a = row["위치"]
        cx, cy, w = cells[(i, "위치")]
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


def map_anim(df):
    """위치 데이터 — 엑셀 시트의 가로칸 · 세로칸 → 지도의 칸 (8칸이 차례로) → 600칸 전체를 등급 색으로 → 가장자리 띠에 불량이 몰림. 20초 · 한 번."""
    d = _D("vm", 20)
    rows = _rows8(df)
    scol = [("사과번호", 100, False), ("가로칸", 72, True), ("세로칸", 72, True), ("위치", 84, False), ("등급", 66, False)]
    sh, cells, W_ = _sheet(d, rows, len(df), "가로칸", 6, scol)
    x2, _, w2 = cells[(0, "세로칸")]
    sh += f'<rect x="{x2}" y="44" width="{w2}" height="{26 + 8 * _RH}" fill="none" stroke="{O}" stroke-width="3" {d.show(6)}/>'
    nx, ny = int(df["가로칸"].max()), int(df["세로칸"].max())
    C, X0, Y0 = 14, W_ + 90, 52
    gx = lambda x: X0 + (x - 1) * C  # noqa: E731
    gy = lambda y: Y0 + (ny - y) * C  # noqa: E731
    col = lambda g: "#2BA84A" if g == "상품" else "#E8344E"  # noqa: E731
    s = sh + f'<g {d.show(6)}>' + _t(X0, 20, "가로칸 · 세로칸 → 지도의 칸 · 색 = 등급", "to", "start", 'style="font-size:17px"') + "</g>"
    s += f'<g {d.show(14)}>' + "".join(f'<rect x="{gx(r["가로칸"])}" y="{gy(r["세로칸"])}" width="{C - 2}" height="{C - 2}" rx="2" fill="#E1E5EB"/>'
                                     for _, r in df.iterrows()) + "</g>"
    for i, (_, r) in enumerate(rows.iterrows()):
        t = 20 + i * 3.5
        for c_ in ("가로칸", "세로칸"):
            cx, cy, w = cells[(i, c_)]
            s += f'<rect x="{cx}" y="{cy}" width="{w}" height="{_RH}" fill="{O}" fill-opacity=".22" {d.show(t)}/>'
        s += (f'<rect x="{gx(r["가로칸"]) - 2}" y="{gy(r["세로칸"]) - 2}" width="{C + 2}" height="{C + 2}" rx="3" fill="{col(r["등급"])}" '
              f'stroke="{N}" stroke-width="2" {d.show(t)}/>')
    s += f'<g {d.show(56)}>' + "".join(f'<rect x="{gx(r["가로칸"])}" y="{gy(r["세로칸"])}" width="{C - 2}" height="{C - 2}" rx="2" fill="{col(r["등급"])}"/>'
                                     for _, r in df.iterrows()) + "</g>"
    # 가장자리 띠 (바깥 두 줄) · 불량 몰림
    ring = df.apply(lambda r: min(r["가로칸"] - 1, nx - r["가로칸"], r["세로칸"] - 1, ny - r["세로칸"]) + 1, axis=1)
    k = int(df[df["위치"] == "가장자리"]["등급"].ne("상품").sum())
    n = int((df["위치"] == "가장자리").sum())
    k2 = int(df[df["위치"] != "가장자리"]["등급"].ne("상품").sum())
    band = int(ring[df["위치"] == "가장자리"].max())
    w_, h_ = nx * C, ny * C
    s += (f'<g {d.show(74)}><rect x="{X0 - 4}" y="{Y0 - 4}" width="{w_ + 6}" height="{h_ + 6}" fill="none" stroke="{N}" stroke-width="2.5" stroke-dasharray="7 5"/>'
          f'<rect x="{X0 + band * C - 3}" y="{Y0 + band * C - 3}" width="{w_ - 2 * band * C + 4}" height="{h_ - 2 * band * C + 4}" fill="none" stroke="{N}" stroke-width="2.5" stroke-dasharray="7 5"/>'
          + _t(X0, Y0 + h_ + 30, f"가장자리 띠(바깥 {band}줄) · 불량 {k} / {n}", "to", "start", 'style="font-size:16px"')
          + _t(X0, Y0 + h_ + 56, f"나머지 안쪽 · 불량 {k2} / {len(df) - n}", "tn", "start", 'style="font-size:15px"') + "</g>")
    return d.svg(1160, 430, s)


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
    """사과 A07 · 멍 → 벌레 먹음 → 무게 미달 → 당도 미달 → 상품 (labs/make_apple.py judge 순서). 사유마다 한 개 + 상품 둘."""
    df = _d07()
    w, b = sk.MIN_W, sk.MIN_SUGAR
    steps = [("멍", "멍 = 1", "", lambda r: ["멍"] if r["멍"] else []),
             ("벌레 먹음", "벌레 = 1", "", lambda r: ["벌레"] if r["벌레"] else []),
             ("무게 미달", f"무게 &lt; {w}", f"{w}g", lambda r: ["무게"] if r["무게"] < w else []),
             ("당도 미달", f"당도 &lt; {b:g}", f"{b:g} brix", lambda r: ["당도"] if r["당도"] < b else [])]
    cols = ["멍", "벌레", "무게", "당도"]
    df = df.assign(n=df["멍"] + df["벌레"] + (df["무게"] < w) + (df["당도"] < b))
    pick = [df[df["불량사유"] == "없음"].iloc[i] for i in (0, 1)]
    for rs in sk.D_ORDER:
        pick.append(df[df["불량사유"] == rs].sort_values("n", ascending=False).iloc[0])
    pick = pd.DataFrame(pick).sort_values("사과번호")
    return judge_build(pick, ("사과번호", lambda r: r["사과번호"]), cols, steps, ("남은 행", "상품", "", "상품"))
