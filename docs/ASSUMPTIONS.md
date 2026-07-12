# Register of Exogenous Assumptions and Parameters

Every exogenous parameter, threshold, conversion factor, and modeling
convention used in `analysis/` or asserted in the paper
(`paper/land-restrictions-paper.html`), compiled by an adversarial audit
2026-07-12. "Paper §" refers to the numbered sections of the background
paper. "Disclosed?" states whether the *value* appears in the paper and
where; justification/caveat disclosure is noted separately when it differs.
Statutory facts (the 10%/20-ac cap itself, the class-A ban, Ord 25-2's
1.25-mi setback) are the *object* of study, not assumptions, and appear here
only where the analysis adds an interpretive reading.

## A. Conversions and geodesy

| # | Assumption | Value | Where used | Source / justification | Sensitivity / alternative | Disclosed in paper? |
|---|---|---|---|---|---|---|
| A1 | Land-to-capacity density | 5 ac/MWac (headline) and 7 ac/MWac | `cap_scenarios.py`, `transmission_screen.py`, `corridor_candidates.py`, `nonag_classify.py`; paper §§4, 6, 8, Tables 4, 6 | Conventional utility-scale PV density range; consistent with NREL land-use benchmarks and recent Hawaii projects. No repo citation to a specific source | All MW figures scale linearly; both ends reported in the CSVs (`mw_at_5ac`, `mw_at_7ac`) | Yes — §6 "all figures at 5 acres/MW; 7 acres/MW scales them by 5/7". Underlying source not cited |
| A2 | Area conversion / CRS | 1 ac = 4046.8564224 m²; EPSG:26904 projected areas (scale distortion <0.1%) | every GIS script | NAD83 / UTM 4N; distortion argument in `cap_scenarios.py` docstring and METHODS | Negligible vs source-polygon noise | Yes — §12 (CRS named); distortion note in docs only |
| A3 | DEM and slope method | USGS 3DEP 1/3″ (~10 m), bilinear to 10 m grid, percent slope = 100·\|∇z\| central differences; 1 cell = 0.02471 ac | `slope_screen.py` and everything downstream | ≈ GDAL/Horn method; raster/vector totals reconcile <0.1% (METHODS §3) | 10 m smooths gulch walls → steep-margin acreage slightly optimistic (flagged in METHODS) | Yes — §5, §12 ("10-meter USGS elevation model") |

## B. Statutory-reading and scenario-design assumptions

| # | Assumption | Value | Where used | Source / justification | Sensitivity / alternative | Disclosed in paper? |
|---|---|---|---|---|---|---|
| B1 | Class A excluded from all solar-eligibility and buildability screens | A acres never counted; "no SUP path on A" | `cap_scenarios.py` (BC-only cap base), `corridor_candidates.py`, `transmission_expansion.py`, figures F1–F8 | Reading of § 205-4.5(a)(20) proviso + (a)(21) (SUP authorized on B/C only); corroborated by the SUP census (no A-soil SUP ever granted) | If reclassification (LUC boundary amendment) is counted as a path, A land re-enters at high transaction cost | Yes — Table 1 states the reading and the evidence |
| B2 | Cap applies to B/C area only; D/E "uncapped, no SUP" | scenario base = b_acres + c_acres | `cap_scenarios.py` S0–S4; paper Table 1, §6 | § 205-4.5(a)(20)–(21), § 205-2(d)(6) | — (statutory) | Yes — Table 1 |
| B3 | Class E excluded from the expansion optimization (B/C/D only), though E is included in "D/E" screens elsewhere | eligibility raster = {B,C,D} | `transmission_expansion.py` (`bcd` mask) | Per Mike's B–D spec for the optimization (exogenous instruction, not statute — E land is legally open to solar) | Including E would raise coverage totals; cross-figure comparability with the D/E screens (F2, F7) is imperfect — noted inconsistency | Yes — §4 "Class E is excluded here along with class A"; Fig 5 footnote. The *reason* (spec choice, not law) is not stated |
| B4 | S3 (20%, no hard cap) is the headline counterfactual | S3 of S0–S4 | `cap_scenarios.py`, F1, paper §6 | Design choice — isolates the 20-ac term, which the decile table shows does the binding | S1/S2/S4 all computed and reported | Yes — §6 reports all scenarios |
| B5 | Grazing satisfies the SUP ag co-use condition (≥50%-below-FMR compatible-ag lease) | "grazing qualifies… substitutes for vegetation management" | paper §2, §7; `data/sup_census.csv` coding | Observed SUP conditions and practice in the docket record (`notes/sup-census.md`) | If counties/LUC tightened "compatible agriculture," the SUP path's cost rises; treated as cheap throughout §2 | Yes — asserted in §2; presented as observed practice, not flagged as an interpretive assumption |
| B6 | Conservation district treated as unavailable for utility solar | 158,668 ac excluded | paper §8 | HRS ch. 183C CDUP requirement; no utility-scale solar ever permitted there | A CDUP is not literally impossible; assumption is conservative | Yes — §8 states the reasoning |
| B7 | SUP cost = "mainly time (~6 months) + case-by-case uncertainty"; process "routine" for large owners/developers | qualitative | paper §2, §3 exposed-set argument | Inference from the 8-docket census (7 approved, unanimous, 0 intervenors, median ≈6 mo) | n = 8, all developer-driven, all post-2014; selection into applying is unobserved (owners deterred by the SUP never appear) — the census cannot reject deterrence | Partially — census facts disclosed (Table 2); the selection caveat is not stated in the paper |

