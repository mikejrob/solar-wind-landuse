# Available-land map: three layers, method, and totals

Plausibly available solar land on Oahu at <=15% slope totals ~76,300 ac
across seven land categories, plus 264 ac of unscreened reservoir surface.
The three military categories added 2026-07-24 (urban fee, ESQD buffer,
Kahuku lease parcel) account for ~22,700 ac of the total and carry heavier
availability caveats than the ag categories. The modeling subset (Layer 2)
is 15,370 ac of all D/E at <=10% slope (military and non-military, of which
5,435 ac is military fee land) plus a quasi-random 3,778-ac draw of B/C
parcels. Figure:
`analysis/figs/paper/f_available_land.png`. Script:
`analysis/available_land_map.py`. Selection file:
`data/oahu_bc_10pct_selection.csv`.

## Category definitions

All ag and military categories are filtered to <=15% slope on the 10 m band
raster (`data/gis/dem/oahu_slope_bands.tif`). Layer-1 masks are mutually
exclusive; the subtractions are listed after the table.

| category | definition | source layers |
|---|---|---|
| ag D/E | LSB class D/E in the State Ag district, non-military (fee footprint and Kahuku lease parcel removed). Permitted use, no cap, no SUP (HRS 205-2(d)(6)) | `data/gis/lsb_ag.parquet` |
| ag B/C | LSB class B/C in the Ag district, non-military (same removals). 10%/20-ac cap; SUP above the cap (HRS 205-4.5(a)(20)-(21)) | `data/gis/lsb_ag.parquet` |
| military ag | DoD fee land inside the Ag district, ESQD footprint removed. Available only at DoD discretion via enhanced-use lease (10 USC 2667) | `data/gis/military/oahu_military_screen.parquet` x `data/gis/slud.parquet` |
| military urban fee | DoD fee land inside the Urban district, ESQD footprint removed. The fee-x-Urban class of `notes/military-land-solar.md` sec. 5. EUL discretion | same |
| military ESQD buffer | The four ordnance/ESQD constraint-tier installations (`viability_flag` in `data/oahu_military_land.csv`; `notes/military-land-solar.md` sec. 2): West Loch Annex, Lualualei, Kipapa Ammo Storage Site, Puuloa Range Training Facility. ESQD arcs restrict occupied structures; unoccupied PV can be compatible — Kupono (42 MW) sits on ESQD-restricted West Loch land | `data/gis/military/oahu_military_screen.parquet` |
| Kahuku lease parcel | TMK 158002002, state land, lease x Ag, Army-retained under the Aug-2025 ROD. 451 ac total, 230 ac at <=15% slope. Drawn with a bold outline and crosshatch | same |
| durable non-ag | 2 closed golf courses + quarries/landfills/brownfields + urban parcels with `viability_class == durable` | `data/oahu_golf_courses.csv`, `data/oahu_nonag_solar_candidates.csv` |
| reservoirs | OSM `water=reservoir` / `landuse=reservoir` polygons. Floating-solar candidates. Not screened; no slope filter | `data/gis/osm_reservoirs_oahu.json` (Overpass pull 2026-07-24) |

Class A land is absent from the map: solar is banned there with no SUP path
(HRS 205-4.5(a)(20)).

### Overlap subtractions (each acre draws in exactly one Layer-1 category)

- ESQD footprint out of the military urban fill: 2,312 ac (West Loch Annex
  and Puuloa are Urban district). Fee x Urban at <=15% is 16,045 ac before
  the subtraction (matching `notes/military-land-solar.md` sec. 5), 13,733
  ac after.
- ESQD footprint out of the military ag fill: 6,354 ac (Lualualei and
  Kipapa are Ag district). Military ag drops from 14,335 to 7,980 ac.
- Kahuku lease parcel out of the civilian ag fills: 64 ac of D/E and 167 ac
  of B/C at <=15%. The parcel is lease tenure, so the fee-footprint mask
  never covered it; before 2026-07-24 those acres drew as civilian ag.
- The ESQD category totals 8,736 ac at <=15%: 2,312 Urban + 6,354 Ag + 70
  ac outside both districts. It is not district-filtered.
- The Kahuku parcel touches no fee-military category (raster overlap 0 ac).

## Acreage totals

| category | acres |
|---|---:|
| Layer 1: ag D/E, <=15% slope | 14,247 |
| Layer 1: ag B/C, <=15% slope | 25,503 |
| Layer 1: military ag (DoD discretion), <=15% slope | 7,980 |
| Layer 1: military urban fee (EUL discretion), <=15% slope | 13,733 |
| Layer 1: military ESQD buffer (unoccupied-PV-compatible), <=15% slope | 8,736 |
| Layer 1: Kahuku lease parcel (Army-retained 2025 ROD), <=15% slope | 230 |
| Layer 1: durable non-ag sites, <=15% slope | 5,908 |
| Layer 1: reservoirs (32 polygons, unscreened) | 264 |
| Layer 2: all D/E, <=10% slope (all tenure) | 15,370 |
| Layer 2:   of which military fee land | 5,435 |
| Layer 2: selected B/C (118 parcels, <=10%-slope basis) | 3,778 |

