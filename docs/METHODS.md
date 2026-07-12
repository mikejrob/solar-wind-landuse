# Methods

Concise write-up of each analytical pipeline. Full detail lives in the cited
`notes/*.md` file and in the producing script's docstring; caveats stated
there apply wherever results are used.

Conventions: CRS **EPSG:26904** (NAD83 / UTM 4N; scale distortion <0.1%
across the islands); areas from projected geometry, 1 ac = 4046.8564224 m²;
TMK keys 9-digit statewide. MW conversions use 5 and 7 ac/MWac.

---

## 1. Cap scenarios (S0–S4)

Script: `analysis/cap_scenarios.py` · Notes: `notes/cap-quantification.md`

Quantifies land eligible for utility-scale solar under HRS § 205-4.5(a)(20)
versus counterfactual rules. Inputs (geodata.hawaii.gov ArcGIS REST,
downloaded 2026-07-11, cached in `data/gis/pages_*`): Land Study Bureau
overall-productivity polygons (classes A–E), State Land Use Districts, and
county TMK parcel layers (all four counties). Procedure: repair geometry
(`make_valid`), clip LSB to the Ag District (`ludcode=='A'`), intersect with
parcels, compute per-parcel acres by LSB class. Per parcel, with BC = class
B + C acres (the constrained resource; class A banned, D/E unconstrained):

| Scenario | Eligible acres |
|---|---|
| S0 (current law) | min(0.10 × parcel, 20 ac, BC) |
| S1 | min(0.10 × parcel, BC) — drop the hard ceiling |
| S2 | min(0.20 × parcel, 20 ac, BC) |
| S3 (headline counterfactual) | min(0.20 × parcel, BC) |
| S4 | BC — no cap |

Validation: computed LSB acreage matches Office of Planning 2011 figures
within ~0.2%. Caveats: statutory-eligibility acres, not developable land (no
engineering screens at this stage); parcel ≠ project; the § 205-6 SUP path
above the cap exists since 2014, so S0 measures the *as-of-right* envelope;
~1.5% of Oahu B/C falls outside any TMK. Key result: the hard 20-acre
ceiling, not the 10%, does the constraining, and binds only on parcels
>~200 ac.

## 2. Transmission screen

Script: `analysis/transmission_screen.py` · Notes: `notes/oahu-transmission-screen.md`

Cross-tabulates Oahu ag-district land by LSB class and boundary distance to
the mapped grid. **Line sources** (no public HECO route layer exists):
HIFLD Open "US Electric Power Transmission Lines" (91 Oahu features, source
dates 2017–2020) and OSM Overpass `power=line/minor_line` (87 ways, pulled
2026-07-11). Classification: 138 kV where either source tags it (the two
agree at median 0 m separation → reliable, ~325 km); "46 kV+" = the union of
everything else mapped in either source. **46 kV under-mapping caveat**: the
two sources barely overlap at that tier (~80–140 km mapped vs several
hundred real circuit-km), so distances to 46 kV+ are UPPER bounds and
far-from-grid acreage is overstated; 138 kV numbers are the solid ones.
Distance = polygon boundary distance (0 if a line crosses). Class × band
tabs are polygon-accurate; parcel-level eligible-by-band assigns the whole
parcel to its nearest band (near-grid bias, noted).

## 3. Slope screen

Script: `analysis/slope_screen.py` · Notes: `notes/oahu-slope-screen.md`

**DEM**: USGS 3DEP 1/3 arc-second (~10 m) tiles n22w158 + n22w159
(downloaded 2026-07-12), merged, reprojected bilinear to a 10 m EPSG:26904
grid. Percent slope = 100·|∇z| by central differences (≈ GDAL/Horn).
**Banding**: 0-5, 5-10, 10-15, 15-20, 20-25, 25-30, >30%. All vector layers
are rasterized onto the same 10 m grid; cross-tabs are cell counts (1 cell =
0.0247 ac), polygon-accurate at 10 m. **Allocation rules** for S3-eligible
acres by slope (the cap is a per-parcel quota, not a mapped footprint), both
reported: `flattest_first` — fill the quota from the parcel's flattest B/C
cells up (how a developer sites; headline) — and `proportional` (uniform;
pessimistic bound). Validation: raster vs vector totals agree to <0.1%;
per-parcel median absolute error 2.0%. Caveat: 10 m smooths gulch walls, so
steep-margin acreage is slightly optimistic. Cost context for interpreting
the bands is in `notes/slope-cost-literature.md` (no published continuous
cost-vs-slope curve exists; 15% is a Honolulu grading-permit bright line).

