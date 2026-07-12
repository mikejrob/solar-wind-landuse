#!/usr/bin/env python3
"""
Oahu north->south bulk-delivery screenline analysis.

Question (Mike, 2026-07): Oahu's load is concentrated in the south (Pearl
Harbor-downtown-east); historic generation is the southwest coast (Kahe,
Waiau, Campbell Industrial Park). Future utility-scale solar sits central/
north (Kunia, Waialua, Wahiawa, Kahuku). Is the N->S corridor capacity
anywhere near what 1-4 GW of northern solar (with co-located storage)
requires, and what would closing the gap cost?

Method:
 1. Three east-west screenlines (defined in lon/lat, cut in EPSG:26904):
      SL-A  Waipahu-Pearl City-Aiea band: central plateau vs Pearl Harbor
            load pocket (Waianae crest to Koolau crest).
      SL-B  between Wahiawa and Waipio (mid-plateau cut).
      SL-C  North Shore neck: Waialua/Kahuku vs Wahiawa (coast to coast).
    For each: geometric circuit crossings by voltage class from the
    HIFLD+OSM classified line layer (oahu_lines_classified.parquet), with
    HIFLD SUB_1/SUB_2 names and OSM tags. Crossing points are clustered
    (<=500 m along the screenline) into CORRIDORS; per corridor the circuit
    count is max(HIFLD features, OSM ways weighted by circuits= tag).
    Features crossing an EVEN number of times (the Kahe-Halawa / Kahe-Waiau
    circuits loop up through the Waipio/Kunia bench and back) are pass-
    throughs w.r.t. net N->S flow UNLESS tapped north of the line; both a
    parity-based (conservative) and a geometric (central) count are kept.
 2. Capacity guesses per crossing: 138 kV single circuit 150-250 MVA,
    46 kV 30-60 MVA (planning-typical ACSR thermal ratings, ambient-
    derated; HECO actual ratings are confidential -> educated guesses).
 3. Requirement model (transparent scenario grid): northern solar S,
    co-located storage power rho*S (4-6 h), southern load share sigma,
    Oahu peak load L. Evening: corridor must carry
    min(sigma*L - G_south_firm, rho*S). Midday: S - rho*S - northern load,
    capped by southern absorption. Requirement = max of the two; N-1 adds
    the largest single circuit (250 MVA).
 4. Upgrade options and planning-level costs for the binding cuts.

Outputs:
  data/gis/screenline_analysis.csv        per-screenline counts + capacity
  data/gis/screenline_requirements.csv    full scenario grid (tidy, for R)
  analysis/figs/paper/f_screenlines.png   map
All ratings and costs are ASSUMPTIONS (docs/ASSUMPTIONS.md conventions),
not HECO data.
"""

import json
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
from shapely.geometry import LineString, Point

PROJECT = Path("/Users/michaelroberts/Research/solar-wind-landuse")
GIS = PROJECT / "data" / "gis"
FIGS = PROJECT / "analysis" / "figs" / "paper"
CRS = "EPSG:26904"

# ---------------- screenlines (lon/lat; drawn ridge-to-ridge) ------------
SCREENLINES = {
    "SL-A": {
        "desc": ("Waipahu-Pearl City-Aiea band: central plateau vs Pearl "
                 "Harbor load pocket (Waianae crest to Koolau crest)"),
        "coords": [(-158.11, 21.405), (-157.87, 21.425)],
    },
    "SL-B": {
        "desc": "Mid-plateau cut between Wahiawa and Waipio",
        "coords": [(-158.16, 21.455), (-157.93, 21.47)],
    },
    "SL-C": {
        "desc": ("North Shore neck: Waialua/Kahuku vs Wahiawa "
                 "(leeward coast to windward coast)"),
        "coords": [(-158.23, 21.545), (-157.84, 21.545)],
    },
}
CLUSTER_GAP_M = 500.0

# ---------------- capacity guesses (ASSUMPTIONS, not HECO data) ----------
RATE_138 = (150.0, 200.0, 250.0)   # MVA per circuit: low / central / high
RATE_46 = (30.0, 45.0, 60.0)
# N-1: largest single circuit crossing each cut today (138 kV at A/B,
# 46 kV at C; a post-upgrade C would be 250 as well)
LARGEST_CKT_MVA = {"SL-A": 250.0, "SL-B": 250.0, "SL-C": 60.0}

