#!/usr/bin/env python3
"""
STRETCH: Oahu large-wind setback geometry under Honolulu Ord. 25-2 (2025)
vs the pre-2025 LUO rule.

Data: City & County of Honolulu open geodata "Zoning" layer (LUO zoning
districts, zone_class field), cached by cap_scenarios workflow at
data/gis/pages_zoning_oahu/.

Target land (where large wind could in principle site): AG-1, AG-2, C
(country) zoned lots.

"Sensitive" zones per Ord 25-2 large-wind rule: residential (R-*),
apartment (A-1/2/3, AMX-*), country (C), resort. We also include the state
HCDA-style residential/apartment mixed classes (Apart, ApartMix, ResMix)
as apartment-equivalents. Note: because country (C) is itself a sensitive
zone, all C land is within 1.25 mi of a C boundary, so the post-Ord-25-2
viable area is effectively a subset of AG-1/AG-2 only.

Rules compared (both computed as distance-to-sensitive-zone-boundary
approximations):
  - Ord 25-2: >= 1.25 mi (2011.68 m) from any sensitive-zoned lot boundary.
  - Pre-2025: setback = 1x turbine tip height (~200 m) from property lines.
    APPROXIMATION: we compute target land >= 200 m from sensitive-zone
    boundaries. The real pre-2025 rule applied to the project parcel's own
    property lines (any neighbor, not just sensitive zones), so the true
    pre-2025 viable area is parcel-configuration-dependent; this is an
    upper-bound-flavored screen using the same sensitive set for
    comparability.

CRS: EPSG:26904. Areas in acres (4046.8564224 m2).
"""

import geopandas as gpd
import pandas as pd
from pathlib import Path
from shapely import make_valid

DATA_DIR = Path("/Users/michaelroberts/Research/solar-wind-landuse/data/gis")
M2_PER_ACRE = 4046.8564224
CRS = "EPSG:26904"

TARGET = {"AG-1", "AG-2", "C"}
SENSITIVE = {"C", "Resort", "Apart", "ApartMix", "ResMix",
             "A-1", "A-2", "A-3", "AMX-1", "AMX-2", "AMX-3",
             "R-3.5", "R-5", "R-7.5", "R-10", "R-20"}

MILE = 1609.344
SETBACK_NEW = 1.25 * MILE   # Ord 25-2
SETBACK_OLD = 200.0         # ~1x tip height, pre-2025 approximation


def main():
    pages = sorted((DATA_DIR / "pages_zoning_oahu").glob("page_*.geojson"))
    z = gpd.GeoDataFrame(
        pd.concat([gpd.read_file(p) for p in pages], ignore_index=True),
        crs="EPSG:4326").to_crs(CRS)
    z["geometry"] = z.geometry.apply(
        lambda g: make_valid(g) if g is not None and not g.is_valid else g)
    z = z[z.geometry.notna() & ~z.geometry.is_empty]

    target = z[z.zone_class.isin(TARGET)]
    sens = z[z.zone_class.isin(SENSITIVE)]
    target_u = target.union_all()
    sens_u = sens.union_all()

    total_ac = target_u.area / M2_PER_ACRE
    ag_only = z[z.zone_class.isin({"AG-1", "AG-2"})].union_all()
    ag_ac = ag_only.area / M2_PER_ACRE

    rows = []
    for label, dist in [("ord_25_2_1.25mi", SETBACK_NEW),
                        ("pre2025_200m_approx", SETBACK_OLD)]:
        excl = sens_u.buffer(dist)
        ok = target_u.difference(excl)
        ok_ac = ok.area / M2_PER_ACRE
        ok_ag = ag_only.difference(excl).area / M2_PER_ACRE
        rows.append({"rule": label, "setback_m": round(dist, 1),
                     "agc_total_acres": round(total_ac),
                     "agc_viable_acres": round(ok_ac),
                     "agc_viable_share": round(ok_ac / total_ac, 4),
                     "ag12_total_acres": round(ag_ac),
                     "ag12_viable_acres": round(ok_ag),
                     "ag12_viable_share": round(ok_ag / ag_ac, 4)})
    out = pd.DataFrame(rows)
    out.to_csv(DATA_DIR / "wind_setback_oahu.csv", index=False)
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()
