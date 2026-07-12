# Data Dictionary

Every CSV in `data/` and `data/gis/`, plus the structure of `data/raw/` and
`testimony/`. Row counts exclude the header. "Producer" is the script in
`analysis/` that writes the file; "hand-curated" means it was compiled from
primary documents in a research session (per-row `source` columns cite them).
Acres are computed in EPSG:26904 (NAD83 / UTM 4N); 1 ac = 4046.8564224 m².
TMK keys are 9-digit statewide (leading digit = county: 1 Oahu, 2 Maui,
3 Hawaii, 4 Kauai).

Scenario codes used throughout (see `analysis/cap_scenarios.py`):

| Code | Rule (per parcel, B/C-soil area only) |
|---|---|
| S0_current_10pct_20ac | min(10% of parcel, 20 ac, B/C area) — current HRS § 205-4.5(a)(20) |
| S1_10pct_nocap | min(10% of parcel, B/C area) — drop hard 20-ac cap |
| S2_20pct_20ac | min(20% of parcel, 20 ac, B/C area) |
| S3_20pct_nocap | min(20% of parcel, B/C area) — headline counterfactual |
| S4_all_BC | all B/C area — no cap |

---

## data/ — legislative & documentary tables (hand-curated)

### bills.csv — 12 rows
Inventory of the key measures amending §§ 205-2 / 205-4.5 solar siting,
2011–2025. One row per bill. Hand-curated from capitol.hawaii.gov (via
Wayback), committee reports, and session laws; vintage July 2026.

| column | description |
|---|---|
| bill | Measure number (e.g. SB631) |
| year | Session year |
| act | Act number if enacted (e.g. "Act 217"), else status note |
| title | Official measure title |
| sponsors | Introducers (semicolon-separated) |
| siting_change | What the enacted/final version did to solar siting rules |
| introduced_vs_final_delta | Draft-by-draft narrative of what each committee inserted/removed — the core "who changed what" field |
| committees | Referral path |
| status | Final disposition and date |
| sources | Pointers to notes/, data/raw/capitol/, testimony/, and archive URLs |

Caveats: narrative fields are long prose with embedded semicolons; parse as
quoted CSV. Committee-insertion attributions are cross-checked against
committee reports cited in `notes/sb631-2011.md` and `notes/acts-2014-2022.md`.

### pre2011_bills.csv — 13 rows
Failed (and context) solar-liberalization measures ~2005–2010, with who
opposed on the record. Hand-curated via Wayback captures of
capitol.hawaii.gov; vintage July 2026. Full narrative in
`notes/pre2011-solar-bills.md`.

| column | description |
|---|---|
| bill, year, title, sponsors | Measure identity (sponsors sometimes `UNVERIFIED (not pulled)`) |
| siting_change_proposed | Proposed change to ag-district solar rules, incl. committee-draft caps |
| final_status | Enacted/died, with act number where applicable |
| died_in_committee | Committee where the measure died (blank if enacted) |
| opponents_on_record | Testifiers opposing or seeking caps (or `UNVERIFIED (testimony not pulled)`) |
| source_url | Wayback URL of status page or session law |

Caveat: rows explicitly mark unpulled testimony as UNVERIFIED — do not treat
blanks as "no opposition."

### sup_census.csv — 16 rows
Census of LUC Special Use Permit dockets for utility-scale solar on ag land
(SP15-405 through SP26-417 era). One row per docket. Hand-curated from LUC
decision-and-order PDFs, county planning-commission records, and meeting
minutes (all in `data/raw/dockets/`); method in `notes/sup-census.md`.
Vintage July 2026.

