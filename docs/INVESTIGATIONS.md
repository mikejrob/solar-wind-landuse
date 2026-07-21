# Investigations index

Every investigation in one table. Each row: the question, the one-line finding,
the note, key data files, and figures. Prose annotations per note are in
`docs/NOTES_INDEX.md`. Findings tiered verified / plausible / unverified in the
notes.

## Land rules and statutory history

| Investigation | Question | Finding | Note | Data |
|---|---|---|---|---|
| 2011 cap origin | Who inserted the 10% and 20-acre solar caps? | Senate SD1 set 10%; House HD1 added the 20-acre ceiling, sized to the 5 MW competitive-bid threshold. | `notes/sb631-2011.md` | `testimony/sb631_2011/` |
| Pre-2011 bills | What solar-siting bills preceded 2011? | 2008 Act 31 first allowed solar, on D/E soils; a cap was proposed and removed. | `notes/pre2011-solar-bills.md` | `data/pre2011_bills.csv` |
| 2014–2025 acts | What changed after 2011? | Act 55 (2014) added the SUP-above-cap path; no solar-siting change since. | `notes/acts-2014-2022.md` | `data/bills.csv` |
| Wind statutory entry | When did wind become permitted on ag land? | Act 24 (1980), uncapped; unchanged since. | `notes/wind-statutory-entry.md` | — |
| Wind setbacks | What restricts wind now? | Honolulu Ordinance 25-2 (2025): setback ≥ max(10× tip height, 1.25 mi); repowering barred. | `notes/wind-setbacks.md` | `data/wind_setback_bills.csv` |

## Land quantification (GIS)

| Investigation | Question | Finding | Note | Data / Figures |
|---|---|---|---|---|
| Cap scenarios | How much B/C land is solar-eligible? | ~3,600 ac by right; ~15,700 ac at 20% no-hard-cap (4.3×). The 20-acre ceiling binds. | `notes/cap-quantification.md` | `data/cap_scenarios_*.csv`; F1 |
| Grid proximity | How far is eligible land from the grid? | 75% of B/C within 3 km; ~20,400 ac D/E within 1 km. | `notes/oahu-transmission-screen.md` | `data/oahu_land_transmission.csv`; F2, F4 |
| Slope | How much is buildable by terrain? | 6,100 ac (≤15%) to 11,100 ac (≤30%) of near-grid D/E. | `notes/oahu-slope-screen.md` | `data/oahu_parcel_slope.csv`; F7 |
| Ownership | Who owns the ag district? | Government ~50%; Kamehameha Schools ~13% (a quarter of private). | `notes/oahu-ownership.md` | `data/oahu_ag_owners.csv`; F3 |
| Non-ag land | Is there urban/damaged land? | ~11,900 ac urban physically suitable; durable slice ~5,700 ac. | `notes/oahu-nonag-solar.md` | `data/oahu_nonag_solar_candidates.csv`; F9 |
| Military land | Can military land host solar? | ~0 new near-grid civilian supply; energy-security buildout for DoD's own load could reach ~1 GW; federal control, not soil class, is the barrier. | `notes/military-land-solar.md` | `data/oahu_military_land.csv` |
| Golf courses | Can closed courses host solar? | Viable subset is 0; closed courses go to housing or conservation. | `notes/golf-course-solar.md` | `data/oahu_golf_courses.csv` |
| State land | Can the state lease land for solar? | Authority exists (HRS §171-95); use is piecemeal; PLDC repealed 2013. | `notes/state-land-solar.md` | — |
| Slope cost | What does building on slope cost? | No published continuous curve; ≤15% mainstream, 15–30% premium, >30% infeasible. | `notes/slope-cost-literature.md` | — |

## Process to build

