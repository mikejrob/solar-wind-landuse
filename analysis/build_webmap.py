#!/usr/bin/env python3
"""
Build the static data behind site/ (the interactive Oahu land-use map).

Writes simplified WGS84 GeoJSON layers and HCDL raster overlays to site/data/:
  slud.geojson              state land-use districts (Oahu)
  lsb.geojson               LSB overall productivity classes A-E (Oahu)
  hdoa2020.geojson          HDOA 2020 Agricultural Land Use Baseline polygons (Oahu)
  ag_parcels.geojson        ag-district parcels (6,274) with all compiled attributes
  lines.geojson             transmission lines (HIFLD + OSM; 138 kV, 46 kV+)
  solar_osm.geojson         existing solar-plant footprints (OSM)
  military.geojson          DoD fee/lease land (screen layer)
  wind_turbines.geojson     OSM wind turbines
  hcdl_2024.png, hcdl_2025.png + hcdl_bounds.json   HCDL class rasters (EPSG:3857 native)
  hcdl_legend.json          class code -> name/color
  manifest.json             layer list, sizes, build date

All vectors: simplified in EPSG:26904 (tolerance in metres below), reprojected
to EPSG:4326, coordinates rounded to 6 decimals. Everything is derived from
layers and tables already in data/ (see docs/DATA_DICTIONARY.md).
"""
from pathlib import Path
import json, datetime
import numpy as np, pandas as pd, geopandas as gpd, rasterio
from rasterio.windows import from_bounds
from shapely import make_valid
from shapely.ops import unary_union
from PIL import Image

PROJECT = Path(__file__).resolve().parents[1]
DATA, GIS, SITE = PROJECT / "data", PROJECT / "data" / "gis", PROJECT / "site" / "data"
SITE.mkdir(parents=True, exist_ok=True)
CRS = "EPSG:26904"; M2AC = 4046.8564224

def polygonal(geom):
    g = make_valid(geom)
    if g.geom_type in ("Polygon", "MultiPolygon"): return g
    if g.geom_type == "GeometryCollection":
        parts = [p for p in g.geoms if p.geom_type in ("Polygon", "MultiPolygon")]
        return unary_union(parts) if parts else None
    return None

def fix(g):
    g = g.copy(); g["geometry"] = g.geometry.apply(polygonal); return g[g.geometry.notna() & ~g.geometry.is_empty]

def write(gdf, name, tol=None, precision=6):
    g = gdf.copy()
    if tol: g["geometry"] = g.geometry.simplify(tol, preserve_topology=True)
    g = g[~g.geometry.is_empty].to_crs(4326)
    if g.geometry.geom_type.isin(["Polygon", "MultiPolygon", "GeometryCollection"]).all():
        import shapely
        g["geometry"] = shapely.set_precision(g.geometry.values, 10 ** -precision)   # round first, so no slivers collapse inside the writer
        g["geometry"] = g.geometry.apply(polygonal)
        g = g[g.geometry.notna() & ~g.geometry.is_empty]
    out = SITE / name
    g.to_file(out, driver="GeoJSON", COORDINATE_PRECISION=precision, RFC7946="NO", WRITE_BBOX="NO")
    print(f"{name:24s} {len(g):7,d} features  {out.stat().st_size / 1e6:6.2f} MB")
    return len(g), out.stat().st_size