| column | description |
|---|---|
| docket | LUC docket (e.g. SP15-405) |
| county | Permitting county |
| project | Project name, size, developer lineage |
| applicant | Applicant entity (with corporate successors) |
| landowner | Fee owner at application |
| counsel | Law firm and named attorneys (from signature blocks) |
| tmk | TMK(s), "(por.)" = portion |
| parcel_acres / sup_acres | Parcel size / permitted SUP area (acres) |
| mw | Nameplate MW |
| soil_class | LSB class(es) of the site; IAL status noted |
| county_filed / county_decision | County application and decision dates |
| luc_transmittal / luc_decision | LUC receipt and decision dates |
| luc_vote | Vote tally |
| outcome | e.g. "approved with conditions" |
| duration_county_days / duration_luc_days | Processing lags |
| intervenors | Intervenors admitted (usually "none") |
| ag_couse_condition | Compatible-agriculture condition (≥50%-below-FMR rent language etc.) |
| decommissioning_condition | Security amount and restoration terms |
| permit_duration | Permit term and establishment deadlines |
| source_urls | Direct PDF links (semicolon-separated) |
| notes | Verification flags, testimony counts, disclosures |

Caveats: some `parcel_acres` cells marked UNVERIFIED; fields contain long
quoted prose with embedded commas/newlines — use a real CSV parser.

### hei_board_interlocks.csv — 37 rows
Person-level interlocks between HEI/HECO/ASB boards and Hawaii trusts,
estates, and landholders. One row per person × affiliation. Hand-curated from
SEC EDGAR DEF 14A proxies (`data/raw/edgar/`), KS/trust publications, and
press; full narrative in `notes/hei-interlocks.md`. Vintage July 2026.

| column | description |
|---|---|
| person | Individual name |
| role_at_hei | Position(s) and years at HEI/HECO/ASB |
| years_at_hei | Overall HEI-family span |
| other_affiliation | The interlocking position (trust, estate, landholder board) |
| affiliation_type | trust / landholder / ag / other |
| affiliation_years | Span of the other affiliation |
| source_url | Primary sources (proxy URL + corroboration) |
| verified | Y/N — N rows are Tier-3 until confirmed |
| notes | Timing overlaps (e.g. simultaneous roles during the SB 631 session) |

### legal_edges.csv — 37 rows
Attorney/party edges for contested renewable-energy proceedings (PUC dockets,
LUC SUPs, appellate cases). One row per party × attorney. Built from counsel
signature blocks in filings and opinions (`data/raw/dockets/`); narrative in
`notes/legal-representation-map.md`. Vintage July 2026.

| column | description |
|---|---|
| forum | PUC / LUC / courts |
| docket_or_case | Docket or case number(s) |
| year | Span of the proceeding |
| project | Project at issue |
| party / party_side | Represented party and stance (e.g. intervenor_opposed) |
| attorney / firm | Counsel of record |
| also_represents | Other clients of the same counsel (the network edge) |
| also_represents_source | Where those other representations are documented |
| lobbyist_principal_matches | Ethics-registry matches for the attorney (or "none found") |
| source_url | Signature-block source |
| notes | Role details |

Caveat: "also_represents" is compiled from public counsel blocks only; the
absence of a utility/landholder client is a *no-evidence-found* finding, not
proof of absence.

### wind_setback_bills.csv — 12 rows
Inventory of county wind-setback measures (Honolulu Res 19-305, Bill 28
(2021), Bill 10 (2022), Bill 64 (2023), Ord 25-2, plus neighbor-island
items). Hand-curated from county docushare/hnldoc records
(`data/raw/wind-setbacks/`); narrative in `notes/wind-setbacks.md`.
Columns: jurisdiction, bill_or_ord, year, sponsors, setback_formula, status,
source_url, notes.

### campaign_contributions_siting.csv — 730 rows
Producer: `analysis/campaign_finance_extract.py`. Classified contributions
to legislators/council members who controlled solar/wind siting measures.
Source A: CSC CKAN datastore dump captured by the Internet Archive
2025-03-31 (218,392 rows, Nov 2006–late 2024) — the live portals were
truncated to 2015+ in 2025. Source B: live SODA API top-up
(hicscdata.hawaii.gov jexd-xbcg), cached in `data/raw/csc/live_*.json`.

