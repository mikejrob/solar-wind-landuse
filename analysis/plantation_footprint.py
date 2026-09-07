#!/usr/bin/env python3
"""1978-80 plantation footprint vs current zoning, state district, and LSB class.

QUESTION
  Of the sugarcane and pineapple land mapped on Oahu at the end of the
  plantation era (1978-80), how much is agricultural today, and what LSB
  soil classes does the footprint carry? Feeds
  notes/plantation-footprint-1980.md.

SOURCES
  data/raw/alum/alum.shp.zip - State of Hawaii Agricultural Land Use Maps
    (ALUM), field boundaries compiled 1978-80, statewide; vendored from
    https://files.hawaii.gov/dbedt/op/gis/data/alum.shp.zip (fetched
    2026-09-07; the script re-downloads if the zip is absent). Commodity
    codes: S = sugarcane, P = pineapple; the layer PDF (alum.pdf inside the
    zip) documents the rest.
  data/gis/slud.parquet   - state land use district boundaries (A/U/C/R).
  data/gis/lsb.parquet    - Land Study Bureau overall productivity ratings
    (classes A-E). The LSB never rated some lands; coverage gaps are
    reported, denominators for class shares are LSB-rated acres.
  data/gis/pages_zoning_oahu/page_*.geojson - City & County of Honolulu
    zoning (zone_class; AG-1/AG-2 agricultural, C country).
  data/gis/parcels_oahu.parquet - parcel index (tmk9txt), --parcel mode.

METHOD
  Clip ALUM S+P polygons to Oahu (union of Oahu SLUD polygons), intersect
  with each current layer, sum areas in EPSG:26904 meters. Areas are the
  mapped field footprint; they run above harvested-acre statistics because
  field boundaries include roads, mill yards, and fallow rotation land.

OUTPUT
  data/gis/alum_plantation_crosstabs.csv - long table:
    table       one of lsb_class | state_district | county_zone_group |
                county_zone_class | lsb_x_district
    commodity   S | P | S+P
    category    class letter, district code, or zone class
    acres       GIS acres (1 dp)

  --parcel TMK9 prints the LSB and district composition of one parcel
  (e.g. --parcel 192004008 for the Kupehau Solar host parcel).

CAVEATS
  Current-layer vintages are the 2025-26 pulls cached in data/gis/ (see
  docs/DATA_DICTIONARY.md); the comparison is 1978-80 against today, single
  snapshot each. Overlay slivers at layer edges are kept; they are small
  relative to every reported total.
"""

import argparse
import io
import pathlib
import sys
import urllib.request
import zipfile

import geopandas as gpd
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
ALUM_ZIP = ROOT / 'data' / 'raw' / 'alum' / 'alum.shp.zip'
ALUM_URL = 'https://files.hawaii.gov/dbedt/op/gis/data/alum.shp.zip'
CACHE = ROOT / 'cache' / 'alum'
OUT = ROOT / 'data' / 'gis' / 'alum_plantation_crosstabs.csv'
EQ = 26904          # NAD83 / UTM zone 4N, meters
ACRE = 4046.8564224


def load_alum():
    if not ALUM_ZIP.exists():
        ALUM_ZIP.parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(ALUM_URL, timeout=120) as r:
            ALUM_ZIP.write_bytes(r.read())
    CACHE.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(ALUM_ZIP) as z:
        z.extractall(CACHE)
    return gpd.read_file(CACHE / 'alum.shp')


def acres(gdf):
    return gdf.geometry.to_crs(EQ).area / ACRE


def zone_group(z):
    if str(z).startswith('AG'):
        return 'AG'
    if str(z) == 'C':
        return 'Country'
    return 'other'


