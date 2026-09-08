#!/usr/bin/env python3
"""
Overlay the HDOA 2020 Agricultural Land Use Baseline (Perroy & Collier 2022,
UH Hilo SDAV, for the Hawaii Dept of Agriculture) on the Oahu agricultural
district, LSB soil classes, TMK parcels, owners, and the solar-cap scenarios.

Question: how is the ag-district land that the solar caps govern actually
used today (2018-2020 imagery), by soil class, by parcel, by owner type, and
within the cap-eligible acreage?

Source layer: geodata.hawaii.gov LandUseLandCover/MapServer/19 ("2020
Agricultural Land Use"; fields crops_2020, island, acreage). Downloaded as
GeoJSON from the ArcGIS Hub item 342ee6c7547f45ddbfc07caf4ca2887d and cached
at data/gis/aglanduse_2020.geojson. Report: data/raw/hdoa-baseline/
2020_Update_Ag_Baseline_all_Hawaiian_Islands_v5.pdf. Mapping protocol
(report App. A1/A2): commercial operations, 3-acre minimum, satellite
imagery 2018-2020, field roads and buffers included, gulches/homes/fallow
excluded; "Seed Production" is gross land under seed-company control (~25%
planted at any time); "Pasture" is fenced commercial cattle land.

CRS EPSG:26904; 1 ac = 4046.8564224 m2. Areas from projected geometry.

Outputs (data/):
  oahu_ag_use_2020_by_soil.csv        soil class x crop acres, ag district
  oahu_ag_use_2020_by_district.csv    state LU district x crop acres
  oahu_parcel_ag_use_2020.csv         per ag-district parcel, acres by crop
  oahu_ag_use_2020_by_owner_type.csv  owner type x crop acres
  oahu_eligible_by_use_2020.csv       S0/S3 B/C-eligible and D/E acres by use
"""
from pathlib import Path
import json, sys, urllib.request
import numpy as np, pandas as pd, geopandas as gpd
from shapely import make_valid

PROJECT = Path(__file__).resolve().parents[1]
DATA, GIS = PROJECT / "data", PROJECT / "data" / "gis"
CRS = "EPSG:26904"; M2AC = 4046.8564224
SRC = GIS / "aglanduse_2020.geojson"
URL = ("https://prod-histategis.opendata.arcgis.com/api/download/v1/items/"
       "342ee6c7547f45ddbfc07caf4ca2887d/geojson?layers=19")
CROPS = ["Diversified Crop", "Seed Production", "Pineapple", "Pasture",
         "Flowers / Foliage / Landscape", "Banana", "Aquaculture",
         "Tropical Fruits", "Coffee", "Papaya", "Taro", "Commercial Forestry",
         "Macadamia Nuts"]
SLUG = {c: c.lower().replace(" / ", "_").replace(" ", "_") for c in CROPS}
CROP_ONLY = [c for c in CROPS if c != "Pasture"]

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

def ac(g): return g.geometry.area / M2AC

def pivot(df, row, val="acres"):
    p = df.pivot_table(index=row, columns="crops_2020", values=val, aggfunc="sum", fill_value=0.0)
    for c in CROPS:
        if c not in p.columns: p[c] = 0.0
    p = p[CROPS]; p.columns = [SLUG[c] for c in CROPS]
    p["crop_acres"] = p[[SLUG[c] for c in CROP_ONLY]].sum(axis=1)
    p["ag_use_acres"] = p["crop_acres"] + p["pasture"]
    return p.round(2)