# ---------------- requirement-model parameter grid -----------------------
S_GW = [1.0, 2.0, 3.0, 4.0]        # installed northern/central solar
RHO = [0.5, 0.75, 1.0]             # storage power as share of S (4-6 h)
L_PEAK_GW = [1.2, 1.75, 2.0]       # Oahu peak: today / mid / 2045 electrif.
SIGMA = [0.70, 0.775, 0.85]        # southern share of load
G_SOUTH_MW = [0.0, 400.0]          # southern firm gen at evening peak
MID_LOAD_FRAC = 0.85               # midday load / peak load (assumption)
# share of the northern portfolio sitting north of each cut (illustrative
# split: Kunia ~50% [north of A only], Wahiawa ~25% [north of B],
# Waialua+Kahuku ~25% [north of C]) -- ASSUMPTION
F_SHARE = {"SL-A": 1.00, "SL-B": 0.50, "SL-C": 0.25}
# load sitting NORTH of each cut, as a fraction of island load: north of A
# it is (1 - sigma) by construction; north of B (Wahiawa/North Shore) and
# north of C (Waialua/Kahuku) it is small -- population-share ASSUMPTION
LOADN_FRAC = {"SL-B": 0.05, "SL-C": 0.025}


def load_lines():
    h = gpd.read_file(GIS / "hifld_lines_oahu.geojson").to_crs(CRS)
    h["kv"] = np.where((h.VOLTAGE == 138) | (h.VOLT_CLASS == "100-161"),
                       "138", "46plus")
    h["label"] = h.SUB_1.astype(str) + " - " + h.SUB_2.astype(str)
    h["src"], h["ckt_w"] = "HIFLD", 1.0
    d = json.load(open(GIS / "osm_power_oahu.json"))
    rows = []
    for w in d["elements"]:
        t = w["tags"]
        rows.append({
            "kv": {"138000": "138"}.get(t.get("voltage"), "46plus"),
            "label": t.get("name") or f"osm:{w.get('id', '?')}",
            "src": "OSM",
            "ckt_w": float(t.get("circuits", 1) or 1),
            "geometry": LineString([(p["lon"], p["lat"])
                                    for p in w["geometry"]])})
    o = gpd.GeoDataFrame(rows, crs="EPSG:4326").to_crs(CRS)
    cols = ["kv", "label", "src", "ckt_w", "geometry"]
    return gpd.GeoDataFrame(pd.concat([h[cols], o[cols]], ignore_index=True),
                            crs=CRS)


def crossings_for(sl_geom, lines):
    """All geometric crossing points of line features with one screenline."""
    rows = []
    for i, r in lines.iterrows():
        inter = r.geometry.intersection(sl_geom)
        if inter.is_empty:
            continue
        pts = []
        for g in getattr(inter, "geoms", [inter]):
            if g.geom_type == "Point":
                pts.append(g)
            elif g.geom_type == "LineString":     # collinear overlap: rare
                pts.append(Point(g.coords[0]))
        for p in pts:
            rows.append({"fid": i, "kv": r.kv, "src": r.src,
                         "label": r.label, "ckt_w": r.ckt_w,
                         "s_along": sl_geom.project(p),
                         "n_cross_feat": len(pts), "x": p.x, "y": p.y})
    return pd.DataFrame(rows)


def cluster_corridors(cr):
    """Cluster crossing points along the screenline into corridors."""
    cr = cr.sort_values("s_along").copy()
    cid, last = 0, None
    ids = []
    for s in cr.s_along:
        if last is not None and s - last > CLUSTER_GAP_M:
            cid += 1
        ids.append(cid)
        last = s
    cr["corridor"] = ids
    return cr