def parcel_report(tmk9):
    par = gpd.read_parquet(ROOT / 'data/gis/parcels_oahu.parquet')
    lsb = gpd.read_parquet(ROOT / 'data/gis/lsb.parquet')
    slud = gpd.read_parquet(ROOT / 'data/gis/slud.parquet')
    p = par[par.tmk9txt == str(tmk9)]
    if p.empty:
        sys.exit(f'no parcel {tmk9}')
    print(f'parcel {tmk9}: {p.gisacres.sum():.1f} ac (RPAD gisacres)')
    for name, layer, col in [('LSB class', lsb, 'type'),
                             ('state district', slud, 'ludcode')]:
        i = gpd.overlay(p.to_crs(layer.crs), layer[[col, 'geometry']],
                        how='intersection')
        i['ac'] = acres(i)
        comp = i.groupby(col).ac.sum().sort_values(ascending=False)
        print(f'{name}:')
        for k, v in comp.items():
            print(f'  {k}  {v:8.1f} ac')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--parcel', help='TMK9 (e.g. 192004008): report one '
                    'parcel LSB/district composition and exit')
    args = ap.parse_args()
    if args.parcel:
        parcel_report(args.parcel)
        return

    alum = load_alum()
    sp = alum[alum.commodity.isin(['S', 'P'])][['commodity', 'geometry']]

    slud = gpd.read_parquet(ROOT / 'data/gis/slud.parquet')
    oahu = slud[slud.island == 'Oahu']
    mask = oahu.to_crs(sp.crs).union_all()
    sp = sp[sp.geometry.intersects(mask)].copy()
    sp['geometry'] = sp.geometry.intersection(mask)
    sp['ac'] = acres(sp)

    rows = []

    def emit(table, df, col):
        for (com, cat), ac in df.groupby(['commodity', col]).ac.sum().items():
            rows.append((table, com, str(cat), round(ac, 1)))
        for cat, ac in df.groupby(col).ac.sum().items():
            rows.append((table, 'S+P', str(cat), round(ac, 1)))

    lsb = gpd.read_parquet(ROOT / 'data/gis/lsb.parquet').to_crs(sp.crs)
    i_lsb = gpd.overlay(sp, lsb[['type', 'geometry']], how='intersection')
    i_lsb['ac'] = acres(i_lsb)
    emit('lsb_class', i_lsb, 'type')
    for com, g in sp.groupby('commodity'):
        rated = i_lsb[i_lsb.commodity == com].ac.sum()
        rows.append(('lsb_class', com, 'unrated', round(g.ac.sum() - rated, 1)))
    rows.append(('lsb_class', 'S+P', 'unrated',
                 round(sp.ac.sum() - i_lsb.ac.sum(), 1)))

    i_sd = gpd.overlay(sp, oahu.to_crs(sp.crs)[['ludcode', 'geometry']],
                       how='intersection')
    i_sd['ac'] = acres(i_sd)
    emit('state_district', i_sd, 'ludcode')

    pages = sorted((ROOT / 'data/gis/pages_zoning_oahu').glob('page_*.geojson'))
    zon = pd.concat([gpd.read_file(p) for p in pages], ignore_index=True)
    zon = gpd.GeoDataFrame(zon, crs=gpd.read_file(pages[0]).crs).to_crs(sp.crs)
    i_z = gpd.overlay(sp, zon[['zone_class', 'geometry']], how='intersection')
    i_z['ac'] = acres(i_z)
    i_z['zgrp'] = i_z.zone_class.map(zone_group)
    emit('county_zone_group', i_z, 'zgrp')
    emit('county_zone_class', i_z, 'zone_class')

    i_x = gpd.overlay(i_lsb.drop(columns='ac'),
                      oahu.to_crs(sp.crs)[['ludcode', 'geometry']],
                      how='intersection')
    i_x['ac'] = acres(i_x)
    i_x['cat'] = i_x['type'] + '_' + i_x['ludcode']
    emit('lsb_x_district', i_x, 'cat')

    out = pd.DataFrame(rows, columns=['table', 'commodity', 'category', 'acres'])
    out.to_csv(OUT, index=False)
    print(f'wrote {OUT} ({len(out)} rows)')
    for t in ['lsb_class', 'state_district', 'county_zone_group']:
        print(f'\n== {t} (S+P, ac) ==')
        sub = out[(out.table == t) & (out.commodity == 'S+P')]
        print(sub[['category', 'acres']].to_string(index=False))


if __name__ == '__main__':
    main()
