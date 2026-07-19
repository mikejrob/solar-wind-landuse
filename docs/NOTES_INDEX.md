# Notes Index

Annotated index of `notes/*.md`. Verification vocabulary used throughout the
notes: **[V]** verified with a primary source (cited by URL), **[P]** plausible
awaiting evidence, **[U]/UNVERIFIED** flagged until confirmed. Ordered
thematically.

## Legislative history

### sb631-2011.md
The origin dossier for the 10%/20-acre solar cap (SB 631 → Act 217, 2011),
verified against bill drafts, committee reports, and testimony PDFs. Key
findings: the 10%-of-parcel cap was inserted by the **Senate** (SD1), and the
20-acre "whichever is lesser" ceiling by House EEP/WLO (HD1) — expressly sized
so permitted solar stays under the ~5 MW utility competitive-bid waiver
(HSCR1152). The cap's constituency was the ag-preservation/planning
establishment (Office of Planning, HDOA, Honolulu DPP, Hawaii Farm Bureau) —
**not** the utility or large landholders: HECO/HEI, LURF, and Kamehameha
Schools never testified; Castle & Cooke supported the *uncapped* introduced
bill. Farm Bureau flipped from strong opposition to acceptance once the 10%
cap was in; Sierra Club opposed even the capped bill. Verification: very high
(all drafts, reports, and testimony cached in `data/raw/capitol/` and
`testimony/sb631_2011/`); a few items flagged TO VERIFY.