def count_screenline(cr):
    """Per kv-class: corridors, geometric circuit crossings, parity-net."""
    out = {}
    for kv in ["138", "46plus"]:
        c = cr[cr.kv == kv]
        if c.empty:
            out[kv] = dict(n_corr=0, n_circ_geo=0, n_net_odd=0, detail="")
            continue
        n_corr = c.corridor.nunique()
        # per corridor: best-informed source count (OSM weighted by
        # circuits= tag); a corridor mapped by both sources is NOT summed;
        # a feature crossing the SAME cluster an even number of times is a
        # local wiggle, not an extra circuit (mod-2 collapse)
        n_circ = 0
        details = []
        for _, grp in c.groupby("corridor"):
            per_feat = grp.groupby(["src", "fid"]).agg(
                n=("fid", "size"), w=("ckt_w", "first"))
            per_feat["circ"] = (per_feat.n % 2) * per_feat.w
            per_src = per_feat.groupby(level="src").circ.sum()
            n = int(round(per_src.max()))
            n_circ += n
            labs = "; ".join(sorted(set(
                grp[grp.src == "HIFLD"].label if (grp.src == "HIFLD").any()
                else grp.label)))
            details.append(f"[{n}x {labs}]")
        # parity: features crossing an odd number of times, per source; a
        # feature crossing twice (bench loop) nets zero UNLESS tapped north
        best_net = 0
        for src, grp in c.groupby("src"):
            odd = grp.drop_duplicates("fid")
            n_odd = int(((odd.n_cross_feat % 2) * odd.ckt_w).sum())
            best_net = max(best_net, n_odd)
        out[kv] = dict(n_corr=n_corr, n_circ_geo=n_circ,
                       n_net_odd=best_net, detail=" ".join(details))
    return out


def capacity(counts):
    """(low, central, high) MVA. Low = parity-net circuits at low rating
    (bench loops untapped); central/high = geometric crossings at
    central/high ratings (loops tapped north of the line)."""
    lo = counts["138"]["n_net_odd"] * RATE_138[0] \
        + counts["46plus"]["n_net_odd"] * RATE_46[0]
    mid = counts["138"]["n_circ_geo"] * RATE_138[1] \
        + counts["46plus"]["n_circ_geo"] * RATE_46[1]
    hi = counts["138"]["n_circ_geo"] * RATE_138[2] \
        + counts["46plus"]["n_circ_geo"] * RATE_46[2]
    return lo, mid, hi


def requirement_grid(caps):
    """Tidy scenario grid: required N->S transfer vs guessed capacity."""
    rows = []
    for sl, f in F_SHARE.items():
        lo, mid, hi = caps[sl]
        for S in S_GW:
            for rho in RHO:
                for L in L_PEAK_GW:
                    for sg in SIGMA:
                        for gs in G_SOUTH_MW:
                            Smw, Lmw = S * 1000 * f, L * 1000
                            P = rho * Smw
                            lmid = MID_LOAD_FRAC * Lmw
                            # load north of the cut: (1-sigma) at SL-A by
                            # construction; small population-share
                            # assumption at B/C
                            ln_frac = LOADN_FRAC.get(sl, 1 - sg)
                            # evening: what the north-of-cut storage can
                            # send vs what the south of the cut needs (net
                            # of southern firm gen)
                            t_eve = min(max(sg * Lmw - gs, 0.0), P)
                            # midday: direct delivery while charging, net
                            # of local (north-of-cut) load, capped by
                            # southern absorption
                            t_mid = min(max(Smw - P - ln_frac * lmid, 0.0),
                                        sg * lmid)
                            req = max(t_eve, t_mid)
                            n1 = LARGEST_CKT_MVA[sl]
                            rows.append({
                                "screenline": sl, "f_share": f,
                                "solar_gw_total": S, "storage_ratio": rho,
                                "peak_load_gw": L, "south_share": sg,
                                "south_firm_mw": gs,
                                "t_evening_mw": round(t_eve),
                                "t_midday_mw": round(t_mid),
                                "required_mw": round(req),
                                "required_n1_mw": round(req + n1),
                                "cap_low_mva": lo, "cap_central_mva": mid,
                                "cap_high_mva": hi,
                                "gap_n0_vs_central_mw": round(req - mid),
                                "gap_n1_vs_central_mw": round(req + n1
                                                              - mid),
                                "gap_n0_vs_low_mw": round(req - lo),
                                "gap_n1_vs_low_mw": round(req + n1 - lo),
                            })
    return pd.DataFrame(rows)