| column | description |
|---|---|
| candidate / office / election_period | Recipient and cycle |
| donor / donor_type | Donor name and CSC donor-type field |
| employer / occupation | CSC fields (often blank for entities) |
| amount / date | Contribution amount and date |
| donor_class | Project classification: hei_utility, hei_person, hei_asb, utility_other, landholder_dev, ag_seed, solar_wind, union_construction |
| confidence | Classification confidence (high/med/low) |
| group | Which bill cohort the recipient belongs to (e.g. sb631) |
| source | Provenance string (Wayback capture id or live API) |

Caveat: only rows matching classified donors are retained — this is not the
candidate's full donor file (see summary file for totals).

### campaign_contrib_summary.csv — 59 rows
Producer: `analysis/campaign_finance_extract.py`. Per candidate × election
period: `n_contributions` and `total_raised` over the FULL donor file, plus
`amt_*` totals per donor class (columns mirror `donor_class` above).
Denominators are complete; classified columns are lower bounds.

---

## data/ — GIS pipeline outputs (parcel-level)

### cap_scenarios_by_parcel.csv — 115,856 rows
Producer: `analysis/cap_scenarios.py` (statewide). One row per ag-district
parcel intersecting LSB polygons, all four counties. Inputs: geodata.hawaii.gov
LSB overall-productivity polygons, State Land Use Districts, county TMK
parcels (downloaded July 2026, cached in `data/gis/pages_*`).

| column | description |
|---|---|
| tmk | 9-digit TMK |
| island | Oahu / Hawaii / Maui / Kauai |
| county_layer | Source parcel layer (parcels_oahu etc.) |
| owner | Raw owner string where the county layer provides one (blank on Oahu — see oahu_ag_owners.csv) |
| parcel_acres | Parcel area in ag district |
| a_acres … e_acres | LSB class A–E acres within the parcel (ag district only) |
| S0_… S4_all_BC | Eligible acres under each scenario (see table above) |

### cap_scenarios_results.csv — 35 rows
Producer: `cap_scenarios.py`. Island × scenario totals: `eligible_acres`,
plus MW conversions at 5 and 7 ac/MW (`mw_at_5ac`, `mw_at_7ac`).

### oahu_land_transmission.csv — 6,274 rows
Producer: `analysis/transmission_screen.py`. Oahu ag parcels with soil-class
acres, S0/S3 eligible acres, and boundary distance (km) to the mapped 46 kV+
network (`dist_46kv_km`) and 138 kV network (`dist_138kv_km`). Line sources:
HIFLD Open (2017–2020 vintage) + OSM Overpass (2026 pull). **Caveat: the
46 kV system is under-mapped (~80–140 km mapped vs several hundred real
circuit-km), so `dist_46kv_km` is an upper bound; 138 kV distances are
reliable.** Distance 0 = line crosses the parcel.

### oahu_ag_owners.csv — 6,239 rows
Producer: `analysis/fetch_ownall.py` (fetch) + `analysis/resolve_owners.py`
(entity resolution). Owner of record for each Oahu ag-district TMK from the
Honolulu RPAD OWNALL table (taxyr 2027) cached in `data/raw/rpad/`, plus the
state Government Lands layer for public parcels.

| column | description |
|---|---|
| tmk | 9-digit TMK |
| owner_raw | OWNALL own1 string as recorded |
| owner_resolved | Canonical entity after manual mapping + rule-based resolution |
| owner_type | state, federal, county, dhhl, trust_estate, utility, landholder_dev, corporate_other, nonprofit, individual, etc. |
| source | bulk (OWNALL) / govlands / manual |
| source_url | REST endpoint + taxyr provenance |
| confidence | high/med/low resolution confidence |
| note | e.g. CPR/condo caveat: treating a CPR master as one owner overstates concentration |

Caveat: fee owner only — leaseholds invisible; ~35 parcels lack OWNALL rows.

### oahu_owner_class_transmission.csv — 6,274 rows
Session-built merge (no standalone script) of `oahu_land_transmission.csv` ×
`oahu_ag_owners.csv`, adding `band46` (0-1km/1-3km/3-5km/>5km distance band),
`bc_acres`, `de_acres`. Consumed by `analysis/make_paper_figs.py` (Figure 3
ownership panel). Columns = union of the two parents + the three derived
fields. Regenerate by re-merging the parents on `tmk`.

