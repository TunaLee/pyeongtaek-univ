"""실습 데이터 생성기 — 합성 웨이퍼 테스트 CSV (LOT 1개 · 웨이퍼 25장 · 다이 616개/장).

실행: python3 labs/make_data.py   → labs/wafer-lab/data/ 를 새로 만든다 (시드 고정 · 매번 같은 결과)

설계
- 300 mm 웨이퍼 · 다이 10×10 mm · 가장자리 제외 3 mm → Gross die 616.
- 설비 3대: ETCH_01(W01~W08) · ETCH_02(W09~W16) · ETCH_03(W17~W25). ETCH_03 은 가장자리 링 불량이 강하다(원인 후보 실습).
- 웨이퍼별 패턴: W07 스크래치(대각선) · W12 중심 클러스터 · 나머지는 랜덤 + 약한 가장자리.
- 정제 실습용 결함(원시 파일에만): W05 중복 행 · W11 vth 단위 mV · W19 ioff_na 결측.
- 원시 파일의 bin · fail_type · pass_fail 은 테스터 판정. spec.csv 로 다시 판정하면 W11 은 전부 vth_shift 로 잘못 나온다(단위 오류를 찾게 하는 장치).
"""
import csv
import json
import shutil
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
LAB = ROOT / "wafer-lab"
DATA = LAB / "data"
RAW = DATA / "raw"
LOT = "LOT2611-07"
R_WAFER, EDGE, DIE = 150.0, 3.0, 10.0
FAIL_ORDER = ["crack", "open_short", "leakage", "vth_shift", "particle", "parametric"]
BIN = {"none": 1, "vth_shift": 2, "leakage": 3, "open_short": 4, "crack": 5, "particle": 6, "parametric": 7}
HEADER = ["lot_id", "wafer_id", "die_x", "die_y", "center_x_mm", "center_y_mm", "radius_mm", "zone", "vth_v", "idsat_ma",
          "ioff_na", "rc_ohm", "ox_thk_nm", "crack", "particle_cnt", "bin", "fail_type", "pass_fail"]
SPEC = [  # param, lsl, usl, unit, fail_type
    ("vth_v", 0.38, 0.52, "V", "vth_shift"), ("idsat_ma", 0.92, "", "mA", "parametric"),
    ("ioff_na", "", 10, "nA", "leakage"), ("rc_ohm", "", 15, "Ω", "open_short"),
    ("ox_thk_nm", 2.85, 3.15, "nm", "parametric"), ("crack", "", 0, "개", "crack"), ("particle_cnt", "", 4, "개", "particle")]


def eqp_of(w):
    return "ETCH_01" if w <= 8 else ("ETCH_02" if w <= 16 else "ETCH_03")


def dies():
    r = R_WAFER - EDGE
    out = []
    for dy in range(-15, 15):
        for dx in range(-15, 15):
            if all(((dx + a) * DIE) ** 2 + ((dy + b) * DIE) ** 2 <= r * r for a in (0, 1) for b in (0, 1)):
                out.append((dx, dy, (dx + .5) * DIE, (dy + .5) * DIE))
    return np.array(out)


def classify(vth, idsat, ioff, rc, ox, crack, particle):
    if crack: return "crack"
    if rc > 15: return "open_short"
    if ioff > 10: return "leakage"
    if not (0.38 <= vth <= 0.52): return "vth_shift"
    if particle >= 5: return "particle"
    if idsat < 0.92 or not (2.85 <= ox <= 3.15): return "parametric"
    return "none"


