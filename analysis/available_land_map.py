#!/usr/bin/env python3
"""
Three-layer map of plausibly-available solar land on Oahu.

Layer 1 (plausibly available, <=15% slope unless noted):
  a. Class D/E ag-district land (uncapped, permitted use).
  b. Class B/C ag-district land (SUP path above the cap).
  c. Military fee land inside the state Ag district (DoD discretion; EUL
     only), minus the ESQD footprint (drawn as its own category).
  d. Military fee land inside the state Urban district (EUL discretion),
     minus the ESQD footprint.
  e. Military ESQD/ordnance-buffer land (West Loch Annex, Lualualei, Kipapa,
     Puuloa — the ordnance/ESQD constraint tier of
     notes/military-land-solar.md; unoccupied PV can be compatible, Kupono
     precedent).
  f. Kahuku lease parcel TMK 158002002 (state land, lease x Ag,
     Army-retained under the Aug-2025 ROD). Bold outline + crosshatch.
  g. Durable non-ag sites: closed golf courses, quarries/landfills/brownfields,
     durable urban candidates (viability_class == durable).
  h. Reservoirs (OSM water=reservoir / landuse=reservoir): floating-solar
     candidates, unscreened; no slope filter.
Layer 2 (modeling subset, <=10% slope):
  a. All class D/E ag land <=10% slope.
  b. Quasi-random, spatially even selection of B/C parcels: 2-km grid +
     per-cell Halton(2,3) anchor points (skip 42), round-robin across cells,
     accumulating each parcel's B/C-on-<=10%-slope acreage until 10% of TOTAL
     Oahu B/C acreage (target ~3,437 of 34,370 ac). Only the <=10%-slope B/C
     portion counts toward the target. Output:
     data/oahu_bc_10pct_selection.csv (Switch-Oahu modeling input).
  c. Military fee-x-Ag land on LSB class D/E at <=10% slope, minus the ESQD
     footprint (DoD discretion; subset of category c).
Layer 3: existing 138 kV (heavy) and 46 kV+ (thin) lines; greedy expansion
  build-out segments dashed.

Category masks are mutually exclusive: the military fee footprint is removed
from the D/E and B/C fills (and from the B/C selection pool); the ESQD
footprint is removed from the military ag and military urban fills; the
lease-tenure Kahuku parcel is removed from the civilian D/E and B/C fills
and touches no fee-military category. Each acre draws in exactly one
Layer-1 category. Layer-2 fills are emphasis overlays on their own Layer-1
base (D/E, selected B/C, military ag). No grid-distance filter is applied
anywhere; published near-grid figures
(data/gis/oahu_de_neargrid_by_slope.csv) are smaller.

Slope: cached 10 m band raster data/gis/dem/oahu_slope_bands.tif
(bands 1..7 = 0-5,5-10,10-15,15-20,20-25,25-30,>30%; 0 = nodata).
CRS EPSG:26904 throughout; acres = cells * 100 m^2 / 4046.8564224.

Colors validated with the dataviz palette checker (light surface #fcfcfb):
#279e6c,#e39a3b,#b85a0a,#2a78d6 all-pairs PASS (worst CVD deltaE 8.3 protan;
normal-vision floor 17.6). All military categories are achromatic gray tones
distinguished by hatch direction (//// ag, \\\\ urban, .. ESQD, xx Kahuku) —
texture carries identity, so no new chromatic hues were added; the Layer-2
military emphasis is a darker lightness step of the same neutral. Durable
sites are near-black ink markers (annotation layer, not categorical hues).
The light tints of green/orange are lightness steps of the same hues
(emphasis coding).

Outputs:
  analysis/figs/paper/f_available_land.png
  data/oahu_bc_10pct_selection.csv
(console prints the acreage reconciliation used in notes/available-land-map.md)
"""

import json
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
from rasterio import features
from shapely import make_valid
from shapely.geometry import LineString, Point, Polygon
from shapely.ops import polygonize, unary_union

PROJECT = Path("/Users/michaelroberts/Research/solar-wind-landuse")
DATA, GIS = PROJECT / "data", PROJECT / "data" / "gis"
FIGS = PROJECT / "analysis" / "figs" / "paper"
CRS = "EPSG:26904"
M2AC = 4046.8564224
CELL_AC = 100.0 / M2AC
CLS_CODE = {c: i + 1 for i, c in enumerate("ABCDE")}

