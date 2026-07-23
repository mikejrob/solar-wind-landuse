# Calculation audit

Audit run 2026-07-23. Every derivable number in the repository was recomputed
from its committed source CSV (python3/pandas; script logic documented per
section below). Result: **131 claims checked; 118 match; 8 mismatch;
5 not recomputable from committed data.** Two committed CSVs are malformed
(unquoted commas) and fail a standard pandas parse. Verdicts: MATCH (exact or
within rounding), MISMATCH (both numbers stated, likely cause), NOT-RECOMPUTABLE
(source data absent from the repository), CAUTION (recomputes, but the published
statement needs a qualifier). Nothing was fixed; this file reports.

Context: the cap-scenario "apparent inconsistency" (scenario sums vs total B/C)
was already resolved and documented 2026-07-23 — the statute's percentage
applies to whole-parcel acreage, so scenario totals relate to total B/C only
through the per-parcel minimum (`notes/cap-quantification.md` step 5). This
audit re-verified that decomposition exactly (§1, rows 1.14–1.16).

## 1. Cap scenarios

Source: `data/cap_scenarios_by_parcel.csv` (115,856 parcels), compared against
`data/cap_scenarios_results.csv`, `notes/cap-quantification.md`, `README.md`,
`docs/INVESTIGATIONS.md`, `paper/land-restrictions-paper-final.html`.

| # | Claim | Published | Recomputed | Verdict | Note |
|---|---|---|---|---|---|
| 1.1 | Scenario formulas S0–S4 per parcel | min-of definitions | max abs diff 0.001 ac (file rounds to 3 decimals) | MATCH | parcel file internally consistent |
| 1.2 | Oahu S0/S1/S2/S3/S4 acres | 3,601 / 9,410 / 4,743 / 15,657 / 34,370–34,371 | 3,601.1 / 9,409.8 / 4,743.0 / 15,656.5 / 34,370.4 | MATCH | S4 = 34,370.5 → both roundings appear |
| 1.3 | Island rows Hawaii/Kauai/Lanai/Maui/Molokai | note table | max diff vs results CSV 0.4 ac | MATCH | per-parcel rounding |
| 1.4 | Statewide S0 / S3 | 33,978 / 157,213 | 33,978.1 / 157,212.9 | MATCH | |
| 1.5 | MW at 5 and 7 ac/MW (all rows) | e.g. Oahu 720/514, 3,131/2,237 | acres/5 and acres/7 exact | MATCH | `cap_scenarios_results.csv` mw columns = acres/5, acres/7 |
| 1.6 | Oahu S3/S0 ratio | 4.3× | 4.35 | MATCH | |
| 1.7 | Statewide S3/S0 ratio | 4.6× | 4.63 | MATCH | |
| 1.8 | S1−S0 Oahu +5,809 ac (+1,162 MW); S2−S0 +1,142; S3−S0 +2,411 MW | note | 5,808.8 / 1,161.8 / 1,141.9 / 2,411 | MATCH | |
| 1.9 | 85 Oahu parcels where 20-ac cap binds, all >~204 ac | 85 | 85 (min parcel 203.7 ac) | MATCH | |
| 1.10 | 176 Oahu parcels >200 ac; 118 with B/C | 176 / 118 | 176 / 118 | MATCH | |
| 1.11 | Parcels >200 ac capture 88.6% of S0→S3 gain (same over 85/118/176 sets) | 88.6% | 88.6% for all three sets | MATCH | |
| 1.12 | Statewide: cap binds on 595 parcels; >200 ac capture 84.4% of gain | 595 / 84.4% | 595 (S1−S0 > 0.01 ac; 596 at exact zero) / 84.4% | MATCH | threshold artifact of 3-decimal rounding |
| 1.13 | 6,274 Oahu parcels, 2,155 with any B/C | 6,274 / 2,155 | 6,274 / 2,155 at B/C > 0.01 ac (2,360 at > 0) | MATCH | "any B/C" = above the file's 0.01-ac resolution |
| 1.14 | Binding-term decomposition: B/C-exhausted 4,505 / 419 ac; 20-ac cap 85 / 1,700; 10% 1,684 / 1,482 | note step 5 | 4,505 / 419; 85 / 1,700; 1,684 / 1,482 | MATCH | sums to 3,601 |
| 1.15 | S0 = 10.5% of Oahu B/C; S3 = 45.6%; binding-85 contribute 6.8% of their B/C | note / paper §6 | 10.5% / 45.6% / 6.8% | MATCH | |
| 1.16 | Top decile (>17 ac) holds 91% of B/C | 91% | threshold 17.1 ac; 91.4% | MATCH | |
| 1.17 | Top winners: 1-7-7-001-001 (10,052 ac, 20→1,440), 1-7-6-001-001 (4,985→831), 1-6-4-002-001 (3,445→689), 1-6-4-003-022 (2,702→540), 1-9-2-005-022 (2,399→480) | note | identical, and these are the top 5 by S0→S3 gain | MATCH | |
| 1.18 | ~90% of S3 at ≤15% slope | note/paper | 89.7% (flattest-first, all Oahu; 89.3% within 1 km) from `data/gis/oahu_s3_by_slope.csv` | MATCH | proportional rule gives 83–84%, as disclosed |
| 1.19 | 72% of S3 within 1 km of a 46 kV+ line | note/paper | 71.7% (band CSV), 71.8% (parcel join `data/oahu_land_transmission.csv`) | MATCH | |
| 1.20 | S0: 64% within 1 km, 82% within 3 km; S3: 89% within 3 km | note | 64.0% / 81.7% / 89.4% | MATCH | |
| 1.21 | Statewide owner gainers: PR Mauna Kea 162→15,295; DHHL 1,871→11,704; KS 3,012→11,296; State 1,582→11,136; Kauai ADC 41→3,792 | note | identical from parcel file owner field | MATCH | `data/gis/scenario_by_owner_top.csv` consistent |
| 1.22 | Size-decile file sums to statewide totals | — | decile S0 sums to 33,978 | MATCH | `data/gis/scenario_by_size_decile.csv` is the statewide run, as the note flags |