Layer 2's modeled D/E is ALL ag D/E at <=10% slope, military and non-
military (Mike, 2026-07-24): the modeling assumption is that every D/E
acre is available, so tenure does not subset it. It is drawn as one green
emphasis fill; the military hatches (ag, urban, ESQD) overlay it, so
military D/E reads as green + hatch and private D/E as solid green. The
15,370-ac total is 9,904 ac non-military (the earlier "civilian D/E
<=10%") + 5,435 ac military fee D/E (all of it, ESQD tier included, since
the "all D/E" set ignores the Layer-1 ESQD subtraction) + ~31 ac of
Kahuku D/E. The military share is larger than the 1,604-ac Layer-1
"military ag D/E" figure because that figure excluded the ESQD tier;
Layer 2 does not. The B/C selection is unchanged (still drawn only from
non-military parcels; see below).

## B/C selection method (Layer 2b)

The target is 10% of total Oahu B/C acreage: 3,437 of 34,370 ac
(`data/cap_scenarios_by_parcel.csv`). The draw pool is smaller than the
universe: parcels qualify by their B/C acreage on <=10% slope, computed as
10 m raster cells with LSB class B/C, slope band 0-10%, outside the
fee-military footprint. Only that portion counts toward the target. The pool is 22,405 ac
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

### Military land and the selection (verified 2026-07-24; selection unchanged)

The 2026-07-24 military categories change no input to the selection, and
the regenerated `data/oahu_bc_10pct_selection.csv` is byte-identical to the
committed file. The draw's treatment of military land, verified against the
script:

- The pool basis excludes fee-military cells: a parcel's `bc10_acres`
  counts B/C cells at <=10% slope outside the fee footprint, and the map
  fill uses the same mask. Six selected TMKs straddle the fee boundary
  (177001001, 176001001, 192005026, 158002006, 191010015, 186003042); their
  counted acreage and drawn fills contain no military cells.
- The 2029 state-lease parcels were not masked (lease tenure). The Kahuku
  parcel TMK 158002002 was therefore eligible, with 98.5 ac on the
  <=10%-slope B/C basis, and was not drawn. Its selection probability under
  a different `HALTON_SKIP` is nonzero; a rerun should mask lease parcels
  too.

## Reconciliation with published numbers

- Ag D/E and B/C at <=15% slope INCLUDING the military footprint reproduce
  `data/gis/oahu_lsb_by_slope.csv` exactly: D/E 21,391 ac, B/C 30,852 ac.
  The map's fills show 14,247 and 25,503 ac because the military footprint
  (7,081 D/E ac, 5,182 B/C ac) and the Kahuku lease parcel (64 D/E ac, 167
  B/C ac) are drawn as their own categories.
- Military fee x Ag at <=15% slope is 14,335 ac and fee x Urban is 16,045
  ac, matching `notes/military-land-solar.md` sec. 5 before the ESQD
  subtraction; the map splits them into ag 7,980 + urban 13,733 + the ESQD
  share of each (6,354 and 2,312).
- This map applies NO grid-distance filter. The published near-grid D/E
  figures are smaller: 6,083 ac within 1 km and 13,424 ac within 3 km of a
  mapped 46 kV+ line at <=15% slope
  (`data/gis/oahu_de_neargrid_by_slope.csv`).
- Durable non-ag acreage (5,908 ac at <=15%) sums the `durable` rows of
  `data/oahu_nonag_solar_candidates.csv` plus the two closed golf courses
  (Ko'olau 111 ac, Makaha Valley 131 ac; `data/oahu_golf_courses.csv`).

## Caveats

- All military categories are available only at DoD discretion via
  enhanced-use lease (10 USC 2667), except the Kahuku parcel, which the
  Army retains under the 2025 ROD. One Oahu solar EUL exists to date
  (Kupono, ~131 ac; `notes/military-land-solar.md`). The ~30,700 military
  ac on this map (ag + urban + ESQD + Kahuku at <=15% slope) is a ceiling
  on a DoD-energy-security scenario, not supply;
  `notes/military-land-solar.md` sec. 5 puts net NEW near-grid acreage
  beyond the paper's tallies at ~0.
- The ESQD constraint tiers are a screen-level reading of DESR 6055.09, not
  DoD determinations; "unoccupied-PV-compatible" rests on the Kupono
  precedent (built on ESQD-restricted West Loch land), and the 8,736-ac
  figure includes the ~231 ac already hosting solar there (Kupono plus the
  HECO West Loch array).
- The military urban fee figure counts developed cantonment, housing, and
  airfield land; the constraint tiers in `data/oahu_military_land.csv` mark
  most of it excluded (airfield/airspace, developed/small). EUL discretion
  is the label, not a viability finding.
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
