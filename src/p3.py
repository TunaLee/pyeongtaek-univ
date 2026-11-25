"""3교시 HTML 첫 화면 · Plan Mode.

도입(완성 시뮬레이터 · 엑셀 화면과 웹 화면 · 웹의 3요소 — HTML만 → + CSS → + JS 화면) → 설명(3요소가 들어가는 곳 · 예시 파일 고쳐 보기 · 바로 실행과 계획 먼저 · Plan Mode · 권한 모드)
→ 적용(실습 3-1 사과 숫자 카드 → 3-2 웨이퍼 숫자 카드 · 꾸밈 전후).
"""
import sk
import viz2
from deck import lab, light
from hx import code, esc
from pkit import brief, tag
from stats_hx import src

T = tag("3")
WN, DN = sk.WN, sk.DN
CSS = """
  .sksn{margin:0; background:#1E1E2E; color:#E6E6E6; border-radius:10px; padding:12px 14px; font-family:var(--mono); font-size:13px; line-height:1.6; white-space:pre; overflow:hidden;}
  /* 웹의 3요소 — HTML만 → + CSS → + JS · 같은 화면이 바뀜 */
  .p3w{display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:20px; align-items:start;}
  .p3wc{display:flex; flex-direction:column; gap:10px; opacity:0; animation:p3wIn .5s var(--d) forwards;}
  @keyframes p3wIn{from{opacity:0; transform:translateY(10px)} to{opacity:1; transform:none}}
  .p3wh{display:flex; align-items:baseline; gap:10px;} .p3wh b{font-size:21px; color:#16233A;} .p3wh span{font-size:14px; color:#6B7785;}
  .p3wc.p3wOn .p3wh b{color:#E07A12;}
  .p3wb{border:1.5px solid #C9CFD8; border-radius:10px; overflow:hidden; background:#fff; height:262px; box-shadow:0 2px 8px rgba(0,0,0,.06);}
  .p3wb .p3wBar{display:flex; align-items:center; gap:5px; height:26px; padding:0 10px; background:#EEF1F4; border-bottom:1px solid #D9DDE3;}
  .p3wb .p3wBar i{width:9px; height:9px; border-radius:50%; background:#C9CFD8;}
  .p3wb .p3wBar span{margin-left:8px; font-size:11.5px; color:#6B7785; font-family:var(--mono);}
  .p3w .p3wR{font-family:"Times New Roman",Times,serif; color:#000; padding:8px 12px; font-size:15px; line-height:1.35;}
  .p3w .p3wR h1{font-size:24px; font-weight:700; margin:4px 0 8px; color:#000; font-family:inherit;} .p3w .p3wR p{margin:0 0 6px;}
  .p3w .p3wR .p3wRng{display:inline-block; vertical-align:middle; width:96px; height:4px; background:#9A9A9A; border-radius:2px; position:relative; margin:0 6px;}
  .p3w .p3wR .p3wRng i{position:absolute; left:30%; top:-5px; width:13px; height:13px; border-radius:50%; background:#E9E9E9; border:1px solid #767676;}
  .p3w .p3wS{color:#16233A; font-size:13px;}
  .p3w .p3wS .p3wHd{background:#1F3A5F; color:#fff; font-weight:800; font-size:15px; padding:9px 14px;}
  .p3w .p3wS .p3wCs{display:grid; grid-template-columns:repeat(3,1fr); gap:8px; padding:10px 12px 4px;}
  .p3w .p3wS .p3wCd{border-radius:10px; box-shadow:0 2px 8px rgba(0,0,0,.14); padding:7px 9px; background:#fff;}
  .p3w .p3wS .p3wCd span{display:block; font-size:11px; color:#6B7785;}
  .p3w .p3wS .p3wCd b{display:block; position:relative; height:24px; font-size:19px; font-weight:800;} .p3w .p3wS .p3wCd b.p3wG{color:#2BA84A;}
  .p3w .p3wS .p3wSl{display:grid; grid-template-columns:auto 1fr 38px; gap:9px; align-items:center; padding:8px 12px;}
  .p3w .p3wS .p3wSl span{font-size:12px; font-weight:700;}
  .p3w .p3wS .p3wSl em{font-style:normal; font-weight:800; color:#E07A12; position:relative; height:18px;}
  .p3w .p3wS .p3wTr{height:6px; border-radius:3px; background:#F6C99A; position:relative;}
  .p3w .p3wS .p3wTh{position:absolute; left:33%; top:-6px; width:18px; height:18px; margin-left:-9px; border-radius:50%; background:#fff; border:3px solid #F28C28; box-sizing:border-box;}
  .p3w .p3wS .p3wCh{padding:2px 12px;} .p3w .p3wS .p3wCh > span{font-size:11.5px; font-weight:700; color:#6B7785;}
  .p3w .p3wS .p3wRow{display:grid; grid-template-columns:54px 1fr 50px; gap:6px; align-items:center; font-size:11px; margin-top:5px;}
  .p3w .p3wS .p3wRow em{font-style:normal; position:relative; height:14px; font-weight:700;}
  .p3w .p3wS .p3wBk{height:10px; background:#EEF1F4; border-radius:3px; position:relative; overflow:hidden;}
  .p3w .p3wS .p3wBk i{position:absolute; left:0; top:0; bottom:0; border-radius:3px; width:var(--w0);}
  .p3w .p3wA, .p3w .p3wB{position:absolute; left:0; top:0; font-style:normal; white-space:nowrap;}
  .p3w .p3wA{animation:p3wA .4s var(--d) forwards;} .p3w .p3wB{opacity:0; animation:p3wB .4s var(--d) forwards;}
  @keyframes p3wA{to{opacity:0}} @keyframes p3wB{to{opacity:1}}
  .p3w .p3wMv{animation:p3wMv 1s ease-in-out var(--d) forwards;} @keyframes p3wMv{to{left:var(--x1)}}
  .p3w .p3wBk i.p3wJs{animation:p3wW 1s ease-in-out var(--d) forwards;} @keyframes p3wW{to{width:var(--w1)}}
  @media print{.p3wc{animation:none; opacity:1} .p3w .p3wA{animation:none; opacity:0} .p3w .p3wB{animation:none; opacity:1}
    .p3w .p3wMv{animation:none; left:var(--x1)} .p3w .p3wBk i.p3wJs{animation:none; width:var(--w1)}}
"""