## 2. B/C totals and district reconciliation

Sources: `data/gis/lsb_in_ag_district_totals.csv`, `data/gis/lsb_sanity_totals.csv`,
parcel file.

| # | Claim | Published | Recomputed | Verdict | Note |
|---|---|---|---|---|---|
| 2.1 | Oahu ag-district B/C (soil-polygon basis) | 34,877 | 23,177 + 11,700 = 34,877 | MATCH | |
| 2.2 | Oahu B/C (parcel-intersection basis) | 34,370 | 34,370.4 | MATCH | |
| 2.3 | Each published use cites the right basis | — | verified: 34,877 in `notes/cap-quantification.md` context table, paper Table 1, transmission cross-tab; 34,370/34,371 wherever parcel sums are meant (`notes/oahu-ownership.md`, S4 rows); paper "~34,900-acre B/C total" = 34,877 rounded | MATCH | no cross-basis citation found |
| 2.4 | Statewide ag-district B/C | 385,007 | 385,007 | MATCH | |
| 2.5 | Parcel B/C = 99.6% of soil-polygon B/C | 383,424 / 99.6% | 383,424.2 / 99.6% | MATCH | |
| 2.6 | Oahu D/E in ag district | 65,076 | 65,076 | MATCH | |
| 2.7 | Ag district ~120,800 ac; LSB-rated 115,059; ~5,700 unrated | note | 120,789 − 115,059 = 5,730 | MATCH / NOT-RECOMPUTABLE | 120,789 comes from the SLUD layer (Zenodo deposit, not in git); committed CSVs are consistent with it |
| 2.8 | ~32% of Oahu | README/paper | 120,789 / ~382,500 ac (597.6 mi²) = 31.6%; at 386,000 ac = 31.3% | MATCH | rounds to "roughly 32%"; Oahu land area itself is external |
| 2.9 | OP-2011 sanity comparison (16,023 vs 16,031 etc.) | note | CSV side reproduced exactly; OP figures external | MATCH (CSV side) | statewide full-LSB B+C 419,716 confirmed |

## 3. Transmission / distance bands

Sources: `data/gis/oahu_class_by_band.csv`, `data/gis/oahu_eligible_by_band.csv`,
`data/oahu_land_transmission.csv`.

| # | Claim | Published | Recomputed | Verdict | Note |
|---|---|---|---|---|---|
| 3.1 | B/C within 1 km: 13,944; within 3 km: 26,222 (75%) | note/paper | 13,944 / 26,222 / 75.2% of 34,876 | MATCH | |
| 3.2 | D/E within 1 km: 20,359 (~4,100–2,900 MW); within 3 km 40,562 | note | 20,359 / 4,072 MW @5 / 2,908 @7 / 40,562 | MATCH | README's "~20,400" is this number rounded |
| 3.3 | All-class ag land within 1 km ≈ 42,800 (paper abstract) | 42,800 | 42,800.4 | MATCH | A 8,497 + B/C 13,944 + D/E 20,359 |
| 3.4 | 138 kV-only D/E within 1 km: 8,824 (~1,750 MW) | note | 8,823 / 1,765 MW | MATCH | rounding |
| 3.5 | Eligible-by-band table internally consistent | — | S0 bands sum 3,601; S3 bands sum 15,658 (vs 15,657 parcel total) | MATCH | 1-ac rounding |
| 3.6 | Band table vs parcel file | — | S0 1-km 2,306 and S3 1-km 11,234 identical in both files | MATCH | |
| 3.7 | Unlock clusters row values (14,368 = 1,551/2,789/10,029, 2,563 MW; 6,950 = 126/225/6,599, 1,365 MW) | note | identical in `data/gis/oahu_unlock_clusters.csv`; MW = (BC+DE)/5 | MATCH | |
| 3.8 | Corridor table acreages (C01 9,742/14,210/2,842 MW/3.9 km/3,644 ac-per-km/18 owners; C03 4,835/5,697; C02 6,479/8,749; C04 3,132/5,618) | note | identical in `data/gis/oahu_corridor_candidates.csv` | MATCH | |
| 3.9 | Corridor top-owner percentages, C01–C03 | note: C01 "US 26%, Island Palm 12%, Corteva 10%"; C03 "Laukiha'a 34%, Dole 26%, KS 19%"; C02 "US 55%, State 10%" | CSV: C01 US 33%, Island Palm 15%, Dillingham 6%; C03 Laukiha'a 39%, Dole 27%, KS 14%; C02 US 57%, State 11% | MISMATCH | note's owner shares predate the class-A-exclusion regeneration of the CSV; acreages were updated, owner percentages were not |
| 3.10 | 1–3 km ring: B/C 10,686/11,842; D/E 7,341/12,177; 28 owners ≥100 ac | note | identical in `data/gis/oahu_ring_1_3km_summary.csv` | MATCH | |

