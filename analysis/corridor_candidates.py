#!/usr/bin/env python3
"""
Strategic transmission "unlock" analysis for Oahu ag land.

Question: where would new/upgraded transmission most increase access AND
competition? Buildable (slope-screened) ag-district land more than 1 km
from any mapped 46 kV+ line is clustered; each cluster is scored on
buildable acres per km of new ROW and on distinct-owners-unlocked per km
(corridors unlocking many owners' land increase PPA-bid competition more
than corridors serving a single estate).

Inputs (all cached by earlier scripts):
  data/gis/dem/oahu_slope_bands.tif   10 m slope-band raster (EPSG:26904)
  data/gis/lsb_ag.parquet             LSB x Ag District polygons
  data/gis/oahu_lines_classified.parquet  HIFLD+OSM lines (kv: 138/46plus)
  data/gis/parcels_oahu.parquet       TMK parcels
  data/oahu_land_transmission.csv     ag-parcel list (TMK-keyed)
  data/oahu_ag_owners.csv             resolved owners (TMK-keyed)

Buildable = percent slope <= 30 (headline; <=15 also reported).
Clusters = 8-connected components of (ag-district & >1 km from 46 kV+)
on the 10 m grid, reported if buildable_le30 >= 250 ac.

Outputs:
  data/gis/oahu_corridor_candidates.csv
  data/gis/oahu_ring_1_3km_summary.csv   (the "cheap upgrades" ring)
  analysis/figs/paper/f_corridors.png
"""

from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
from rasterio import features
from scipy import ndimage
from shapely.geometry import shape as shp_shape
from shapely.ops import nearest_points

PROJECT = Path("/Users/michaelroberts/Research/solar-wind-landuse")
DATA, GIS = PROJECT / "data", PROJECT / "data" / "gis"
FIGS = PROJECT / "analysis" / "figs"
CRS = "EPSG:26904"
CELL_AC = 100.0 / 4046.8564224
CLS_CODE = {c: i + 1 for i, c in enumerate("ABCDE")}
MIN_BUILDABLE_AC = 250.0
COMPASS = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]


def rasterize(geoms, values, shape, transform, dtype="uint32"):
    return features.rasterize(list(zip(geoms, values)), out_shape=shape,
                              transform=transform, fill=0, dtype=dtype)