## 4. Transmission expansion (greedy optimization)

Script: `analysis/transmission_expansion.py` (+ `make_expansion_fig_cost.py`)
· Notes: `notes/oahu-transmission-screen.md`

Budget-constrained heuristic: given L km of new line branching off the
mapped 46 kV+ network, maximize B/C/D ag-district acres (class A excluded —
banned; class E excluded per spec) passing the ≤30% slope screen brought
within 1 km of a line. **Greedy procedure** on a 100 m lattice: (a) payoff
G(q) = uncovered eligible acres within a 1 km disk of cell q (FFT
convolution); (b) multi-source Dijkstra from every network cell, 8-connected,
with a 6× length penalty entering cells >30% steep in >30% of their 10 m
subcells; (c) top ~15 approximate scorers re-scored by exact
new-coverage-per-km of the full path; (d) commit the best path in ≤1 km
increments; repeat to ~112 km. **Caveats (always repeat)**: geometric routing
only — no line capacities, substation headroom, or interconnection
engineering; the public 46 kV map is incomplete, so baseline coverage is
understated and some "expansion" may duplicate real unmapped lines; greedy is
approximate; the 1 km service radius is a cost simplification, not a tariff
rule. The cost overlay in `make_expansion_fig_cost.py` uses ~$2.5M/km
(range $1.5–4M/km, MISO benchmarks × island multiplier), wire only.
`corridor_candidates.py` complements this with named cluster ranking
(8-connected components ≥250 buildable ac more than 1 km from the grid,
scored on buildable acres and distinct owners unlocked per km of new ROW).

## 5. Ownership build (OWNALL)

Scripts: `analysis/fetch_ownall.py`, `analysis/resolve_owners.py` · Notes:
`notes/oahu-ownership.md`

Bulk source (no scraping): Honolulu RPAD cadastral tables as hosted ArcGIS
services — owner table **OWNALL** (583,721 rows islandwide, tax year 2027),
queried in 100-TMK batches for the 6,274 Oahu ag-district parcels; RPAD tmk
is the 9-digit TMK minus the county digit. Per-parcel owner = fee parcel
(suffix 0000), ownseq 0, own1. Cross-checked against the state Government
Lands layer. **Entity resolution**: manual mapping for every raw name ≥50 ac
(160 names, 95% of acreage; the `MAP` dict in `resolve_owners.py`) plus
regex heuristics for the tail; every row keeps `owner_raw`, a resolved name,
an `owner_type`, and a confidence flag. **Coverage**: 99.4% of parcels /
99.0% of acreage attributed; 35 parcels (1.0% of acres) have no RPAD row.
Caveats: assessment owner ≠ beneficial owner (DCCA cross-ref deferred);
leaseholds invisible; ag-CPR "owners" can overstate or understate
concentration (flagged per row); qPublic is Cloudflare-blocked.

## 6. SUP census

Data: `data/sup_census.csv` · Notes: `notes/sup-census.md` (documentary; no script)

