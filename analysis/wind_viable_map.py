#!/usr/bin/env python3
"""
Publication map: Oahu land where large wind (>= 100 kW) remains geometrically
permitted under Honolulu Ordinance 25-2 (effective Jan 2025).

Rule mapped (verified in notes/wind-setbacks.md):
  - Large wind is a permitted/conditional use ONLY in AG-1, AG-2 and Country
    zoning districts; AND
  - must sit >= max(10x tip height, 1.25 mi) from the property line of ANY
    zoning lot in the country, residential, apartment, apartment mixed-use,
    or resort districts. We map the 1.25-mi (2,011.68 m) flat floor: modern
    tip heights ~200 m make 10x = 2,000 m ~= the same.
  - The additional 1x-tip-height setback from ALL property lines is
    second-order at this scale and is ignored.

Because Country (C) is itself a protected district, all C-zoned land lies
within 1.25 mi of a C lot line, so the viable area is a subset of AG-1/AG-2.

Viable area is split by slope using data/gis/dem/oahu_slope_bands.tif
(10 m; band codes 1..7 = 0-5,5-10,10-15,15-20,20-25,25-30,>30 pct):
<= 30 pct (bands 1-6) vs > 30 pct (band 7, steep - ridge access only).

Inputs (cached): data/gis/pages_zoning_oahu/ (Honolulu LUO zoning),
data/gis/slud.parquet (island silhouette), data/gis/oahu_lines_classified
.parquet (HIFLD+OSM 138/46kV lines), slope raster above,
data/gis/osm_wind_turbines_oahu.json (OSM Overpass, power=generator +
generator:source=wind; fetched 2026-07; 50 turbines). CRS EPSG:26904.

Outputs:
  analysis/figs/paper/f_wind_map.png
  data/gis/wind_viable_areas.csv   (summary + named-region rows)
  data/gis/osm_wind_turbines_oahu.csv  (per-turbine location conformity)

Geometric screen only: no FAA/radar, noise-at-receptor, habitat, or
cultural screens; zoning layer as cached from the C&C Honolulu open-data
LUO layer (2024/25 vintage).
"""

import json
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
from rasterio import features
from scipy import ndimage
from shapely import make_valid

PROJECT = Path("/Users/michaelroberts/Research/solar-wind-landuse")
GIS = PROJECT / "data" / "gis"
FIGS = PROJECT / "analysis" / "figs" / "paper"
M2_PER_ACRE = 4046.8564224
CELL_AC = 100.0 / M2_PER_ACRE          # 10 m cell
CRS = "EPSG:26904"
MILE = 1609.344
SETBACK = 1.25 * MILE                  # 2,011.68 m flat floor

TARGET = {"AG-1", "AG-2", "C"}
SENSITIVE = {"C", "Resort", "Apart", "ApartMix", "ResMix",
             "A-1", "A-2", "A-3", "AMX-1", "AMX-2", "AMX-3",
             "R-3.5", "R-5", "R-7.5", "R-10", "R-20"}

# existing farms: label anchors (lon, lat); turbine points come from OSM.
# OSM manufacturer tag identifies the farm: Vestas 3.45 MW = Na Pua Makani
# (8), Clipper 2.5 MW = Kahuku Wind 2011 (12), Siemens 2.3 MW = Kawailoa (30).
WIND_FARMS = [
    ("Na Pua Makani", -157.943, 21.674),
    ("Kahuku Wind (2011)", -157.956, 21.683),
    ("Kawailoa Wind", -158.041, 21.611),
]
FARM_BY_MANUFACTURER = {"Vestas": "Na Pua Makani",
                        "Clipper": "Kahuku Wind (2011)",
                        "Siemens": "Kawailoa Wind"}

# locality anchors (lon, lat) for naming viable-area components
ANCHORS = {
    "Kaena Point": (-158.24, 21.57), "Mokuleia": (-158.17, 21.575),
    "Waianae Range mauka": (-158.155, 21.50), "Lualualei": (-158.145, 21.43),
    "Nanakuli": (-158.13, 21.40), "Waialua": (-158.07, 21.57),
    "Kahuku": (-157.96, 21.68), "Laie/Malaekahana": (-157.935, 21.635),
    "Hauula/Punaluu": (-157.90, 21.58), "Kaaawa/Kualoa": (-157.85, 21.54),
    "Waiahole/Waikane": (-157.86, 21.49), "Kahaluu/Kaneohe": (-157.84, 21.44),
    "Waimanalo": (-157.72, 21.34), "Ewa/Kalaeloa": (-158.06, 21.33),
    "Kunia": (-158.05, 21.42), "Schofield/Wahiawa": (-158.03, 21.49),
    "Helemano/Poamoho": (-157.99, 21.53), "Pupukea/Waimea": (-158.05, 21.63),
    "Kawailoa": (-158.04, 21.60), "Waipio/Waiawa": (-157.99, 21.42),
}