## C. Grid-proximity and transmission-cost parameters

| # | Assumption | Value | Where used | Source / justification | Sensitivity / alternative | Disclosed in paper? |
|---|---|---|---|---|---|---|
| C1 | Interconnection service radius | 1 km from a mapped line = "served" | `transmission_expansion.py` (RADIUS_CELLS=10), `slope_screen.py` (le_1km), `corridor_candidates.py` (>1 km = unserved), paper §§4–6 | Simplification of interconnection cost; explicitly "not a tariff rule" (script docstring, METHODS §4) | Doubling the radius roughly quadruples served area near lines; no sensitivity run exists | Value yes (§4, §6, figure captions); its status as a cost simplification only in METHODS/docstrings |
| C2 | Distance band edges | 0–1 / 1–3 / 3–5 / >5 km | `transmission_screen.py` BANDS; F2; DATA_DICTIONARY | Ad hoc banding | Different edges shift the headline "within 1 km / within 3 km" numbers | Values yes (Fig 2); no justification given anywhere |
| C3 | "Cheap upgrade ring" | 1–3 km from a mapped line | `corridor_candidates.py`, paper Table 4 row 1, Table 6 tranche 1 | Ad hoc: close enough for short spurs/reconductoring | Ring contents are the paper's largest single resource claim (≈24,000 ac) | Yes (Table 4); no justification |
| C4 | Far-cluster reporting thresholds | >3 km = "far" and ≥100 ac (transmission_screen); >1 km and ≥250 buildable ac (corridor_candidates) | `transmission_screen.py`, `corridor_candidates.py` | Ad hoc reporting floors | Smaller clusters silently dropped from tables/maps | 250-ac floor in METHODS §4; **>100 ac floor disclosed nowhere** (code only) |
| C5 | New-build line cost | $2.5M/km central; $1.5–4M/km range (138 kV) | `make_expansion_fig_cost.py` (COST_PER_KM_M=2.5), paper §4, Table 5, Fig 5 | MISO transmission cost estimation guides (2024$) × Hawaii multiplier; wire only | Order-of-magnitude driver of the $-axis; HECO actuals confidential | Yes — Table 5 and Fig 5 caption, wire-only caveat stated |
| C6 | Hawaii construction multiplier | 1.5–2.5× mainland | paper Table 5 | **UNVERIFIED** — flagged "U" in the paper; no primary source in repo | Entire Table 5 scales with it | Yes — disclosed with U flag |
| C7 | Transfer-capacity ranges | 46–69 kV ≈ 20–60 MW; 138 kV ≈ 150–250 MW | paper Table 5, Table 6 rationale ("138 kV moves 3–5× the power") | Planning rules of thumb; no repo citation; HECO actuals confidential | Drives $/MW-km and the "build spurs at 138 kV" recommendation | Yes — Table 5; source not cited |
| C8 | Substation / collector-bay cost | ≈ $10–30M per station, fixed | paper Table 5, Table 6 tranche 2 | Planning benchmark; no repo citation | For short spurs, dominates wire cost (stated) | Yes — Table 5 |
| C9 | Hawaii all-in solar capex | ≈ $2–2.5M/MWac | paper §4 ("a 3-km spur adds… 1.5–3.5%") | No repo citation; consistent with recent HI PPA-era reporting | Anchors the "wire is second-order" argument | Yes — §4; source not cited, not U-flagged |
| C10 | Line-data vintage/completeness | HIFLD 2017–2020 + OSM 2026 pull; 46 kV network under-mapped (~80–140 km of several hundred); 138 kV reliable (~325 km) | `transmission_screen.py` and all distance outputs | Cross-validation of the two sources (METHODS §2) | All 46 kV distances are upper bounds; far-cluster/"unlock" results partly artifacts (C01, Ewa, Waiau, Helemano flagged) | Under-mapping yes (§4 and figure notes, repeatedly); vintages only in docs |
| C11 | Voltage classification rule | 138 kV iff HIFLD VOLTAGE==138 or VOLT_CLASS=='100-161' (or OSM voltage=138000); everything else = "46 kV+" | `transmission_screen.py` `load_lines()` | Median 0 m agreement between sources at 138 kV | Untagged OSM ways may include distribution, inflating the 46 kV+ network | Implicitly (§4 "cross-validated"); rule itself in METHODS/docstring |

