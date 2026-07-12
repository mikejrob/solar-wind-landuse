#!/usr/bin/env python3
"""
Slope screen for the Oahu ag-district solar analysis.

Adds percent-slope banding (0-5, 5-10, 10-15, 15-20, 20-25, 25-30, >30%)
to the cap-scenario and transmission screens.

DEM: USGS 3DEP 1/3 arc-second (~10 m) tiles n22w158 + n22w159
(prd-tnm.s3.amazonaws.com StagedProducts, downloaded 2026-07-12), cached in
data/gis/dem/.

Method:
 1. Merge/crop tiles to the Oahu bbox; reproject (bilinear) to EPSG:26904 on
    a 10 m grid.
 2. Percent slope = 100 * |grad z| via central differences (np.gradient) on
    the 10 m grid -- equivalent to GDAL/Horn slope up to edge handling.
 3. Everything (LSB-class polygons, parcels, 1/3 km line buffers) is
    rasterized onto the same 10 m grid; cross-tabs are cell counts
    (1 cell = 100 m^2 = 0.02471 ac). Class x slope tabs are therefore
    polygon-accurate at 10 m resolution (NOT allocated via parcel shares).
 4. S3-eligible acres by slope: eligibility is a per-parcel quota
    (min(0.2*parcel, BC)), not a mapped footprint. Two allocations reported:
    - 'flattest_first': fill the parcel's quota from its flattest B/C cells
      upward (how a developer would site);
    - 'proportional': spread the quota over the parcel's B/C cells uniformly.
    Both stated in outputs; use flattest_first as the headline.

Outputs:
  data/oahu_parcel_slope.csv                (TMK-keyed parcel x slope band)
  data/gis/oahu_lsb_by_slope.csv            (LSB class x slope band, ag district)
  data/gis/oahu_de_neargrid_by_slope.csv    (D/E near 46kV+ by slope band)
  data/gis/oahu_s3_by_slope.csv             (S3-eligible by slope band x distance)
  data/gis/dem/oahu_slope_bands.tif         (uint8 band raster, cached)
  analysis/figs/oahu_slope_bands.png
"""

from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
from rasterio import features
from rasterio.merge import merge as rio_merge
from rasterio.warp import Resampling, reproject

PROJECT = Path("/Users/michaelroberts/Research/solar-wind-landuse")
DATA, GIS = PROJECT / "data", PROJECT / "data" / "gis"
DEM_DIR = GIS / "dem"
FIGS = PROJECT / "analysis" / "figs"
CRS = "EPSG:26904"
RES = 10.0                      # m
CELL_AC = RES * RES / 4046.8564224
BANDS = [0, 5, 10, 15, 20, 25, 30, np.inf]   # percent slope
BAND_COLS = ["slope_0_5", "slope_5_10", "slope_10_15", "slope_15_20",
             "slope_20_25", "slope_25_30", "slope_gt30"]
CLS_CODE = {c: i + 1 for i, c in enumerate("ABCDE")}


def build_slope_raster():
    out = DEM_DIR / "oahu_slope_bands.tif"
    if out.exists():
        with rasterio.open(out) as src:
            return src.read(1), src.transform
    srcs = [rasterio.open(DEM_DIR / f"USGS_13_{t}.tif")
            for t in ("n22w158", "n22w159")]
    dem, tr = rio_merge(srcs, bounds=(-158.32, 21.20, -157.60, 21.78))
    dem = dem[0]
    # target 10 m grid in EPSG:26904 covering the same bbox
    b = gpd.GeoSeries.from_xy([-158.32, -157.60], [21.20, 21.78],
                              crs="EPSG:4326").to_crs(CRS)
    x0, x1 = b.x.min(), b.x.max()
    y0, y1 = b.y.min(), b.y.max()
    w, h = int((x1 - x0) / RES), int((y1 - y0) / RES)
    dst_tr = rasterio.transform.from_origin(x0, y1, RES, RES)
    z = np.full((h, w), np.nan, dtype=np.float32)
    reproject(dem, z, src_transform=tr, src_crs="EPSG:4269",
              dst_transform=dst_tr, dst_crs=CRS,
              resampling=Resampling.bilinear,
              src_nodata=srcs[0].nodata, dst_nodata=np.nan)
    for s in srcs:
        s.close()
    gy, gx = np.gradient(z, RES)
    slope_pct = 100.0 * np.hypot(gx, gy)
    del gy, gx, z, dem
    band = np.digitize(slope_pct, BANDS[1:-1]) + 1   # 1..7
    band = band.astype(np.uint8)
    band[np.isnan(slope_pct)] = 0
    with rasterio.open(out, "w", driver="GTiff", width=w, height=h, count=1,
                       dtype="uint8", crs=CRS, transform=dst_tr, nodata=0,
                       compress="deflate") as dst:
        dst.write(band, 1)
    print(f"wrote {out} ({w}x{h} @ {RES}m)")
    return band, dst_tr


def rasterize(gdf_or_geoms, values, shape, transform, dtype="uint16"):
    shapes = list(zip(gdf_or_geoms, values))
    return features.rasterize(shapes, out_shape=shape, transform=transform,
                              fill=0, dtype=dtype)