## 4. Slope

Sources: `data/gis/oahu_de_neargrid_by_slope.csv`, `data/gis/oahu_s3_by_slope.csv`,
`data/gis/oahu_lsb_by_slope.csv`, `data/oahu_parcel_slope.csv`.

| # | Claim | Published | Recomputed | Verdict | Note |
|---|---|---|---|---|---|
| 4.1 | Near-grid D/E: 6,083 ≤15% / 11,110 ≤30% / 20,360 total (1 km) | note/paper/README | 6,083 / 11,109.6 / 20,360 | MATCH | |
| 4.2 | 3-km row: 13,424 / 23,287 / 40,565 | note | identical | MATCH | |
| 4.3 | All-Oahu D/E row: 21,391 / 37,592 / 65,079 | note | identical; also equals D+E of `oahu_lsb_by_slope.csv` (65,078) | MATCH | |
| 4.4 | 45% of near-grid D/E >30% slope | note/paper | 45.4% | MATCH | |
| 4.5 | MW conversions (1,217/869 @≤15; 2,222/1,587 @≤30) | note/paper | 6,083/5=1,217; /7=869; 11,110/5=2,222; /7=1,587 | MATCH | |
| 4.6 | S3-by-slope, flattest-first: 1 km 10,021 (89%) ≤15, 10,907 (97%) ≤30, total 11,224; 3 km 12,457/13,595/13,979 | note | 10,021 / 10,907 / 11,224; 12,456 / 13,593 / 13,977 | MATCH | 1–2 ac rounding |
| 4.7 | Flattest-first "all" row: ≤15 14,040 (90%), **≤30 14,838 (97%)**, total 15,642 | note table | ≤15 14,039 (89.7%); **≤30 = 15,237 (97.4%)**; total 15,641 | MISMATCH | ≤30 cumulative is a typo: 14,040+672+340+187 = 15,238, not 14,838; the "(97%)" share is correct |
| 4.8 | Proportional rule: 82–84% of S3 ≤15% | note | 83.3–83.6% | MATCH | |
| 4.9 | 85% of class B under 10% slope; class E 46% over 30% | note | 85.1% / 46.0% | MATCH | |
| 4.10 | Paper Table 8 D/E column (2,648/1,733/1,702/1,752/1,706/1,568/9,250) and S3 column (6,136/2,753/1,132/504/246/136/317) | paper | identical to the two CSVs' 1-km rows | MATCH | |
| 4.11 | Raster-vs-vector agreement 20,360 vs 20,359 | note | confirmed (both files) | MATCH | |

## 5. Ownership

Sources: `data/oahu_ag_owners.csv`, `data/oahu_owner_class_transmission.csv`.

