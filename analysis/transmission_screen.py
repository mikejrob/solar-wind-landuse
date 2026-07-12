#!/usr/bin/env python3
"""
Oahu ag-district land x distance-to-transmission screen.

Cross-tabulates State Ag District land by LSB productivity class (A-E) and
distance to the existing HECO transmission / sub-transmission network, and
identifies clusters of ag land far from the grid whose "unlock" would yield
the most solar-eligible acreage per km of new/upgraded corridor.

Line data (cached in data/gis/):
  - hifld_lines_oahu.geojson : HIFLD Open "US Electric Power Transmission
    Lines" (services2.arcgis.com/FiaPA4ga0iQKduv3), Oahu bbox, VOLTAGE /
    VOLT_CLASS fields, source dates 2017-2020. 91 features.
  - osm_power_oahu.json : OpenStreetMap power=line / minor_line ways,
    Overpass API, voltage tags. 87 ways.

Classification (cross-checked):
  - 138 kV: HIFLD VOLTAGE==138 or VOLT_CLASS=='100-161' (40 features,
    325 km). OSM 138kV-tagged ways sit at median 0 m from these -> the two
    sources agree; 138 kV coverage is reliable.
  - 46 kV / sub-transmission ("46kV+aux"): everything else in either source
    (HIFLD 'UNDER 100' + HIFLD unknown-voltage + OSM 46kV-tagged + OSM
    untagged power lines). IMPORTANT: both sources under-map the 46 kV
    system (~80-140 km mapped vs several hundred circuit-km in reality),
    so distances to "46kV+" are UPPER bounds and far-from-grid acreage is
    overstated at the 46 kV tier. 138 kV results are the solid ones.

Distance = parcel/polygon boundary distance (shapely distance; 0 if a line
crosses the polygon). CRS EPSG:26904, acres = m2/4046.8564224.

Outputs:
  data/oahu_land_transmission.csv          parcel-level (TMK-keyed)
  data/gis/oahu_class_by_band.csv          LSB class x distance band acres
  data/gis/oahu_unlock_clusters.csv        ranked far-cluster table
  analysis/figs/oahu_transmission_screen.png
"""

import json
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
from shapely import make_valid
from shapely.geometry import LineString
from shapely.ops import nearest_points, unary_union

PROJECT = Path("/Users/michaelroberts/Research/solar-wind-landuse")
DATA = PROJECT / "data"
GIS = DATA / "gis"
FIGS = PROJECT / "analysis" / "figs"
M2_PER_ACRE = 4046.8564224
CRS = "EPSG:26904"
BANDS = [(0, 1), (1, 3), (3, 5), (5, np.inf)]
BAND_LABELS = ["0-1km", "1-3km", "3-5km", ">5km"]


def band_label(km):
    for (lo, hi), lab in zip(BANDS, BAND_LABELS):
        if lo <= km < hi:
            return lab
    return BAND_LABELS[-1]


def load_lines():
    h = gpd.read_file(GIS / "hifld_lines_oahu.geojson").to_crs(CRS)
    h["kv"] = np.where((h.VOLTAGE == 138) | (h.VOLT_CLASS == "100-161"),
                       "138", "46plus")
    h["src"] = "HIFLD"
    d = json.load(open(GIS / "osm_power_oahu.json"))
    rows = []
    for w in d["elements"]:
        t = w["tags"]
        rows.append({"kv": {"138000": "138"}.get(t.get("voltage"), "46plus"),
                     "src": "OSM",
                     "geometry": LineString([(p["lon"], p["lat"])
                                             for p in w["geometry"]])})
    o = gpd.GeoDataFrame(rows, crs="EPSG:4326").to_crs(CRS)
    lines = pd.concat([h[["kv", "src", "geometry"]],
                       o[["kv", "src", "geometry"]]], ignore_index=True)
    lines = gpd.GeoDataFrame(lines, crs=CRS)
    lines.to_parquet(GIS / "oahu_lines_classified.parquet")
    return lines, h  # h kept for corridor naming (SUB_1/SUB_2)


