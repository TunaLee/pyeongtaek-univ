"""정제 · 검증 — 원시 CSV 한 장 → 정제본 + 검증 보고서.

사용: python scripts/clean.py data/raw/wafer_test_W11.csv
"""
import sys
from pathlib import Path

import pandas as pd

from common import OUT, rejudge


def clean(df):
    issues = []
    n0 = len(df)
    df = df.drop_duplicates(subset=["wafer_id", "die_x", "die_y"])
    if len(df) < n0:
        issues.append(f"중복 행 {n0 - len(df)}개 삭제 (같은 다이 좌표)")
    if df.vth_v.median() > 10:
        df = df.assign(vth_v=(df.vth_v / 1000).round(3))
        issues.append("vth_v 단위가 mV — 1000으로 나눠 V로 변환")
    na = df[["vth_v", "idsat_ma", "ioff_na", "rc_ohm", "ox_thk_nm"]].isna().sum()
    for c, k in na[na > 0].items():
        issues.append(f"{c} 결측 {k}칸 — 해당 다이는 재측정(RETEST)으로 분류")
    tester = df.pass_fail.copy()
    df = rejudge(df)
    diff = int((tester != df.pass_fail).sum())
    if diff:
        issues.append(f"테스터 판정과 다른 다이 {diff}개")
    return df, issues


def validate(df):
    """검증 규칙 — (규칙, 통과 여부)."""
    return [
        ("다이 수 616", len(df) == 616),
        ("다이 좌표 중복 없음", not df.duplicated(["die_x", "die_y"]).any()),
        ("vth_v 범위 0.2~0.8 V", df.vth_v.between(.2, .8).all()),
        ("zone 값은 center · mid · edge", set(df.zone) <= {"center", "mid", "edge"}),
        ("양품 + 불량 + 재측정 = 전체", df.pass_fail.isin(["PASS", "FAIL", "RETEST"]).all()),
    ]


def main(path):
    raw = pd.read_csv(path)
    df, issues = clean(raw)
    wid = df.wafer_id.iloc[0]
    (OUT / "clean").mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT / "clean" / f"{wid}.csv", index=False)
    rules = validate(df)
    y = (df.pass_fail == "PASS").mean() * 100
    lines = [f"# 검증 보고서 · {wid}", "", f"- 원시 {len(raw)}행 → 정제 {len(df)}행 · 수율 {y:.2f}%", "", "## 발견한 문제"]
    lines += [f"- {x}" for x in issues] or ["- 없음"]
    lines += ["", "## 검증 규칙"] + [f"- [{'x' if ok else ' '}] {r}" for r, ok in rules]
    (OUT / f"qc_{wid}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    assert all(ok for _, ok in rules), "검증 실패"


if __name__ == "__main__":
    main(Path(sys.argv[1]))
