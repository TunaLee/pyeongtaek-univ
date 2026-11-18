"""1교시 반도체 테스트 데이터와 Claude Code.

배경(2026 반도체 숫자 · 웨이퍼와 다이 · 공정 흐름 · CP 테스트 · 테스트 → CSV) → 데이터 읽기(열 네 묶음 · 수도꼭지 비유 · 판정 순서 · 수율)
→ Claude Code(대화형과 위임형 · 데이터 작업 고리 · 사내 사례 · CLAUDE.md · 데이터 사전) → 실습 1.
숫자는 labs/ref.json · labs/solution 에서 읽는다.
"""
import pviz
import viz2
from deck import lab, light
from hx import code, esc, note
from pkit import REF, SOL, W, brief, chat, tag
from stats_hx import big, src

T = tag("1")
W07 = W("W07")
FAIL07 = W07["crack"] + W07["open_short"] + W07["leakage"] + W07["vth_shift"] + W07["particle"] + W07["parametric"]


def _claude_md():
    """CLAUDE.md 에서 판정 규칙 · 작업 규칙 두 칸만 (코드 10줄 이내)."""
    t = (SOL / "CLAUDE.md").read_text(encoding="utf-8")
    keep = t[t.index("## 판정 규칙"):].strip().split("\n")
    return "\n".join(x for x in keep if x.strip())[:2000]


CSS = """
  .p1grp{display:grid; grid-template-columns:repeat(4,1fr); gap:14px; margin-top:8px;}
  .p1g{border-radius:14px; padding:16px 16px 14px; border:2px solid #C9D6E6; background:#fff; opacity:0; animation:p1In .45s var(--d) forwards;}
  .p1g b{display:block; font-size:21px; color:#16233A; margin-bottom:10px;}
  .p1g code{display:block; font-family:var(--mono); font-size:14.5px; color:#1F3A5F; background:#F4F6F9; border-radius:6px; padding:3px 8px; margin:4px 0;}
  .p1g small{display:block; margin-top:10px; font-size:14.5px; color:#6B7785;}
  .p1g.k{border-color:#F28C28; background:#FFF8F0;}
  @keyframes p1In{from{opacity:0; transform:translateY(10px)} to{opacity:1; transform:none}}
  @media print{.p1g{opacity:1; animation:none}}
"""


def _groups():
    gs = [("식별", ["lot_id", "wafer_id"], "어느 LOT · 웨이퍼", ""),
          ("위치", ["die_x · die_y", "center_x_mm · center_y_mm", "radius_mm · zone"], "웨이퍼 위 어디", ""),
          ("측정", ["vth_v · idsat_ma · ioff_na", "rc_ohm · ox_thk_nm", "crack · particle_cnt"], "전기 · 검사 값", "k"),
          ("판정", ["bin", "fail_type", "pass_fail"], "측정값 → 양품 · 불량", "")]
    return '<div class="p1grp">' + "".join(
        f'<div class="p1g {k}" style="--d:{.2 + i * .35:.2f}s"><b>{h}</b>{"".join(f"<code>{c}</code>" for c in cs)}<small>{t}</small></div>'
        for i, (h, cs, t, k) in enumerate(gs)) + "</div>"