def main():
    if not SRC.exists():
        print("downloading", URL); urllib.request.urlretrieve(URL, SRC)
    crop = gpd.read_file(SRC); crop = crop[crop["island"] == "Oahu"].to_crs(CRS)
    crop = fix(crop)[["crops_2020", "acreage", "geometry"]]
    crop["acres_calc"] = ac(crop)
    print("Oahu 2020 polygons:", len(crop), "source acreage %.0f  computed %.0f" % (crop.acreage.sum(), crop.acres_calc.sum()))

    slud = gpd.read_parquet(GIS / "slud.parquet"); slud = slud[slud.island.str.lower() == "oahu"].to_crs(CRS)
    slud = fix(slud)
    lsb_ag = gpd.read_parquet(GIS / "lsb_ag.parquet"); lsb_ag = lsb_ag[lsb_ag.island.str.lower() == "oahu"].to_crs(CRS)
    lsb_ag = fix(lsb_ag); lsb_ag["type"] = lsb_ag["type"].astype(str).str.strip()
    ag_district = slud[slud.ludcode == "A"].geometry.union_all()

    # 1. crop x state land use district
    d = gpd.overlay(crop, slud[["ludcode", "geometry"]], how="intersection", keep_geom_type=True)
    d["acres"] = ac(d)
    by_dist = pivot(d, "ludcode"); by_dist.index.name = "slud_district"
    by_dist.to_csv(DATA / "oahu_ag_use_2020_by_district.csv")
    print("\nby state land-use district (acres):\n", by_dist[["crop_acres", "pasture", "ag_use_acres"]])

    # 2. crop x LSB class within the ag district
    crop_ag = crop.copy(); crop_ag["geometry"] = crop_ag.geometry.intersection(ag_district)
    crop_ag = crop_ag[~crop_ag.geometry.is_empty]
    s = gpd.overlay(crop_ag, lsb_ag[["type", "geometry"]], how="intersection", keep_geom_type=True)
    s["acres"] = ac(s)
    rated = s.groupby("crops_2020")["acres"].sum()
    tot_ag = crop_ag.assign(acres=ac(crop_ag)).groupby("crops_2020")["acres"].sum()
    unrated = (tot_ag - rated.reindex(tot_ag.index).fillna(0)).clip(lower=0)
    s2 = pd.concat([s[["type", "crops_2020", "acres"]],
                    pd.DataFrame({"type": "unrated", "crops_2020": unrated.index, "acres": unrated.values})])
    by_soil = pivot(s2, "type"); by_soil.index.name = "lsb_class"
    cls_tot = lsb_ag.assign(a=ac(lsb_ag)).groupby("type")["a"].sum()
    by_soil["class_total_ag_district_acres"] = cls_tot.reindex(by_soil.index).round(1)
    by_soil["not_in_mapped_ag_acres"] = (by_soil["class_total_ag_district_acres"] - by_soil["ag_use_acres"]).round(1)
    by_soil["share_in_mapped_ag"] = (by_soil["ag_use_acres"] / by_soil["class_total_ag_district_acres"]).round(3)
    by_soil.to_csv(DATA / "oahu_ag_use_2020_by_soil.csv")
    print("\nby LSB class in ag district:\n", by_soil[["crop_acres", "pasture", "ag_use_acres", "class_total_ag_district_acres", "not_in_mapped_ag_acres", "share_in_mapped_ag"]])

    # 3. parcel level (ag-district parcels from the cap-scenario table)
    cap = pd.read_csv(DATA / "cap_scenarios_by_parcel.csv", dtype={"tmk": str})
    cap = cap[cap.island == "Oahu"].set_index("tmk")
    par = gpd.read_parquet(GIS / "parcels_oahu.parquet").to_crs(CRS)
    par = par[par.tmk9txt.isin(cap.index)].dissolve(by="tmk9txt")[["geometry"]].reset_index().rename(columns={"tmk9txt": "tmk"})
    par = fix(par)
    p = gpd.overlay(crop, par, how="intersection", keep_geom_type=True); p["acres"] = ac(p)
    # B/C-only use within each parcel (for attributing capped eligibility)
    pbc = gpd.overlay(p.drop(columns="acres"), lsb_ag[lsb_ag["type"].isin(["B", "C"])][["type", "geometry"]], how="intersection", keep_geom_type=True); pbc["acres"] = ac(pbc)
    pde = gpd.overlay(p.drop(columns="acres"), lsb_ag[lsb_ag["type"].isin(["D", "E"])][["type", "geometry"]], how="intersection", keep_geom_type=True); pde["acres"] = ac(pde)
    pp = pivot(p, "tmk").reindex(cap.index).fillna(0.0)
    pp.insert(0, "parcel_acres", cap.parcel_acres)
    pp["ag_district_rated_acres"] = (cap.a_acres + cap.b_acres + cap.c_acres + cap.d_acres + cap.e_acres).round(2)
    pp["bc_acres"] = (cap.b_acres + cap.c_acres).round(2)
    pp["de_acres"] = (cap.d_acres + cap.e_acres).round(2)
    bcu = pbc.groupby("tmk")["acres"].sum(); deu = pde.groupby("tmk")["acres"].sum()
    bcp = pbc[pbc.crops_2020 == "Pasture"].groupby("tmk")["acres"].sum()
    dep = pde[pde.crops_2020 == "Pasture"].groupby("tmk")["acres"].sum()
    pp["bc_in_ag_use_acres"] = bcu.reindex(cap.index).fillna(0).round(2)
    pp["bc_in_pasture_acres"] = bcp.reindex(cap.index).fillna(0).round(2)
    pp["de_in_ag_use_acres"] = deu.reindex(cap.index).fillna(0).round(2)
    pp["de_in_pasture_acres"] = dep.reindex(cap.index).fillna(0).round(2)
    pp["share_parcel_in_ag_use"] = (pp.ag_use_acres / pp.parcel_acres).clip(upper=1).round(3)
    dom = pivot(p, "tmk")[[SLUG[c] for c in CROPS]]
    pp["dominant_use"] = dom.idxmax(axis=1).where(dom.max(axis=1) > 0, "none_mapped").reindex(cap.index).fillna("none_mapped")
    pp["S0_current_10pct_20ac"] = cap.S0_current_10pct_20ac; pp["S3_20pct_nocap"] = cap.S3_20pct_nocap
    own = pd.read_csv(DATA / "oahu_ag_owners.csv", dtype={"tmk": str}).set_index("tmk")
    pp["owner_resolved"] = own.owner_resolved.reindex(cap.index); pp["owner_type"] = own.owner_type.reindex(cap.index).fillna("unknown")
    pp.index.name = "tmk"; pp.to_csv(DATA / "oahu_parcel_ag_use_2020.csv")
    print("\nparcel rows:", len(pp), " parcels with any mapped ag use:", int((pp.ag_use_acres > 0).sum()))

    # 4. owner type x use (ag-district parcels)
    # parcel_acres is the FULL parcel area (statute base); ag_district_rated_acres is
    # the LSB-rated area inside the ag district, the denominator for use shares.
    ot = pp.groupby("owner_type")[[SLUG[c] for c in CROPS] + ["crop_acres", "ag_use_acres", "parcel_acres", "ag_district_rated_acres", "bc_acres", "de_acres"]].sum().round(1)
    ot["parcels"] = pp.groupby("owner_type").size()
    ot["share_of_rated_ag_land_in_use"] = (ot.ag_use_acres / ot.ag_district_rated_acres).round(3)
    ot = ot.sort_values("ag_district_rated_acres", ascending=False); ot.to_csv(DATA / "oahu_ag_use_2020_by_owner_type.csv")
    pd.set_option("display.width", 200)
    print("\nby owner type:\n", ot[["parcels", "ag_district_rated_acres", "crop_acres", "pasture", "ag_use_acres", "share_of_rated_ag_land_in_use"]])

    # 5. eligible acreage by use. B/C eligibility (S0/S3) is attributed in
    # proportion to the parcel's B/C use composition; D/E acres directly.
    def bc_mix(tmk_series, col):
        m = pbc.pivot_table(index="tmk", columns="crops_2020", values="acres", aggfunc="sum", fill_value=0.0)
        for c in CROPS:
            if c not in m.columns: m[c] = 0.0
        m = m[CROPS].reindex(cap.index).fillna(0.0)
        bc_tot = pp.bc_acres.replace(0, np.nan)
        share = m.div(bc_tot, axis=0).clip(upper=1).fillna(0.0)
        share["not_in_mapped_ag"] = (1 - share.sum(axis=1)).clip(lower=0)
        return share.mul(col, axis=0).sum()
    rows = {"S0_current_10pct_20ac (B/C, by right)": bc_mix(cap.index, pp.S0_current_10pct_20ac),
            "S3_20pct_nocap (B/C)": bc_mix(cap.index, pp.S3_20pct_nocap),
            "S4_all_BC (all B/C, ag district)": bc_mix(cap.index, pp.bc_acres)}
    dm = pde.pivot_table(index="tmk", columns="crops_2020", values="acres", aggfunc="sum", fill_value=0.0)
    for c in CROPS:
        if c not in dm.columns: dm[c] = 0.0
    de_row = dm[CROPS].sum(); de_row["not_in_mapped_ag"] = max(pp.de_acres.sum() - de_row.sum(), 0)
    rows["D/E (uncapped, ag district)"] = de_row
    el = pd.DataFrame(rows).T; el.columns = [SLUG.get(c, c) for c in el.columns]
    el["crop_acres"] = el[[SLUG[c] for c in CROP_ONLY]].sum(axis=1); el["total_acres"] = el[[SLUG[c] for c in CROPS] + ["not_in_mapped_ag"]].sum(axis=1)
    el = el.round(1); el.index.name = "scenario"; el.to_csv(DATA / "oahu_eligible_by_use_2020.csv")
    print("\neligible acreage by 2020 use:\n", el[["crop_acres", "pasture", "seed_production", "not_in_mapped_ag", "total_acres"]])

if __name__ == "__main__":
    main()
