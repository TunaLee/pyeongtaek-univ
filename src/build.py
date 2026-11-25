#!/usr/bin/env python3
"""평택대 반도체 품질데이터 교안 → docs/

사용: python3 src/build.py          (전체)
      (교시 없이 한 파일 docs/index.html — 장은 OUTLINE · CHAPTERS 로 제목을 골라 엮는다)
"""
import importlib
import os
import re

import anim
import art
import deck
import deck_gas
import explain
import hx
import intro
import p0
import pbg
import sk
import pgen
import pkit
import stats_hx
import v1kit
import v3kit

ROOT = pkit.ROOT
BASE_CSS = (p0.CSS + pbg.CSS + sk.CSS + intro.CSS + explain.CSS + deck.CSS + deck_gas.CSS + hx.CSS + stats_hx.CSS + hx.mcp_fig.CSS + hx.viz2.CSS
            + v3kit.CSS + v1kit.CSS)


def _tpl(css):
    return (ROOT / "src" / "template.html").read_text().replace("</style>", css + "</style>", 1)


def cover():
    return '''<section class="slide dk cover-dk active" data-title="표지">
  <div class="glow"></div>
  <div class="kick">평택대학교 · 반도체 품질데이터 · 바이브코딩</div>
  <h1>엑셀 데이터로 만드는<br/>수율 시뮬레이터</h1>
</section>'''


# ── 구성 — 교시 없음. 장 제목으로 골라 순서를 정한다 (OUTLINE). ─────────────────────
# 각 모듈(p0 · p1 … p8 · pnew)이 만든 장을 제목으로 모으고, 부 · 장마다 도입 → 설명 → 적용 순서로 엮는다.
# 실습 번호는 OUTLINE 에 나오는 차례대로 1 부터 다시 매긴다(모듈 안의 「1-2 · 21-1」 같은 번호는 자리표).
STEPS = ("도입", "설명", "적용")
VIBE = {  # Ⅱ AI와 바이브코딩 — AI 활용 방식의 변화(프롬프트 → 컨텍스트 → 에이전틱 → 하네스) → LLM → 에이전트 → 컨텍스트 → .claude → CLAUDE.md → Skill → Sub Agent → Hook
    "도입": ["프로그래밍 언어의 발전", "AI 코딩 도구의 변화",
             "AI 활용 방식의 변화", "프롬프트 엔지니어링", "프롬프트만의 한계", "컨텍스트 엔지니어링", "컨텍스트만의 한계",
             "에이전틱 AI", "AI가 맡을 수 있는 작업 길이", "에이전트만의 한계", "마구와 하네스", "하네스 엔지니어링",
             "바이브코딩의 등장", "바이브코딩 사례", "바이브코딩의 흐름"],
    "설명": ["LLM", "도구가 필요한 이유", "Claude와 Claude Code", "에이전트 루프",
             "컨텍스트", "컨텍스트 관리가 필요한 이유", "대화 비우기와 요약", "새 대화의 시작",
             "Claude가 작업할 때 참고하는 것", "프로젝트 폴더 구조 · .claude/", "전역 · 프로젝트 하네스 위치",
             "CLAUDE.md", "CLAUDE.md에 적을 내용", "확인할 수 있는 문장",
             "매번 같은 설명", "Skill의 정의", "SKILL.md 예", "Skill 을 불러오는 순서", "CLAUDE.md vs Skill",
             "Sub Agent의 흐름", "부탁과 Hook", "Hook 이 끼어드는 시점", "Claude Code = 기본 하네스"],
    "적용": [],
}
APPENDIX = ("플러그인 마켓플레이스", "부록",  # 마지막 프로젝트 뒤 · 과정 이후 앞
            {"도입": ["플러그인"], "설명": ["마켓플레이스", "플러그인 설치 순서", "많이 쓰는 공개 하네스"], "적용": ["설치 전 점검"]})
