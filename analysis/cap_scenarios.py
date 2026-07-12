#!/usr/bin/env python3
"""
Quantify land eligible for utility-scale solar on Hawaii agricultural lands
under HRS 205-4.5(a)(20)'s per-parcel cap vs counterfactual rules.

Current rule (S0): solar permitted on class B/C (LSB overall productivity
rating) ag-district land up to min(10% of parcel area, 20 acres) per parcel.
Class A soils: banned. D/E soils: not constrained by this cap.

Scenarios (per parcel, counting only B/C area as the constrained resource):
  S0: min(0.10 * parcel_area, 20 ac, BC_area)   -- current law
  S1: min(0.10 * parcel_area, BC_area)          -- drop hard 20-ac cap
  S2: min(0.20 * parcel_area, 20 ac, BC_area)   -- 20% with hard cap
  S3: min(0.20 * parcel_area, BC_area)          -- 20% no hard cap (headline)
  S4: BC_area                                   -- no cap at all

Data (State of Hawaii geospatial portal, geodata.hawaii.gov ArcGIS REST):
  - Land Study Bureau (LSB) overall productivity ratings, statewide polygons:
      LandUseLandCover/MapServer/3   (fields: type A-E, island, gisacres)
  - State Land Use Districts (ludcode A/U/R/C):
      ParcelsZoning/MapServer/20
  - County TMK parcels:
      ParcelsZoning/MapServer/11 (Oahu), /5 (Hawaii), /30 (Maui), /9 (Kauai)

Everything is cached under DATA_DIR; the script is resume-safe and re-runs
end-to-end from cache without hitting the network.

CRS: EPSG:26904 (NAD83 / UTM zone 4N). Not strictly equal-area, but scale
distortion across the Hawaiian islands is <0.1%, far below the noise in the
source polygons. All areas computed from projected geometry; 1 ac = 4046.8564224 m2.

Usage:
  python cap_scenarios.py download [oahu|statewide]   # fetch layers to cache
  python cap_scenarios.py analyze  [oahu|statewide]   # run scenario analysis
"""

import json
import math
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

PROJECT = Path("/Users/michaelroberts/Research/solar-wind-landuse")
DATA_DIR = PROJECT / "data" / "gis"
OUT_RESULTS = PROJECT / "data" / "cap_scenarios_results.csv"
OUT_PARCELS = PROJECT / "data" / "cap_scenarios_by_parcel.csv"

BASE = "https://geodata.hawaii.gov/arcgis/rest/services"
M2_PER_ACRE = 4046.8564224
CRS = "EPSG:26904"  # NAD83 / UTM zone 4N
SLEEP = 0.4         # polite rate limit between requests
RETRIES = 5

LAYERS = {
    "lsb": {
        "url": f"{BASE}/LandUseLandCover/MapServer/3",
        "out_fields": "objectid,type,island,gisacres",
        "page": 2000,
    },
    "slud": {
        "url": f"{BASE}/ParcelsZoning/MapServer/20",
        "out_fields": "objectid,ludcode,island,acres",
        "page": 50,   # few features but very complex statewide polygons
    },
    "parcels_oahu": {
        "url": f"{BASE}/ParcelsZoning/MapServer/11",
        "out_fields": "objectid,tmk9txt,gisacres",
        "page": 1000,
        "island": "Oahu",
    },
    "parcels_hawaii": {
        "url": f"{BASE}/ParcelsZoning/MapServer/5",
        "out_fields": "objectid,tmk_txt,majorowner,gisacres",
        "page": 1000,
        "island": "Hawaii",
    },
    "parcels_maui": {
        "url": f"{BASE}/ParcelsZoning/MapServer/30",
        "out_fields": "objectid,tmk_txt,gisacres",
        "page": 1000,
        "island": "MauiCounty",  # Maui/Molokai/Lanai/Kahoolawe; split later
    },
    "parcels_kauai": {
        "url": f"{BASE}/ParcelsZoning/MapServer/9",
        "out_fields": "objectid,tmk_txt,owner,gisacres",
        "page": 1000,
        "island": "Kauai",
    },
}


