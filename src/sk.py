"""시뮬레이터 과정 공통 — 데이터 · 판정 · 기준 숫자. 교시 모듈(p1 … p8)이 쓴다.

웨이퍼: labs/wafer-lab/data/wafer_test_W07.csv (합성 · 616칩) + spec.csv(합격 기준표)
택배:   labs/wafer-lab/data/practice/delivery_D07.csv (합성 · 600건) · 판정 파손 → 주소 오류 → 지연 → 부재
화면 숫자는 여기서 계산한다(손으로 적지 않는다). 조절 바를 바꾼 숫자도 같은 판정 함수로 구한다.
"""
import json

import pandas as pd

from pkit import LAB

DATA = LAB / "wafer-lab" / "data"
SPEC = pd.read_csv(DATA / "spec.csv")
ORDER = ["crack", "open_short", "leakage", "vth_shift", "particle", "parametric"]
KO = {"crack": "깨짐 · 긁힘", "open_short": "접촉저항 초과", "leakage": "누설전류 초과", "vth_shift": "문턱전압 범위 밖",
      "particle": "먼지 많음", "parametric": "기타 측정값", "none": "합격"}
COL_KO = {"crack": "깨짐 · 긁힘", "rc_ohm": "접촉저항", "ioff_na": "누설전류", "vth_v": "문턱전압",
          "particle_cnt": "먼지 개수", "idsat_ma": "포화전류", "ox_thk_nm": "산화막 두께"}
ZONE_KO = {"center": "중심", "mid": "중간", "edge": "가장자리"}
D_ORDER = ["damaged", "addr_error", "late", "absent"]
D_KO = {"damaged": "파손", "addr_error": "주소 오류", "late": "지연", "absent": "부재", "none": "정시"}
AREA = ["도심", "중간", "외곽"]
PROMISE = 120
SIM = json.loads((LAB / "sim_ref.json").read_text(encoding="utf-8"))  # labs/make_sim.py 결과 · 시뮬레이터 화면 숫자


def wafer(w="W07"):
    return pd.read_csv(DATA / f"wafer_test_{w}.csv") if w == "W07" else pd.read_csv(DATA / "raw" / f"wafer_test_{w}.csv")


def delivery():
    return pd.read_csv(DATA / "practice" / "delivery_D07.csv")


def limits(**over):
    """기준표 → {열: (하한, 상한)} · over 로 바꿈 (예: ioff_na=(None, 20))."""
    lim = {r.param: (None if pd.isna(r.lsl) else r.lsl, None if pd.isna(r.usl) else r.usl) for r in SPEC.itertuples()}
    lim.update(over)
    return lim


def judge(df, **over):
    """기준표 순서대로 · 처음 걸린 사유 하나 · 안 걸리면 none."""
    lim = limits(**over)
    ft = pd.Series("none", index=df.index)
    for t in reversed(ORDER):
        bad = pd.Series(False, index=df.index)
        for p in SPEC[SPEC.fail_type == t].param:
            lo, hi = lim[p]
            if lo is not None:
                bad |= df[p] < lo
            if hi is not None:
                bad |= df[p] > hi
        ft[bad] = t
    return ft


def yld(df, **over):
    ft = judge(df, **over)
    return int((ft == "none").sum()), round((ft == "none").mean() * 100, 2)


def d_judge(df, promise=PROMISE):
    r = pd.Series("none", index=df.index)
    r[df.absent == 1] = "absent"
    r[df.delivery_min > promise] = "late"
    r[df.addr_error == 1] = "addr_error"
    r[df.damaged == 1] = "damaged"
    return r


def d_rate(df, promise=PROMISE):
    r = d_judge(df, promise)
    return int((r == "none").sum()), round((r == "none").mean() * 100, 2)


W07 = wafer()
D07 = delivery()
assert (judge(W07) == W07.fail_type).all(), "기준표 재판정이 fail_type 과 다르다"
assert (d_judge(D07) == D07.reason).all(), "택배 판정이 reason 과 다르다"
WN = {"rows": len(W07), "cols": W07.shape[1], "pass": yld(W07)[0], "fail": len(W07) - yld(W07)[0], "yield": yld(W07)[1],
      "reason": judge(W07).value_counts().drop("none").reindex(ORDER).to_dict(),
      "zone": {z: round((g.pass_fail == "PASS").mean() * 100, 2) for z, g in W07.groupby("zone")}}