HALTON_SKIP = 42          # fixed seed/skip for the Halton sequence
GRID_M = 2000.0           # selection grid cell size (m)
TARGET_FRAC = 0.10        # of TOTAL Oahu B/C acreage

# palette (validated; see module docstring)
C_DE_LT, C_DE = "#a9dcc6", "#279e6c"      # D/E <=15% tint, <=10% emphasis
C_BC_LT, C_BC = "#f3d3a4", "#b85a0a"      # B/C <=15% tint, selected parcels
C_MIL_FILL, C_MIL_HATCH = "#dedbd4", "#6b6862"
C_URB_FILL = "#cfcdc7"                    # military urban fee (\\\\ hatch)
C_ESQD_FILL = "#e8e5df"                   # military ESQD buffer (.. hatch)
C_KAH_FILL = "#b7b3ab"                    # Kahuku lease parcel (xx hatch)
C_MILDE = "#55534e"                       # Layer-2 military ag D/E emphasis
C_INK, C_MUTE = "#0b0b0b", "#52514e"
C_138, C_46 = "#4a3aa7", "#2a78d6"
C_SITE, C_RES = "#262626", "#2a78d6"
SURFACE, ISLAND, ISLAND_EC = "#fcfcfb", "#f0efec", "#d8d6d0"


def halton(i, base):
    f, r = 1.0, 0.0
    while i > 0:
        f /= base
        r += f * (i % base)
        i //= base
    return r


def rasterize(geoms, values, shape, transform, dtype="uint8"):
    return features.rasterize(list(zip(geoms, values)), out_shape=shape,
                              transform=transform, fill=0, dtype=dtype)


def load_reservoirs():
    """OSM reservoir polygons (cached Overpass pull, data/gis/)."""
    d = json.load(open(GIS / "osm_reservoirs_oahu.json"))
    geoms, names = [], []
    for e in d["elements"]:
        if e["type"] == "way":
            pts = [(p["lon"], p["lat"]) for p in e["geometry"]]
            if len(pts) >= 4:
                geoms.append(Polygon(pts))
                names.append(e.get("tags", {}).get("name", ""))
        elif e["type"] == "relation":
            rings = [LineString([(p["lon"], p["lat"]) for p in m["geometry"]])
                     for m in e.get("members", [])
                     if m.get("role") == "outer" and "geometry" in m]
            polys = list(polygonize(rings))
            if polys:
                geoms.append(unary_union(polys))
                names.append(e.get("tags", {}).get("name", ""))
    g = gpd.GeoDataFrame({"name": names}, geometry=geoms,
                         crs="EPSG:4326").to_crs(CRS)
    g["geometry"] = g.geometry.apply(
        lambda x: make_valid(x) if not x.is_valid else x)
    g["acres"] = g.area / M2AC
    return g