def bearing_to(g, net):
    p_from, p_to = nearest_points(g, net)
    br = (np.degrees(np.arctan2(p_to.x - p_from.x, p_to.y - p_from.y))
          + 360) % 360
    return COMPASS[int(((br + 22.5) % 360) // 45)], p_from, p_to


def main():
    with rasterio.open(GIS / "dem" / "oahu_slope_bands.tif") as src:
        band = src.read(1)
        tr = src.transform
    shape = band.shape

    lsb_ag = gpd.read_parquet(GIS / "lsb_ag.parquet")
    lsb_ag = lsb_ag[lsb_ag.island == "Oahu"]
    cls = rasterize(lsb_ag.geometry, lsb_ag["type"].map(CLS_CODE),
                    shape, tr, "uint8")

    lines = gpd.read_parquet(GIS / "oahu_lines_classified.parquet")
    net46 = lines.union_all()
    net138 = lines[lines.kv == "138"].union_all()
    buf1 = rasterize([net46.buffer(1000)], [1], shape, tr, "uint8") == 1
    buf3 = rasterize([net46.buffer(3000)], [1], shape, tr, "uint8") == 1

    # distance-to-network rasters (meters), for MEAN new-ROW per cluster:
    # a spur to the cluster edge does not serve its far side, so the mean
    # buildable-cell distance is the ranking denominator; the edge (min)
    # distance is also reported.
    line46 = rasterize([net46.buffer(15)], [1], shape, tr, "uint8") == 1
    line138 = rasterize([net138.buffer(15)], [1], shape, tr, "uint8") == 1
    dist46 = ndimage.distance_transform_edt(~line46, sampling=10.0) \
        .astype(np.float32)
    dist138 = ndimage.distance_transform_edt(~line138, sampling=10.0) \
        .astype(np.float32)

    # parcels + owners
    pt = pd.read_csv(DATA / "oahu_land_transmission.csv", dtype={"tmk": str})
    own = pd.read_csv(DATA / "oahu_ag_owners.csv", dtype={"tmk": str})
    parcels = gpd.read_parquet(GIS / "parcels_oahu.parquet").to_crs(CRS)
    parcels["tmk9txt"] = parcels.tmk9txt.astype(str)
    pg = (parcels[parcels.tmk9txt.isin(set(pt.tmk))]
          .dissolve(by="tmk9txt")[["geometry"]].reset_index())
    pid = rasterize(pg.geometry, pg.index + 1, shape, tr, "uint32")
    tmk_of = pg.tmk9txt.values  # index i -> tmk of pid i+1
    own_map = own.set_index("tmk")[["owner_resolved", "owner_type"]]

    # ---- clusters: ag-district land >1 km from any mapped 46kV+ line
    far = (cls > 0) & (band > 0) & ~buf1
    lab, nlab = ndimage.label(far, structure=np.ones((3, 3)))
    print(f"{nlab} raw components")

    m = lab > 0
    cells = pd.DataFrame({
        "lab": lab[m], "cls": cls[m], "band": band[m], "pid": pid[m],
        "d46": dist46[m], "d138": dist138[m]})
    cells["le15"] = cells.band <= 3
    cells["le30"] = cells.band <= 6

    g = cells.groupby("lab")
    tab = pd.DataFrame({
        "total_ac": g.size() * CELL_AC,
        "buildable_ac_le15": g.le15.sum() * CELL_AC,
        "buildable_ac_le30": g.le30.sum() * CELL_AC,
    })
    b30 = cells[cells.le30]
    tab["de_ac_le30"] = (b30[b30.cls.isin([4, 5])].groupby("lab").size()
                         * CELL_AC)
    tab["bc_ac_le30"] = (b30[b30.cls.isin([2, 3])].groupby("lab").size()
                         * CELL_AC)
    tab["mean_km46"] = b30.groupby("lab").d46.mean() / 1000
    tab["mean_km138"] = b30.groupby("lab").d138.mean() / 1000
    tab = tab.fillna(0.0)
    keep = tab[tab.buildable_ac_le30 >= MIN_BUILDABLE_AC] \
        .sort_values("buildable_ac_le30", ascending=False)
    print(f"{len(keep)} clusters with >= {MIN_BUILDABLE_AC} buildable ac")

    # vectorize kept clusters for distance/bearing/figure
    keep_ids = set(keep.index)
    mask = np.isin(lab, list(keep_ids))
    geoms = {}
    for geom, val in features.shapes(lab.astype(np.int32), mask=mask,
                                     transform=tr):
        v = int(val)
        geoms.setdefault(v, []).append(shp_shape(geom))
    from shapely.ops import unary_union
    geoms = {v: unary_union(gl) for v, gl in geoms.items()}

    # owners per cluster (buildable_le30 acres by resolved owner)
    ob = b30[b30.pid > 0].copy()
    ob["tmk"] = tmk_of[ob.pid.values - 1]
    ob = ob.join(own_map, on="tmk")
    ow = (ob.groupby(["lab", "owner_resolved", "owner_type"],
                     dropna=False).size() * CELL_AC).rename("ac").reset_index()

    # rough locality anchors for the notes column (nearest to centroid)
    anchors = {
        "Waianae Range mauka": (-158.155, 21.50), "Lualualei": (-158.145, 21.43),
        "Nanakuli": (-158.13, 21.40), "Kaena/Mokuleia": (-158.20, 21.575),
        "Waialua": (-158.07, 21.57), "Kahuku": (-157.96, 21.68),
        "Laie/Malaekahana": (-157.935, 21.635), "Hauula/Punaluu": (-157.90, 21.58),
        "Kaaawa/Kualoa": (-157.85, 21.54), "Waiahole/Waikane": (-157.86, 21.49),
        "Kahaluu/Kaneohe": (-157.84, 21.44), "Waimanalo": (-157.72, 21.34),
        "Ewa/Kalaeloa": (-158.06, 21.33), "Kunia": (-158.05, 21.42),
        "Schofield/Wahiawa": (-158.03, 21.49), "Helemano/Poamoho": (-157.99, 21.53),
        "Pupukea/Waimea": (-158.05, 21.63), "Waipio/Waiawa": (-157.99, 21.42),
        "Pearl City/Waiau": (-157.95, 21.40), "Kaneohe Bay/Mokapu": (-157.77, 21.45),
    }

    def locality(lon, lat):
        return min(anchors,
                   key=lambda k: (anchors[k][0] - lon) ** 2
                   + (anchors[k][1] - lat) ** 2)

    rows, spurs = [], []
    for rank, (cid, r) in enumerate(keep.iterrows(), 1):
        geom = geoms[cid]
        d46_edge = geom.distance(net46) / 1000
        d138_edge = geom.distance(net138) / 1000
        dir46, p_from, p_to = bearing_to(geom, net46)
        spurs.append((p_from, p_to))
        o = ow[ow.lab == cid].sort_values("ac", ascending=False)
        big = o[(o.ac >= 100) & o.owner_resolved.notna()
                & ~o.owner_resolved.str.contains("Various owners", na=False)]
        n_owners = big.owner_resolved.nunique()
        top = "; ".join(
            f"{x.owner_resolved} ({100 * x.ac / r.buildable_ac_le30:.0f}%)"
            for x in o.head(3).itertuples() if pd.notna(x.owner_resolved))
        fed_ac = o[o.owner_type == "federal"].ac.sum()
        lon = round(gpd.GeoSeries([geom.centroid], crs=CRS)
                    .to_crs(4326).iloc[0].x, 4)
        lat = round(gpd.GeoSeries([geom.centroid], crs=CRS)
                    .to_crs(4326).iloc[0].y, 4)
        rows.append({
            "cluster_id": f"C{rank:02d}",
            "buildable_ac_le15": round(r.buildable_ac_le15),
            "buildable_ac_le30": round(r.buildable_ac_le30),
            "mw_5ac": round(r.buildable_ac_le30 / 5),
            "mw_7ac": round(r.buildable_ac_le30 / 7),
            "pct_de": round(100 * r.de_ac_le30 / r.buildable_ac_le30),
            "pct_bc_s3": round(100 * r.bc_ac_le30 / r.buildable_ac_le30),
            # mean = mean buildable-cell distance (ranking denominator);
            # edge = min distance from cluster boundary to the network
            "km_new_row_46kv": round(r.mean_km46, 1),
            "km_new_row_46kv_edge": round(d46_edge, 1),
            "km_new_row_138kv": round(r.mean_km138, 1),
            "km_new_row_138kv_edge": round(d138_edge, 1),
            "dir_to_46kv": dir46,
            "acres_per_km": round(r.buildable_ac_le30 / max(r.mean_km46, .1)),
            "n_owners_100ac": n_owners,
            "owners_per_km": round(n_owners / max(r.mean_km46, 0.1), 1),
            "top_owners": top,
            "majority_federal_flag": bool(fed_ac > 0.5 * r.buildable_ac_le30),
            "centroid_lon": lon, "centroid_lat": lat,
            "notes": locality(lon, lat) + " (approx)",
            "_geom": geom,
        })
    out = pd.DataFrame(rows)
    out.drop(columns="_geom").to_csv(GIS / "oahu_corridor_candidates.csv",
                                     index=False)
    show_cols = ["cluster_id", "buildable_ac_le15", "buildable_ac_le30",
                 "mw_5ac", "pct_de", "pct_bc_s3", "km_new_row_46kv",
                 "km_new_row_138kv", "acres_per_km", "n_owners_100ac",
                 "owners_per_km", "majority_federal_flag", "notes"]
    print(out[show_cols].to_string(index=False))

    # ---- the cheap-upgrade ring: buildable land 1-3 km from a line
    ring = (cls > 0) & (band > 0) & buf3 & ~buf1
    rc = pd.DataFrame({"cls": cls[ring], "band": band[ring],
                       "pid": pid[ring]})
    rc["le15"] = rc.band <= 3
    rc["le30"] = rc.band <= 6
    grp = np.select([rc.cls.isin([2, 3]), rc.cls.isin([4, 5])],
                    ["BC", "DE"], default="A")
    ring_tab = pd.DataFrame({
        "buildable_ac_le15": rc[rc.le15].groupby(grp[rc.le15]).size()
        * CELL_AC,
        "buildable_ac_le30": rc[rc.le30].groupby(grp[rc.le30]).size()
        * CELL_AC}).round(0)
    rb = rc[rc.le30 & (rc.pid > 0)].copy()
    rb["tmk"] = tmk_of[rb.pid.values - 1]
    rb = rb.join(own_map, on="tmk")
    rown = (rb.groupby("owner_resolved").size() * CELL_AC)
    n_ring_owners = int((rown[rown >= 100]).shape[0])
    ring_tab.to_csv(GIS / "oahu_ring_1_3km_summary.csv")
    print("\n1-3 km ring (buildable acres by soil group):")
    print(ring_tab)
    print(f"distinct resolved owners with >=100 buildable(le30) ac in ring: "
          f"{n_ring_owners}")
    with open(GIS / "oahu_ring_1_3km_summary.csv", "a") as f:
        f.write(f"\n# distinct owners >=100 buildable_le30 ac in ring,"
                f"{n_ring_owners}\n")

    make_figure(out, lines, lsb_ag, spurs)


def make_figure(out, lines, lsb_ag, spurs):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.colors import ListedColormap
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch

    C_138, C_46, SPUR = "#4a3aa7", "#2a78d6", "#d55181"
    # acres-per-km quartile ramp (sequential, single warm hue)
    ramp = ["#fde8d7", "#f6b988", "#e88a3c", "#b35b17"]

    fig, ax = plt.subplots(figsize=(11, 8.5), dpi=160)
    slud = gpd.read_parquet(GIS / "slud.parquet").to_crs(CRS)
    slud[slud.island == "Oahu"].plot(ax=ax, color="#f0efec",
                                     edgecolor="#d8d6d0", linewidth=0.4)
    lsb_ag.plot(ax=ax, color="#e2efe2", edgecolor="none")
    q = pd.qcut(out.acres_per_km, 4, labels=False)
    gdf = gpd.GeoDataFrame(out.assign(q=q), geometry=out._geom, crs=CRS)
    for qi in range(4):
        gdf[gdf.q == qi].plot(ax=ax, color=ramp[qi], edgecolor="#7a4a12",
                              linewidth=0.5)
    lines[lines.kv != "138"].plot(ax=ax, color=C_46, linewidth=0.9)
    lines[lines.kv == "138"].plot(ax=ax, color=C_138, linewidth=1.6)
    for p_from, p_to in spurs:
        ax.plot([p_from.x, p_to.x], [p_from.y, p_to.y], color=SPUR,
                linewidth=1.4, linestyle=(0, (4, 2)))
    for _, r in gdf.iterrows():
        c = r._geom.centroid
        ax.annotate(r.cluster_id, (c.x, c.y), fontsize=7.5,
                    fontweight="bold", color="#0b0b0b", ha="center",
                    va="center",
                    bbox=dict(boxstyle="round,pad=0.15", fc="white",
                              ec="#7a4a12", lw=0.7, alpha=0.9))
    handles = ([Patch(fc=ramp[i], ec="#7a4a12", lw=0.5,
                      label=f"unlock cluster - acres/km Q{i + 1}"
                      + (" (best)" if i == 3 else ""))
                for i in range(4)]
               + [Patch(fc="#e2efe2", label="ag district (served/other)"),
                  Line2D([], [], color=C_138, lw=1.6, label="138 kV"),
                  Line2D([], [], color=C_46, lw=0.9,
                         label="46 kV+ (mapped)"),
                  Line2D([], [], color=SPUR, lw=1.4, linestyle="--",
                         label="shortest new-ROW spur")])
    ax.legend(handles=handles, loc="lower left", fontsize=8, frameon=True,
              framealpha=0.95, edgecolor="#d8d6d0")
    ax.set_title("Candidate transmission unlocks: buildable (slope<=30%) "
                 "ag land >1 km from a mapped line", fontsize=11.5,
                 color="#0b0b0b")
    ax.set_axis_off()
    fig.tight_layout()
    paper = FIGS / "paper"
    paper.mkdir(exist_ok=True)
    fig.savefig(paper / "f_corridors.png", bbox_inches="tight")
    print(f"wrote {paper / 'f_corridors.png'}")


if __name__ == "__main__":
    main()
