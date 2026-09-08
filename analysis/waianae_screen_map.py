#!/usr/bin/env python3
"""
Map of the "Upper Waianae Mountains" screen used in notes/review-plasch-2026-09.md.

Definition (analysis/review_area_screen.py): ag-district parcels whose
centroid lies in the box lon -158.21..-158.06, lat 21.40..21.60 AND whose
boundary is >2 km from the mapped 46 kV+ network (data/oahu_land_transmission.csv,
dist_46kv_km). Drawn: the box, the 2-km buffer around mapped 46 kV+ and
138 kV lines, the screened parcels, their D/E land at <=15% slope (10 m
cells), the rest of the ag district for context, and a west-Oahu inset.
Output: analysis/figs/waianae_screen_map.png
"""
from pathlib import Path
import numpy as np, pandas as pd, geopandas as gpd, rasterio
from rasterio import features
from shapely import make_valid
from shapely.geometry import box
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

PROJECT = Path(__file__).resolve().parents[1]
DATA, GIS = PROJECT / "data", PROJECT / "data" / "gis"
CRS = "EPSG:26904"; M2AC = 4046.8564224
BOX_WGS = (-158.21, 21.40, -158.06, 21.60); BUF_M = 2000.0

def polygonal(geom):
    from shapely.ops import unary_union
    g = make_valid(geom)
    if g.geom_type in ("Polygon", "MultiPolygon"): return g
    if g.geom_type == "GeometryCollection":
        parts = [p for p in g.geoms if p.geom_type in ("Polygon", "MultiPolygon")]
        return unary_union(parts) if parts else None
    return None

def fix(g):
    g = g.copy(); g["geometry"] = g.geometry.apply(polygonal); return g[g.geometry.notna() & ~g.geometry.is_empty]

