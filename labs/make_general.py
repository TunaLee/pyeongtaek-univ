"""일반 예제 데이터 — 택배 배송 (반도체 데이터와 같은 구조 · 교시마다 「일반 예 → 반도체 적용」 에 쓴다).

실행: python3 labs/make_general.py  → labs/wafer-lab/data/practice/  · ref.json["general"]

대응
  배송 1건 = 1행            ↔ 다이 1개 = 1행
  하루 파일 (D01~D25)        ↔ 웨이퍼 파일 (W01~W25)
  구역 좌표 · 거리 · area    ↔ die_x · die_y · radius_mm · zone
  배송 시간 · 약속 120분     ↔ 측정값 · 스펙
  사유 · 판정                ↔ fail_type · pass_fail
  정시 도착률                ↔ 수율
  차량 TRUCK_A/B/C           ↔ 설비 ETCH_01/02/03 (TRUCK_C 는 외곽 지연이 많다)
정제 실습용 결함: D05 중복 10행 · D11 무게 g 단위 · D19 배송 시간 결측 8칸.
"""
import csv
import json
import shutil
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "wafer-lab" / "data" / "practice"
RAW = OUT / "raw"
HEADER = ["date", "order_id", "zone_x", "zone_y", "dist_km", "area", "truck_id", "weight_kg", "delivery_min",
          "damaged", "addr_error", "absent", "reason", "status"]
PROMISE = 120  # 약속 시간(분)


def judge(dmg, addr, mins, absent):
    """판정 순서: 파손 → 주소 오류 → 지연 → 부재 → 정시."""
    if mins == "" or mins is None:
        return "retest"
    if dmg: return "damaged"
    if addr: return "addr_error"
    if float(mins) > PROMISE: return "late"
    if absent: return "absent"
    return "none"


def day(k, rng):
    rows = []
    n = 600
    zx = rng.integers(-7, 8, n)
    zy = rng.integers(-7, 8, n)
    dist = np.round(np.hypot(zx, zy) * 1.5, 1)
    area = np.where(dist < 4, "도심", np.where(dist <= 8, "중간", "외곽"))
    truck = np.where(dist < 4, "TRUCK_A", np.where(dist <= 8, "TRUCK_B", "TRUCK_C"))
    swap = rng.random(n) < .25  # 일부는 다른 차량이 맡음
    truck = np.where(swap, rng.choice(["TRUCK_A", "TRUCK_B", "TRUCK_C"], n), truck)
    weight = np.round(rng.gamma(2.2, 1.4, n) + .2, 2)
    mins = rng.normal(55, 14, n) + dist * 3.2
    mins += np.where(truck == "TRUCK_C", rng.normal(22, 12, n), 0)
    mins = np.round(np.clip(mins, 15, None), 0)
    dmg = (rng.random(n) < .010).astype(int)
    addr = (rng.random(n) < .012).astype(int)
    absent = (rng.random(n) < .03).astype(int)
    for i in range(n):
        r = judge(dmg[i], addr[i], mins[i], absent[i])
        rows.append([f"2026-10-{k:02d}", f"D{k:02d}-{i + 1:04d}", int(zx[i]), int(zy[i]), f"{dist[i]:.1f}", area[i], truck[i],
                     f"{weight[i]:.2f}", int(mins[i]), int(dmg[i]), int(addr[i]), int(absent[i]), r,
                     "ON_TIME" if r == "none" else "FAIL"])
    return rows


def write(p, rows):
    with p.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(HEADER)
        w.writerows(rows)


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    RAW.mkdir(parents=True)
    rng = np.random.default_rng(1025)
    stat = {"days": {}}
    allrows = []
    for k in range(1, 26):
        rows = day(k, rng)
        allrows += rows
        ok = sum(r[-1] == "ON_TIME" for r in rows)
        stat["days"][f"D{k:02d}"] = round(ok / len(rows) * 100, 2)
        if k == 5:
            rows = rows[:300] + [rows[i] for i in rng.choice(len(rows), 10, replace=False)] + rows[300:]
        if k == 11:
            for r in rows:
                r[7] = f"{float(r[7]) * 1000:.0f}"
        if k == 19:
            for i in rng.choice(len(rows), 8, replace=False):
                rows[i][8] = ""
        write(RAW / f"delivery_D{k:02d}.csv", rows)
    write(OUT / "delivery_D07.csv", [r for r in allrows if r[0] == "2026-10-07"])
    n = len(allrows)
    ok = [r for r in allrows if r[-1] == "ON_TIME"]
    stat["rows_per_day"] = 600
    stat["on_time"] = round(len(ok) / n * 100, 2)
    stat["area"] = {a: round(sum(r[-1] == "ON_TIME" for r in allrows if r[5] == a) / sum(r[5] == a for r in allrows) * 100, 2)
                    for a in ("도심", "중간", "외곽")}
    stat["truck"] = {t: round(sum(r[-1] == "ON_TIME" for r in allrows if r[6] == t) / sum(r[6] == t for r in allrows) * 100, 2)
                     for t in ("TRUCK_A", "TRUCK_B", "TRUCK_C")}
    stat["reason"] = {x: sum(r[12] == x for r in allrows) for x in ("late", "absent", "addr_error", "damaged")}
    d7 = [r for r in allrows if r[0] == "2026-10-07"]
    stat["D07"] = {"rows": len(d7), "on_time": sum(r[-1] == "ON_TIME" for r in d7),
                   "rate": round(sum(r[-1] == "ON_TIME" for r in d7) / len(d7) * 100, 2),
                   "mean_min": round(float(np.mean([r[8] for r in d7])), 1),
                   "std_min": round(float(np.std([r[8] for r in d7], ddof=1)), 1)}
    stat["raw_issues"] = {"D05": "중복 행 10개", "D11": "weight_kg 단위 g", "D19": "delivery_min 결측 8칸"}
    ref_p = ROOT / "ref.json"
    ref = json.loads(ref_p.read_text(encoding="utf-8"))
    ref["general"] = stat
    ref_p.write_text(json.dumps(ref, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({k: v for k, v in stat.items() if k != "days"}, ensure_ascii=False))
    print(stat["days"])


if __name__ == "__main__":
    main()
