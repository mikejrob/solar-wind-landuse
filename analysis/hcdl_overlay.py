#!/usr/bin/env python3
"""
USDA NASS / UH Manoa Hawaii Cropland Data Layer (HCDL) 2023-2025 on Oahu:
warp to the repository's 10 m EPSG:26904 grid, tabulate by year, cross
against the HDOA 2020 Agricultural Land Use Baseline polygons, the ag
district, LSB soil class, and TMK parcels, and flag candidate changes.

Source: Hawaii_CDL_2023_2024_2025.zip (V2.1, released 2026-06-12),
https://www.nass.usda.gov/Research_and_Science/Cropland/Release/datasets/
Cached data/raw/hcdl/. Rasters are EPSG:3857 at a nominal 10 m (about
9.3 m on the ground at 21.5 N), uint8 CDL class codes. They are warped
(nearest neighbour) onto the grid of data/gis/dem/oahu_slope_bands.tif so
every cell is 100 m^2 and aligns with the slope, LSB, and district masks.

Classes (HCDL V2.0 report Table 1, CDL code -> name) and the crosswalk to
HDOA 2020 categories used here:
  1 Corn -> seed_production (Oahu corn is seed corn; HDOA maps the gross
     seed footprint, so HCDL corn should be a subset of it)
  45 Sugarcane -> sugar; 47 Misc Vegs & Fruits, 101 Sweet Basil, 46 Sweet
  Potatoes, 6 Sunflower, 106 Other Crops -> diversified_crop
  93 Banana -> banana; 95 Coffee -> coffee; 97 Papaya -> papaya;
  98 Pineapple -> pineapple; 100 Taro -> taro; 96 Macadamia -> macadamia
  94 Other Exotic Fruits, 72 Citrus, 215 Avocados, 102 Coconut ->
     tropical_fruits
  103 Plumeria, 104 Noni, 105 Dracaena -> flowers_foliage_landscape
  99 Commercial Forest -> commercial_forestry
  176 Grassland/Pasture -> grassland (NOT equated with HDOA pasture: the
     HCDL class is an NLCD-style cover class, HDOA pasture is fenced
     commercial cattle land)
  63 Forest, 152 Shrubland, 131 Barren, 82 Developed, 111 Water -> non-ag
Cells with code 0 are background/nodata.

Outputs (data/):
  oahu_hcdl_class_acres.csv          class x year acres, all Oahu / ag district
  oahu_hcdl_by_soil.csv              crop group x LSB class x year (ag district)
  oahu_hcdl_vs_hdoa2020.csv          HDOA 2020 category x HCDL 2024 group (ag district), acres
  oahu_hcdl_stability.csv            3-year stability of HCDL crop groups, by HDOA category
  oahu_parcel_hcdl.csv               per ag-district parcel: HCDL crop-group acres by year, HDOA 2020 acres, flags
  oahu_hcdl_change_candidates.csv    parcels where HCDL (stable 3 yr) disagrees with HDOA 2020
"""
from pathlib import Path
import numpy as np, pandas as pd, geopandas as gpd, rasterio
from rasterio import features
from rasterio.warp import reproject, Resampling
from shapely import make_valid

PROJECT = Path(__file__).resolve().parents[1]
DATA, GIS, RAW = PROJECT / "data", PROJECT / "data" / "gis", PROJECT / "data" / "raw" / "hcdl" / "unz"
OUT = GIS / "hcdl"; OUT.mkdir(exist_ok=True)
CRS = "EPSG:26904"; M2AC = 4046.8564224; CELL_AC = 100.0 / M2AC
YEARS = (2023, 2024, 2025)

CDL_NAME = {1: "Corn", 6: "Sunflower", 45: "Sugarcane", 46: "Sweet Potatoes", 47: "Misc Vegs & Fruits",
            63: "Forest", 72: "Citrus", 82: "Developed", 93: "Banana", 94: "Other Exotic Fruits", 95: "Coffee",
            96: "Macadamia", 97: "Papaya", 98: "Pineapple", 99: "Commercial Forest", 100: "Taro", 101: "Sweet Basil",
            102: "Coconut", 103: "Plumeria", 104: "Noni Fruit", 105: "Dracaena", 106: "Other Crops", 111: "Open Water",
            131: "Barren", 152: "Shrubland", 176: "Grassland/Pasture", 215: "Avocados", 0: "background"}
