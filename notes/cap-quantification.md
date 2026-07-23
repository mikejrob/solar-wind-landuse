# Quantifying the HRS § 205-4.5(a)(20) solar cap: eligible acreage under current law vs counterfactuals

Analysis run: 2026-07-11. Script: `analysis/cap_scenarios.py` (Python,
geopandas 1.1.4 / GDAL 3.12.4 via pyogrio; venv-reproducible). All inputs
cached under `data/gis/`; the script re-runs end-to-end offline from cache.

## Question

Under current law, solar on class B/C agricultural-district soils is a
permitted use only up to **min(10% of parcel acreage, 20 acres) per parcel**
(HRS § 205-4.5(a)(20)); class A soils are off-limits entirely; D/E soils are
not constrained by this cap. How much land does the cap actually make
available, versus counterfactual rules — including Mike's headline
counterfactual, "20% without the hard acreage cap"?

## Data (all State of Hawaii geoportal, geodata.hawaii.gov ArcGIS REST; downloaded 2026-07-11)

| Layer | Endpoint | Features | Notes |
|---|---|---|---|
| Land Study Bureau (LSB) overall productivity ratings | `LandUseLandCover/MapServer/3` | 5,560 statewide polygons | field `type` = A–E |
| State Land Use Districts | `ParcelsZoning/MapServer/20` | 906 polygons | `ludcode` A/U/R/C |
| Oahu TMK parcels | `ParcelsZoning/MapServer/11` | 171,953 parcels | no owner field |
| Hawaii County parcels | `ParcelsZoning/MapServer/5` | 135,718 | `majorowner` field |
| Maui County parcels | `ParcelsZoning/MapServer/30` | 51,245 | no owner field |
| Kauai County parcels | `ParcelsZoning/MapServer/9` | 25,119 | `owner` field |
| Honolulu LUO zoning (wind stretch) | `services.arcgis.com/tNJpAOha4mODLkXz/.../Zoning/FeatureServer/0` | 1,950 | `zone_class` |

Downloaded via paginated GeoJSON queries (`resultOffset`, ordered by
objectid, geometryPrecision=6, 0.4 s between requests, resume-safe page
cache in `data/gis/pages_*/`).

## Method

1. **CRS**: everything projected to EPSG:26904 (NAD83 / UTM zone 4N). Not
   formally equal-area, but scale distortion across the islands is <0.1%,
   far below source-polygon noise. Areas from projected geometry;
   1 ac = 4,046.8564224 m².
2. Invalid geometries repaired with `make_valid` (polygonal parts kept).
3. LSB polygons clipped to the State **Agricultural District** (`ludcode ==
   'A'`) — the statute applies to the ag district.