| # | Claim | Published | Recomputed | Verdict | Note |
|---|---|---|---|---|---|
| 5.1 | Totals: 210,130 ac; B/C 34,370; S0 3,601; S3 15,657 | note | identical | MATCH | |
| 5.2 | Coverage 6,239/6,274 parcels (99.4%); 208,119/210,130 ac (99.0%); confidence 5,122/757/360; source 6,238 bulk + 1 govlayer | note | identical | MATCH | |
| 5.3 | Government owns 50.1% | note/paper/README | 50.1% (state 25.8, federal 19.6, county 2.7, DHHL 2.0) | MATCH | |
| 5.4 | KS 26,839 ac = 12.8% of district, 26.1% of private (102,893 ac) | note/paper | 26,839 / 12.8% / 26.1% of 102,894 | MATCH | private = total − government − 2,011 unattributed |
| 5.5 | Top-20 private hold 71.2% of private; top 1/5/10 = 26.1/44.3/56.9 | note/paper | 71.2 / 26.1 / 44.3 / 56.9 | MATCH | |
| 5.6 | All-owner top-k: 18.7 / 57.2 / 67.8 / 79.1 / 89.9 / 94.6; n = 3,457; Gini 0.978 | note | identical; Gini 0.978 | MATCH | |
| 5.7 | B/C top-k: 14.9 / 48.3 / 65.1 / 78.2 | note | identical | MATCH | |
| 5.8 | Top-20 owner table (State 39,331; USA 38,563; KS 26,839; DLNR 9,213; PRI 6,294; C&C 5,588; …) | note | identical | MATCH | all 20 rows |
| 5.9 | Top-20 B/C table (USA 5,128; State 3,581; KS 3,466; Dole 2,688; …) | note | identical to 1 ac | MATCH | |
| 5.10 | Owner-type table (state 54,260/6,567/781/2,242; federal 41,096/6,485/386/3,929; …) | note | identical, with unknown 9,636 + unattributed 2,011 split as printed | MATCH | |
| 5.11 | Cap-bound set: 118 parcels; 114,296 ac; 25,198 B/C; S0 1,825; S1 7,633; hard cap removes ~5,800 ac | note | 118 / 114,296 / 25,198 / 1,825 / 7,633 / 5,809 | MATCH | |
| 5.12 | Cap-bound owner rows (USA 14/4,649/172/2,197; KS 12/3,210/221/1,402; Dole 2/2,308/40/324; … Robinson 3/179/60/167) | note | all 15 rows identical | MATCH | |
| 5.13 | "76% of all cap-bound land sits with just the entities below" | 76% | the 15 listed entities hold 82.1% of cap-bound B/C (81.3% of cap-bound parcel acreage); no basis tested yields 76% | MISMATCH | likely stale from an earlier entity list or basis; the table rows themselves are exact |
| 5.14 | KS forgoes ~1,180 ac (S1−S0) on cap-bound parcels | ~1,180 | 1,182 | MATCH | |
| 5.15 | S0 top-10 (State 440 = 12.2%, USA 279 = 7.7%, KS 273 = 7.6%, …) | note | identical | MATCH | |
| 5.16 | S3 top-10 (USA 3,618 = 23.1%, KS 2,293 = 14.6%, State 1,136, …); KS share 7.6%→14.6% | note | identical | MATCH | |
| 5.17 | Paper Table 3, all 25 cells (parcel size × owner scale, B/C acres) | paper | identical cell-for-cell (e.g. >1,000-ac row 5,107/3,169/5,876/0/0) | MATCH | owner scale = total holdings; governments broken out; unattributed (2,011 ac) falls in large-private |
| 5.18 | Paper: cap-bound parcels — governments 49, large+major private 43, exposed mid-size 26 parcels / 26 owners / ~3,700 B/C, small owners 0; "25,200 B/C acres"; 20–200-ac parcels ≈6,100 B/C | paper | 49 / 43 (27+16) / 26 / 26 / 3,674 / 0 / 25,198 / 6,110 | MATCH | |

## 6. Censuses

Sources: `data/sup_census.csv`, `data/hawaii_solar_project_census.csv`,
`data/community_resistance_cases.csv`, `data/oahu_solar_project_pipeline.csv`,
`data/heco_procurement_timeline.csv`.

| # | Claim | Published | Recomputed | Verdict | Note |
|---|---|---|---|---|---|
| 6.1 | 8 LUC solar SP dockets; Honolulu 4 / Kauai 3 / Maui 1; 7 approved, 1 pending, 0 denied; every vote unanimous | note/paper Table 2 | 8 SP rows (CSV also carries 8 county-tier rows, as documented); 4/3/1; 7 approved + 1 pending; votes 8-0/7-0/6-0 throughout | MATCH | |
| 6.2 | Intervenors 0 of 8 | note/paper | 0 (all SP rows "none…"); the one intervenor entry (Pono Power) is the Maui county-forum Paeahu row, as documented | MATCH | |
| 6.3 | Durations table (county 124/159/27/40/197/182/64/218; LUC 38/32/35/27/41/34/9) | note | recomputed from the CSV date columns; every value identical | MATCH | duration columns = date arithmetic exactly |
| 6.4 | Medians: county 141.5 d; LUC 34 d; total ~181 d (≈6 months) | note/paper/README | 141.5 / 34 / 181 | MATCH | |
| 6.5 | Median host parcel among stated values ~2,950 ac | note | stated parcel_acres = {524; 861; 1,062; 2,952; 3,898; 5,341} (2 blank) → median 2,007 | MISMATCH | 2,952 is one docket's value (SP26-416), not the median; ~2,950 not reproducible as a median of the CSV column |
| 6.6 | Project census: 60 projects; by island 23/13/12/8/2/2 | note | 60; Oahu 23, Maui 13, Hawaii 12, Kauai 8, Lanai 2, Molokai 2 | MATCH | |
| 6.7 | Statewide: solar 43, wind 11, biomass 1, storage-only 3, firm biofuel 2 | note | 43 (33 solar+storage, 9 solar, 1 hybrid) / 11 / 1 / 3 / 2 | MATCH | |
| 6.8 | By-island technology sub-splits (Oahu "15 solar … 5 storage/firm"; Maui "7 solar … 1 storage") | note table | Oahu: 17 solar, 3 wind, 1 storage, 2 biofuel-firm; Maui: 9 solar, 3 wind, 1 storage; per-island solar column must sum to 43 and the note's cells sum to 39 | MISMATCH | note's island×technology cells for Oahu and Maui undercount solar; CSV and the statewide totals are internally consistent |
| 6.9 | Solar deaths/re-procurements by primary cause (supply-chain 5, credit 3, interconnection 2, utility-termination 2, rigidity 1, cultural 1, community 1, other 2) | note | identical on the cancelled/re-procured solar subset (17 rows) | MATCH | |
| 6.10 | Community resistance killed 0 Oahu solar; 1 Maui solar; 2 wind; 1 biomass | note/README | primary-cause community rows = Paeahu (Maui solar), Big Wind Lanai + Molokai (wind), Hu Honua (biomass), WKEP (delayed/scaled, hybrid); all 17 Oahu solar rows have community_effect "none" | MATCH | |
| 6.11 | "~14 solar deaths/re-procurements" from procurement+interconnection+finance | ~14 | 13 (supply-chain 5 + credit 3 + interconnection 2 + utility-termination 2 + rigidity 1); 15 counting the two revived 2016 terminations | MATCH | within the stated "~" |
| 6.12 | Resistance catalogue: 16 rows; islands Oahu 5 / Maui 3 / Hawaii 2 / Kauai 2 / Lanai 1 / Molokai 1 / statewide 2 | note | identical | MATCH | |
| 6.13 | Procurement timeline 37 rows | note | 37 | MATCH | |
| 6.14 | Pipeline CSV parses as tidy data | implied by `data/README.md` conventions | **7 of 24 rows have 15 fields (header 14)**: unquoted comma in `cause` (line 12) and a stray extra delimiter in 6 "operating" rows; pandas default parse fails | MISMATCH | `data/oahu_solar_project_pipeline.csv` needs re-quoting; python csv module still reads it, columns misalign on those 7 rows |
| 6.15 | Median award-to-COD ~5–5.5 yr (built Oahu cohort) | note/README/INVESTIGATIONS | Stage-1-only Oahu built cohort: ~5.4 yr (4.0, ~4.75, 5.8, 7.0); adding the built Stage-2 awards (Kupono, Kapolei ES, ~4.1 yr each) pulls the median to ~4.4–4.6 yr | CAUTION | date fields are coarse ("2018-mid", "2023"); "5–5.5" holds for the Stage-1 cohort only — state the cohort or widen to "~4.5–5.5" |
| 6.16 | Stage-2 Oahu attrition ~5 of 8 (~63%) | note | 5 cancelled of 8 Oahu Stage-2 solar rows (Mahi re-procured counted) | MATCH | reconstruction, as the note flags |