ONEFILE = """<!doctype html>
<html>
<head>
  <style>   … 꾸밈 (CSS) …   </style>
</head>
<body>
  … 뼈대 (HTML) …
  <script>  … 동작 (JS) …    </script>
</body>
</html>"""


def _web3():
    """HTML만 → HTML + CSS → HTML + CSS + JS · 같은 사과 상품률 화면이 바뀜.
    JS 칸에서는 조절 바(당도 하한)가 11 → 12 로 움직이면 상품 · 상품률 · 위치별 막대가 다시 계산된다. 숫자는 sk.d_rate 로 계산."""
    import pbg
    df = sk.D07
    n = len(df)
    s0, s1 = sk.MIN_SUGAR, 12.0
    (p0, r0), (p1, r1) = sk.d_rate(df, sugar=s0), sk.d_rate(df, sugar=s1)
    z0 = DN["area"]
    z1 = {a: round((sk.d_judge(g, sugar=s1) == "없음").mean() * 100, 2) for a, g in df.groupby("위치")}
    lo, hi = 9.0, 15.0
    pos = lambda v: f"{(v - lo) / (hi - lo) * 100:.0f}%"  # noqa: E731
    title = "사과 상품률 시뮬레이터"
    raw = (f'<div class="p3wR"><h1>{title}</h1><p>전체 {n}</p><p>상품 -</p><p>상품률 -</p>'
           f'<p>당도 하한<span class="p3wRng"><i></i></span>{s0:.1f}</p><p>위치별 상품률</p></div>')
    swap = lambda x, y: f'<i class="p3wA">{x}</i><i class="p3wB">{y}</i>'  # noqa: E731

    def page(js):
        pv = swap(p0, p1) if js else "-"
        rv = swap(f"{r0:.2f}%", f"{r1:.2f}%") if js else "-"
        sv = swap(f"{s0:.1f}", f"{s1:.1f}") if js else f"{s0:.1f}"
        rows = ""
        for a in sk.AREA:
            bar = (f'<i class="p3wJs" style="--w0:{z0[a]:.0f}%;--w1:{z1[a]:.0f}%;background:{pbg.ZCOL[a]}"></i>' if js else "")
            val = swap(f"{z0[a]:.2f}%", f"{z1[a]:.2f}%") if js else "-"
            rows += f'<div class="p3wRow"><span>{a}</span><div class="p3wBk">{bar}</div><em>{val}</em></div>'
        th = f'<i class="p3wTh{" p3wMv" if js else ""}" style="left:{pos(s0)};--x1:{pos(s1)}"></i>'
        dst = ' style="--d:6.3s"' if js else ""                        # JS 칸 · 조절 바가 움직이는 시점
        return (f'<div class="p3wS"{dst}><div class="p3wHd">{title}</div>'
                f'<div class="p3wCs"><div class="p3wCd"><span>전체</span><b>{n}</b></div><div class="p3wCd"><span>상품</span><b>{pv}</b></div>'
                f'<div class="p3wCd"><span>상품률</span><b class="p3wG">{rv}</b></div></div>'
                f'<div class="p3wSl"><span>당도 하한</span><div class="p3wTr">{th}</div><em>{sv}</em></div>'
                f'<div class="p3wCh"><span>위치별 상품률</span>{rows}</div></div>')
    code_h = f"""<h1>{title}</h1>
<p>상품률 <b id="rate">-</b></p>
<input type="range" id="sugar">"""
    code_c = """h1 { background: #1F3A5F;
     color: #fff; }
.card { border-radius: 10px;
  box-shadow: 0 2px 8px #0002; }"""
    code_j = f"""const rate = {p0} / {n} * 100;
document.getElementById("rate")
  .textContent = rate.toFixed(2) + "%";"""
    cols = [("HTML만", "뼈대 · 내용", raw, code_h), ("+ CSS", "꾸밈 · 배치 · 색", page(False), code_c),
            ("+ JS", "계산 · 조절 바 동작", page(True), code_j)]
    return '<div class="p3w">' + "".join(
        f'<div class="p3wc{" p3wOn" if i == 2 else ""}" style="--d:{.3 + i * 2:.1f}s"><div class="p3wh"><b>{h}</b><span>{sub}</span></div>'
        f'<div class="p3wb"><div class="p3wBar"><i></i><i></i><i></i><span>예시.html</span></div>{pg}</div>'
        f'<pre class="sksn">{esc(code)}</pre></div>'
        for i, (h, sub, pg, code) in enumerate(cols)) + "</div>"