## D. Expansion-optimization internals

| # | Assumption | Value | Where used | Source / justification | Sensitivity / alternative | Disclosed in paper? |
|---|---|---|---|---|---|---|
| D1 | Greedy heuristic (not an optimum) | iterative best-path commits | `transmission_expansion.py` | Tractability; curve is an approximation from below of the true optimum coverage (and an upper bound on real-world routing, per paper) | An exact or MIP formulation not attempted | Yes — §4 and Fig 5/6 captions say "greedy heuristic" |
| D2 | Steep-cell routing penalty | 6× geometric length entering a 100 m cell with >30% of its 10 m subcells at >30% slope (SLOPE_PENALTY=6.0, STEEP_FRAC=0.30) | `transmission_expansion.py` | Ad hoc — "lines can cross steep ground but the router avoids it when it can" | Routes shift with the penalty; no sensitivity run | **No** — METHODS §4 discloses it; absent from the paper |
| D3 | Commit increment | ≤1.0 km per step (STEP_KM) | `transmission_expansion.py` | Produces the approach-then-jump artifacts (flagged) | Cosmetic to the curve shape | METHODS yes; paper indirectly (jump annotation) |
| D4 | Candidate shortlist | top ~15 approximate scorers, ≥1 km apart, re-scored exactly (TOP_K=15) | `transmission_expansion.py` | Compute budget | Larger K could find better paths | METHODS yes; paper no |
| D5 | Score denominator floor | approximate score = gain / max(dist, 500 m) | `transmission_expansion.py` `run_greedy` | Prevents division blow-up next to the network | Biases candidate shortlist near existing lines | **Nowhere disclosed** — code only |
| D6 | Budget horizon | 112 km build-out | `transmission_expansion.py` (BUDGET_KM) | Enough to reach ~88% of eligible land | — | Yes — Fig 6 caption ("to 112 km") |
| D7 | Coverage lattice | 100 m cells, cell-center-within-1-km test (<~1% vs 10 m polygon buffers) | `transmission_expansion.py` | Compute; discrepancy quantified in docstring | — | Docs only; immaterial |

## E. Slope screen and buildability conventions

| # | Assumption | Value | Where used | Source / justification | Sensitivity / alternative | Disclosed in paper? |
|---|---|---|---|---|---|---|
| E1 | Slope bands | 0–5, 5–10, 10–15, 15–20, 20–25, 25–30, >30 % | `slope_screen.py` BANDS; F7, Table 7 | Five-point bands bracketing the 15% tracker limit and 30% infeasibility line | — | Yes — §5, Table 7 |
| E2 | Buildability convention | ≤15% = mainstream tracker envelope; 15–30% = specialized premium margin; >30% = infeasible | all "buildable" quantities (`corridor_candidates.py`, `transmission_expansion.py`, `wind_viable_map.py` slope split, §§5–6, 8) | `notes/slope-cost-literature.md`: NREL flat-site benchmarks, tracker spec limits (~15% N–S), one vendor's 37% claim, no completed project >25% found; Honolulu grading code engineer's-report line at 15% | No published continuous cost-vs-slope curve exists (stated); the 30% line is a judgment | Yes — §5 and Table 7 lay out the evidence and the convention explicitly |
| E3 | S3-by-slope allocation | `flattest_first` headline (fill quota from flattest B/C cells); `proportional` alternative also computed | `slope_screen.py`; feeds §5's "89% ≤15%" claim | Developer-siting logic | Proportional bound reported in `oahu_s3_by_slope.csv` | Partially — the number is used in §5 without naming the allocation rule; METHODS §3 discloses both |
| E4 | Parcel band assignment | whole parcel assigned to band of its minimum boundary distance | `transmission_screen.py` eligible-by-band | Simplicity | Near-grid bias for large parcels (flagged) | METHODS yes; paper no (Fig 2 uses polygon-accurate tabs, so exposure is limited) |

