# What the ag district is used for: the HDOA 2020 Agricultural Land Use Baseline overlaid on the solar-cap geography

Analysis run: 2026-09-07. Script: `analysis/ag_baseline_overlay.py`
(geopandas 1.0.1 / shapely 2.0.7, `.venv`). Outputs in `data/`
(`oahu_ag_use_2020_*.csv`, `oahu_parcel_ag_use_2020.csv`,
`oahu_eligible_by_use_2020.csv`).

## Finding

Seventy percent of Oʻahu's agricultural district was not in mapped
commercial agriculture in 2020. The HDOA baseline maps 36,139 ac of
commercial crops and pasture inside the ~120,800-ac district; 21,227 ac is
cropped and 14,912 ac is fenced cattle pasture. On the B/C soils the solar
cap governs, 43% is in mapped use (15,132 of 34,876 ac). On the uncapped
D/E soils, 15% is (10,013 of 65,076 ac), and 87% of that is pasture. Of
the acreage eligible by right under the current cap (3,601 ac), 24% is
cropped, 11% is pasture, and 65% carries no mapped commercial use. The
same split holds for the 20%-no-hard-cap counterfactual (15,657 ac: 23%
cropped, 15% pasture, 62% unmapped). Every acre of existing utility-scale
solar in the district sits on land the 2015 baseline had mapped as pasture
or cropland (Waipio: 515 ac of former pasture, per the report).

## The source