4. Parcels intersected with ag-district LSB polygons → per-parcel acreage by
   LSB class (A, B, C, D, E) plus total parcel acreage (full parcel area,
   since the statute's 10% is "the acreage of the parcel").
5. Per-parcel eligible-for-solar acreage, counting **only B/C area** as the
   capped resource (A is banned; D/E is unconstrained by this provision):
   - S0 current law: `min(0.10 × parcel_acres, 20, BC)`
   - S1 drop hard cap: `min(0.10 × parcel_acres, BC)`
   - S2 20% with hard cap: `min(0.20 × parcel_acres, 20, BC)`
   - S3 20% no hard cap (headline counterfactual): `min(0.20 × parcel_acres, BC)`
   - S4 no cap: `BC`

   The percentage base is the WHOLE parcel's acreage, per the statute
   ("ten per cent of the acreage of the parcel", §205-2(d)(6)(B)); the
   eligible area must sit on B/C soil. Scenario totals therefore relate to
   total B/C acreage only through the per-parcel minimum. Do not divide a
   scenario total by its percentage to infer a B/C base: Oahu S0 (3,601 ac)
   is 10.5% of B/C because 4,505 small-B/C parcels contribute 100% of their
   B/C (10% of a mostly-D/E parcel exceeds its B/C patch) while the 85
   cap-bound parcels contribute 6.8% of theirs; S3 (15,657 ac) is 45.6% of
   B/C, bounded above by S4 (34,370), never by 20%-of-B/C arithmetic.
   Binding-term decomposition (Oahu S0): B/C-exhausted 4,505 parcels /
   419 ac; 20-ac cap 85 parcels / 1,700 ac; 10%-of-parcel 1,684 parcels /
   1,482 ac. Recomputed from `cap_scenarios_by_parcel.csv` 2026-07-23;
   reproduces the published totals exactly.
6. MW-equivalents at 5 ac/MWac and 7 ac/MWac (sensitivity).

## Sanity check vs Office of Planning 2011 LSB figures

Computed LSB acreage (full LSB coverage, this analysis) vs OP 2011:

| Oahu class | This analysis | OP 2011 |
|---|---|---|
| A | 16,023 | 16,031 |
| B | 25,853 | 25,854 |
| C | 14,965 | 14,958 |
| D | 10,560 | 10,561 |
| E | 208,594 | 208,602 |

Statewide B+C: 419,716 ac vs OP's ≈418,701 (+0.2%) — same source layer.

## LSB class acreage WITHIN the State Ag District (context)

| Island | A | B | C | D | E |
|---|---|---|---|---|---|
| Hawaii | 0 | 45,368 | 196,438 | 335,207 | 605,088 |
| Kauai | 9,152 | 26,658 | 24,008 | 18,195 | 64,458 |
| Lanai | 0 | 0 | 4,067 | 18,100 | 22,307 |
| Maui | 30,644 | 17,183 | 32,881 | 38,905 | 113,911 |
| Molokai | 573 | 0 | 3,527 | 37,687 | 68,588 |
| Oahu | 15,106 | 23,177 | 11,700 | 8,468 | 56,608 |

Oahu: **34,877 ac of B/C** ag-district land is the capped resource;
**65,076 ac of D/E** ag-district land is outside this cap (but D/E is
mostly marginal/steep/dry land, much of it far from the grid).
Reconciliation: Oahu Ag District totals 120,789 ac (SLUD layer); LSB-rated
ag land sums to 115,059 ac — ~5,700 ac of ag district carries no LSB
rating (unrated in the source survey).

## Results — Oahu (headline)

Per-parcel eligibility summed over the 6,274 Oahu ag-district parcels that
intersect LSB coverage (2,155 with any B/C area):

| Scenario | Eligible acres | MW @5 ac/MW | MW @7 ac/MW | vs S0 |
|---|---|---|---|---|
| S0 current (10%, 20 ac) | 3,601 | 720 | 514 | — |
| S1 10%, no hard cap | 9,410 | 1,882 | 1,344 | 2.6× |
| S2 20%, 20 ac | 4,743 | 949 | 678 | 1.3× |
| S3 20%, no hard cap | 15,657 | 3,131 | 2,237 | **4.3×** |
| S4 no cap (all B/C) | 34,371 | 6,874 | 4,910 | 9.5× |

Reading:

- The hard 20-acre cap does most of the constraining; the percentage does
  little. Keeping 10% but dropping the 20-ac cap (S1) already adds +5,809 ac
  (+1,162 MW @5 ac/MW). Raising to 20% while keeping the 20-ac cap (S2)
  adds only +1,142 ac.
- Mike's counterfactual (S3, 20% no hard cap) yields **15,657 ac ≈ 3,131 MW**
  vs current-law 3,601 ac ≈ 720 MW — a 4.3× increase, +2,411 MW at
  5 ac/MW. For scale, HECO's entire Oahu Stage 1+2 procurement footprint
  was ~3,000 ac (Civil Beat 2020).
- The 20-ac hard cap actively binds (S0 below the uncapped S1) on **85
  Oahu parcels**, all > ~204 ac. Oahu has **176 parcels above 200 ac** in
  total, **118 of them carrying B/C soil** (the count used in the paper's
  Table 3). Parcels above 200 ac capture **88.6% of the S0→S3 gain** (the
  same 88.6% whether measured over the 85 binding, 118 B/C-bearing, or 176
  total large parcels, since the extra parcels add ~no gain). The top parcel-size decile (>17 ac) holds
  91% of all ag-district B/C acreage. Any relaxation of the hard cap is,
  mechanically, a transfer of development option value to large landowners
  — which is exactly the scarcity-rent structure hypothesized.
- Largest single winners (Oahu TMKs, owner not in GIS layer — resolve via
  qPublic/RPAD): 1-7-7-001-001 (10,052 ac parcel, S0 20 ac → S3 1,440 ac),
  1-7-6-001-001 (4,985 ac, → 831), 1-6-4-002-001 (3,445 ac, → 689),
  1-6-4-003-022 (2,702 ac, → 540), 1-9-2-005-022 (2,399 ac, → 480).

Distribution detail: `data/gis/scenario_by_size_decile.csv` (note: file
reflects the statewide run; Oahu-only figures in this section were computed
from the Oahu subset of `cap_scenarios_by_parcel.csv`).

## Results — statewide (all four counties, 115,856 ag-district parcels)

| Island | S0 current | S1 10% no cap | S2 20%+20ac | S3 20% no cap | S4 all B/C |
|---|---|---|---|---|---|
| Hawaii | 20,043 | 51,157 | 31,353 | 90,241 | 241,784 |
| Kauai | 4,162 | 12,398 | 5,920 | 22,680 | 50,666 |
| Lanai | 71 | 2,627 | 98 | 3,895 | 4,047 |
| Maui | 5,513 | 13,033 | 8,400 | 22,475 | 49,062 |
| Molokai | 588 | 1,668 | 736 | 2,266 | 3,494 |
| Oahu | 3,601 | 9,410 | 4,743 | 15,657 | 34,371 |
| **Statewide** | **33,978** | **90,292** | **51,250** | **157,213** | **383,424** |

(acres; MW equivalents in `data/cap_scenarios_results.csv`.)

- Statewide, S0 → S3 is 34.0k → 157.2k ac (**4.6×**; 6,796 → 31,443 MW at
  5 ac/MW). The 20-ac hard cap binds on 595 parcels statewide; parcels
  >200 ac capture 84.4% of the S0→S3 gain.
- Parcel-level B/C total (383,424 ac) captures 99.6% of the LSB-in-ag
  B/C total (385,007 ac) — the residual is unparceled land.
- Owner concentration (`data/gis/scenario_by_owner_top.csv`; Hawaii County
  `majorowner` is a coarse category, Kauai `owner` is a name field, Oahu and
  Maui GIS layers carry no owner): on Hawaii island the biggest S0→S3
  gainers are Parker Ranch ("PR Mauna Kea": S0 162 ac → S3 15,295 ac),
  DHHL (1,871 → 11,704), Kamehameha Schools (3,012 → 11,296), and State
  lands (1,582 → 11,136); on Kauai, the State ADC (41 → 3,792 ac). The cap
  binds hardest on exactly the large trust/estate/public landholders —
  consistent with the scarcity-rent framing in which relaxation transfers
  option value to them.

## STRETCH — Oahu large-wind setbacks (Ord. 25-2 vs pre-2025)

Using Honolulu LUO zoning (`zone_class`): target land = AG-1 + AG-2 + C
(country) = 108,417 zoned acres (AG-1+AG-2 alone: 105,164). "Sensitive"
zones = all R-*, A-1/2/3, AMX-*, Apart/ApartMix/ResMix, Country, Resort.

| Rule | Setback | Viable AG+C acres | Share | Viable AG-1/2 acres | Share |
|---|---|---|---|---|---|
| Ord 25-2 (2025) | 1.25 mi from sensitive-zone lots | 39,386 | 36.3% | 39,386 | 37.5% |
| Pre-2025 (approx) | ~200 m (≈1× tip height) | 91,856 | 84.7% | 91,856 | 87.3% |

The 1.25-mile rule removes roughly **half of Oahu's agricultural zoning**
from wind eligibility relative to the old tip-height setback (84.7% →
36.3% of AG+C land; the viable remainder is entirely in AG-1/AG-2 since
Country land is within 1.25 mi of its own boundaries by construction).
Caveats: the pre-2025 rule was a setback from the *project parcel's own
property lines* (all neighbors, not just sensitive zones) — our 200 m
screen from sensitive-zone boundaries is an approximation for
comparability; no slope/wind-resource/military-airspace screening.
Script: `analysis/wind_setback_oahu.py`; output
`data/gis/wind_setback_oahu.csv`.

## Caveats (both analyses)

- **No engineering screens**: no slope, flood, gulch, grid-distance,
  substation-capacity, or irrigation-infrastructure screening. These
  scenario acreages are *statutory* eligibility, not developable land. The
  binding comparison is across scenarios, not levels.
- **Parcel ≠ project**: developers assemble multiple parcels/leases; the cap
  is per-parcel, so S0 could in principle be stacked across many small
  parcels — but the top decile owns 91% of B/C land, so assembly of small
  parcels cannot replicate the counterfactual.
- **SUP path exists**: since 2014, § 205-4.5(a)(21)/§ 205-6 allows solar
  above the cap on B/C soils via county Special Use Permit (with ag-rent
  and decommissioning conditions). S0 measures the *as-of-right* (permitted
  use) envelope — the thing the cap actually rations is freedom from the
  discretionary SUP process.
- The statute's cap applies "whichever is lesser" of 10%/20 ac; we apply it
  to total parcel area per the statutory text ("ten per cent of the
  acreage of the parcel").
- LSB coverage is incomplete on some islands (no A on Hawaii island, etc. —
  matches the source data); ~1.5% of Oahu ag-district B/C acreage falls
  outside any TMK parcel (roads/gaps/slivers).
- Owner names: not present in the Oahu GIS layer (Hawaii County
  `majorowner` and Kauai `owner` fields captured where available in
  `cap_scenarios_by_parcel.csv`; Oahu owners resolvable via qPublic/RPAD by
  TMK — top-20 TMKs listed above are the priority lookups).
- Areas computed in EPSG:26904; UTM scale error <0.1% at Hawaii latitudes.

## Files

- `analysis/cap_scenarios.py` — download + analysis, reproducible from cache
- `analysis/wind_setback_oahu.py` — wind stretch
- `data/cap_scenarios_results.csv` — island × scenario totals
- `data/cap_scenarios_by_parcel.csv` — parcel-level detail
- `data/gis/lsb_sanity_totals.csv`, `lsb_in_ag_district_totals.csv`,
  `scenario_by_size_decile.csv`, `scenario_by_owner_top.csv` (non-Oahu),
  `wind_setback_oahu.csv`