## F. Ownership build

| # | Assumption | Value | Where used | Source / justification | Sensitivity / alternative | Disclosed in paper? |
|---|---|---|---|---|---|---|
| F1 | Ownership source and vintage | Honolulu RPAD OWNALL, taxyr 2027; fee parcel (suffix 0000), ownseq 0, own1 = "the owner" | `fetch_ownall.py`, `resolve_owners.py`, F3, §3 | Only bulk machine-readable source; cross-checked vs Government Lands layer | Assessment owner ≠ beneficial owner; leaseholds invisible (KS land leased to Dole etc. shows as KS) | Coverage (99%) yes §3/§12; vintage and fee-owner-only caveat only in docs |
| F2 | CPR/condo masters treated as single owners | one row per master | `resolve_owners.py`, F3 | RPAD structure | Overstates concentration (flagged per-row in the CSV and DD) | No — docs only |
| F3 | Owner scale classes | breaks at 100 / 1,000 / 5,000 ac total holdings; "exposed set" = mid-size 100–1,000 ac owners of >200-ac B/C parcels | paper §3, Table 3; F3 aggregates | Ad hoc classing; 200-ac threshold is arithmetic (20 ac = 10% × 200 ac), not assumed | Different breaks change the "exposed set" size (26 owners) | Yes — Table 3 defines the classes; 200-ac derivation stated §2 |

## G. Non-agricultural screen

| # | Assumption | Value | Where used | Source / justification | Sensitivity / alternative | Disclosed in paper? |
|---|---|---|---|---|---|---|
| G1 | Vacancy proxy | assessed building value < 10% of assessed land value (taxyr 2026 ASMTGIS) | session-built screen (notes/oahu-nonag-solar.md); `oahu_nonag_solar_candidates.csv` `low_improvement_flag` | Only islandwide proxy available; imperfectly flags parks, drainage, paper improvements, entitled-unbuilt land (flagged) | Threshold is arbitrary; no sensitivity run | Yes — §8 states "under 10% of land value (a vacancy proxy)" |
| G2 | Candidate floor | ≥10 ac at ≤15% slope, single parcel (no assembly), non-military, airports/harbors/golf/cemeteries excluded by owner-name keyword | screen + `nonag_classify.py` `strict` tier | Utility-scale minimum; keyword netting is crude | Assembly of adjacent <10-ac parcels ignored → undercount | Yes — §8 |
| G3 | Viability class thresholds | durable if private land < $50k/ac (or public, or quarry/landfill/brownfield); higher-value if ≥ $500k/ac or named entitled-pipeline owner; public-land guard at ≥ $2M/ac → uncertain | `nonag_classify.py` (LOW_VAL, HIGH_VAL, PUB_GUARD) | Ad hoc value cutoffs; pipeline-owner override justified (pipeline land assessed near ag rates pre-subdivision) | Tier totals (≈5,660 / 2,446 / 3,749 ac) move with the cutoffs; no sensitivity run | $50k and $500k yes (§8); **$2M public guard only in Figure 9's embedded annotation**, not the text; pipeline override yes §8 |
| G4 | Named pipeline owners | D.R. Horton, Makaiwa Hills, Haseko/Hoakalei, North Shore Bay/Turtle Bay, Castle & Cooke, Gentry, Ko Olina, Aina Nui (regex) | `nonag_classify.py` PIPE | Hand list from entitlement records | Missing names → misclassified as durable/uncertain | Named in §8 and Fig 9 note |
| G5 | Special-site floor | OSM landfill/quarry/brownfield sites ≥5 ac | `nonag_classify.py` | Ad hoc floor | — | **No** — code only ("roughly 600 net acres" appears without the floor) |
| G6 | Assessed value ≈ economic availability | assessed $/ac used as the price screen | `nonag_classify.py`, §8 | Assessed ≠ market (flagged in METHODS §7) | Market appraisal would re-rank candidates | Partially — §8 says "assessed", caveat in docs |

## H. Wind screen