def slides():
    return [
        # ── 도입
        light("완성 시뮬레이터", sk.duo("sim/apple_s8.webp", "sim/wafer_s8.webp", "사과 상품률 시뮬레이터", "웨이퍼 수율 시뮬레이터"), T),
        light("엑셀 화면과 웹 화면", viz2.pair(
            "엑셀 화면", [("화면 구성", "표 · 차트 · 수식"), ("기준 바꾸기", "수식 · 필터를 다시 손봄"), ("나누기", "엑셀이 있어야 열림")],
            "웹 화면 · HTML", [("화면 구성", "숫자 카드 · 지도 · 차트 · 조절 바"), ("기준 바꾸기", "조절 바 → 화면이 바로 다시 그려짐"),
                              ("나누기", "파일 하나 · 브라우저만 있으면 열림")]), T),
        light("웹의 3요소", _web3(), T),
        # ── 설명
        light("3요소가 들어가는 곳", '<div class="twocol w"><div>' + code("simulator.html", esc(ONEFILE)) + "</div><div>"
              + viz2.tiles([("&lt;style&gt;", "꾸밈 · head 안"), ("본문 태그", "뼈대 · body 안"), ("&lt;script&gt;", "동작 · body 끝")], 1)
              + "</div></div>", T),
        light("예시 파일 고쳐 보기", viz2.maprows([
            ("브라우저로 열기", "html_css_js_예시.html 더블클릭", "화면"), ("메모장 · VS Code 로 열기", "같은 파일", "글자"),
            ("색 한 줄 바꾸기", "#2BA84A → #E8344E", "저장 → 새로 고침"), ("세 구역 찾기", "style · body · script", "위치 확인")], "할 일", "결과"), T),
        light("계획부터 보기", viz2.pair(
            "바로 실행", [("요청 직후", "파일을 바로 작성"), ("화면 구성 · 계산", "Claude 가 정함"), ("마음에 안 들면", "다시 만들기 · 되돌리기")],
            "계획 먼저", [("요청 직후", "만들 파일 · 화면 구성 · 순서만 보여 줌"), ("고칠 곳", "계획에 말로 수정"),
                        ("승인 후", "그때 파일 작성")]), T),
        light("Plan Mode", viz2.tiles([
            ("켜기", "Shift + Tab 두 번 · 입력창 아래 plan mode"), ("계획 내용", "만들 파일 · 화면 구성 · 계산 방법 · 순서"),
            ("승인", "계획 확인 → 실행 선택 · 그때 파일 작성"), ("사용 시점", "새 화면 · 여러 파일을 바꾸기 전")], 2)
              + src(("Claude Code 문서 · Permission modes", "https://code.claude.com/docs/en/permission-modes")), T),
        light("권한 모드", viz2.maprows([
            ("기본", "파일 수정 · 명령 실행 전에 물어봄", "처음 쓸 때"), ("자동 수락", "파일 수정은 묻지 않음", "익숙해진 뒤"),
            ("Plan", "읽기만 · 계획만", "큰 변경 전")], "모드", "동작")
              + src(("Claude Code 문서 · Permission modes", "https://code.claude.com/docs/en/permission-modes")), T),
        # ── 적용
        lab("3-1", "사과 숫자 카드", T, "사과 CSV 로 전체 · 상품 · 불량 · 상품률 카드 4개 화면을 만들고 꾸밈을 넣는다",
            ["Plan Mode 로 계획 받기", "꾸밈 없이 숫자 4개 화면", "CSS 로 카드 4장", "말로 색 · 크기 바꾸기 · 되돌리기"],
            [f"{DN['rows']} · {DN['pass']} · {DN['fail']} · {DN['rate']}%", "output/apple_sim.html"], files="output/apple_A07.csv"),
        light("사과 카드 전후", sk.duo("sim/apple_s3a.webp", "sim/apple_s3b.webp", "꾸밈 전", "꾸밈 후"), T),
        lab("3-2", "웨이퍼 숫자 카드", T, "W07 CSV 로 숫자 카드 4개 simulator.html 을 만들고 꾸밈을 넣는다",
            ["Plan Mode 로 계획 받기", "꾸밈 없이 숫자 4개 화면", "CSS 로 카드 4장", "말로 색 · 크기 바꾸기 · 되돌리기"],
            [f"{WN['rows']} · {WN['pass']} · {WN['fail']} · {WN['yield']}%", "output/simulator.html"], files="output/wafer_test_W07.csv"),
        brief("3-2", T,
              ["Plan Mode 로 계획 받기", "뼈대 · 계산 요청", "꾸밈 요청", "색 · 크기 바꾸기"],
              [("목표", "제목 + 숫자 카드 4개"), ("입력", "output/wafer_test_W07.csv"),
               ("산출물", "output/simulator.html 한 파일"), ("하지 말 것", "외부 라이브러리 · 파일 여러 개")],
              [], [f"수율 {WN['yield']}%", "브라우저 새로 고침으로 확인"], ""),
        light("웨이퍼 카드 전후", sk.duo("sim/wafer_s3a.webp", "sim/wafer_s3b.webp", "꾸밈 전", "꾸밈 후"), T),
    ]