### pre2011-solar-bills.md
Pre-2011 attempts to open ag land to solar (~2003–2010) plus early post-2011
follow-ons. Key episode: 2008 HB 2502 → Act 31 first opened solar on D/E
soils only; House EEP inserted a 10-ac/1% acreage cap **endorsed in writing by
HDOA** (the earliest documented acreage-cap advocacy, three years before
SB 631), which the House ag/water-land committees then removed. Revealed 2008
positions: HECO/MECO/HELCO *supported* liberalization, as did LURF and Castle
& Cooke; farm bureaus opposed stand-alone solar. Documents the Wayback recipe
for the Cloudflare-blocked capitol site and HRS-snapshot diffing. Verification:
careful and explicitly search-limited — negative findings ("no bill found in
2009") are flagged as non-exhaustive; several act mappings UNVERIFIED.

### acts-2014-2022.md
Traces every act touching §§ 205-2(d)(6)/205-4.5(a)(20)–(21) after Act 217:
only Acts 52 and 55 (both 2014) changed solar siting; seven later acts left
the solar paragraphs verbatim. Pins the SUP-clause provenance: inserted by
Act 55/SB 2658 (2014) — Senate WTL SD2 on an LUC recommendation, House AGR
HD1, and the new (a)(21) SUP category created in House EEP/WAL HD2. On both
2014 bills the *loosen* side was agricultural (HARC, ranchers, Farm Bureau,
First Wind) and the *tighten* side was state agencies (LUC, DBEDT, HDOA, OP);
First Wind (KS's tenant) requested the 50%-below-FMR co-use condition.
Corrects CLAUDE.md: Act 52 amends only § 205-4.5(a), not § 205-2. LURF,
HECO/HEI, KS filed zero testimony. Verification: high; every claim cites a
Wayback capture; unresolved items marked UNVERIFIED.

### wind-statutory-entry.md
Wind's permissive entry into Chapter 205: **Act 24, SLH 1980 (H.B. 2418-80)**
made wind a permitted use in the ag district with no acreage cap, no
soil-class exclusion, and no decommissioning conditions — before any Hawaii
wind farm existed — and the operative language has never been substantively
amended (only renumbered). Side-by-side text: wind (a)(15) ~50 words vs solar
(a)(20)–(21) ~330 words. Verification: very high (read directly from scanned
Session Laws volumes on the Internet Archive, page-cited). Key gap flagged
[U]: who requested H.B. 2418-80 — 1980 journals exist only on paper (archive
visit pending); an HEI role is plausible-but-undocumented.

### wind-setbacks.md
County wind-setback history culminating in Honolulu **Ordinance 25-2**
(Bill 64/2023, signed 1/3/2025): large wind ≥ max(10× tip height, 1.25 mi)
from residential/country/apartment/resort lots, DPP waivers banned,
repowering clamped — 18 of 20 Kahuku turbines nonconforming, all ~155 MW of
Oahu wind expected retired 2031–2040. Documents the full proposal chain
(Res 19-305 five-mile, Bills 28/10/55) and failed state bills; HECO was the
*sole organizational opponent* of the 2020 state 1-mile bill; wind opposition
was organic. Concludes the solar/wind statutory asymmetry has effectively
reversed at the county level. Verification: high (hnldoc measure pages,
enrolled ordinance PDF); OCR ambiguities and neighbor-island sections flagged.

## Interests and influence

### hei-interlocks.md
Board/executive interlocks from SEC EDGAR DEF 14A proxies (eight years
cached in `data/raw/edgar/`): at least four person-level HEI–Kamehameha
Schools simultaneous roles (Plotts, Lau, Kāne, Kimura); three sitting HEI
directors — including CEO Lau and chairman Watanabe — simultaneously on
Alexander & Baldwin's board during the 2011 SB 631 session; a HECO executive
was LURF president FY2005-06 and HECO a LURF member in 2011; a retired HECO
SVP chairs the LUC as of 2025. Explicit nulls: no Farm Bureau, PUC, legislator,
or Ulupono overlaps found. Feeds `data/hei_board_interlocks.csv`.
Verification: high; distinguishes HEI vs HECO vs ASB boards; unconfirmed
dates flagged UNVERIFIED; LURF rosters FY2009-21 not yet located.

### campaign-finance.md
Money flows to the 16 legislators/council members who controlled siting
bills, from the recovered pre-truncation CSC archive (see METHODS). Headline
is a set of **nulls**: HEI-affiliated money is minimal ($250 total to all 12
SB 631-era legislators in the relevant window; zero to the three Senate
chairs); construction unions dominate the classified total ($316k of $779k);
seed/ag money tracked ag-committee gatekeepers but is confounded by the
concurrent GMO fight. "The rate-base hypothesis gets NO support from
candidate-level campaign money." Feeds `data/campaign_contributions_siting.csv`
and the summary. Verification: strong and self-critical (name-match
confidence flags, explicit per-candidate nulls, known undercounts stated).

### legal-representation-map.md
Tests the astroturf hypothesis via counsel signature blocks in PUC dockets,
LUC SUPs, and appeals: **null in every case**. Community intervenors are
represented by a small recurring public-interest bar with no utility or
landholder clients or lobbyist registrations found; conversely the
traditional large-landowner land-use bar appears *for* renewable applicants,
and legacy landholders appear as project *lessors*, not opponents. Feeds
`data/legal_edges.csv`. Verification: signature-block sourced; the lobbyist
cross-reference uses the 2013–2020 registry snapshot only (2021–26 Salesforce
portal not scraped — flagged limitation).

### sierra-club-food-security.md
Was Sierra Club Hawai'i's 2011 opposition to SB 631 sincere food policy or
the legislative arm of its Koa Ridge/Ho'opili anti-sprawl litigation
strategy? On revealed conduct, largely the latter: same two authors ran both
campaigns; the stated objection (solar raises ag land prices) is exactly the
economic premise the LUC litigation required; the chapter simultaneously
supported solar in every non-ag venue. Explicit funding null: no landholder/
utility funding evidence — the conduct was adversarial to Castle & Cooke and
HECO. Verification: heavily Wayback- and court-opinion-sourced with many
UNVERIFIED tags; falsification tests listed.

## Quantitative screens (Oahu GIS)

### cap-quantification.md
The headline quantification of HRS § 205-4.5(a)(20): current law makes
**3,601 ac eligible on Oahu (~720 MW)**; the S3 counterfactual (20%, no hard
cap) yields 15,657 ac (~3,131 MW, 4.3×; statewide 4.6×). **The hard 20-acre
ceiling, not the percentage, does the constraining**, and it binds on only
85 Oahu / 595 statewide parcels, all >~200 ac — so relaxation mechanically
transfers option value to large landholders. Validated against Office of
Planning 2011 LSB acreage (within 0.2%). Includes the wind-setback STRETCH
(Ord 25-2 cuts viable AG/Country land 85%→36%). Feeds
`data/cap_scenarios_*.csv`. Verification: high on computation; prominent
caveat that these are statutory-eligibility acres, not developable land.

### oahu-transmission-screen.md
Distance-to-grid cross-tabs: grid access is **not** the binding constraint
for B/C land (13,944 B/C ac within 1 km of a mapped 46 kV+ line vs 3,601 ac
legally eligible) — the cap is. Near-grid D/E (no cap, no SUP) is 20,359 ac
within 1 km. Documents the 46 kV under-mapping caveat at length (HIFLD and
OSM barely overlap at that tier; 138 kV is reliable), the corridor-candidate
ranking, and the greedy expansion heuristic (short spurs dominate long
corridors). Feeds `data/oahu_land_transmission.csv` and the `data/gis/`
summary CSVs. Verification: good; data-quality caveats emphatic.

### oahu-bulk-delivery.md
North→south bulk-delivery screenlines (2026-07-12): mapped circuit crossings
at three east–west cuts. SL-A (plateau vs Pearl Harbor load): 8 geometric
138 kV crossings / 5 corridors (parity-net 2 — the Kahe–Halawa/Waiau loops
through the Kunia bench are tappable, so the central ~1,600 MVA reading is
preferred). SL-B (Wahiawa–Waipio): only **2 138 kV circuits** (~445 MVA
central). SL-C (North Shore neck): **zero 138 kV**, 2 mapped 46 kV
(~90 MVA). With 4–6 h co-located storage, required N→S transfer saturates
at σ×evening load (~0.9–1.7 GW), not installed solar MW; SL-C and SL-B bind
from ~0.2 and ~2 GW of northern solar respectively. Closing the gap ≈
$0.1–0.25B (2 GW) / $0.2–0.5B (4 GW) — ~2–5% of solar capex — via parallel
138 kV in existing ROWs (230 kV not needed at 10–25 km). ALL ratings/costs
are flagged planning guesses (HECO data confidential). Feeds
`data/gis/screenline_analysis.csv`, `screenline_requirements.csv`, and
`analysis/figs/paper/f_screenlines.png`. Verification: crossing counts
solid (138 kV mapping reliable); everything else assumption-flagged.

### oahu-slope-screen.md
Slope banding on the 10 m 3DEP DEM. LSB class and slope are highly collinear
(85% of class B under 10% slope; class E 46% over 30%). The money table:
near-grid D/E shrinks from 20,359 ac to 6,083 ac at ≤15% slope. Conversely,
slope does *not* blunt cap reform: ~89–90% of S3-eligible B/C acres sit on
≤15% terrain (flattest-first allocation). Raster/vector cross-validation
within 2%. Feeds `data/oahu_parcel_slope.csv` and `data/gis/oahu_*_by_slope.csv`.
Verification: high; 10 m smoothing caveat noted.

### oahu-ownership.md
TMK-keyed ownership build for the Oahu ag district (99.4% of parcels
attributed): government holds **50.1%** of the district; top owners State of
Hawaii (18.7%), USA (18.4%), Kamehameha Schools (12.8%; 26.1% of private
acres; Gini 0.978). Scarcity-rent finding: cap removal roughly doubles KS's
share of eligible private acreage (7.6%→14.6%); KS is the largest private
"loser" from the per-parcel cap. Feeds `data/oahu_ag_owners.csv`.
Verification: high, with per-row confidence flags; assessment owner ≠
beneficial owner caveat; DCCA cross-reference deferred to Phase 4.

### oahu-nonag-solar.md
How much *non*-ag (urban-district) Oahu land could host solar: ~11,900 ac
durable at ≤15% slope (~1,700–2,400 MW) on low-improvement non-military
urban parcels plus landfills/quarries/brownfields. Conclusion: physical
scarcity of non-ag land is **not** what confines solar to ag land — the
constraint is economic (urban land value; entitled housing pipeline). The
defensible durable slice is ~4,600–5,300 ac (public land + brownfields).
Feeds `data/oahu_nonag_solar_candidates.csv` and figure `f_nonag_map.png`.
Verification: moderate — RPAD/OSM sourced, vacancy proxy imperfect, several
UNVERIFIED site details flagged.

### slope-cost-literature.md
Literature/engineering review of solar cost vs slope: standard practice
0–10%; buildable 10–20% at a real but unpublished premium; terrain-following
racking demonstrated to ~25–37% (single-vendor evidence). **Key gap: no
published continuous cost-vs-slope curve exists** — NREL treats slope as a
binary exclusion. Hawaii specifics: no utility-scale project found on >15%
average slope; Honolulu grading rules make 15% and 40% bright regulatory
lines. Verification: unusually rigorous source tiering; several figures
explicitly marked "do not cite."

## Institutions and land

### sup-census.md
Census of LUC solar Special Use Permits: the population 1963–present is
**exactly 8, all post-Act 55 (2014)** — 7 approved unanimously, 1 pending,
0 denied, **0 intervenors in 8 dockets**. LUC stage is fast (median 34 days);
county stage carries the variance. The SUP operates as a *compliance tax*
(below-market ag co-use, decommissioning security) whose incidence favors host
landowners; opposition does not surface there. Selection: the LUC tier is reached only by
projects wanting >20 ac of B/C soils — typically on large legacy-landholder
land. Feeds `data/sup_census.csv`. Verification: LUC tier complete
(docket sequence enumerated, gap #410 documented); Maui county-tier records
403-blocked (UIPA request flagged).

### state-land-solar.md
Nothing in Hawaii law prevents leasing state land for solar (direct-
negotiation path since 2002/2009, §§ 171-95/95.3, 65-year terms, used by
DHHL/UH/DLNR) — what's missing is any *program* for DLNR/ADC fallow ag land.
Binding constraints are political (the 2011–13 PLDC creation-and-repeal
episode), institutional (ADC mission; >1,700 idle central-Oahu acres per
Audit 21-01), and procedural — not statutory. Corrects earlier act-number
errors (PLDC repeal = Act 38/2013; Act 176 is a sales moratorium).
Verification: high, with many UNVERIFIED tags on project statuses.

### property-tax-wedge.md
Stub on the county fiscal layer: Honolulu ag dedication assesses dedicated ag
land at 1–5% of FMV (near-zero carrying cost — subsidized land banking),
while in 2021 the assessor reclassified operating solar farms ag→industrial
(~25× tax jump mid-PPA; Clearway ~$30k→~$800k/yr), patched by an 80%
renewable exemption whose ordinance status is **UNVERIFIED**. Flags the
discretionary ex-post repricing as a regulatory-risk premium on PPA bids.
Verification: mechanics and the 2021 shock primary-sourced; Bill 39
follow-ups open.

## Synthesis

### synthesis-2026-07-11.md
End-of-day-one synthesis across all threads — the paper's skeleton. Inventories
the four restriction layers by technology, tabulates who built and maintains
the solar cap (tighten side: HDOA/OP/county planning/Farm Bureau + Sierra
Club; liberalize side: energy agencies, solar industry, the utility, and
large landholders), and scores the three working hypotheses against the
evidence (scarcity-rent: mechanically supported; rate-base: no support in
testimony or campaign money; astroturf: null everywhere tested). Every line
carries a [V]/[P]/[U] status tag pointing back to the per-thread notes.

> Grid-thread notes (oahu-bulk-delivery, oahu-grid-public-record) are frozen copies as of 2026-07-12; development continues in the `oahu-grid` repository.
