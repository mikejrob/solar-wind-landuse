# Reviewer comments on land availability (B. Plasch, 2026-09-07): investigation and disposition

Framing (Mike, 2026-09-07): the reviewer's items become **issue labels** on
the available-land accounting, not subtractions. Each flagged area keeps its
acreage in the envelope and the modeled subset and carries a named issue
(public park, refuge, ordnance, farm-lot program, owner preference,
terrain/access, seed rotation). "Exclude" below means "label as a
potential issue"; the acreage tables say how much land each label touches.

The letter is in `docs/reviews/plasch-2026-09-07.md`. Screens run
2026-09-07 with `analysis/review_area_screen.py` (outputs
`data/oahu_review_area_screen.csv`, `data/oahu_review_area_parcels.csv`,
`data/oahu_eligible_by_parcel_size.csv`, `data/oahu_existing_solar_osm.csv`).
Each parcel in the screen is an ag-district parcel from
`data/cap_scenarios_by_parcel.csv`, matched by owner of record
(`data/oahu_ag_owners.csv`) or a lat/lon box. "D/E ≤15%" is the parcel's
D/E acreage scaled by its ≤15%-slope share (`data/oahu_parcel_slope.csv`),
an approximation to the raster basis of the available-land map.

## Summary

The named exclusions are small against the map's modeled subset. The
public parks, the wildlife refuge, the state farm-lot program, the Pūpūkea
park reserve, the Haleʻiwa airstrip parcels, and the Waikāne impact area
total about 910 ac of D/E at ≤15% slope (6% of the modeled 14,247 ac) and
352 ac of S3 B/C (2% of 15,657). The Kahuku motocross track sits on the
Army-retained lease parcel the map already carves out. Kualoa Ranch and the
Waikāne valley floor add about 570 ac of D/E ≤15% and 395 ac of S3. The
"upper Waiʻanae Mountains" contribute almost nothing: the mountain
interior is Conservation district, and the flat D/E land the box-and-grid
screen catches is 80% below 100 m elevation (Waiʻanae valley floor,
Mokulēʻia plain), flagged only because the 46 kV network is under-mapped. The
minimum-size point is already the repository's stranded-segment finding
(`notes/process-cost-channel.md`); a ≥30-ac per-parcel screen passes 81%
of S3 acreage and 80% of D/E ≤15% acreage, and 0% of S0 by construction.
The North Shore Neighborhood Board policy exists: its 2020-02-25
"Resolution Regarding Agriculture" limits renewable-energy projects on
prime ag land to those serving the farm's own operations. The state's
North Shore agricultural commitments are documented and the 2020 HDOA
layer shows no solar on them.

## 1. Areas to remove