def select_bc_parcels(pg, bc10_ac, bc_all_ac, target_ac):
    """2-km-grid Halton round-robin selection over parcels with B/C on
    <=10% slope. Deterministic: HALTON_SKIP fixes the sequence."""
    elig = pg[bc10_ac > 0].copy()
    elig["bc10_acres"] = bc10_ac[bc10_ac > 0]
    elig["bc_acres"] = bc_all_ac[bc10_ac > 0]
    cx = elig.geometry.centroid
    minx, miny = np.floor(cx.x.min() / GRID_M) * GRID_M, \
        np.floor(cx.y.min() / GRID_M) * GRID_M
    col = ((cx.x - minx) // GRID_M).astype(int)
    row = ((cx.y - miny) // GRID_M).astype(int)
    elig["cell"] = ["c%03d_r%03d" % (c, r) for c, r in zip(col, row)]
    cells = sorted(elig.cell.unique())
    # one Halton(2,3) anchor point per occupied cell, in sorted-cell order
    order_in_cell = {}
    for i, cell in enumerate(cells):
        h2 = halton(HALTON_SKIP + i, 2)
        h3 = halton(HALTON_SKIP + i, 3)
        c, r = int(cell[1:4]), int(cell[6:9])
        ax = minx + (c + h2) * GRID_M
        ay = miny + (r + h3) * GRID_M
        sub = elig[elig.cell == cell]
        d = sub.geometry.centroid.distance(Point(ax, ay))
        order_in_cell[cell] = list(d.sort_values().index)
    # Round-robin across cells, next-nearest parcel per cell. Cells are
    # visited in a FIXED pseudorandom permutation (seed 42), not sorted
    # order: the target is reached after ~70 of the occupied cells, so a
    # sorted (west-to-east) sweep would concentrate the selection in
    # western Oahu. The permutation spreads contributing cells island-wide.
    rng = np.random.RandomState(HALTON_SKIP)
    visit = [cells[i] for i in rng.permutation(len(cells))]
    picked, total, rank, exhausted = [], 0.0, 0, set()
    while total < target_ac and len(exhausted) < len(cells):
        for cell in visit:
            if total >= target_ac:
                break
            q = order_in_cell[cell]
            if not q:
                exhausted.add(cell)
                continue
            idx = q.pop(0)
            rank += 1
            total += elig.loc[idx, "bc10_acres"]
            picked.append({"tmk": elig.loc[idx, "tmk"],
                           "parcel_acres": elig.loc[idx, "parcel_acres"],
                           "bc_acres": round(elig.loc[idx, "bc_acres"], 2),
                           "bc10_acres": round(elig.loc[idx, "bc10_acres"], 2),
                           "grid_cell": cell, "selection_rank": rank})
    sel = pd.DataFrame(picked)
    print(f"selection grid: {len(cells)} occupied 2-km cells "
          f"({len(elig)} eligible parcels)")
    return sel, elig, total


def main():
    # ---- rasters ------------------------------------------------------
    with rasterio.open(GIS / "dem" / "oahu_slope_bands.tif") as src:
        band, tr = src.read(1), src.transform
    shape = band.shape
    le15 = np.isin(band, [1, 2, 3])
    le10 = np.isin(band, [1, 2])

    lsb_ag = gpd.read_parquet(GIS / "lsb_ag.parquet")
    lsb_ag = lsb_ag[lsb_ag.island == "Oahu"].copy()
    lsb_ag["geometry"] = lsb_ag.geometry.apply(
        lambda g: make_valid(g) if not g.is_valid else g)
    cls = rasterize(lsb_ag.geometry, lsb_ag["type"].map(CLS_CODE), shape, tr)
    is_de = np.isin(cls, [CLS_CODE["D"], CLS_CODE["E"]])
    is_bc = np.isin(cls, [CLS_CODE["B"], CLS_CODE["C"]])

    # military fee footprint, ESQD tier, Kahuku lease parcel, districts
    mil = gpd.read_parquet(GIS / "military" / "oahu_military_screen.parquet")
    mil_fee = mil[mil.tenure == "fee_or_other"]
    milmask = rasterize(mil_fee.geometry, np.ones(len(mil_fee)),
                        shape, tr) == 1
    # ordnance/ESQD constraint tier (notes/military-land-solar.md sec. 2;
    # viability tiers in data/oahu_military_land.csv): the four ESQD-bound
    # installations where unoccupied PV can be compatible (Kupono precedent)
    ESQD_NAMES = ["West Loch Annex", "Lualualei", "Kipapa Ammo Storage Site",
                  "Puuloa Range Training Facility"]
    esqd = mil_fee[mil_fee.name.isin(ESQD_NAMES)]
    assert len(esqd) == 4, "expected 4 ESQD installation polygons"
    esqdmask = rasterize(esqd.geometry, np.ones(len(esqd)), shape, tr) == 1
    # Kahuku retained lease parcel (lease x Ag, Army-retained 2025 ROD)
    kah = mil[(mil.tenure == "state_lease_2029") & (mil.tmk == "158002002")]
    assert len(kah) == 1, "expected 1 Kahuku lease parcel"
    kahmask = rasterize(kah.geometry, np.ones(len(kah)), shape, tr) == 1
    slud = gpd.read_parquet(GIS / "slud.parquet").to_crs(CRS)
    slud_o = slud[slud.island == "Oahu"]
    agmask = rasterize(slud_o[slud_o.ludcode == "A"].geometry,
                       np.ones((slud_o.ludcode == "A").sum()), shape, tr) == 1
    urbmask = rasterize(slud_o[slud_o.ludcode == "U"].geometry,
                        np.ones((slud_o.ludcode == "U").sum()),
                        shape, tr) == 1

    # ---- Layer-1/2 category masks (mutually exclusive) ----------------
    # subtractions: ESQD out of the military ag and urban fills; the
    # lease-tenure Kahuku parcel out of the civilian D/E and B/C fills
    # (it is not in milmask, which is fee-only). Each acre draws once.
    m_de15 = is_de & le15 & ~milmask & ~kahmask
    m_bc15 = is_bc & le15 & ~milmask & ~kahmask
    m_de10 = is_de & le10 & ~milmask & ~kahmask
    m_mil15 = milmask & agmask & le15 & ~esqdmask
    m_urb15 = milmask & urbmask & le15 & ~esqdmask
    m_esqd15 = esqdmask & le15
    m_kah15 = kahmask & le15
    m_milde10 = milmask & agmask & is_de & le10 & ~esqdmask
    # Layer-2 modeled D/E is ALL ag D/E at <=10% slope, military and
    # non-military (Mike 2026-07-24): one emphasis fill. Military hatches
    # overlay it (zorder 3), so military D/E reads as green + hatch and
    # private D/E as solid green. The modeling assumption is "all D/E".
    m_de10_all = is_de & le10

    ac = {k: v.sum() * CELL_AC for k, v in
          [("de15", m_de15), ("bc15", m_bc15), ("de10", m_de10),
           ("mil15", m_mil15), ("urb15", m_urb15), ("esqd15", m_esqd15),
           ("kah15", m_kah15), ("milde10", m_milde10),
           ("de10_all", m_de10_all)]}
    ac["milde10_all"] = (is_de & le10 & milmask).sum() * CELL_AC
    # subtraction accounting for the note
    ac["esqd_from_urb"] = (milmask & urbmask & le15 & esqdmask).sum() * CELL_AC
    ac["esqd_from_ag"] = (milmask & agmask & le15 & esqdmask).sum() * CELL_AC
    ac["kah_from_de"] = (is_de & le15 & ~milmask & kahmask).sum() * CELL_AC
    ac["kah_from_bc"] = (is_bc & le15 & ~milmask & kahmask).sum() * CELL_AC
    ac["milde10_in_esqd"] = \
        (milmask & agmask & is_de & le10 & esqdmask).sum() * CELL_AC
    # reconciliation against published class x slope table (incl. military)
    ac["de15_incl_mil"] = (is_de & le15).sum() * CELL_AC
    ac["bc15_incl_mil"] = (is_bc & le15).sum() * CELL_AC

    # ---- parcels + B/C-on-<=10% acreage -------------------------------
    bp = pd.read_csv(DATA / "cap_scenarios_by_parcel.csv", dtype={"tmk": str})
    bp = bp[bp.island == "Oahu"].copy()
    bc_total = (bp.b_acres + bp.c_acres).sum()
    target = TARGET_FRAC * bc_total
    parcels = gpd.read_parquet(GIS / "parcels_oahu.parquet").to_crs(CRS)
    parcels["tmk9txt"] = parcels.tmk9txt.astype(str)
    haveb = bp[(bp.b_acres + bp.c_acres) > 0]
    pg = (parcels[parcels.tmk9txt.isin(set(haveb.tmk))]
          .dissolve(by="tmk9txt")[["geometry"]].reset_index()
          .rename(columns={"tmk9txt": "tmk"})
          .merge(haveb[["tmk", "parcel_acres", "b_acres", "c_acres"]],
                 on="tmk"))
    pid = rasterize(pg.geometry, pg.index + 1, shape, tr, "uint32")
    sel_cells = (pid > 0) & is_bc & le10 & ~milmask
    counts = np.bincount(pid[sel_cells], minlength=len(pg) + 1)[1:]
    bc10_ac = pd.Series(counts * CELL_AC, index=pg.index)
    bc_all = pg.b_acres + pg.c_acres

    sel, elig, sel_total = select_bc_parcels(pg, bc10_ac, bc_all, target)
    pool = bc10_ac.sum()
    shortfall = max(0.0, target - sel_total)
    sel.to_csv(DATA / "oahu_bc_10pct_selection.csv", index=False)

    # selected-parcel B/C-on-<=10% cells for the fill
    sel_idx = set(pg.index[pg.tmk.isin(set(sel.tmk))] + 1)
    m_sel = sel_cells & np.isin(pid, list(sel_idx))

    # ---- durable non-ag sites -----------------------------------------
    na = pd.read_csv(DATA / "oahu_nonag_solar_candidates.csv",
                     dtype={"tmk_or_site": str})
    dur = na[na.viability_class == "durable"]
    urb = gpd.read_parquet(DATA / "intermediates" /
                           "urban_candidates_enriched.parquet")
    urb["tmk9txt"] = urb.tmk9txt.astype(str)
    osm = gpd.read_parquet(DATA / "intermediates" / "osm_sites.parquet")
    pts, matched = [], 0
    for _, r in dur.iterrows():
        if r["type"] == "urban_parcel":
            g = urb[urb.tmk9txt == r.tmk_or_site]
        else:
            g = osm[osm.osm_id == r.tmk_or_site]
        if len(g):
            pts.append(g.geometry.iloc[0].representative_point())
            matched += 1
    golf = pd.read_csv(DATA / "oahu_golf_courses.csv")
    golf_closed = golf[golf.status == "closed"]
    gpts = gpd.GeoSeries.from_xy(golf_closed.lon, golf_closed.lat,
                                 crs="EPSG:4326").to_crs(CRS)
    site_pts = gpd.GeoSeries(pts + list(gpts), crs=CRS)
    ac["durable15"] = dur.acres_le15.sum() + golf_closed.acres_le15.sum()
    n_sites = len(site_pts)
    print(f"durable sites: {matched}/{len(dur)} candidates matched to "
          f"geometry + {len(golf_closed)} closed golf = {n_sites} markers")

    # ---- reservoirs ----------------------------------------------------
    res = load_reservoirs()
    ac["res"] = res.acres.sum()

    # ---- lines ---------------------------------------------------------
    lines = gpd.read_parquet(GIS / "oahu_lines_classified.parquet")
    exp = gpd.read_parquet(GIS / "expansion_segments.parquet")

    # ---- console reconciliation ---------------------------------------
    print(f"\nOahu B/C total (cap_scenarios): {bc_total:,.0f} ac; "
          f"target {target:,.0f} ac")
    print(f"B/C-on-<=10%-slope pool (non-military parcels): {pool:,.0f} ac "
          f"across {(bc10_ac > 0).sum()} parcels")
    print(f"selected {len(sel)} parcels, {sel_total:,.0f} ac (<=10% basis); "
          f"shortfall {shortfall:,.0f} ac")
    # B/C-selection integrity: pool basis is unchanged (fee-military cells
    # excluded, as before); the lease-tenure Kahuku parcel was in the pool
    # but must not have been drawn.
    assert "158002002" not in set(sel.tmk), \
        "Kahuku lease parcel entered the B/C selection"
    print("B/C selection check: TMK 158002002 in pool "
          f"{bc10_ac[pg.tmk == '158002002'].sum():,.1f} ac, "
          "selected: no (selection unchanged)")
    print("\nacreage (this map, <=15% slope, military excluded from ag "
          "fills):")
    for k in ["de15", "bc15", "mil15", "urb15", "esqd15", "kah15",
              "durable15", "res", "de10", "milde10"]:
        print(f"  {k:10s} {ac[k]:>10,.0f}")
    print("overlap subtractions (stated in notes/available-land-map.md):")
    print(f"  ESQD out of military urban fill: {ac['esqd_from_urb']:,.0f}")
    print(f"  ESQD out of military ag fill:    {ac['esqd_from_ag']:,.0f}")
    print(f"  Kahuku parcel out of ag D/E fill: {ac['kah_from_de']:,.0f}")
    print(f"  Kahuku parcel out of ag B/C fill: {ac['kah_from_bc']:,.0f}")
    print(f"  (mil ag D/E <=10% if ESQD were included: "
          f"{ac['milde10'] + ac['milde10_in_esqd']:,.0f})")
    print("reconciliation vs data/gis/oahu_lsb_by_slope.csv (which includes "
          "the military footprint):")
    print(f"  D/E <=15% incl. military: {ac['de15_incl_mil']:,.0f} "
          f"(published 21,391)")
    print(f"  B/C <=15% incl. military: {ac['bc15_incl_mil']:,.0f} "
          f"(published 30,852)")
    print(f"  reservoirs: {len(res)} polygons, {ac['res']:,.0f} ac "
          f"(unscreened)")

    mil_masks = {"mil": m_mil15, "urb": m_urb15, "esqd": m_esqd15,
                 "kah": m_kah15}
    make_figure(band, tr, slud_o, m_de15, m_bc15, m_de10_all, m_sel, mil_masks,
                m_milde10, kah, site_pts, res, lines, exp, ac, sel, sel_total)


def make_figure(band, tr, slud_o, m_de15, m_bc15, m_de10, m_sel, mil_masks,
                m_milde10, kah, site_pts, res, lines, exp, ac, sel,
                sel_total):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.colors import to_rgba
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch

    h, w = band.shape
    extent = (tr.c, tr.c + w * tr.a, tr.f + h * tr.e, tr.f)

    # priority-stacked RGBA overlay (highest priority last); Layer-1 masks
    # are mutually exclusive, Layer-2 emphasis fills draw on top
    img = np.zeros((h, w, 4), dtype=np.float32)
    for mask, color in [(m_bc15, C_BC_LT), (m_de15, C_DE_LT),
                        (mil_masks["urb"], C_URB_FILL),
                        (mil_masks["esqd"], C_ESQD_FILL),
                        (mil_masks["mil"], C_MIL_FILL),
                        (mil_masks["kah"], C_KAH_FILL),
                        (m_de10, C_DE),
                        (m_sel, C_BC)]:
        img[mask] = to_rgba(color)

    fig, ax = plt.subplots(figsize=(11, 8.5), dpi=170)
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)
    slud_o.plot(ax=ax, color=ISLAND, edgecolor=ISLAND_EC, linewidth=0.4)
    ax.imshow(img, extent=extent, interpolation="nearest", zorder=2)

    # military hatches, aligned with the slope-filtered fills (vectorized
    # masks); hatch direction carries category identity on the gray tones
    from shapely.geometry import shape as shp_shape

    def hatch_mask(mask, hatch, alpha=0.55):
        polys = [shp_shape(g) for g, v in
                 features.shapes(mask.astype(np.uint8), mask=mask,
                                 transform=tr) if v == 1]
        if polys:
            gpd.GeoSeries(polys, crs=CRS).plot(
                ax=ax, facecolor="none", edgecolor=C_MIL_HATCH,
                linewidth=0.0, hatch=hatch, zorder=3, alpha=alpha)

    hatch_mask(mil_masks["mil"], "////")
    hatch_mask(mil_masks["urb"], "\\\\\\\\")
    hatch_mask(mil_masks["esqd"], "..")
    hatch_mask(mil_masks["kah"], "xxxx", alpha=0.7)
    # Kahuku retained lease parcel: bold ink outline (small; make it legible)
    kah.boundary.plot(ax=ax, color=C_INK, linewidth=1.4, zorder=4)

    # transmission
    lines[lines.kv != "138"].plot(ax=ax, color=C_46, linewidth=0.8, zorder=5)
    lines[lines.kv == "138"].plot(ax=ax, color=C_138, linewidth=1.7, zorder=6)
    exp.plot(ax=ax, color=C_138, linewidth=1.3, linestyle=(0, (4, 2.4)),
             zorder=7)

    # markers
    ax.scatter([p.x for p in site_pts], [p.y for p in site_pts], s=16,
               marker="o", facecolor=C_SITE, edgecolor="white",
               linewidth=0.7, zorder=8)
    rc = res.geometry.representative_point()
    ax.scatter(rc.x, rc.y, s=26, marker="^", facecolor=C_RES,
               edgecolor="white", linewidth=0.7, zorder=8)

    handles = [
        Patch(fc=C_DE_LT, label="ag D/E, ≤15% slope (uncapped, no permit)"),
        Patch(fc=C_BC_LT, label="ag B/C, ≤15% slope (SUP above cap)"),
        Patch(fc=C_MIL_FILL, ec=C_MIL_HATCH, hatch="////",
              label="military ag land (DoD discretion)"),
        Patch(fc=C_URB_FILL, ec=C_MIL_HATCH, hatch="\\\\\\\\",
              label="military urban fee land (EUL discretion)"),
        Patch(fc=C_ESQD_FILL, ec=C_MIL_HATCH, hatch="..",
              label="military ESQD buffer (unoccupied-PV-\n"
                    "compatible; Kupono precedent)"),
        Patch(fc=C_KAH_FILL, ec=C_INK, hatch="xxxx", lw=1.2,
              label="Kahuku lease parcel (Army-retained\n2025 ROD)"),
        Patch(fc=C_DE, label="modeled-available: all D/E ≤10% slope\n"
                             "(military + non-military; military hatched)"),
        Patch(fc=C_BC, label="modeled-available: quasi-random 10% of B/C,\n"
                             "drawn from ≤10% slope"),
        Line2D([], [], marker="o", ls="none", mfc=C_SITE, mec="white",
               ms=6, label="durable non-ag site (closed golf, quarry,\n"
                           "landfill, brownfield, urban parcel)"),
        Line2D([], [], marker="^", ls="none", mfc=C_RES, mec="white",
               ms=7, label="reservoirs: floating-solar candidates,\n"
                           "unscreened"),
        Line2D([], [], color=C_138, lw=1.7, label="138 kV (existing)"),
        Line2D([], [], color=C_46, lw=0.8, label="46 kV+ (mapped)"),
        Line2D([], [], color=C_138, lw=1.3, ls=(0, (4, 2.4)),
               label="modeled expansion paths (greedy build-out)"),
    ]
    leg = ax.legend(handles=handles, loc="upper right", fontsize=7.6,
                    frameon=True, framealpha=0.95, edgecolor=ISLAND_EC,
                    borderpad=0.9, labelspacing=0.55)
    leg.get_frame().set_facecolor(SURFACE)

    # acreage table annotation
    rows = [
        ("Layer 1  (≤15% slope)", ""),
        ("  ag D/E (uncapped)", f"{ac['de15']:,.0f} ac"),
        ("  ag B/C (SUP path)", f"{ac['bc15']:,.0f} ac"),
        ("  military ag (DoD discretion)", f"{ac['mil15']:,.0f} ac"),
        ("  military urban fee (EUL)", f"{ac['urb15']:,.0f} ac"),
        ("  military ESQD buffer", f"{ac['esqd15']:,.0f} ac"),
        ("  Kahuku lease parcel", f"{ac['kah15']:,.0f} ac"),
        ("  durable non-ag sites", f"{ac['durable15']:,.0f} ac"),
        ("  reservoirs (unscreened)", f"{ac['res']:,.0f} ac"),
        ("Layer 2  (≤10% slope)", ""),
        ("  D/E ≤10% (all tenure)", f"{ac['de10_all']:,.0f} ac"),
        ("    of which military (fee)", f"{ac['milde10_all']:,.0f} ac"),
        (f"  selected B/C ({len(sel)} parcels)", f"{sel_total:,.0f} ac"),
    ]
    tab = "\n".join(f"{k:<30s}{v:>10s}" for k, v in rows)
    ax.text(0.005, 0.015, tab, transform=ax.transAxes, fontsize=7.6,
            family="monospace", color=C_INK, va="bottom", ha="left",
            bbox=dict(boxstyle="round,pad=0.5", fc=SURFACE, ec=ISLAND_EC))

    ax.set_title("Oahu: plausibly available solar land, the modeled subset, "
                 "and transmission", fontsize=12.5, color=C_INK, loc="left",
                 pad=44)
    ax.text(0.0, 1.008,
            "Ag and military categories filtered to ≤15% slope (10 m "
            "DEM); modeled subset to ≤10%. Layer-1 acres draw in one "
            "category (military excluded from the ag D/E\nand B/C fills). "
            "Layer 2's modeled D/E is ALL ag D/E ≤10%, military and non-"
            "military (military shown green + hatch). No grid-distance\n"
            "filter: published near-grid figures are smaller "
            "(notes/available-land-map.md).",
            transform=ax.transAxes, fontsize=7.8, color=C_MUTE, va="bottom")
    # scale bar, lower right
    x0 = ax.get_xlim()[1] - 16000
    y0 = ax.get_ylim()[0] + 3500
    ax.plot([x0, x0 + 10000], [y0, y0], color=C_INK, lw=2, zorder=9)
    ax.text(x0 + 5000, y0 + 800, "10 km", ha="center", fontsize=8,
            color=C_INK)
    ax.set_axis_off()
    fig.tight_layout()
    out = FIGS / "f_available_land.png"
    fig.savefig(out, bbox_inches="tight", facecolor=SURFACE)
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
