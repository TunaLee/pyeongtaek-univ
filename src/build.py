#!/usr/bin/env python3
"""평택대 반도체 품질데이터 교안 → docs/

사용: python3 src/build.py          (전체)
      (교시를 나누지 않고 한 파일 docs/index.html 로 합친다)
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


def roadmap():
    cells = "".join(f'<div class="v1u"><span class="c">{u}교시</span><b>{t}</b><small>{o}</small></div>' for u, t, o in pkit.UNITS)
    return deck.light("과정 지도", f'<div class="v1map">{cells}</div>'
                      , "전체")


# 교시마다 도입 → 설명 → 적용. 도입 · 설명은 장 제목을 순서대로 적고, 나머지는 적용(원래 순서 · 「반도체 적용」 먼저).
PHASES = {
    "1": (["Claude Code가 데이터를 다루는 순서"], ["요청 쓰는 법", "데이터 종류와 차트"]),
    "2": (["웨이퍼와 칩", "엑셀 행과 맵 칸"],
          ["같은 질문, 세 가지 도구", "수율 계산", "사과 집계 표", "칩 집계 표", "엑셀과 CSV", "새 대화의 시작",
           "CLAUDE.md", "확인할 수 있는 문장", "숫자 맞춰 보기"]),
    "3": (["완성 시뮬레이터", "엑셀 화면과 웹 화면", "웹 화면의 세 부분"], ["세 부분이 들어가는 곳", "예시 파일 고쳐 보기", "계획부터 보기",
                                                 "Plan Mode", "권한 모드"]),
    "4": (["좌표에서 사각형까지"], ["색과 범례", "칩 정보 풍선", "글 설명과 화면 캡처", "화면 캡처 첨부"]),
    "5": (["맵과 차트"], ["막대 차트 읽는 법", "사과 사유별 막대", "칩 사유별 막대", "두 칸 배치",
                        "나눠서 요청하기", "파일 이름 버전 관리", "Git 커밋", "체크포인트"]),
    "6": (["당도 조절 바"], ["사과 판정 조건", "누설전류 합격선", "조절 바 동작 순서", "함께 바뀌는 화면", "완료처럼 보이는 결과",
                              "다시 지시하는 법", "검증 루프"]),
    "7": (["조절 바 설계표"], ["왼쪽 조절 · 오른쪽 결과", "처음 값과 원본 비교", "점검할 숫자", "컨텍스트", "대화 비우기와 요약",
                          "매번 같은 설명", "Skill 이 열리는 단계", "SKILL.md"]),
    "8": (["남은 기능"], ["다른 파일 불러오기", "목표 수율 표시", "판정 결과 내려받기", "실험 기록", "프롬프트 · 컨텍스트 · 하네스", "마구와 하네스",
                             "지금까지 쓴 하네스", "부탁과 Hook",
                             "Hook 이 끼어드는 시점"]),
}
STEPS = ("도입", "설명", "적용")


def _title(sl):
    return re.search(r'data-title="([^"]*)"', sl).group(1)


def _mark(sl, phase):
    """머리 꼬리표 옆에 도입 · 설명 · 적용 — 지금 단계만 주황."""
    ph = "".join(f'<i class="on">{x}</i>' if x == phase else f"<i>{x}</i>" for x in STEPS)
    return re.sub(r'(<span class="tag">[^<]*</span>)', rf'\1<span class="p0ph">{ph}</span>', sl, count=1)


def phased(u, slides):
    intro_t, expl_t = PHASES[u]
    slides = [x for sl in slides for x in re.split(r"\n*(?=<section )", sl) if x.strip()]  # brief() 처럼 두 장이 한 문자열인 경우
    by = {}
    for sl in slides:
        by.setdefault(_title(sl), []).append(sl)
    for t in intro_t + expl_t:
        assert len(by.get(t, [])) == 1, f"{u}교시 · 장 제목 없음 또는 중복: {t}"
    pick = lambda ts: [by[t][0] for t in ts]  # noqa: E731
    used = set(intro_t + expl_t)
    rest = [sl for sl in slides if _title(sl) not in used]
    return ([_mark(x, "도입") for x in pick(intro_t)] + [_mark(x, "설명") for x in pick(expl_t)]
            + [_mark(x, "적용") for x in rest])


def main():
    """한 파일 docs/index.html — 표지 · 개요 두 부분(데이터 분석 → 바이브코딩) · 과정 지도 · 교시마다 [간지 + 도입 · 설명 · 적용] · 마지막 장."""
    mods = [(u, t, o, importlib.import_module(f"p{u}")) for u, t, o in pkit.UNITS]
    css = (BASE_CSS + "".join(getattr(m, "CSS", "") for *_, m in mods)
           + ".v1shot figcaption,.ph figcaption,.v3ph figcaption{display:none}")  # 그림 밑 설명 줄은 내지 않는다
    parts = [art.DEFS, cover()]
    for div0, ph0 in p0.slides():          # 개요 두 부분 · 바이브코딩까지 → 데이터 분석과 엔지니어링
        parts.append(div0)
        for k in STEPS:
            parts += [_mark(x, k) for x in ph0[k]]
    parts.append(roadmap())                 # 과정 지도 — 데이터 분석 · 바이브코딩 다음, 1교시 바로 앞
    for u, t, o, m in mods:
        parts.append(deck.divider(u, t, "").replace(f'<div class="kick">{u}</div>', f'<div class="kick">{u}교시</div>'))
        parts += phased(u, m.slides())
    parts.append(pkit.nextup("8"))
    out = ROOT / "docs" / "index.html"
    body = re.sub(r"--d:([\d.]+)s", lambda m: f"--d:{float(m.group(1)) * anim.SPEED:.2f}s", "\n\n".join(parts))   # 카드 지연도 같은 속도
    out.write_text(_tpl(css).replace("{{DECK_TITLE}}", "엑셀 데이터로 만드는 수율 시뮬레이터").replace("{{SLIDES}}", body))
    print(out.name, len(parts) - 1, "장")


if __name__ == "__main__":
    main()
