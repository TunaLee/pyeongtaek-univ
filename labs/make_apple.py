"""연습 데이터 — 사과 선별 (웨이퍼 데이터와 같은 구조 · 교시마다 [실습 N-1] 에 쓴다).

실행: python3 labs/make_apple.py  → labs/wafer-lab/data/practice/  · ref.json["general"]

구조
  사과 1개 = 1행 = 과수원 지도 한 칸(나무 한 그루에서 고른 사과)
  하루 파일 A01~A25 (10월 1일~25일 수확) · 화면 기본 파일은 A07
  열 이름은 모두 한글 (처음 다루는 데이터 · 웨이퍼는 영어 열 이름)
  위치 가로칸 · 세로칸 (1~30 · 1~20 · 과수원 지도의 칸 번호) · 중심거리(m) · 위치(안쪽 · 중간 · 가장자리)
  측정 무게(g) · 지름(mm) · 당도(brix) · 검사 멍 · 벌레 (0 · 1)
  판정 순서 멍 → 벌레 먹음 → 무게 미달(250g 미만) → 당도 미달(11 brix 미만) → 상품 · 불량사유 · 등급
  상품률 = 상품 ÷ 전체
"""
import csv
import json
import shutil
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "wafer-lab" / "data" / "practice"
RAW = OUT / "raw"
HEADER = ["날짜", "사과번호", "가로칸", "세로칸", "중심거리", "위치", "품종", "무게", "지름", "당도",
          "멍", "벌레", "불량사유", "등급"]
MIN_WEIGHT, MIN_SUGAR = 250, 11.0
NX, NY, STEP = 30, 20, 4.0          # 나무 30 × 20 그루 · 나무 간격 4m


def judge(bruise, worm, w, b):
    if bruise: return "멍"
    if worm: return "벌레 먹음"
    if w < MIN_WEIGHT: return "무게 미달"
    if b < MIN_SUGAR: return "당도 미달"
    return "없음"


def day(k, rng):
    xs, ys = np.meshgrid(np.arange(1, NX + 1), np.arange(1, NY + 1))
    xs, ys = xs.ravel(), ys.ravel()
    n = len(xs)
    cx, cy = (NX + 1) / 2, (NY + 1) / 2
    dist = np.round(np.hypot(xs - cx, ys - cy) * STEP, 1)
    edge = (np.minimum.reduce([xs - 1, NX - xs, ys - 1, NY - ys]))     # 가장자리에서 몇 줄 안쪽
    zone = np.where(edge <= 1, "가장자리", np.where(edge <= 4, "중간", "안쪽"))
    variety = rng.choice(["부사", "홍옥", "감홍"], n, p=[.5, .3, .2])
    ed = (zone == "가장자리").astype(float)
    shift = rng.normal(0, .25)                                         # 날마다 조금씩 다름
    weight = np.round(rng.normal(292, 28, n) - ed * 22, 0)
    diam = np.round(52 + weight * .095 + rng.normal(0, 2.2, n), 1)
    vb = np.select([variety == "부사", variety == "홍옥", variety == "감홍"], [.3, -.4, .7])
    sugar = np.round(rng.normal(12.5 + shift, 1.0, n) + vb - ed * 1.1, 1)
    bruise = (rng.random(n) < .025 + ed * .03).astype(int)
    worm = (rng.random(n) < .015 + ed * .02).astype(int)
    rows = []
    for i in range(n):
        r = judge(bruise[i], worm[i], weight[i], sugar[i])
        rows.append([f"2026-10-{k:02d}", f"A{k:02d}-{i + 1:04d}", int(xs[i]), int(ys[i]), f"{dist[i]:.1f}", zone[i], variety[i],
                     int(weight[i]), f"{diam[i]:.1f}", f"{sugar[i]:.1f}", int(bruise[i]), int(worm[i]), r,
                     "상품" if r == "없음" else "불량"])
    return rows


ODD_DAY = 18          # 특이한 날 — 멍 불량이 몰린 날 (데이터 분석 흐름 · 「특이한 날 들여다보기」 예)


def odd_day(rows):
    """ODD_DAY 하루만 멍 든 사과를 늘린다. 따로 만든 난수만 써서 다른 날(A07 · A25 등) 값은 그대로."""
    r2 = np.random.default_rng(1818)
    for r in rows:
        if r[10] == 0 and r2.random() < .24:
            r[10] = 1
            r[12] = judge(1, r[11], float(r[7]), float(r[9]))
            r[13] = "상품" if r[12] == "없음" else "불량"
    return rows


def write(p, rows):
    with p.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(HEADER)
        w.writerows(rows)


def rate(rows):
    return round(sum(r[-1] == "상품" for r in rows) / len(rows) * 100, 2)


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    RAW.mkdir(parents=True)
    rng = np.random.default_rng(1007)
    stat = {"days": {}}
    allrows = []
    for k in range(1, 26):
        rows = day(k, rng)
        if k == ODD_DAY:
            rows = odd_day(rows)
        allrows += rows
        stat["days"][f"A{k:02d}"] = rate(rows)
        write(RAW / f"apple_A{k:02d}.csv", rows)
    a7 = [r for r in allrows if r[0] == "2026-10-07"]
    write(OUT / "apple_A07.csv", a7)
    stat["rows_per_day"] = len(a7)
    stat["rate_all"] = rate(allrows)
    stat["zone"] = {z: rate([r for r in a7 if r[5] == z]) for z in ("안쪽", "중간", "가장자리")}
    stat["variety"] = {v: rate([r for r in a7 if r[6] == v]) for v in ("부사", "홍옥", "감홍")}
    stat["reason"] = {x: sum(r[12] == x for r in a7) for x in ("멍", "벌레 먹음", "무게 미달", "당도 미달")}
    odd = [r for r in allrows if r[0] == f"2026-10-{ODD_DAY:02d}"]
    rest = [r for r in allrows if r[0] != f"2026-10-{ODD_DAY:02d}"]
    stat["odd_day"] = {"day": f"A{ODD_DAY:02d}", "rate": rate(odd),
                       "reason": {x: sum(r[12] == x for r in odd) for x in ("멍", "벌레 먹음", "무게 미달", "당도 미달")},
                       "reason_avg_other": {x: round(sum(r[12] == x for r in rest) / 24, 1) for x in ("멍", "벌레 먹음", "무게 미달", "당도 미달")}}
    stat["A07"] = {"rows": len(a7), "good": sum(r[-1] == "상품" for r in a7), "rate": rate(a7),
                   "mean_w": round(float(np.mean([r[7] for r in a7])), 1), "std_w": round(float(np.std([r[7] for r in a7], ddof=1)), 1)}
    ref_p = ROOT / "ref.json"
    ref = json.loads(ref_p.read_text(encoding="utf-8"))
    ref["general"] = stat
    ref_p.write_text(json.dumps(ref, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({k: v for k, v in stat.items() if k != "days"}, ensure_ascii=False))
    print(stat["days"])


if __name__ == "__main__":
    main()
