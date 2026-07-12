"""Expansion-frontier chart with approximate-cost vertical reference lines.
Cost assumption: 138 kV new build, Hawaii-adjusted central ~$2.5M/km (range
$1.5-4M/km per MISO benchmarks x island multiplier), WIRE ONLY - substation
and interconnection costs excluded. Redraws analysis/figs/paper/f_expansion_curve.png
from data/gis/expansion_curve.csv.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pathlib import Path

ROOT = Path("/Users/michaelroberts/Research/solar-wind-landuse")
SURF = "#fcfcfb"; INK = "#0b0b0b"; INK2 = "#52514e"; MUTED = "#898781"
GRID = "#e1e0d9"; BASE = "#c3c2b7"; BLUE = "#2a78d6"; AQUA = "#1baf7a"
PINK = "#d03b6f"; COST = "#8a8880"

COST_PER_KM_M = 2.5  # $M per km, central

d = pd.read_csv(ROOT / "data/gis/expansion_curve.csv")
plt.rcParams.update({"font.family": "sans-serif", "font.size": 11,
    "figure.facecolor": SURF, "axes.facecolor": SURF})

fig, ax = plt.subplots(figsize=(9.4, 5.6), dpi=200)
for s in ["top", "right"]: ax.spines[s].set_visible(False)
for s in ["left", "bottom"]: ax.spines[s].set_color(BASE)
ax.yaxis.grid(True, color=GRID, lw=0.8); ax.set_axisbelow(True)
ax.tick_params(colors=MUTED)

baseline = d["cum_acres_le30"].iloc[0]
ax.axhline(baseline, color=BASE, lw=1.1, ls=(0, (5, 4)))
ax.text(58, baseline - 900, f"baseline (mapped 46 kV+ network): {baseline:,.0f} ac",
        fontsize=9.5, color=INK2)

# cost verticals: $50M steps at $2.5M/km -> every 20 km
for cost_m in [50, 100, 150, 200, 250]:
    km = cost_m / COST_PER_KM_M
    if km > d["cum_km"].max() + 6: continue
    ax.axvline(km, color=COST, lw=0.9, ls=(0, (2, 3)), alpha=0.85, zorder=1)
    ax.text(km, ax.get_ylim()[1], "", fontsize=1)  # placeholder
ymax = 38500
ax.set_ylim(12000, ymax)
for cost_m in [50, 100, 150, 200, 250]:
    km = cost_m / COST_PER_KM_M
    if km > d["cum_km"].max() + 6: continue
    ax.text(km, ymax - 250, f"≈${cost_m}M", ha="center", va="top",
            fontsize=9.3, color=COST,
            bbox=dict(facecolor=SURF, edgecolor="none", pad=1.2))

ax.plot(d["cum_km"], d["cum_acres_le30"], color=BLUE, lw=2.4, zorder=4)
ax.plot(d["cum_km"], d["cum_acres_le15"], color=AQUA, lw=2.0, zorder=4)
ax.text(d["cum_km"].iloc[-1] + 1.5, d["cum_acres_le30"].iloc[-1], "slope ≤30%\n(headline)",
        color=BLUE, fontsize=10.5, fontweight="bold", va="center")
ax.text(d["cum_km"].iloc[-1] + 1.5, d["cum_acres_le15"].iloc[-1], "slope ≤15%",
        color="#128a60", fontsize=10.5, fontweight="bold", va="center")

# budget markers on the headline curve
for L in [10, 25, 50, 75, 100]:
    y = np.interp(L, d["cum_km"], d["cum_acres_le30"])
    ax.plot([L], [y], marker="o", ms=7, mfc=SURF, mec=BLUE, mew=1.6, zorder=5)
    ax.annotate(f"L={L}\n{y:,.0f} ac", (L, y), xytext=(6, -34),
                textcoords="offset points", fontsize=8.8, color=INK2)


ax.set_xlim(-2, 132)
ax.set_xlabel("km of new line (greedy build-out)", fontsize=10.5, color=INK2)
ax.set_ylabel("B–D ag-district acres within 1 km of a line", fontsize=10.5, color=INK2)
ax.set_title("Coverage of solar-eligible ag land vs new-line budget, Oʻahu",
             loc="left", fontsize=13, color=INK, fontweight="bold", pad=20)
fig.text(0.005, 0.03, "Vertical lines: approximate cumulative cost at ~\\$2.5M/km (138 kV new build, Hawaiʻi-adjusted central value; range \\$1.5–4M/km) — wire only,", fontsize=8, color=MUTED)
fig.text(0.005, 0.006, "excludes substations/interconnection. Greedy heuristic; geometric routes; mapped 46 kV network incomplete, so baseline is understated. Class A and E excluded.", fontsize=8, color=MUTED)
fig.tight_layout(rect=(0, 0.05, 1, 1))
fig.savefig(ROOT / "analysis/figs/paper/f_expansion_curve.png", facecolor=SURF)
print("wrote f_expansion_curve.png")