### oahu_parcel_slope.csv — 6,274 rows
Producer: `analysis/slope_screen.py`. Per-parcel acres in percent-slope bands
0-5, 5-10, 10-15, 15-20, 20-25, 25-30, >30. DEM: USGS 3DEP 1/3 arc-second
(~10 m) tiles n22w158/n22w159, downloaded 2026-07-12, reprojected to a 10 m
EPSG:26904 grid; slope via central differences. Band acres are 10 m cell
counts (0.02471 ac/cell) within the parcel.

### oahu_nonag_solar_candidates.csv — 827 rows
Session-built (research session documented in `notes/oahu-nonag-solar.md`;
no standalone script). Non-agricultural-district candidate sites for solar:
urban-district vacant/low-improvement parcels, military notes, etc. Sources
per row: SLUD + parcels + RPAD ASMTGIS/OWNALL (taxyr 2026/27).

| column | description |
|---|---|
| tmk_or_site | TMK or named site |
| type | Candidate class (e.g. military_note, vacant_urban) |
| acres_total / acres_le15 / acres_le30 | Total and slope-screened (≤15%, ≤30%) acres |
| dist_46kv_km / dist_138kv_km | Grid distances (same caveats as above) |
| owner | Owner of record |
| low_improvement_flag | True if improvement value ≈ 0 relative to land value (vacancy proxy) |
| notes / source | Screening notes and provenance |

Caveat: the vacancy proxy (assessed improvement value) flags parking lots and
paper improvements imperfectly; single-parcel screening basis noted per row.

---

## data/gis/ — derived summary CSVs (tracked)

Large layers here (`*.parquet`, `*.tif`, `*.geojson`, `*.json`, `pages_*/`,
`dem/`) are gitignored caches; only these CSVs are tracked.

| file | rows | producer | contents |
|---|---|---|---|
| lsb_sanity_totals.csv | 6 | cap_scenarios.py | Island × LSB class acreage, ALL districts — sanity check vs published LSB totals |
| lsb_in_ag_district_totals.csv | 6 | cap_scenarios.py | Island × LSB class acreage restricted to the State Ag District |
| scenario_by_size_decile.csv | 10 | cap_scenarios.py | Statewide S0–S4 eligible acres by parcel-size decile (shows the cap binds only on large parcels) |
| scenario_by_owner_top.csv | 40 | cap_scenarios.py | S0–S4 by top owners per county layer (owner strings only where county layer carries them) |
| oahu_class_by_band.csv | 10 | transmission_screen.py | LSB class × distance band (0-1/1-3/3-5/>5 km) acres, by network tier (46kVplus, 138kV) |
| oahu_eligible_by_band.csv | 4 | transmission_screen.py | S0 vs S3 eligible acres × distance band × network tier |
| oahu_unlock_clusters.csv | 13 | transmission_screen.py | Far-from-grid ag clusters ranked by acres unlocked per km of new corridor; columns incl. cluster acres by class, MW at 5/7 ac, extension km, nearest corridor |
| oahu_lsb_by_slope.csv | 5 | slope_screen.py | LSB class × slope band acres, ag district (10 m cell counts) |
| oahu_de_neargrid_by_slope.csv | 3 | slope_screen.py | D/E land within 1/3 km of 46 kV+ by slope band |
| oahu_s3_by_slope.csv | 6 | slope_screen.py | S3-eligible acres by slope band × grid distance, under two quota allocations: `flattest_first` (headline) and `proportional` |
| oahu_corridor_candidates.csv | 16 | corridor_candidates.py | Candidate corridors C01…: buildable acres (≤15/≤30% slope), MW, % D/E vs B/C-S3, km of new ROW to 46 kV and 138 kV, owners unlocked per km, top owners, federal-majority flag, centroid |
| oahu_ring_1_3km_summary.csv | 4 | corridor_candidates.py | Buildable acres in the 1–3 km "cheap upgrade" ring, B/C vs D/E |
| expansion_curve.csv | 154 | transmission_expansion.py | Greedy expansion frontier: per step, segment km, cumulative km, cumulative buildable acres (≤30 and ≤15% slope), marginal ac/km, segment WKT (EPSG:26904), 5-step smoothed ac/km |
| wind_setback_oahu.csv | 2 | wind_setback_oahu.py | Viable AG-zoned acres under Honolulu Ord 25-2 (1.25 mi) vs pre-2025 (~200 m) setback rules; totals and shares for AG+C and AG-1/2 |
| wind_viable_areas.csv | 10 | wind_viable_map.py | Summary + named-region rows of Oahu land where large wind remains geometrically permitted under Ord 25-2 (AG-1/AG-2 beyond the 1.25 mi floor), split ≤30% vs >30% slope, with centroids |
| nonag_top_parcels.csv | 20 | session-built (see notes/oahu-nonag-solar.md) | Top non-ag candidate parcels/sites: owner, flat acres (≤15%), assessed land value per acre, 138 kV distance, durable-vs-pipeline viability class |

