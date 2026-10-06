#!/usr/bin/env python3
"""
Screen the areas a reviewer (B. Plasch, 2026-09-07; docs/reviews/) says
should not count as available solar land, and locate existing solar farms,
against the repository's Oahu ag-district parcel tables.

Each named area is identified by owner-of-record (data/oahu_ag_owners.csv)
and/or a lat/lon box (WGS84) around the place. For every matching
ag-district parcel the script reports LSB class acres, slope-band acres,
2020 ag use, grid distance, and whether it sits in the modeled B/C draw.
Existing solar plants come from OpenStreetMap (power=plant, plant:source
containing "solar"; Overpass pull 2026-10-06 by osm_footprint_check.py
--refresh, data/gis/osm_solar_plants_oahu.json).

Outputs: data/oahu_review_area_screen.csv (per area totals),
         data/oahu_review_area_parcels.csv (per parcel),
         data/oahu_existing_solar_osm.csv (per plant: acres, LSB mix, district).
"""
from pathlib import Path
import json
import numpy as np, pandas as pd, geopandas as gpd
from shapely.geometry import box, Polygon, MultiPolygon, shape
from shapely.ops import unary_union
from shapely import make_valid

PROJECT = Path(__file__).resolve().parents[1]
DATA, GIS = PROJECT / "data", PROJECT / "data" / "gis"
CRS = "EPSG:26904"; M2AC = 4046.8564224

# (label, owner_resolved regex or None, bbox (minlon,minlat,maxlon,maxlat) or explicit TMK list, reviewer's reason)
AREAS = [
 ("James Campbell NWR (Kahuku)", r"United States - FWS", None, "federal wildlife refuge"),
 ("Kualoa Regional Park", r"City & County of Honolulu", (-157.86, 21.50, -157.82, 21.53), "county park"),
 ("Patsy T. Mink Central Oahu Regional Park", r"City & County of Honolulu", (-158.03, 21.42, -157.99, 21.46), "county park"),
 ("Kualoa Ranch (Morgan family)", r"Kualoa Ranch", None, "owner's higher-value use (tourism/ranch)"),
 ("Waikane Valley Impact Area (MCBH parcel)", None, ["148014006"], "WWII unexploded ordnance (Marine Corps impact area; 2010 munitions-response site)"),
 ("Waikane valley floor (non-HHFDC, non-federal)", r"^(?!State of Hawaii - HHFDC|United States)", (-157.895, 21.485, -157.845, 21.512), "context: private/City parcels around the impact area"),
 ("Waiahole Valley (HHFDC)", r"HHFDC", None, "state farm lots used mostly for homes"),
 ("Old Haleiwa airfield (Puaena Point, KS)", None, ["162002031", "162002001", "162001002"], "de facto public park (WWII fighter strip; KS-owned per Wikipedia)"),
 ("Pupukea-Paumalu Park Reserve (TPL 2007 -> State Parks; Army ACUB buffer)", None, ["159005087", "159006018", "159033001", "159003053"], "de facto public park: mountain-bike/hiking trail network"),
 ("Kahuku motocross (TMK 158002002, Army-retained lease parcel)", None, ["158002002"], "commercial motocross track (21.6782, -158.0178) sits on the Army-retained Kahuku parcel, already a separate map category"),
 ("Upper Waianae Mountains (interior, >2 km from 46 kV)", None, (-158.21, 21.40, -158.06, 21.60), "rough terrain, small pads, access, far from grid"),
]

def polygonal(geom):
    """make_valid, then keep only polygonal parts (GeometryCollection -> union of its polygons)."""
    from shapely.geometry import GeometryCollection
    from shapely.ops import unary_union
    g = make_valid(geom)
    if g.geom_type in ("Polygon", "MultiPolygon"): return g
    if g.geom_type == "GeometryCollection":
        parts = [p for p in g.geoms if p.geom_type in ("Polygon", "MultiPolygon")]
        return unary_union(parts) if parts else None
    return None

def fix(g):
    g = g.copy(); g["geometry"] = g.geometry.apply(polygonal)
    return g[g.geometry.notna() & ~g.geometry.is_empty]

