# Available-land map: three layers, method, and totals

Plausibly available solar land on Oahu at <=15% slope totals ~60,200 ac
across four land categories, plus 264 ac of unscreened reservoir surface.
The modeling subset (Layer 2) is 9,936 ac of D/E at <=10% slope plus a
quasi-random 3,778-ac draw of B/C parcels. Figure:
`analysis/figs/paper/f_available_land.png`. Script:
`analysis/available_land_map.py`. Selection file:
`data/oahu_bc_10pct_selection.csv`.

## Category definitions

All ag and military categories are filtered to <=15% slope on the 10 m band
raster (`data/gis/dem/oahu_slope_bands.tif`). The military fee footprint is
removed from the D/E and B/C fills, so categories do not double-count.

| category | definition | source layers |
|---|---|---|
| ag D/E | LSB class D/E in the State Ag district, non-military. Permitted use, no cap, no SUP (HRS 205-2(d)(6)) | `data/gis/lsb_ag.parquet` |
| ag B/C | LSB class B/C in the Ag district, non-military. 10%/20-ac cap; SUP above the cap (HRS 205-4.5(a)(20)-(21)) | `data/gis/lsb_ag.parquet` |
| military ag | DoD fee land inside the Ag district. Available only at DoD discretion via enhanced-use lease (10 USC 2667) | `data/gis/military/oahu_military_screen.parquet` x `data/gis/slud.parquet` |
| durable non-ag | 2 closed golf courses + quarries/landfills/brownfields + urban parcels with `viability_class == durable` | `data/oahu_golf_courses.csv`, `data/oahu_nonag_solar_candidates.csv` |
| reservoirs | OSM `water=reservoir` / `landuse=reservoir` polygons. Floating-solar candidates. Not screened; no slope filter | `data/gis/osm_reservoirs_oahu.json` (Overpass pull 2026-07-24) |

Class A land is absent from the map: solar is banned there with no SUP path
(HRS 205-4.5(a)(20)).

## Acreage totals

| category | acres |
|---|---:|
| Layer 1: ag D/E, <=15% slope | 14,310 |
| Layer 1: ag B/C, <=15% slope | 25,670 |
| Layer 1: military ag, <=15% slope | 14,335 |
| Layer 1: durable non-ag sites, <=15% slope | 5,908 |
| Layer 1: reservoirs (32 polygons, unscreened) | 264 |
| Layer 2: ag D/E, <=10% slope | 9,936 |
| Layer 2: selected B/C (118 parcels, <=10%-slope basis) | 3,778 |

## B/C selection method (Layer 2b)

The target is 10% of total Oahu B/C acreage: 3,437 of 34,370 ac
(`data/cap_scenarios_by_parcel.csv`). The draw pool is smaller than the
universe: parcels qualify by their B/C acreage on <=10% slope, computed as
10 m raster cells with LSB class B/C, slope band 0-10%, outside the military
footprint. Only that portion counts toward the target. The pool is 22,405 ac
across 1,980 parcels.

Procedure (deterministic, seed/skip 42):

1. Join ag-district parcels with B/C acreage to parcel geometry
   (`data/gis/parcels_oahu.parquet`, dissolved by TMK).
2. Overlay a 2-km square grid on the parcel-centroid extent; assign each
   parcel to a cell by centroid. 169 cells are occupied.
3. Place one Halton-sequence point (bases 2, 3; index = 42 + cell order) in
   each occupied cell. Order each cell's parcels by centroid distance to
   that point.
4. Walk cells round-robin, taking the next-nearest unused parcel per cell,
   accumulating each parcel's <=10%-slope B/C acreage, until the total
   reaches the target. Stop.
5. Record the selection: `data/oahu_bc_10pct_selection.csv` (tmk,
   parcel_acres, bc_acres, bc10_acres, grid_cell, selection_rank).

One deviation from a sorted-order walk: cells are visited in a fixed
pseudorandom permutation (numpy RandomState seed 42). The target is reached
after 118 parcels drawn from 118 of the 169 cells, so a sorted west-to-east
sweep would confine the selection to western Oahu. The permutation spreads
the contributing cells island-wide, which is the stated purpose of the grid.

Result: 118 parcels, 3,778 ac on the <=10%-slope basis (8,488 ac of B/C at
all slopes). The 341-ac overshoot is the final parcel crossing the target;
the rule includes it. Median parcel contribution is 2.3 ac; the largest is
622 ac (TMK 161006001).

## Reconciliation with published numbers

- Ag D/E and B/C at <=15% slope INCLUDING the military footprint reproduce
  `data/gis/oahu_lsb_by_slope.csv` exactly: D/E 21,391 ac, B/C 30,852 ac.
  The map's fills show 14,310 and 25,670 ac because the military footprint
  (7,081 D/E ac, 5,182 B/C ac) is drawn as its own category.
- Military ag at <=15% slope is 14,335 ac, matching the fee-x-Ag figure in
  `notes/military-land-solar.md`.
- This map applies NO grid-distance filter. The published near-grid D/E
  figures are smaller: 6,083 ac within 1 km and 13,424 ac within 3 km of a
  mapped 46 kV+ line at <=15% slope
  (`data/gis/oahu_de_neargrid_by_slope.csv`).
- Durable non-ag acreage (5,908 ac at <=15%) sums the `durable` rows of
  `data/oahu_nonag_solar_candidates.csv` plus the two closed golf courses
  (Ko'olau 111 ac, Makaha Valley 131 ac; `data/oahu_golf_courses.csv`).

## Caveats

- Military ag land is available only at DoD discretion. One Oahu solar EUL
  exists to date (Kupono, ~131 ac; `notes/military-land-solar.md`). The
  14,335 ac is a ceiling on a DoD-energy-security scenario, not supply.
- Reservoirs are unscreened: no ownership, drawdown, habitat, or
  structural check. OSM coverage of small ag reservoirs is incomplete.
- No grid-distance filter anywhere on this map. Near-grid availability is
  smaller (see reconciliation).
- The B/C selection is one draw of a random process. Rerun with a different
  `HALTON_SKIP` for sensitivity; the acreage target is fixed, the parcels
  are not.
- The 46 kV network is under-mapped in HIFLD/OSM
  (`analysis/transmission_screen.py`), so thin-line coverage understates
  the real sub-transmission system.
- Parcel B/C-on-slope acreage is raster-derived (10 m cells); parcel-sum
  rasterization error is small (`analysis/slope_screen.py`: median 0.1%,
  95th pct ~2%).
