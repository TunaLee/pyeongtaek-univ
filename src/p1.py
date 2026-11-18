"""1교시 반도체 테스트 데이터와 Claude Code.

배경(2026 반도체 숫자 · 웨이퍼와 다이 · 공정 흐름 · CP 테스트 · 테스트 → CSV) → 데이터 읽기(열 네 묶음 · 수도꼭지 비유 · 판정 순서 · 수율)
→ 분석과 엔지니어링 → Claude Code(대화형과 위임형 · 데이터 작업 고리 · 사내 사례 · CLAUDE.md · 데이터 사전) → 실습 1.
숫자는 labs/ref.json · labs/solution 에서 읽는다.
"""
import pviz
import viz2
from deck import lab, light
from hx import code, esc, note
from pkit import REF, SOL, W, brief, chat, tag
from stats_hx import big, src
from v3kit import phmap

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
        # ── 배경 · 반도체와 데이터
        light("2026 반도체 수출", big([
            ("564.4", "억 달러", "2026년 10월 반도체 수출 (월간 역대 2위)", True),
            ("+259.4", "%", "전년 같은 달 대비"),
            ("49", "%", "전체 수출 1,153억 달러 중 반도체")], 3)
              + src(("산업통상부 · 2026년 10월 수출입 동향 (2026-11-01)", "https://www.korea.kr/news/policyNewsView.do?newsId=148974851")), T),
        light("세계 반도체 시장 전망", big([
            ("1.51", "조 달러", "2026년 세계 반도체 시장 (+90%)", True),
            ("8,000", "억 달러+", "메모리 (+약 250%)"),
            ("1.9", "조 달러", "2027년 전망")], 3)
              + src(("WSTS Spring 2026 Forecast (2026-06-02)", "https://www.wsts.org/esraCMS/extension/media/f/WST/7618/WSTS_FC-Release-2026-May.pdf")), T),
        light("웨이퍼와 다이", phmap(
            "wafer_photo.webp", "웨이퍼 · 격자 한 칸이 다이 하나", "사진 · Silicon wafer (Inductiveload) · 퍼블릭 도메인",
            "https://commons.wikimedia.org/wiki/File:Silicon_wafer.jpg",
            viz2.maprows([
                ("웨이퍼", "실리콘 원판", "지름 300 mm"), ("다이 (die)", "웨이퍼 위 칩 한 개", "10 × 10 mm"),
                ("Gross die", "웨이퍼 한 장의 다이 수", f"{REF['gross_die']}개"), ("LOT", "같이 공정을 도는 웨이퍼 묶음", "25장")], "용어", "실습 데이터")), T),
        light("반도체가 만들어지는 순서", pviz.fab_flow(), T),
        light("CP 테스트", phmap(
            "probe_card.webp", "프로브 카드 · 바늘이 다이 패드에 닿음", "사진 · Probe card (Ajoones) · CC BY 3.0",
            "https://commons.wikimedia.org/wiki/File:Probe_card.JPG",
            viz2.maprows([
                ("프로브 카드", "바늘 묶음", "다이 전극에 접촉"), ("측정", "전압 · 전류 · 저항", "다이마다 수십 항목"),
                ("판정", "스펙과 비교", "Bin 번호"), ("기록", "테스터 파일 (STDF)", "→ CSV 로 내려받음")], "단계", "내용")), T),
        light("테스트 결과가 CSV 가 되는 과정", pviz.test_to_csv(), T),
        light("테스트 데이터 용어", viz2.tiles([
            ("CP · Wafer sort", "자르기 전 웨이퍼 상태의 전기 검사"), ("Bin", "판정 번호 · 1 양품 · 2~7 불량 유형"),
            ("STDF", "테스터 결과 파일 표준 형식 (Teradyne)"), ("MES", "공장 생산 기록 시스템 · 데이터를 내려받는 곳")], 2)
              + src(("SemiEngineering · STDF", "https://semiengineering.com/knowledge_centers/test/data-analytics/standard-test-data-format-stdf/")), T),
        # ── 데이터 읽기
        light("열 18개 네 묶음", _groups() + note("한 행", "다이 한 개 · wafer_test_W07.csv = 616행"), T),
        light("비유 · 트랜지스터와 수도꼭지", viz2.maprows([
            ("vth_v · 문턱전압", "꼭지를 얼마나 돌려야 물이 나오나", "0.38~0.52 V"),
            ("idsat_ma · 포화전류", "활짝 열었을 때 물줄기", "0.92 mA 이상"),
            ("ioff_na · 누설전류", "잠갔는데 새는 물", "10 nA 이하"),
            ("rc_ohm · 접촉저항", "배관 이음새가 막힌 정도", "15 Ω 이하")], "측정값", "수도꼭지")
              + note("비전공자", "뜻은 이 정도면 충분 · 스펙 숫자는 spec.csv 에 있음"), T),
        light("판정 순서", pviz.sieve(), T),
        light("수율", big([
            (f"{W07['pass']}", "개", "양품 다이 (PASS)"), (f"{REF['gross_die']}", "개", "전체 다이"),
            (f"{W07['yield']}", "%", "수율 = 양품 ÷ 전체 · W07", True)], 3)
              + note("목표", "이 과정의 목표 수율 90% · 1%p 는 웨이퍼 한 장에 다이 약 6개"), T),
        light("데이터 규모", viz2.tiles([
            ("웨이퍼 한 장", f"{REF['gross_die']}행 × 18열"), ("LOT 하나", f"25장 · {REF['gross_die'] * 25:,}행"),
            ("공정 센서 (SECOM)", f"{REF['secom']['rows']:,}행 × {REF['secom']['features']}열")], 3)
              + note("엑셀로 하는 일", "열고 · 필터 · 피벗 · 복사 — 파일이 늘면 같은 일을 매번 반복"), T),
        light("분석과 엔지니어링", viz2.pair(
            "데이터 분석", [("질문", "W07 수율은 왜 낮은가"), ("결과", "차트 · 원인 후보 · 요약"), ("주기", "질문이 생길 때 한 번")],
            "데이터 엔지니어링", [("질문", "매일 같은 답이 자동으로 나오게"), ("결과", "정제 · 적재 · 집계 스크립트"), ("주기", "파일이 들어올 때마다")]), T),
        # ── Claude Code
        light("Claude 와 Claude Code", viz2.pair(
            "Claude (claude.ai)", [("하는 일", "질문에 글로 답함"), ("CSV", "붙여 넣은 만큼만 봄"), ("결과", "사람이 복사 · 실행")],
            "Claude Code", [("하는 일", "내 폴더의 파일을 읽고 실행"), ("CSV", "파일을 직접 열어 계산"), ("결과", "스크립트 · 엑셀 · HTML 파일")]), T),
        light("Claude Code 의 데이터 작업 고리", pviz.data_loop()
              + src(("Claude Code 문서 · How Claude Code works", "https://code.claude.com/docs/en/how-claude-code-works")), T),
        light("Anthropic 사내 데이터 분석", big([
            ("95", "%", "Claude 로 처리하는 분석 질의 비율", True), ("21", "% 이하", "스킬 · 정의 없을 때 정확도"),
            ("95 → 65", "%", "관리하지 않은 한 달 뒤 정확도")], 3)
              + note("지표 정의", "사람이 소유 · 데이터 사전 · 규칙 파일로 고정")
              + src(("Claude 블로그 · How Anthropic enables self-service data analytics (2026-06-03)",
                     "https://claude.com/blog/how-anthropic-enables-self-service-data-analytics-with-claude")), T),
        light("CLAUDE.md", '<div class="twocol w"><div>' + code("CLAUDE.md · 예", esc(_claude_md())) + "</div><div>"
              + viz2.tiles([("읽는 때", "Claude Code 시작마다 자동"), ("담는 것", "폴더 · 판정 규칙 · 작업 규칙"),
                            ("효과", "매번 같은 설명을 반복하지 않음")], 1) + "</div></div>", T),
        light("데이터 사전", viz2.maprows([
            ("열 이름", "vth_v", "문턱전압"), ("단위", "V", "mV 로 들어오면 오류"), ("스펙", "0.38~0.52", "판정 기준"),
            ("기준 숫자", f"{REF['gross_die']} · {W07['pass']} · {W07['yield']}%", "결과 대조용")], "칸", "예")
              + note("파일", "docs/data_dictionary.md · Claude 가 쓰고 사람이 확인"), T),
        light("실습 폴더 wafer-lab", viz2.maprows([
            ("data/", "wafer_test_W07.csv · spec.csv · equipment.csv", "읽기만"), ("data/raw/", "원시 파일 25장", "2 · 6교시"),
            ("docs/", "데이터 사전 · 보고서", "문서"), ("scripts/ · output/", "스크립트 · 결과 파일", "Claude 가 만듦")], "폴더", "내용"), T),
        light("실습 환경", viz2.tiles([
            ("VS Code", "편집기 · 파일 탐색기 · 터미널"), ("Claude Code 확장", "VS Code 확장 · 교육용 계정 로그인"),
            ("Python", "pandas · openpyxl — 없으면 Claude Code 가 설치 안내"), ("wafer-lab 폴더", "파일 → 폴더 열기")], 2)
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
                   f"불량 1위 crack {W07['crack']}개 — 대각선 위치에 몰려 있음")], "요약 대화 예")
              + note("대조", "엑셀에서 pass_fail 필터 → PASS 개수가 같은지"), T),
    ]