def main():
    cap = pd.read_csv(DATA / "cap_scenarios_by_parcel.csv", dtype={"tmk": str}); cap = cap[cap.island == "Oahu"].set_index("tmk")
    own = pd.read_csv(DATA / "oahu_ag_owners.csv", dtype={"tmk": str}).set_index("tmk")
    slope = pd.read_csv(DATA / "oahu_parcel_slope.csv", dtype={"tmk": str}).set_index("tmk")
    tx = pd.read_csv(DATA / "oahu_land_transmission.csv", dtype={"tmk": str}).set_index("tmk")
    use = pd.read_csv(DATA / "oahu_parcel_ag_use_2020.csv", dtype={"tmk": str}).set_index("tmk")
    sel = set(pd.read_csv(DATA / "oahu_bc_10pct_selection.csv", dtype={"tmk": str}).tmk)
    par = gpd.read_parquet(GIS / "parcels_oahu.parquet").to_crs(CRS)
    par = par[par.tmk9txt.isin(cap.index)].dissolve(by="tmk9txt")[["geometry"]]; par.index.name = "tmk"
    par = fix(par); cen = par.geometry.centroid.to_crs(4326)

    t = cap[["parcel_acres", "a_acres", "b_acres", "c_acres", "d_acres", "e_acres", "S0_current_10pct_20ac", "S3_20pct_nocap"]].copy()
    t["bc_acres"] = t.b_acres + t.c_acres; t["de_acres"] = t.d_acres + t.e_acres
    t["slope_le15"] = slope[["slope_0_5", "slope_5_10", "slope_10_15"]].sum(axis=1).reindex(t.index)
    t["slope_15_30"] = slope[["slope_15_20", "slope_20_25", "slope_25_30"]].sum(axis=1).reindex(t.index)
    t["slope_gt30"] = slope.slope_gt30.reindex(t.index)
    t["ag_use_2020"] = use.ag_use_acres.reindex(t.index); t["dominant_use_2020"] = use.dominant_use.reindex(t.index)
    t["dist_46kv_km"] = tx.dist_46kv_km.reindex(t.index); t["dist_138kv_km"] = tx.dist_138kv_km.reindex(t.index)
    t["owner_resolved"] = own.owner_resolved.reindex(t.index); t["owner_type"] = own.owner_type.reindex(t.index)
    t["in_bc_selection"] = t.index.isin(sel)
    t["lon"] = cen.x.reindex(t.index); t["lat"] = cen.y.reindex(t.index)

    rows, prows = [], []
    for label, rx, bb, why in AREAS:
        m = pd.Series(True, index=t.index)
        if rx: m &= t.owner_resolved.fillna("").str.contains(rx, regex=True)
        if isinstance(bb, list): m &= t.index.isin(bb)
        elif bb: m &= (t.lon >= bb[0]) & (t.lon <= bb[2]) & (t.lat >= bb[1]) & (t.lat <= bb[3])
        if label.startswith("Upper Waianae"): m &= (t.dist_46kv_km > 2.0)
        sub = t[m].copy(); sub.insert(0, "area", label)
        prows.append(sub)
        rows.append({"area": label, "reviewer_reason": why, "how_identified": ("owner=" + rx if rx else "") + (" bbox=" + str(bb) if bb else ""),
                     "parcels": len(sub), "ag_district_acres": sub.parcel_acres.sum(), "bc_acres": sub.bc_acres.sum(), "de_acres": sub.de_acres.sum(),
                     "de_le15_acres_approx": (sub.de_acres * (sub.slope_le15 / sub.parcel_acres).fillna(0)).sum(),
                     "S0_eligible_acres": sub.S0_current_10pct_20ac.sum(), "S3_eligible_acres": sub.S3_20pct_nocap.sum(),
                     "ag_use_2020_acres": sub.ag_use_2020.sum(), "parcels_in_bc_selection": int(sub.in_bc_selection.sum()),
                     "bc_selected_acres": sub[sub.in_bc_selection].bc_acres.sum(),
                     "median_dist_138kv_km": sub.dist_138kv_km.median(), "owners": "; ".join(sub.owner_resolved.fillna("?").value_counts().head(4).index)})
    out = pd.DataFrame(rows).round(1); out.to_csv(DATA / "oahu_review_area_screen.csv", index=False)
    pd.concat(prows).round(2).to_csv(DATA / "oahu_review_area_parcels.csv")
    pd.set_option("display.width", 250); pd.set_option("display.max_columns", 30)
    print(out.drop(columns=["how_identified", "owners"]).to_string())
    print("\nowners by area:"); [print(" ", r.area, "|", r.owners) for r in out.itertuples()]

    # existing solar farms (OSM)
    d = json.load(open(GIS / "osm_solar_plants_oahu.json"))
    feats = []
    for e in d["elements"]:
        tg = e.get("tags", {})
        if e["type"] == "way" and "geometry" in e:
            pts = [(p["lon"], p["lat"]) for p in e["geometry"]]
            if len(pts) >= 4 and pts[0] == pts[-1]: geom = Polygon(pts)
            else: continue
        elif e["type"] == "relation":
            outers = [Polygon([(p["lon"], p["lat"]) for p in mm["geometry"]]) for mm in e.get("members", []) if mm.get("role") in ("outer", "") and "geometry" in mm and len(mm["geometry"]) >= 4]
            if not outers: continue
            geom = unary_union([make_valid(o) for o in outers])
        else: continue
        feats.append({"osm_id": f"{e['type']}/{e['id']}", "name": tg.get("name"), "mw": tg.get("plant:output:electricity"), "operator": tg.get("operator"), "geometry": geom})
    pl = gpd.GeoDataFrame(feats, crs=4326).to_crs(CRS); pl = fix(pl); pl["acres"] = pl.geometry.area / M2AC
    lsb = gpd.read_parquet(GIS / "lsb.parquet"); lsb = lsb[lsb.island.str.lower() == "oahu"].to_crs(CRS); lsb = fix(lsb); lsb["type"] = lsb["type"].astype(str).str.strip()
    slud = gpd.read_parquet(GIS / "slud.parquet"); slud = slud[slud.island.str.lower() == "oahu"].to_crs(CRS); slud = fix(slud)
    o1 = gpd.overlay(pl, lsb[["type", "geometry"]], how="intersection", keep_geom_type=True); o1["a"] = o1.geometry.area / M2AC
    lsbmix = o1.pivot_table(index="osm_id", columns="type", values="a", aggfunc="sum", fill_value=0.0)
    o2 = gpd.overlay(pl, slud[["ludcode", "geometry"]], how="intersection", keep_geom_type=True); o2["a"] = o2.geometry.area / M2AC
    dmix = o2.pivot_table(index="osm_id", columns="ludcode", values="a", aggfunc="sum", fill_value=0.0)
    o3 = gpd.overlay(pl, par.reset_index()[["tmk", "geometry"]], how="intersection", keep_geom_type=True); o3["a"] = o3.geometry.area / M2AC
    tmks = o3.sort_values("a", ascending=False).groupby("osm_id")["tmk"].agg(lambda x: ";".join(x.head(5)))
    res = pl.drop(columns="geometry").set_index("osm_id")
    for c in "ABCDE": res["lsb_" + c] = lsbmix.get(c, pd.Series(dtype=float)).reindex(res.index).fillna(0)
    for c in ["A", "U", "C", "R"]: res["slud_" + c] = dmix.get(c, pd.Series(dtype=float)).reindex(res.index).fillna(0)
    res["ag_district_tmks"] = tmks.reindex(res.index)
    res = res.sort_values("acres", ascending=False).round(1); res.to_csv(DATA / "oahu_existing_solar_osm.csv")
    print("\nexisting solar (OSM), acres:", round(res.acres.sum()), "\n", res[["name", "mw", "acres", "lsb_A", "lsb_B", "lsb_C", "lsb_D", "lsb_E", "slud_A", "slud_U"]].head(20).to_string())
    print("\ntotals by LSB class (ac):", res[["lsb_A", "lsb_B", "lsb_C", "lsb_D", "lsb_E"]].sum().round(0).to_dict(), " ag district:", round(res.slud_A.sum()), " urban:", round(res.slud_U.sum()))

