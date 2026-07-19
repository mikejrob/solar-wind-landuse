#!/usr/bin/env python3
"""Figures f_military_land.png and f_golf_courses.png (paper style)."""
from pathlib import Path
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

PROJECT = Path("/Users/michaelroberts/Research/solar-wind-landuse")
GIS = PROJECT / "data" / "gis"
MIL = GIS / "military"
FIGS = PROJECT / "analysis" / "figs" / "paper"
CRS = "EPSG:26904"

slud = gpd.read_parquet(GIS / "slud.parquet").to_crs(CRS)
oa = slud[slud.island == "Oahu"]
lines = gpd.read_parquet(GIS / "oahu_lines_classified.parquet")
C_138, C_46 = "#4a3aa7", "#a7a2d8"


def base_ax(title, sub):
    fig, ax = plt.subplots(figsize=(11, 9), dpi=160)
    fig.patch.set_facecolor("#fcfcfb"); ax.set_facecolor("#fcfcfb")
    oa.plot(ax=ax, color="#f0efec", edgecolor="#d8d6d0", linewidth=0.4)
    oa[oa.ludcode == "U"].plot(ax=ax, color="#e7e2da", edgecolor="none", alpha=0.8)
    oa[oa.ludcode == "A"].plot(ax=ax, color="#eef1e8", edgecolor="none", alpha=0.6)
    lines[lines.kv != "138"].plot(ax=ax, color=C_46, linewidth=0.8)
    lines[lines.kv == "138"].plot(ax=ax, color=C_138, linewidth=1.5)
    ax.set_title(title, fontsize=12, color="#0b0b0b")
    ax.text(0.01, 0.985, sub, transform=ax.transAxes, fontsize=7.5,
            color="#52514e", va="top")
    return fig, ax


def scalebar(ax):
    x0, y0 = ax.get_xlim()[1] - 15000, ax.get_ylim()[0] + 3500
    ax.plot([x0, x0 + 10000], [y0, y0], color="#0b0b0b", lw=2)
    ax.text(x0 + 5000, y0 + 700, "10 km", ha="center", fontsize=8, color="#0b0b0b")
    ax.set_axis_off()


# ================= MILITARY =================
def norm(t):
    if t is None or (isinstance(t, float) and np.isnan(t)):
        return ""
    t = str(t)
    if t in ("nan", "None"):
        return ""
    return t[:-2] if t.endswith(".0") else t

g = gpd.read_parquet(MIL / "oahu_military_screen.parquet")
g["tmk"] = g.tmk.map(norm)
csv = pd.read_csv(PROJECT / "data" / "oahu_military_land.csv")
csv["tmk"] = csv.tmk.map(norm)
g = g.merge(csv[["name", "tenure", "tmk", "viability_flag"]],
            on=["name", "tenure", "tmk"], how="left")

fig, ax = base_ax(
    "Oahu military land and utility-scale solar: tenure and constraint screen",
    "DoD land (ParcelsZoning layers 34/35). 'Fee/other' polygons are federal fee or ceded-land tenure (not deed-resolved).\n"
    "State land leased to the Army expiring 2029: per the Aug-2025 Army ROD, Kawailoa-Poamoho and Makua leases expire\n"
    "(return to State); ~450 ac at Kahuku retained. Constraint tiers are a screen-level reading of DoD rules, not DoD findings.")

EXCL = g[g.viability_flag.str.startswith("excluded", na=False)]
EUL = g[g.viability_flag == "plausibly_usable_eul"]
PREC = g[g.viability_flag == "precedent_built"]
LR = g[g.viability_flag == "retained_army_rod"]
LRET = g[g.tenure == "state_lease_2029"]
LRETURN = LRET[LRET.viability_flag != "retained_army_rod"]

EXCL.plot(ax=ax, facecolor="#d8d6d0", edgecolor="#9a978f", linewidth=0.4, hatch="///")
EUL.plot(ax=ax, facecolor="#7fa9dc", edgecolor="#4a7ab3", linewidth=0.5)
PREC.plot(ax=ax, facecolor="#1baf7a", edgecolor="#0d7a52", linewidth=1.0)
LRETURN.plot(ax=ax, facecolor="#f0b458", edgecolor="#b9822a", linewidth=0.8, hatch="..")
LR.plot(ax=ax, facecolor="none", edgecolor="#c0392b", linewidth=2.0)

for nm, txt, (dx, dy) in [
        ("West Loch Annex", "West Loch / Kupono\n(42 MW built, Navy EUL)", (7000, -8000)),
        ("Schofield Barracks", "Schofield (EUL\nprecedent: 50 MW biofuel)", (-30000, 6000)),
        ("Poamoho Training Area", "Kawailoa-Poamoho\n(lease expires 2029)", (9000, 6000)),
        ("Makua Military Reserve", "Makua (expires 2029;\nUXO, remote)", (-8000, 12000))]:
    r = g[g.name == nm]
    if len(r):
        c = r.geometry.iloc[0].centroid
        ax.annotate(txt, (c.x, c.y), xytext=(c.x + dx, c.y + dy), fontsize=8,
                    color="#0b0b0b", arrowprops=dict(arrowstyle="-", color="#52514e", lw=0.7))
