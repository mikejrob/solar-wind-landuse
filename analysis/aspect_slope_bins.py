#!/usr/bin/env python3
"""Aspect + fine slope-bin cross-tab for the Oahu ag-district solar screen.

Implements follow-on #1 and #3 from notes/slope-15-30-challenges.md: the slope
screen bins grade only, but a 15-30% acre's yield depends on which way it faces
(south-facing gains, north-facing loses; notes/slope-15-30-challenges.md sec. 2).
This script overlays a per-cell aspect on the same 10 m grid as the slope screen,
splits the 15-30% band into 15-20% and 20-30%, and reweights each
(slope-bin x aspect) group by the plane-of-array (POA) yield factor.

ASPECT
  Elevation is the same reprojected 10 m grid slope_screen.py derives slope from
  (USGS 3DEP 1/3 arc-second, EPSG:26904). Aspect = compass azimuth of steepest
  descent (the direction the surface faces / water runs downhill), from
  np.gradient of elevation in projected meters. Downhill vector = -grad(z).
  In the array, col increases east, row increases south (origin top-left), so
  east_comp = -d z/d col, north_comp = d z/d row; azimuth = atan2(east, north).
  Classes (bin edges, degrees clockwise from north):
    South   135 <= az < 225
    North   az >= 315 or az < 45
    Neutral otherwise (E/W-facing: 45-135 and 225-315)
  South and North are the +-45 deg wedges about due south / due north; the rest
  is E/W-neutral, where annual POA is within ~2% of flat (sec. 2 table).

SLOPE BINS (from the cached categorical band raster, bands 1..7 =
  0-5,5-10,10-15,15-20,20-25,25-30,>30%):
    <=15   bands 1-3
    15-20  band 4
    20-30  bands 5-6  (20-25 + 25-30)
    >30    band 7

POA WEIGHTING
  data/oahu_poa_aspect_slope.csv gives clear-sky annual POA vs a flat surface at
  21.35N by slope% and aspect (poa_south/north/east columns; east = the neutral
  representative, E/W symmetric). poa_factor = poa_aspect(slope) / poa_flat,
  linearly interpolated at each bin's representative slope:
    <=15 -> 7.5%,  15-20 -> 17.5%,  20-30 -> 25%,  >30 -> 30% (table max; real
    >30 slopes are steeper, so the >30 magnitudes are conservative floors).
  effective_acres = acres * poa_factor = flat-equivalent yield-weighted acreage.
  A north-facing 25% acre (factor ~0.91) counts less than a south-facing one
  (~1.06). Factors are clear-sky ceilings; Oahu cloud damps the swing
  (notes/slope-15-30-challenges.md caveat 2). Grade only, no cost premium.

Categories (existing masks from available_land_map.py):
  de_nonmil  is_de & ~milmask & ~kahmask   (uncapped, permitted use; headline)
  bc_nonmil  is_bc & ~milmask & ~kahmask   (SUP envelope above the cap)
  de_all     is_de                          (all tenure; reconciles to lsb table)
  mil_ag     milmask & agmask & ~esqdmask   (DoD-tenure ag land, for completeness)

Outputs:
  data/oahu_slope_aspect_bins.csv   (category, slope_bin, aspect_class, acres,
                                      poa_factor, effective_acres)
  analysis/figs/paper/f_slope_aspect_bins.png
Reconciles the all-tenure D/E and B/C slope-bin acres to
data/gis/oahu_lsb_by_slope.csv.
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
FIGS = PROJECT / "analysis" / "figs" / "paper"
CRS = "EPSG:26904"
RES = 10.0
CELL_AC = RES * RES / 4046.8564224
CLS_CODE = {c: i + 1 for i, c in enumerate("ABCDE")}

# slope bins as sets of band codes (1..7 = 0-5,5-10,10-15,15-20,20-25,25-30,>30)
SLOPE_BINS = {"<=15": [1, 2, 3], "15-20": [4], "20-30": [5, 6], ">30": [7]}
# representative slope% per bin for the POA lookup (sec. 2 of the note)
BIN_SLOPE = {"<=15": 7.5, "15-20": 17.5, "20-30": 25.0, ">30": 30.0}
ASPECTS = ["South", "Neutral", "North"]
CATS = {
    "de_nonmil": "D/E ag, non-military",
    "bc_nonmil": "B/C ag, non-military (SUP)",
    "de_all": "D/E ag, all tenure",
    "bc_all": "B/C ag, all tenure",
    "mil_ag": "military ag land",
}


def elevation_grid():
    """Reprojected 10 m elevation on the slope_bands.tif grid (same as
    slope_screen.build_slope_raster, but keeps the float DEM for aspect)."""
    srcs = [rasterio.open(DEM_DIR / f"USGS_13_{t}.tif")
            for t in ("n22w158", "n22w159")]
    dem, tr = rio_merge(srcs, bounds=(-158.32, 21.20, -157.60, 21.78))
    dem = dem[0]
    b = gpd.GeoSeries.from_xy([-158.32, -157.60], [21.20, 21.78],
                              crs="EPSG:4326").to_crs(CRS)
    x0, x1, y0, y1 = b.x.min(), b.x.max(), b.y.min(), b.y.max()
    w, h = int((x1 - x0) / RES), int((y1 - y0) / RES)
    dst_tr = rasterio.transform.from_origin(x0, y1, RES, RES)
    z = np.full((h, w), np.nan, dtype=np.float32)
    reproject(dem, z, src_transform=tr, src_crs="EPSG:4269",
              dst_transform=dst_tr, dst_crs=CRS,
              resampling=Resampling.bilinear,
              src_nodata=srcs[0].nodata, dst_nodata=np.nan)
    for s in srcs:
        s.close()
    return z, dst_tr


def aspect_class(z):
    """Per-cell aspect class (South / Neutral / North) from steepest descent."""
    gy, gx = np.gradient(z, RES)          # d z / d(row), d z / d(col)
    east = -gx                            # downhill east component
    north = gy                            # row increases south -> +row = -north
    az = np.degrees(np.arctan2(east, north)) % 360.0
    cls = np.full(z.shape, -1, dtype=np.int8)         # -1 = flat/nodata
    valid = np.isfinite(az)
    south = valid & (az >= 135) & (az < 225)
    nnorth = valid & ((az >= 315) | (az < 45))
    cls[valid] = 1                        # Neutral default for valid cells
    cls[south] = 0                        # South
    cls[nnorth] = 2                       # North
    return cls                            # 0 South, 1 Neutral, 2 North, -1 flat


def rasterize(geoms, values, shape, transform, dtype="uint8"):
    return features.rasterize(list(zip(geoms, values)), out_shape=shape,
                              transform=transform, fill=0, dtype=dtype)


def poa_factors():
    """poa_factor[slope%][aspect] = poa_aspect(slope)/poa_flat, interpolated."""
    p = pd.read_csv(DATA / "oahu_poa_aspect_slope.csv")
    flat = float(p.loc[p.slope_pct == 0, "poa_south"].iloc[0])   # flat, any col
    col = {"South": "poa_south", "Neutral": "poa_east", "North": "poa_north"}
    fac = {}
    for binlab, s in BIN_SLOPE.items():
        fac[binlab] = {a: float(np.interp(s, p.slope_pct, p[col[a]])) / flat
                       for a in ASPECTS}
    return fac


def main():
    band_path = DEM_DIR / "oahu_slope_bands.tif"
    with rasterio.open(band_path) as src:
        band, tr = src.read(1), src.transform
    shape = band.shape

    z, dst_tr = elevation_grid()
    assert z.shape == shape, f"aspect grid {z.shape} != band grid {shape}"
    assert np.allclose([dst_tr.a, dst_tr.e, dst_tr.c, dst_tr.f],
                       [tr.a, tr.e, tr.c, tr.f]), "aspect/band transform mismatch"
    asp = aspect_class(z)

    # LSB class raster (same rasterization as slope_screen / available_land_map)
    lsb_ag = gpd.read_parquet(GIS / "lsb_ag.parquet")
    lsb_ag = lsb_ag[lsb_ag.island == "Oahu"]
    cls = rasterize(lsb_ag.geometry, lsb_ag["type"].map(CLS_CODE), shape, tr)
    is_de = np.isin(cls, [CLS_CODE["D"], CLS_CODE["E"]])
    is_bc = np.isin(cls, [CLS_CODE["B"], CLS_CODE["C"]])

    # tenure / district masks (available_land_map.py definitions)
    mil = gpd.read_parquet(GIS / "military" / "oahu_military_screen.parquet")
    mil_fee = mil[mil.tenure == "fee_or_other"]
    milmask = rasterize(mil_fee.geometry, np.ones(len(mil_fee)), shape, tr) == 1
    ESQD_NAMES = ["West Loch Annex", "Lualualei", "Kipapa Ammo Storage Site",
                  "Puuloa Range Training Facility"]
    esqd = mil_fee[mil_fee.name.isin(ESQD_NAMES)]
    esqdmask = rasterize(esqd.geometry, np.ones(len(esqd)), shape, tr) == 1
    kah = mil[(mil.tenure == "state_lease_2029") & (mil.tmk == "158002002")]
    kahmask = rasterize(kah.geometry, np.ones(len(kah)), shape, tr) == 1
    slud = gpd.read_parquet(GIS / "slud.parquet").to_crs(CRS)
    slud_o = slud[slud.island == "Oahu"]
    agmask = rasterize(slud_o[slud_o.ludcode == "A"].geometry,
                       np.ones((slud_o.ludcode == "A").sum()), shape, tr) == 1

    cat_mask = {
        "de_nonmil": is_de & ~milmask & ~kahmask,
        "bc_nonmil": is_bc & ~milmask & ~kahmask,
        "de_all": is_de,
        "bc_all": is_bc,
        "mil_ag": milmask & agmask & ~esqdmask,
    }

    fac = poa_factors()

    # cross-tab acreage by (category x slope bin x aspect class)
    rows = []
    for ck, cmask in cat_mask.items():
        for binlab, codes in SLOPE_BINS.items():
            bmask = cmask & np.isin(band, codes)
            for ai, aname in enumerate(ASPECTS):
                acres = (bmask & (asp == ai)).sum() * CELL_AC
                f = fac[binlab][aname]
                rows.append({
                    "category": CATS[ck], "category_key": ck,
                    "slope_bin": binlab, "aspect_class": aname,
                    "acres": round(acres, 1), "poa_factor": round(f, 4),
                    "effective_acres": round(acres * f, 1)})
    out = pd.DataFrame(rows)
    out.to_csv(DATA / "oahu_slope_aspect_bins.csv", index=False)
    print(f"wrote {DATA / 'oahu_slope_aspect_bins.csv'} ({len(out)} rows)")

    report(out)
    reconcile(out)
    make_figure(out)


def report(out):
    for ck in ("de_nonmil", "bc_nonmil"):
        d = out[out.category_key == ck]
        name = CATS[ck]
        print(f"\n{name}: acres by slope bin x aspect")
        piv = d.pivot_table(index="slope_bin", columns="aspect_class",
                            values="acres", aggfunc="sum",
                            observed=True).reindex(SLOPE_BINS)[ASPECTS]
        piv["total"] = piv.sum(axis=1)
        print(piv.round(0).to_string())
        inc = d[d.slope_bin.isin(["15-20", "20-30"])]
        raw = inc.acres.sum()
        eff = inc.effective_acres.sum()
        print(f"  15-30% increment: raw {raw:,.0f} ac -> "
              f"POA-weighted {eff:,.0f} ac ({eff / raw * 100 - 100:+.1f}%)")
        for binlab in ("15-20", "20-30"):
            b = inc[inc.slope_bin == binlab]
            s = b.set_index("aspect_class")
            print(f"    {binlab}: South {s.loc['South','acres']:,.0f} / "
                  f"Neutral {s.loc['Neutral','acres']:,.0f} / "
                  f"North {s.loc['North','acres']:,.0f} ac  "
                  f"(eff {b.effective_acres.sum():,.0f})")


def reconcile(out):
    """All-tenure D/E and B/C slope-bin acres vs data/gis/oahu_lsb_by_slope.csv."""
    lsb = pd.read_csv(GIS / "oahu_lsb_by_slope.csv", index_col=0)
    pub = {"de_all": lsb.loc[["D", "E"]].sum(),
           "bc_all": lsb.loc[["B", "C"]].sum()}
    band_of = {"<=15": ["slope_0_5", "slope_5_10", "slope_10_15"],
               "15-20": ["slope_15_20"], "20-30": ["slope_20_25", "slope_25_30"],
               ">30": ["slope_gt30"]}
    print("\nreconciliation vs data/gis/oahu_lsb_by_slope.csv (all tenure):")
    worst = 0.0
    for key, label in [("de_all", "D/E all tenure"), ("bc_all", "B/C all tenure")]:
        mine = (out[out.category_key == key].groupby("slope_bin", observed=True)
                .acres.sum())
        for binlab in SLOPE_BINS:
            m = mine.get(binlab, 0.0)
            p = pub[key][band_of[binlab]].sum()
            worst = max(worst, abs(m - p))
            flag = "OK" if abs(m - p) < max(2.0, 0.005 * p) else "DIFF"
            print(f"  {label} {binlab}: mine {m:,.0f} vs pub {p:,.0f}  [{flag}]")
    print(f"  worst abs discrepancy: {worst:.1f} ac")


def make_figure(out):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    SURFACE, INK, MUTE, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#eceae6"
    # house hues: D/E green, B/C orange (available_land_map palette)
    HUE = {"de_nonmil": "#279e6c", "bc_nonmil": "#e39a3b"}

    def lt(hexc, f=0.5):
        h = hexc.lstrip("#")
        r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
        return "#%02x%02x%02x" % tuple(int(v + (255 - v) * f) for v in (r, g, b))

    panels = [("de_nonmil", "D/E ag, non-military (uncapped)"),
              ("bc_nonmil", "B/C ag, non-military (SUP above cap)")]
    fig, axes = plt.subplots(1, 2, figsize=(12, 5.6), dpi=170)
    fig.patch.set_facecolor(SURFACE)
    fig.subplots_adjust(left=0.07, right=0.985, top=0.80, bottom=0.14,
                        wspace=0.17)

    groups = [("15-20", a) for a in ASPECTS] + [("20-30", a) for a in ASPECTS]
    xlab = [a for _, a in groups]
    x = np.arange(len(groups), dtype=float)
    x[3:] += 0.6                                   # gap between the slope bins
    wbar = 0.38

    for ax, (ck, title) in zip(axes, panels):
        ax.set_facecolor(SURFACE)
        d = out[out.category_key == ck].set_index(["slope_bin", "aspect_class"])
        raw = [d.loc[g, "acres"] for g in groups]
        eff = [d.loc[g, "effective_acres"] for g in groups]
        base, light = HUE[ck], lt(HUE[ck])
        ax.bar(x - wbar / 2, raw, wbar, color=light, edgecolor="white",
               linewidth=1.2, label="raw acres")
        ax.bar(x + wbar / 2, eff, wbar, color=base, edgecolor="white",
               linewidth=1.2, label="POA-weighted (flat-equiv.)")
        ymax = max(raw + eff)
        for xi, r, e in zip(x, raw, eff):
            ax.annotate(f"{r:,.0f}", (xi - wbar / 2, r), ha="center",
                        va="bottom", fontsize=7.0, color=MUTE)
            ax.annotate(f"{e:,.0f}", (xi + wbar / 2, e), ha="center",
                        va="bottom", fontsize=7.0, color=INK)
        ax.set_ylim(0, ymax * 1.16)
        ax.set_xticks(x, xlab, fontsize=8.5, color=MUTE)
        ax.set_title(title, fontsize=10.5, color=INK, loc="left", pad=8)
        ax.spines[["top", "right"]].set_visible(False)
        ax.tick_params(colors=MUTE, labelsize=8.5)
        ax.grid(axis="y", color=GRID, linewidth=0.8)
        ax.set_axisbelow(True)
        # slope-bin group labels below the aspect ticks (data x, axes-frac y)
        trans = ax.get_xaxis_transform()
        for xc, binlab in [(x[:3].mean(), "15-20% slope"),
                           (x[3:].mean(), "20-30% slope")]:
            ax.text(xc, -0.11, binlab, transform=trans, ha="center", va="top",
                    fontsize=9.2, color=INK, fontweight="bold")
        ax.legend(fontsize=8.2, frameon=False, loc="upper right")
    axes[0].set_ylabel("acres", fontsize=9.5, color=MUTE)

    fig.suptitle("Oahu 15-30% ag land: slope band x aspect, raw vs "
                 "yield-weighted acreage", fontsize=13, color=INK, x=0.07,
                 y=0.955, ha="left")
    fig.text(0.07, 0.885,
             "South-facing (azimuth 135-225) gains yield, north-facing "
             "(315-45) loses; neutral = E/W. POA-weight = clear-sky annual "
             "yield vs flat at 21.35N\n(data/oahu_poa_aspect_slope.csv). Grade "
             "only, no cost premium; clear-sky ceiling, cloud damps the swing.",
             fontsize=8.2, color=MUTE, ha="left")
    out_png = FIGS / "f_slope_aspect_bins.png"
    fig.savefig(out_png, facecolor=SURFACE)
    print(f"\nwrote {out_png}")


if __name__ == "__main__":
    main()