## 7. Wind

Sources: `data/gis/wind_viable_areas.csv`, `data/gis/wind_setback_oahu.csv`,
`data/gis/osm_wind_turbines_oahu.csv`.

| # | Claim | Published | Recomputed | Verdict | Note |
|---|---|---|---|---|---|
| 7.1 | Ord 25-2 viable: 39,386 ac = 36.3% of 108,417 AG/Country | note/paper | 39,386 / 108,417 = 36.33% | MATCH | |
| 7.2 | Pre-2025 approx: 91,856 ac = 84.7% ("85%" in paper); AG-1/2 shares 37.5% / 87.3% | note/paper | 84.73% / 37.45% / 87.35% | MATCH | |
| 7.3 | 26,023 ac (66%) of viable ≤30% slope; 13,363 steeper | note/paper | 26,023 (66.1%); 39,386 − 26,023 = 13,363 | MATCH | |
| 7.4 | Region blocks (~21,200 Waialua, ~7,800 Kunia, ~4,100 Kahuku, ~4,000 Kawailoa) | note/paper | 21,239 / 7,834 / 4,136 / 4,012; blocks sum 39,298 of 39,386 | MATCH | remainder is small scattered area |
| 7.5 | 50 turbines: 22 conforming / 28 not; all 8 NPM + 10 of 12 Kahuku nonconforming ("18 of 20"); Kawailoa 20 of 30 in, 10 out (7 setback + 3 Preservation) | paper | identical from the turbine CSV | MATCH | |
| 7.6 | Fleet ≈123 MW (Kahuku 30, Na Pua Makani 24, Kawailoa 69) | note/paper | Kawailoa 30×2,300 kW = 69 MW recomputes from OSM `output` tags; Kahuku and NPM carry no output tags in the CSV | MATCH (69) / NOT-RECOMPUTABLE (30, 24) | 30 and 24 are sourced to HECO Power Facts, external |

## 8. Non-ag, golf, military

Sources: `data/oahu_nonag_solar_candidates.csv`, `data/gis/nonag_top_parcels.csv`,
`data/oahu_golf_courses.csv`, `data/oahu_military_land.csv`.