CHAPTERS = [  # (제목, 꼬리표, 산출물, 도입, 설명, 적용)
    ("사과 데이터 분석", "사과 분석", "사과 요약 · 차트 세 장 · 집계 엑셀",
     ["실습 지도"], ["실습 환경", "실습 폴더 sim-lab", "요청 쓰는 법"],
     ["[실습 1-1] 사과 데이터 읽기", "[실습 1-2] 사과 차트 세 장", "실습 1-2 순서", "실습 1-2 요청 항목", "사과 차트 결과",
      "사과 차트에서 읽은 사실", "사과 집계 표", "[실습 11-3] 사과 집계 엑셀 · CSV", "실습 11-3 순서", "실습 11-3 요청 항목",
      "실습 11-3 확인"]),
    ("Skill 로 반도체 분석", "반도체 분석", "data-report Skill · 웨이퍼 분석",
     ["웨이퍼와 칩", "엑셀 행과 맵 칸"], ["수율 계산", "분석 Skill 흐름"],
     ["[실습 21-1] 사과 분석 Skill 만들기", "실습 21-1 순서", "실습 21-1 요청 항목", "[실습 21-2] Skill 로 웨이퍼 분석",
      "실습 21-2 순서", "실습 21-2 요청 항목", "웨이퍼 차트 결과", "웨이퍼 차트에서 읽은 사실", "칩 집계 표", "숫자 맞춰 보기"]),
    ("시뮬레이터 화면", "화면", "simulator.html · 숫자 카드",
     ["완성 시뮬레이터", "엑셀 화면과 웹 화면", "웹의 3요소"],
     ["정적 웹과 동적 웹", "3요소가 들어가는 곳", "예시 파일 고쳐 보기", "계획부터 보기", "Plan Mode", "권한 모드"],
     ["[실습 3-2] 웨이퍼 숫자 카드", "실습 3-2 순서", "실습 3-2 요청 항목", "웨이퍼 카드 전후"]),
    ("웨이퍼 맵", "맵", "맵 · 색 · 툴팁",
     ["좌표에서 사각형까지"], ["색과 범례", "칩 정보 툴팁", "캡처 첨부 전후", "캡처 첨부 방법"],
     ["[실습 4-2] 웨이퍼 맵", "실습 4-2 순서", "실습 4-2 요청 항목", "웨이퍼 맵 결과"]),
    ("불합격 차트", "차트", "사유별 · 위치별 막대",
     ["칩 사유별 막대"], ["화면 배치", "나눠서 요청하기"],
     ["[실습 5-2] 웨이퍼 차트", "실습 5-2 순서", "실습 5-2 요청 항목", "차트를 넣은 웨이퍼 화면"]),
    ("조절 바", "조절 바", "누설전류 조절 바",
     ["당도 조절 바"], ["사과 판정 조건", "누설전류 합격선", "조절 바 동작 순서", "함께 바뀌는 화면", "완료 보고와 증거", "다시 지시하는 법"],
     ["[실습 6-2] 누설전류 조절 바", "실습 6-2 순서", "실습 6-2 요청 항목", "실습 6-2 확인", "누설전류 조절 바 결과"]),
    ("조절 바 전체", "조절 바", "조절 바 8종 · 처음 값",
     ["조절 바 설계표"], ["왼쪽 조절 · 오른쪽 결과", "처음 값과 원본 비교", "점검할 숫자"],
     ["[실습 7-2] 조절 바 8종", "실습 7-2 순서", "실습 7-2 요청 항목"]),
    ("보고서 템플릿", "보고서", "엑셀 올리기 · 결과 내려받기",
     ["보고서 템플릿"], ["다른 파일 불러오기", "판정 결과 내려받기"],
     ["[실습 31-1] 보고서 템플릿", "실습 31-1 순서", "실습 31-1 요청 항목", "웨이퍼 시뮬레이터 완성"]),
    ("GitHub · Vercel 배포", "배포", "저장소 주소 · 배포 주소",
     ["배포 흐름"], ["파일 이름 버전 관리", "Git 커밋", "체크포인트", "GitHub · Vercel 준비", "수정과 재배포", "배포 전 점검"],
     ["[실습 31-2] GitHub · Vercel 배포", "실습 31-2 순서", "실습 31-2 요청 항목"]),
    ("마지막 프로젝트", "프로젝트", "내 웹 · 배포 주소",
     ["프로젝트 주제"], ["프로젝트 진행 순서"],
     ["[실습 41-1] 마지막 프로젝트", "실습 41-1 순서", "실습 41-1 요청 항목", "제출물"]),
]


def _title(sl):
    return re.search(r'data-title="([^"]*)"', sl).group(1)


def _mark(sl, phase):
    """머리 꼬리표 옆에 도입 · 설명 · 적용 — 지금 단계만 주황."""
    ph = "".join(f'<i class="on">{x}</i>' if x == phase else f"<i>{x}</i>" for x in STEPS)
    return re.sub(r'(<span class="tag">[^<]*</span>)', rf'\1<span class="p0ph">{ph}</span>', sl, count=1)


def _retag(sl, tag):
    return re.sub(r'<span class="tag">[^<]*</span>', f'<span class="tag">{tag}</span>', sl, count=1)


def _chdiv(n, title):
    return f"""<section class="slide dk divider" data-title="[{n:02d}] {title}">
  <div class="ghost">{n:02d}</div>
  <div class="kick">실습</div>
  <h2 class="big">{title}</h2>
</section>"""


