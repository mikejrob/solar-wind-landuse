#!/usr/bin/env python3
"""
Budget-constrained transmission-expansion heuristic for Oahu.

Question: given L km of NEW line (branching off the existing mapped 46 kV+
network or off previously built expansion), where should it go to MAXIMIZE
the acreage of class B, C, and D agricultural-district land (class A
excluded: solar banned; class E excluded per spec) brought within 1 km of a
line, counting only land passing the <=30% slope screen (<=15% variant also
recorded)?

Method (GREEDY HEURISTIC -- an approximation, not an optimum):
 1. Eligibility raster at 10 m (LSB class in {B,C,D} within the ag district,
    slope band <=30% resp. <=15%), aggregated to eligible-acres per 100 m
    cell. Network growth happens on the 100 m lattice.
 2. Coverage = 100 m cells within 1 km (10-cell disk) of any network cell
    (existing mapped 46kV+ lines rasterized, plus built expansion).
    Baseline = coverage of the existing mapped network (L = 0).
 3. Greedy growth. Each iteration:
      a. G(q) = uncovered eligible acres inside the 1 km disk at q
         (FFT convolution) -- the payoff of reaching cell q.
      b. Multi-source Dijkstra from every network cell over the land grid
         (8-connected; moving into a cell whose 10 m subcells are >30%
         slope in >30% of area costs 6x its geometric length -- lines can
         cross steep ground but the router avoids it when it can).
      c. Score candidates by exact new-coverage-per-km of their full
         slope-aware shortest path (disk stamped along the path), for the
         top ~15 approximate scorers (spatially de-duplicated).
      d. Commit the best path in a <=1.0 km increment (so long approach
         runs to far clusters appear as several low-gain steps followed
         by a jump when the cluster comes into range).
    Repeat to ~112 km. Marginal gain is mostly non-increasing except at
    those approach-then-jump events.
 4. Knee = end of the committed segment at the maximum of the 5-step
    (~5 km) centered moving average of marginal acres/km, i.e. the best
    sustained single-segment payoff on the curve.

CAVEATS (repeat these wherever results are used):
 - Geometric routing only: line capacities, substation headroom, and
   interconnection engineering are unknown and ignored.
 - The public 46 kV map (HIFLD + OSM) is incomplete, so baseline coverage
   is UNDERSTATED and some "expansion" may duplicate real unmapped lines.
 - Greedy is approximate; the 1-km service radius is a simplification of
   interconnection cost, not a tariff rule.
 - Coverage is evaluated on the 100 m lattice (cell-center within 1 km of a
   network cell), so acreages differ slightly (<~1%) from the 10 m
   polygon-buffer numbers in slope_screen.py.

Outputs:
  data/gis/expansion_curve.csv            step log (cum_km, acres, WKT)
  data/gis/expansion_segments.parquet     committed segments (geometry)
  analysis/figs/paper/f_expansion_curve.png
  analysis/figs/paper/f_expansion_map.png
"""

import heapq  # noqa: F401  (kept for the pure-python fallback path)
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
from rasterio import features
from scipy.signal import fftconvolve
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import dijkstra
from shapely.geometry import LineString

PROJECT = Path("/Users/michaelroberts/Research/solar-wind-landuse")
DATA, GIS = PROJECT / "data", PROJECT / "data" / "gis"
FIGS = PROJECT / "analysis" / "figs"
CRS = "EPSG:26904"
M2_PER_ACRE = 4046.8564224
CELL10_AC = 100.0 / M2_PER_ACRE          # one 10 m cell in acres
RES = 100.0                               # working lattice (m)
AGG = 10                                  # 10 m cells per 100 m cell edge
RADIUS_CELLS = 10                         # 1 km service radius on lattice
STEP_KM = 1.0                             # max committed length per step
BUDGET_KM = 112.0
SLOPE_PENALTY = 6.0                       # cost multiplier through steep cells
STEEP_FRAC = 0.30                         # cell "steep" if >30% of it is >30% slope
TOP_K = 15                                # candidates exactly scored per iter
CLS_CODE = {c: i + 1 for i, c in enumerate("ABCDE")}
L_MARKS = [10, 25, 50, 75, 100]

# palette (validated set from transmission_screen.py / slope_screen.py)
SURF, INK, MUT = "#fcfcfb", "#0b0b0b", "#52514e"
C_138, C_46, C_EXP, C_NEW = "#4a3aa7", "#2a78d6", "#d55181", "#1baf7a"