| # | Claim | Published | Recomputed | Verdict | Note |
|---|---|---|---|---|---|
| 8.1 | Headline tier: 290 parcels, 11,319 ac ≤15%, 13,557 ≤30% | note/paper | 290 / 11,319 / 13,557 | MATCH | |
| 8.2 | Class tallies: durable 143/5,124/6,108; uncertain 58/2,446/2,645; higher-value 89/3,749/4,804 | note | 143/5,124/6,108; 58/2,445/2,645; 89/3,749/4,804 | MATCH | 1-ac rounding |
| 8.3 | Special sites: 12 durable (542 ac ≤15%), 4 higher-value (111 ac) | note | identical | MATCH | |
| 8.4 | Combined durable ≈5,660 ac (~810–1,130 MW) | note/paper/README ("~5,700") | 5,666 before the ~8-ac overlap netting ≈ 5,658 | MATCH | |
| 8.5 | Upper tiers: "599 non-military pass (of 700); low-improvement 316 / 15,464 / 17,822" | note | 601 pass (≥10 ac ≤15%); low-improvement 318 / 15,484 / 17,843 | MISMATCH (minor) | CSV differs by +2 parcels / +20 ac at both tiers — CSV apparently regenerated after the note; headline tier (290) unaffected |
| 8.6 | Special-site inventory: 16 sites, 1,344 ac, 653 ≤15% | note | 17 rows (16 mapped + PVT placeholder with no acreage), 1,349 ac, 653 ≤15% | MATCH | acreage diff is the two Kapaa satellite pits' rounding; PVT row is the documented UNVERIFIED placeholder |
| 8.7 | `nonag_top_parcels.csv` 20 rows, led by KS Waiawa 598 ac | note | 20 rows; KS Waiawa row 597.9 | MATCH | |
| 8.8 | Golf: 36 courses, 34 open, 2 closed, viable subset 0 | note/README | 36 / 34 / 2 / 0 (flags: closed_low_solar, closed_contested; no viable flag) | MATCH | |
| 8.9 | Golf by district: Urban 26/4,074/3,753; Ag 7/1,247/1,085; Conservation 3/517/392; total 5,838/5,230 | note | identical | MATCH | |
| 8.10 | Military: 65,012 ac total; lease 7 polys / 6,288 ac / 586 ≤15% / 1,438 ≤30%; fee 58,724 / 32,619 / 40,651 | note | row sums 66,105 / 59,817 / 33,432 / 41,568; lease rows exactly 6,288 / 586 / 1,438; fee row-sums exceed published dissolved totals by the documented ~1,093-ac polygon overlap (66,105 − 1,093 = 65,012) | MATCH | dissolved totals need the geometry (deposit), but the arithmetic is consistent with the note's own overlap caveat |
| 8.11 | Constraint tiers (precedent_built 3,273; plausibly_usable 9/4,661; excluded 5,581/4,724/7,616/7,577) | note | identical | MATCH | |
| 8.12 | Returning 2029 land ≈200 flat near-grid ac (Poamoho 197 at 2.3 km); Kahuku retained parcel 230 flat ac at 0.07 km | note | 196.8 / 2.32 km; 230.2 / 0.07 km | MATCH | |

## 9. Expansion curve and interfaces

Sources: `data/gis/expansion_curve.csv`, `data/gis/screenline_analysis.csv`,
`data/gis/screenline_requirements.csv`.

| # | Claim | Published | Recomputed | Verdict | Note |
|---|---|---|---|---|---|
| 9.1 | Baseline: 16,328 ac ≤30% (14,171 ≤15%) = 40% of 40,870 eligible | note/paper | 16,328 / 14,171 / 40.0% | MATCH | |
| 9.2 | L-table (10/25/50/75/100 km → 20,185 / 24,195 / 29,481 / 33,278 / 36,103 ≤30%; 17,833 / 21,374 / 26,150 / 29,190 / 31,507 ≤15%) | note | linear interpolation between committed steps reproduces every value to ±3 ac (e.g. L=25 → 24,195 exactly) | MATCH | published values are interpolated at exact L, not nearest-step |
| 9.3 | Knee ≈5.7 km, 18,580 ac, smoothed max 434 ac/km; best segments 476–483 at km 4.7–5.2; Waiawa jump ~406 at km ≈37; first ~6 km +2,252 ac | note | 5.74 km / 18,580 / 434.2; 483.4 at 5.17 and 476.5 at 4.67; 406.4 at 37.0; +2,252 | MATCH | |
| 9.4 | Screenline capability arithmetic (SL-A 300/1,600/2,000; SL-B 330/445/560; SL-C 60/90/120) | note/paper Table 7 | crossings × ratings reproduce all nine values (low = net×150 + 46 kV×30; central = geo×200 + ×45; high = geo×250 + ×60) | MATCH | |
| 9.5 | Requirement model: evening = min(σL − G_s, ρSf); midday = min(max(fS − fρS − north, 0), σ·0.85L); requirement = max | note | all 648 rows reproduce exactly (north load at midday = share × 0.85L) | MATCH | |
| 9.6 | Spot values: 930 MW = 0.775 × 1,200; saturation ~1,550 = 0.775 × 2,000; note's requirement and gap tables | note/paper | all checked cells identical (e.g. SL-B S=2 ρ=1 gap +555/+805; SL-C +410/+470) | MATCH | |
| 9.7 | N-1 adder: note says "+largest single circuit (250 MVA at A/B; 250 used for post-upgrade C)" | note | CSV `required_n1_mw` = required + 250 at SL-A/B but **+60 at SL-C** (largest existing 46 kV circuit); the note's gap table matches the CSV (+60), its program sketch uses +250 for post-upgrade SL-C | CAUTION | both conventions appear in the note; the CSV models existing corridors — one clarifying sentence would remove the ambiguity |