r = g[g.tmk == "158002002"]
if len(r):
    c = r.geometry.iloc[0].centroid
    ax.annotate("Kahuku TA parcel\n(flat, grid-adjacent —\nArmy RETAINS)", (c.x, c.y),
                xytext=(c.x + 6000, c.y - 6000), fontsize=8, color="#c0392b",
                arrowprops=dict(arrowstyle="-", color="#c0392b", lw=0.8))

handles = [
    Patch(fc="#1baf7a", ec="#0d7a52", label="precedent-built solar (West Loch / Kupono, Navy EUL)"),
    Patch(fc="#7fa9dc", ec="#4a7ab3", label="fee land, EUL mechanically plausible (unproven at scale)"),
    Patch(fc="#d8d6d0", ec="#9a978f", hatch="///", label="excluded by DoD constraint (ordnance/ESQD, training/UXO,\nairfield/airspace, or developed/small)"),
    Patch(fc="#f0b458", ec="#b9822a", hatch="..", label="2029 state lease — returns to State (mostly steep/remote)"),
    Patch(fc="none", ec="#c0392b", lw=2, label="2029 state lease — Army retains (Kahuku ~450 ac)"),
    Patch(fc="#e7e2da", label="state Urban district"), Patch(fc="#eef1e8", label="state Ag district"),
    Line2D([], [], color=C_138, lw=1.5, label="138 kV line"),
    Line2D([], [], color=C_46, lw=0.8, label="46 kV+ (mapped)"),
]
ax.legend(handles=handles, loc="lower left", fontsize=7.3, frameon=True,
          framealpha=0.95, edgecolor="#d8d6d0", facecolor="#fcfcfb")
scalebar(ax)
fig.tight_layout()
fig.savefig(FIGS / "f_military_land.png", bbox_inches="tight", facecolor="#fcfcfb")
print("wrote f_military_land.png")

# ================= GOLF =================
gg = gpd.read_parquet(MIL / "oahu_golf_screen.parquet")
gc = pd.read_csv(PROJECT / "data" / "oahu_golf_courses.csv")
RENAME = {"__noname_221300526": "Barbers Point Golf Course",
          "__noname_8987946": "Mid-Pacific Country Club",
          "__noname_1094652470": "Olomana Golf Links"}
gg["name"] = gg.name.replace(RENAME)
gg = gg.merge(gc[["name", "status", "solar_side", "viability_flag", "acres"]],
              on="name", how="left")

fig, ax = base_ax(
    "Oahu golf courses: operating status and solar viability",
    "OSM golf polygons. Open courses are not available without closure. The two CLOSED courses are Ko'olau (windward/wet,\n"
    "Conservation-zoned, poor solar) and Makaha (leeward/sunny but in a housing-redevelopment pipeline and ~6.7 km from grid).\n"
    "Viable solar subset (closed + leeward + flat + near-grid + not housing/flood/military) = none.")

openc = gg[gg.status == "open"]
lee = openc[openc.solar_side == "leeward_sunny"]
wind = openc[openc.solar_side != "leeward_sunny"]
closed = gg[gg.status == "closed"]
wind.plot(ax=ax, facecolor="#cfd8e6", edgecolor="#9aa7bd", linewidth=0.4)
lee.plot(ax=ax, facecolor="#f4d9a0", edgecolor="#c9a24a", linewidth=0.4)
closed.plot(ax=ax, facecolor="#d55181", edgecolor="#8f2f53", linewidth=1.2, hatch="xx")

for nm, txt, (dx, dy), col in [
        ("Ko'olau Golf Club", "Ko'olau (CLOSED 2020,\nwindward, → conservation)", (10000, 4000), "#8f2f53"),
        ("Makaha Valley Country Club", "Makaha (CLOSED course,\n→ housing; grid-distant)", (5000, 7000), "#8f2f53")]:
    r = gg[gg.name == nm]
    if len(r):
        c = r.geometry.iloc[0].centroid
        ax.annotate(txt, (c.x, c.y), xytext=(c.x + dx, c.y + dy), fontsize=8.5,
                    color=col, arrowprops=dict(arrowstyle="-", color=col, lw=0.8))

handles = [
    Patch(fc="#f4d9a0", ec="#c9a24a", label="open, leeward/sunny (good solar — but operating)"),
    Patch(fc="#cfd8e6", ec="#9aa7bd", label="open, windward/marginal (poor solar)"),
    Patch(fc="#d55181", ec="#8f2f53", hatch="xx", label="CLOSED course"),
    Patch(fc="#e7e2da", label="state Urban district"), Patch(fc="#eef1e8", label="state Ag district"),
    Line2D([], [], color=C_138, lw=1.5, label="138 kV line"),
    Line2D([], [], color=C_46, lw=0.8, label="46 kV+ (mapped)"),
]
ax.legend(handles=handles, loc="lower left", fontsize=7.8, frameon=True,
          framealpha=0.95, edgecolor="#d8d6d0", facecolor="#fcfcfb")
scalebar(ax)
fig.tight_layout()
fig.savefig(FIGS / "f_golf_courses.png", bbox_inches="tight", facecolor="#fcfcfb")
print("wrote f_golf_courses.png")