GROUP = {1: "seed_production", 45: "sugar", 47: "diversified_crop", 101: "diversified_crop", 46: "diversified_crop",
         6: "diversified_crop", 106: "diversified_crop", 93: "banana", 95: "coffee", 97: "papaya", 98: "pineapple",
         100: "taro", 96: "macadamia_nuts", 94: "tropical_fruits", 72: "tropical_fruits", 215: "tropical_fruits",
         102: "tropical_fruits", 103: "flowers_foliage_landscape", 104: "flowers_foliage_landscape",
         105: "flowers_foliage_landscape", 99: "commercial_forestry", 176: "grassland", 63: "non_ag", 152: "non_ag",
         131: "non_ag", 82: "non_ag", 111: "non_ag", 0: "background"}
GROUPS = ["seed_production", "sugar", "diversified_crop", "banana", "coffee", "papaya", "pineapple", "taro",
          "macadamia_nuts", "tropical_fruits", "flowers_foliage_landscape", "commercial_forestry", "grassland",
          "non_ag", "background"]
GID = {g: i for i, g in enumerate(GROUPS)}
CROP_GROUPS = GROUPS[:12]
HDOA_CATS = ["Diversified Crop", "Seed Production", "Pineapple", "Pasture", "Flowers / Foliage / Landscape", "Banana",
             "Aquaculture", "Tropical Fruits", "Coffee", "Papaya", "Taro", "Commercial Forestry", "Macadamia Nuts"]
HID = {c: i + 1 for i, c in enumerate(HDOA_CATS)}  # 0 = not mapped

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

def rasterize(geoms, values, shape, transform, dtype="int32"):
    if len(geoms) == 0: return np.zeros(shape, dtype=dtype)
    return features.rasterize(zip(geoms, values), out_shape=shape, transform=transform, fill=0, dtype=dtype)

def warp_year(y, shape, transform):
    dst = OUT / f"hcdl_{y}_oahu_26904.tif"
    if dst.exists():
        with rasterio.open(dst) as r: return r.read(1)
    with rasterio.open(RAW / f"{y}_10m_cdl_hawaii.tif") as src:
        out = np.zeros(shape, dtype="uint8")
        reproject(rasterio.band(src, 1), out, dst_transform=transform, dst_crs=CRS, resampling=Resampling.nearest)
    with rasterio.open(dst, "w", driver="GTiff", height=shape[0], width=shape[1], count=1, dtype="uint8", crs=CRS,
                       transform=transform, compress="lzw") as d: d.write(out, 1)
    return out