def slides():
    return [
        light("데이터 용어", viz2.maprows([
            ("다이", "CSV 한 행", f"웨이퍼 한 장 {REF['gross_die']}행"), ("웨이퍼", "CSV 파일 하나", "W01 ~ W25"),
            ("LOT", "파일 묶음", "LOT2611-07 · 25장"), ("Bin · pass_fail", "판정 열", "1 = 양품")], "용어", "데이터"), T),
        light("테스트 결과가 CSV 가 되는 과정", pviz.test_to_csv(), T),
        # ── 데이터 읽기
        light("열 18개 네 묶음", _groups(), T),
        light("판정 순서", pviz.sieve(), T),
        light("수율", big([
            (f"{W07['pass']}", "개", "양품 다이 (PASS)"), (f"{REF['gross_die']}", "개", "전체 다이"),
            (f"{W07['yield']}", "%", "수율 = 양품 ÷ 전체 · W07", True)], 3), T),
        light("데이터 규모", viz2.tiles([
            ("웨이퍼 한 장", f"{REF['gross_die']}행 × 18열"), ("LOT 하나", f"25장 · {REF['gross_die'] * 25:,}행"),
            ("공정 센서 (SECOM)", f"{REF['secom']['rows']:,}행 × {REF['secom']['features']}열")], 3), T),
        # ── Claude Code
        light("Claude 와 Claude Code", viz2.pair(
            "Claude (claude.ai)", [("하는 일", "질문에 글로 답함"), ("CSV", "붙여 넣은 만큼만 봄"), ("결과", "사람이 복사 · 실행")],
            "Claude Code", [("하는 일", "내 폴더의 파일을 읽고 실행"), ("CSV", "파일을 직접 열어 계산"), ("결과", "스크립트 · 엑셀 · HTML 파일")]), T),
        light("Claude Code 의 데이터 작업 고리", pviz.data_loop()
              + src(("Claude Code 문서 · How Claude Code works", "https://code.claude.com/docs/en/how-claude-code-works")), T),
        light("Anthropic 사내 데이터 분석", big([
            ("95", "%", "Claude 로 처리하는 분석 질의 비율", True), ("21", "% 이하", "스킬 · 정의 없을 때 정확도"),
            ("95 → 65", "%", "관리하지 않은 한 달 뒤 정확도")], 3)
              + src(("Claude 블로그 · How Anthropic enables self-service data analytics (2026-06-03)",
                     "https://claude.com/blog/how-anthropic-enables-self-service-data-analytics-with-claude")), T),
        light("CLAUDE.md", '<div class="twocol w"><div>' + code("CLAUDE.md · 예", esc(_claude_md())) + "</div><div>"
              + viz2.tiles([("읽는 때", "Claude Code 시작마다 자동"), ("담는 것", "폴더 · 판정 규칙 · 작업 규칙"),
                            ], 1) + "</div></div>", T),
        light("데이터 사전", viz2.maprows([
            ("열 이름", "vth_v", "문턱전압"), ("단위", "V", "mV 로 들어오면 오류"), ("스펙", "0.38~0.52", "판정 기준"),
            ("기준 숫자", f"{REF['gross_die']} · {W07['pass']} · {W07['yield']}%", "결과 대조용")], "칸", "예"), T),
        light("실습 폴더 wafer-lab", viz2.maprows([
            ("data/", "wafer_test_W07.csv · spec.csv · equipment.csv", "읽기만"), ("data/raw/", "원시 파일 25장", "2 · 6교시"),
            ("docs/", "데이터 사전 · 보고서", "문서"), ("scripts/ · output/", "스크립트 · 결과 파일", "Claude 가 만듦")], "폴더", "내용"), T),
        light("실습 환경", viz2.tiles([
            ("VS Code", "편집기 · 파일 탐색기 · 터미널"), ("Claude Code 확장", "VS Code 확장 · 교육용 계정 로그인"),
            ("Python", "pandas · openpyxl"), ("wafer-lab 폴더", "파일 → 폴더 열기")], 2)
              + src(("Claude Code 문서 · VS Code", "https://code.claude.com/docs/en/vs-code")), T),
        light("요청 한 문장의 구성", viz2.maprows([
            ("대상", "data/wafer_test_W07.csv", "어느 파일"), ("할 일", "행 · 열 · 결측 · 양불 개수 요약", "무엇을"),
            ("결과", "docs/data_dictionary.md", "어디에 남길지"), ("조건", "원본 수정 금지 · 앞 5줄만 출력", "하지 말 것")], "칸", "예"), T),
        # ── 실습
        lab("1", "데이터 사전 · CLAUDE.md", T, "wafer-lab 폴더에서 Claude Code 로 W07 을 읽고 데이터 사전 · CLAUDE.md 를 만든다",
            ["VS Code 로 wafer-lab 열기 · Claude Code 실행", "W07 요약 · 결측 보고 요청", "데이터 사전 작성 요청", "CLAUDE.md 작성 요청",
             "숫자 대조"],
            [f"행 {REF['gross_die']} · 열 18 · 결측 0", f"양품 {W07['pass']} · 수율 {W07['yield']}%", "docs/data_dictionary.md · CLAUDE.md"],
            files="data/wafer_test_W07.csv · data/spec.csv"),
        brief("1", T,
              ["wafer-lab 열기 · Claude Code 실행", "W07 요약 요청 (행 · 열 · 결측)", "데이터 사전 요청", "CLAUDE.md 요청", "엑셀 필터로 양품 수 대조"],
              [("목표", "W07 의 구조 · 열 뜻 · 기준 숫자 정리"), ("입력", "wafer_test_W07.csv · spec.csv"),
               ("산출물", "docs/data_dictionary.md · CLAUDE.md"), ("하지 말 것", "data/ 원본 수정 · CSV 전체 출력")],
              [], [f"양품 {W07['pass']} · 불량 {FAIL07}", "열 18개의 뜻 · 단위 · 스펙"], ""),
        light("실습 1 확인", chat([
            ("me", "data/wafer_test_W07.csv 를 요약해 줘. 행 · 열 수, 결측, 양불 개수만."),
            ("ai", f"616행 × 18열 · 결측 0\nPASS {W07['pass']} · FAIL {FAIL07} · 수율 {W07['yield']}%\n"
                   f"불량 1위 crack {W07['crack']}개 — 대각선 위치에 몰려 있음")], "요약 대화 예"), T),
    ]
