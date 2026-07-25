#!/usr/bin/env python3
"""
Map of plausibly-available solar land on Oahu, in two slope bands.

Every slope-filled group has a base fill for <=15% slope and a lighter tint
of the same hue for the 15-30% increment (Mike 2026-07-24). The <=10%
threshold was dropped. Groups:
  D/E ag, ALL tenure: class D/E in the Ag district, military and non-military
    (uncapped, permitted use). This is both the availability envelope and the
    modeling subset (the model assumes all D/E is available). Military hatches
    overlay it, so military D/E reads as fill + hatch.
  B/C ag envelope: class B/C in the Ag district, non-military (SUP above the
    cap). Shown as the full envelope plus the modeled 10% draw on top.
  selected B/C: quasi-random, spatially even 10%-of-B/C draw. 2-km grid +
    per-cell Halton(2,3) anchor points (skip 42), round-robin across cells,
    accumulating each parcel's B/C-on-<=15%-slope acreage until 10% of TOTAL
    Oahu B/C acreage (target ~3,437 of 34,370 ac). Only the <=15% B/C portion
    counts. Output: data/oahu_bc_10pct_selection.csv (Switch-Oahu input).
  military ag / urban fee / ESQD buffer / Kahuku lease parcel: DoD-tenure
    categories (see notes/military-land-solar.md), hatched by direction.
  durable non-ag sites and reservoirs: point markers (no slope shading).
Lines: existing 138 kV (heavy) and 46 kV+ (thin); greedy expansion dashed.

Subtractions keep military land, the Kahuku parcel, and the B/C envelope
mutually exclusive: the ESQD footprint is removed from the military ag and
urban fills; the lease-tenure Kahuku parcel is removed from the B/C envelope
and touches no fee-military category. The all-tenure D/E group deliberately
overlaps the military fills (drawn as fill + hatch), so the D/E and military
acreages must not be summed. No grid-distance filter is applied anywhere;
published near-grid figures (data/gis/oahu_de_neargrid_by_slope.csv) are
smaller.

Slope: cached 10 m band raster data/gis/dem/oahu_slope_bands.tif
(bands 1..7 = 0-5,5-10,10-15,15-20,20-25,25-30,>30%; 0 = nodata).
CRS EPSG:26904 throughout; acres = cells * 100 m^2 / 4046.8564224.

Colors validated with the dataviz palette checker (light surface #fcfcfb):
the four base hues #279e6c (D/E), #e39a3b (B/C envelope), #b85a0a (selected
B/C), #2a78d6 (lines/reservoirs) all-pairs PASS (worst CVD deltaE 8.3 protan;
normal-vision floor 17.6). Each group's 15-30% band is a white-blend tint of
its base (lightness step of the same hue via _lt()), so no new chromatic
hues are added. Military categories are achromatic gray tones distinguished
by hatch direction (//// ag, \\\\ urban, .. ESQD, xx Kahuku); each also
carries a lighter 15-30% gray. Durable sites and reservoirs are markers.

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

# palette (validated; see module docstring). Each slope-banded group uses a
# base color for <=15% slope and a lighter tint (blend toward white) for the
# 15-30% increment; the tint is a lightness step of the same hue.
def _lt(hexc, f=0.55):
    h = hexc.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return "#%02x%02x%02x" % tuple(int(v + (255 - v) * f) for v in (r, g, b))


C_DE = "#279e6c"                          # D/E, base (<=15%)
C_BC_ENV = "#e39a3b"                      # ag B/C envelope, base (<=15%)
C_BC = "#b85a0a"                          # selected B/C, base (<=15%)
C_MIL_FILL, C_MIL_HATCH = "#cdc9c1", "#6b6862"
C_URB_FILL = "#bcbab3"                    # military urban fee (\\\\ hatch)
C_ESQD_FILL = "#ddd9d2"                   # military ESQD buffer (.. hatch)
C_KAH_FILL = "#a9a59d"                    # Kahuku lease parcel (xx hatch)
# 15-30% tints of each base
C_DE_L, C_BC_ENV_L, C_BC_L = _lt(C_DE), _lt(C_BC_ENV), _lt(C_BC)
C_MIL_L, C_URB_L = _lt(C_MIL_FILL), _lt(C_URB_FILL)
C_ESQD_L, C_KAH_L = _lt(C_ESQD_FILL), _lt(C_KAH_FILL)
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


def select_bc_parcels(pg, bc15_ac, bc_all_ac, target_ac):
    """2-km-grid Halton round-robin selection over parcels with B/C on
    <=15% slope. Deterministic: HALTON_SKIP fixes the sequence."""
    elig = pg[bc15_ac > 0].copy()
    elig["bc15_acres"] = bc15_ac[bc15_ac > 0]
    elig["bc_acres"] = bc_all_ac[bc15_ac > 0]
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
            total += elig.loc[idx, "bc15_acres"]
            picked.append({"tmk": elig.loc[idx, "tmk"],
                           "parcel_acres": elig.loc[idx, "parcel_acres"],
                           "bc_acres": round(elig.loc[idx, "bc_acres"], 2),
                           "bc15_acres": round(elig.loc[idx, "bc15_acres"], 2),
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
    le15 = np.isin(band, [1, 2, 3])       # <=15% slope, base band
    b1530 = np.isin(band, [4, 5, 6])      # 15-30% increment, light band

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

    # ---- category masks: base <=15% + light 15-30% band per group -----
    # Two disjoint slope masks per group (Mike 2026-07-24): base color at
    # <=15%, lighter tint at 15-30%. The <=10% threshold is dropped. D/E is
    # one all-tenure group (the modeling assumption is "all D/E available",
    # so the envelope and the modeled subset coincide); military hatches
    # overlay it so military D/E reads as green + hatch. B/C keeps the
    # envelope/selected distinction. Subtractions (ESQD out of military ag
    # and urban; Kahuku out of civilian ag) apply to BOTH bands.
    def bands(base):
        return base & le15, base & b1530

    m_de_15, m_de_30 = bands(is_de)                       # all-tenure D/E
    m_bc_15, m_bc_30 = bands(is_bc & ~milmask & ~kahmask)  # B/C envelope
    m_mil_15, m_mil_30 = bands(milmask & agmask & ~esqdmask)
    m_urb_15, m_urb_30 = bands(milmask & urbmask & ~esqdmask)
    m_esqd_15, m_esqd_30 = bands(esqdmask)
    m_kah_15, m_kah_30 = bands(kahmask)

    ac = {k: v.sum() * CELL_AC for k, v in
          [("de_15", m_de_15), ("de_30", m_de_30),
           ("bc_15", m_bc_15), ("bc_30", m_bc_30),
           ("mil_15", m_mil_15), ("mil_30", m_mil_30),
           ("urb_15", m_urb_15), ("urb_30", m_urb_30),
           ("esqd_15", m_esqd_15), ("esqd_30", m_esqd_30),
           ("kah_15", m_kah_15), ("kah_30", m_kah_30)]}
    # military share of the all-tenure D/E group, per band
    ac["milde_15"] = (is_de & le15 & milmask).sum() * CELL_AC
    ac["milde_30"] = (is_de & b1530 & milmask).sum() * CELL_AC
    # subtraction accounting for the note (<=15% basis)
    ac["esqd_from_urb"] = (milmask & urbmask & le15 & esqdmask).sum() * CELL_AC
    ac["esqd_from_ag"] = (milmask & agmask & le15 & esqdmask).sum() * CELL_AC
    ac["kah_from_de"] = (is_de & le15 & ~milmask & kahmask).sum() * CELL_AC
    ac["kah_from_bc"] = (is_bc & le15 & ~milmask & kahmask).sum() * CELL_AC
    # reconciliation against published class x slope table (incl. military)
    ac["de15_incl_mil"] = (is_de & le15).sum() * CELL_AC
    ac["bc15_incl_mil"] = (is_bc & le15).sum() * CELL_AC
    ac["de30_incl_mil"] = (is_de & (le15 | b1530)).sum() * CELL_AC
    ac["bc30_incl_mil"] = (is_bc & (le15 | b1530)).sum() * CELL_AC

    # ---- parcels + B/C-on-<=15% acreage (selection pool basis) --------
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
    sel_cells = (pid > 0) & is_bc & le15 & ~milmask
    counts = np.bincount(pid[sel_cells], minlength=len(pg) + 1)[1:]
    bc15_ac = pd.Series(counts * CELL_AC, index=pg.index)
    bc_all = pg.b_acres + pg.c_acres

    sel, elig, sel_total = select_bc_parcels(pg, bc15_ac, bc_all, target)
    pool = bc15_ac.sum()
    shortfall = max(0.0, target - sel_total)
    sel.to_csv(DATA / "oahu_bc_10pct_selection.csv", index=False)

    # selected-parcel B/C cells for the fill, split into the two slope bands
    sel_idx = set(pg.index[pg.tmk.isin(set(sel.tmk))] + 1)
    in_sel = np.isin(pid, list(sel_idx))
    m_sel_15 = sel_cells & in_sel                                   # <=15%
    m_sel_30 = (pid > 0) & is_bc & b1530 & ~milmask & in_sel        # 15-30%
    ac["sel_15"] = m_sel_15.sum() * CELL_AC
    ac["sel_30"] = m_sel_30.sum() * CELL_AC

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
    ac["durable_15"] = dur.acres_le15.sum() + golf_closed.acres_le15.sum()
    ac["durable_30"] = (dur.acres_le30.sum() + golf_closed.acres_le30.sum()
                        - ac["durable_15"])
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
    print(f"B/C-on-<=15%-slope pool (non-military parcels): {pool:,.0f} ac "
          f"across {(bc15_ac > 0).sum()} parcels")
    print(f"selected {len(sel)} parcels, {sel_total:,.0f} ac (<=15% basis); "
          f"shortfall {shortfall:,.0f} ac")
    assert "158002002" not in set(sel.tmk), \
        "Kahuku lease parcel entered the B/C selection"
    print("B/C selection check: TMK 158002002 in pool "
          f"{bc15_ac[pg.tmk == '158002002'].sum():,.1f} ac, selected: no")
    print("\nacreage (base <=15% / +15-30% increment):")
    for k, lab in [("de", "D/E (all tenure)"), ("bc", "B/C envelope"),
                   ("sel", "selected B/C"), ("mil", "military ag"),
                   ("urb", "military urban"), ("esqd", "military ESQD"),
                   ("kah", "Kahuku"), ("durable", "durable non-ag")]:
        print(f"  {lab:22s} {ac[k + '_15']:>9,.0f} / +{ac[k + '_30']:>8,.0f}")
    print(f"  {'reservoirs (no slope)':22s} {ac['res']:>9,.0f}")
    print(f"  of D/E, military share:  {ac['milde_15']:,.0f} / "
          f"+{ac['milde_30']:,.0f}")
    print("overlap subtractions (<=15%; stated in notes):")
    print(f"  ESQD out of military urban fill: {ac['esqd_from_urb']:,.0f}")
    print(f"  ESQD out of military ag fill:    {ac['esqd_from_ag']:,.0f}")
    print(f"  Kahuku out of ag D/E / B/C fill: {ac['kah_from_de']:,.0f} / "
          f"{ac['kah_from_bc']:,.0f}")
    print("reconciliation vs data/gis/oahu_lsb_by_slope.csv (incl. military):")
    print(f"  D/E <=15% {ac['de15_incl_mil']:,.0f} (pub 21,391); "
          f"<=30% {ac['de30_incl_mil']:,.0f}")
    print(f"  B/C <=15% {ac['bc15_incl_mil']:,.0f} (pub 30,852); "
          f"<=30% {ac['bc30_incl_mil']:,.0f}")
    print(f"  reservoirs: {len(res)} polygons, {ac['res']:,.0f} ac "
          f"(unscreened)")

    masks = {
        "de_15": m_de_15, "de_30": m_de_30,
        "bc_15": m_bc_15, "bc_30": m_bc_30,
        "sel_15": m_sel_15, "sel_30": m_sel_30,
        "mil_15": m_mil_15, "mil_30": m_mil_30,
        "urb_15": m_urb_15, "urb_30": m_urb_30,
        "esqd_15": m_esqd_15, "esqd_30": m_esqd_30,
        "kah_15": m_kah_15, "kah_30": m_kah_30,
    }
    make_figure(band, tr, slud_o, masks, kah, site_pts, res, lines, exp,
                ac, sel, sel_total)


def make_figure(band, tr, slud_o, masks, kah, site_pts, res, lines, exp,
                ac, sel, sel_total):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.colors import to_rgba
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch

    h, w = band.shape
    extent = (tr.c, tr.c + w * tr.a, tr.f + h * tr.e, tr.f)

    # priority-stacked RGBA overlay (highest priority last). Each group has a
    # base (<=15%) and a lighter tint (15-30%) drawn at the same priority.
    # Order: B/C envelope, then military fills, then all-tenure D/E (covers
    # military-D/E so it reads green under the hatch), then selected B/C.
    img = np.zeros((h, w, 4), dtype=np.float32)
    for mask, color in [(masks["bc_15"], C_BC_ENV), (masks["bc_30"], C_BC_ENV_L),
                        (masks["urb_15"], C_URB_FILL), (masks["urb_30"], C_URB_L),
                        (masks["esqd_15"], C_ESQD_FILL),
                        (masks["esqd_30"], C_ESQD_L),
                        (masks["mil_15"], C_MIL_FILL), (masks["mil_30"], C_MIL_L),
                        (masks["kah_15"], C_KAH_FILL), (masks["kah_30"], C_KAH_L),
                        (masks["de_15"], C_DE), (masks["de_30"], C_DE_L),
                        (masks["sel_15"], C_BC), (masks["sel_30"], C_BC_L)]:
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

    # hatch the union of both slope bands per military group (identity)
    hatch_mask(masks["mil_15"] | masks["mil_30"], "////")
    hatch_mask(masks["urb_15"] | masks["urb_30"], "\\\\\\\\")
    hatch_mask(masks["esqd_15"] | masks["esqd_30"], "..")
    hatch_mask(masks["kah_15"] | masks["kah_30"], "xxxx", alpha=0.7)
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

    from matplotlib.legend_handler import HandlerTuple
    handles = [
        Patch(fc=C_DE, label="D/E ag, all tenure — modeled-available\n"
                             "(uncapped; military shown as fill + hatch)"),
        Patch(fc=C_BC_ENV, label="B/C ag — available via SUP (envelope)"),
        Patch(fc=C_BC, label="B/C modeled subset: quasi-random 10% draw"),
        Patch(fc=C_MIL_FILL, ec=C_MIL_HATCH, hatch="////",
              label="military ag land (DoD discretion)"),
        Patch(fc=C_URB_FILL, ec=C_MIL_HATCH, hatch="\\\\\\\\",
              label="military urban fee land (EUL discretion)"),
        Patch(fc=C_ESQD_FILL, ec=C_MIL_HATCH, hatch="..",
              label="military ESQD buffer (unoccupied-PV-\n"
                    "compatible; Kupono precedent)"),
        Patch(fc=C_KAH_FILL, ec=C_INK, hatch="xxxx", lw=1.2,
              label="Kahuku lease parcel (Army-retained\n2025 ROD)"),
        (Patch(fc=C_DE), Patch(fc=C_DE_L)),
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
    labels = [h.get_label() if isinstance(h, Patch) or isinstance(h, Line2D)
              else "each fill: darker ≤15% / lighter 15–30% slope"
              for h in handles]
    leg = ax.legend(handles=handles, labels=labels, loc="upper right",
                    fontsize=7.6, frameon=True, framealpha=0.95,
                    edgecolor=ISLAND_EC, borderpad=0.9, labelspacing=0.55,
                    handler_map={tuple: HandlerTuple(ndivide=None, pad=0.0)})
    leg.get_frame().set_facecolor(SURFACE)

    # acreage table: base <=15% and the +15-30% increment, two columns
    def f0(v):
        return "—" if v is None else f"{v:,.0f}"

    rows = [
        ("Available land", "≤15%", "15–30%"),
        ("  D/E ag, all tenure *", f0(ac["de_15"]), f0(ac["de_30"])),
        ("    of which military", f0(ac["milde_15"]), f0(ac["milde_30"])),
        ("  B/C ag (SUP envelope)", f0(ac["bc_15"]), f0(ac["bc_30"])),
        ("  military ag", f0(ac["mil_15"]), f0(ac["mil_30"])),
        ("  military urban fee", f0(ac["urb_15"]), f0(ac["urb_30"])),
        ("  military ESQD buffer", f0(ac["esqd_15"]), f0(ac["esqd_30"])),
        ("  Kahuku lease parcel", f0(ac["kah_15"]), f0(ac["kah_30"])),
        ("  durable non-ag sites", f0(ac["durable_15"]), f0(ac["durable_30"])),
        ("  reservoirs (no slope)", f0(ac["res"]), "—"),
        ("Modeled subset", "", ""),
        ("  all D/E (= * above)", f0(ac["de_15"]), f0(ac["de_30"])),
        (f"  selected B/C ({len(sel)} par.)", f0(sel_total), f0(ac["sel_30"])),
    ]
    tab = "\n".join(f"{k:<26s}{a:>8s}{b:>9s}" for k, a, b in rows)
    ax.text(0.005, 0.015, tab, transform=ax.transAxes, fontsize=7.4,
            family="monospace", color=C_INK, va="bottom", ha="left",
            bbox=dict(boxstyle="round,pad=0.5", fc=SURFACE, ec=ISLAND_EC))

    ax.set_title("Oahu: plausibly available solar land, the modeled subset, "
                 "and transmission", fontsize=12.5, color=C_INK, loc="left",
                 pad=44)
    ax.text(0.0, 1.008,
            "Each fill has two shades: darker = ≤15% slope, lighter = the "
            "15–30% increment (10 m DEM). D/E ag is one all-tenure group "
            "(the\nmodeling assumes all D/E is available; military shown as "
            "fill + hatch); B/C shows the full SUP envelope plus the modeled "
            "10% draw.\nNo grid-distance filter: published near-grid figures "
            "are smaller (notes/available-land-map.md).",
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