def main():
    FIGS.mkdir(exist_ok=True)
    lines, hifld = load_lines()
    net138 = lines[lines.kv == "138"].union_all()
    net46 = lines.union_all()  # 46kV+ = everything mapped (138 included)
    print(f"138kV: {net138.length/1000:.0f} km | 46kV+ (incl 138): "
          f"{net46.length/1000:.0f} km (double-counts HIFLD/OSM overlap)")

    # ---- ag-district LSB polygons, Oahu
    lsb_ag = gpd.read_parquet(GIS / "lsb_ag.parquet")
    lsb_ag = lsb_ag[lsb_ag.island == "Oahu"].copy()
    lsb_ag["geometry"] = lsb_ag.geometry.apply(
        lambda g: make_valid(g) if not g.is_valid else g)

    # ---- class x band cross-tab (polygon-accurate, via buffer rings)
    rings = {}
    prev = None
    for (lo, hi), lab in zip(BANDS, BAND_LABELS):
        if np.isinf(hi):
            rings[lab] = None  # complement handled below
            continue
        buf = gpd.GeoSeries([net46], crs=CRS).buffer(hi * 1000).iloc[0]
        rings[lab] = buf if prev is None else buf.difference(prev)
        prev = buf
    out_rows = []
    covered = None
    for lab in BAND_LABELS:
        if rings[lab] is not None:
            piece = lsb_ag.geometry.intersection(rings[lab])
            covered = (rings[lab] if covered is None
                       else unary_union([covered, rings[lab]]))
        else:
            piece = lsb_ag.geometry.difference(covered)
        ac = piece.area / M2_PER_ACRE
        for cls, a in ac.groupby(lsb_ag["type"]).sum().items():
            out_rows.append({"band": lab, "lsb_class": cls,
                             "acres": round(a, 1)})
    xt = (pd.DataFrame(out_rows)
          .pivot(index="lsb_class", columns="band", values="acres")
          [BAND_LABELS].fillna(0))
    print("\nAg-district acres by LSB class x distance to 46kV+ network:")
    print(xt.round(0))

    # same cross-tab against 138 kV only
    rings138, prev, covered = {}, None, None
    for (lo, hi), lab in zip(BANDS, BAND_LABELS):
        if np.isinf(hi):
            rings138[lab] = None
            continue
        buf = gpd.GeoSeries([net138], crs=CRS).buffer(hi * 1000).iloc[0]
        rings138[lab] = buf if prev is None else buf.difference(prev)
        prev = buf
    rows138 = []
    for lab in BAND_LABELS:
        if rings138[lab] is not None:
            piece = lsb_ag.geometry.intersection(rings138[lab])
            covered = (rings138[lab] if covered is None
                       else unary_union([covered, rings138[lab]]))
        else:
            piece = lsb_ag.geometry.difference(covered)
        ac = piece.area / M2_PER_ACRE
        for cls, a in ac.groupby(lsb_ag["type"]).sum().items():
            rows138.append({"band": lab, "lsb_class": cls,
                            "acres": round(a, 1)})
    xt138 = (pd.DataFrame(rows138)
             .pivot(index="lsb_class", columns="band", values="acres")
             [BAND_LABELS].fillna(0))
    print("\n... x distance to 138kV network only:")
    print(xt138.round(0))
    xt_out = pd.concat({"46kVplus": xt, "138kV": xt138}, names=["network"])
    xt_out.to_csv(GIS / "oahu_class_by_band.csv")

    # ---- parcel-level distances
    bp = pd.read_csv(DATA / "cap_scenarios_by_parcel.csv",
                     dtype={"tmk": str})
    bp = bp[bp.island == "Oahu"].copy()
    parcels = gpd.read_parquet(GIS / "parcels_oahu.parquet").to_crs(CRS)
    parcels["tmk9txt"] = parcels["tmk9txt"].astype(str)
    pg = parcels[parcels.tmk9txt.isin(set(bp.tmk))]
    pg = pg.dissolve(by="tmk9txt")[["geometry"]]  # one geom per TMK
    pg["dist_46kv_km"] = pg.geometry.distance(net46) / 1000
    pg["dist_138kv_km"] = pg.geometry.distance(net138) / 1000
    bp = bp.merge(pg[["dist_46kv_km", "dist_138kv_km"]].round(3),
                  left_on="tmk", right_index=True, how="left")
    cols = ["tmk", "parcel_acres", "a_acres", "b_acres", "c_acres",
            "d_acres", "e_acres", "S0_current_10pct_20ac", "S3_20pct_nocap",
            "dist_46kv_km", "dist_138kv_km"]
    bp[cols].rename(columns={"S0_current_10pct_20ac": "s0_eligible_acres",
                             "S3_20pct_nocap": "s3_eligible_acres"}) \
        .to_csv(DATA / "oahu_land_transmission.csv", index=False)
    print(f"\nwrote {DATA/'oahu_land_transmission.csv'} ({len(bp)} parcels)")

    # ---- scenario-eligible acres by band (parcel min-distance assignment)
    bp["band_46"] = bp.dist_46kv_km.map(band_label)
    bp["band_138"] = bp.dist_138kv_km.map(band_label)
    elig = bp.groupby("band_46")[["S0_current_10pct_20ac",
                                  "S3_20pct_nocap"]].sum().round(0) \
        .reindex(BAND_LABELS).fillna(0)
    elig138 = bp.groupby("band_138")[["S0_current_10pct_20ac",
                                      "S3_20pct_nocap"]].sum().round(0) \
        .reindex(BAND_LABELS).fillna(0)
    elig_out = pd.concat({"46kVplus": elig.T, "138kV": elig138.T},
                         names=["network"])
    elig_out.to_csv(GIS / "oahu_eligible_by_band.csv")
    print("\nScenario-eligible acres by parcel distance band (46kV+):")
    print(elig)
    print("(parcel assigned to band of its minimum boundary distance;")
    print(" large parcels span bands - see caveats)")

    # ---- far clusters (>3 km from any 46kV+ line)
    far = lsb_ag.union_all().difference(
        gpd.GeoSeries([net46], crs=CRS).buffer(3000).iloc[0])
    comps = gpd.GeoDataFrame(geometry=list(getattr(far, "geoms", [far])),
                             crs=CRS)
    comps["acres"] = comps.area / M2_PER_ACRE
    comps = comps[comps.acres > 100].sort_values("acres", ascending=False)
    rows = []
    for i, r in comps.iterrows():
        piece = lsb_ag.geometry.intersection(r.geometry)
        ac = (piece.area / M2_PER_ACRE).groupby(lsb_ag["type"]).sum()
        p_far, p_line = nearest_points(r.geometry, net46)
        dx, dy = p_line.x - p_far.x, p_line.y - p_far.y
        bearing = (np.degrees(np.arctan2(dx, dy)) + 360) % 360
        compass = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"][
            int(((bearing + 22.5) % 360) // 45)]
        # new-ROW length needed to reach the cluster's nearest edge
        ext_km = r.geometry.distance(net46) / 1000
        # nearest HIFLD feature -> corridor name
        hd = hifld.geometry.distance(p_line)
        near = hifld.loc[hd.idxmin()]
        bc, de = ac.get("B", 0) + ac.get("C", 0), ac.get("D", 0) + ac.get("E", 0)
        rows.append({
            "cluster_acres": round(r.acres),
            "a_acres": round(ac.get("A", 0)), "bc_acres": round(bc),
            "de_acres": round(de),
            "mw_5ac": round((bc + de) / 5), "mw_7ac": round((bc + de) / 7),
            "ext_km_to_cluster_edge": round(ext_km, 1),
            "direction_to_corridor": compass,
            "nearest_corridor": (f"{near.SUB_1} - {near.SUB_2} "
                                 f"({'138kV' if near.kv=='138' else '46kV+'})"),
            "acres_per_km": round(r.acres / ext_km),
            "centroid_lon": round(gpd.GeoSeries([r.geometry.centroid],
                                  crs=CRS).to_crs(4326).iloc[0].x, 4),
            "centroid_lat": round(gpd.GeoSeries([r.geometry.centroid],
                                  crs=CRS).to_crs(4326).iloc[0].y, 4),
        })
    cl = pd.DataFrame(rows).sort_values("acres_per_km", ascending=False)
    cl.to_csv(GIS / "oahu_unlock_clusters.csv", index=False)
    print("\nFar (>3km from 46kV+) ag-land clusters, ranked by acres/km:")
    print(cl.to_string(index=False))

    comps.to_parquet(GIS / "oahu_far_clusters.parquet")
    make_figure(lines, lsb_ag, comps, cl)
    return lines, lsb_ag, comps, bp


# Colors: sequential single-hue green ramp for LSB class (A most productive =
# darkest); line/cluster accents #4a3aa7 / #2a78d6 / #d55181 validated
# (CVD deltaE >= 16.6, contrast >= 3:1 on light surface).
LSB_RAMP = {"A": "#00441b", "B": "#1a7a37", "C": "#58b368",
            "D": "#a8d9a8", "E": "#e3f2e3"}
C_138, C_46, C_CL = "#4a3aa7", "#2a78d6", "#d55181"


def make_figure(lines, lsb_ag, comps, cl):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch

    fig, ax = plt.subplots(figsize=(11, 9), dpi=160)
    ax.set_facecolor("#ffffff")

    # island silhouette from the full SLUD layer
    slud = gpd.read_parquet(GIS / "slud.parquet").to_crs(CRS)
    slud[slud.island == "Oahu"].plot(ax=ax, color="#f0efec",
                                     edgecolor="#d8d6d0", linewidth=0.4)
    for cls in "ABCDE":
        lsb_ag[lsb_ag["type"] == cls].plot(ax=ax, color=LSB_RAMP[cls],
                                           edgecolor="none")
    lines[lines.kv != "138"].plot(ax=ax, color=C_46, linewidth=1.0)
    lines[lines.kv == "138"].plot(ax=ax, color=C_138, linewidth=1.8)
    comps.plot(ax=ax, facecolor="none", edgecolor=C_CL, linewidth=1.6,
               hatch="///")
    # label the three largest clusters by acres
    top3 = comps.nlargest(3, "acres")
    for rank, (_, r) in enumerate(top3.iterrows(), 1):
        c = r.geometry.centroid
        ax.annotate(f"{rank}", (c.x, c.y), fontsize=13, fontweight="bold",
                    color="#0b0b0b", ha="center", va="center",
                    bbox=dict(boxstyle="circle,pad=0.25", fc="white",
                              ec=C_CL, lw=1.4))

    handles = ([Patch(fc=LSB_RAMP[c], label=f"LSB class {c}") for c in "ABCDE"]
               + [Line2D([], [], color=C_138, lw=1.8, label="138 kV line"),
                  Line2D([], [], color=C_46, lw=1.0,
                         label="46 kV / sub-transmission (mapped)"),
                  Patch(fc="none", ec=C_CL, hatch="///",
                        label="ag land >3 km from any line")])
    ax.legend(handles=handles, loc="lower left", fontsize=8.5, frameon=True,
              framealpha=0.95, edgecolor="#d8d6d0")
    ax.set_title("Oahu agricultural-district land by LSB soil class and "
                 "distance to transmission", fontsize=12, color="#0b0b0b")
    ax.text(0.01, 0.985,
            "Numbered circles: 3 largest far clusters (see "
            "oahu_unlock_clusters.csv).\nLines: HIFLD + OSM; 46 kV network "
            "under-mapped in public data.", transform=ax.transAxes,
            fontsize=8, color="#52514e", va="top")
    # simple scale bar (10 km), lower right to avoid the legend
    x0, y0 = ax.get_xlim()[1] - 15000, ax.get_ylim()[0] + 3500
    ax.plot([x0, x0 + 10000], [y0, y0], color="#0b0b0b", lw=2)
    ax.text(x0 + 5000, y0 + 700, "10 km", ha="center", fontsize=8,
            color="#0b0b0b")
    ax.set_axis_off()
    fig.tight_layout()
    out = FIGS / "oahu_transmission_screen.png"
    fig.savefig(out, bbox_inches="tight")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
