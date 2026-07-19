# Oahu slope screen: ag-district land by percent-slope band

Run date: 2026-07-12. Script: `analysis/slope_screen.py`.
Figure: `analysis/figs/oahu_slope_bands.png`.
Companion to `notes/oahu-transmission-screen.md` (same grid, same caveats).

## Data and method

- **DEM**: USGS 3DEP 1/3 arc-second (~10 m) tiles `n22w158`, `n22w159`
  (prd-tnm.s3.amazonaws.com StagedProducts, retrieved 2026-07-12), cached in
  `data/gis/dem/`.
- Merged/cropped to the Oahu bbox, reprojected (bilinear) to EPSG:26904 on
  a 10 m grid; percent slope = 100·|∇z| by central differences
  (numpy.gradient), equivalent to GDAL slope up to edge handling. Bands:
  0–5, 5–10, 10–15, 15–20, 20–25, 25–30, >30%.
- LSB-class polygons (ag district), parcels, and 1/3 km buffers of the
  mapped 46 kV+ network were rasterized onto the same 10 m grid; all
  cross-tabs are cell counts (1 cell = 100 m² = 0.0247 ac). The class ×
  slope tabs are therefore polygon-accurate at 10 m resolution. They are not
  allocated from parcel-level shares.
- Raster/vector agreement: the D/E-within-1-km total is 20,360 ac raster vs
  20,359 ac vector. Per-parcel rasterized area vs vector area: median
  absolute error 2.0%; 95th pct 21.3% (driven by sub-acre parcels whose
  boundaries are a large share of their area — negligible in acreage
  aggregates).
- **S3-eligible by slope** requires an allocation rule, because the cap is a
  per-parcel quota; it is not a mapped footprint. Two rules reported in
  `data/gis/oahu_s3_by_slope.csv`: `flattest_first` (fill the parcel's
  quota from its flattest B/C cells up — how a developer would site;
  headline) and `proportional` (uniform over the parcel's B/C cells;
  pessimistic bound).

## LSB class × slope band (Oahu ag district, acres)

| Class | 0–5 | 5–10 | 10–15 | 15–20 | 20–25 | 25–30 | >30 |
|---|---|---|---|---|---|---|---|
| A | 8,886 | 4,889 | 777 | 198 | 109 | 69 | 178 |
| B | 13,953 | 5,777 | 1,771 | 721 | 344 | 185 | 425 |
| C | 4,433 | 3,236 | 1,682 | 913 | 517 | 302 | 619 |
| D | 1,604 | 1,296 | 1,291 | 1,147 | 970 | 730 | 1,430 |
| E | 7,146 | 5,325 | 4,729 | 4,711 | 4,497 | 4,147 | 26,057 |

Validation of LSB semantics: prime soils are flat (85% of class B is under
10% slope), class E is 46% over 30% slope. Slope and soil class are highly
collinear — which is exactly why the slope screen matters for D/E and
barely matters for B/C.

## The money table: D/E ag-district acres near a mapped 46 kV+ line, by slope

(D/E = no acreage cap, no SUP: the zero-legal-friction resource.)

| Within | 0–5 | 5–10 | 10–15 | 15–20 | 20–25 | 25–30 | >30 | ≤15% cum | ≤30% cum | total |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 km | 2,648 | 1,733 | 1,702 | 1,752 | 1,706 | 1,568 | 9,250 | **6,083** | **11,110** | 20,360 |
| 3 km | 5,980 | 3,926 | 3,518 | 3,467 | 3,319 | 3,077 | 17,278 | **13,424** | **23,287** | 40,565 |
| all Oahu | 8,750 | 6,620 | 6,020 | 5,858 | 5,466 | 4,877 | 27,487 | 21,391 | 37,592 | 65,079 |

The unscreened "20,359 ac of near-grid D/E" from the transmission note
shrinks to **6,083 ac at ≤15% slope (~1,217 MW @5 ac/MW, ~869 @7)** and
**11,110 ac at ≤30% (~2,222 MW @5, ~1,587 @7)**; 45% of near-grid D/E is
over 30% slope. Within 3 km: 13,424 ac ≤15% and 23,287 ac ≤30%.

## S3-eligible (20%, no hard cap) acres by slope band

Flattest-first allocation (headline):

| Within 46 kV+ | 0–5 | 5–10 | 10–15 | 15–20 | 20–25 | 25–30 | >30 | ≤15% | ≤30% | total |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 km | 6,136 | 2,753 | 1,132 | 504 | 246 | 136 | 317 | 10,021 (89%) | 10,907 (97%) | 11,224 |
| 3 km | 7,928 | 3,120 | 1,409 | 638 | 322 | 178 | 384 | 12,457 (89%) | 13,595 (97%) | 13,979 |
| all | 9,224 | 3,329 | 1,486 | 672 | 340 | 187 | 404 | 14,040 (90%) | 14,838 (97%) | 15,642 |

Even under the pessimistic proportional allocation, 82–84% of S3-eligible
acres sit at ≤15% slope. **Slope does not blunt the cap-reform result**:
B/C land is flat almost by construction (it is prime ag soil), so nearly
all of the acreage that cap reform (S3) would unlock is on ≤15% terrain,
89% of it within 1 km of a mapped line. By contrast the D/E "no-cap"
envelope loses roughly half its area to a 30% slope screen.

## Caveats

- 10 m DEM smooths microterrain: short steep breaks, rock outcrops, and
  gulch walls narrower than ~20–30 m are averaged away, so band acreage at
  the steep margins is slightly optimistic; conversely bilinear resampling
  can smear flat benches near cliffs into middle bands.
- Percent slope only — no aspect, no solar-irradiance, no flood/gulch
  hydrology, no geotechnical screen.
- Slope bands are terrain, not buildability: drainage, access roads, and
  grading economics vary within a band; Mike's "costs rising in slope"
  premise motivates slope banding. The analysis does not impose a single cutoff.
- Inherits all transmission-screen caveats (46 kV network under-mapped →
  near-grid D/E figures are conservative/understated; no capacity data).
- S3-by-slope depends on the stated allocation rule; both rules bracket it.

## Files

- `analysis/slope_screen.py` — DEM → slope raster → cross-tabs → figure
- `data/oahu_parcel_slope.csv` — TMK-keyed parcel × slope-band acres
  (joins to `oahu_land_transmission.csv`, `cap_scenarios_by_parcel.csv`,
  `oahu_ag_owners.csv`)
- `data/gis/oahu_lsb_by_slope.csv`, `oahu_de_neargrid_by_slope.csv`,
  `oahu_s3_by_slope.csv`
- `data/gis/dem/oahu_slope_bands.tif` — 10 m uint8 slope-band raster