# ------------------------------------------------------------ raster build

def build_grids():
    """Return (elig30_ac, elig15_ac, steep_frac, land, net0, transform100)."""
    with rasterio.open(GIS / "dem" / "oahu_slope_bands.tif") as src:
        band = src.read(1)
        tr10 = src.transform
    H = (band.shape[0] // AGG) * AGG
    W = (band.shape[1] // AGG) * AGG
    band = band[:H, :W]
    shape10 = (H, W)

    lsb = gpd.read_parquet(GIS / "lsb_ag.parquet")
    lsb = lsb[lsb.island == "Oahu"]
    cls = features.rasterize(
        zip(lsb.geometry, lsb["type"].map(CLS_CODE)),
        out_shape=shape10, transform=tr10, fill=0, dtype="uint8")

    bcd = np.isin(cls, [CLS_CODE["B"], CLS_CODE["C"], CLS_CODE["D"]])
    e30 = bcd & (band >= 1) & (band <= 6)     # slope <=30%
    e15 = bcd & (band >= 1) & (band <= 3)     # slope <=15%
    steep10 = band == 7

    def agg_sum(a):
        return a.reshape(H // AGG, AGG, W // AGG, AGG).sum(axis=(1, 3))

    elig30_ac = agg_sum(e30).astype(np.float64) * CELL10_AC
    elig15_ac = agg_sum(e15).astype(np.float64) * CELL10_AC
    steep_frac = agg_sum(steep10).astype(np.float64) / (AGG * AGG)

    tr100 = rasterio.transform.Affine(RES, 0, tr10.c, 0, -RES, tr10.f)
    shape100 = (H // AGG, W // AGG)

    slud = gpd.read_parquet(GIS / "slud.parquet").to_crs(CRS)
    land = features.rasterize(
        zip(slud[slud.island == "Oahu"].geometry,
            np.ones((slud.island == "Oahu").sum(), dtype=np.uint8)),
        out_shape=shape100, transform=tr100, fill=0, dtype="uint8",
        all_touched=True).astype(bool)

    lines = gpd.read_parquet(GIS / "oahu_lines_classified.parquet")
    net0 = features.rasterize(
        zip(lines.geometry, np.ones(len(lines), dtype=np.uint8)),
        out_shape=shape100, transform=tr100, fill=0, dtype="uint8",
        all_touched=True).astype(bool)
    net0 &= land  # a few offshore artifacts
    return elig30_ac, elig15_ac, steep_frac, land, net0, tr100


def disk(r):
    y, x = np.ogrid[-r:r + 1, -r:r + 1]
    return (x * x + y * y) <= r * r


def cover(mask, k):
    """Cells within the disk kernel k of any True cell in mask."""
    return fftconvolve(mask.astype(np.float32), k.astype(np.float32),
                       mode="same") > 0.5


# ------------------------------------------------------------ graph

def build_graph(land, steep_frac):
    """Static 8-connected sparse graph over land cells.

    Edge weight into cell v = geometric length * (SLOPE_PENALTY if v steep).
    Also returns per-edge geometric length is implicit (recomputed on path).
    """
    H, W = land.shape
    idx = np.arange(H * W).reshape(H, W)
    rows, cols, wts = [], [], []
    for di, dj in [(0, 1), (1, 0), (1, 1), (1, -1)]:
        step = RES * (2 ** 0.5 if di and dj else 1.0)
        if dj >= 0:
            a = idx[:H - di or H, :W - dj or W]
            b = idx[di:, dj:]
            ok = land[:H - di or H, :W - dj or W] & land[di:, dj:]
            pen_b = steep_frac[di:, dj:] > STEEP_FRAC
            pen_a = steep_frac[:H - di or H, :W - dj or W] > STEEP_FRAC
        else:  # dj == -1
            a = idx[:H - di, -dj:]
            b = idx[di:, :W + dj]
            ok = land[:H - di, -dj:] & land[di:, :W + dj]
            pen_b = steep_frac[di:, :W + dj] > STEEP_FRAC
            pen_a = steep_frac[:H - di, -dj:] > STEEP_FRAC
        a, b = a[ok], b[ok]
        wab = step * np.where(pen_b[ok], SLOPE_PENALTY, 1.0)
        wba = step * np.where(pen_a[ok], SLOPE_PENALTY, 1.0)
        rows += [a, b]
        cols += [b, a]
        wts += [wab, wba]
    rows = np.concatenate(rows)
    cols = np.concatenate(cols)
    wts = np.concatenate(wts)
    n = H * W
    return coo_matrix((wts, (rows, cols)), shape=(n, n)).tocsr()


def reconstruct(pred, node):
    path = [node]
    while pred[path[-1]] >= 0:
        path.append(pred[path[-1]])
    return path[::-1]  # network cell first


def path_len_km(path, W):
    ii, jj = np.divmod(np.asarray(path), W)
    return float(np.hypot(np.diff(ii), np.diff(jj)).sum() * RES / 1000.0)


# ------------------------------------------------------------ greedy

def run_greedy(elig30, elig15, steep_frac, land, net0, tr100):
    H, W = land.shape
    k = disk(RADIUS_CELLS)
    koff = np.argwhere(k) - RADIUS_CELLS          # disk offsets
    graph = build_graph(land, steep_frac)

    net = net0.copy()
    covered = cover(net, k)
    base30 = float(elig30[covered].sum())
    base15 = float(elig15[covered].sum())
    print(f"baseline: {base30:,.0f} ac (<=30%), {base15:,.0f} ac (<=15%) "
          f"within 1 km of the mapped 46kV+ network")

    def stamp(cells_ij, cov):
        """Return newly-covered mask from disks at cells_ij (n,2)."""
        new = np.zeros_like(cov)
        pts = (cells_ij[:, None, :] + koff[None, :, :]).reshape(-1, 2)
        ok = ((pts[:, 0] >= 0) & (pts[:, 0] < H)
              & (pts[:, 1] >= 0) & (pts[:, 1] < W))
        pts = pts[ok]
        new[pts[:, 0], pts[:, 1]] = True
        return new & ~cov

    rows = [dict(step=0, seg_km=0.0, cum_km=0.0, cum_acres_le30=base30,
                 cum_acres_le15=base15, marginal_ac_per_km=np.nan,
                 segment_wkt="")]
    seg_geoms = []
    cum_km, step = 0.0, 0
    x0, y0 = tr100.c, tr100.f  # raster origin

    while cum_km < BUDGET_KM:
        step += 1
        U = np.where(covered, 0.0, elig30)
        G = fftconvolve(U, k.astype(np.float32), mode="same")
        G[~land] = 0.0

        src_nodes = np.flatnonzero(net.ravel())
        dist, pred, _src = dijkstra(graph, indices=src_nodes, min_only=True,
                                    return_predecessors=True)
        dflat = dist
        gflat = G.ravel()
        score = gflat / np.maximum(dflat, 500.0)
        score[~np.isfinite(dflat) | (dflat < RES)] = 0.0

        # top-K approximate candidates, >=1 km apart
        order = np.argsort(score)[::-1]
        cands, taken = [], []
        for node in order[:4000]:
            if score[node] <= 0:
                break
            i, j = divmod(int(node), W)
            if any((i - ti) ** 2 + (j - tj) ** 2 < RADIUS_CELLS ** 2
                   for ti, tj in taken):
                continue
            cands.append(int(node))
            taken.append((i, j))
            if len(cands) >= TOP_K:
                break
        if not cands:
            print("no positive-gain candidate left; stopping")
            break

        # exact score: new acres of the full path tube / geometric km
        best = None
        for node in cands:
            path = reconstruct(pred, node)
            ij = np.column_stack(divmod(np.asarray(path), W))
            newmask = stamp(ij, covered)
            gain = float(elig30[newmask].sum())
            km = path_len_km(path, W)
            if km <= 0:
                continue
            if best is None or gain / km > best[0]:
                best = (gain / km, path, km)
        _, path, full_km = best

        # commit at most STEP_KM along the path (network end first)
        ii, jj = np.divmod(np.asarray(path), W)
        seg_len = np.hypot(np.diff(ii), np.diff(jj)) * RES / 1000.0
        cum = np.concatenate([[0.0], np.cumsum(seg_len)])
        take = int(np.searchsorted(cum, min(STEP_KM, cum[-1]), side="left"))
        take = max(take, 1)
        commit = path[:take + 1]
        seg_km = float(cum[take])

        cij = np.column_stack(divmod(np.asarray(commit), W))
        newmask = stamp(cij, covered)
        covered |= newmask
        net.ravel()[commit] = True
        gained30 = float(elig30[newmask].sum())
        cum_km += seg_km

        xs = x0 + (cij[:, 1] + 0.5) * RES
        ys = y0 - (cij[:, 0] + 0.5) * RES
        geom = LineString(np.column_stack([xs, ys])).simplify(50)
        seg_geoms.append(geom)
        rows.append(dict(
            step=step, seg_km=round(seg_km, 3), cum_km=round(cum_km, 3),
            cum_acres_le30=round(rows[-1]["cum_acres_le30"] + gained30, 1),
            cum_acres_le15=round(rows[-1]["cum_acres_le15"]
                                 + float(elig15[newmask].sum()), 1),
            marginal_ac_per_km=round(gained30 / seg_km, 1),
            segment_wkt=geom.wkt))
        if step % 10 == 0:
            print(f"  step {step:3d}  cum {cum_km:6.1f} km  "
                  f"{rows[-1]['cum_acres_le30']:9,.0f} ac  "
                  f"(+{gained30 / seg_km:6.0f} ac/km)")

    curve = pd.DataFrame(rows)
    # knee: max of ~5-step centered moving average of marginal ac/km
    marg = curve.marginal_ac_per_km.iloc[1:]
    sm = marg.rolling(5, center=True, min_periods=2).mean()
    kidx = sm.idxmax()
    curve["smoothed_ac_per_km"] = np.nan
    curve.loc[sm.index, "smoothed_ac_per_km"] = sm.round(1)
    knee_km = float(curve.loc[kidx, "cum_km"])
    knee_ac = float(curve.loc[kidx, "cum_acres_le30"])
    print(f"knee: {knee_km:.1f} km, {knee_ac:,.0f} ac "
          f"(smoothed marginal {sm.max():,.0f} ac/km)")

    curve.to_csv(GIS / "expansion_curve.csv", index=False)
    print(f"wrote {GIS / 'expansion_curve.csv'} ({len(curve) - 1} steps)")
    segs = gpd.GeoDataFrame(
        {"step": curve.step.iloc[1:].values}, geometry=seg_geoms, crs=CRS)
    segs.to_parquet(GIS / "expansion_segments.parquet")
    return curve, segs, (knee_km, knee_ac, kidx), covered, net


# ------------------------------------------------------------ figures

def interp(curve, L):
    return float(np.interp(L, curve.cum_km, curve.cum_acres_le30))


def fig_curve(curve, knee):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    knee_km, knee_ac, kidx = knee
    fig, ax = plt.subplots(figsize=(9.5, 5.8), dpi=160)
    fig.patch.set_facecolor(SURF)
    ax.set_facecolor(SURF)

    ax.plot(curve.cum_km, curve.cum_acres_le15, color=C_NEW, lw=2,
            solid_capstyle="round", zorder=3)
    ax.plot(curve.cum_km, curve.cum_acres_le30, color=C_46, lw=2.4,
            solid_capstyle="round", zorder=4)
    # direct series labels (single-hue lines, labeled at the right end)
    xe = curve.cum_km.iloc[-1]
    ax.annotate("slope ≤30% (headline)",
                (xe, curve.cum_acres_le30.iloc[-1]), xytext=(6, 2),
                textcoords="offset points", fontsize=9.5, color=C_46,
                va="center", fontweight="bold")
    ax.annotate("slope ≤15%", (xe, curve.cum_acres_le15.iloc[-1]),
                xytext=(6, -2), textcoords="offset points", fontsize=9.5,
                color=C_NEW, va="center", fontweight="bold")

    base = curve.cum_acres_le30.iloc[0]
    ax.axhline(base, color="#c9c7c1", lw=1, ls=(0, (4, 3)), zorder=1)
    ax.annotate(f"baseline (mapped 46 kV+ network): {base:,.0f} ac",
                (xe * 0.55, base), xytext=(0, -12),
                textcoords="offset points", fontsize=8.5, color=MUT,
                ha="center")

    for L in L_MARKS:
        y = interp(curve, L)
        ax.plot([L], [y], "o", ms=6, mfc="white", mec=C_46, mew=1.6,
                zorder=5)
        dx, dy, ha = (0, -30, "center") if L > 10 else (10, -24, "left")
        ax.annotate(f"L={L}\n{y:,.0f} ac", (L, y), xytext=(dx, dy),
                    textcoords="offset points", ha=ha, fontsize=8,
                    color=MUT)

    ax.plot([knee_km], [knee_ac], "D", ms=7, color=C_EXP, zorder=6)
    sm_pk = curve.smoothed_ac_per_km.max()
    ax.annotate(f"knee ≈ {knee_km:.0f} km, {knee_ac:,.0f} ac\n(peak "
                f"smoothed marginal, {sm_pk:,.0f} ac/km;\npayoff plateau "
                f"of ~400 ac/km runs to ~11 km)",
                (knee_km, knee_ac), xytext=(2.0, 30900),
                textcoords="data", ha="left", va="bottom", fontsize=9,
                color=C_EXP, fontweight="bold",
                arrowprops=dict(arrowstyle="-", color=C_EXP, lw=1,
                                shrinkB=5))

    # the one big mid-curve jump (long approach finally reaches Waiawa)
    j = curve[(curve.cum_km > 30) & (curve.cum_km < 45)]
    if len(j):
        jr = j.loc[j.marginal_ac_per_km.idxmax()]
        ax.annotate("local jump: approach segments\nreach the Waiawa "
                    "cluster", (jr.cum_km, jr.cum_acres_le30),
                    xytext=(20, -62), textcoords="offset points",
                    fontsize=8, color=MUT,
                    arrowprops=dict(arrowstyle="-", color="#c9c7c1", lw=1))

    ymin = 12000
    ax.set_xlim(0, xe + 20)
    ax.set_ylim(ymin, curve.cum_acres_le30.iloc[-1] * 1.06)
    ax.set_xlabel("km of new line (greedy build-out)", fontsize=10,
                  color=MUT)
    ax.set_ylabel("B–D ag-district acres within 1 km of a line",
                  fontsize=10, color=MUT)
    fig.suptitle("Coverage of solar-eligible ag land vs new-line budget, "
                 "Oahu", fontsize=12.5, color=INK, x=0.065, ha="left",
                 y=0.985)
    fig.text(0.065, 0.925,
             "Greedy heuristic; geometric routes only (no capacity or "
             "substation data); mapped 46 kV network is incomplete, so the "
             "baseline is understated. Y-axis starts at 12,000 ac.",
             fontsize=8, color=MUT)
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color("#d8d6d0")
    ax.tick_params(colors=MUT, labelsize=8.5)
    ax.grid(axis="y", color="#eceae6", linewidth=0.8)
    ax.set_axisbelow(True)
    fig.tight_layout(rect=(0, 0, 1, 0.90))
    out = FIGS / "paper" / "f_expansion_curve.png"
    fig.savefig(out, bbox_inches="tight", facecolor=SURF)
    print(f"wrote {out}")


def fig_map(curve, segs, knee, elig30, net0, tr100):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch

    knee_km, knee_ac, kidx = knee
    kstep = int(curve.loc[kidx, "step"])
    k = disk(RADIUS_CELLS)
    cov0 = cover(net0, k)
    seg_knee = segs[segs.step <= kstep]
    seg_rest = segs[segs.step > kstep]
    H, W = net0.shape
    segras = features.rasterize(
        zip(seg_knee.geometry, np.ones(len(seg_knee), dtype=np.uint8)),
        out_shape=(H, W), transform=tr100, fill=0, dtype="uint8",
        all_touched=True).astype(bool)
    covk = cover(net0 | segras, k)
    newly = (elig30 > 0) & covk & ~cov0

    fig, ax = plt.subplots(figsize=(11, 9), dpi=160)
    fig.patch.set_facecolor(SURF)
    ax.set_facecolor(SURF)
    slud = gpd.read_parquet(GIS / "slud.parquet").to_crs(CRS)
    oahu = slud[slud.island == "Oahu"]
    oahu.plot(ax=ax, color="#f0efec", edgecolor="#d8d6d0", linewidth=0.4)
    oahu[oahu.ludcode == "A"].plot(ax=ax, color="#e7f2e9", edgecolor="none")

    # newly covered eligible land at the knee
    x0, y0 = tr100.c, tr100.f
    extent = (x0, x0 + W * RES, y0 - H * RES, y0)
    from matplotlib.colors import ListedColormap
    show = np.where(newly, 1.0, np.nan)
    ax.imshow(show, extent=extent, origin="upper",
              cmap=ListedColormap([C_NEW]), alpha=0.75, zorder=2,
              interpolation="nearest")

    lines = gpd.read_parquet(GIS / "oahu_lines_classified.parquet")
    lines[lines.kv != "138"].plot(ax=ax, color=C_46, linewidth=0.9, zorder=3)
    lines[lines.kv == "138"].plot(ax=ax, color=C_138, linewidth=1.7,
                                  zorder=3)
    if len(seg_rest):
        seg_rest.plot(ax=ax, color=C_EXP, linewidth=1.1, alpha=0.35,
                      linestyle=(0, (3, 2)), zorder=4)
    seg_knee.plot(ax=ax, color=C_EXP, linewidth=2.8, zorder=5,
                  capstyle="round")
    # name the knee spurs
    for name, lon, lat in [("Kahuku", -157.935, 21.685),
                           ("Waialua", -158.075, 21.555),
                           ("Kunia /\ncentral plateau", -158.095, 21.465)]:
        p = gpd.GeoSeries.from_xy([lon], [lat], crs=4326).to_crs(CRS).iloc[0]
        ax.annotate(name, (p.x, p.y), fontsize=9, color=INK, ha="right",
                    fontstyle="italic",
                    bbox=dict(boxstyle="round,pad=0.2", fc="white",
                              ec="#d8d6d0", lw=0.6, alpha=0.9))

    handles = [
        Line2D([], [], color=C_138, lw=1.7, label="138 kV (mapped)"),
        Line2D([], [], color=C_46, lw=0.9,
               label="46 kV / sub-transmission (mapped)"),
        Line2D([], [], color=C_EXP, lw=2.8,
               label=f"greedy expansion, first {knee_km:.0f} km (knee)"),
        Line2D([], [], color=C_EXP, lw=1.1, alpha=0.5, ls=(0, (3, 2)),
               label=f"remainder of greedy build-out (to "
                     f"{curve.cum_km.iloc[-1]:.0f} km)"),
        Patch(fc=C_NEW, alpha=0.75,
              label="B–D land ≤30% slope newly within 1 km at the knee"),
        Patch(fc="#e7f2e9", label="ag district"),
    ]
    ax.legend(handles=handles, loc="lower left", fontsize=8.5, frameon=True,
              framealpha=0.95, edgecolor="#d8d6d0")
    ax.set_title(f"Greedy transmission expansion at the knee budget "
                 f"(≈{knee_km:.0f} km): +"
                 f"{knee_ac - curve.cum_acres_le30.iloc[0]:,.0f} eligible "
                 f"acres", fontsize=12, color=INK)
    ax.text(0.01, 0.985,
            "Routes are geometric (no capacity/substation data); the public "
            "46 kV map is incomplete, so some\nexpansion may duplicate real "
            "unmapped lines. Greedy heuristic, 1 km service radius.",
            transform=ax.transAxes, fontsize=8, color=MUT, va="top")
    xr, yr = ax.get_xlim()[1] - 15000, ax.get_ylim()[0] + 3500
    ax.plot([xr, xr + 10000], [yr, yr], color=INK, lw=2)
    ax.text(xr + 5000, yr + 700, "10 km", ha="center", fontsize=8, color=INK)
    ax.set_axis_off()
    fig.tight_layout()
    out = FIGS / "paper" / "f_expansion_map.png"
    fig.savefig(out, bbox_inches="tight", facecolor=SURF)
    print(f"wrote {out}")


def main(figs_only=False):
    (FIGS / "paper").mkdir(parents=True, exist_ok=True)
    elig30, elig15, steep_frac, land, net0, tr100 = build_grids()
    print(f"grid {land.shape}, eligible<=30%: {elig30.sum():,.0f} ac, "
          f"<=15%: {elig15.sum():,.0f} ac (B-D, ag district)")
    if figs_only and (GIS / "expansion_curve.csv").exists():
        curve = pd.read_csv(GIS / "expansion_curve.csv")
        segs = gpd.read_parquet(GIS / "expansion_segments.parquet")
        kidx = curve.smoothed_ac_per_km.idxmax()
        knee = (float(curve.loc[kidx, "cum_km"]),
                float(curve.loc[kidx, "cum_acres_le30"]), kidx)
    else:
        curve, segs, knee, covered, net = run_greedy(
            elig30, elig15, steep_frac, land, net0, tr100)
    for L in L_MARKS:
        print(f"  L={L:3d} km -> {interp(curve, L):9,.0f} ac (<=30%)")
    fig_curve(curve, knee)
    fig_map(curve, segs, knee, elig30, net0, tr100)


if __name__ == "__main__":
    import sys
    main(figs_only=len(sys.argv) > 1 and sys.argv[1] == "figs")