def wafer(w, rng, d):
    n = len(d)
    cx, cy = d[:, 2], d[:, 3]
    r = np.hypot(cx, cy)
    eqp = eqp_of(w)
    vth = rng.normal(0.452, 0.019, n) + 0.016 * r / R_WAFER
    idsat = rng.normal(1.05, 0.04, n)
    ioff = np.exp(rng.normal(np.log(2.0), 0.45, n))
    rc = rng.normal(8.0, 1.2, n)
    ox = rng.normal(3.00, 0.05, n) - 0.03 * r / R_WAFER
    particle = rng.poisson(0.55, n)
    crack = np.zeros(n, dtype=int)
    hit = np.zeros(n, dtype=bool)
    # 가장자리 링 — ETCH_03 은 강하게, 나머지는 약하게
    p_ring = 0.30 if eqp == "ETCH_03" else 0.07
    m = (r > 120) & (rng.random(n) < p_ring)
    leak = m & (rng.random(n) < .6)
    ioff[leak] = rng.uniform(14, 60, leak.sum())
    vth[m & ~leak] = rng.uniform(.53, .60, (m & ~leak).sum())
    hit |= m
    if w == 7:  # 스크래치 — 대각선 한 줄
        m = (np.abs(cy - (-0.9 * cx + 10)) < 7) & (np.abs(cx) < 90) & ~hit
        crack[m] = 1
        hit |= m
    if w == 12:  # 중심 클러스터
        m = (np.hypot(cx - 5, cy + 5) <= 28) & (rng.random(n) < .65) & ~hit
        rc[m] = rng.uniform(18, 32, m.sum())
        hit |= m
    u = rng.random(n)  # 랜덤 불량 — 다이마다 독립
    m = ~hit & (u < .012); particle[m] = rng.integers(5, 12, m.sum())
    m = ~hit & (u >= .012) & (u < .025); idsat[m] = rng.uniform(.82, .91, m.sum())
    m = ~hit & (u >= .025) & (u < .035); rc[m] = rng.uniform(16, 26, m.sum())
    vth, idsat, ioff, rc, ox = (np.round(x, k) for x, k in ((vth, 3), (idsat, 3), (ioff, 2), (rc, 2), (ox, 3)))
    zone = np.where(r < 50, "center", np.where(r <= 110, "mid", "edge"))
    rows = []
    for i in range(n):
        ft = classify(vth[i], idsat[i], ioff[i], rc[i], ox[i], crack[i], particle[i])
        rows.append([LOT, f"W{w:02d}", int(d[i, 0]), int(d[i, 1]), f"{cx[i]:.1f}", f"{cy[i]:.1f}", f"{r[i]:.1f}", zone[i],
                     f"{vth[i]:.3f}", f"{idsat[i]:.3f}", f"{ioff[i]:.2f}", f"{rc[i]:.2f}", f"{ox[i]:.3f}", int(crack[i]),
                     int(particle[i]), BIN[ft], ft, "PASS" if ft == "none" else "FAIL"])
    return rows


def write(path, header, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(header)
        wr.writerows(rows)


def main():
    if RAW.exists():
        shutil.rmtree(RAW)  # secom/ 은 make_secom.py 가 따로 만든다
    RAW.mkdir(parents=True)
    rng = np.random.default_rng(2611)
    d = dies()
    ref = {"gross_die": len(d), "wafers": {}}
    eq_rows = []
    for w in range(1, 26):
        rows = wafer(w, rng, d)
        clean = [r[:] for r in rows]
        npass = sum(r[-1] == "PASS" for r in clean)
        cnt = {t: sum(r[16] == t for r in clean) for t in FAIL_ORDER}
        ref["wafers"][f"W{w:02d}"] = {"eqp": eqp_of(w), "pass": npass, "yield": round(npass / len(d) * 100, 2), **cnt}
        # 원시 파일 결함
        if w == 5:
            dup = [rows[i] for i in rng.choice(len(rows), 12, replace=False)]
            rows = rows[:300] + dup + rows[300:]
        if w == 11:
            for r_ in rows:
                r_[8] = f"{float(r_[8]) * 1000:.1f}"
        if w == 19:
            for i in rng.choice(len(rows), 9, replace=False):
                rows[i][10] = ""
        write(RAW / f"wafer_test_W{w:02d}.csv", HEADER, rows)
        eq_rows.append([f"W{w:02d}", eqp_of(w), "CH" + "AB"[w % 2], f"2026-11-{3 + (w - 1) // 5:02d}"])
    write(DATA / "equipment.csv", ["wafer_id", "eqp_id", "chamber", "test_date"], eq_rows)
    write(DATA / "spec.csv", ["param", "lsl", "usl", "unit", "fail_type"], SPEC)
    shutil.copy(RAW / "wafer_test_W07.csv", DATA / "wafer_test_W07.csv")
    ys = [v["yield"] for v in ref["wafers"].values()]
    ref["lot_yield"] = round(sum(v["pass"] for v in ref["wafers"].values()) / (len(d) * 25) * 100, 2)
    ref["eqp_yield"] = {e: round(np.mean([v["yield"] for v in ref["wafers"].values() if v["eqp"] == e]), 2)
                        for e in ("ETCH_01", "ETCH_02", "ETCH_03")}
    ref["raw_issues"] = {"W05": "중복 행 12개", "W11": "vth_v 단위 mV", "W19": "ioff_na 결측 9칸"}
    old = ROOT / "ref.json"
    if old.exists():
        ref["secom"] = json.loads(old.read_text(encoding="utf-8")).get("secom")
    (ROOT / "ref.json").write_text(json.dumps(ref, ensure_ascii=False, indent=1), encoding="utf-8")
    print("gross", len(d), "lot yield", ref["lot_yield"], ref["eqp_yield"], "min", min(ys), "max", max(ys))
    print("W07", ref["wafers"]["W07"])
    print("W12", ref["wafers"]["W12"])


if __name__ == "__main__":
    main()