# ---------------------------------------------------------------- download

def _get(url, params):
    qs = urllib.parse.urlencode(params)
    for attempt in range(RETRIES):
        try:
            with urllib.request.urlopen(f"{url}?{qs}", timeout=300) as r:
                return json.loads(r.read())
        except Exception as e:  # noqa: BLE001
            wait = 2 ** attempt
            print(f"    retry {attempt + 1}/{RETRIES} after error: {e} (wait {wait}s)")
            time.sleep(wait)
    raise RuntimeError(f"failed after {RETRIES} retries: {url}")

def download_layer(name):
    """Paginated GeoJSON download, one file per page, resume-safe."""
    spec = LAYERS[name]
    pages_dir = DATA_DIR / f"pages_{name}"
    pages_dir.mkdir(parents=True, exist_ok=True)
    done_marker = pages_dir / "_COMPLETE"
    if done_marker.exists():
        print(f"[{name}] already complete")
        return
    count = _get(spec["url"] + "/query",
                 {"where": "1=1", "returnCountOnly": "true", "f": "json"})["count"]
    page = spec["page"]
    npages = math.ceil(count / page)
    print(f"[{name}] {count} features, {npages} pages of {page}")
    for i in range(npages):
        pf = pages_dir / f"page_{i:05d}.geojson"
        if pf.exists() and pf.stat().st_size > 0:
            continue
        params = {
            "where": "1=1",
            "outFields": spec["out_fields"],
            "orderByFields": "objectid",
            "resultOffset": i * page,
            "resultRecordCount": page,
            "outSR": 4326,
            "geometryPrecision": 6,
            "f": "geojson",
        }
        data = _get(spec["url"] + "/query", params)
        if "features" not in data:
            raise RuntimeError(f"bad response page {i}: {str(data)[:300]}")
        tmp = pf.with_suffix(".tmp")
        tmp.write_text(json.dumps(data))
        tmp.rename(pf)
        if (i + 1) % 10 == 0 or i == npages - 1:
            print(f"  [{name}] page {i + 1}/{npages}")
        time.sleep(SLEEP)
    done_marker.write_text(time.strftime("%Y-%m-%dT%H:%M:%S"))
    print(f"[{name}] download complete")

def load_layer(name):
    """Load all cached pages into one GeoDataFrame (cached as GeoParquet)."""
    import geopandas as gpd
    import pandas as pd

    pq = DATA_DIR / f"{name}.parquet"
    if pq.exists():
        return gpd.read_parquet(pq)
    pages_dir = DATA_DIR / f"pages_{name}"
    assert (pages_dir / "_COMPLETE").exists(), f"{name} not fully downloaded"
    parts = [gpd.read_file(p) for p in sorted(pages_dir.glob("page_*.geojson"))]
    gdf = gpd.GeoDataFrame(pd.concat(parts, ignore_index=True), crs="EPSG:4326")
    gdf = gdf.drop_duplicates(subset="objectid" if "objectid" in gdf else None)
    gdf.to_parquet(pq)
    print(f"[{name}] merged {len(gdf)} features -> {pq.name}")
    return gdf


# ---------------------------------------------------------------- analysis

SCENARIOS = {  # (fraction of parcel area, hard cap in acres)
    "S0_current_10pct_20ac": (0.10, 20.0),
    "S1_10pct_nocap": (0.10, None),
    "S2_20pct_20ac": (0.20, 20.0),
    "S3_20pct_nocap": (0.20, None),
    "S4_all_BC": (None, None),
}