C_LE30, C_GT30 = "#b35b17", "#e88a3c"   # viable, two slope tones
C_AG, C_ISL = "#e2efe2", "#f0efec"      # background washes
C_138, C_46 = "#4a3aa7", "#2a78d6"      # transmission (family colors)
PAPER = "#fcfcfb"


def locality(lon, lat):
    return min(ANCHORS, key=lambda k: (ANCHORS[k][0] - lon) ** 2
               + (ANCHORS[k][1] - lat) ** 2)


def load_turbines(target_u, sens_u, viable):
    """OSM turbine points classified against the Ord 25-2 geometry.

    conforming_location = >= 1.25 mi from every protected-district lot AND
    inside AG-1/AG-2/Country zoning (i.e., inside the mapped viable area).
    Location only: the repowering clamp (<= 7% height increase / 575 ft,
    within current PPA) applies to ALL existing turbines regardless.
    """
    d = json.load(open(GIS / "osm_wind_turbines_oahu.json"))
    rows = []
    for e in d["elements"]:
        t = e.get("tags", {})
        rows.append({"osm_id": e["id"], "osm_type": e["type"],
                     "farm": FARM_BY_MANUFACTURER.get(
                         t.get("manufacturer", ""), "unknown"),
                     "manufacturer": t.get("manufacturer", ""),
                     "output": t.get("generator:output:electricity", ""),
                     "lon": e.get("lon") or e["center"]["lon"],
                     "lat": e.get("lat") or e["center"]["lat"]})
    tb = gpd.GeoDataFrame(
        pd.DataFrame(rows),
        geometry=gpd.points_from_xy([r["lon"] for r in rows],
                                    [r["lat"] for r in rows]),
        crs=4326).to_crs(CRS)
    tb["dist_sens_mi"] = tb.geometry.apply(
        lambda p: p.distance(sens_u)) / MILE
    tb["beyond_setback"] = tb["dist_sens_mi"] >= 1.25
    tb["in_target_zone"] = tb.geometry.apply(target_u.contains)
    tb["conforming_location"] = tb.geometry.apply(viable.contains)
    summ = tb.groupby("farm").agg(
        n=("osm_id", "size"), beyond_setback=("beyond_setback", "sum"),
        conforming_location=("conforming_location", "sum"),
        min_dist_mi=("dist_sens_mi", "min"),
        max_dist_mi=("dist_sens_mi", "max"))
    print(summ.round(2).to_string())
    tb.drop(columns="geometry").round(
        {"dist_sens_mi": 3}).to_csv(
        GIS / "osm_wind_turbines_oahu.csv", index=False)
    print(f"wrote {GIS / 'osm_wind_turbines_oahu.csv'}")
    return tb


