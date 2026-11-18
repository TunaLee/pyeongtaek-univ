"""UCI SECOM (CC BY 4.0, https://archive.ics.uci.edu/dataset/179/secom) → labs/wafer-lab/data/secom/secom.csv

실행: python3 labs/make_secom.py   (_raw/secom/ 에 secom.data · secom_labels.data 를 먼저 받아 둔다)
열: timestamp · result(PASS/FAIL) · f000~f589 (공정 센서 값 · 이름은 원본에도 없음)
"""
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent
RAW = ROOT.parent / "_raw" / "secom"
OUT = ROOT / "wafer-lab" / "data" / "secom"

X = pd.read_csv(RAW / "secom.data", sep=" ", header=None)
L = pd.read_csv(RAW / "secom_labels.data", sep=" ", header=None, names=["label", "ts"])
X.columns = [f"f{i:03d}" for i in range(X.shape[1])]
df = pd.concat([pd.to_datetime(L.ts, format="%d/%m/%Y %H:%M:%S").rename("timestamp"),
                L.label.map({-1: "PASS", 1: "FAIL"}).rename("result"), X], axis=1)
OUT.mkdir(parents=True, exist_ok=True)
df.to_csv(OUT / "secom.csv", index=False)
miss = X.isna().mean()
st = {"rows": len(df), "features": X.shape[1], "fail": int((L.label == 1).sum()),
      "cells_missing_pct": round(float(X.isna().values.mean()) * 100, 2), "cols_any_missing": int((miss > 0).sum()),
      "cols_missing_over50": int((miss > .5).sum()), "cols_constant": int((X.nunique() <= 1).sum()),
      "start": str(df.timestamp.min()), "end": str(df.timestamp.max())}
ref_p = ROOT / "ref.json"
ref = json.loads(ref_p.read_text(encoding="utf-8"))
ref["secom"] = st
ref_p.write_text(json.dumps(ref, ensure_ascii=False, indent=1), encoding="utf-8")
print(st)
