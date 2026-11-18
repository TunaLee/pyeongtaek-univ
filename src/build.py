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


def index():
    """docs/index.html — 교시 여덟 개 목록 (덱과 같은 색 · 한 장)."""
    cells = "".join(f'<a href="{pkit.file_of(u)}"><span>{u}교시</span><b>{t}</b><small>{o}</small></a>' for u, t, o in pkit.UNITS)
    html = f"""<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>반도체 품질데이터 분석 · 엔지니어링</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css">
<style>body{{margin:0;font-family:Pretendard,sans-serif;background:#0F1B2D;color:#fff;min-height:100vh}}
main{{max-width:1080px;margin:0 auto;padding:56px 20px}} .k{{color:#F28C28;font-weight:800;font-size:15px;letter-spacing:.04em}}
h1{{font-size:clamp(30px,5vw,46px);margin:10px 0 34px;line-height:1.2}}
.g{{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:14px}}
a{{display:flex;flex-direction:column;gap:6px;padding:20px;border:1.5px solid #2C3E57;border-radius:16px;text-decoration:none;color:#fff;background:#16233A;min-height:130px}}
a:hover{{border-color:#F28C28}} a span{{font-size:14px;font-weight:800;color:#F28C28}} a b{{font-size:21px;line-height:1.3}}
a small{{margin-top:auto;font-size:14px;color:#AEB8C6}} p{{color:#AEB8C6;font-size:14px;margin-top:30px;line-height:1.6}}</style>
<main><div class="k">평택대학교 · 반도체 품질데이터 · Claude Code</div><h1>반도체 품질데이터 분석 · 엔지니어링</h1>
<div class="g">{cells}</div>
<p>실습 폴더 · labs/wafer-lab · 완성본 · labs/solution · 웨이퍼 데이터는 교육용 합성 데이터 · SECOM 은 UCI (CC BY 4.0)</p></main></html>"""
    (ROOT / "docs" / "index.html").write_text(html, encoding="utf-8")


if __name__ == "__main__":
    main()
    index()