def main():
    rp = pd.read_csv(DATA / "oahu_review_area_parcels.csv", dtype={"tmk": str})
    sel = set(rp[rp.area.str.startswith("Upper Waianae")].tmk)
    cap = pd.read_csv(DATA / "cap_scenarios_by_parcel.csv", dtype={"tmk": str}); cap = cap[cap.island == "Oahu"]
    par = gpd.read_parquet(GIS / "parcels_oahu.parquet").to_crs(CRS)
    par = fix(par[par.tmk9txt.isin(cap.tmk)].dissolve(by="tmk9txt")[["geometry"]]).reset_index().rename(columns={"tmk9txt": "tmk"})
    own = pd.read_csv(DATA / "oahu_ag_owners.csv", dtype={"tmk": str}).set_index("tmk")
    par["owner_type"] = own.owner_type.reindex(par.tmk).fillna("unknown").values
    scr = par[par.tmk.isin(sel)]; rest = par[~par.tmk.isin(sel)]
    slud = gpd.read_parquet(GIS / "slud.parquet"); slud = fix(slud[slud.island.str.lower() == "oahu"].to_crs(CRS))
    island = slud.geometry.union_all()
    lines = gpd.read_parquet(GIS / "oahu_lines_classified.parquet").to_crs(CRS)
    buf46 = lines[lines.kv != "138"].geometry.union_all().buffer(BUF_M)
    bx = gpd.GeoSeries([box(*BOX_WGS)], crs=4326).to_crs(CRS).iloc[0]

    # D/E <=15% cells inside the screened parcels
    with rasterio.open(GIS / "dem" / "oahu_slope_bands.tif") as r:
        slope = r.read(1); tr = r.transform; shape = r.shape
    lsb = gpd.read_parquet(GIS / "lsb_ag.parquet"); lsb = fix(lsb[lsb.island.str.lower() == "oahu"].to_crs(CRS))
    lsb["type"] = lsb["type"].astype(str).str.strip()
    de = features.rasterize(((g, 1) for g in lsb[lsb["type"].isin(["D", "E"])].geometry), out_shape=shape, transform=tr, fill=0, dtype="uint8").astype(bool)
    scr_r = features.rasterize(((g, 1) for g in scr.geometry), out_shape=shape, transform=tr, fill=0, dtype="uint8").astype(bool)
    le15 = (slope >= 1) & (slope <= 3); s1530 = (slope >= 4) & (slope <= 6)
    de15 = scr_r & de & le15; de30 = scr_r & de & s1530
    with rasterio.open(GIS / "dem" / "oahu_elev_m_10m_26904.tif") as r: elev = r.read(1)
    ag = features.rasterize(((g, 1) for g in slud[slud.ludcode == "A"].geometry), out_shape=shape, transform=tr, fill=0, dtype="uint8").astype(bool)
    box_r = features.rasterize([(bx, 1)], out_shape=shape, transform=tr, fill=0, dtype="uint8").astype(bool)
    bands = [(0, 100), (100, 200), (200, 300), (300, 500), (500, 800), (800, 2000)]
    rows = []
    for lo, hi in bands:
        eb = (elev >= lo) & (elev < hi)
        rows.append({"elev_band_m": f"{lo}-{hi}", "screened_de_le15_ac": (de15 & eb).sum() * 100 / M2AC, "screened_de_15_30_ac": (de30 & eb).sum() * 100 / M2AC,
                     "box_ag_de_le15_ac": (box_r & ag & de & le15 & eb).sum() * 100 / M2AC, "oahu_ag_de_le15_ac": (ag & de & le15 & eb).sum() * 100 / M2AC})
    et = pd.DataFrame(rows).round(0); et.to_csv(DATA / "oahu_waianae_screen_by_elevation.csv", index=False); print(et.to_string(index=False))
    # hillshade
    gy, gx = np.gradient(np.where(elev > -9000, elev, 0), 10.0); slp = np.arctan(np.hypot(gx, gy)); asp = np.arctan2(-gx, gy)
    az, alt = np.radians(315), np.radians(45)
    hs = np.sin(alt) * np.cos(slp) + np.cos(alt) * np.sin(slp) * np.cos(az - asp); hs = np.clip(hs, 0, 1)
    print(f"screened parcels {len(scr)}; D/E <=15% inside them {de15.sum() * 100 / M2AC:,.0f} ac; D/E 15-30% {de30.sum() * 100 / M2AC:,.0f} ac")
    ot = scr.owner_type.value_counts(); print(ot.head(6).to_dict())

    # figure
    fig, ax = plt.subplots(figsize=(9, 11.9), dpi=170)
    fig.subplots_adjust(top=0.855, bottom=0.05, left=0.02, right=0.98)
    minx, miny, maxx, maxy = bx.bounds; pad = 2500
    ax.set_xlim(minx - pad, maxx + pad); ax.set_ylim(miny - pad, maxy + pad)
    gpd.GeoSeries([island], crs=CRS).plot(ax=ax, color="#f3f1ec", edgecolor="#9a9a9a", linewidth=0.6, zorder=0)
    ext = (tr.c, tr.c + tr.a * shape[1], tr.f + tr.e * shape[0], tr.f)
    ax.imshow(hs, extent=ext, origin="upper", cmap="gray", vmin=0, vmax=1, alpha=0.45, interpolation="bilinear", zorder=0.5)
    slud[slud.ludcode == "A"].plot(ax=ax, color="#e9ecdf", edgecolor="none", alpha=0.55, zorder=1)
    slud[slud.ludcode == "C"].plot(ax=ax, facecolor="none", edgecolor="#5a7a4a", hatch="....", linewidth=0.3, alpha=0.5, zorder=1.5)
    cs = ax.contour(np.linspace(ext[0], ext[1], shape[1]), np.linspace(ext[3], ext[2], shape[0]), np.where(elev > -9000, elev, np.nan), levels=[300, 600, 900], colors="#6b6b6b", linewidths=0.5, alpha=0.8, zorder=2.5)
    ax.clabel(cs, fmt="%d m", fontsize=6, inline=True)
    rest.plot(ax=ax, facecolor="none", edgecolor="#c9c9c9", linewidth=0.15, zorder=2)
    gpd.GeoSeries([buf46.intersection(island)], crs=CRS).plot(ax=ax, color="#2a78d6", alpha=0.10, edgecolor="#2a78d6", linewidth=0.6, linestyle=(0, (3, 2)), zorder=3)
    ag_union = slud[slud.ludcode == "A"].geometry.union_all()
    scr_ag = scr.copy(); scr_ag["geometry"] = scr_ag.geometry.intersection(ag_union); scr_ag = scr_ag[~scr_ag.geometry.is_empty]
    scr.plot(ax=ax, facecolor="none", edgecolor="#8c5a1a", linewidth=0.35, zorder=4)          # whole-parcel outlines
    scr_ag.plot(ax=ax, facecolor="#f2c98a", edgecolor="none", alpha=0.9, zorder=4.1)          # ag-district part only
    for arr, col in [(de30, "#9dd7bd"), (de15, "#1b8a5a")]:
        rgba = np.zeros(shape + (4,), dtype=np.float32); c = matplotlib.colors.to_rgb(col)
        rgba[..., :3] = c; rgba[..., 3] = arr.astype(np.float32)
        ax.imshow(rgba, extent=ext, origin="upper", interpolation="nearest", zorder=5)
    lines[lines.kv != "138"].plot(ax=ax, color="#2a78d6", linewidth=1.0, zorder=6)
    lines[lines.kv == "138"].plot(ax=ax, color="#4a3aa7", linewidth=1.8, zorder=7)
    gpd.GeoSeries([bx.exterior], crs=CRS).plot(ax=ax, color="#b3261e", linewidth=1.6, linestyle=(0, (6, 3)), zorder=8)
    for nm, lon, lat in [("Waiʻanae", -158.185, 21.447), ("Mākaha", -158.21, 21.475), ("Nānākuli", -158.15, 21.39), ("Lualualei", -158.13, 21.43),
                         ("Mākua", -158.22, 21.53), ("Mokulēʻia", -158.13, 21.575), ("Kunia", -158.06, 21.43), ("Schofield", -158.07, 21.50), ("Mt. Kaʻala", -158.145, 21.507)]:
        p = gpd.GeoSeries([gpd.points_from_xy([lon], [lat])[0]], crs=4326).to_crs(CRS).iloc[0]
        ax.annotate(nm, (p.x, p.y), fontsize=7.5, color="#333", ha="center", zorder=9)
    ax.set_axis_off()
    fig.suptitle("Potential-issue flag, \"Upper Waiʻanae Mountains\" (reviewer item): ag-district parcels in the box and >2 km from a mapped 46 kV+ line",
                 fontsize=10, x=0.02, y=0.985, ha="left")
    leg = [Line2D([], [], color="#b3261e", lw=1.6, ls=(0, (6, 3)), label="screening box (−158.21…−158.06, 21.40…21.60)"),
           Patch(facecolor="none", edgecolor="#8c5a1a", label=f"parcels carrying the flag (not removed from the accounting): {len(scr):,} parcels; {scr.geometry.area.sum() / M2AC:,.0f} ac, whole-parcel outline"),
           Patch(facecolor="#f2c98a", label="flagged parcels: ag-district part with soil class A/B/C, or D/E steeper than 30%, or unrated"),
           Patch(facecolor="#1b8a5a", label=f"flagged parcels: class D/E soil, ≤15% slope — the part the modeled subset counts ({de15.sum() * 100 / M2AC:,.0f} ac)"),
           Patch(facecolor="#9dd7bd", label=f"flagged parcels: class D/E soil, 15–30% slope ({de30.sum() * 100 / M2AC:,.0f} ac)"),
           Patch(facecolor="#2a78d6", alpha=0.15, edgecolor="#2a78d6", label="within 2 km of mapped 46 kV+ (parcels here are not flagged)"),
           Line2D([], [], color="#2a78d6", lw=1.0, label="46 kV+ (mapped; under-mapped)"),
           Line2D([], [], color="#4a3aa7", lw=1.8, label="138 kV"),
           Patch(facecolor="#e9ecdf", edgecolor="#c9c9c9", label="other ag-district land"),
           Patch(facecolor="none", edgecolor="#5a7a4a", hatch="....", label="Conservation district (mountain interior; never counted)"),
           Line2D([], [], color="#6b6b6b", lw=0.5, label="300 / 600 / 900 m contours")]
    fig.legend(handles=leg, loc="upper left", bbox_to_anchor=(0.02, 0.975), fontsize=7.2, frameon=False, ncol=1, handlelength=2.2)
    fig.text(0.02, 0.04, "Sources: geodata.hawaii.gov parcels, SLUD, LSB; HIFLD/OSM lines; USGS 3DEP (slope, elevation, hillshade). Parcel-centroid box rule; "
             "distance = parcel boundary to nearest mapped 46 kV+ line.\nThe 46 kV network is under-mapped, so parcels along Farrington Hwy can be closer to a line than shown. "
             "DHHL homestead parcels in Waiʻanae and Lualualei are inside the screen.", fontsize=6.3, color="#555", va="top")
    # inset
    ia = fig.add_axes([0.72, 0.70, 0.24, 0.16]); gpd.GeoSeries([island], crs=CRS).plot(ax=ia, color="#e6e6e6", edgecolor="#999", linewidth=0.4)
    scr.plot(ax=ia, color="#e39a3b", edgecolor="none"); gpd.GeoSeries([bx.exterior], crs=CRS).plot(ax=ia, color="#b3261e", linewidth=1.0)
    ia.set_axis_off(); ia.set_title("Oʻahu", fontsize=7)
    out = PROJECT / "analysis" / "figs" / "waianae_screen_map.png"; fig.savefig(out, bbox_inches="tight"); print("wrote", out)

if __name__ == "__main__":
    main()