def main():
    band, tr = build_slope_raster()
    shape = band.shape

    lsb_ag = gpd.read_parquet(GIS / "lsb_ag.parquet")
    lsb_ag = lsb_ag[lsb_ag.island == "Oahu"]
    cls = rasterize(lsb_ag.geometry, lsb_ag["type"].map(CLS_CODE),
                    shape, tr, "uint8")

    # (a) LSB class x slope band (ag district, polygon-accurate at 10 m)
    m = (cls > 0) & (band > 0)
    counts = np.bincount((cls[m].astype(np.int64) * 8 + band[m]),
                         minlength=6 * 8)
    xt = pd.DataFrame(
        {BAND_COLS[b - 1]: [counts[c * 8 + b] * CELL_AC for c in range(1, 6)]
         for b in range(1, 8)}, index=list("ABCDE")).round(1)
    xt.index.name = "lsb_class"
    xt.to_csv(GIS / "oahu_lsb_by_slope.csv")
    print("LSB class x slope band (acres, Oahu ag district):")
    print(xt.round(0))

    # distance masks from the classified line network
    lines = gpd.read_parquet(GIS / "oahu_lines_classified.parquet")
    net46 = lines.union_all()
    buf1 = rasterize([net46.buffer(1000)], [1], shape, tr, "uint8") == 1
    buf3 = rasterize([net46.buffer(3000)], [1], shape, tr, "uint8") == 1

    # (b) the money table: D/E near grid, by slope band
    rows = {}
    for lab, dist_mask in [("le_1km", buf1), ("le_3km", buf3),
                           ("all", np.ones(shape, bool))]:
        sel = m & np.isin(cls, [CLS_CODE["D"], CLS_CODE["E"]]) & dist_mask
        bc_ = np.bincount(band[sel], minlength=8)[1:8] * CELL_AC
        rows[lab] = bc_
    de = pd.DataFrame(rows, index=BAND_COLS).T.round(1)
    de.index.name = "within_46kvplus"
    de.to_csv(GIS / "oahu_de_neargrid_by_slope.csv")
    print("\nD/E ag-district acres by slope band x distance to 46kV+:")
    print(de.round(0))

    # parcel raster (ag-district parcels from the transmission screen)
    pt = pd.read_csv(DATA / "oahu_land_transmission.csv", dtype={"tmk": str})
    parcels = gpd.read_parquet(GIS / "parcels_oahu.parquet").to_crs(CRS)
    parcels["tmk9txt"] = parcels.tmk9txt.astype(str)
    pg = (parcels[parcels.tmk9txt.isin(set(pt.tmk))]
          .dissolve(by="tmk9txt")[["geometry"]].reset_index())
    pid = rasterize(pg.geometry, pg.index + 1, shape, tr, "uint32")

    # parcel x slope band cell counts
    pm = (pid > 0) & (band > 0)
    key = pid[pm].astype(np.int64) * 8 + band[pm]
    pc = np.bincount(key, minlength=(len(pg) + 1) * 8)
    ptab = pd.DataFrame(
        {BAND_COLS[b - 1]: pc[(np.arange(1, len(pg) + 1)) * 8 + b] * CELL_AC
         for b in range(1, 8)})
    ptab.insert(0, "tmk", pg.tmk9txt.values)
    ptab = ptab.merge(pt[["tmk", "parcel_acres"]], on="tmk")
    cols = ["tmk", "parcel_acres", *BAND_COLS]
    ptab[cols].round(3).to_csv(DATA / "oahu_parcel_slope.csv", index=False)
    err = (ptab[BAND_COLS].sum(axis=1) - ptab.parcel_acres) / ptab.parcel_acres
    print(f"\nwrote oahu_parcel_slope.csv ({len(ptab)} parcels); "
          f"rasterization error median {err.abs().median():.1%}, "
          f"95th pct {err.abs().quantile(.95):.1%}")

    # (c) S3-eligible acres by slope band, within 1 km / 3 km (parcel dist)
    # per-parcel B/C cell counts by band
    bc_mask = pm & np.isin(cls, [CLS_CODE["B"], CLS_CODE["C"]])
    kbc = pid[bc_mask].astype(np.int64) * 8 + band[bc_mask]
    cbc = np.bincount(kbc, minlength=(len(pg) + 1) * 8)
    bc_by_band = np.stack([cbc[(np.arange(1, len(pg) + 1)) * 8 + b]
                           for b in range(1, 8)], axis=1) * CELL_AC
    info = pg[["tmk9txtx" if False else "tmk9txt"]].rename(
        columns={"tmk9txt": "tmk"}).merge(
        pt[["tmk", "s3_eligible_acres", "dist_46kv_km"]], on="tmk")
    s3 = info.s3_eligible_acres.values
    out_rows = []
    for method in ("flattest_first", "proportional"):
        alloc = np.zeros_like(bc_by_band)
        tot = bc_by_band.sum(axis=1)
        with np.errstate(divide="ignore", invalid="ignore"):
            if method == "proportional":
                frac = np.where(tot > 0, np.minimum(s3 / tot, 1.0), 0)
                alloc = bc_by_band * frac[:, None]
            else:
                rem = np.minimum(s3, tot)
                for b in range(7):
                    take = np.minimum(rem, bc_by_band[:, b])
                    alloc[:, b] = take
                    rem = rem - take
        for lab, sel in [("le_1km", info.dist_46kv_km < 1),
                         ("le_3km", info.dist_46kv_km < 3),
                         ("all", np.ones(len(info), bool))]:
            r = alloc[sel.values if hasattr(sel, "values") else sel].sum(0)
            out_rows.append({"method": method, "within_46kvplus": lab,
                             **dict(zip(BAND_COLS, r.round(1)))})
    s3tab = pd.DataFrame(out_rows)
    s3tab.to_csv(GIS / "oahu_s3_by_slope.csv", index=False)
    print("\nS3-eligible acres by slope band:")
    print(s3tab.to_string(index=False))

    slud = gpd.read_parquet(GIS / "slud.parquet").to_crs(CRS)
    island = rasterize(slud[slud.island == "Oahu"].geometry,
                       np.ones(int((slud.island == "Oahu").sum())),
                       shape, tr, "uint8") == 1
    make_figure(band, cls, buf1, buf3, island)