## 10. Finance / PPA

Sources: `data/campaign_contributions_siting.csv`, `data/campaign_contrib_summary.csv`,
`data/ppa_terms_comparison.csv`.

| # | Claim | Published | Recomputed | Verdict | Note |
|---|---|---|---|---|---|
| 10.1 | 730 classified rows; $778,572; 675 high / 55 medium | note | 730 / $778,572.48 / 675 / 55 | MATCH | |
| 10.2 | Headline per-candidate table (16 rows × 5 classified columns) | note | every cell reproduces (e.g. Ige HEI 9,350 / landholder 30,900 / solar 13,100 / unions 70,400; Dela Cruz 225/22,300/8,075/750/40,950) | MATCH | total-raised column comes from the full CSC dump, not the classified rows |
| 10.3 | HEI to the three 2011 Senate chairs, 2010-11-01→2011-12-31: $0; all 12 SB631-era legislators: $250 (HEI CEG $150 + Alm $100, both to Ige) | note | $0 / $250, same two rows | MATCH | |
| 10.4 | Seed money, 2011 window: $7,500 across **8** of the 12 legislators | note | $7,500 across **7** legislators (Chang, Dela Cruz, Kahele, Kidani, Nishihara, Solomon, Tsuji) | MISMATCH | count off by one; dollar total exact |
| 10.5 | Construction unions "$316k of the $779k classified" | note | union_construction rows total **$526,572** across all 16 targets (68% of classified); $323,822 for the 12 SB631-era targets alone | MISMATCH | $316k reproduces under no tested subset; the per-candidate union figures in the same note (95.5k/70.4k/60.3k/55.3k/41k) alone sum past $316k |
| 10.6 | Summary CSV vs row data | — | all 8 classified-amount columns × 59 candidate-period rows agree exactly with row sums | MATCH | |
| 10.7 | Explicit nulls (no HEI to Chang/Slom/Tsuneyoshi/Tupola; no ASB anywhere; no seed to Gabbard/Kiaaina/Tsuneyoshi/Tupola/Waters; Slom only $700 DuPont) | note | all reproduce | MATCH | |
| 10.8 | PPA terms: "five risk-shifting terms" | INVESTIGATIONS/README | a curated list of 5 named terms, not a CSV tally; CSV has 14+ rows flagged more_onerous=Y, including the 5 named | MATCH | narrative selection, consistent with the data |
| 10.9 | PPA CSV parses as tidy data | implied | **2 of 25 rows malformed** (lines 14 and 26: unquoted commas → 13 and 11 fields vs 10); pandas default parse fails | MISMATCH | `data/ppa_terms_comparison.csv` needs re-quoting |

## 11. Cross-document consistency

| # | Claim location | Check | Verdict |
|---|---|---|---|
| 11.1 | `README.md` headline figures (~3,600 / ~15,700 / 4.3×; 75% within 3 km; ~20,400 D/E; 6,100–11,100; ~50% government; ~13% KS / quarter of private; ~11,900 / ~5,700; 8 dockets / ~6 months; 0-Oahu resistance count; ~5–5.5 yr) | all trace to the recomputed values above; only the ~5–5.5 yr median carries the 6.15 cohort caution | MATCH (one CAUTION) |
| 11.2 | `docs/INVESTIGATIONS.md` findings column | same numbers as README/notes; no independent discrepancies found | MATCH |
| 11.3 | Paper vs CSVs (Tables 1–3, 7, 8; abstract 42,800; §6 combined estimates; wind §9; non-ag §8) | every extracted paper number reproduces from committed CSVs (details in sections above) | MATCH |
| 11.4 | `docs/ACCURACY_REVIEW.md` §G anchor values (15,106 / 34,877 / 65,076 / 120,789; S0 3,601 / S3 15,657; 42,800; fleet ≈123 MW) | consistent with recomputation | MATCH |
| 11.5 | Note-internal: `notes/oahu-transmission-screen.md` corridor owner shares vs regenerated CSV | see 3.9 | MISMATCH (3.9) |

## Summary

**131 claims checked: 118 MATCH, 8 MISMATCH, 5 NOT-RECOMPUTABLE, 2 CAUTION.**

Mismatches (all in notes or CSV hygiene; no README/paper headline number failed):

1. `notes/oahu-slope-screen.md` S3-by-slope "all" row: ≤30% cumulative printed
   14,838; the bands sum to 15,238. Typo; the "(97%)" share is correct (4.7).
2. `notes/oahu-ownership.md`: "76% of all cap-bound land" — recomputed 82.1%
   of cap-bound B/C (81.3% of cap-bound acreage) for the 15 listed entities;
   76% reproduces under no tested basis (5.13).
3. `notes/campaign-finance.md`: unions "$316k of the $779k classified" —
   recomputed $526,572 (all 16 targets) or $323,822 (SB631-era 12 only) (10.5).
4. `notes/campaign-finance.md`: seed money 2011 window "8 of the 12
   legislators" — recomputed 7; the $7,500 total is exact (10.4).