def make_figure(lines, sl_gdf, all_cr, counts_by_sl):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch

    C_138, C_46, C_SL = "#4a3aa7", "#2a78d6", "#d55181"
    fig, ax = plt.subplots(figsize=(11, 8.5), dpi=160)
    slud = gpd.read_parquet(GIS / "slud.parquet").to_crs(CRS)
    slud[slud.island == "Oahu"].plot(ax=ax, color="#f0efec",
                                     edgecolor="#d8d6d0", linewidth=0.4)
    lsb_ag = gpd.read_parquet(GIS / "lsb_ag.parquet")
    lsb_ag[lsb_ag.island == "Oahu"].plot(ax=ax, color="#e2efe2",
                                         edgecolor="none")
    lines[lines.kv != "138"].plot(ax=ax, color=C_46, linewidth=0.9)
    lines[lines.kv == "138"].plot(ax=ax, color=C_138, linewidth=1.6)
    sl_gdf.plot(ax=ax, color=C_SL, linewidth=2.4, linestyle=(0, (5, 2)))

    # crossing points
    for kv, col, ms in [("138", C_138, 42), ("46plus", C_46, 30)]:
        c = all_cr[(all_cr.kv == kv) & (all_cr.src == "HIFLD")]
        if c.empty:
            c = all_cr[all_cr.kv == kv]
        ax.scatter(c.x, c.y, s=ms, facecolor="white", edgecolor=col,
                   linewidth=1.4, zorder=5)

    # per-screenline count labels at the western end
    for name, row in sl_gdf.iterrows():
        cnt = counts_by_sl[name]
        txt = (f"{name}\n138 kV: {cnt['138']['n_circ_geo']} ckt x-ings "
               f"({cnt['138']['n_corr']} corr.)\n"
               f"46 kV: {cnt['46plus']['n_circ_geo']} ckt x-ings "
               f"({cnt['46plus']['n_corr']} corr.)")
        x0, y0 = row.geometry.coords[0]
        ax.annotate(txt, (x0, y0), xytext=(-8, 0),
                    textcoords="offset points", fontsize=7.5,
                    fontweight="bold", color="#0b0b0b",
                    ha="right", va="center",
                    bbox=dict(boxstyle="round,pad=0.3", fc="white",
                              ec=C_SL, lw=1.0, alpha=0.95))

    # context annotations: southern plants (approx), northern solar areas
    plants = {"Kahe (~650 MW)": (-158.129, 21.355),
              "Waiau (~470 MW)": (-157.957, 21.395),
              "CIP/Kalaeloa (~400 MW)": (-158.093, 21.302)}
    pp = gpd.GeoSeries([Point(xy) for xy in plants.values()],
                       crs=4326).to_crs(CRS)
    ax.scatter([p.x for p in pp], [p.y for p in pp], marker="^", s=70,
               color="#3d3b38", zorder=6)
    for (lab, _), p in zip(plants.items(), pp):
        ax.annotate(lab, (p.x, p.y), xytext=(5, -11),
                    textcoords="offset points", fontsize=7.5,
                    color="#3d3b38")
    areas = {"Kunia": (-158.035, 21.435), "Waialua": (-158.09, 21.565),
             "Wahiawa": (-158.02, 21.503), "Kahuku": (-157.95, 21.67)}
    ap = gpd.GeoSeries([Point(xy) for xy in areas.values()],
                       crs=4326).to_crs(CRS)
    for (lab, _), p in zip(areas.items(), ap):
        ax.annotate(lab, (p.x, p.y), fontsize=8.5, fontstyle="italic",
                    color="#1a7a37", ha="center", fontweight="bold")

    handles = [Line2D([], [], color=C_138, lw=1.6, label="138 kV"),
               Line2D([], [], color=C_46, lw=0.9, label="46 kV+ (mapped)"),
               Line2D([], [], color=C_SL, lw=2.4, linestyle="--",
                      label="screenline"),
               Line2D([], [], marker="o", mfc="white", mec=C_138, lw=0,
                      label="circuit crossing"),
               Line2D([], [], marker="^", color="#3d3b38", lw=0,
                      label="thermal plant (approx site)"),
               Patch(fc="#e2efe2", label="ag district")]
    ax.legend(handles=handles, loc="lower left", fontsize=8, frameon=True,
              framealpha=0.95, edgecolor="#d8d6d0")
    ax.set_title("North->south bulk-delivery screenlines: mapped circuit "
                 "crossings (HIFLD+OSM; 46 kV under-mapped)",
                 fontsize=11.5, color="#0b0b0b")
    ax.text(0.01, 0.985,
            "Crossing counts are from public line maps; parallel circuits "
            "on shared towers may be drawn as one line.\nHECO ratings "
            "confidential; capacity figures in the note are "
            "planning-typical guesses. 46 kV badly under-mapped\n"
            "(0 mapped crossings at SL-A is a data artifact, not reality).",
            transform=ax.transAxes, fontsize=7.5, color="#52514e",
            va="top")
    ax.set_axis_off()
    fig.tight_layout()
    FIGS.mkdir(parents=True, exist_ok=True)
    out = FIGS / "f_screenlines.png"
    fig.savefig(out, bbox_inches="tight")
    print(f"wrote {out}")


