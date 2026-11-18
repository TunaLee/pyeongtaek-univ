#!/usr/bin/env python3
"""평택대 반도체 품질데이터 교안 → docs/

사용: python3 src/build.py          (전체)
      (교시를 나누지 않고 한 파일 docs/index.html 로 합친다)
"""
import importlib
import os
import re

import art
import deck
import deck_gas
import explain
import hx
import intro
import p0
import pgen
import pkit
import stats_hx
import v1kit
import v3kit

ROOT = pkit.ROOT
BASE_CSS = (p0.CSS + intro.CSS + explain.CSS + deck.CSS + deck_gas.CSS + hx.CSS + stats_hx.CSS + hx.mcp_fig.CSS + hx.viz2.CSS
            + v3kit.CSS + v1kit.CSS)


def _tpl(css):
    return (ROOT / "src" / "template.html").read_text().replace("</style>", css + "</style>", 1)


def cover():
    return '''<section class="slide dk cover-dk active" data-title="표지">
  <div class="glow"></div>
  <div class="kick">평택대학교 · 반도체 품질데이터 · Claude Code</div>
  <h1>반도체 품질데이터<br/>분석 · 엔지니어링</h1>
</section>'''


def roadmap():
    cells = "".join(f'<div class="v1u"><span class="c">{u}교시</span><b>{t}</b><small>{o}</small></div>' for u, t, o in pkit.UNITS)
    return deck.light("과정 지도", f'<div class="v1map">{cells}</div>'
                      , "전체")


# 교시마다 도입 → 설명 → 적용. 도입 · 설명은 장 제목을 순서대로 적고, 나머지는 적용(원래 순서 · 「반도체 적용」 먼저).
PHASES = {
    "1": (["반도체 적용", "테스트 결과가 CSV 가 되는 과정", "데이터 규모"],
          ["데이터 용어", "열 18개 네 묶음", "판정 순서", "수율", "Claude 와 Claude Code", "Claude Code 의 데이터 작업 고리",
           "Anthropic 사내 데이터 분석", "CLAUDE.md", "데이터 사전"]),
    "2": (["택배 원시 파일의 문제", "공정 데이터가 지저분한 이유", "실제 공정 데이터 · UCI SECOM", "SECOM 의 결측 · 상수 열"],
          ["비유 · 택배 분류장 검수", "결측 처리 세 가지", "원본 보존"]),
    "3": (["구역별 정시 도착률", "실패 사유 Pareto"],
          ["수율 집계 세 가지", "피벗 테이블과 요청"]),
    "4": (["구역 지도", "지도의 효과"],
          ["표와 맵", "웨이퍼 맵", "좌표에서 사각형까지", "HTML · SVG 한 파일", "WM-811K 공개 데이터셋", "불량 패턴 9종", "패턴 비율"]),
    "5": (["배송 시간 분포", "평균은 같고 퍼짐이 다름"],
          ["분포와 스펙 한계", "비유 · 차선과 차", "Cp 와 Cpk", "분포 모양과 Cpk"]),
    "6": (["매일 쌓이는 배송 파일", "차량별 정시율", "매일 쌓이는 테스트 파일", "업계 사례 · 테스트 데이터 레이크"],
          ["비유 · 물류센터", "파이프라인 다섯 단계", "CSV 와 Parquet", "같은 데이터의 파일 크기", "DuckDB", "다시 돌려도 같은 결과"]),
    "7": (["배송 현황판", "매일 들어오는 파일"],
          ["자동화의 조건", "비유 · 자동 세차장", "차트 고르는 기준", "정기 실행", "claude -p"]),
    "8": (["외곽 지연의 원인 후보", "차트에서 결정까지"],
          ["분석 요약 네 칸", "근거 묶기", "상관과 원인", "발표 2분", "사람의 판단 영역"]),
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
    rest.sort(key=lambda sl: _title(sl) != "반도체 적용")
    return ([_mark(x, "도입") for x in pick(intro_t)] + [_mark(x, "설명") for x in pick(expl_t)]
            + [_mark(x, "적용") for x in rest])


def main():
    """한 파일 docs/index.html — 표지 · 과정 지도 · 개요 · 교시마다 [간지 + 도입 · 설명 · 적용] · 마지막 장."""
    mods = [(u, t, o, importlib.import_module(f"p{u}")) for u, t, o in pkit.UNITS]
    css = (BASE_CSS + "".join(getattr(m, "CSS", "") for *_, m in mods)
           + ".v1shot figcaption,.ph figcaption,.v3ph figcaption{display:none}")  # 그림 밑 설명 줄은 내지 않는다
    parts = [art.DEFS, cover(), roadmap()]
    div0, ph0 = p0.slides()
    parts.append(div0)
    for k in STEPS:
        parts += [_mark(x, k) for x in ph0[k]]
    for u, t, o, m in mods:
        parts.append(deck.divider(u, t, "").replace(f'<div class="kick">{u}</div>', f'<div class="kick">{u}교시</div>'))
        parts += phased(u, pgen.slides_for(u) + m.slides())
    parts.append(pkit.nextup("8"))
    out = ROOT / "docs" / "index.html"
    out.write_text(_tpl(css).replace("{{DECK_TITLE}}", "반도체 품질데이터 분석 · 엔지니어링").replace("{{SLIDES}}", "\n\n".join(parts)))
    print(out.name, len(parts) - 1, "장")


if __name__ == "__main__":
    main()