DN = {"rows": len(D07), "cols": D07.shape[1], "pass": d_rate(D07)[0], "fail": len(D07) - d_rate(D07)[0], "rate": d_rate(D07)[1],
      "reason": d_judge(D07).value_counts().drop("none").reindex(D_ORDER).fillna(0).astype(int).to_dict(),
      "area": {a: round((g.status == "ON_TIME").mean() * 100, 2) for a, g in D07.groupby("area")}}


# ── 화면 도구 ───────────────────────────────────────
FOLDER = "sim-lab"
CSS = """
  .skduo{display:grid; grid-template-columns:1fr 1fr; gap:22px; align-items:start;}
  .skduo figure{margin:0; opacity:0; animation:skIn .5s var(--d) forwards;}
  .skduo figure b{display:block; font-size:18px; color:#16233A; margin-bottom:8px;}
  .skduo img{width:100%; border:1.5px solid #D9DDE3; border-radius:12px; box-shadow:0 8px 22px rgba(15,27,45,.10); background:#fff;}
  .skone img{width:100%; max-height:450px; object-fit:contain; object-position:top; border:1.5px solid #D9DDE3; border-radius:12px; box-shadow:0 8px 22px rgba(15,27,45,.10); background:#fff;}
  .skgrp{display:grid; grid-template-columns:repeat(4,1fr); gap:14px; margin-top:8px;}
  .skg{border-radius:14px; padding:16px 16px 14px; border:2px solid #C9D6E6; background:#fff; opacity:0; animation:skIn .45s var(--d) forwards;}
  .skg b{display:block; font-size:21px; color:#16233A; margin-bottom:10px;}
  .skg code{display:block; font-family:var(--mono); font-size:14.5px; color:#1F3A5F; background:#F4F6F9; border-radius:6px; padding:3px 8px; margin:4px 0;}
  .skg small{display:block; margin-top:10px; font-size:14.5px; color:#6B7785;}
  .skg.k{border-color:#F28C28; background:#FFF8F0;}
  .skg.dim{border-style:dashed; background:#F7F8FA;} .skg.dim code{color:#9AA3AF;}
  .skg.dim small{color:#E07A12; font-weight:800;}
  .skhcj{display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:18px;}
  .skhcj > div{display:flex; flex-direction:column; gap:10px; opacity:0; animation:skIn .5s var(--d) forwards;}
  .skhcj > div > b{font-size:20px; color:#16233A;} .skhcj > div > b small{font-size:14px; color:#6B7785; font-weight:600; margin-left:6px;}
  .skhcj .code{margin:0;} .skhcj .code pre, .skhcj .code code{font-size:12.5px !important; white-space:pre;}
  .skhcj .pv{border:1.5px solid #D9DDE3; border-radius:10px; background:#fff; padding:12px; min-height:118px; font-family:var(--sans);}
  @keyframes skIn{from{opacity:0; transform:translateY(8px)} to{opacity:1; transform:none}}
  @media print{.skduo figure,.skg,.skhcj > div{animation:none; opacity:1}}
"""


def duo(a, b, la, lb):
    """두 화면 나란히 · docs/img/ 아래 경로."""
    return (f'<div class="skduo"><figure style="--d:.2s"><b>{la}</b><img src="img/{a}" alt="{la}"/></figure>'
            f'<figure style="--d:1.2s"><b>{lb}</b><img src="img/{b}" alt="{lb}"/></figure></div>')


def one(img, alt):
    return f'<div class="skone"><img src="img/{img}" alt="{alt}"/></div>'


def groups(gs):
    """열 묶음 카드 · gs=[(머리, [열], 아래 줄, 'k'|'dim'|'')]."""
    return '<div class="skgrp">' + "".join(
        f'<div class="skg {k}" style="--d:{.2 + i * .35:.2f}s"><b>{h}</b>{"".join(f"<code>{c}</code>" for c in cs)}<small>{t}</small></div>'
        for i, (h, cs, t, k) in enumerate(gs)) + "</div>"