| # | Assumption | Value | Where used | Source / justification | Sensitivity / alternative | Disclosed in paper? |
|---|---|---|---|---|---|---|
| H1 | 1.25-mi flat floor binds | 10× tip height ≈ 2,000 m ≈ 1.25 mi for ~200 m tips, so the flat floor is mapped; the extra 1×-tip setback from all property lines ignored as second-order | `wind_viable_map.py` (SETBACK = 1.25·1609.344 m) | Ord 25-2 text + modern tip heights | Taller turbines (>212 m tip) would make 10× bind instead, shrinking viable area | Yes — Fig 10 footnote ("1.25-mi flat floor assumed to bind"); §9 states the rule in full |
| H2 | Pre-2025 comparison rule | ≈200 m (~1× tip height) from the same sensitive-zone set | `wind_setback_oahu.py` (SETBACK_OLD=200) | Approximation: the real pre-2025 rule ran from the project parcel's own property lines — "upper-bound-flavored" | True pre-2025 share is parcel-configuration-dependent | Partially — §9 cites "85% under the prior 1×-tip-height standard" without the approximation caveat in text; caveat in Fig 10 annotation, METHODS §8, and the CSV |
| H3 | Sensitive-zone set | C, Resort, Apart, ApartMix, ResMix, A-1/2/3, AMX-1/2/3, R-3.5…R-20 | both wind scripts | Ord 25-2 district list + HCDA-style mixed classes added as apartment-equivalents | Adding/removing mixed classes moves boundaries slightly | Districts named §9; mixed-class addition in docstrings only |
| H4 | Zoning-layer vintage | C&C Honolulu open-data LUO layer, 2024/25 | both wind scripts | As cached | — | Fig 10 footnote yes |
| H5 | Existing-fleet retirement | nonconforming turbines cannot repower beyond current PPAs → ~155 MW retires 2031–2040 | paper §9 | Ord 25-2 repowering clause + PPA end dates | Legislative change could reopen | Yes — §9 |

## I. Macro premises (exogenous to this analysis)

| # | Assumption | Value | Where used | Source / justification | Sensitivity / alternative | Disclosed in paper? |
|---|---|---|---|---|---|---|
| I1 | Decarbonization land requirement | ~30,000 ac ≈ 5–6 GW utility solar at current densities | paper §4 (greedy-curve interpretation; Table 6 tranche 4) | Mike's premise (exogenous); consistent with A1 at 5–6 ac/MW | Higher-density later builds "need less" (stated) | Yes — §4, stated as a premise with the density hedge |
| I2 | Owner count → PPA competition | each owner reached ≈ one potential PPA bidder | `corridor_candidates.py` owners-per-km metric; §4, Table 6 tranche 2 | Design argument, not evidence | Developers, not owners, bid; one developer can option many owners | Yes — §4 states the reasoning as rationale, not finding |
| I3 | $500M program tranche sizes | Table 6 allocations ($150M/$120M/$60–80M/$120M/$30M) | paper §4 Table 6 | Illustrative arithmetic from C5–C8 | Explicitly "illustrative, planning-level" | Yes — labeled illustrative |
| I4 | Campaign-finance attribution windows | sb631 cohort 2006-11-01–2014-12-31; council cohort 2012-01-01–2024-12-31; donor-class regexes | `campaign_finance_extract.py` | Windows bracket the relevant sessions/terms | Different windows change totals | N/A — campaign-finance results are not used in this paper (documentary notes only) |

## Found in code but disclosed nowhere (action items)

1. **D5 — 500 m floor in the greedy candidate score** (`transmission_expansion.py`): affects which spurs are shortlisted. Add to METHODS §4.
2. **C4 — 100-ac far-cluster floor** (`transmission_screen.py`): clusters under 100 ac vanish from `oahu_unlock_clusters.csv` and Figure 3. Add to METHODS §2 / DATA_DICTIONARY.
3. **G5 — 5-ac OSM special-site floor** (`nonag_classify.py`): under-counts small quarry/landfill sites in the "≈600 ac" figure. Add to METHODS §7.
4. **G3 — $2M/ac public-land guard**: in the paper only via Figure 9's embedded annotation; absent from §8 text and METHODS §7.
5. **D2 — 6× slope routing penalty and the 30%-of-cell steepness trigger**: in METHODS but not the paper, though it shapes Figures 5–6 routes.
6. **F1 — RPAD taxyr 2027 vintage and fee-owner-only basis**: docs only; the paper's ownership section (§3) never states the tax year or the leasehold caveat.
7. **B7 — SUP selection caveat**: the paper infers the SUP path is cheap from 8 self-selected applications; deterred non-applicants are unobservable. Worth one sentence in §2.
8. **H2 — pre-2025 wind approximation caveat** absent from the §9 body text (figure annotation only).
