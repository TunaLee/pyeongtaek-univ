"""공통 — 경로 · 스펙 · 양불 판정 (판정 순서는 CLAUDE.md 와 같다)."""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent          # 프로젝트 폴더
DATA = ROOT / "data"
OUT = ROOT / "output"
ORDER = ["crack", "open_short", "leakage", "vth_shift", "particle", "parametric"]
BIN = {"none": 1, "vth_shift": 2, "leakage": 3, "open_short": 4, "crack": 5, "particle": 6, "parametric": 7, "retest": 9}
MEAS = ["vth_v", "idsat_ma", "ioff_na", "rc_ohm", "ox_thk_nm", "crack", "particle_cnt"]
KO = {"none": "양품", "crack": "크랙", "open_short": "오픈·쇼트", "leakage": "누설전류", "vth_shift": "문턱전압 이탈",
      "particle": "파티클", "parametric": "기타 파라미터", "retest": "재측정"}
COLOR = {"none": "#2BA84A", "crack": "#7B1FA2", "open_short": "#1565C0", "leakage": "#E65100", "vth_shift": "#C62828",
         "particle": "#00897B", "parametric": "#6D4C41", "retest": "#9E9E9E"}


def judge(r):
    """다이 한 개 → fail_type. 측정값이 비면 retest."""
    if any(pd.isna(r[c]) for c in MEAS):
        return "retest"
    if r.crack != 0: return "crack"
    if r.rc_ohm > 15: return "open_short"
    if r.ioff_na > 10: return "leakage"
    if not (0.38 <= r.vth_v <= 0.52): return "vth_shift"
    if r.particle_cnt >= 5: return "particle"
    if r.idsat_ma < 0.92 or not (2.85 <= r.ox_thk_nm <= 3.15): return "parametric"
    return "none"


def rejudge(df):
    df = df.copy()
    df["fail_type"] = df.apply(judge, axis=1)
    df["bin"] = df.fail_type.map(BIN)
    df["pass_fail"] = df.fail_type.map(lambda t: "PASS" if t == "none" else ("RETEST" if t == "retest" else "FAIL"))
    return df
