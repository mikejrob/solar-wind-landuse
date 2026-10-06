#!/usr/bin/env python3
"""Classify OSM-mapped Oahu solar plant footprints by state district and LSB class.

QUESTION
  Which built utility-scale solar arrays sit on agricultural-district
  D/E land, which on B/C, which outside the agricultural district?
  Feeds the by-project table in notes/plantation-footprint-1980.md.

SOURCES
  data/raw/osm/oahu_solar_plants_20261006.json - Overpass API snapshot
    (fetched 2026-10-06): every way/relation tagged power=plant with
    plant:source containing "solar" (so hybrids tagged "solar;battery"
    are included) in the Oahu bounding box (21.2,-158.35,21.75,-157.6),
    full geometry. --refresh re-queries and also writes the copy at
    data/gis/osm_solar_plants_oahu.json read by build_webmap.py,
    review_area_screen.py and hcdl_overlay.py. The 2026-09-07 snapshot
    matched plant:source=solar exactly and so missed every hybrid plant.
  data/gis/slud.parquet, data/gis/lsb.parquet - as in
    analysis/plantation_footprint.py.

METHOD
  Assemble each plant's outer polygons, keep plants over 20 GIS acres
  (screens out rooftop/FIT arrays), intersect with SLUD and LSB, report
  acres by district code and soil class. OSM coverage is partial: as of
  the 2026-10-06 snapshot, Kupono and Mountain View have no mapped
  footprint. (The 2026-09-07 snapshot also lacked Mililani I, Ho'ohana,
  AES West O'ahu, and Waiawa Phase 1, an artifact of its exact-match
  filter; their rows in the note come from LUC dockets and permit records.)

OUTPUT
  data/gis/osm_solar_footprints.csv - one row per (plant, layer,
  category): name, centroid, footprint acres, layer (slud|lsb),
  category, acres.
"""

import argparse
import json
import pathlib
import urllib.parse
import urllib.request

import geopandas as gpd
import pandas as pd
from shapely.geometry import Polygon
from shapely.ops import unary_union

ROOT = pathlib.Path(__file__).resolve().parents[1]
SNAP = ROOT / 'data/raw/osm/oahu_solar_plants_20261006.json'
GIS_COPY = ROOT / 'data/gis/osm_solar_plants_oahu.json'
OUT = ROOT / 'data/gis/osm_solar_footprints.csv'
QUERY = ('[out:json][timeout:90];('
         'way["power"="plant"]["plant:source"~"solar"](21.2,-158.35,21.75,-157.6);'
         'relation["power"="plant"]["plant:source"~"solar"](21.2,-158.35,21.75,-157.6);'
         ');out geom;')
EQ = 26904
ACRE = 4046.8564224
MIN_AC = 20


def plants(doc):
    rows = []
    for e in doc['elements']:
        name = e.get('tags', {}).get('name', '?')
        polys = []
        if e['type'] == 'way' and 'geometry' in e:
            pts = [(g['lon'], g['lat']) for g in e['geometry']]
            if len(pts) >= 4:
                polys.append(Polygon(pts))
        elif e['type'] == 'relation':
            for m in e.get('members', []):
                if m.get('role') == 'outer' and 'geometry' in m:
                    pts = [(g['lon'], g['lat']) for g in m['geometry']]
                    if len(pts) >= 4:
                        try:
                            polys.append(Polygon(pts))
                        except Exception:
                            pass
        if polys:
            rows.append({'name': name, 'geometry': unary_union(polys)})
    g = gpd.GeoDataFrame(rows, crs=4326)
    g['ac'] = g.geometry.to_crs(EQ).area / ACRE
    return g[g.ac > MIN_AC].sort_values('ac', ascending=False)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--refresh', action='store_true',
                    help='re-query Overpass and overwrite the snapshot')
    args = ap.parse_args()
    if args.refresh or not SNAP.exists():
        url = ('https://overpass-api.de/api/interpreter?data='
               + urllib.parse.quote(QUERY))
        req = urllib.request.Request(url, headers={
            'User-Agent': 'solar-wind-landuse research (UH Manoa)'})
        with urllib.request.urlopen(req, timeout=180) as r:
            SNAP.parent.mkdir(parents=True, exist_ok=True)
            body = r.read()
        SNAP.write_bytes(body)
        GIS_COPY.write_bytes(body)
    g = plants(json.load(open(SNAP)))

    layers = {'slud': ('ludcode', gpd.read_parquet(ROOT / 'data/gis/slud.parquet')),
              'lsb': ('type', gpd.read_parquet(ROOT / 'data/gis/lsb.parquet'))}
    rows = []
    for _, r in g.iterrows():
        gg = gpd.GeoDataFrame([r], crs=4326)
        c = r.geometry.centroid
        parts = []
        for lname, (col, layer) in layers.items():
            i = gpd.overlay(gg.to_crs(layer.crs), layer[[col, 'geometry']],
                            how='intersection')
            i['a'] = i.geometry.to_crs(EQ).area / ACRE
            comp = i.groupby(col).a.sum().sort_values(ascending=False)
            for k, v in comp.items():
                rows.append({'name': r['name'], 'lat': round(c.y, 4),
                             'lon': round(c.x, 4), 'footprint_ac': round(r.ac, 1),
                             'layer': lname, 'category': k, 'acres': round(v, 1)})
            parts.append(f"{lname}[" + ' '.join(f'{k}:{v:.0f}'
                                                for k, v in comp.items()) + ']')
        print(f"{r['name'][:34]:34s} {r.ac:6.0f}ac ({c.y:.4f},{c.x:.4f}) "
              + ' '.join(parts))
    pd.DataFrame(rows).to_csv(OUT, index=False)
    print(f'wrote {OUT}')


if __name__ == '__main__':
    main()