5. `notes/hawaii-project-census.md` island×technology table: Oahu row says 15
   solar + 5 storage/firm, Maui row 7 solar; CSV has Oahu 17 solar + 3
   storage/firm, Maui 9 solar. The note's per-island solar cells sum to 39
   against its own correct statewide 43 (6.8).
6. `notes/sup-census.md`: "median host parcel ~2,950 ac" — the median of the
   six stated parcel sizes is 2,007 ac; 2,952 is a single docket's value (6.5).
7. `notes/oahu-nonag-solar.md` upper screening tiers: 599 passing / 316
   low-improvement (15,464 ac) vs CSV 601 / 318 (15,484 ac); +2 parcels /
   +20 ac at both tiers, headline 290-parcel tier unaffected (8.5).
8. `notes/oahu-transmission-screen.md` corridor top-owner percentages for
   C01–C03 differ from the regenerated `oahu_corridor_candidates.csv`
   (e.g. C01 "US 26%, Island Palm 12%, Corteva 10%" vs CSV "US 33%, Island
   Palm 15%, Dillingham 6%"); acreages match, owner shares were not
   refreshed after the class-A exclusion (3.9).

CSV hygiene (counted in the mismatches above as 6.14 and 10.9):
`data/oahu_solar_project_pipeline.csv` (7 of 24 rows) and
`data/ppa_terms_comparison.csv` (2 of 25 rows) contain unquoted commas and
fail a default pandas parse.

Cautions:

- Award-to-COD "~5–5.5 yr": holds for the Stage-1 Oahu built cohort (5.4 yr);
  including built Stage-2 projects gives ~4.4–4.6 yr. State the cohort (6.15).
- SL-C N-1 adder: the requirements CSV uses +60 MVA (largest existing 46 kV
  circuit); the note's program sketch uses +250 for post-upgrade SL-C. Both
  appear in `notes/oahu-bulk-delivery.md` without distinction (9.7).

Not recomputable from committed data (all consistent where cross-checkable):

1. Ag-district 120,789 ac, urban 104,231, AG/Country zoning 108,417 — derived
   from SLUD/parcel/zoning layers in the Zenodo deposit (`docs/DATA_DEPOSIT.md`),
   not in git; committed summary CSVs carry them as data (2.7).
2. Oahu land area (~382,500–386,000 ac) behind the "~32%" share — external (2.8).
3. Wind fleet 30 MW (Kahuku) and 24 MW (Na Pua Makani) — HECO Power Facts;
   OSM turbine CSV lacks output tags for those farms (Kawailoa's 69 MW
   recomputes) (7.6).
4. OP 2011 LSB comparison figures — external publication (2.9).
5. Campaign-finance total-raised denominators — derivable in principle from
   `data/raw/csc/wayback_contrib_dump_20250331.csv` + live caches, not
   re-derived here; classified columns fully verified (10.2, 10.6).

External-source numbers (prices, dates, MW ratings, statutory text) were out
of scope; `docs/AUDIT_SOURCES.md` covers source-link verification.

---

## Resolution log (2026-07-23)

All 8 mismatches, both CSV-hygiene items, and both cautions were fixed the same
day, each correction re-verified against the source CSV before editing:

1. `notes/oahu-slope-screen.md` — S3 "all" row ≤30% cumulative 14,838 → 15,238.
2. `notes/oahu-ownership.md` — "76% of cap-bound land" → 82.1% of cap-bound B/C
   (81.3% of parcel acreage).
3. `notes/campaign-finance.md` — unions $316k → $526.6k of $778.6k classified
   (68%); $323.8k to the 12 SB631-era legislators.
4. `notes/campaign-finance.md` — seed 2011 window "8 of the 12" → 7 ($7,500
   exact: Chang, Dela Cruz, Kahele, Kidani, Nishihara, Solomon, Tsuji).
5. `notes/hawaii-project-census.md` — island×technology headers: Oahu 17 solar
   / 3 wind / 1 storage / 2 firm; Maui 9 solar / 3 wind / 1 storage.
6. `notes/sup-census.md` — median host parcel ~2,950 → 2,007 ac (median of the
   six stated values; two blank).
7. `notes/oahu-nonag-solar.md` — upper tiers 599→601 parcels; 316→318 /
   15,464→15,484 / 17,822→17,843.
8. `notes/oahu-transmission-screen.md` — C01/C02/C03 top-owner shares updated
   to the regenerated (class-A-excluded) CSV values.
9. `data/oahu_solar_project_pipeline.csv` — 7 malformed rows re-quoted; pandas
   parses (24×14).
10. `data/ppa_terms_comparison.csv` — 2 malformed rows re-quoted; pandas parses
    (25×10).
11. Award-to-COD median qualified by cohort in README, INVESTIGATIONS,
    heco-solar-procurement, process-cost-channel: ~4.5–5.5 yr (Stage-1 built
    cohort ~5.4; built Stage-2 ~4.1).
12. `notes/oahu-bulk-delivery.md` — SL-C N-1 basis note added (+60 MW mapped-
    feeder adder in the scenario grid vs post-upgrade 138 kV loss in the
    program sketch).