def main():
    with rasterio.open(GIS / "dem" / "oahu_slope_bands.tif") as r:
        shape, tr = r.shape, r.transform
    print("grid", shape, tr)
    cdl = {y: warp_year(y, shape, tr) for y in YEARS}
    grp = {y: np.vectorize(lambda v: GID[GROUP.get(int(v), "non_ag")], otypes=[np.uint8])(np.unique(cdl[y]))[np.searchsorted(np.unique(cdl[y]), cdl[y])] for y in YEARS}

    slud = gpd.read_parquet(GIS / "slud.parquet"); slud = fix(slud[slud.island.str.lower() == "oahu"].to_crs(CRS))
    ag = rasterize(slud[slud.ludcode == "A"].geometry, [1] * int((slud.ludcode == "A").sum()), shape, tr, "uint8").astype(bool)
    lsb = gpd.read_parquet(GIS / "lsb.parquet"); lsb = fix(lsb[lsb.island.str.lower() == "oahu"].to_crs(CRS))
    lsb["type"] = lsb["type"].astype(str).str.strip()
    lsb_r = rasterize(lsb.geometry, [("ABCDE".index(t) + 1) if t in "ABCDE" else 0 for t in lsb["type"]], shape, tr, "uint8")
    hd = gpd.read_file(GIS / "aglanduse_2020.geojson"); hd = fix(hd[hd.island == "Oahu"].to_crs(CRS))
    hd_r = rasterize(hd.geometry, [HID[c] for c in hd.crops_2020], shape, tr, "uint8")
    cap = pd.read_csv(DATA / "cap_scenarios_by_parcel.csv", dtype={"tmk": str}); cap = cap[cap.island == "Oahu"].set_index("tmk")
    par = gpd.read_parquet(GIS / "parcels_oahu.parquet").to_crs(CRS)
    par = fix(par[par.tmk9txt.isin(cap.index)].dissolve(by="tmk9txt")[["geometry"]]).reset_index().rename(columns={"tmk9txt": "tmk"})
    tmk_idx = {t: i + 1 for i, t in enumerate(par.tmk)}
    par_r = rasterize(par.geometry, [tmk_idx[t] for t in par.tmk], shape, tr, "int32")

    # 1. class x year acres
    rows = []
    for y in YEARS:
        for mask, scope in [(np.ones(shape, bool), "oahu_all"), (ag, "ag_district")]:
            u, c = np.unique(cdl[y][mask], return_counts=True)
            for k, n in zip(u, c): rows.append({"year": y, "scope": scope, "cdl_code": int(k), "class": CDL_NAME.get(int(k), str(k)), "group": GROUP.get(int(k), "non_ag"), "acres": n * CELL_AC})
    t1 = pd.DataFrame(rows).round(1); t1.to_csv(DATA / "oahu_hcdl_class_acres.csv", index=False)
    piv = t1[t1.scope == "ag_district"].pivot_table(index=["cdl_code", "class", "group"], columns="year", values="acres", aggfunc="sum").fillna(0).round(0)
    print("\nHCDL acres in the Oahu ag district by year:\n", piv.to_string())

    # 2. crop group x LSB class x year (ag district)
    rows = []
    for y in YEARS:
        for gi, g in enumerate(GROUPS):
            m = ag & (grp[y] == gi)
            for ci, cl in enumerate("ABCDE"):
                rows.append({"year": y, "group": g, "lsb_class": cl, "acres": int((m & (lsb_r == ci + 1)).sum()) * CELL_AC})
            rows.append({"year": y, "group": g, "lsb_class": "unrated", "acres": int((m & (lsb_r == 0)).sum()) * CELL_AC})
    pd.DataFrame(rows).round(1).to_csv(DATA / "oahu_hcdl_by_soil.csv", index=False)

    # 3. HDOA 2020 category x HCDL 2024 group, ag district
    def crosstab(y):
        rows = []
        for hi, hc in [(0, "not_mapped_2020")] + [(HID[c], c) for c in HDOA_CATS]:
            m = ag & (hd_r == hi)
            for gi, g in enumerate(GROUPS):
                rows.append({"hdoa_2020": hc, "hcdl_group": g, "acres": int((m & (grp[y] == gi)).sum()) * CELL_AC})
        return pd.DataFrame(rows)
    x24 = crosstab(2024); x24["year"] = 2024; x25 = crosstab(2025); x25["year"] = 2025
    xt = pd.concat([x24, x25]).round(1); xt.to_csv(DATA / "oahu_hcdl_vs_hdoa2020.csv", index=False)
    p24 = x24.pivot(index="hdoa_2020", columns="hcdl_group", values="acres").reindex(["not_mapped_2020"] + HDOA_CATS)[GROUPS].round(0)
    print("\nHDOA 2020 (rows) x HCDL 2024 (cols), ag district, acres:\n", p24.to_string())

    # 4. three-year stability by HDOA category
    stable_crop = np.zeros(shape, bool); anycrop = np.zeros(shape, bool)
    cropmask = {y: (grp[y] < len(CROP_GROUPS)) for y in YEARS}
    same_all = (grp[2023] == grp[2024]) & (grp[2024] == grp[2025])
    stable_crop = same_all & cropmask[2024]
    stable_noncrop = same_all & ~cropmask[2024]
    anycrop = cropmask[2023] | cropmask[2024] | cropmask[2025]
    allcrop = cropmask[2023] & cropmask[2024] & cropmask[2025]
    rows = []
    for hi, hc in [(0, "not_mapped_2020")] + [(HID[c], c) for c in HDOA_CATS]:
        m = ag & (hd_r == hi); n = int(m.sum())
        rows.append({"hdoa_2020": hc, "acres": n * CELL_AC,
                     "crop_all_3yr": int((m & allcrop).sum()) * CELL_AC, "crop_same_class_3yr": int((m & stable_crop).sum()) * CELL_AC,
                     "crop_any_yr": int((m & anycrop).sum()) * CELL_AC, "noncrop_all_3yr": int((m & ~anycrop).sum()) * CELL_AC,
                     "grassland_all_3yr": int((m & (grp[2023] == GID["grassland"]) & (grp[2024] == GID["grassland"]) & (grp[2025] == GID["grassland"])).sum()) * CELL_AC})
    st = pd.DataFrame(rows).round(1); st.to_csv(DATA / "oahu_hcdl_stability.csv", index=False)
    print("\n3-year stability by HDOA 2020 category (ag district):\n", st.to_string())

    # 5. parcel level
    ids = par_r[par_r > 0]; n_par = len(par)
    def tally(mask):
        return np.bincount(par_r[mask & (par_r > 0)], minlength=n_par + 1)[1:] * CELL_AC
    pp = pd.DataFrame({"tmk": par.tmk})
    pp["parcel_cells_acres"] = tally(np.ones(shape, bool))
    for y in YEARS:
        pp[f"hcdl_crop_{y}"] = tally(cropmask[y]); pp[f"hcdl_grass_{y}"] = tally(grp[y] == GID["grassland"])
        pp[f"hcdl_corn_{y}"] = tally(grp[y] == GID["seed_production"])
    pp["hcdl_crop_all3"] = tally(allcrop); pp["hcdl_crop_any"] = tally(anycrop)
    pp["hdoa2020_crop"] = tally((hd_r > 0) & (hd_r != HID["Pasture"])); pp["hdoa2020_pasture"] = tally(hd_r == HID["Pasture"])
    pp["hdoa_crop_x_hcdl_noncrop3"] = tally((hd_r > 0) & (hd_r != HID["Pasture"]) & ~anycrop)   # candidate loss / omission
    pp["hdoa_unmapped_x_hcdl_crop3"] = tally((hd_r == 0) & allcrop)                               # candidate gain / commission
    pp = pp.set_index("tmk").join(cap[["parcel_acres", "b_acres", "c_acres", "d_acres", "e_acres"]])
    own = pd.read_csv(DATA / "oahu_ag_owners.csv", dtype={"tmk": str}).set_index("tmk")
    pp["owner_resolved"] = own.owner_resolved.reindex(pp.index); pp["owner_type"] = own.owner_type.reindex(pp.index)
    cen = par.set_index("tmk").geometry.centroid.to_crs(4326); pp["lon"] = cen.x.reindex(pp.index).round(5); pp["lat"] = cen.y.reindex(pp.index).round(5)
    pp = pp.round(2); pp.to_csv(DATA / "oahu_parcel_hcdl.csv")
    cand = pp[(pp.hdoa_crop_x_hcdl_noncrop3 >= 5) | (pp.hdoa_unmapped_x_hcdl_crop3 >= 5)].copy()
    cand["candidate_type"] = np.where(cand.hdoa_crop_x_hcdl_noncrop3 >= cand.hdoa_unmapped_x_hcdl_crop3, "hdoa_crop_now_noncrop_3yr", "hdoa_unmapped_now_crop_3yr")
    cand["candidate_acres"] = cand[["hdoa_crop_x_hcdl_noncrop3", "hdoa_unmapped_x_hcdl_crop3"]].max(axis=1)
    # composition of the disagreeing cells in 2024, to separate fallow/grass from built/bare
    for nm, code in [("grass", GID["grassland"]), ("nonag", GID["non_ag"])]:
        pp[f"loss_cells_{nm}_2024"] = tally((hd_r > 0) & (hd_r != HID["Pasture"]) & ~anycrop & (grp[2024] == code))
    dev = np.isin(cdl[2024], [82, 131]); forest = np.isin(cdl[2024], [63, 152])
    pp["loss_cells_developed_barren_2024"] = tally((hd_r > 0) & (hd_r != HID["Pasture"]) & ~anycrop & dev)
    pp["loss_cells_forest_shrub_2024"] = tally((hd_r > 0) & (hd_r != HID["Pasture"]) & ~anycrop & forest)
    pp["gain_cells_other_crops_2024"] = tally((hd_r == 0) & allcrop & (cdl[2024] == 106))
    pp = pp.round(2); pp.to_csv(DATA / "oahu_parcel_hcdl.csv")
    cand = pp.loc[cand.index].copy()
    cand["candidate_type"] = np.where(cand.hdoa_crop_x_hcdl_noncrop3 >= cand.hdoa_unmapped_x_hcdl_crop3, "hdoa_crop_now_noncrop_3yr", "hdoa_unmapped_now_crop_3yr")
    cand["candidate_acres"] = cand[["hdoa_crop_x_hcdl_noncrop3", "hdoa_unmapped_x_hcdl_crop3"]].max(axis=1)
    cand = cand.sort_values("candidate_acres", ascending=False)
    cand["verification_status"] = "UNVERIFIED"
    cand["verification_note"] = ""
    cand.to_csv(DATA / "oahu_hcdl_change_candidates.csv")
    print(f"\nchange candidates (>=5 ac, 3-yr consistent): {len(cand)} parcels, {cand.candidate_acres.sum():.0f} ac")
    print(cand[["candidate_type", "candidate_acres", "loss_cells_grass_2024", "loss_cells_developed_barren_2024", "loss_cells_forest_shrub_2024", "gain_cells_other_crops_2024", "owner_resolved"]].head(20).to_string())
    print("\ncandidate totals by type:\n", cand.groupby("candidate_type").agg(parcels=("candidate_acres", "size"), acres=("candidate_acres", "sum")).round(0))
    print(" loss composition (2024):", cand[["loss_cells_grass_2024", "loss_cells_developed_barren_2024", "loss_cells_forest_shrub_2024"]].sum().round(0).to_dict())

    # 6. existing solar footprints (OSM) as seen by HCDL
    import json
    from shapely.geometry import Polygon
    from shapely.ops import unary_union
    d = json.load(open(GIS / "osm_solar_plants_oahu.json")); feats = []
    for e in d["elements"]:
        tg = e.get("tags", {})
        if e["type"] == "way" and "geometry" in e:
            pts = [(p["lon"], p["lat"]) for p in e["geometry"]]
            if len(pts) >= 4 and pts[0] == pts[-1]: feats.append({"name": tg.get("name") or f"way/{e['id']}", "geometry": Polygon(pts)})
        elif e["type"] == "relation":
            outers = [Polygon([(p["lon"], p["lat"]) for p in mm["geometry"]]) for mm in e.get("members", []) if mm.get("role") in ("outer", "") and "geometry" in mm and len(mm["geometry"]) >= 4]
            if outers: feats.append({"name": tg.get("name") or f"relation/{e['id']}", "geometry": unary_union([make_valid(o) for o in outers])})
    pl = fix(gpd.GeoDataFrame(feats, crs=4326).to_crs(CRS)); pl = pl[pl.geometry.area / M2AC >= 10]
    pl_r = rasterize(pl.geometry, range(1, len(pl) + 1), shape, tr, "int32")
    rows = []
    for i, nm in enumerate(pl.name, start=1):
        m = pl_r == i
        r = {"name": nm, "acres": int(m.sum()) * CELL_AC, "hdoa2020_mapped_ac": int((m & (hd_r > 0)).sum()) * CELL_AC}
        for y in YEARS:
            u, c = np.unique(cdl[y][m], return_counts=True); top = sorted(zip(c, u), reverse=True)[:2]
            r[f"hcdl_{y}_top"] = "; ".join(f"{CDL_NAME.get(int(k), k)} {n * CELL_AC:.0f}" for n, k in top)
        rows.append(r)
    sol = pd.DataFrame(rows).round(1); sol.to_csv(DATA / "oahu_existing_solar_hcdl.csv", index=False)
    print("\nexisting solar footprints as classed by HCDL:\n", sol.to_string())

if __name__ == "__main__":
    main()
