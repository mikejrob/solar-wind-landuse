#!/usr/bin/env python3
"""
Oahu golf-course solar screen (Part B).

Builds polygons from OSM leisure=golf_course (ways + relations), dedupes,
and for each course computes acreage, <=15%/<=30%-slope acres (cached band
raster), boundary distance to 46 kV+ / 138 kV, State Land Use District,
Honolulu county zoning class, an insolation proxy (leeward-sunny vs
windward-wet by location), and the majority-overlap TMK + RPAD owner.

Operating status / redevelopment / viability are merged from a hand-coded
table (analysis/golf_status.csv) grounded in the research memo; sources are
carried in the notes column.

Outputs:
  data/oahu_golf_courses.csv
  data/gis/military/oahu_golf_screen.parquet
"""
import json
from pathlib import Path
import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio
from rasterio import features
from shapely import make_valid
from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import polygonize, unary_union

PROJECT = Path("/Users/michaelroberts/Research/solar-wind-landuse")
GIS = PROJECT / "data" / "gis"
MIL = GIS / "military"
CRS = "EPSG:26904"
M2AC = 4046.8564224
CELL_AC = 100.0 / M2AC


def osm_polys():
    d = json.load(open(MIL / "osm_golf_oahu.json"))
    rows = []
    for e in d["elements"]:
        t = e.get("tags", {})
        name = t.get("name", "").strip()
        try:
            if e["type"] == "way":
                coords = [(p["lon"], p["lat"]) for p in e["geometry"]]
                if len(coords) < 4:
                    continue
                g = Polygon(coords)
            else:  # relation (multipolygon)
                from shapely.geometry import LineString
                outer_ls, inner_ls = [], []
                for m in e["members"]:
                    if m.get("type") == "way" and "geometry" in m:
                        c = [(p["lon"], p["lat"]) for p in m["geometry"]]
                        if len(c) < 2:
                            continue
                        (inner_ls if m.get("role") == "inner" else outer_ls).append(LineString(c))
                outers = list(polygonize(outer_ls))
                inners = list(polygonize(inner_ls))
                if not outers:
                    continue
                g = unary_union(outers)
                if inners:
                    g = g.difference(unary_union(inners))
        except Exception as ex:
            print("skip", e["type"], e["id"], ex)
            continue
        rows.append({"osm_type": e["type"], "osm_id": e["id"], "name": name,
                     "access": t.get("access", ""), "geometry": g})
    gdf = gpd.GeoDataFrame(rows, crs="EPSG:4326").to_crs(CRS)
    gdf["geometry"] = gdf.geometry.apply(lambda x: make_valid(x) if not x.is_valid else x)
    return gdf


# canonical name + grouping (merge multi-part courses, drop dup mappings)
CANON = {
    "Championship Course": "Hawaii Kai Golf Course",
    "Executive Course": "Hawaii Kai Golf Course",
    "Kealohi Golf Course": "Hoakalei Country Club",
}
DROP_NONAME_KEEP = True  # keep noname polygons, try to name via nearest


def main():
    band = rasterio.open(GIS / "dem" / "oahu_slope_bands.tif").read(1)
    tr = rasterio.open(GIS / "dem" / "oahu_slope_bands.tif").transform
    sh = band.shape

    def sl(g):
        m = features.geometry_mask([g], out_shape=sh, transform=tr, invert=True)
        v = band[m]
        return (round(np.isin(v, [1, 2, 3]).sum() * CELL_AC, 1),
                round(np.isin(v, [1, 2, 3, 4, 5, 6]).sum() * CELL_AC, 1))

    g = osm_polys()
    g["cname"] = g.name.replace("", np.nan).map(lambda x: CANON.get(x, x))
    # dissolve by canonical name (noname stay separate by id)
    g["grp"] = g.apply(lambda r: r.cname if isinstance(r.cname, str) and r.cname
                       else f"__noname_{r.osm_id}", axis=1)
    diss = g.dissolve(by="grp", aggfunc={"name": "first"}).reset_index()

    lines = gpd.read_parquet(GIS / "oahu_lines_classified.parquet")
    net46 = lines.union_all()
    net138 = lines[lines.kv == "138"].union_all()
    slud = gpd.read_parquet(GIS / "slud.parquet").to_crs(CRS)
    slud = slud[slud.island == "Oahu"]
    sdis = {c: slud[slud.ludcode == c].union_all() for c in ["A", "U", "C"]}
    DN = {"A": "Ag", "U": "Urban", "C": "Conservation"}
    zon = gpd.read_file(MIL / "honolulu_zoning.geojson").to_crs(CRS)
    parcels = gpd.read_parquet(GIS / "parcels_oahu.parquet").to_crs(CRS)

    def majority(geom, gdf, col):
        cand = gdf[gdf.intersects(geom)]
        best, ba = "", 0.0
        for _, r in cand.iterrows():
            a = geom.intersection(r.geometry).area
            if a > ba:
                ba, best = a, r[col]
        return best

    rows = []
    outg = []
    for _, r in diss.iterrows():
        geom = r.geometry
        ac = geom.area / M2AC
        if ac < 3:
            continue
        le15, le30 = sl(geom)
        d46 = round(geom.distance(net46) / 1000, 2)
        d138 = round(geom.distance(net138) / 1000, 2)
        dist_sl = max([(geom.intersection(p).area, DN[c]) for c, p in sdis.items()],
                      key=lambda x: x[0])[1]
        zclass = majority(geom, zon, "zone_class")
        tmk = majority(geom, parcels, "tmk9txt")
        c = gpd.GeoSeries([geom.centroid], crs=CRS).to_crs(4326).iloc[0]
        name = r["name"] or r["grp"]
        rows.append(dict(name=name, osm_grp=r["grp"], acres=round(ac, 1),
                         acres_le15=le15, acres_le30=le30,
                         dist_46kv_km=d46, dist_138kv_km=d138,
                         slud=dist_sl, zone_class=zclass, tmk=str(tmk),
                         lon=round(c.x, 4), lat=round(c.y, 4)))
        outg.append(dict(name=name, geometry=geom))

    df = pd.DataFrame(rows).sort_values("acres", ascending=False)
    gdf = gpd.GeoDataFrame(outg, crs=CRS)
    df.to_csv(PROJECT / "data" / "oahu_golf_courses_gis.csv", index=False)
    gdf.to_parquet(MIL / "oahu_golf_screen.parquet")
    print(df.to_string(index=False))
    print(f"\n{len(df)} courses, {df.acres.sum():,.0f} ac total, "
          f"{df.acres_le15.sum():,.0f} ac <=15%")
    # TMKs for RPAD owner lookup
    print("\nTMKS:", ",".join(sorted(set(df.tmk[df.tmk != ""]))))


if __name__ == "__main__":
    main()
