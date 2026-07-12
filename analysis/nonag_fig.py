"""Step 9: recolored non-ag candidate map by economic viability class."""
from pathlib import Path
import geopandas as gpd
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from shapely.geometry import MultiPolygon, Polygon

SCRATCH = Path("/private/tmp/claude-503/-Users-michaelroberts-Research-solar-wind-landuse/d73405a1-d30d-4ac4-8a47-d64b30b982a9/scratchpad")
PROJECT = Path("/Users/michaelroberts/Research/solar-wind-landuse")
GIS = PROJECT / "data" / "gis"
CRS = "EPSG:26904"

def poly_only(g):
    if isinstance(g, (Polygon, MultiPolygon)):
        return g
    parts = [p for p in getattr(g, "geoms", []) if isinstance(p, Polygon)]
    return MultiPolygon(parts) if parts else Polygon()

cand = gpd.read_parquet(SCRATCH / "urban_candidates_enriched.parquet")
cand = cand.drop_duplicates(subset="tmk9txt").reset_index(drop=True)
cand["geometry"] = cand.geometry.apply(poly_only)
cls = pd.read_csv(SCRATCH / "class_by_tmk.csv", dtype={"tmk9txt": str})
cand = cand.merge(cls[["tmk9txt", "viability_class", "strict"]], on="tmk9txt")
cand["viability_class"] = cand.viability_class.fillna("")

dur = cand[cand.viability_class == "durable"]
unc = cand[cand.viability_class == "uncertain"]
hvd = cand[cand.viability_class == "higher_value_development"]
flat_excl = cand[~cand.military & (cand.acres_le15 >= 10) & ~cand.strict]
mil = cand[cand.military & (cand.acres_le15 >= 10)]
sites = gpd.read_parquet(SCRATCH / "osm_sites.parquet")
sites = sites[sites.acres >= 5]

slud = gpd.read_parquet(GIS / "slud.parquet").to_crs(CRS)
oa = slud[slud.island == "Oahu"]
lines = gpd.read_parquet(GIS / "oahu_lines_classified.parquet")

C_DUR, C_DUR_E = "#2a78d6", "#12457f"
C_UNC, C_UNC_E = "#7fa9dc", "#4a7ab3"
C_HVD, C_HVD_E = "#d7e6f7", "#6d9bd1"
C_SITE, C_SITE_E = "#1baf7a", "#0d7a52"
C_138, C_46 = "#4a3aa7", "#a7a2d8"

fig, ax = plt.subplots(figsize=(11, 9), dpi=160)
fig.patch.set_facecolor("#fcfcfb")
ax.set_facecolor("#fcfcfb")
oa.plot(ax=ax, color="#f0efec", edgecolor="#d8d6d0", linewidth=0.4)
oa[oa.ludcode == "U"].plot(ax=ax, color="#e7e2da", edgecolor="none", alpha=0.8)
lines[lines.kv != "138"].plot(ax=ax, color=C_46, linewidth=0.8)
lines[lines.kv == "138"].plot(ax=ax, color=C_138, linewidth=1.5)
mil.plot(ax=ax, facecolor="#d8d6d0", edgecolor="#9a978f", linewidth=0.5, hatch="///")
flat_excl.plot(ax=ax, facecolor="#dbdcd8", edgecolor="#bdbeb8", linewidth=0.3)
hvd.plot(ax=ax, facecolor=C_HVD, edgecolor=C_HVD_E, linewidth=0.5, hatch="\\\\\\")
unc.plot(ax=ax, facecolor=C_UNC, edgecolor=C_UNC_E, linewidth=0.4)
dur.plot(ax=ax, facecolor=C_DUR, edgecolor=C_DUR_E, linewidth=0.4)
sites.plot(ax=ax, facecolor=C_SITE, edgecolor=C_SITE_E, linewidth=1.2)

