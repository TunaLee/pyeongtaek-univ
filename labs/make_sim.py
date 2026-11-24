"""수율 시뮬레이터 실습 자료 생성기 — 엑셀 데이터 → HTML 시뮬레이터 (8교시 누적).

실행: .venv/bin/python labs/make_sim.py   (pandas · openpyxl 필요 · Chrome 이 있으면 캡처까지)
      옵션 --no-shots : 캡처 생략

만드는 것
  labs/sim-lab/data/            실습용 엑셀 4개 (wafer_test_W07 · W21 · apple_A07 · A25, csv 에서 변환)
  labs/sim-solution/stageN/     교시별 누적 완성본 (1 · 2 · 3a · 3b · 4 ~ 8) — output · docs · scripts
  labs/sim_ref.json             덱에 쓰는 숫자 (웨이퍼 · 사과)
  docs/img/sim/*.webp           완성본 화면 캡처 (1280×720)

HTML 원본은 labs/sim-src/s*.html (손으로 짠 바닐라 JS). 여기서 데이터 CSV 글자와 CFG 를 끼워 넣는다.
판정 규칙은 아래 DOMAINS 한 곳에만 있고, 파이썬 판정(숫자 계산)과 HTML 의 CFG 가 같은 값을 쓴다.
"""
import csv
import io
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from openpyxl import Workbook

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
SRC = ROOT / "sim-src"
LAB = ROOT / "sim-lab"
SOL = ROOT / "sim-solution"
DATA_IN = ROOT / "wafer-lab" / "data"
IMG = REPO / "docs" / "img" / "sim"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

DOMAINS = {
    "wafer": {
        "src": DATA_IN / "wafer_test_W07.csv",
        "alt": DATA_IN / "raw" / "wafer_test_W21.csv",
        "xlsx": "wafer_test_W07.xlsx",
        "alt_xlsx": "wafer_test_W21.xlsx",
        "html": "simulator.html",
        "summary": "yield_summary.xlsx",
        "script": "summary.py",
        "cfg": {
            "title": "웨이퍼 수율 시뮬레이터",
            "dataName": "wafer_test_W07.xlsx",
            "item": "칩", "count": "개",
            "labels": {"total": "전체 칩", "pass": "합격", "fail": "불합격", "rate": "수율",
                       "scope": "집계 대상 칩", "orig": "엑셀 원본 수율"},
            "judgeCol": "pass_fail", "passValue": "PASS", "reasonCol": "fail_type",
            "x": "die_x", "y": "die_y", "outline": 15,
            "mapTitle": "웨이퍼 맵", "reasonTitle": "불합격 사유별 칩 수", "zoneTitle": "위치별 합격률",
            "zoneCol": "zone", "zones": [["center", "중심"], ["mid", "중간"], ["edge", "가장자리"]],
            "reasons": [["crack", "깨짐·긁힘"], ["open_short", "접촉저항 초과"], ["leakage", "누설전류 초과"],
                        ["vth_shift", "문턱전압 범위 밖"], ["particle", "먼지 많음"], ["parametric", "기타 측정값"]],
            "rules": [
                {"col": "crack", "name": "깨짐·긁힘", "kind": "flag", "reason": "crack", "flagText": "깨진 칩 불합격"},
                {"col": "rc_ohm", "name": "접촉저항", "unit": "Ω", "hi": 15, "step": 0.1, "reason": "open_short"},
                {"col": "ioff_na", "name": "누설전류", "unit": "nA", "hi": 10, "step": 0.1, "reason": "leakage"},
                {"col": "vth_v", "name": "문턱전압", "unit": "V", "lo": 0.38, "hi": 0.52, "step": 0.01, "reason": "vth_shift"},
                {"col": "particle_cnt", "name": "먼지 개수", "unit": "개", "hi": 4, "step": 1, "reason": "particle"},
                {"col": "idsat_ma", "name": "포화전류", "unit": "mA", "lo": 0.92, "step": 0.01, "reason": "parametric"},
                {"col": "ox_thk_nm", "name": "산화막 두께", "unit": "nm", "lo": 2.85, "hi": 3.15, "step": 0.01, "reason": "parametric"},
            ],
            "scopes": [{"col": "radius_mm", "name": "중심에서 거리", "unit": "mm", "step": 1}],
            "slider": "ioff_na",
            "target": 90,
        },
    },
    "apple": {
        "src": DATA_IN / "practice" / "apple_A07.csv",
        "alt": DATA_IN / "practice" / "raw" / "apple_A25.csv",
        "xlsx": "apple_A07.xlsx",
        "alt_xlsx": "apple_A25.xlsx",
        "html": "apple_sim.html",
        "summary": "apple_summary.xlsx",
        "script": "apple_summary.py",
        "cfg": {
            "title": "사과 상품률 시뮬레이터",
            "dataName": "apple_A07.xlsx",
            "item": "사과", "count": "개",
            "labels": {"total": "전체 사과", "pass": "상품", "fail": "불량", "rate": "상품률",
                       "scope": "집계 대상 사과", "orig": "엑셀 원본 상품률"},
            "judgeCol": "grade", "passValue": "상품", "failValue": "불량", "reasonCol": "reason",
            "x": "tree_x", "y": "tree_y", "outline": 0,
            "mapTitle": "과수원 지도", "reasonTitle": "불량 사유별 개수", "zoneTitle": "구역별 상품률",
            "zoneCol": "zone", "zones": [["안쪽", "안쪽"], ["중간", "중간"], ["가장자리", "가장자리"]],
            "reasons": [["bruise", "멍"], ["worm", "벌레 먹음"], ["light", "무게 미달"], ["low_sugar", "당도 미달"]],
            "rules": [
                {"col": "bruise", "name": "멍", "kind": "flag", "reason": "bruise", "flagText": "멍 든 사과 불량"},
                {"col": "worm", "name": "벌레", "kind": "flag", "reason": "worm", "flagText": "벌레 먹은 사과 불량"},
                {"col": "weight_g", "name": "무게", "unit": "g", "lo": 250, "step": 1, "reason": "light"},
                {"col": "sugar_brix", "name": "당도", "unit": "brix", "lo": 11.0, "step": 0.1, "reason": "low_sugar"},
            ],
            "scopes": [{"col": "dist_m", "name": "중심에서 거리", "unit": "m", "step": 0.1},
                       {"col": "diameter_mm", "name": "지름", "unit": "mm", "step": 0.1}],
            "slider": "sugar_brix",
            "target": None,            # 아래에서 웨이퍼 목표와 같은 값으로
        },
    },
}
DOMAINS["apple"]["cfg"]["target"] = DOMAINS["wafer"]["cfg"]["target"]