| Investigation | Question | Finding | Note | Data |
|---|---|---|---|---|
| SUP census | Does the LUC block solar SUPs? | 8 dockets, 7 approved, 0 denied, 0 intervenors, median ~6 months. | `notes/sup-census.md` | `data/sup_census.csv` |
| Pipeline mortality | Where do projects die? | At HECO procurement and interconnection, not land-use permitting. | `notes/project-pipeline-mortality.md` | `data/oahu_solar_project_pipeline.csv` |
| Project census | Did community resistance block Oʻahu solar? | 0 Oʻahu utility-scale solar projects. Resistance killed 1 Maui solar, 2 wind, 1 biomass. | `notes/hawaii-project-census.md` | `data/hawaii_solar_project_census.csv` |
| HECO procurement | How does the RFP work and where does it fail? | Staged RFP under Docket 2017-0352; median award-to-COD ~5–5.5 yr; cancellations from supply chain, credit, interconnection, price rigidity. | `notes/heco-solar-procurement.md` | `data/heco_procurement_timeline.csv` |
| Procurement comparison | Who procures faster and why? | KIUC ~18 mo (negotiated coop); ERCOT via connect-and-manage; FPL self-builds fast. Speed tracks process design. | `notes/procurement-comparison-kiuc-ercot.md` | `data/procurement_speed_benchmarks.csv` |
| PPA terms | What does HECO require, and what could soften? | Availability toll, not energy contract. Five risk-shifting terms (price rigidity, zero-degradation, 98% availability, full interconnection cost, self-build asymmetry); most are PUC-orderable to soften. | `notes/heco-ppa-terms.md` | `data/ppa_terms_comparison.csv` |
| Neighbor opposition | How does a neighbor oppose a project? | County contested-case intervention (HRS ch. 91) blocks by delay. An IPP cannot condemn a gen-tie easement. | `notes/neighbor-opposition-and-interconnection.md` | — |
| Community resistance | Where has resistance occurred, by island? | 16 cases; wind/biomass/Maui-solar, not Oʻahu solar. | `notes/community-resistance-cases.md` | `data/community_resistance_cases.csv` |

## Political economy

| Investigation | Question | Finding | Note | Data |
|---|---|---|---|---|
| Board interlocks | Are the utility and landholders linked? | HEI–Kamehameha Schools trustee overlaps; HECO officers ran LURF. Structure documented; motive not. | `notes/hei-interlocks.md` | `data/hei_board_interlocks.csv` |
| Campaign finance | Did interested money flow to cap-writers? | No pattern. Zero HEI dollars to the cap-inserting Senate chairs in the 2011 cycle. | `notes/campaign-finance.md` | `data/campaign_contributions_siting.csv` |
| Legal representation | Who lawyers for whom in dockets? | Community intervenors use one small public-interest bar; the landholder bar works for solar. | `notes/legal-representation-map.md` | `data/legal_edges.csv` |
| Food-security frame | Where did the food-security argument come from? | State-supplied vocabulary wrapped around Sierra Club anti-sprawl litigation. | `notes/sierra-club-food-security.md` | — |
| Property tax | How are solar-farm lands taxed? | 2021 reclassification to industrial (~25× jump); Ordinance 21-32 gives an 80% exemption. | `notes/property-tax-wedge.md` | — |

## Grid (companion repository)

Electricity-system modeling continues in
[`oahu-grid`](https://github.com/mikejrob/oahu-grid). Snapshots here:

| Investigation | Finding | Note |
|---|---|---|
| Bulk delivery | No 138 kV north of the central spine; storage-capped N→S requirement. | `notes/oahu-bulk-delivery.md` |
| Grid public record | FERC Form 1 circuit counts; HECO's ~$1.2 B studied delivery options. | `notes/oahu-grid-public-record.md` |

## Synthesis and audit

| Document | Purpose |
|---|---|
| `notes/synthesis-2026-07-11.md` | Cross-thread synthesis of the political-economy hypotheses. |
| `docs/ACCURACY_REVIEW.md` | Internal-consistency audit and verification log (§G verification pass). |
| `docs/ASSUMPTIONS.md` | Every exogenous parameter with its justification and disclosure status. |
| `docs/AUDIT_SOURCES.md`, `docs/AUDIT_REPRO.md` | Source-link and reproducibility audits. |