| area | reviewer reason | parcels | ag-district ac | D/E ≤15% ac | S3 B/C ac | in B/C draw | disposition |
|---|---|---:|---:|---:|---:|---:|---|
| James Campbell NWR (Kahuku) | federal refuge | 33 | 831 | 358 | 100 | 0 | **exclude** (owner = US Fish & Wildlife Service) |
| Kualoa Regional Park | county park | 2 | 155 | 55 | 31 | 1 parcel, 0.7 ac | **exclude** |
| Patsy T. Mink Central Oʻahu Regional Park | county park | 3 | 15 | 1 | 1 | 0 | **exclude** (park is mostly Urban district; ag slivers only) |
| Waiāhole Valley (HHFDC, ~750 ac, 159 lots) | farm lots used as homes | 93 | 682 | 174 | 90 | 0 | **exclude** from modeled subset; keep as state-tenure envelope |
| Old Haleʻiwa airfield (Puaʻena Point; TMKs 162002031, 162002001, 162001002) | de facto park | 3 | 239 | 200 | 0.4 | 1 parcel, 0.4 ac | **exclude the airstrip**; the three parcels are KS (2) and City (1) and extend beyond the strip (UNVERIFIED which part is the strip) |
| Pūpūkea-Paumalu Park Reserve (TMKs 159005087, 159006018, 159033001, 159003053) | de facto park: mountain-bike/hiking trails | 4 | 714 | 121 | 111 | 0 | **exclude**; TPL bought 1,129 ac from Obayashi (2007), 1,104 ac to State Parks as a Park Reserve, 25 ac to the City; Army ACUB buffer (https://www.tpl.org/media-room/protection-pupukea-paumalu-celebrated-hi). The ag-district parts are these four state/City parcels |
| Kahuku motocross (TMK 158002002) | commercial use | 1 | 451 | 108 | 90 | 0 | **already excluded**: the track (21.6782, −158.0178, naturalatlas.com) sits inside the state-owned, Army-retained 450-ac Kahuku lease parcel, drawn as its own category on the map (`notes/available-land-map.md`) |
| Waikāne Valley Impact Area (TMK 148014006, US/MCBH) | WWII ordnance | 1 | 200 | 3 | 19 | 0 | **exclude**; 159 of 200 ac is >30% slope, so nothing material is at stake |
| Waikāne valley floor around it (non-HHFDC, non-federal) | context | 107 | 1,645 | 206 | 154 | 2 parcels, 11.8 ac | **flag**; Kualoa Ranch 32 parcels, City 14; ask whether the reviewer meant the impact area only |
| Kualoa Ranch (Morgan family) | tourism is the higher use | 64 | 3,687 | 363 | 241 | 1 parcel, 9.8 ac | **flag as owner-preference**, not physical; 1,203 ac in mapped 2020 use (pasture) |
| Upper Waiʻanae Mountains (interior box, >2 km from mapped 46 kV) | terrain, access, grid | 1,481 | 24,065 | 3,086 | 666 | 10 parcels, 64 ac | **no change needed for terrain**: only 61 ac of the flat D/E is above 300 m; the rest is valley floor and the Mokulēʻia plain; see below and the map |

The seven public-park, refuge, HHFDC, and ordnance items together: 912 ac
of D/E at ≤15% slope (6.4% of the modeled 14,247 ac) and 352 ac of S3
B/C (2.2% of 15,657 ac).

Public-park and refuge exclusions are unambiguous and should be
subtracted from the D/E envelope and the B/C selection pool in
`analysis/available_land_map.py` (owner classes `county` park parcels,
`United States - FWS`, `State of Hawaii - HHFDC`). The county class as a
whole is 1,853 rated ag-district acres at 6% mapped use
(`notes/ag-land-use-baseline.md`), so a blanket county-park exclusion costs
little.

Waiʻanae interior. The map `analysis/figs/waianae_screen_map.png`
(`analysis/waianae_screen_map.py`) shows what the screen catches, and it
is not the upper mountains. The 1,481 parcels (671 individual owners, 527
DHHL homestead parcels, 58 state) are the Waiʻanae and Mākaha valley
floors, the Mokulēʻia coastal plain mauka of Farrington Highway, and
Lualualei parcels; the mountain interior around Mt. Kaʻala is
Conservation district and has never been in the accounting. Their D/E
land at ≤15% slope by elevation
(`data/oahu_waianae_screen_by_elevation.csv`, 10 m USGS DEM):

| elevation | screened D/E ≤15% | screened D/E 15–30% | all ag D/E ≤15% in the box |
|---|---:|---:|---:|
| 0–100 m | 2,368 | 616 | 7,274 |
| 100–200 m | 413 | 490 | 1,416 |
| 200–300 m | 118 | 452 | 1,133 |
| 300–500 m | 60 | 384 | 1,299 |
| ≥500 m | 1 | 6 | 16 |

Eighty percent of the screened flat D/E (2,368 of 2,960 ac) lies below
100 m. Above 200 m there is 179 ac, and above 300 m 61 ac. The box's
300–500 m band is the Schofield plateau, not the range. The earlier
statement that the interior holds 22% of the modeled D/E was an artifact
of the under-mapped 46 kV network: Farrington Highway's distribution and
sub-transmission lines are missing from HIFLD and OSM, so valley-floor
parcels test as "far from grid". The reviewer's point stands for the
steep, high ground, and that ground is already outside the modeled subset
by slope and district. What remains open is whether he would also exclude
the Waiʻanae valley floor (DHHL homesteads, small individual lots), which
is a tenure and owner-intent question, not a terrain one.

## 2. Minimum farm size

The reviewer suggests ~6 MW ≈ 30 ac at 5 ac/MW. The repository already
finds that as-of-right B/C parcels (≤20 ac ≈ 4–5 MW) fall below HECO's
>5 MW RFP floor and have no PPA route (`notes/process-cost-channel.md`).
Per-parcel eligible acreage by size bin
(`data/oahu_eligible_by_parcel_size.csv`):

| per-parcel eligible acres | S0 by right | S3 20% no cap | all B/C | D/E ≤15% (parcel approx.) |
|---|---:|---:|---:|---:|
| <5 | 814 | 1,066 | 1,680 | 2,150 |
| 5–20 | 1,087 | 1,177 | 2,382 | 2,351 |
| 20–30 | 1,700 | 767 | 615 | 933 |
| 30–100 | 0 | 3,634 | 4,734 | 4,216 |
| ≥100 | 0 | 9,013 | 24,960 | 17,051 |
| **share ≥30 ac** | **0%** | **81%** | **86%** | **80%** |

A 30-ac per-parcel floor removes about a fifth of S3 and D/E acreage. It
is a lower bound on viable land because adjacent parcels under one owner
aggregate (Kawailoa and Waipio each span 2–3 TMKs,
`data/oahu_existing_solar_osm.csv`). Disposition: report the ≥30-ac
sensitivity alongside the headline; keep the by-right S0 figure as the
statute's own number with the note that none of it clears the floor.

## 3. Existing solar farms on the map

The map does not mark built farms. OSM polygons give 1,373 ac of footprint
on Oʻahu, 925 ac inside the ag district, 680 ac of it on B/C and 236 ac on
D/E (`notes/ag-land-use-baseline.md`, "Existing solar farms"). OSM misses
several plants (Mililani, Mountain View, Kupono, Waiawa 1, Mahi). Disposition:
add an existing-solar layer (OSM plus the project census
`data/hawaii_solar_project_census.csv` for the missing ones, digitized or
TMK-matched) and subtract it from the envelopes. The subtraction is ~2.7%
of the B/C envelope and <2% of D/E.

## 4. Agrivoltaics

The reviewer's cost caveat is right and the paper's §7 states only that the
constraints are "economic — racking height, row spacing, and operations
coordination". NREL's dual-use cost study documents the premium for
elevated and wide-row designs (NREL, *Capital Costs for Dual-Use
Photovoltaic Installations*, 2020, https://docs.nrel.gov/docs/fy21osti/77811.pdf)
and the InSPIRE program's summaries put the vertical-design premium near
20% (https://openei.org/wiki/InSPIRE/Resources). Sheep grazing under
standard racking is the low-cost variant and is what Hawaiʻi SUP
applicants promised (sheep in 5 of 8 dockets, `notes/sup-census.md`). The
reviewer's slaughterhouse point is a supply-chain observation; the 2020
baseline notes the Kalaeloa meat-processing operation as unmapped
(report p. 22). Disposition: one sentence added to paper §7 (template
`paper/land-restrictions-paper.html`; final HTML/PDF not regenerated).

## 5. State commitment to North Shore agriculture; neighborhood-board policy

Documented, and consistent with the repository's finding that ADC's
Oʻahu lands host no solar (`notes/state-land-solar.md` §5.3):

- Galbraith Estate: 1,743 ac bought by Trust for Public Land 2012-12,
  $25 M, ~1,207 ac to ADC and ~511 ac to OHA; ag-only deed restriction
  (https://www.tpl.org/media-room/galbraith-estate-central-oahu-protected-farming).
- Whitmore Village: 257 ac from Dole to ADC 2015-02-26
  (https://environment-hawaii.org/?p=10924).
- Wahiawā Irrigation System and dam: Act 218 (2023) authorized
  acquisition; BLNR approved DLNR's acquisition of the WIS lands 2026-03-27
  (https://dlnr.hawaii.gov/blog/2026/03/27/nr26-34/); ADC board approved
  final terms 2026-04 (https://dbedt.hawaii.gov/blog/26-43/; Civil Beat
  2026-04, https://www.civilbeat.org/2026/04/wahiawa-dam-takeover-state-signs-off-on-acquisition-from-dole/).
  The system irrigates ~2,600 ac of Dole land.
- Central Oʻahu Agriculture and Food Hub: 34-ac ADC site at Whitmore;
  ~$30 M legislative allocation; construction began 2025-11
  (https://www.hawaiipublicradio.org/local-news/2025-11-17/construction-begins-on-central-oahu-agriculture-and-food-hub).

North Shore Neighborhood Board No. 27, "Resolution Regarding Agriculture",
adopted 2020-02-25 (Ag Committee 2020-02-24; chair Kathleen Pahinui):
"BE IT RESOLVED that prime Ag lands be preserved and used in a sustainable
manner for agricultural purposes, local food production, and accessory ag
purposes. Renewable energy projects shall be limited to those that make
the farm's or agriculture company's day-to-day operations more economically
viable." Source: https://www4.honolulu.gov/docushare/dsweb/Get/Document-319276/2020-02_Resolution_Regarding_Agriculture.pdf
(cached `data/raw/nb27/`). This is the policy the reviewer describes; its
text limits renewable projects on prime ag land to farm-serving ones rather
than opposing utility solar by name. The same board's 2013-02-26
"Resolution Regarding Windmill Farms" advocated "that no more windmill
projects be built in Hawaii" after Kawailoa Wind (30 turbines)
(https://www4.honolulu.gov/docushare/dsweb/Get/Document-319277/2013-02_Resolution_Relating_to_Windmill_Farms.pdf;
transcript `data/raw/nb27/2013-02_Resolution_Relating_to_Windmill_Farms.txt`).
Added to `notes/wind-setbacks.md`.

Disposition: cite both in the political-economy discussion. The 2020
resolution is a documented community position against non-farm solar on
prime North Shore ag land; it is organic (board resolution, no
interested-party sponsor visible) and belongs with the HB 2665 (2018)
counterexample to the astroturf hypothesis.

## 6. Seed corn buffers

Confirmed by the HDOA protocol: seed-production acreage is gross land
under seed-company control including pollen-drift buffers and rotation
ground, ~25% planted at any time (2020 report App. A2). Disposition: treat
seed land as fully in use. It is 7,376 ac on Oʻahu, 1,211 ac inside S3
(`notes/ag-land-use-baseline.md`).

## 7. Rents and farmer receptiveness

The reviewer's claims (solar rent ≫ pasture rent; irrigated cropland
competitive; small lots with homes higher; lifestyle farmers unreceptive)
are UNVERIFIED with data in this repository. What the record has: the
state's Act 278 study says solar "confers higher land values with much
greater revenue" than agriculture (CLAUDE.md, verified); HRS
§205-4.5(a)(21) requires SUP-tier solar land be offered for ag co-use at
≥50% below fair-market rent, which Honolulu DPP called unadministrable
(`notes/acts-2014-2022.md`). No pasture, cropland, or solar lease-rate
series is in the repository. The 2020 layer shows small-owner ag land is
21% in mapped use (individual owners, 5,662 rated ac) and concentrated in
Koʻolauloa, the North Shore, and Waiʻanae, consistent with the reviewer's
description. Disposition: open item. Candidate sources: ADC and HDOA
agricultural-park lease schedules, HHFDC Waiāhole rent renegotiation
(2022–23, https://dbedt.hawaii.gov/hhfdc/files/2022/06/2022-0623-II.A.-Waiahole-Valley-Lease-Rent-Renegotiations.pdf),
solar lease rents disclosed in SUP dockets and PUC PPA filings.

## 8. Funded feasibility study with a planning firm

Recorded as a recommendation. It is the survey step this repository cannot
do from public data: owner intent, community-plan conformity, access, and
neighborhood-board positions. The 2020 HDOA layer and the parcel tables
here are the desk inputs such a study would start from.

## Changes made in the repository

- New: `notes/ag-land-use-baseline.md`, `analysis/ag_baseline_overlay.py`,
  `analysis/review_area_screen.py`, the `data/oahu_*_2020*.csv` and
  `data/oahu_review_area_*.csv`, `data/oahu_eligible_by_parcel_size.csv`,
  `data/oahu_existing_solar_osm.csv` tables; `docs/reviews/`;
  `data/raw/hdoa-baseline/`, `data/raw/nb27/`.
- Paper §7: one sentence on agrivoltaic cost premiums (template only).
- `notes/wind-setbacks.md`: NB27 2013 resolution.

## Not yet done (Mike's call)

- Subtract the park/refuge/HHFDC parcels, existing solar footprints, and
  a Waiʻanae-interior or grid-distance screen from the modeled subset in
  `analysis/available_land_map.py` and redraw `f_available_land.png`. The
  script hardcodes `/Users/michaelroberts/...`; the repo now lives under
  `/Users/mike/...`.
- Regenerate `paper/land-restrictions-paper-final.html` and the PDF.
- Clarifications to request from the reviewer (2026-09-07 status):
  1. Motocross: confirm it is the Kahuku Motocross Park on the Army-retained
     Kahuku lease parcel (TMK 158002002). If so, no change is needed.
  2. Pūpūkea trails: confirm the Pūpūkea-Paumalu park reserve (state/City,
     TPL 2007) is the land meant, or name the parcel if it is private land
     abutting it.
  3. Waikāne: the impact area only (TMK 148014006, 200 ac, mostly >30%
     slope), or the whole valley including Kualoa Ranch and City parcels?
  4. Kualoa Ranch: all 64 fee parcels (3,687 ac ag district), or the
     Kaʻaʻawa–Kualoa valley floor around the ranch operation?
  5. Upper Waiʻanae Mountains: the steep interior is Conservation district
     and never counted, and the ag-district flat D/E above 300 m in the
     range is 61 ac. Does he also mean the Waiʻanae and Mākaha valley
     floors (DHHL homesteads, small lots), which the map does count? Send
     him `analysis/figs/waianae_screen_map.png`.
  6. The North Shore Neighborhood Board "policy strongly opposing utility
     solar farms": is it the 2020-02-25 Resolution Regarding Agriculture,
     or a later document?
  7. Haleʻiwa airfield: the strip at Puaʻena Point on KS land, or the
     larger Kawailoa parcel?
  8. Rents: any source for pasture, irrigated-cropland, and solar lease
     rates on Oʻahu (the repository has none).
- Pull the NASS/UH Cropland Data Layer (2023–2025) to update the 2020
  snapshot.