def analyze(parcel_layers):
    import geopandas as gpd
    import numpy as np
    import pandas as pd
    from shapely import make_valid

    from shapely.ops import unary_union

    def _polygonal(g):
        """make_valid can yield GeometryCollections; keep polygon parts only."""
        if g is None or g.is_empty:
            return None
        if g.geom_type in ("Polygon", "MultiPolygon"):
            return g
        if g.geom_type == "GeometryCollection":
            polys = [p for p in g.geoms
                     if p.geom_type in ("Polygon", "MultiPolygon")]
            return unary_union(polys) if polys else None
        return None

    def prep(gdf):
        g = gdf.to_crs(CRS)
        bad = ~g.geometry.is_valid
        if bad.any():
            g.loc[bad, "geometry"] = (g.loc[bad, "geometry"]
                                      .apply(make_valid).apply(_polygonal))
        g = g[g.geometry.notna() & ~g.geometry.is_empty]
        return g

    print("loading LSB + SLUD ...")
    lsb = prep(load_layer("lsb"))
    slud = prep(load_layer("slud"))
    ag = slud[slud.ludcode == "A"]

    # LSB acreage sanity check (full LSB coverage, before ag-district clip)
    lsb["lsb_acres"] = lsb.geometry.area / M2_PER_ACRE
    sanity = lsb.pivot_table(index="island", columns="type",
                             values="lsb_acres", aggfunc="sum").round(0)
    print("LSB acres by island/class (full coverage):\n", sanity)
    sanity.to_csv(DATA_DIR / "lsb_sanity_totals.csv")

    # Clip LSB to the State Ag District once, per island (cached)
    lsb_ag_pq = DATA_DIR / "lsb_ag.parquet"
    if lsb_ag_pq.exists():
        lsb_ag = gpd.read_parquet(lsb_ag_pq)
    else:
        print("clipping LSB to Ag District ...")
        lsb_ag = gpd.overlay(lsb[["type", "island", "geometry"]],
                             ag[["ludcode", "geometry"]], how="intersection",
                             keep_geom_type=True)
        lsb_ag["ag_acres"] = lsb_ag.geometry.area / M2_PER_ACRE
        lsb_ag.to_parquet(lsb_ag_pq)
    ag_by_class = lsb_ag.pivot_table(index="island", columns="type",
                                     values="ag_acres", aggfunc="sum").round(0)
    print("LSB acres by island/class WITHIN Ag District:\n", ag_by_class)
    ag_by_class.to_csv(DATA_DIR / "lsb_in_ag_district_totals.csv")

    all_parcel_rows = []
    for name in parcel_layers:
        print(f"processing {name} ...")
        parcels = prep(load_layer(name))
        tmk_col = "tmk9txt" if "tmk9txt" in parcels else "tmk_txt"
        owner_col = ("owner" if "owner" in parcels
                     else "majorowner" if "majorowner" in parcels else None)
        parcels = parcels[~parcels.geometry.is_empty & parcels.geometry.notna()]
        parcels["parcel_acres"] = parcels.geometry.area / M2_PER_ACRE
        parcels = parcels[parcels.parcel_acres > 0.01]

        # restrict LSB-in-ag to this county's bbox, then keep only parcels
        # that intersect it (cuts 172k Oahu parcels to the ag-relevant few k)
        from shapely.geometry import box
        sub = lsb_ag[lsb_ag.geometry.intersects(box(*parcels.total_bounds))]
        hits = gpd.sjoin(parcels, sub, how="inner", predicate="intersects")
        keep_ids = hits.index.unique()
        pw = parcels.loc[keep_ids].copy()
        print(f"  {len(parcels)} parcels -> {len(pw)} intersect ag-district LSB")

        cols = ["objectid", tmk_col, "parcel_acres", "geometry"]
        if owner_col:
            cols.insert(2, owner_col)
        inter = gpd.overlay(pw[cols], sub[["type", "island", "geometry"]],
                            how="intersection", keep_geom_type=True)
        inter["class_acres"] = inter.geometry.area / M2_PER_ACRE

        wide = (inter.groupby(["objectid", tmk_col, "parcel_acres", "type"],
                              dropna=False)["class_acres"].sum()
                .unstack("type").fillna(0.0).reset_index())
        for c in "ABCDE":
            if c not in wide:
                wide[c] = 0.0
        # island: dominant island of intersected LSB polys (handles Maui Cty)
        isl = (inter.groupby("objectid")
               .apply(lambda d: d.groupby("island")["class_acres"].sum().idxmax(),
                      include_groups=False).rename("island"))
        wide = wide.merge(isl, on="objectid")
        if owner_col:
            own = inter.groupby("objectid")[owner_col].first().rename("owner")
            wide = wide.merge(own, on="objectid")
        else:
            wide["owner"] = ""
        wide = wide.rename(columns={tmk_col: "tmk",
                                    **{c: f"{c.lower()}_acres" for c in "ABCDE"}})

        bc = wide.b_acres + wide.c_acres
        pa = wide.parcel_acres
        for sname, (frac, cap) in SCENARIOS.items():
            v = bc.copy() if frac is None else np.minimum(frac * pa, bc)
            if cap is not None:
                v = np.minimum(v, cap)
            wide[sname] = v
        wide["county_layer"] = name
        all_parcel_rows.append(wide)

    out = pd.concat(all_parcel_rows, ignore_index=True)
    cols = ["tmk", "island", "county_layer", "owner", "parcel_acres",
            "a_acres", "b_acres", "c_acres", "d_acres", "e_acres",
            *SCENARIOS.keys()]
    out[cols].round(3).to_csv(OUT_PARCELS, index=False)
    print(f"wrote {OUT_PARCELS} ({len(out)} parcels)")

    # island x scenario aggregate
    rows = []
    for (isl), grp in out.groupby("island"):
        for sname in SCENARIOS:
            ac = grp[sname].sum()
            rows.append({"island": isl, "scenario": sname,
                         "eligible_acres": round(ac, 1),
                         "mw_at_5ac": round(ac / 5.0, 1),
                         "mw_at_7ac": round(ac / 7.0, 1)})
    total_label = "STATEWIDE" if len(parcel_layers) > 1 else "ALL_DOWNLOADED"
    for sname in SCENARIOS:  # total over downloaded counties
        ac = out[sname].sum()
        rows.append({"island": total_label, "scenario": sname,
                     "eligible_acres": round(ac, 1),
                     "mw_at_5ac": round(ac / 5.0, 1),
                     "mw_at_7ac": round(ac / 7.0, 1)})
    pd.DataFrame(rows).to_csv(OUT_RESULTS, index=False)
    print(f"wrote {OUT_RESULTS}")

    # supporting tables for the notes file
    dec = out.copy()
    dec["bc_acres"] = dec.b_acres + dec.c_acres
    dec["size_decile"] = pd.qcut(dec.parcel_acres, 10, labels=False,
                                 duplicates="drop") + 1
    dtab = dec.groupby("size_decile").agg(
        n=("tmk", "size"),
        min_ac=("parcel_acres", "min"), max_ac=("parcel_acres", "max"),
        bc_acres=("bc_acres", "sum"),
        **{s: (s, "sum") for s in SCENARIOS})
    dtab.round(1).to_csv(DATA_DIR / "scenario_by_size_decile.csv")
    if (out.owner != "").any():
        otab = (out[out.owner != ""].groupby(["county_layer", "owner"])
                [["parcel_acres", "b_acres", "c_acres", *SCENARIOS.keys()]]
                .sum().sort_values("S3_20pct_nocap", ascending=False).head(40))
        otab.round(1).to_csv(DATA_DIR / "scenario_by_owner_top.csv")
    print("supporting tables written to", DATA_DIR)
    return out


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "analyze"
    scope = sys.argv[2] if len(sys.argv) > 2 else "oahu"
    parcel_layers = (["parcels_oahu"] if scope == "oahu" else
                     ["parcels_oahu", "parcels_hawaii", "parcels_maui",
                      "parcels_kauai"])
    if mode == "download":
        for lyr in ["lsb", "slud", *parcel_layers]:
            download_layer(lyr)
    else:
        analyze(parcel_layers)