def _apdiv(title):
    return f"""<section class="slide dk divider" data-title="[부록] {title}">
  <div class="ghost">+</div>
  <div class="kick">부록</div>
  <h2 class="big">{title}</h2>
</section>"""


def lab_map():
    cells = "".join(f'<div class="v1u"><span class="c">{i:02d}</span><b>{t}</b><small>{o}</small></div>'
                    for i, (t, _, o, *_) in enumerate(CHAPTERS, 1))
    return deck.light("실습 지도", f'<div class="v1map">{cells}</div>', "실습")


def closing():
    return """<section class="slide dk" data-title="과정 이후">
  <div class="coord"><b></b> / <span class="tot"></span></div>
  <div class="v1end"><div class="v1got"><span>오늘 만든 것</span><b>data-report Skill · 보고서 템플릿 · 배포 주소</b></div>
  <div class="v1next"><span>과정 이후</span><b>내 엑셀로 같은 순서</b><small>→ 분석 · Skill · 보고서 · 배포</small></div></div>
</section>"""


def main():
    """한 파일 docs/index.html — 표지 · Ⅰ 데이터 분석 · Ⅱ AI와 바이브코딩 · 실습 장 열 개(장마다 도입 · 설명 · 적용) · 마지막 장. 교시 없음."""
    import pai
    import pana
    import pnew
    mods = [importlib.import_module(f"p{u}") for u, *_ in pkit.UNITS] + [pnew, pai]
    css = (BASE_CSS + "".join(getattr(m, "CSS", "") for m in mods)
           + ".v1shot figcaption,.ph figcaption,.v3ph figcaption{display:none}")  # 그림 밑 설명 줄은 내지 않는다
    pool = {}

    def add(sl):
        for x in re.split(r"\n*(?=<section )", sl):
            if x.strip():
                k = _title(x)
                assert k not in pool, f"장 제목 중복: {k}"
                pool[k] = x

    (div1, ph1), (div2, _) = p0.slides()
    for k in STEPS:
        for x in ph1[k]:
            add(x)
    for x in [x for _, ph in p0.slides()[1:] for k in STEPS for x in ph[k]]:
        add(x)
    for m in mods:
        for sl in m.slides():
            add(sl)
    add(lab_map())

    def take(t):
        assert t in pool, f"장 없음: {t}"
        return pool[t]

    # Ⅰ 데이터 분석 — p0 의 순서 + 「도구별 상품률 계산」을 「분석 도구의 변화」 뒤로
    ph1 = {k: [_title(x) for x in ph1[k]] for k in STEPS}
    ap = ph1["적용"]
    ap.insert(ap.index("분석 도구의 변화") + 1, "도구별 상품률 계산")
    parts = [art.DEFS, cover()]
    used = set()

    def emit(phases, tag):
        for k in STEPS:
            for t in phases[k]:
                used.add(t)
                parts.append(_mark(_retag(take(t), tag), k))

    parts.append(div1)
    emit(ph1, "데이터 분석")
    parts.append(div2)
    emit(VIBE, "바이브코딩")
    for n, (title, tag, _, intro_t, expl_t, app_t) in enumerate(CHAPTERS, 1):
        parts.append(_chdiv(n, title))
        emit({"도입": intro_t, "설명": expl_t, "적용": app_t}, tag)
    ap_title, ap_tag, ap_ph = APPENDIX
    parts.append(_apdiv(ap_title))
    emit(ap_ph, ap_tag)
    parts.append(closing())
    # 실습 번호 — 나온 차례대로 1, 2, 3 …
    order = [m.group(1) for x in parts for m in [re.match(r'<section[^>]*data-title="\[실습 ([\d-]+)\]', x)] if m]
    num = {o: str(i) for i, o in enumerate(order, 1)}
    body = "\n\n".join(parts)
    body = re.sub(r"실습 (\d+-\d+)", lambda m: f"실습 {num.get(m.group(1), m.group(1))}", body)
    left = sorted(set(re.findall(r"실습 \d+-\d+", body)))
    assert not left, f"번호를 못 바꾼 실습 언급: {left}"
    dropped = sorted(set(pool) - used)
    out = ROOT / "docs" / "index.html"
    body = re.sub(r"--d:([\d.]+)s", lambda m: f"--d:{float(m.group(1)) * anim.SPEED:.2f}s", body)   # 카드 지연도 같은 속도
    out.write_text(_tpl(css).replace("{{DECK_TITLE}}", "엑셀 데이터로 만드는 수율 시뮬레이터").replace("{{SLIDES}}", body))
    print(out.name, len(parts) - 1, "장 · 실습", len(order), "개 · 쓰지 않은 장", len(dropped))
    print("  쓰지 않은 장:", " | ".join(dropped))


if __name__ == "__main__":
    main()
