#!/usr/bin/env python3
"""평택대 반도체 품질데이터 교안 → docs/

사용: python3 src/build.py          (전체)
      P_ONLY=1,3 python3 src/build.py  (일부 교시만)
"""
import importlib
import os

import art
import deck
import deck_gas
import explain
import hx
import intro
import pkit
import stats_hx
import v1kit
import v3kit

ROOT = pkit.ROOT
BASE_CSS = (intro.CSS + explain.CSS + deck.CSS + deck_gas.CSS + hx.CSS + stats_hx.CSS + hx.mcp_fig.CSS + hx.viz2.CSS
            + v3kit.CSS + v1kit.CSS)


def _tpl(css):
    return (ROOT / "src" / "template.html").read_text().replace("</style>", css + "</style>", 1)


def main():
    only = [x for x in os.environ.get("P_ONLY", "").split(",") if x]
    for u, title, _ in pkit.UNITS:
        if only and u not in only:
            continue
        try:
            mod = importlib.import_module(f"p{u}")
        except ModuleNotFoundError:
            continue
        tpl = _tpl(BASE_CSS + getattr(mod, "CSS", ""))
        parts = [art.DEFS, pkit.cover(u), pkit.roadmap(u)] + mod.slides() + [pkit.nextup(u)]
        out = ROOT / "docs" / pkit.file_of(u)
        out.write_text(tpl.replace("{{DECK_TITLE}}", f"{u}교시 {title}").replace("{{SLIDES}}", "\n\n".join(parts)))
        print(out.name, len(parts) - 1, "장")


if __name__ == "__main__":
    main()
