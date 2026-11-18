#!/usr/bin/env python3
"""평택대 반도체 품질데이터 교안 → docs/

사용: python3 src/build.py          (전체)
      (교시를 나누지 않고 한 파일 docs/index.html 로 합친다)
"""
import importlib
import os

import art
import deck
import deck_gas
import explain
import hx
import intro
import pgen
import pkit
import stats_hx
import v1kit
import v3kit

ROOT = pkit.ROOT
BASE_CSS = (intro.CSS + explain.CSS + deck.CSS + deck_gas.CSS + hx.CSS + stats_hx.CSS + hx.mcp_fig.CSS + hx.viz2.CSS
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


def main():
    """한 파일 docs/index.html — 표지 · 과정 지도 · 교시마다 [간지 + 일반 예 + 본문] · 마지막 장."""
    mods = [(u, t, o, importlib.import_module(f"p{u}")) for u, t, o in pkit.UNITS]
    css = (BASE_CSS + "".join(getattr(m, "CSS", "") for *_, m in mods)
           + ".v1shot figcaption,.ph figcaption,.v3ph figcaption{display:none}")  # 그림 밑 설명 줄은 내지 않는다
    parts = [art.DEFS, cover(), roadmap()]
    for u, t, o, m in mods:
        parts.append(deck.divider(u, t, "").replace(f'<div class="kick">{u}</div>', f'<div class="kick">{u}교시</div>'))
        parts += pgen.slides_for(u) + m.slides()
    parts.append(pkit.nextup("8"))
    out = ROOT / "docs" / "index.html"
    out.write_text(_tpl(css).replace("{{DECK_TITLE}}", "반도체 품질데이터 분석 · 엔지니어링").replace("{{SLIDES}}", "\n\n".join(parts)))
    print(out.name, len(parts) - 1, "장")


if __name__ == "__main__":
    main()
