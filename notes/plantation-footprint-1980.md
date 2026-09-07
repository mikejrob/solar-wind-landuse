# The 1978-80 plantation footprint: what it is zoned now, what soils it carries, and where solar actually sits

Oahu's mapped 1978-80 sugarcane and pineapple footprint is 50,700 acres.
Three quarters of it is still agricultural today (74% county AG-1/AG-2,
72% state agricultural district). Of the acreage the Land Study Bureau
rated, 78% is class A or B — the classes HRS § 205-4.5 excludes from
as-of-right solar or caps at 10%-of-parcel/20 acres. The utility-scale
solar record matches the statute's geometry: of ~339 MW built on Oahu,
107 MW reached B-bearing parcels through the SUP pathway, 114-178 MW
sits partly or wholly outside the agricultural district (urban district,
federal land), and the D/E as-of-right category — the bulk of every
published land screen — holds one verified project, Lanikuhana
(14.7 MW). Computations: `analysis/plantation_footprint.py` →
`data/gis/alum_plantation_crosstabs.csv`; per-array footprints:
`analysis/osm_footprint_check.py` → `data/gis/osm_solar_footprints.csv`.

## 1. The footprint [V]

Source: State ALUM field boundaries, compiled 1978-80
(`data/raw/alum/alum.shp.zip`, sha256 74ae4883…, fetched 2026-09-07 from
https://files.hawaii.gov/dbedt/op/gis/data/alum.shp.zip). Oahu clip:

| commodity | acres |
|---|---|
| Sugarcane (S) | 37,689 |
| Pineapple (P) | 13,007 |
| total | 50,696 |

These are mapped field boundaries, which include roads, mill yards, and
fallow rotation; harvested-acre statistics for the same era run lower
(~45,000).

## 2. Zoning and district survival [V]

| layer | still ag | converted |
|---|---|---|
| County zoning | AG-1/AG-2 37,302 ac (74%); Country 6 ac | 13,372 ac (26%) |
| State district | agricultural 36,527 ac (72%) | urban 14,083 ac (28%); conservation 87 ac |

Largest converted county-zone classes: R-5 residential 3,472 ac, P-2
public 2,290 ac, A-1/A-2 apartment 2,497 ac, F-1 military/federal
1,238 ac, BMX-3 940 ac (full detail in the output CSV, table
`county_zone_class`).

## 3. Soil class [V]

LSB rated 39,921 of the 50,696 acres; 10,775 acres carry no rating.
Shares below are of rated acres.

| class | sugar | pineapple | S+P | share |
|---|---|---|---|---|
| A | 13,521 | 34 | 13,556 | 34% |
| B | 9,250 | 8,412 | 17,662 | 44% |
| C | 3,821 | 948 | 4,769 | 12% |
| D | 744 | 853 | 1,597 | 4% |
| E | 1,513 | 825 | 2,337 | 6% |

Sugar land is 47% class A; pineapple is 76% class B. The still-ag subset
keeps the same mix: A+B 78%, D/E 10% (output CSV, table
`lsb_x_district`). The island's flat, cleared, previously-irrigated,
transmission-adjacent land is prime-rated land; D/E acreage sits almost
entirely outside the old plantation core.

## 4. Where built utility-scale solar sits, by land bucket

Soil classes for the SUP tier come from the LUC dockets
(`data/sup_census.csv`); routes for the rest from
[[sup-census]] ("dogs that didn't bark" table),
[[project-pipeline-mortality]], and OSM-mapped array footprints
intersected with the SLUD and LSB layers
(`analysis/osm_footprint_check.py`, snapshot 2026-09-07). Footprint
checks confirm the SUP-tier docket soils: Waipiʻo array 243 of 245 ac
class B; Kawailoa array 253 of 284 ac class B.

| bucket | projects | MW | share of ~339 MW built |
|---|---|---|---|
| Ag district, B/C via SUP [V] | Waipiʻo (B, ALISH prime/unique), Kawailoa (majority B, panel areas on A and B, IAL), AES West Oʻahu (B 46 ac of 96) | 107.4 | 32% |
| Urban district, ex-plantation [V] | Hoʻohana (A92-683 boundary-amendment route) | 52 | 15% |
| Federal land, ch. 205 inapplicable [V] | Kūpono, West Loch (Navy West Loch Annex; West Loch's footprint carries a nominal ag-district code and LSB class C — ch. 205 does not bind the federal landlord) | 62 | 18% |
| Ag district, D/E as-of-right [V] | Lanikuhana (footprint 106 ac: D 61, E 45) — the one verified D/E build | 14.7 | 4% |
| Mixed urban / ag-E [V] | Eurus Waianae (2017, pre-RFP; footprint 144 ac: urban 92, ag-district class E 52) | 27.6 | 8% |
| Ag district, mechanism unresolved [U] | Mililani I (D/E soils or parcel structuring — flagged in [[sup-census]]; sits in the ex-pineapple belt this note maps at 76% class B, 2 km from Lanikuhana's D/E footprint) | 39 | 12% |
| District unverified [P] | Waiawa (KS master-plan lands; the adjacent Waiawa Phase 2 footprint is 271 of 271 ac urban district) | 36 | 11% |

Floors for the "share off D/E" claim, counting every unresolved MW as
D/E and attributing Eurus proportionally (52/144 of its footprint on
class E → 10 MW): built capacity off D/E ≥ (339 − 14.7 − 39 − 10)/339
= 81%. Adding withdrawn capacity (Kupehau 60 D/E-verified, Mehana 6.6,
Barbers Point 15, Kaukonahua 6 unknown): ≥ 296.6/426.3 = 69.6%,
i.e. roughly 70%. An unidentified 41-ac array on Navy Waipiʻo
Peninsula (OSM "Waipio Peninsula", ~11 MW [U]) would push the combined
floor to 70.3% if counted as federal.

Mahi (120 MW, PPA approved, construction expected 2026) is 65% class B
with 69.5 acres IAL (SP21-412), extending the SUP tier. The one project
verified on D/E land is Kupehau (cancelled 2021, on-site cultural
resources): its 1,272-acre host parcel is 96% D/E
(`analysis/plantation_footprint.py --parcel 192004008`; TMK from the
2020 CIA notice, https://kawaiola.news/nuhou/hoolahalehulehu/public-notice-september-2020/).

## 5. Reading

The published land screens (NREL PV-Alt-1, HECO IGP, HSEO; adopted by the
Switch-Oahu electricity model) draw most of their acreage from uncapped
D/E land and admit B/C only through the capped as-of-right draw plus a
priced SUP pathway. The built record runs the other way: developers site
on the old plantation core — A/B land — and reach it through the SUP
tier, the urban district, or federal leases. Both facts can hold because
the statute prices the routes: the plantation core is flat, cleared, and
near transmission, and the SUP record shows the pathway costs time and
conditions and denies nothing ([[sup-census]], `docs/sup-receipts.md`:
all four Oahu dockets approved unanimously, zero intervenors; statewide
7 of 7 decided, ~181-day median). The screens'
D/E-heavy composition is a statutory-eligibility map; observed siting is
a cost map.

## Open items

- Mililani I footprint soils [U]: no OSM footprint as of the 2026-09-07
  snapshot; settle with imagery digitization over `data/gis/lsb.parquet`.
  Lanikuhana, 2 km away on the same ex-pineapple lands, resolved to
  D 61 / E 45 ac, which supports the D/E-soils explanation for the
  missing SP docket. (Resolved 2026-09-07: Lanikuhana, via OSM footprint.)
- Waiawa (Clearway, 36 MW) state district [P]: adjacent Waiawa Phase 2
  footprint is 100% urban district; Phase 1 needs its own footprint or
  TMK to move to [V].
- OSM "Waipio Peninsula" array (41 ac, ~11 MW, Navy Waipiʻo Peninsula)
  [U]: identify the project and operator; unmapped in the project census.
- Kaukonahua Solar (6 MW, cancelled) parcel [U].
- Hoʻohana, AES West Oʻahu, Kūpono, Mililani I, Waiawa Phase 1 lack OSM
  footprints; the census rows for them rest on dockets and permit records.
