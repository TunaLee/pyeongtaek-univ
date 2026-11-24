"""3교시 HTML 첫 화면 · Plan Mode.

도입(완성 시뮬레이터 · 엑셀 화면과 웹 화면 · 웹 화면의 세 부분) → 설명(한 파일 안의 위치 · 예시 파일 고쳐 보기 · 바로 실행과 계획 먼저 · Plan Mode · 권한 모드)
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
"""

HTML = """<h1>W07 수율</h1>
<div class="card">수율
  <span id="y">-</span></div>"""
CSS_ = """.card { border-radius: 12px;
  box-shadow: 0 2px 10px #0002; }
#y { color: #2BA84A; }"""
JS = f"""const y = {WN['pass']} / {WN['rows']} * 100;
document.getElementById("y")
  .textContent = y.toFixed(2) + "%";"""

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


def _hcj():
    pv_h = '<div class="pv"><div style="font-size:22px;font-weight:800">W07 수율</div><div>수율</div><div>-</div></div>'
    pv_c = ('<div class="pv"><div style="font-size:22px;font-weight:800">W07 수율</div><div style="margin-top:8px;padding:12px;border-radius:12px;'
            'box-shadow:0 2px 10px rgba(0,0,0,.12)"><b>수율</b><div style="color:#2BA84A;font-size:30px;font-weight:800">-</div></div></div>')
    pv_j = ('<div class="pv"><div style="font-size:22px;font-weight:800">W07 수율</div><div style="margin-top:8px;padding:12px;border-radius:12px;'
            f'box-shadow:0 2px 10px rgba(0,0,0,.12)"><b>수율</b><div style="color:#2BA84A;font-size:30px;font-weight:800">{WN["yield"]:.2f}%</div></div></div>')
    snip = lambda t: f'<pre class="sksn">{esc(t)}</pre>'  # noqa: E731
    cols = [("HTML", "뼈대 · 무엇이 있나", snip(HTML), pv_h), ("CSS", "꾸밈 · 어떻게 보이나", snip(CSS_), pv_c),
            ("JS", "동작 · 계산 · 바꿈", snip(JS), pv_j)]
    return '<div class="skhcj">' + "".join(
        f'<div style="--d:{.3 + i * 2.2:.1f}s"><b>{h}<small>{s}</small></b>{c}{p}</div>' for i, (h, s, c, p) in enumerate(cols)) + "</div>"


def slides():
    return [
        # ── 도입
        light("완성 시뮬레이터", sk.duo("sim/apple_s8.webp", "sim/wafer_s8.webp", "사과 상품률 시뮬레이터", "웨이퍼 수율 시뮬레이터"), T),
        light("엑셀 화면과 웹 화면", viz2.pair(
            "엑셀 화면", [("화면 구성", "표 · 차트 · 수식"), ("기준 바꾸기", "수식 · 필터를 다시 손봄"), ("나누기", "엑셀이 있어야 열림")],
            "웹 화면 · HTML", [("화면 구성", "숫자 카드 · 지도 · 차트 · 조절 바"), ("기준 바꾸기", "조절 바 → 화면이 바로 다시 그려짐"),
                              ("나누기", "파일 하나 · 브라우저만 있으면 열림")]), T),
        light("웹 화면의 세 부분", _hcj(), T),
        # ── 설명
        light("한 파일 안의 위치", '<div class="twocol w"><div>' + code("simulator.html", esc(ONEFILE)) + "</div><div>"
              + viz2.tiles([("&lt;style&gt;", "꾸밈 · head 안"), ("본문 태그", "뼈대 · body 안"), ("&lt;script&gt;", "동작 · body 끝")], 1)
              + "</div></div>", T),
        light("예시 파일 고쳐 보기", viz2.maprows([
            ("브라우저로 열기", "html_css_js_예시.html 더블클릭", "화면"), ("메모장 · VS Code 로 열기", "같은 파일", "글자"),
            ("색 한 줄 바꾸기", "#2BA84A → #E8344E", "저장 → 새로 고침"), ("세 구역 찾기", "style · body · script", "위치 확인")], "할 일", "결과"), T),
        light("바로 실행과 계획 먼저", viz2.pair(
            "바로 실행", [("요청 직후", "파일을 바로 작성"), ("화면 구성 · 계산", "Claude 가 정함"), ("마음에 안 들면", "다시 만들기 · 되돌리기")],
            "계획 먼저", [("요청 직후", "만들 파일 · 화면 구성 · 순서만 보여 줌"), ("고칠 곳", "계획에 말로 수정"),
                        ("승인 후", "그때 파일 작성")]), T),
        light("Plan Mode", viz2.tiles([
            ("켜는 법", "Shift + Tab 두 번 · 입력창 아래 plan mode"), ("계획 내용", "만들 파일 · 화면 구성 · 계산 방법 · 순서"),
            ("승인", "계획 확인 → 실행 선택 · 그때 파일 작성"), ("쓰는 때", "새 화면 · 여러 파일을 바꾸기 전")], 2)
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
