"""Paper figures for the solar/wind land-use working paper.
Light surface, dataviz-reference palette. Soil-group identity is fixed across
figures: B/C (capped) = blue, D/E (open) = aqua, A (banned) = yellow.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pathlib import Path

ROOT = Path("/Users/michaelroberts/Research/solar-wind-landuse")
FIGS = ROOT / "analysis" / "figs" / "paper"
FIGS.mkdir(parents=True, exist_ok=True)

SURF = "#fcfcfb"; INK = "#0b0b0b"; INK2 = "#52514e"; MUTED = "#898781"
GRID = "#e1e0d9"; BASE = "#c3c2b7"
BLUE = "#2a78d6"; AQUA = "#1baf7a"; YELLOW = "#eda100"
SEQ = ["#86b6ef", "#5598e7", "#2a78d6", "#1c5cab", "#104281"]  # ordinal blue 250..650

plt.rcParams.update({
    "font.family": "sans-serif", "font.size": 11,
    "figure.facecolor": SURF, "axes.facecolor": SURF,
    "axes.edgecolor": BASE, "axes.labelcolor": INK2,
    "xtick.color": MUTED, "ytick.color": MUTED,
    "axes.grid": False, "svg.fonttype": "none",
})

def style(ax, xgrid=False, ygrid=False):
    for s in ["top", "right", "left"]:
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(BASE)
    if xgrid:
        ax.xaxis.grid(True, color=GRID, lw=0.8, zorder=0)
    if ygrid:
        ax.yaxis.grid(True, color=GRID, lw=0.8, zorder=0)
    ax.set_axisbelow(True)

# ---------------------------------------------------------------- F1 scenarios
res = pd.read_csv(ROOT / "data" / "cap_scenarios_results.csv")
oahu = res[res["island"].str.lower() == "oahu"].copy()
order = ["S0_current_10pct_20ac", "S1_10pct_nocap", "S2_20pct_20ac", "S3_20pct_nocap", "S4_all_bc"]
labels = {
    "S0_current_10pct_20ac": "S0  Current law\nmin(10%, 20 ac)",
    "S1_10pct_nocap": "S1  10%, no hard cap",
    "S2_20pct_20ac": "S2  min(20%, 20 ac)",
    "S3_20pct_nocap": "S3  20%, no hard cap",
    "S4_all_bc": "S4  No cap (all B/C)",
}
oahu = oahu.set_index("scenario").loc[[o for o in order if o in set(oahu["scenario"])]]
fig, ax = plt.subplots(figsize=(8.6, 4.4), dpi=200)
y = np.arange(len(oahu))[::-1]
bars = ax.barh(y, oahu["eligible_acres"], height=0.62, color=SEQ[: len(oahu)], zorder=3)
for yi, (idx, row) in zip(y, oahu.iterrows()):
    ax.text(row["eligible_acres"] + 300, yi,
            f"{row['eligible_acres']:,.0f} ac  ≈ {row['mw_at_5ac']:,.0f} MW",
            va="center", color=INK, fontsize=10.5,
            fontweight="bold" if idx in ("S0_current_10pct_20ac", "S3_20pct_nocap") else "normal")
ax.set_yticks(y); ax.set_yticklabels([labels[i] for i in oahu.index], fontsize=10, color=INK2)
ax.set_xlim(0, oahu["eligible_acres"].max() * 1.36)
ax.set_xlabel("Permitted-use-eligible acres on Oʻahu class B/C agricultural soils", fontsize=10)
style(ax, xgrid=True)
ax.set_title("Solar-eligible acreage on Oʻahu B/C agricultural soils under alternative cap rules",
             loc="left", fontsize=12.5, color=INK, fontweight="bold", pad=14)
fig.text(0.005, 0.012, "MW at 5 ac/MW. Source: LSB soils × State Land Use District × county parcels (analysis/cap_scenarios.py).",
         fontsize=8, color=MUTED)
fig.tight_layout(rect=(0, 0.045, 1, 1))
fig.savefig(FIGS / "f1_cap_scenarios.png", facecolor=SURF)
plt.close(fig)

# ------------------------------------------------------- F2 distance x class
byband = pd.read_csv(ROOT / "data" / "gis" / "oahu_class_by_band.csv")
b46 = byband[byband["network"] == "46kVplus"].set_index("lsb_class")
bands = ["0-1km", "1-3km", "3-5km", ">5km"]
groups = {
    "A (solar banned)": (["A"], YELLOW),
    "B/C (capped 10%/20 ac)": (["B", "C"], BLUE),
    "D/E (uncapped, no SUP)": (["D", "E"], AQUA),
}
fig, ax = plt.subplots(figsize=(8.6, 4.6), dpi=200)
x = np.arange(len(bands)); w = 0.26
for i, (name, (classes, color)) in enumerate(groups.items()):
    vals = [b46.loc[classes, band].sum() for band in bands]
    ax.bar(x + (i - 1) * (w + 0.02), vals, width=w, color=color, zorder=3, label=name)
    for xi, v in zip(x + (i - 1) * (w + 0.02), vals):
        ax.text(xi, v + 450, f"{v/1000:,.1f}k", ha="center", fontsize=9.3, color=INK)
ax.set_xticks(x)
ax.set_xticklabels([f"{b}" for b in bands], fontsize=10.5, color=INK2)
ax.set_xlabel("Distance to nearest mapped 46 kV+ line (46 kV network under-mapped → distances are upper bounds)",
              fontsize=9.5)
ax.set_ylabel("Acres (thousands)", fontsize=10)
ax.set_yticks([0, 10000, 20000, 30000, 40000])
ax.set_yticklabels(["0", "10k", "20k", "30k", "40k"])
style(ax, ygrid=True)
ax.legend(loc="upper right", frameon=False, fontsize=9.8, labelcolor=INK2)
ax.set_title("Oʻahu agricultural-district acreage by distance to mapped transmission",
             loc="left", fontsize=12.5, color=INK, fontweight="bold", pad=14)
fig.text(0.005, 0.012, "Oʻahu State Agricultural District, LSB soil classes. Sources: HIFLD + OSM lines (cross-validated), state GIS.",
         fontsize=8, color=MUTED)
fig.tight_layout(rect=(0, 0.045, 1, 1))
fig.savefig(FIGS / "f2_distance_bands.png", facecolor=SURF)
plt.close(fig)

# ------------------------------------------------------------- F3 ownership
m = pd.read_csv(ROOT / "data" / "oahu_owner_class_transmission.csv", dtype={"tmk": str})
m["bc"] = m["b_acres"] + m["c_acres"]; m["de"] = m["d_acres"] + m["e_acres"]
top = (m.groupby("owner_resolved")[["parcel_acres", "a_acres", "bc", "de"]].sum()
         .sort_values("parcel_acres", ascending=False).head(10))
short = {
    "State of Hawaii (agency unspecified)": "State of Hawaiʻi (other)",
    "United States of America": "United States (military etc.)",
    "Kamehameha Schools (B.P. Bishop Estate)": "Kamehameha Schools",
    "State of Hawaii - DLNR": "State — DLNR",
    "Property Reserve Inc (LDS Church real-estate arm)": "Property Reserve (LDS)",
    "City & County of Honolulu": "City & County of Honolulu",
    "Laukiha'a ag CPR (multiple unit owners; developed by Pomaika'i Partners LLC)": "Laukihaʻa ag CPR",
    "DHHL": "DHHL",
    "Dole Food Co Inc": "Dole Food Co",
    "Kualoa Ranch (Morgan family)": "Kualoa Ranch",
}
fig, ax = plt.subplots(figsize=(8.6, 5.0), dpi=200)
y = np.arange(len(top))[::-1]
left = np.zeros(len(top))
for col, color, name in [("a_acres", YELLOW, "A (banned)"), ("bc", BLUE, "B/C (capped)"), ("de", AQUA, "D/E (open)")]:
    vals = top[col].values
    ax.barh(y, vals, left=left, height=0.6, color=color, zorder=3, label=name,
            edgecolor=SURF, linewidth=2)
    left += vals
for yi, (name, row) in zip(y, top.iterrows()):
    ax.text(left[list(top.index).index(name)] + 400, yi, f"{row['parcel_acres']:,.0f} ac total",
            va="center", fontsize=9.5, color=INK2)
ax.set_yticks(y)
ax.set_yticklabels([short.get(i, i[:28]) for i in top.index], fontsize=10, color=INK2)
ax.set_xlim(0, top["parcel_acres"].max() * 1.22)
ax.set_xlabel("Oʻahu State Agricultural District acres (stacked by LSB soil group; remainder = unrated/water)", fontsize=9.5)
style(ax, xgrid=True)
ax.legend(loc="lower right", frameon=False, fontsize=9.8, labelcolor=INK2)
ax.set_title("Government owns half of Oʻahu's ag district;\nKamehameha Schools owns a quarter of what's private",
             loc="left", fontsize=12.5, color=INK, fontweight="bold", pad=14)
fig.text(0.005, 0.012, "Top 10 owners of 210,130 attributed acres (99% coverage). Source: Honolulu RPAD OWNALL bulk table, entity-resolved.",
         fontsize=8, color=MUTED)
fig.tight_layout(rect=(0, 0.045, 1, 1))
fig.savefig(FIGS / "f3_ownership.png", facecolor=SURF)
plt.close(fig)

print("wrote:", sorted(p.name for p in FIGS.glob("*.png")))