# ───────────────────────── 판정 (HTML 의 judge 와 같은 규칙) ─────────────────────────
def read_rows(p):
    with open(p, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def numeric_cols(cfg):
    return [r["col"] for r in cfg["rules"]] + [s["col"] for s in cfg["scopes"]] + [cfg["x"], cfg["y"]]


def to_num(rows, cfg):
    out = []
    for r in rows:
        o = dict(r)
        for c in numeric_cols(cfg):
            o[c] = float(r[c])
        out.append(o)
    return out


def dec_of(step):
    return max(0, -math.floor(math.log10(step) + 1e-9))


def scope_max(rows, sc):
    st = sc["step"]
    return round(math.ceil(max(r[sc["col"]] for r in rows) / st - 1e-9) * st, dec_of(st))


def base_spec(cfg, rows):
    s = {}
    for r in cfg["rules"]:
        s[r["col"]] = {"on": True} if r.get("kind") == "flag" else {"lo": r.get("lo"), "hi": r.get("hi")}
    for sc in cfg["scopes"]:
        s[sc["col"]] = {"hi": scope_max(rows, sc)}
    return s


def judge(r, cfg, spec):
    for rule in cfg["rules"]:
        s, v = spec[rule["col"]], r[rule["col"]]
        if rule.get("kind") == "flag":
            if s["on"] and v > 0:
                return rule["reason"]
            continue
        if (s.get("lo") is not None and v < s["lo"]) or (s.get("hi") is not None and v > s["hi"]):
            return rule["reason"]
    return "none"


def in_scope(r, cfg, spec):
    return all(r[sc["col"]] <= spec[sc["col"]]["hi"] for sc in cfg["scopes"])


def evaluate(rows, cfg, spec):
    res = [(r, in_scope(r, cfg, spec), judge(r, cfg, spec)) for r in rows]
    sc = [(r, k) for r, ins, k in res if ins]
    n = len(sc)
    ok = sum(k == "none" for _, k in sc)
    reasons = {key: sum(k == key for _, k in sc) for key, _ in cfg["reasons"]}
    zones = {}
    for key, name in cfg["zones"]:
        z = [k for r, k in sc if r[cfg["zoneCol"]] == key]
        zones[name] = {"total": len(z), "pass": sum(k == "none" for k in z),
                       "rate": round(sum(k == "none" for k in z) / len(z) * 100, 2) if z else None}
    orig_ok = sum(r[cfg["judgeCol"]] == cfg["passValue"] for r in rows)
    orig_rate = round(orig_ok / len(rows) * 100, 2)
    rate = round(ok / n * 100, 2) if n else 0
    return {"total": n, "pass": ok, "fail": n - ok, "rate": rate, "excluded": len(rows) - n,
            "reasons": reasons, "zones": zones, "orig_rate": orig_rate, "delta_pp": round(rate - orig_rate, 2)}


def with_change(spec, col, **kw):
    s = json.loads(json.dumps(spec))
    s[col].update(kw)
    return s


def brief(ev):
    return {k: ev[k] for k in ("total", "pass", "fail", "rate", "delta_pp")}


# ───────────────────────── 기준 숫자 ─────────────────────────
def numbers(dom):
    cfg = dom["cfg"]
    rows = to_num(read_rows(dom["src"]), cfg)
    alt = to_num(read_rows(dom["alt"]), cfg)
    spec = base_spec(cfg, rows)
    ev = evaluate(rows, cfg, spec)
    mism = sum((judge(r, cfg, spec) == "none") != (r[cfg["judgeCol"]] == cfg["passValue"]) or
               judge(r, cfg, spec) != r[cfg["reasonCol"]] for r in rows)
    out = {"file": cfg["dataName"], "rows": len(rows), "cols": len(read_rows(dom["src"])[0]),
           "total": ev["total"], "pass": ev["pass"], "fail": ev["fail"], "rate": ev["rate"],
           "reasons": ev["reasons"],
           "reasons_sorted": sorted(([dict(cfg["reasons"])[k], v] for k, v in ev["reasons"].items()), key=lambda x: -x[1]),
           "zones": ev["zones"], "rejudge_mismatch": mism, "rejudge_match": mism == 0,
           "spec": spec}
    sl = cfg["slider"]
    rule = next(r for r in cfg["rules"] if r["col"] == sl)
    side = "hi" if rule.get("hi") is not None else "lo"
    vals = [5, 15, 20, 30] if cfg["item"] == "칩" else [10, 10.5, 11.5, 12]
    out["s6_slider"] = {"col": sl, "name": rule["name"], "unit": rule["unit"], "side": side, "base": rule[side],
                        "tries": {fmtnum(v): brief(evaluate(rows, cfg, with_change(spec, sl, **{side: v}))) for v in vals}}
    if cfg["item"] == "칩":
        ops = [("누설전류 상한 10 → 5 nA", with_change(spec, "ioff_na", hi=5)),
               ("문턱전압 범위 0.38~0.52 → 0.36~0.54 V", with_change(spec, "vth_v", lo=0.36, hi=0.54)),
               ("깨짐·긁힘 판정 끄기", with_change(spec, "crack", on=False)),
               (f"중심에서 거리 상한 {fmtnum(spec['radius_mm']['hi'])} → 120 mm", with_change(spec, "radius_mm", hi=120))]
    else:
        ops = [("무게 하한 250 → 230 g", with_change(spec, "weight_g", lo=230)),
               ("벌레 판정 끄기", with_change(spec, "worm", on=False)),
               (f"중심에서 거리 상한 {fmtnum(spec['dist_m']['hi'])} → 40 m", with_change(spec, "dist_m", hi=40)),
               (f"지름 상한 {fmtnum(spec['diameter_mm']['hi'])} → 80 mm", with_change(spec, "diameter_mm", hi=80))]
    out["s7_checks"] = [{"op": name, **brief(evaluate(rows, cfg, s)), "hash": spec_hash(s, spec)} for name, s in ops]
    # 8교시: 둘째 파일 · 목표 수율
    alt_spec = base_spec(cfg, alt)
    ea = evaluate(alt, cfg, alt_spec)
    out["s8_alt"] = {"file": dom["alt_xlsx"], "rows": len(alt), "total": ea["total"], "pass": ea["pass"], "fail": ea["fail"],
                     "rate": ea["rate"], "orig_rate": ea["orig_rate"], "reasons": ea["reasons"], "zones": ea["zones"],
                     "scope_max": {sc["col"]: alt_spec[sc["col"]]["hi"] for sc in cfg["scopes"]}}
    out["s8_target"] = target_combos(cfg, rows, spec, alt, alt_spec)
    return out


def spec_hash(s, base):
    """기준값이 바뀐 항목만 #키=값 으로 (HTML 이 처음 값으로 읽는다)."""
    parts = []
    for k, v in s.items():
        for kk, vv in v.items():
            if base[k].get(kk) != vv:
                parts.append(f"{k}_{kk}={int(vv) if isinstance(vv, bool) else vv}")
    return "#" + "&".join(parts)


def loosen_to(cfg, rows, spec, col, side, target):
    """조절 바 하나만 움직여 목표를 넘는 가장 작은 변화."""
    rule = next(r for r in cfg["rules"] if r["col"] == col)
    st, d = rule["step"], dec_of(rule["step"])
    v = spec[col][side]
    for i in range(1, 2000):
        nv = round(v + (i if side == "hi" else -i) * st, d)
        ev = evaluate(rows, cfg, with_change(spec, col, **{side: nv}))
        if ev["rate"] >= target:
            return {"col": col, "side": side, "value": nv, **brief(ev)}
    return None


def target_combos(cfg, rows, spec, alt, alt_spec):
    t = cfg["target"]
    out = {"target": t}
    for label, rs, sp in (("main", rows, spec), ("alt", alt, alt_spec)):
        ev = evaluate(rs, cfg, sp)
        singles = []
        for rule in cfg["rules"]:
            if rule.get("kind") == "flag":
                e2 = evaluate(rs, cfg, with_change(sp, rule["col"], on=False))
                singles.append({"col": rule["col"], "flag_off": True, **brief(e2), "reach": e2["rate"] >= t})
                continue
            for side in ("lo", "hi"):
                if sp[rule["col"]].get(side) is not None:
                    r = loosen_to(cfg, rs, sp, rule["col"], side, t)
                    if r:
                        singles.append(r)
        out[label] = {"base_rate": ev["rate"], "reached_at_base": ev["rate"] >= t, "single": singles}
    return out


def pick_combo(cfg, rs, sp, steps):
    """steps: [(col, side, value)] 차례로 적용한 결과."""
    s = json.loads(json.dumps(sp))
    for col, side, v in steps:
        s[col][side] = v
    return {"set": [{"col": c, "side": sd, "value": v} for c, sd, v in steps], **brief(evaluate(rs, cfg, s)),
            "hash": spec_hash(s, sp)}


def find_pick(cfg, rs, sp, t):
    """판정 조절 바 두 개(무게 하한 · 당도 하한)를 함께 낮춰 목표를 넘는 조합 중 변화가 가장 작은 것.
    무게는 5 g, 당도는 0.5 brix 눈금. 변화 크기 = 무게 10 g 과 당도 0.5 brix 를 1 로 친 합."""
    w0, s0 = sp["weight_g"]["lo"], sp["sugar_brix"]["lo"]
    best = None
    for dw in range(1, 11):
        for ds in range(1, 5):
            w, s = w0 - dw * 5, round(s0 - ds * 0.5, 1)
            ev = evaluate(rs, cfg, with_change(with_change(sp, "weight_g", lo=w), "sugar_brix", lo=s))
            if ev["rate"] < t:
                continue
            key = (dw / 2 + ds, ev["rate"])
            if best is None or key < best[0]:
                best = (key, [("weight_g", "lo", w), ("sugar_brix", "lo", s)])
    return best and best[1]


# ───────────────────────── 엑셀 · CSV ─────────────────────────
def csv_to_xlsx(src, dst, sheet):
    rows = read_rows(src)
    wb = Workbook()
    ws = wb.active
    ws.title = sheet
    head = list(rows[0].keys())
    ws.append(head)
    for r in rows:
        out = []
        for h in head:
            v = r[h]
            try:
                f = float(v)
                out.append(int(f) if v.lstrip("-").isdigit() else f)
            except ValueError:
                out.append(v)
        ws.append(out)
    ws.freeze_panes = "A2"
    wb.save(dst)


def rule_cond(rule):
    if rule.get("kind") == "flag":
        return "0 (1 이면 걸림)"
    lo, hi = rule.get("lo"), rule.get("hi")
    if lo is not None and hi is not None:
        return f"{fmtnum(lo)} 이상 {fmtnum(hi)} 이하"
    return f"{fmtnum(lo)} 이상" if lo is not None else f"{fmtnum(hi)} 이하"


def criteria_md(key, ref):
    cfg, r = DOMAINS[key]["cfg"], ref[key]
    L = cfg["labels"]
    reason = dict(cfg["reasons"])
    title = "합격 기준표" if key == "wafer" else "선별 기준표"
    lines = [f"# {title}", "",
             "위에서부터 차례로 확인하고, 먼저 걸린 줄의 사유 하나로 판정한다. 하나도 안 걸리면 "
             f"{L['pass']}(none)이다.", "",
             "| 순서 | 열 이름 | 화면 이름 | 단위 | 합격 조건 | 걸렸을 때 사유 | 사유 화면 이름 |", "|---|---|---|---|---|---|---|"]
    order = 0
    prev = None
    for rule in cfg["rules"]:
        if rule["reason"] != prev:
            order += 1
        prev = rule["reason"]
        lines.append(f"| {order} | {rule['col']} | {rule['name']} | {rule.get('unit', '0 또는 1')} | {rule_cond(rule)} | "
                     f"{rule['reason']} | {reason[rule['reason']]} |")
    lines += ["", "## 집계 범위", "", "| 열 이름 | 화면 이름 | 단위 | 처음 값 |", "|---|---|---|---|"]
    for sc in cfg["scopes"]:
        lines.append(f"| {sc['col']} | {sc['name']} | {sc['unit']} | 데이터 최댓값 (모두 집계) |")
    lines += ["", "## 확인용 숫자", "",
              f"이 기준표로 `{cfg['dataName']}` 를 다시 판정하면 엑셀의 `{cfg['judgeCol']}` 열과 {r['rows']}줄 모두 같다.",
              f"{L['total']} {r['total']}, {L['pass']} {r['pass']}, {L['fail']} {r['fail']}, {L['rate']} {r['rate']:.2f}%."]
    return "\n".join(lines) + "\n"


def claude_md(ref):
    w, d = ref["wafer"], ref["apple"]
    return f"""# 수율 시뮬레이터 프로젝트

## 만드는 것
엑셀 파일을 읽어, 합격 기준을 조절 바로 바꾸면 수율이 바로 바뀌는 HTML 화면을 만든다.
- 웨이퍼: `data/wafer_test_W07.xlsx` → `output/simulator.html`
- 사과(연습): `data/apple_A07.xlsx` → `output/apple_sim.html`
교시마다 사과로 먼저 같은 기능을 만들고, 이어서 웨이퍼로 만든다.

## 폴더
- `data/` 원본 엑셀. 읽기만 하고 고치지 않는다.
- `docs/` 데이터 요약 · 실험 기록
- `output/` 결과물 (엑셀 · CSV · HTML)
- `scripts/` 파이썬 스크립트
- `templates/` 합격기준표 · 선별기준표 · HTML 예시 · 실험기록 양식

## 데이터
- 엑셀 가로 한 줄 = 칩 한 개 (웨이퍼 맵의 네모 한 칸). 사과는 한 줄 = 사과 한 개 (과수원 지도의 네모 한 칸).
- 웨이퍼 위치 열: `die_x` · `die_y` (맵의 칸 번호), `radius_mm` (중심에서 거리), `zone` (center · mid · edge)
- 사과 위치 열: `tree_x` · `tree_y` (과수원 지도의 칸 번호), `dist_m` (중심에서 거리), `zone` (안쪽 · 중간 · 가장자리)
- 판정 열: 웨이퍼 `pass_fail` · `fail_type`, 사과 `grade` · `reason`
- 합격 기준은 `templates/합격기준표.md` · `templates/선별기준표.md` 를 따른다.

## 작업 규칙
- 답은 한국어로, 쉬운 말로 한다. 반도체 용어를 새로 꺼내지 않는다.
- 화면에는 「다이」 대신 「칩」이라고 쓴다.
- HTML 은 파일 하나에 HTML · CSS · JS 를 모두 넣는다. 외부 라이브러리 없이 SVG 로 그린다.
- 데이터는 CSV 글자 그대로 HTML 안에 넣는다.
- 기능을 더할 때는 이미 있는 화면을 지우지 않고 그 위에 더한다.
- 화면은 1280×720 한 화면에 다 보이게 한다.
- 색: 합격 #2BA84A · 불합격 · 강조 #E8344E · 글자 #17181A · 배경 흰색. 이모지는 쓰지 않는다.
- 파이썬은 pandas · openpyxl 만 쓴다.
- 작업이 끝나면 화면에 보이는 숫자(전체 · 합격 · 불합격 · 수율)를 보고한다.

## 정답 숫자 (교육용 합성 데이터 기준)
- 웨이퍼 W07: 전체 {w['total']} · 합격 {w['pass']} · 불합격 {w['fail']} · 수율 {w['rate']:.2f}%
- 사과 A07: 전체 {d['total']} · 상품 {d['pass']} · 불량 {d['fail']} · 상품률 {d['rate']:.2f}%
"""


EXPERIMENT_FORM = """# 수율 시뮬레이터 실험 기록

데이터: (   ) · 처음 수율: (   )%

| 번호 | 움직인 조절 바 | 집계 대상 | 합격 | 수율(%) | 처음 대비(%p) |
|---|---|---|---|---|---|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |

## 목표 수율을 맞춘 조합
- 데이터:
- 목표 수율: (   )%
- 움직인 조절 바와 값:
- 나온 수율: (   )%
- 내려받은 파일 이름:

## 발표 한 줄
(수율이 가장 크게 움직인 조절 바와 그 숫자)
"""


def make_lab(ref):
    shutil.rmtree(LAB / "data", ignore_errors=True)
    shutil.rmtree(LAB / "templates", ignore_errors=True)
    (LAB / "data").mkdir(parents=True, exist_ok=True)
    (LAB / "templates").mkdir()
    (LAB / "CLAUDE.md").write_text(claude_md(ref), encoding="utf-8")
    (LAB / "templates" / "합격기준표.md").write_text(criteria_md("wafer", ref), encoding="utf-8")
    (LAB / "templates" / "선별기준표.md").write_text(criteria_md("apple", ref), encoding="utf-8")
    (LAB / "templates" / "실험기록_양식.md").write_text(EXPERIMENT_FORM, encoding="utf-8")
    for d in ("docs", "output", "scripts"):
        (LAB / d).mkdir(exist_ok=True)
        (LAB / d / ".gitkeep").touch()
    for dom in DOMAINS.values():
        csv_to_xlsx(dom["src"], LAB / "data" / dom["xlsx"], Path(dom["xlsx"]).stem)
        csv_to_xlsx(dom["alt"], LAB / "data" / dom["alt_xlsx"], Path(dom["alt_xlsx"]).stem)
    shutil.copy(SRC / "html_css_js_예시.html", LAB / "templates" / "html_css_js_예시.html")


# ───────────────────────── 완성본 ─────────────────────────
STAGES = ["1", "2", "3a", "3b", "4", "5", "6", "7", "8"]
HTML_TPL = {"3a": "s3a.html", "3b": "s3b.html", "4": "s4.html", "5": "s5.html", "6": "s6.html", "7": "s78.html", "8": "s78.html"}


def cfg_js(cfg):
    return json.dumps(cfg, ensure_ascii=False, indent=2)


def render(tpl, cfg, csv_text, stage):
    t = (SRC / tpl).read_text(encoding="utf-8")
    if tpl == "s78.html":  # 8교시 기능은 /*s8*/ … /*/s8*/ · <!--s8--> … <!--/s8--> 안에 있다
        if stage == "7":
            t = re.sub(r"(?s)[ \t]*/\*s8\*/\n.*?/\*/s8\*/\n", "", t)
            t = re.sub(r"(?s)<!--s8-->\n.*?<!--/s8-->\n", "", t)
        t = re.sub(r"[ \t]*(/\*/?s8\*/|<!--/?s8-->)\n", "", t)
    t = t.replace("__TITLE__", cfg["title"]).replace("/*__CFG__*/{}", cfg_js(cfg))
    return t.replace("__CSV__", csv_text.strip().replace("\\", "\\\\").replace("`", "\\`"))


def run_scripts(stage_dir):
    """2교시 스크립트를 실제로 돌려 엑셀 · CSV 를 만든다 (data 는 실습 폴더 것을 잠깐 연결)."""
    link = stage_dir / "data"
    if link.exists() or link.is_symlink():
        link.unlink()
    link.symlink_to(os.path.relpath(LAB / "data", stage_dir))
    try:
        for dom in DOMAINS.values():
            subprocess.run([sys.executable, f"scripts/{dom['script']}"], cwd=stage_dir, check=True,
                           stdout=subprocess.DEVNULL)
    finally:
        link.unlink()


def summary_doc(dom, ref):
    cfg, n = dom["cfg"], ref
    L = cfg["labels"]
    rows = read_rows(dom["src"])
    head = list(rows[0].keys())
    lines = [f"# {cfg['dataName']} 데이터 요약", "",
             f"- 줄 수: {n['rows']}줄 (한 줄 = {cfg['item']} 한 {cfg['count']})",
             f"- 열 수: {len(head)}개", "", "## 열 묶음", ""]
    if cfg["item"] == "칩":
        groups = [("이름표", ["lot_id", "wafer_id"]), ("위치", ["die_x", "die_y", "center_x_mm", "center_y_mm", "radius_mm", "zone"]),
                  ("측정값", ["vth_v", "idsat_ma", "ioff_na", "rc_ohm", "ox_thk_nm", "crack", "particle_cnt"]),
                  ("판정", ["bin", "fail_type", "pass_fail"])]
    else:
        groups = [("이름표", ["date", "apple_id", "variety"]), ("위치", ["tree_x", "tree_y", "dist_m", "zone"]),
                  ("측정값", ["weight_g", "diameter_mm", "sugar_brix", "bruise", "worm"]),
                  ("판정", ["reason", "grade"])]
    lines += ["| 묶음 | 열 |", "|---|---|"] + [f"| {g} | {', '.join(c)} |" for g, c in groups]
    lines += ["", "## 판정 숫자", "", f"| 항목 | 값 |", "|---|---|",
              f"| {L['total']} | {n['total']} |", f"| {L['pass']} | {n['pass']} |", f"| {L['fail']} | {n['fail']} |",
              f"| {L['rate']} | {n['rate']:.2f}% |", "", "## 사유별", "", "| 사유 | 개수 |", "|---|---|"]
    lines += [f"| {name} | {v} |" for name, v in n["reasons_sorted"]]
    return "\n".join(lines) + "\n"


def result_csv(dom, rows_raw, spec, name):
    """8교시 「내려받기」 와 같은 모양: 기준 줄 → 빈 줄 → 판정 결과 표."""
    cfg = dom["cfg"]
    rows = to_num(rows_raw, cfg)
    out = io.StringIO()
    w = csv.writer(out, lineterminator="\n")
    w.writerow(["기준", "값"])
    w.writerow(["데이터", name])
    for rule in cfg["rules"]:
        s = spec[rule["col"]]
        if rule.get("kind") == "flag":
            w.writerow([rule["name"], "판정함" if s["on"] else "판정 안 함"])
        else:
            if s.get("lo") is not None:
                w.writerow([f"{rule['name']} 하한({rule['unit']})", fmtnum(s["lo"])])
            if s.get("hi") is not None:
                w.writerow([f"{rule['name']} 상한({rule['unit']})", fmtnum(s["hi"])])
    for sc in cfg["scopes"]:
        w.writerow([f"{sc['name']} 상한({sc['unit']})", fmtnum(spec[sc["col"]]["hi"])])
    ev = evaluate(rows, cfg, spec)
    w.writerow([cfg["labels"]["rate"] + "(%)", f"{ev['rate']:.2f}"])
    w.writerow([])
    head = list(rows_raw[0].keys())
    w.writerow(head + ["sim_scope", "sim_reason", "sim_result"])
    for raw, r in zip(rows_raw, rows):
        ins = in_scope(r, cfg, spec)
        k = judge(r, cfg, spec)
        w.writerow([raw[h] for h in head] + ["IN" if ins else "OUT", k, (cfg["passValue"] if k == "none" else cfg.get("failValue", "FAIL")) if ins else ""])
    return "﻿" + out.getvalue()


def xlsx_rows(p):
    from openpyxl import load_workbook
    ws = load_workbook(p, read_only=True).worksheets[0]
    it = ws.iter_rows(values_only=True)
    head = [str(h) for h in next(it)]

    def js(v):  # 브라우저 Number → 글자와 같은 모양 (-35.0 → -35)
        if isinstance(v, float):
            return str(int(v)) if v.is_integer() else repr(v)
        return "" if v is None else str(v)
    return [dict(zip(head, map(js, r))) for r in it]


def fmtnum(v):
    return str(int(v)) if float(v).is_integer() else str(v)


def make_solution(ref):
    if SOL.exists():
        shutil.rmtree(SOL)
    for st in STAGES:
        d = SOL / f"stage{st}"
        for sub in ("docs", "output", "scripts"):
            (d / sub).mkdir(parents=True)
        n = int(st[0])
        for key, dom in DOMAINS.items():
            r = ref[key]
            name = "데이터_요약.md" if key == "wafer" else "사과_요약.md"
            (d / "docs" / name).write_text(summary_doc(dom, r), encoding="utf-8")
            if n >= 2:
                shutil.copy(SRC / "scripts" / dom["script"], d / "scripts" / dom["script"])
        if n >= 2:
            run_scripts(d)
        if st in HTML_TPL:
            for key, dom in DOMAINS.items():
                csv_text = (d / "output" / Path(dom["xlsx"]).with_suffix(".csv").name).read_text(encoding="utf-8")
                (d / "output" / dom["html"]).write_text(render(HTML_TPL[st], dom["cfg"], csv_text, st), encoding="utf-8")
        if st == "8":
            for key, dom in DOMAINS.items():
                r = ref[key]
                combo = r["s8_target"]["pick"]
                if combo["data"] == "alt":  # 화면이 엑셀을 불러온 것과 같은 글자로
                    rows_raw = xlsx_rows(LAB / "data" / dom["alt_xlsx"])
                else:                       # 화면에 넣은 CSV 글자 그대로
                    rows_raw = read_rows(d / "output" / Path(dom["xlsx"]).with_suffix(".csv").name)
                cfg = dom["cfg"]
                spec = base_spec(cfg, to_num(rows_raw, cfg))
                for c in combo["set"]:
                    spec[c["col"]][c["side"]] = c["value"]
                fname = combo["data_file"]
                out = d / "output" / f"판정결과_{Path(fname).stem}.csv"
                out.write_text(result_csv(dom, rows_raw, spec, fname), encoding="utf-8")
            (d / "docs" / "실험기록.md").write_text(experiment_doc(ref), encoding="utf-8")
    for sub in SOL.glob("stage*/*"):
        if sub.is_dir() and not any(sub.iterdir()):
            (sub / ".gitkeep").touch()


def experiment_doc(ref):
    out = []
    for key, title in (("wafer", "웨이퍼"), ("apple", "사과")):
        r, cfg = ref[key], DOMAINS[key]["cfg"]
        L = cfg["labels"]
        out += [f"# {title} 실험 기록", "", f"데이터: {r['file']} · 처음 {L['rate']}: {r['rate']:.2f}%", "",
                f"| 번호 | 움직인 조절 바 | {L['scope']} | {L['pass']} | {L['rate']}(%) | 처음 대비(%p) |", "|---|---|---|---|---|---|"]
        for i, c in enumerate(r["s7_checks"][:3], 1):
            out.append(f"| {i} | {c['op']} | {c['total']} | {c['pass']} | {c['rate']:.2f} | {c['delta_pp']:+.2f} |")
        p = r["s8_target"]["pick"]
        out += ["", f"## 목표 {L['rate']}을 맞춘 조합", "", f"- 데이터: {p['data_file']}",
                f"- 목표 {L['rate']}: {r['s8_target']['target']}%",
                "- 움직인 조절 바와 값: " + " · ".join(f"{c['label']} {c['display']}" for c in p["set"]),
                f"- 나온 {L['rate']}: {p['rate']:.2f}%", f"- 내려받은 파일 이름: 판정결과_{Path(p['data_file']).stem}.csv", ""]
    return "\n".join(out)


# ───────────────────────── 캡처 ─────────────────────────
def shot(html, out_webp, hash_="", wait=1500):
    with tempfile.TemporaryDirectory() as td:
        png = Path(td) / "s.png"
        url = Path(html).resolve().as_uri() + hash_
        subprocess.run([CHROME, "--headless", "--disable-gpu", "--hide-scrollbars", "--window-size=1280,720",
                        f"--virtual-time-budget={wait}", f"--screenshot={png}", url],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["cwebp", "-q", "80", "-quiet", str(png), "-o", str(out_webp)], check=True)


def alt_copy(html, dom, td):
    """불러오기 후 화면: 둘째 파일 CSV 를 넣은 사본 (headless 에서는 파일 선택을 누를 수 없다)."""
    t = Path(html).read_text(encoding="utf-8")
    i, j = t.index("const CSV_TEXT = `") + len("const CSV_TEXT = `"), t.index("`;", t.index("const CSV_TEXT = `"))
    alt = dom["alt"].read_text(encoding="utf-8").strip()
    t = t[:i] + alt + t[j:]
    t = t.replace(f'"dataName": "{dom["cfg"]["dataName"]}"', f'"dataName": "{dom["alt_xlsx"]}"')
    p = Path(td) / f"alt_{dom['html']}"
    p.write_text(t, encoding="utf-8")
    return p


def make_shots(ref):
    IMG.mkdir(parents=True, exist_ok=True)
    for key, dom in DOMAINS.items():
        for st in HTML_TPL:
            shot(SOL / f"stage{st}" / "output" / dom["html"], IMG / f"{key}_s{st}.webp")
        r = ref[key]
        sl = r["s6_slider"]
        v = "5" if key == "wafer" else "12"
        shot(SOL / "stage6" / "output" / dom["html"], IMG / f"{key}_s6_moved.webp", f"#{sl['col']}_{sl['side']}={v}")
        shot(SOL / "stage7" / "output" / dom["html"], IMG / f"{key}_s7_moved.webp", r["s7_checks"][0]["hash"])
        p = r["s8_target"]["pick"]
        with tempfile.TemporaryDirectory() as td:
            html = SOL / "stage8" / "output" / dom["html"]
            if p["data"] == "alt":
                a = alt_copy(html, dom, td)
                shot(a, IMG / f"{key}_s8_loaded.webp")
                shot(a, IMG / f"{key}_s8_target.webp", p["hash"])
            else:
                a = alt_copy(html, dom, td)
                shot(a, IMG / f"{key}_s8_loaded.webp")
                shot(html, IMG / f"{key}_s8_target.webp", p["hash"])
        xlsx_shot(SOL / "stage2" / "output" / dom["summary"], IMG / f"xlsx_{key}.webp")


def xlsx_shot(xlsx, out):
    from openpyxl import load_workbook
    wb = load_workbook(xlsx)
    parts = []
    for ws in wb.worksheets:
        rows = list(ws.iter_rows(values_only=True))
        th = "".join(f"<th>{v}</th>" for v in rows[0])
        tb = "".join("<tr>" + "".join(f"<td>{'' if v is None else v}</td>" for v in r) + "</tr>" for r in rows[1:])
        parts.append(f"<section><div class='tab'>{ws.title}</div><table><tr>{th}</tr>{tb}</table></section>")
    html = ("<!doctype html><meta charset=utf-8><style>body{margin:0;padding:28px;font:15px -apple-system,'Apple SD Gothic Neo',sans-serif;"
            "color:#17181A;background:#fff;display:flex;gap:24px;align-items:flex-start}section{flex:1}"
            ".tab{display:inline-block;background:#E8F5EC;border:1px solid #2BA84A;border-bottom:0;padding:5px 14px;font-weight:700;border-radius:6px 6px 0 0}"
            "table{border-collapse:collapse;width:100%}th,td{border:1px solid #C9CDD1;padding:6px 9px;text-align:left}"
            "th{background:#F2F3F4}</style>" + "".join(parts))
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "x.html"
        p.write_text(html, encoding="utf-8")
        shot(p, out)


# ───────────────────────── main ─────────────────────────
def main():
    ref = {"note": "labs/make_sim.py 가 계산 · 합성 데이터 기준 · rate 는 % (소수 둘째 자리)"}
    for key, dom in DOMAINS.items():
        ref[key] = numbers(dom)
    # 8교시 목표 조합 (웨이퍼는 손으로 고른 값 · 사과는 find_pick 이 찾은 값)
    w = ref["wafer"]
    wcfg = DOMAINS["wafer"]["cfg"]
    walt = to_num(read_rows(DOMAINS["wafer"]["alt"]), wcfg)
    wsp = base_spec(wcfg, walt)
    w["s8_target"]["pick"] = {"data": "alt", "data_file": DOMAINS["wafer"]["alt_xlsx"],
                              **pick_combo(wcfg, walt, wsp, [("ioff_na", "hi", 30), ("vth_v", "hi", 0.55)])}
    ap, acfg = ref["apple"], DOMAINS["apple"]["cfg"]
    for data, src, fname in (("main", "src", acfg["dataName"]), ("alt", "alt", DOMAINS["apple"]["alt_xlsx"])):
        arows = to_num(read_rows(DOMAINS["apple"][src]), acfg)
        asp = base_spec(acfg, arows)
        steps = find_pick(acfg, arows, asp, acfg["target"])
        if steps:   # A07 에서 되면 A07, 안 되면 A25
            ap["s8_target"]["pick"] = {"data": data, "data_file": fname, **pick_combo(acfg, arows, asp, steps)}
            break
    for key in ("wafer", "apple"):
        cfg = DOMAINS[key]["cfg"]
        names = {r["col"]: r["name"] for r in cfg["rules"]} | {s["col"]: s["name"] for s in cfg["scopes"]}
        for c in ref[key]["s8_target"]["pick"]["set"]:
            c["label"] = names[c["col"]] + {"lo": " 하한", "hi": " 상한", "on": " 판정"}[c["side"]]
            c["display"] = ("켜기" if c["value"] else "끄기") if c["side"] == "on" else fmtnum(c["value"])
    (ROOT / "sim_ref.json").write_text(json.dumps(ref, ensure_ascii=False, indent=1), encoding="utf-8")
    make_lab(ref)
    make_solution(ref)
    if "--no-shots" not in sys.argv and Path(CHROME).exists():
        make_shots(ref)
    for key in ("wafer", "apple"):
        r = ref[key]
        print(key, r["total"], r["pass"], r["fail"], r["rate"], "재판정 일치" if r["rejudge_match"] else f"불일치 {r['rejudge_mismatch']}")


if __name__ == "__main__":
    main()
