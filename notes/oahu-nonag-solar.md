# Oahu non-agricultural land for grid-scale solar (urban-district screen)

Question: how much NON-AG land on Oahu could host grid-scale solar? Wind is
legally confined to AG/Country zoning under Honolulu Ord. 25-2, so this is a
solar-only screen. The state URBAN district is the live candidate;
CONSERVATION is legally/practically unavailable (acreage noted only).

Date: 2026-07-12. Script chain in scratchpad (step1_urban.py ... step7_fig.py);
outputs: `data/oahu_nonag_solar_candidates.csv`,
`analysis/figs/paper/f_nonag_map.png`.

## Method

1. State Land Use Districts (`data/gis/slud.parquet`), Oahu polygons, EPSG:26904.
   Urban portions intersected with the Honolulu parcel layer
   (`data/gis/parcels_oahu.parquet`, dissolved to one geometry per TMK).
2. Slope screen on the cached 10 m band raster
   (`data/gis/dem/oahu_slope_bands.tif`): per-parcel acres at <=15% (bands
   0-15) and <=30% slope, computed on the URBAN PORTION of each parcel only.
   Candidacy threshold: >= 10 acres at <=15% slope (<=30% variant reported).
   SINGLE-PARCEL basis - no assembly of adjacent sub-10-ac parcels
   (conservative on parcel count; the 10-ac bar is low, so little is lost).
3. Improvement screen: City & County RPAD ASMTGIS table (CadastralTables
   FeatureServer layer 9, taxyr 2026) building vs land assessed value, summed
   over condo suffixes per TMK. `low_improvement` = building value < 10% of
   land value. Owners from OWNALL (layer 5, taxyr 2027, ownseq 0, fee parcel
   preferred). Federal/military parcels identified by owner string +
   `govlands_detailed_oahu.csv` (Public-Federal) and EXCLUDED from candidate
   totals (noted below). Obvious non-solar uses netted out by owner keyword
   (airport, harbor, golf/country club, cemetery).
4. Special sites: OSM Overpass (2026-07-12), landuse=landfill/quarry/brownfield
   in the Oahu bbox; polygon acreage, same slope screen, distance to mapped
   46kV+/138kV lines (`data/gis/oahu_lines_classified.parquet`, HIFLD+OSM).
   Owners looked up via the majority-overlap parcel TMK in RPAD.
5. Distances are parcel/site boundary distances (0 if a line crosses).

## Context acres (SLUD, Oahu)

| district | acres |
|---|---|
| Urban | 104,231 |
| Conservation (not screened - unavailable) | 158,668 |
| Rural | 0 (no Rural-district polygons on Oahu in the SLUD layer) |
| Agricultural (for reference) | 120,789 |

165,760 parcels intersect the Urban district (>0.01 ac of overlap); parcels
cover 93,928 of the 104,231 urban acres (the rest is roads/ROW/unparceled).
950 parcels have >= 9.5 urban acres; 700 pass the >=10 ac at <=15% slope
screen (599 non-military + 101 military).

## Results: urban-parcel candidates (non-military)

| tier | parcels | ac <=15% | ac <=30% | MW @ 7-5 ac/MW (<=15%) |
|---|---|---|---|---|
| all passing slope screen (>=10 ac <=15%) | 599 | 23,714 | 26,894 | 3,390-4,740 |
| low-improvement (bldg < 10% of land value) | 316 | 15,464 | 17,822 | 2,210-3,090 |
| ... excluding airports/harbors | 303 | 11,984 | 14,323 | 1,710-2,400 |
| ... also excluding golf/cemetery (HEADLINE) | 290 | 11,319 | 13,557 | 1,620-2,260 |

Military parcels (noted, excluded): 101 parcels, 16,155 ac at <=15% slope -
Schofield Barracks (~2,600 flat urban ac), JBPHH (~2,200), MCBH Kaneohe
(~1,360), Wheeler and others. A large physical resource, entirely outside
state/county siting control; DOD has its own resilience programs. Qualitative
note only.

