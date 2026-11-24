"""평택대 공통 도구 — 교시 표지 · 과정 지도 · 다음 교시 · 실습 데이터 숫자. 교시 모듈(p1 … p8)이 쓴다.

반도체 품질데이터 분석 · 엔지니어링 (1일 8교시). 교시마다 HTML 한 파일(docs/N-이름.html).
공통 실습 데이터 = labs/wafer-lab (LOT2611-07 · 웨이퍼 25장 · 다이 616개/장 · 설비 3대) + UCI SECOM.
화면의 숫자는 labs/ref.json · labs/solution 출력에서 그대로 읽는다(손으로 적지 않는다).
이어지는 산출물: 데이터 사전 → clean.py → 수율 표 → 웨이퍼 맵 → SPC 차트 → 파이프라인 → 대시보드 → 분석 요약
"""
import json
from pathlib import Path

from deck import light
from hx import note
from v1kit import brief, chat, codemap, shot  # noqa: F401 — 교시 모듈이 pkit 에서 가져다 쓴다

ROOT = Path(__file__).resolve().parent.parent
LAB = ROOT / "labs"
REF = json.loads((LAB / "ref.json").read_text(encoding="utf-8"))
SOL = LAB / "solution"
FOLDER = "wafer-lab"

# (교시, 제목, 남는 것)
UNITS = [
    ("1", "엑셀 데이터 구조 · Claude Code 시작", "데이터 요약 문서"),
    ("2", "엑셀 집계 자동화 · CLAUDE.md", "yield_summary.xlsx · CSV"),
    ("3", "HTML 첫 화면 · Plan Mode", "simulator.html · 숫자 카드"),
    ("4", "웨이퍼 맵 · 화면 보고 고치기", "simulator.html · 웨이퍼 맵"),
    ("5", "불합격 차트 · 나눠서 요청하기", "simulator.html · 차트 2종"),
    ("6", "분포와 조절 바 · 검증", "simulator.html · 조절 바 1개"),
    ("7", "조절 바 전체 · Skill", "simulator.html · 조절 바 8종"),
    ("8", "시뮬레이터 완성 · 하네스 · 발표", "simulator.html 완성 · 실험 기록"),
]
BY = {u[0]: u for u in UNITS}
SLUG = {"1": "data", "2": "clean", "3": "yield", "4": "wafer-map", "5": "spc", "6": "pipeline", "7": "dashboard", "8": "report"}


def tag(u):
    return f"{u}교시"


def file_of(u):
    return f"{u}-{SLUG[u]}.html"


def W(w):
    """웨이퍼 한 장의 기준 숫자 — REF['wafers']['W07'] 등."""
    return REF["wafers"][w]


def cover(u):
    _, title, _ = BY[u]
    return f'''<section class="slide dk cover-dk active" data-title="표지">
  <div class="glow"></div>
  <div class="kick">반도체 품질데이터 · {u}교시</div>
  <h1>{title}</h1>
</section>'''


def roadmap(u):
    cur = [x[0] for x in UNITS].index(u)
    cells = []
    for i, (c, t, out) in enumerate(UNITS):
        cls = "on" if i == cur else ("done" if i < cur else "")
        cells.append(f'<a class="v1u {cls}" href="{file_of(c)}"><span class="c">{c}교시</span><b>{t}</b><small>{out}</small></a>')
    return light("과정 지도", f'<div class="v1map">{"".join(cells)}</div>'
                 + "", tag(u))


def nextup(u):
    i = [x[0] for x in UNITS].index(u)
    _, _, out = UNITS[i]
    if i + 1 < len(UNITS):
        c, t, nout = UNITS[i + 1]
        nxt = f'<a class="v1next" href="{file_of(c)}"><span>{c}교시</span><b>{t}</b><small>→ {nout}</small></a>'
    else:
        nxt = '<div class="v1next"><span>과정 이후</span><b>내 엑셀로 같은 순서</b><small>→ 요약 · 집계 · 화면 · 조절 바</small></div>'
    return f'''<section class="slide dk" data-title="다음 교시">
  <div class="coord"><b></b> / <span class="tot"></span></div>
  <div class="v1end"><div class="v1got"><span>{u}교시 산출물</span><b>{out}</b></div>{nxt}</div>
</section>'''