def main():
    # ---- zoning geometry
    pages = sorted((GIS / "pages_zoning_oahu").glob("page_*.geojson"))
    z = gpd.GeoDataFrame(
        pd.concat([gpd.read_file(p) for p in pages], ignore_index=True),
        crs="EPSG:4326").to_crs(CRS)
    z["geometry"] = z.geometry.apply(
        lambda g: make_valid(g) if g is not None and not g.is_valid else g)
    z = z[z.geometry.notna() & ~z.geometry.is_empty]

    target_u = z[z.zone_class.isin(TARGET)].union_all()
    sens_u = z[z.zone_class.isin(SENSITIVE)].union_all()
    viable = target_u.difference(sens_u.buffer(SETBACK))
    viable_old = target_u.difference(sens_u.buffer(200.0))  # pre-2025 approx

    agc_ac = target_u.area / M2_PER_ACRE
    viable_ac = viable.area / M2_PER_ACRE
    old_ac = viable_old.area / M2_PER_ACRE
    print(f"AG/Country total: {agc_ac:,.0f} ac")
    print(f"Ord 25-2 viable:  {viable_ac:,.0f} ac ({viable_ac/agc_ac:.1%})")
    print(f"pre-2025 approx:  {old_ac:,.0f} ac ({old_ac/agc_ac:.1%})")

    # ---- slope split on the 10 m grid
    with rasterio.open(GIS / "dem" / "oahu_slope_bands.tif") as src:
        band = src.read(1)
        tr = src.transform
        bounds = src.bounds
    shape = band.shape
    vr = features.rasterize([(viable, 1)], out_shape=shape, transform=tr,
                            fill=0, dtype="uint8").astype(bool)
    le30 = vr & (band >= 1) & (band <= 6)
    gt30 = vr & (band == 7)
    le30_ac = le30.sum() * CELL_AC
    gt30_ac = gt30.sum() * CELL_AC
    print(f"viable <=30% slope: {le30_ac:,.0f} ac | >30%: {gt30_ac:,.0f} ac "
          f"(raster cell count; vector total {viable_ac:,.0f} ac)")

    # ---- named regions (8-connected components of the viable mask)
    lab, nlab = ndimage.label(vr, structure=np.ones((3, 3)))
    sizes = np.bincount(lab.ravel())
    steep = np.bincount(lab.ravel(), weights=gt30.ravel().astype(float))
    keep = [i for i in range(1, nlab + 1) if sizes[i] * CELL_AC >= 100]
    cy, cx = zip(*ndimage.center_of_mass(vr, lab, keep))
    xs, ys = rasterio.transform.xy(tr, cy, cx)
    ll = gpd.GeoSeries(gpd.points_from_xy(xs, ys), crs=CRS).to_crs(4326)
    rows = []
    for i, idx in enumerate(keep):
        tot = sizes[idx] * CELL_AC
        gt = steep[idx] * CELL_AC
        rows.append({"row_type": "region",
                     "name": locality(ll.iloc[i].x, ll.iloc[i].y),
                     "viable_acres": tot, "viable_le30_acres": tot - gt,
                     "viable_gt30_acres": gt,
                     "centroid_lon": round(ll.iloc[i].x, 4),
                     "centroid_lat": round(ll.iloc[i].y, 4)})
    reg = (pd.DataFrame(rows)
           .groupby(["row_type", "name"], as_index=False)
           .agg({"viable_acres": "sum", "viable_le30_acres": "sum",
                 "viable_gt30_acres": "sum",
                 "centroid_lon": "first", "centroid_lat": "first"})
           .sort_values("viable_acres", ascending=False))
    reg[["viable_acres", "viable_le30_acres", "viable_gt30_acres"]] = \
        reg[["viable_acres", "viable_le30_acres", "viable_gt30_acres"]].round()
    print(reg.to_string(index=False))

    summ = pd.DataFrame([
        {"row_type": "summary", "name": "agc_zoned_total",
         "viable_acres": round(agc_ac),
         "notes": "AG-1 + AG-2 + Country zoned land, Oahu LUO layer"},
        {"row_type": "summary", "name": "ord25_2_viable_total",
         "viable_acres": round(viable_ac),
         "viable_le30_acres": round(le30_ac),
         "viable_gt30_acres": round(gt30_ac),
         "notes": (f"1.25-mi buffer around country/res/apt/apt-MU/resort "
                   f"lots; {viable_ac/agc_ac:.1%} of AG/Country; slope split "
                   f"from 10 m raster cell counts")},
        {"row_type": "summary", "name": "pre2025_200m_viable_total",
         "viable_acres": round(old_ac),
         "notes": (f"~1x tip height (200 m) from same sensitive set, "
                   f"upper-bound-flavored approximation; "
                   f"{old_ac/agc_ac:.1%} of AG/Country")},
    ])
    out = pd.concat([summ, reg], ignore_index=True)
    out.to_csv(GIS / "wind_viable_areas.csv", index=False)
    print(f"wrote {GIS / 'wind_viable_areas.csv'}")

    tb = load_turbines(target_u, sens_u, viable)

    make_figure(z, target_u, le30, gt30, bounds, viable_ac, le30_ac, gt30_ac,
                agc_ac, old_ac, tb)


