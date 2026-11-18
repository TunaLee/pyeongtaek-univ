"""Gross die · 수율 모델 — 다이 크기별 Gross die 와 예상 수율 → output/die_size_yield.csv

Gross die 는 두 가지로 구한다: ① 격자에 놓고 직접 세기 ② 근사식 π·d²/(4S) − π·d/√(2S)
수율 모델: Poisson Y = exp(−A·D0) · Negative binomial Y = (1 + A·D0/α)^−α
"""
import math

import pandas as pd

from common import OUT


def gross_die_count(d=300, edge=3, die=10):
    r = d / 2 - edge
    n = int(r // die) + 2
    return sum(all(((x + a) * die) ** 2 + ((y + b) * die) ** 2 <= r * r for a in (0, 1) for b in (0, 1))
               for x in range(-n, n) for y in range(-n, n))


def gross_die_formula(d=300, die=10):
    s = die * die
    return math.pi * d * d / (4 * s) - math.pi * d / math.sqrt(2 * s)


def poisson(area_cm2, d0):
    return math.exp(-area_cm2 * d0)


def negbin(area_cm2, d0, alpha=2.0):
    return (1 + area_cm2 * d0 / alpha) ** (-alpha)


if __name__ == "__main__":
    y = 0.9042                         # W07 수율
    d0 = -math.log(y) / 1.0            # 다이 10×10 mm = 1 cm²
    print(f"Gross die 직접 세기 {gross_die_count()} · 근사식 {gross_die_formula():.0f} · D0 {d0:.3f}/cm²")
    rows = []
    for s in (5, 8, 10, 12, 15, 20, 25):
        a = s * s / 100
        g = gross_die_count(die=s)
        rows.append({"die_mm": s, "gross_die": g, "formula": round(gross_die_formula(die=s)),
                     "yield_poisson": round(poisson(a, d0) * 100, 1), "yield_negbin": round(negbin(a, d0) * 100, 1),
                     "good_die_poisson": round(g * poisson(a, d0))})
    t = pd.DataFrame(rows)
    t.to_csv(OUT / "die_size_yield.csv", index=False)
    print(t.to_string(index=False))