Frame: the LUC "Completed Dockets — Special Permits" indexes plus the
pending-docket index (the `files.hawaii.gov/luc/dockets/` directory listing
is 403-blocked; individual PDFs fetch with a browser UA). SP dockets are
numbered sequentially statewide; the 2005–2026 sequence was enumerated
continuously (one documented gap, #410), every docket title inspected, and
old dockets with recent motions checked for solar amendments. Per docket:
D&O, county transmittal, staff reports, OP comments, minutes, and testimony
downloaded to `data/raw/dockets/<docket>/`, text-extracted (`pdftotext` +
OCR spot checks), and coded (dates, votes, counsel, intervenors, conditions).
County tier checked by agenda search across all four counties. Result: the
population of LUC solar SUPs is exactly 8, all post-2014, 0 denied, 0
intervenors. Gaps: Maui County ArchiveCenter is 403-blocked even with a
browser UA (UIPA request flagged); Honolulu DPP not full-text searchable.

## 7. Non-ag screen (vacancy proxy)

Data: `data/oahu_nonag_solar_candidates.csv` · Notes: `notes/oahu-nonag-solar.md`
(session-built; step scripts described in the note)

Screens Urban-district Oahu land for solar candidacy: SLUD urban polygons ∩
parcels, per-parcel acres at ≤15% / ≤30% slope computed on the *urban
portion* only (10 m band raster), threshold ≥10 ac at ≤15%, single-parcel
basis (no assembly). **Vacancy proxy**: RPAD ASMTGIS (taxyr 2026) —
`low_improvement` = building assessed value <10% of land assessed value,
summed over condo suffixes. Owners from OWNALL; federal/military identified
and excluded; airports/harbors/golf/cemeteries netted out by keyword.
Special sites (landfill/quarry/brownfield) from OSM. Caveats: assessed ≠
market values; the proxy imperfectly flags parks, drainage, and
entitled-but-unbuilt subdivisions (the headline tier includes the housing
pipeline); no land-price screen — which the note argues is the real
constraint; 46 kV distance caveat applies.

## 8. Wind setback geometry

Scripts: `analysis/wind_setback_oahu.py` (acreage),
`analysis/wind_viable_map.py` (publication map + named-region table) ·
Notes: `notes/wind-setbacks.md`, `notes/cap-quantification.md` (STRETCH
section)

Compares viable large-wind area under Honolulu Ord 25-2 (2025) vs the
pre-2025 LUO rule. Target land: AG-1, AG-2, Country zoning (Honolulu open
geodata LUO layer). Sensitive zones per Ord 25-2: residential R-*, apartment
A-1/2/3 and AMX-*, country, resort (+ mixed residential classes). Rules
computed as distance-to-sensitive-zone-boundary: Ord 25-2 ≥ 1.25 mi
(2011.68 m); pre-2025 ≈ 200 m (~1× tip height). **Approximation caveat**:
the real pre-2025 rule ran from the project parcel's own property lines, so
the pre-2025 figure is an upper-bound-flavored screen using the same
sensitive set for comparability. Result: viable share of AG+C land falls
~85% → ~36%. The legislative/ordinance record behind the rule (measure
chain, setback formulas, sponsors) is hand-tabulated in
`data/wind_setback_bills.csv`.

---

## Data-access workarounds (cross-cutting)

- **capitol.hawaii.gov** returns Cloudflare 403 to all non-browser clients
  (as of 2026-07): every legislative document was retrieved from the Wayback
  Machine using the original-bytes pattern
  `https://web.archive.org/web/<TIMESTAMP>id_/<ORIGINAL_URL>`, cited with
  original URL + capture timestamp. Bill discovery also used diffing of
  dated Wayback snapshots of HRS §§ 205-2/205-4.5 (2003–2015) and archived
  acts-by-year lists. Recipes: `notes/pre2011-solar-bills.md`,
  `notes/acts-2014-2022.md`.
- **Campaign Spending Commission**: the live portals were truncated to
  2015+ in 2025; the 2006–2024 record was recovered from a pre-truncation
  Internet Archive capture (2025-03-31) of the CKAN datastore dump
  (218,392 rows), topped up via the live SODA API. Recipe:
  `notes/campaign-finance.md`, `analysis/campaign_finance_extract.py`.
- Other blocked-to-scripts sources are flagged in the relevant notes:
  qPublic, PUC DMS, Maui County ArchiveCenter, LURF Form 990s on ProPublica,
  and the post-2020 Ethics Commission lobbyist portal (Salesforce,
  JS-only — 2021–26 registrations unchecked, a stated limitation).