def make_figure(band, cls, buf1, buf3, island):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    labels = ["0-5", "5-10", "10-15", "15-20", "20-25", "25-30", ">30"]
    # categorical slots 1-2 from the validated reference palette
    c_abc, c_de = "#2a78d6", "#1baf7a"
    abc = np.isin(cls, [1, 2, 3])

    fig, (ax1, ax3, ax2) = plt.subplots(
        1, 3, figsize=(14, 4.6), dpi=160,
        gridspec_kw={"width_ratios": [1.2, 1.2, 1]})
    x = np.arange(7)
    ymax = 0.0
    for ax, lab, buf in [(ax1, "within 1 km", buf1),
                         (ax3, "within 3 km", buf3)]:
        m = (cls > 0) & (band > 0) & buf
        acres = {g: [((band == b) & m & sel).sum() * CELL_AC
                     for b in range(1, 8)]
                 for g, sel in [("A/B/C (cap or ban applies)", abc),
                                ("D/E (uncapped)", ~abc)]}
        ax.bar(x, acres["D/E (uncapped)"], 0.62, color=c_de,
               label="D/E (uncapped)", edgecolor="white", linewidth=2)
        ax.bar(x, acres["A/B/C (cap or ban applies)"], 0.62,
               bottom=acres["D/E (uncapped)"], color=c_abc,
               label="A/B/C (cap or ban applies)",
               edgecolor="white", linewidth=2)
        tots = (np.array(acres["D/E (uncapped)"])
                + np.array(acres["A/B/C (cap or ban applies)"]))
        ymax = max(ymax, tots.max())
        for i in (0, 1, 2):  # direct labels on the flattest three bands
            ax.annotate(f"{tots[i]:,.0f}", (i, tots[i]), ha="center",
                        va="bottom", fontsize=8.5, color="#0b0b0b")
        ax.set_xticks(x, labels)
        ax.set_xlabel("slope band (percent)", fontsize=9, color="#52514e")
        ax.set_title(f"Ag-district land {lab} of a mapped 46 kV+ line "
                     "(cumulative)", fontsize=9.5, color="#0b0b0b",
                     loc="left")
        ax.spines[["top", "right"]].set_visible(False)
        ax.tick_params(colors="#52514e", labelsize=8.5)
        ax.grid(axis="y", color="#eceae6", linewidth=0.8)
        ax.set_axisbelow(True)
    for ax in (ax1, ax3):  # shared y scale
        ax.set_ylim(0, ymax * 1.1)
    ax1.set_ylabel("acres", fontsize=9, color="#52514e")
    ax3.tick_params(labelleft=False)
    ax1.legend(fontsize=8.5, frameon=False)

    # inset: slope-band map (sequential single hue)
    ramp = ["#ffffff", "#f2f8fd", "#d8eafa", "#b3d6f2", "#84bce7",
            "#569dd9", "#2a78d6", "#12457f"]
    from matplotlib.colors import ListedColormap
    show = band.astype(float).copy()
    show[(band == 0) | ~island] = np.nan
    ax2.imshow(show, cmap=ListedColormap(ramp[1:]), vmin=1, vmax=7,
               interpolation="nearest")
    ax2.set_title("percent slope (light 0-5% ... dark >30%)",
                  fontsize=9, color="#52514e", loc="left")
    ax2.set_axis_off()
    fig.tight_layout()
    out = FIGS / "oahu_slope_bands.png"
    fig.savefig(out, bbox_inches="tight")
    paper = FIGS / "paper"
    paper.mkdir(exist_ok=True)
    fig.savefig(paper / "f4_slope_bands_2panel.png", bbox_inches="tight")
    print(f"wrote {out} and paper/f4_slope_bands_2panel.png")


if __name__ == "__main__":
    main()