Expansion-curve caveats (from the script docstring): geometric routing only —
line capacities, substation headroom, and interconnection engineering ignored;
greedy heuristic, not an optimum; marginal gains show approach-then-jump
artifacts for far clusters.

### Gitignored layers in data/gis/ (regenerable)

- `pages_lsb/`, `pages_slud/`, `pages_parcels_{oahu,hawaii,maui,kauai}/`,
  `pages_zoning_oahu/` — raw ArcGIS REST page dumps (cap_scenarios download).
- `lsb.parquet`, `slud.parquet`, `lsb_ag.parquet`,
  `parcels_{oahu,hawaii,maui,kauai}.parquet` — assembled layers.
- `hifld_lines_oahu.geojson` (91 features), `osm_power_oahu.json` (87 ways),
  `oahu_lines_classified.parquet` — transmission lines.
- `dem/` — 3DEP tiles + `oahu_slope_bands.tif` (10 m uint8 band raster).
- `oahu_far_clusters.parquet`, `expansion_segments.parquet` — cluster/segment
  geometries backing the CSVs above.

---

## data/raw/ — primary-source caches (gitignored, ~390 MB)

| subdir | contents |
|---|---|
| capitol/ (~42 MB, 80 items) | capitol.hawaii.gov captures via Wayback: per-bill folders (`2008_HB2502/`, `hb2665_2018/`, … with introduced/draft texts, committee reports HSCR/SSCR, status pages, testimony PDFs + .txt extracts), SB631 2011 full record, acts lists by year, HRS snapshots |
| csc/ (~58 MB) | `wayback_contrib_dump_20250331.csv` — pre-truncation CSC contribution dump (218,392 rows, 2006–2024); `live_<regno>.json` SODA top-ups |
| dockets/ (~251 MB) | LUC SUP dockets (`sp15-405/` … `sp26-417/`: D&Os, staff reports, minutes), Hawaii Supreme Court opinions (SCOT-*.pdf + .txt), Kahana/WMPA settlement, `lobbyist_registrations.csv` (Ethics Commission extract), `luc-annual-reports/` |
| edgar/ (~16 MB) | HEI DEF 14A proxy statements (2006–…), .htm + .txt pairs |
| lurf/ (192 KB) | LURF membership/officer/board rosters via Wayback (2005–2024) |
| rpad/ (~2.5 MB) | `ownall_oahu_ag_rows.csv` (OWNALL rows for ag TMKs), `govlands_detailed_oahu.csv` |
| wind-setbacks/ (~18 MB) | Honolulu Ord 25-2, Bill 10/64 records, DPP status memos |

## testimony/ — curated testimony (tracked)

One directory per bill: `sb631_2011/` (12 files), `sb2775_2014/` (6),
`sb2658_2014/` (10), `hb2665_2018/` (4), `hb969_2025/` (2), `sb942_2021/`
(**empty** — hearing record not captured). Each compiled-testimony PDF from
capitol.hawaii.gov is paired with a same-basename `.txt` extraction. Filename
convention: `<BILL>_<draft>_TESTIMONY_<committees>_<MM-DD-YY>[_LATE].pdf`.