def main():
    lines = load_lines()
    sl_gdf = gpd.GeoDataFrame(
        {"desc": [v["desc"] for v in SCREENLINES.values()]},
        geometry=gpd.GeoSeries(
            {k: LineString(v["coords"]) for k, v in SCREENLINES.items()},
            crs=4326).to_crs(CRS),
        index=list(SCREENLINES))

    counts_by_sl, caps, all_cr, sl_rows = {}, {}, [], []
    for name, row in sl_gdf.iterrows():
        cr = crossings_for(row.geometry, lines)
        cr = cluster_corridors(cr) if len(cr) else cr.assign(corridor=[])
        cr["screenline"] = name
        all_cr.append(cr)
        cnt = count_screenline(cr)
        counts_by_sl[name] = cnt
        caps[name] = capacity(cnt)
        lo, mid, hi = caps[name]
        print(f"\n=== {name}: {row.desc}")
        for kv in ["138", "46plus"]:
            c = cnt[kv]
            print(f"  {kv:>7}: {c['n_circ_geo']} circuit crossings in "
                  f"{c['n_corr']} corridors (parity-net {c['n_net_odd']})")
            if c["detail"]:
                print(f"           {c['detail']}")
        print(f"  guessed capacity: {lo:.0f} (low/untapped-loops) | "
              f"{mid:.0f} (central) | {hi:.0f} (high) MVA")
        sl_rows.append({
            "screenline": name, "description": row.desc,
            "n_corridors_138": cnt["138"]["n_corr"],
            "n_circuits_138_geo": cnt["138"]["n_circ_geo"],
            "n_circuits_138_net": cnt["138"]["n_net_odd"],
            "n_corridors_46": cnt["46plus"]["n_corr"],
            "n_circuits_46_geo": cnt["46plus"]["n_circ_geo"],
            "n_circuits_46_net": cnt["46plus"]["n_net_odd"],
            "cap_low_mva": lo, "cap_central_mva": mid, "cap_high_mva": hi,
            "corridor_detail_138": cnt["138"]["detail"],
            "corridor_detail_46": cnt["46plus"]["detail"],
        })
    all_cr = pd.concat(all_cr, ignore_index=True)

    pd.DataFrame(sl_rows).to_csv(GIS / "screenline_analysis.csv",
                                 index=False)
    print(f"\nwrote {GIS / 'screenline_analysis.csv'}")

    grid = requirement_grid(caps)
    grid.to_csv(GIS / "screenline_requirements.csv", index=False)
    print(f"wrote {GIS / 'screenline_requirements.csv'} ({len(grid)} rows)")

    # central-slice table for the note
    sl_slice = grid[(grid.south_share == 0.775) & (grid.south_firm_mw == 0)
                    & grid.peak_load_gw.isin([1.2, 2.0])
                    & grid.storage_ratio.isin([0.5, 1.0])]
    piv = sl_slice[sl_slice.screenline == "SL-A"].pivot_table(
        index=["peak_load_gw", "storage_ratio"], columns="solar_gw_total",
        values="required_mw")
    print("\nRequired N->S transfer across SL-A (MW), sigma=0.775, "
          "G_south=0:")
    print(piv)

    make_figure(lines, sl_gdf, all_cr, counts_by_sl)
    return sl_rows, grid


if __name__ == "__main__":
    main()