def main():
    sizes = {}
    slud = gpd.read_parquet(GIS / "slud.parquet"); slud = fix(slud[slud.island.str.lower() == "oahu"].to_crs(CRS))
    slud = slud[["ludcode", "geometry"]].dissolve(by="ludcode").reset_index()
    slud["acres"] = (slud.geometry.area / M2AC).round(0)
    sizes["slud.geojson"] = write(slud, "slud.geojson", tol=8)

    lsb = gpd.read_parquet(GIS / "lsb.parquet"); lsb = fix(lsb[lsb.island.str.lower() == "oahu"].to_crs(CRS))
    lsb["cls"] = lsb["type"].astype(str).str.strip(); lsb["acres"] = (lsb.geometry.area / M2AC).round(1)
    sizes["lsb.geojson"] = write(lsb[["cls", "acres", "geometry"]], "lsb.geojson", tol=5)

    hd = gpd.read_file(GIS / "aglanduse_2020.geojson"); hd = fix(hd[hd.island == "Oahu"].to_crs(CRS))
    hd = hd.rename(columns={"crops_2020": "crop"})[["crop", "acreage", "geometry"]]; hd["acreage"] = hd.acreage.round(1)
    sizes["hdoa2020.geojson"] = write(hd, "hdoa2020.geojson", tol=3)

    # ag-district parcels with attributes
    cap = pd.read_csv(DATA / "cap_scenarios_by_parcel.csv", dtype={"tmk": str}); cap = cap[cap.island == "Oahu"].set_index("tmk")
    par = gpd.read_parquet(GIS / "parcels_oahu.parquet").to_crs(CRS)
    par = fix(par[par.tmk9txt.isin(cap.index)].dissolve(by="tmk9txt")[["geometry"]]); par.index.name = "tmk"
    own = pd.read_csv(DATA / "oahu_ag_owners.csv", dtype={"tmk": str}).set_index("tmk")
    use = pd.read_csv(DATA / "oahu_parcel_ag_use_2020.csv", dtype={"tmk": str}).set_index("tmk")
    hc = pd.read_csv(DATA / "oahu_parcel_hcdl.csv", dtype={"tmk": str}).set_index("tmk")
    sl = pd.read_csv(DATA / "oahu_parcel_slope.csv", dtype={"tmk": str}).set_index("tmk")
    tx = pd.read_csv(DATA / "oahu_land_transmission.csv", dtype={"tmk": str}).set_index("tmk")
    rv = pd.read_csv(DATA / "oahu_review_area_parcels.csv", dtype={"tmk": str})
    sel = set(pd.read_csv(DATA / "oahu_bc_10pct_selection.csv", dtype={"tmk": str}).tmk)
    cand = pd.read_csv(DATA / "oahu_hcdl_change_candidates.csv", dtype={"tmk": str}).set_index("tmk")
    flags = rv.groupby("tmk")["area"].agg(lambda x: "; ".join(sorted(set(x))))
    p = par.copy(); ix = p.index
    p["acres"] = cap.parcel_acres.reindex(ix).round(1)
    for c in "abcde": p[f"lsb_{c}"] = cap[f"{c}_acres"].reindex(ix).round(1)
    soils = cap[["a_acres", "b_acres", "c_acres", "d_acres", "e_acres"]].reindex(ix)
    p["lsb_dom"] = soils.idxmax(axis=1).str[0].str.upper().where(soils.max(axis=1) > 0, "unrated")
    p["s0_ac"] = cap.S0_current_10pct_20ac.reindex(ix).round(1); p["s3_ac"] = cap.S3_20pct_nocap.reindex(ix).round(1)
    p["owner"] = own.owner_resolved.reindex(ix).fillna("UNVERIFIED"); p["owner_type"] = own.owner_type.reindex(ix).fillna("unknown")
    p["use2020"] = use.dominant_use.reindex(ix).fillna("none_mapped"); p["use2020_ac"] = use.ag_use_acres.reindex(ix).round(1)
    p["crop2020_ac"] = use.crop_acres.reindex(ix).round(1); p["past2020_ac"] = use.pasture.reindex(ix).round(1)
    p["hcdl24_crop_ac"] = hc.hcdl_crop_2024.reindex(ix).round(1); p["hcdl24_corn_ac"] = hc.hcdl_corn_2024.reindex(ix).round(1)
    p["hcdl24_grass_ac"] = hc.hcdl_grass_2024.reindex(ix).round(1)
    p["slope_le15"] = sl[["slope_0_5", "slope_5_10", "slope_10_15"]].sum(axis=1).reindex(ix).round(1)
    p["slope_15_30"] = sl[["slope_15_20", "slope_20_25", "slope_25_30"]].sum(axis=1).reindex(ix).round(1)
    p["slope_gt30"] = sl.slope_gt30.reindex(ix).round(1)
    p["d46_km"] = tx.dist_46kv_km.reindex(ix).round(2); p["d138_km"] = tx.dist_138kv_km.reindex(ix).round(2)
    p["flags"] = flags.reindex(ix).fillna("")
    p["bc_sel"] = ix.isin(sel).astype(int)
    p["chg"] = cand.candidate_type.reindex(ix).fillna(""); p["chg_ac"] = cand.candidate_acres.reindex(ix).round(1)
    p = p.reset_index()
    sizes["ag_parcels.geojson"] = write(p, "ag_parcels.geojson", tol=2)

    lines = gpd.read_parquet(GIS / "oahu_lines_classified.parquet").to_crs(CRS)[["kv", "src", "geometry"]]
    sizes["lines.geojson"] = write(lines, "lines.geojson", tol=5)

    from shapely.geometry import Polygon, Point
    d = json.load(open(GIS / "osm_solar_plants_oahu.json")); feats = []
    for e in d["elements"]:
        tg = e.get("tags", {})
        if e["type"] == "way" and "geometry" in e:
            pts = [(q["lon"], q["lat"]) for q in e["geometry"]]
            if len(pts) >= 4 and pts[0] == pts[-1]: feats.append({"name": tg.get("name") or "", "mw": tg.get("plant:output:electricity") or "", "operator": tg.get("operator") or "", "osm": f"{e['type']}/{e['id']}", "geometry": Polygon(pts)})
        elif e["type"] == "relation":
            outers = [Polygon([(q["lon"], q["lat"]) for q in mm["geometry"]]) for mm in e.get("members", []) if mm.get("role") in ("outer", "") and "geometry" in mm and len(mm["geometry"]) >= 4]
            if outers: feats.append({"name": tg.get("name") or "", "mw": tg.get("plant:output:electricity") or "", "operator": tg.get("operator") or "", "osm": f"{e['type']}/{e['id']}", "geometry": unary_union([make_valid(o) for o in outers])})
    sol = fix(gpd.GeoDataFrame(feats, crs=4326).to_crs(CRS)); sol["acres"] = (sol.geometry.area / M2AC).round(1)
    sizes["solar_osm.geojson"] = write(sol, "solar_osm.geojson", tol=2)

    mil = gpd.read_parquet(GIS / "military" / "oahu_military_screen.parquet").to_crs(CRS); mil = fix(mil)
    mil["acres"] = (mil.geometry.area / M2AC).round(0)
    sizes["military.geojson"] = write(mil[["name", "tenure", "acres", "geometry"]], "military.geojson", tol=8)

    wt = pd.read_csv(GIS / "osm_wind_turbines_oahu.csv")
    wtg = gpd.GeoDataFrame(wt[["farm", "output", "manufacturer"]].fillna(""), geometry=gpd.points_from_xy(wt.lon, wt.lat), crs=4326).to_crs(CRS)
    sizes["wind_turbines.geojson"] = write(wtg, "wind_turbines.geojson")

    # HCDL rasters, native EPSG:3857 -> PNG overlays
    legend = {1: ("Corn (seed)", "#FFD300"), 6: ("Sunflower", "#FFFF00"), 45: ("Sugarcane", "#757EFF"), 46: ("Sweet potatoes", "#732600"),
              47: ("Misc vegs & fruits", "#FF6666"), 63: ("Forest", "#93CC93"), 72: ("Citrus", "#FFFF7E"), 82: ("Developed", "#9A9A9A"),
              93: ("Banana", "#D1FF00"), 94: ("Other exotic fruits", "#FF2626"), 95: ("Coffee", "#702600"), 96: ("Macadamia", "#54FF00"),
              97: ("Papaya", "#336600"), 98: ("Pineapple", "#B5705B"), 99: ("Commercial forest", "#007777"), 100: ("Taro", "#A05989"),
              101: ("Sweet basil", "#267000"), 102: ("Coconut", "#999900"), 103: ("Plumeria", "#FF6600"), 104: ("Noni", "#FF3399"),
              105: ("Dracaena", "#DFB9D1"), 106: ("Other crops", "#E3A12B"), 111: ("Open water", "#4D70A3"), 131: ("Barren", "#CCBFA3"),
              152: ("Shrubland", "#C6D69E"), 176: ("Grassland/pasture", "#E8FFBF"), 215: ("Avocados", "#66994D")}
    pal = np.zeros((256, 4), dtype=np.uint8)
    for k, (nm, hx) in legend.items(): pal[k] = [int(hx[1:3], 16), int(hx[3:5], 16), int(hx[5:7], 16), 255]
    pal[111] = [0, 0, 0, 0]  # water transparent
    from rasterio.warp import transform_bounds
    W, S, E, N = -158.30, 21.24, -157.62, 21.74
    for y in (2024, 2025):
        with rasterio.open(PROJECT / "data" / "raw" / "hcdl" / "unz" / f"{y}_10m_cdl_hawaii.tif") as r:
            b = transform_bounds("EPSG:4326", r.crs, W, S, E, N); w = from_bounds(*b, r.transform).round_offsets().round_lengths()
            a = r.read(1, window=w); wb = rasterio.windows.bounds(w, r.transform)
            bb = transform_bounds(r.crs, "EPSG:4326", *wb)
        rgba = pal[a]; Image.fromarray(rgba, "RGBA").save(SITE / f"hcdl_{y}.png", optimize=True)
        print(f"hcdl_{y}.png {a.shape} {(SITE / f'hcdl_{y}.png').stat().st_size / 1e6:.2f} MB bounds {bb}")
        json.dump({"south": bb[1], "west": bb[0], "north": bb[3], "east": bb[2]}, open(SITE / "hcdl_bounds.json", "w"))
    json.dump({str(k): {"name": v[0], "color": v[1]} for k, v in legend.items()}, open(SITE / "hcdl_legend.json", "w"), indent=1)
    json.dump({"built": datetime.date.today().isoformat(), "layers": {k: {"features": v[0], "bytes": v[1]} for k, v in sizes.items()}}, open(SITE / "manifest.json", "w"), indent=1)

if __name__ == "__main__":
    main()