gd = cand.set_index("tmk9txt")
for tmk, txt, (dx, dy), col in [
        ("192050001", "Makaiwa Hills", (-7000, 9500), "#0b0b0b"),
        ("196005013", "Waiawa (KS)", (4000, 5000), "#0b0b0b"),
        ("191013032", "Kalaeloa", (-3000, -9500), "#0b0b0b"),
        ("191018054", "Ho'opili area", (7500, -5500), "#0b0b0b"),
        ("156003062", "Turtle Bay area", (14000, -4500), "#0b0b0b"),
        ("191016179", "UH West O'ahu", (10000, -10500), "#0b0b0b"),
]:
    if tmk in gd.index:
        c = gd.loc[tmk].geometry.centroid
        ax.annotate(txt, (c.x, c.y), xytext=(c.x + dx, c.y + dy),
                    fontsize=8.5, color=col,
                    arrowprops=dict(arrowstyle="-", color="#52514e", lw=0.7))
for osm, txt, (dx, dy) in [
        ("way/239954711", "Kapaa quarry", (5000, 2500)),
        ("way/396515036", "Halawa quarry", (2500, 9500)),
        ("way/267608678", "Makakilo quarry", (-20000, 9500)),
        ("way/446606190", "Waimanalo Gulch\nlandfill", (-20000, 2500)),
        ("way/1354424725", "Pacific Aggregate\n(Wahiawa)", (-19000, 1000))]:
    r = sites[sites.osm_id == osm]
    if len(r):
        c = r.geometry.iloc[0].centroid
        ax.annotate(txt, (c.x, c.y), xytext=(c.x + dx, c.y + dy),
                    fontsize=8.5, color="#0d7a52",
                    arrowprops=dict(arrowstyle="-", color="#52514e", lw=0.7))

handles = [
    Patch(fc=C_DUR, ec=C_DUR_E, label="durable candidate (public / quarry-landfill /\nprivate <\\$50k/ac, no pipeline)"),
    Patch(fc=C_UNC, ec=C_UNC_E, label="uncertain (private, \\$50k–\\$500k/ac)"),
    Patch(fc=C_HVD, ec=C_HVD_E, hatch="\\\\\\", label="higher-value development (entitled pipeline\nor ≥\\$500k/ac)"),
    Patch(fc=C_SITE, ec=C_SITE_E, label="landfill / quarry / brownfield (OSM)"),
    Patch(fc="#dbdcd8", ec="#bdbeb8", label="flat urban parcel, screened out\n(built-out / airport / harbor / golf)"),
    Patch(fc="#d8d6d0", ec="#9a978f", hatch="///", label="military parcel (noted, excluded)"),
    Patch(fc="#e7e2da", label="state Urban district"),
    Line2D([], [], color=C_138, lw=1.5, label="138 kV line"),
    Line2D([], [], color=C_46, lw=0.8, label="46 kV+ (mapped)"),
]
ax.legend(handles=handles, loc="lower left", fontsize=7.5, frameon=True,
          framealpha=0.95, edgecolor="#d8d6d0", facecolor="#fcfcfb")
ax.set_title("Oahu non-agricultural solar candidates by economic viability class",
             fontsize=12, color="#0b0b0b")
ax.text(0.01, 0.985,
        "Candidates: ≥10 parcel-acres at ≤15% slope in the state Urban district, low-improvement, non-military.\n"
        "Durable = public owner (assessed <\\$2M/ac), quarry/landfill/brownfield, or private land assessed <\\$50k/ac\n"
        "with no named development pipeline. Higher-value = entitled pipeline (Ho'opili, Makaiwa Hills, Hoakalei,\n"
        "Turtle Bay, Koa Ridge, Ko Olina) or assessed ≥\\$500k/ac. Uncertain = remainder. RPAD assessed values, 2026.",
        transform=ax.transAxes, fontsize=7.5, color="#52514e", va="top")
x0, y0 = ax.get_xlim()[1] - 15000, ax.get_ylim()[0] + 3500
ax.plot([x0, x0 + 10000], [y0, y0], color="#0b0b0b", lw=2)
ax.text(x0 + 5000, y0 + 700, "10 km", ha="center", fontsize=8, color="#0b0b0b")
ax.set_axis_off()
fig.tight_layout()
out = PROJECT / "analysis" / "figs" / "paper" / "f_nonag_map.png"
fig.savefig(out, bbox_inches="tight", facecolor="#fcfcfb")
print(f"wrote {out}")