The latest HDOA product is the *2020 Update to the Hawaiʻi Statewide
Agricultural Land Use Baseline* (Perroy & Collier, UH Hilo Spatial Data
Analysis & Visualization Lab, for HDOA; released in two parts, May 2021
and 2022-03-08 with Maui County added). It updates the 2015 baseline
(Melrose et al.), which itself replaced the 1978–80 ALUM maps. There is no
HDOA update after 2020 as of 2026-09-07 (HDOA project pages
https://dab.hawaii.gov/salub/ and https://dab.hawaii.gov/salubreports/;
release https://dab.hawaii.gov/blog/main/agbaselineupdate/).

- Report PDF: https://dab.hawaii.gov/wp-content/uploads/2022/04/2020_Update_Ag_Baseline_all_Hawaiian_Islands_v5.pdf
  (cached `data/raw/hdoa-baseline/`, with text extract).
- GIS layer: geodata.hawaii.gov `LandUseLandCover/MapServer/19` ("2020
  Agricultural Land Use"; fields `crops_2020`, `island`, `acreage`); open
  data item 342ee6c7547f45ddbfc07caf4ca2887d; metadata
  https://files.hawaii.gov/dbedt/op/gis/data/aglanduse_2020.pdf. Cached as
  `data/gis/aglanduse_2020.geojson` (4,836 polygons statewide; 535 Oʻahu).
  Oʻahu source acreage 41,310; recomputed in EPSG:26904, 41,041 (−0.7%).

Method (report App. A1–A2): digitized from WorldView-2/3 imagery
2018–2020, verified by site visits, landowner review, and a public web
portal. Commercial operations only, 3-ac minimum. Field roads, buffers,
packing sheds, and freshly tilled fields are counted; homes, gulches,
reservoirs, fallow papaya rotation, backyard orchards, equestrian, piggery,
and poultry uses are not. Two category definitions matter here:

- *Seed Production* is all land under seed-company control including
  pollen-drift buffers and rotation ground; the industry plants about 25%
  of it at any time. It is a gross operational footprint. Buffer fields
  rotate, so no fixed sub-area is "idle" (reviewer point, B. Plasch,
  2026-09-07; `notes/review-plasch-2026-09.md`).
- *Pasture* is fenced land in active commercial cattle operation (troughs
  or cattle trails visible). Grazed seasonally counts; former pasture now
  military, park, or reforestation does not.

The report's own numbers are counts of "land deployed to support" a use and
run 10% or more above what industries report (App. A1).

The newer product is not HDOA's: the USDA NASS / UH Mānoa (Qi Chen)
*Hawaiʻi Cropland Data Layer*, a 10 m annual raster for 2023, 2024, and
2025 (V2.1 released 2026-06-12; https://www.nass.usda.gov/Research_and_Science/Cropland/Release/index.php;
https://www.hawaii.edu/news/2025/09/12/hawaii-cropland-data-layer/). It is
a satellite classification (random forest, ~94% reported accuracy), not a
field-verified digitization, and is the right tool for change detection
after 2020. Pulled and compared in `notes/hcdl-2023-2025.md`.

## Oʻahu footprint, 2020 (report Table 3)

| category | acres |
|---|---:|
| Diversified crop | 10,595 |
| Seed production | 7,376 |
| Pineapple | 3,437 |
| Flowers / foliage / landscape | 510 |
| Banana | 360 |
| Aquaculture | 300 |
| Tropical fruits | 260 |
| Coffee | 169 |
| Papaya | 164 |
| Taro | 77 |
| Commercial forestry, macadamia | 29 |
| **Crop total** | **23,277** |
| Pasture | 18,035 |
| **Total** | **41,312** |

Change 2015→2020: +495 ac total; crops +924, pasture −429 "mainly due to
the creation of a solar project on former cattle pasture lands in Waipio"
(515 ac, NRG land; report p. 17) and a 359-ac subdivision along H-2.
Important Agricultural Lands: 15,205 ac designated on Oʻahu, 60% in active
use (pasture 4,957; crops 4,188, two-thirds of that seed production).

## Overlay on the ag district and soil classes

Acres of mapped 2020 use by state land-use district
(`data/oahu_ag_use_2020_by_district.csv`):

| district | crops | pasture | total |
|---|---:|---:|---:|
| Agricultural | 21,227 | 14,912 | 36,139 |
| Urban | 1,871 | 2,586 | 4,457 |
| Conservation | 25 | 420 | 445 |

By LSB class inside the ag district (`data/oahu_ag_use_2020_by_soil.csv`;
class totals from `data/gis/lsb_in_ag_district_totals.csv`):

| class | ag-district acres | cropped | pasture | in mapped use | share | not mapped |
|---|---:|---:|---:|---:|---:|---:|
| A | 15,106 | 9,117 | 1,577 | 10,694 | 71% | 4,411 |
| B | 23,177 | 9,436 | 2,192 | 11,628 | 50% | 11,549 |
| C | 11,700 | 1,201 | 2,303 | 3,504 | 30% | 8,196 |
| D | 8,468 | 434 | 2,267 | 2,701 | 32% | 5,768 |
| E | 56,608 | 881 | 6,432 | 7,313 | 13% | 49,295 |
| unrated | — | 159 | 141 | 300 | — | — |
| **B+C** | **34,876** | **10,637** | **4,495** | **15,132** | **43%** | **19,744** |
| **D+E** | **65,076** | **1,314** | **8,699** | **10,013** | **15%** | **55,063** |

Use intensity tracks soil class. Class A, which the statute closes to
solar, is the one class mostly farmed. The B/C classes, where the cap
binds, are half farmed. The D/E classes, where solar is uncapped, are
mostly unmapped, and what use exists is grazing. The largest cropped
B/C uses are diversified crops (5,144 ac), pineapple (2,417 ac), and seed
production (2,377 ac).

"Not mapped" is not "vacant". It includes fallow rotation ground, gulches,
non-commercial homesteads, unfenced range, forest, and land the protocol
excludes by design (App. A1). It is the acreage on which no commercial
agricultural use was visible in 2018–2020 imagery.

## Overlay on the cap scenarios

B/C eligibility is attributed to uses in proportion to each parcel's B/C
use mix; D/E acres are counted directly
(`data/oahu_eligible_by_use_2020.csv`).

| scenario | acres | cropped | pasture | not mapped |
|---|---:|---:|---:|---:|
| S0 current 10%/20-ac (B/C, by right) | 3,601 | 878 (24%) | 392 (11%) | 2,332 (65%) |
| S3 20% no hard cap (B/C) | 15,657 | 3,588 (23%) | 2,327 (15%) | 9,741 (62%) |
| S4 all B/C in district | 34,370 | 10,605 (31%) | 4,491 (13%) | 19,275 (56%) |
| D/E, uncapped | 64,541 | 1,312 (2%) | 8,668 (13%) | 54,561 (85%) |

Within S3 the cropped share is diversified crops 1,460 ac, seed production
1,211 ac, pineapple 634 ac. The modeled 98-parcel B/C draw
(`data/oahu_bc_10pct_selection.csv`, 3,535 ac): 52 of the 98 parcels have
no mapped use; 1,935 ac of the selected parcels' B/C is in mapped use, 307
ac of it pasture.

## By owner type

Denominator is LSB-rated acreage inside the ag district
(`data/oahu_ag_use_2020_by_owner_type.csv`; owner classes from
`data/oahu_ag_owners.csv`).

| owner type | parcels | rated ag-district ac | cropped | pasture | in use |
|---|---:|---:|---:|---:|---:|
| federal | 166 | 22,774 | 681 | 0 | 3% |
| corporate ag (Dole, Kualoa Ranch, Mahi Pono affiliates, seed cos.) | 244 | 20,958 | 7,654 | 4,719 | 59% |
| private estate / trust (KS and others) | 128 | 17,516 | 3,424 | 6,807 | 58% |
| state (ADC, HHFDC, DLNR, UH, DOA) | 558 | 16,592 | 3,263 | 1,210 | 27% |
| unknown / unresolved | 411 | 10,467 | 2,356 | 1,860 | 40% |
| developer (Castle & Cooke, D.R. Horton, Hoʻohana) | 121 | 5,988 | 2,616 | 1,818 | 74% |
| individual | 2,903 | 5,662 | 868 | 299 | 21% |
| nonprofit | 206 | 4,674 | 459 | 516 | 21% |
| corporate other | 380 | 4,298 | 663 | 403 | 25% |
| DHHL | 935 | 2,383 | 64 | 61 | 5% |
| county | 198 | 1,853 | 11 | 106 | 6% |
| utility | 24 | 599 | 6 | 0 | 1% |

The public tiers hold the least-used ag land: federal 3%, DHHL 5%, county
6%, state 27%. The commercial tiers (corporate ag, estates, developers)
are 58–74% in use. This is the same ordering as grid proximity and slope in
`notes/oahu-ownership.md`; the 2020 layer adds that the private
landholders' B/C land is where the farming is.

## Existing solar farms

OpenStreetMap `power=plant` polygons with `plant:source` containing
`solar` for Oʻahu (Overpass pull 2026-10-06,
`data/gis/osm_solar_plants_oahu.json`; table
`data/oahu_existing_solar_osm.csv`, built by
`analysis/review_area_screen.py`): 51 features, 1,849 ac of mapped
footprint, 1,112 ac inside the ag district. LSB mix of the footprint: B 583
ac, C 138, D 224, E 173, A 1. (The 2026-09-07 pull matched
`plant:source=solar` exactly and dropped the four `solar;battery` hybrids
now listed: Mililani I, Waiawa Phase 1, AES West Oʻahu, Hoʻohana.) Kawailoa Solar (49 MW) covers 284 ac (253 ac
class B); Waipio Solar (45.9 MW) 245 ac (243 ac B); West Loch (20 MW) 101
ac (class C); Lanikuhana (14.7 MW) 106 ac (D/E). OSM is incomplete: Mountain View and Kupono
are missing (Barbers Point and Mahi are unbuilt). Waiawa Phase 1 and
Hoʻohana sit in the Urban district; Mililani I on D/E. The named farms sit on B soils, consistent with the SUP
census (`notes/sup-census.md`): utility-scale solar has been built on the
capped classes through the SUP tier, on legacy-landholder parcels that were
in pasture or cane rotation. An independent pass over the same OSM
snapshot (`analysis/osm_footprint_check.py`,
`data/gis/osm_solar_footprints.csv`, `notes/plantation-footprint-1980.md`)
reproduces these class splits and places the plants against the 1978–80
plantation footprint.

## What this changes

1. The cap binds on land that is mostly not farmed. Under current law 65%
   of by-right B/C acreage had no mapped commercial use in 2020; under the
   20%-no-cap rule, 62%. The food-security argument for the cap
   (`notes/sierra-club-food-security.md`) is an argument about potential,
   not current, cropping on those acres.
2. The uncapped D/E tier is grazing land or unmapped. A solar buildout on
   D/E displaces pasture first (8,668 ac in pasture of 64,541), as Waipio
   did. Pasture rents are the low end of the ag rent distribution (reviewer
   assertion, UNVERIFIED with data; `notes/review-plasch-2026-09.md`).
3. Seed-production land (7,376 ac Oʻahu; 1,211 ac inside S3) is one
   operational unit with rotating buffers. It should be treated as in use
   in full, not as 25% planted plus idle buffer.
4. Public owners hold 44,000 ac of rated ag-district land at 3–27% use.
   The state's own 16,592 rated acres are 27% in use. The reviewer expects
   the state to withhold irrigable North Shore fields (Galbraith, Whitmore,
   Wahiawā); the 2020 layer shows most state ag land is elsewhere and
   unused.

## Caveats

- The baseline is a 2018–2020 snapshot, pre-COVID (HDOA release note).
  Post-2020 changes (Mahi Solar, Waiawa, Mililani II, Dole/ADC transfers)
  are not in it. The NASS/UH Cropland Data Layer (2023–2025) comparison is
  in `notes/hcdl-2023-2025.md`.
- Areas are recomputed from geometry in EPSG:26904 and differ from the
  report's `acreage` field by <1% in total.
- Parcel attribution uses the ag-district parcel set from
  `cap_scenarios_by_parcel.csv` (6,274 Oʻahu parcels). 1,199 parcels carry
  mapped use.
- Crop polygons are digitized to field edges, not TMK lines (App. A1), so
  small slivers cross parcel boundaries.
- The owner-type table's "unknown" class is 10,467 rated acres; entity
  resolution is in `analysis/resolve_owners.py`.
