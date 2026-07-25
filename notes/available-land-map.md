# Available-land map: category groups, slope bands, method, and totals

The map shows plausibly available Oahu solar land in two slope bands (Mike,
2026-07-24): a base shade for <=15% slope and a lighter tint of the same hue
for the 15-30% increment. The earlier <=10% threshold is dropped. Ag D/E,
all tenure, is 21,391 ac at <=15% and +16,201 ac at 15-30%; the B/C SUP
envelope is 25,503 / +2,325 ac. Military categories add 30,679 ac at <=15%
(ag 7,980, urban fee 13,733, ESQD 8,736, Kahuku 230), of which the 7,080 ac
of military D/E is already inside the D/E total (D/E is one all-tenure
group). Durable non-ag sites are 5,908 / +1,380 ac; reservoirs 264 ac. The
modeling subset is all D/E at <=15% (21,391 ac, all tenure) plus a
quasi-random 3,535-ac draw of B/C parcels (98 parcels, <=15%-slope basis).
Figure: `analysis/figs/paper/f_available_land.png`. Script:
`analysis/available_land_map.py`. Selection file:
`data/oahu_bc_10pct_selection.csv`.

## Slope bands

Every slope-filled group carries two disjoint bands from the 10 m band
raster (`data/gis/dem/oahu_slope_bands.tif`): the base color for <=15% slope
(bands 0-5, 5-10, 10-15) and a lighter tint for the 15-30% increment (bands
15-20, 20-25, 25-30). Durable sites and reservoirs are point markers (no
slope shading). D/E is a single all-tenure group — the modeling assumes all
D/E is available, so its envelope and modeled subset coincide; military
hatches overlay it, so military D/E reads as green + hatch. B/C is shown as
the full SUP envelope (non-military) plus the modeled 10% draw.

## Category definitions

The subtractions below keep military land, the Kahuku parcel, and the B/C
envelope mutually exclusive; the all-tenure D/E group deliberately overlaps
the military fills (drawn as fill + hatch). Both slope bands take the same
subtractions.

| category | definition | source layers |
|---|---|---|
| D/E ag (all tenure) | LSB class D/E in the State Ag district, ALL tenure (military and non-military). Permitted use, no cap, no SUP (HRS 205-2(d)(6)). This is both the envelope and the modeled subset. Military hatches overlay it | `data/gis/lsb_ag.parquet` |
| B/C ag (SUP envelope) | LSB class B/C in the Ag district, non-military (fee footprint and Kahuku removed). 10%/20-ac cap; SUP above the cap (HRS 205-4.5(a)(20)-(21)) | `data/gis/lsb_ag.parquet` |
| selected B/C | modeled 10%-of-B/C draw (see selection method), drawn on top of the envelope in the darker orange | derived |
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

Two slope bands per group: base <=15% and the +15-30% increment (acres).

| category | <=15% | +15-30% |
|---|---:|---:|
| D/E ag, all tenure | 21,391 | 16,201 |
|   of which military | 7,080 | 3,865 |
| B/C ag (SUP envelope) | 25,503 | 2,325 |
| military ag (DoD discretion) | 7,980 | 3,177 |
| military urban fee (EUL discretion) | 13,733 | 892 |
| military ESQD buffer (unoccupied-PV-compatible) | 8,736 | 1,730 |
| Kahuku lease parcel (Army-retained 2025 ROD) | 230 | 161 |
| durable non-ag sites | 5,908 | 1,380 |
| reservoirs (32 polygons, unscreened) | 264 | — |
| **modeled subset:** all D/E (= row 1) | 21,391 | 16,201 |
| **modeled subset:** selected B/C (98 parcels) | 3,535 | 271 |

The modeled subset is all D/E (row 1, all tenure) plus the 98-parcel B/C
draw. The military share of D/E (7,080 ac at <=15%) is counted once, inside
the D/E total; the military ag/urban/ESQD rows are the same land shown by
tenure and hatch, so the D/E and military rows overlap by that 7,080 ac and
must not be summed. The selected-B/C 15-30% figure (271 ac) is context: the
target counts only the parcels' <=15% B/C.

## B/C selection method (modeled subset)

The target is 10% of total Oahu B/C acreage: 3,437 of 34,370 ac
(`data/cap_scenarios_by_parcel.csv`). Parcels qualify by their B/C acreage
on <=15% slope (10 m raster cells with LSB class B/C, slope bands 0-15%,
outside the fee-military footprint); only that <=15% portion counts toward
the target. The pool is 25,207 ac across 2,031 parcels. The pool basis moved
from <=10% to <=15% when the map dropped the <=10% threshold (2026-07-24);
this re-drew the selection.

Procedure (deterministic, seed/skip 42):

1. Join ag-district parcels with B/C acreage to parcel geometry
   (`data/gis/parcels_oahu.parquet`, dissolved by TMK).
2. Overlay a 2-km square grid on the parcel-centroid extent; assign each
   parcel to a cell by centroid. 172 cells are occupied.
3. Place one Halton-sequence point (bases 2, 3; index = 42 + cell order) in
   each occupied cell. Order each cell's parcels by centroid distance to
   that point.
4. Walk cells round-robin, taking the next-nearest unused parcel per cell,
   accumulating each parcel's <=15%-slope B/C acreage, until the total
   reaches the target. Stop.
5. Record the selection: `data/oahu_bc_10pct_selection.csv` (tmk,
   parcel_acres, bc_acres, bc15_acres, grid_cell, selection_rank).

One deviation from a sorted-order walk: cells are visited in a fixed
pseudorandom permutation (numpy RandomState seed 42). The target is reached
after 98 parcels drawn from 98 of the 172 cells, so a sorted west-to-east
sweep would concentrate the selection. The permutation spreads the
contributing cells island-wide, the stated purpose of the grid.

Result: 98 parcels, 3,535 ac on the <=15%-slope basis. The overshoot is the
final parcel crossing the target; the rule includes it. Median parcel
contribution is 2.0 ac; the largest is 478 ac (TMK 164003021). The draw has
fewer parcels than the earlier <=10% draw (118 parcels, 3,778 ac) because
<=15% parcels each carry more eligible B/C, so fewer are needed to reach the
target; the selected parcel set changed.

### Military land and the selection (verified 2026-07-24)

- The pool basis excludes fee-military cells: a parcel's `bc15_acres` counts
  B/C cells at <=15% slope outside the fee footprint, and the map fill uses
  the same mask.
- The 2029 state-lease parcels were not masked (lease tenure). The Kahuku
  parcel TMK 158002002 was therefore eligible, with 166.4 ac of B/C on the
  <=15%-slope basis, and was not drawn. The script asserts it is absent. A
  rerun should mask lease parcels too.

## Reconciliation with published numbers

- Ag D/E and B/C INCLUDING the military footprint reproduce
  `data/gis/oahu_lsb_by_slope.csv` exactly at both slope cuts: D/E 21,391 ac
  (<=15%) and 37,592 ac (<=30%); B/C 30,852 ac (<=15%) and 33,833 ac
  (<=30%). The D/E fill shows all 21,391 ac (all tenure); the B/C envelope
  fill shows 25,503 ac because the military footprint (5,182 B/C ac) and the
  Kahuku lease parcel (167 B/C ac) are drawn as their own categories.
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