Largest headline-tier owners (ac at <=15% slope):
B.P. Bishop Estate / Kamehameha Schools 1,381 (Waiawa); City & County of
Honolulu 1,197; State of Hawaii 953 (+DLNR 410, DHHL 624, HCDA 391, UH 319,
HTDC 132); Makaiwa Hills LLC 741 (Kapolei mauka); D.R. Horton entities 782
(Ho'opili area); North Shore Bay Owner LLC 446 (Turtle Bay area); WT Laulima
Holdings 426; Kapolei Properties (Hunt) 230; HECO itself 168 (Kahe area);
Robinson Kunia Land 149.

## Special-site inventory (OSM; >= 5 ac)

16 mapped sites, 1,344 ac total, 653 ac at <=15% slope; 52 ac overlap the
counted urban parcels -> ~600 net additional flat acres (~85-120 MW).

| site | type | ac total | ac <=15% | km to 46kV+ | km to 138kV | owner (RPAD) |
|---|---|---|---|---|---|---|
| Kapaa Quarry (Kailua) | quarry | 402 | 89 | 0.0 | 0.0 | Kapaa Quarry Holdings LLC (+2 unnamed pits, 43 ac, same owner) |
| Makakilo Quarry | quarry | 184 | 80 | 0.8 | 1.2 | Grace Pacific LLC |
| Pacific Aggregate (Wahiawa) | quarry | 183 | 150 | 0.6 | 7.1 | Sphere LLC |
| Halawa Quarry | quarry | 179 | 80 | 0.0 | 0.0 | Queen Emma Land Co |
| Waimanalo Gulch Sanitary Landfill | landfill | 166 | 56 | 0.0 | 0.0 | City & County of Honolulu |
| unnamed quarry, Kapolei | quarry | 39 | 29 | 1.1 | 1.1 | Grace Pacific LLC |
| Haseko/Hoakalei brownfields (Ewa, 3 polys) | brownfield | 96 | 93 | ~2.5 | ~2.5 | Haseko (Ewa) Inc / Hoakalei Corp (44 ac overlap counted parcels) |
| unnamed quarry, Waialua | quarry | 17 | 16 | 2.6 | 14.3 | Savio Waialua Farmland LLC |
| Mililani brownfield | brownfield | 19 | 19 | 0.4 | 0.4 | Castle & Cooke Homes Hawaii |
| smaller brownfields (Kapolei, Kalihi) | brownfield | 22 | 21 | <1.2 | <1.2 | various |
| PVT landfill (Nanakuli) | landfill | UNVERIFIED | - | - | - | PVT Land Company (UNVERIFIED); NOT mapped in OSM; sits on ag-district land, outside this screen |

Kalaeloa (former Barbers Point NAS) is captured in the parcel screen, not the
OSM inventory: HCDA (391 ac flat), DHHL, Hunt/Kapolei Properties, University
of Hawaii parcels, plus ~2,400 ac of Navy-retained flat land counted under
military. Active solar projects already exist there (e.g., Kalaeloa
Renewable Energy Park).

## Totals and comparison to the ag district

- Headline non-ag candidate supply: ~11,300 ac at <=15% slope on
  low-improvement, non-military urban parcels + ~600 net ac of
  landfill/quarry/brownfield = ~11,900 ac, or ~1,700-2,400 MWac at 5-7 ac/MW.
- Broadest physical envelope (any non-military urban parcel >=10 flat ac,
  regardless of improvement): ~23,700 ac (~3,400-4,700 MW). Military adds
  ~16,200 flat ac more (noted only).
- Ag-district comparison (prior screens): current by-right (10%/20-ac cap)
  ~3,600 B/C ac; near-grid D/E land ~6,100-11,100 ac. So the PHYSICAL non-ag
  urban supply is of the same order as - indeed larger than - the by-right ag
  supply. Physical scarcity of non-ag land is NOT what confines utility-scale
  solar to ag land on Oahu.
- The binding constraint on urban land is ECONOMIC, not physical, and this
  screen does not measure it: median assessed land value in the headline tier
  is ~$124k/ac (p25 $29k, p75 $1.2M) vs low-five-figures for ag land; PPA-level
  solar rents (~$3-5k/ac/yr gross revenue equivalent land rent share) cannot
  compete with urban development values on most of these parcels.
- Much of the headline tier is the ENTITLED HOUSING PIPELINE: D.R. Horton
  (Ho'opili), Makaiwa Hills LLC, Haseko/Hoakalei, Castle & Cooke - vacant
  today, master-planned for residential. Counting it as solar-available would
  put solar in direct competition with housing production.
- The defensible durable non-ag inventory is the special-site + public-land
  slice: quarries/landfills/brownfields (~600-1,300 ac) plus
  state/county/DHHL/HCDA/DLNR/UH flat holdings (~4,000 ac in the headline
  tier: C&C 1,197 + State 953 + DHHL 624 + HCDA 391 + DLNR 410 + UH 319 +
  HTDC 132) - roughly 4,600-5,300 ac, or ~650-1,050 MW - meaningful but well
  short of the multi-GW ag-district resource.

## Caveats

- Improvement-value proxy: assessed (not market) values; "low-improvement"
  includes parks, drainage, beach reserves, and entitled-but-unbuilt
  subdivisions; airports/harbors/golf/cemetery netted out only via owner-name
  keywords (imperfect). 16 candidate TMKs have no RPAD owner row and ~13 no
  value rows (treated as NOT low-improvement -> conservative; largest:
  TMK 194006212, 136 flat ac, no RPAD rows).
- No land-price screen: urban opportunity cost is the real constraint and is
  unmeasured here beyond the assessed-value summary above.
- Single-parcel basis; urban portion of each parcel only; 10 m DEM slope
  bands; rasterization error ~1% typical (see slope_screen.py).
- OSM completeness: PVT landfill unmapped; quarry/brownfield tagging sparse;
  the 46 kV network is under-mapped in HIFLD/OSM, so 46kV+ distances are
  UPPER bounds (138 kV distances are solid).
- Military land excluded from candidate totals; federal ownership identified
  by owner string + govlands table, both current-year snapshots.
- Zoning within the urban district (county residential/industrial/etc.) not
  screened; Honolulu LUO treats utility-scale solar differently across
  county zones - a follow-up if this becomes load-bearing.