def size_bins():
    """Per-parcel eligible acreage by size bin (reviewer: minimum viable farm ~30 ac at 5 ac/MW)."""
    cap = pd.read_csv(DATA / "cap_scenarios_by_parcel.csv", dtype={"tmk": str}); cap = cap[cap.island == "Oahu"]
    slope = pd.read_csv(DATA / "oahu_parcel_slope.csv", dtype={"tmk": str}).set_index("tmk")
    le15 = (slope[["slope_0_5", "slope_5_10", "slope_10_15"]].sum(axis=1) / slope.parcel_acres).clip(upper=1)
    cap["de_le15"] = (cap.d_acres + cap.e_acres) * le15.reindex(cap.tmk).fillna(0).values
    bins = [0, 5, 20, 30, 100, 1e9]; labels = ["<5", "5-20", "20-30", "30-100", ">=100"]
    rows = []
    for col, lab in [("S0_current_10pct_20ac", "S0 by-right B/C"), ("S3_20pct_nocap", "S3 20% no cap B/C"), ("S4_all_BC", "all B/C"), ("de_le15", "D/E <=15% slope (uncapped)")]:
        v = cap[col]; b = pd.cut(v, bins=bins, labels=labels, right=False)
        g = v.groupby(b, observed=False).agg(["count", "sum"])
        for k, rr in g.iterrows(): rows.append({"scenario": lab, "parcel_eligible_acres_bin": k, "parcels": int(rr["count"]), "acres": round(rr["sum"], 1)})
    out = pd.DataFrame(rows); out["share_of_scenario_acres"] = (out.acres / out.groupby("scenario").acres.transform("sum")).round(3)
    out.to_csv(DATA / "oahu_eligible_by_parcel_size.csv", index=False)
    print("\neligible acres by per-parcel size bin:\n", out.pivot(index="parcel_eligible_acres_bin", columns="scenario", values="acres").to_string())

if __name__ == "__main__":
    size_bins()
    main()