def make_figure(z, target_u, le30, gt30, bounds, viable_ac, le30_ac, gt30_ac,
                agc_ac, old_ac, tb):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.colors import to_rgba
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch

    fig, ax = plt.subplots(figsize=(11, 8.5), dpi=160)
    fig.patch.set_facecolor(PAPER)
    ax.set_facecolor(PAPER)

    slud = gpd.read_parquet(GIS / "slud.parquet").to_crs(CRS)
    slud[slud.island == "Oahu"].plot(ax=ax, color=C_ISL,
                                     edgecolor="#d8d6d0", linewidth=0.4)
    gpd.GeoSeries([target_u], crs=CRS).plot(ax=ax, color=C_AG,
                                            edgecolor="none")

    # viable area from the 10 m raster (half-res RGBA overlay for memory)
    idx = (le30.astype(np.uint8) * 2 + gt30.astype(np.uint8))[::2, ::2]
    lut = np.zeros((3, 4), dtype=np.uint8)
    lut[1] = (np.array(to_rgba(C_GT30)) * 255).astype(np.uint8)
    lut[2] = (np.array(to_rgba(C_LE30)) * 255).astype(np.uint8)
    ax.imshow(lut[idx], extent=(bounds.left, bounds.right,
                                bounds.bottom, bounds.top),
              origin="upper", interpolation="nearest", zorder=3)

    lines = gpd.read_parquet(GIS / "oahu_lines_classified.parquet")
    lines[lines.kv != "138"].plot(ax=ax, color=C_46, linewidth=0.6, zorder=4)
    lines[lines.kv == "138"].plot(ax=ax, color=C_138, linewidth=1.2, zorder=4)

    # existing turbines (OSM points), colored by location conformity
    non = tb[~tb.conforming_location]
    con = tb[tb.conforming_location]
    ax.scatter(non.geometry.x, non.geometry.y, marker="o", s=22,
               facecolor="#0b0b0b", edgecolor="white", linewidth=0.7,
               zorder=6)
    ax.scatter(con.geometry.x, con.geometry.y, marker="o", s=22,
               facecolor="white", edgecolor="#0b0b0b", linewidth=0.9,
               zorder=6)
    wf = gpd.GeoSeries(gpd.points_from_xy(
        [lon for _, lon, _ in WIND_FARMS],
        [lat for _, _, lat in WIND_FARMS]), crs=4326).to_crs(CRS)
    lab_off = {"Na Pua Makani": (8500, -1200), "Kahuku Wind (2011)":
               (-8500, 2600), "Kawailoa Wind": (-11500, 2200)}
    for (name, _, _), x, y in zip(WIND_FARMS, wf.x, wf.y):
        dx, dy = lab_off[name]
        ax.annotate(name, (x + dx, y + dy), fontsize=7.5, color="#0b0b0b",
                    ha="center", va="center", zorder=6)

    handles = [
        Patch(fc=C_LE30, label=f"wind-viable, slope <=30%  "
                               f"({le30_ac:,.0f} ac)"),
        Patch(fc=C_GT30, label=f"wind-viable, slope >30% -- steep, "
                               f"ridge-access only  ({gt30_ac:,.0f} ac)"),
        Patch(fc=C_AG, label="AG-1/AG-2/Country zoning, inside the "
                             "1.25-mi exclusion"),
        Line2D([], [], color=C_138, lw=1.2, label="138 kV"),
        Line2D([], [], color=C_46, lw=0.6, label="46 kV+ (mapped)"),
        Line2D([], [], marker="o", markersize=6, mfc="#0b0b0b", mec="white",
               lw=0, label=f"existing turbine, nonconforming location "
                           f"(n={len(non)})"),
        Line2D([], [], marker="o", markersize=6, mfc="white", mec="#0b0b0b",
               lw=0, label=f"existing turbine, conforming location "
                           f"(n={len(con)}; repowering still capped at "
                           f"+7% height)"),
    ]
    ax.legend(handles=handles, loc="lower left", fontsize=8, frameon=True,
              framealpha=0.95, edgecolor="#d8d6d0", facecolor=PAPER)

    ax.set_title("Oahu land where large wind (>=100 kW) remains geometrically"
                 " permitted under Ordinance 25-2 (Jan 2025)",
                 fontsize=11.5, color="#0b0b0b")
    ax.text(0.985, 0.975,
            f"Ord 25-2 (>= 1.25 mi from any country/residential/apartment/"
            f"resort lot line,\nAG-1/AG-2/Country districts only): "
            f"{viable_ac:,.0f} ac viable = {viable_ac/agc_ac:.0%} of "
            f"AG/Country land,\nof which {le30_ac:,.0f} ac at <=30% slope. "
            f"Pre-2025 (~1x tip height ~ 200 m):\n{old_ac/agc_ac:.0%} was "
            f"geometrically available ({old_ac:,.0f} ac).",
            transform=ax.transAxes, fontsize=8.5, color="#0b0b0b",
            ha="right", va="top",
            bbox=dict(boxstyle="round,pad=0.45", fc=PAPER, ec="#d8d6d0"))
    ax.text(0.5, -0.012,
            "Geometric screen only: no FAA/radar, noise-at-receptor, habitat,"
            " or cultural screens. Zoning: C&C Honolulu open-data LUO layer"
            " (2024/25 vintage);\n1.25-mi flat floor assumed to bind (10x tip"
            " height ~= 2,000 m for ~200 m tips). Slope: USGS 10 m DEM."
            " Lines: HIFLD + OSM; 46 kV network under-mapped."
            " Turbine points: OpenStreetMap (2026-07).",
            transform=ax.transAxes, fontsize=7, color="#52514e",
            ha="center", va="top")
    # 10 km scale bar, lower right above footnote
    x0 = ax.get_xlim()[1] - 14000
    y0 = ax.get_ylim()[0] + 6000
    ax.plot([x0, x0 + 10000], [y0, y0], color="#0b0b0b", lw=2)
    ax.text(x0 + 5000, y0 + 700, "10 km", ha="center", fontsize=8,
            color="#0b0b0b")
    ax.set_axis_off()
    fig.tight_layout()
    FIGS.mkdir(parents=True, exist_ok=True)
    out = FIGS / "f_wind_map.png"
    fig.savefig(out, bbox_inches="tight", facecolor=PAPER)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
