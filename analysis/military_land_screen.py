#!/usr/bin/env python3
"""
Oahu military-land solar screen (Part A of the military/golf reference task).

Tenure classes:
  - state_lease_2029  : STATE land leased to the military, lease expiring 2029
                        (ParcelsZoning layer 35). Oahu subset only. These are
                        the parcels that could return to State control and
                        become a state-land solar-siting decision.
  - fee_or_other      : the rest of the DoD land footprint (ParcelsZoning
                        layer 34) minus the 2029-lease parcels. Mostly
                        federal fee / ceded-land tenure; NOT resolved to
                        deed here (flagged).

For each installation / lease parcel: total acres, acres <=15% and <=30%
slope (cached band raster), and boundary distance to the mapped 46 kV+ and
138 kV network. SLUD district of the majority of the polygon is attached.

Outputs:
  data/oahu_military_land.csv
  data/gis/military/oahu_military_screen.parquet   (geoms for the figure)
"""
from pathlib import Path
import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio
from rasterio import features
from shapely import make_valid
from shapely.ops import unary_union

PROJECT = Path("/Users/michaelroberts/Research/solar-wind-landuse")
GIS = PROJECT / "data" / "gis"
MIL = GIS / "military"
CRS = "EPSG:26904"
M2AC = 4046.8564224
CELL_AC = 100.0 / M2AC  # 10 m raster cell

def branch_of(name):
    n = (name or "").lower()
    if "coast guard" in n: return "Coast Guard"
    if "marine" in n or "mcbh" in n or "klipper" in n: return "Marine Corps"
    if any(k in n for k in ["navy","jbphh","pearl","west loch","waipio","ford island",
            "lualualei","puuloa","laulaunui","mcgrew","pearl city peninsula","white plains"]):
        return "Navy"
    if any(k in n for k in ["air force","hickam","wheeler","kaala","kaena","bellow","bellows"]):
        return "Air Force"
    return "Army"

def load_slope():
    r = rasterio.open(GIS / "dem" / "oahu_slope_bands.tif")
    return r.read(1), r.transform, r

def slope_acres(geom, band, transform, shape):
    # rasterize this geom onto the band grid, count cells by slope band
    m = features.geometry_mask([geom], out_shape=shape, transform=transform,
                               invert=True)
    vals = band[m]
    le15 = np.isin(vals, [1, 2, 3]).sum() * CELL_AC
    le30 = np.isin(vals, [1, 2, 3, 4, 5, 6]).sum() * CELL_AC
    return round(le15, 1), round(le30, 1)

def main():
    band, transform, r = load_slope()
    shape = band.shape

    l34 = gpd.read_file(MIL / "dod_lands.geojson").to_crs(CRS)
    l34 = l34[l34.county == "Honolulu"].copy()
    l35 = gpd.read_file(MIL / "dod_leases_2029.geojson").to_crs(CRS)
    l35 = l35[l35.county == "Honolulu"].copy()
    for g in (l34, l35):
        g["geometry"] = g.geometry.apply(lambda x: make_valid(x) if not x.is_valid else x)

    lines = gpd.read_parquet(GIS / "oahu_lines_classified.parquet")
    net46 = lines.union_all()
    net138 = lines[lines.kv == "138"].union_all()

    slud = gpd.read_parquet(GIS / "slud.parquet").to_crs(CRS)
    slud = slud[slud.island == "Oahu"]
    sdis = {c: slud[slud.ludcode == c].union_all() for c in ["A", "U", "C"]}
    DISNAME = {"A": "Ag", "U": "Urban", "C": "Conservation"}

    def slud_of(geom):
        best, ba = "Conservation", 0.0
        for c, poly in sdis.items():
            a = geom.intersection(poly).area
            if a > ba:
                ba, best = a, DISNAME[c]
        return best

    lease_union = l35.union_all()
    rows = []
    geoms = []

    # ---- 2029 state-lease parcels (layer 35) ----
    for _, x in l35.iterrows():
        g = x.geometry
        ac = g.area / M2AC
        le15, le30 = slope_acres(g, band, transform, shape)
        d46 = g.distance(net46) / 1000
        d138 = g.distance(net138) / 1000
        rows.append(dict(
            name=x.base_name, tenure="state_lease_2029",
            branch=x.branch, owner=x.owner, tmk=str(x.tmk_txt),
            acres=round(ac, 1), acres_le15=le15, acres_le30=le30,
            dist_46kv_km=round(d46, 2), dist_138kv_km=round(d138, 2),
            slud=slud_of(g), lease_state_owned=x.lease_own,
            source="ParcelsZoning MapServer layer 35 (DoD leases expiring 2029)"))
        geoms.append(dict(name=x.base_name, tenure="state_lease_2029",
                          tmk=str(x.tmk_txt), geometry=g))

    # ---- fee/other DoD installations (layer 34 minus 2029-lease) ----
    for _, x in l34.iterrows():
        g0 = x.geometry
        g = g0.difference(lease_union) if g0.intersects(lease_union) else g0
        if g.is_empty or g.area < 1:
            continue
        ac = g.area / M2AC
        le15, le30 = slope_acres(g, band, transform, shape)
        d46 = g.distance(net46) / 1000
        d138 = g.distance(net138) / 1000
        rows.append(dict(
            name=x.base_name, tenure="fee_or_other",
            branch=branch_of(x.base_name), owner="United States (DoD)", tmk="",
            acres=round(ac, 1), acres_le15=le15, acres_le30=le30,
            dist_46kv_km=round(d46, 2), dist_138kv_km=round(d138, 2),
            slud=slud_of(g), lease_state_owned="",
            source="ParcelsZoning MapServer layer 34 (DoD Lands), minus layer-35 lease"))
        geoms.append(dict(name=x.base_name, tenure="fee_or_other", tmk="", geometry=g))

    df = pd.DataFrame(rows)
    gdf = gpd.GeoDataFrame(geoms, crs=CRS)

    # ---- summary ----
    print("=== TENURE SUMMARY (Oahu) ===")
    for t in ["state_lease_2029", "fee_or_other"]:
        s = df[df.tenure == t]
        print(f"{t}: {len(s)} polys  {s.acres.sum():,.0f} ac total  "
              f"{s.acres_le15.sum():,.0f} ac <=15%  {s.acres_le30.sum():,.0f} ac <=30%")
    print("\n2029 state-lease parcels:")
    print(df[df.tenure == "state_lease_2029"][
        ["name","branch","tmk","acres","acres_le15","dist_46kv_km","dist_138kv_km","slud"]]
        .to_string(index=False))

    # near-grid flat (<=15% and <=3km to 46kV+)
    for lab, dcap in [("<=1km", 1.0), ("<=3km", 3.0)]:
        for t in ["state_lease_2029", "fee_or_other"]:
            s = df[(df.tenure == t) & (df.dist_46kv_km <= dcap)]
            print(f"flat(<=15%) & {lab} 46kV+  {t}: {s.acres_le15.sum():,.0f} ac")

    df.to_csv(PROJECT / "data" / "oahu_military_land.csv", index=False)
    gdf.to_parquet(MIL / "oahu_military_screen.parquet")
    print("\nwrote data/oahu_military_land.csv,", len(df), "rows")

if __name__ == "__main__":
    main()
