# Census of Special Use Permits for Solar Energy Facilities in Hawaii, 2008–2026

Compiled 2026-07-11. Data: `data/sup_census.csv`; documents: `data/raw/dockets/sp*/`.

## Method

1. **LUC tier (state special permits, HRS §205-6, >15 acres).** The open directory
   at files.hawaii.gov/luc/dockets/ is currently 403-blocked (directory listing
   disabled; individual PDFs remain fetchable with a browser User-Agent). Frame
   built instead from the LUC's complete "Completed Dockets — Special Permits"
   index (luc.hawaii.gov/completed-dockets/special-permits/ + per-county pages)
   plus the pending-dockets index. SP dockets are numbered sequentially statewide;
   the 2005–2026 sequence (SP05-399 … SP26-417) is continuous **except #410**
   (see gaps). Every docket title 2005–2026 was inspected; old dockets with
   recent motion activity (SP90-374 Parker Ranch, SP92-380/381, SP97-390,
   SP09-403) were checked for solar amendments — all are quarry/landfill matters.
2. For each solar docket: downloaded D&O, county transmittal, director's/staff
   report, OP/OPSD comments, minutes, testimony (to `data/raw/dockets/<docket>/`),
   extracted with pdftotext (+ OCR spot-checks), coded fields per document text.
3. **County tier**: web/agenda search across the four counties (see gaps).
4. **Dogs that didn't bark**: HECO Stage 1/2/3 and KIUC projects cross-checked
   against the docket census.

Date conventions in the CSV: `county_decision` = planning-commission approval
vote (written D&O date in notes when it differs); `luc_decision` = LUC approval
vote (D&O filing date in notes). Durations: `duration_county_days` =
county_filed→county_decision; `duration_luc_days` = luc_transmittal→luc_decision.

## The census

**Population of LUC solar special-permit dockets, 1963–present: exactly 8.
Zero before 2015.** All eight fall after Act 55/2014 created the
§205-4.5(a)(21)/§205-2(d)(6) SUP path for above-cap solar on B/C soils.

| Docket | Year | County | Project (MW) | Landowner | Outcome | Vote |
|---|---|---|---|---|---|---|
| SP15-405 | 2015 | Honolulu | Waipiʻo PV (47) | Renewables Land Holdings (ex-Castle & Cooke) | approved | 8-0 |
| SP15-406 | 2015 | Honolulu | Kawailoa Solar (50) | **Kamehameha Schools** | approved | 7-0 |
| SP15-407 | 2016 | Kauai | SolarCity Kapaia (13) | Grove Farm | approved | 8-0 |
| SP17-408 | 2017 | Kauai | AES Lawaʻi (28) | McBryde Sugar (A&B) | approved | 7-0 |
| SP21-411 | 2021 | Honolulu | AES West Oʻahu (12.5) | University of Hawaiʻi | approved | 8-0 |
| SP21-412 | 2021 | Honolulu | Mahi Solar (120) | Monsanto / Hartung Bros / Fat Law's Farm | approved | 8-0 |
| SP26-416 | 2026 | Kauai | Kaʻawanui Solar (43) | Robinson Family Partners | approved | 6-0 |
| SP26-417 | pending | Maui | Kūihelani Phase 2 (40) | MP West (Mahi Pono, ex-A&B) | pending | — |

Counts: by county — Honolulu 4, Kauai 3, Maui 1 (pending), Hawaii 0. By outcome —
7 approved (all unanimous), 1 pending, **0 denied, 0 withdrawn** at the LUC.
By year — 2015×2, 2016×1, 2017×1, 2021×2, 2026×2.

### Durations

| Docket | County stage (days) | LUC stage (days) | Total filed→LUC vote |
|---|---|---|---|
| SP15-405 | 124 | 38 | 181 |
| SP15-406 | 159 | 32 | 214 |
| SP15-407 | 27 | 35 | 105 |
| SP17-408 | 40 | 27 | 83 |
| SP21-411 | 197 | 41 | 282 |
| SP21-412 | 182 | 34 | 260 |
| SP26-416 | 64 | 9 | 128 |
| SP26-417 | 218 | — | pending |

Medians: county stage **141.5 days** (Kauai is far faster: 27–64; Honolulu
124–197; Maui 218 and counting); LUC stage **34 days** (range 9–41 — the
45-day statutory clock in §205-6(e) binds and is always met); total
**~181 days**. The LUC stage is a small, predictable fraction of total
permitting time; the county stage is where variance lives.

### Intervenors and opposition

**Intervenor rate at the LUC: 0/8 (zero).** No party ever sought or obtained
intervention in any solar SP docket. Opposition testimony is nearly absent:
- SP15-406: literally zero public testimony at any county or LUC hearing.
- SP17-408: four individual residents at county PC; one opposed siting on
  prime ag land ("I like solar… I don't like the idea of it in prime ag land").
- SP21-411: ~10 individual opposition emails at the county stage (ag-land-loss
  and Makakilo-resident themes; near-identical subject lines suggest a small
  coordinated email effort, but all individuals — no organizations). All 7 oral
  witnesses at the LUC supported.
- Everything else: support or agency comments only.

**Who testifies FOR solar SUPs:** construction unions (PRP, IBEW, Carpenters,
Operating Engineers — both 2021 Oahu dockets), HSEO, HECO (written support in
both 2021 Oahu dockets, via Rebecca Dayhuff Matsushima), Ulupono, HARC, and
the ag tenants who will graze the sites. HDOA/Board of Agriculture in SP21-412
was supportive but pointed: "research alone is not a satisfactory outcome, nor
is sheep used only for weed control."

Contrast (for the wind/solar asymmetry file): in the same period the LUC solar
dockets drew zero intervenors, Na Pua Makani wind drew ~200 arrests, and the
only successful organized opposition to a solar land-use permit anywhere in the
state was **Paeahu Solar** — in a *county* forum (Maui PC permit vacated by the
2nd Circuit, Jan 2022, Pono Power Coalition), not at the LUC.

### Repeat players

- **Counsel**: Matsubara Kotake (& Tabata) appears in 5 of 8 dockets
  (SP15-407, SP17-408 LUC stage, SP21-411, SP26-416, SP26-417) — the de facto
  LUC solar bar. McCorriston Miller Mukai MacKinnon: 2 (SP15-406, SP21-412).
  Carlsmith Ball: 1 (SP15-405). Belles Graham is the recurring Kauai local
  counsel (SP17-408, SP26-416).
- **Applicants**: AES 4 of 8 (408, 411, 416, 417); First Wind→SunEdison
  (completed by Clearway) 2 (405, 406); SolarCity/Tesla 1; Longroad 1.
- **Landowners**: uniformly large legacy landholders or institutions —
  Kamehameha Schools, Grove Farm, McBryde/A&B, Robinson Family Partners,
  Mahi Pono (ex-A&B/HC&S), Castle & Cooke (via Renewables Land Holdings),
  Monsanto/Hartung/Fat Law's (Kunia corridor), and UH (public). No small
  landowner has ever obtained (or sought) a solar special permit. Median
  host parcel among stated values: ~2,950 acres.
- Governance conduct worth noting: SP26-416 — LUC commissioner **recused as a
  sitting KIUC director** (the off-taker); SP21-412/SP15-406 — Chair Scheuer
  disclosures (spouse's firm; prior work for KS), participated without objection.

### Conditions patterns

- The §205-4.5(a)(21) trio (≥50%-below-FMR ag co-use, decommissioning
  security, restoration) appears verbatim in every D&O. Actual ag co-use is
  grazing/apiary in every case (sheep 5×, cattle 1×, bees 2×; SP21-412 alone
  promises 488.9 ac of cultivated food crops + HARC agrivoltaics). Two
  applicants voluntarily exceed the statutory floor with **zero-rent** ag
  licenses (SP26-416 to a Gay & Robinson family branch; SP26-417 to Living
  Pono Project) — the below-market-ag-lease condition is in practice a
  transfer to grazing operators selected by the landowner/developer.
- Ag-establishment window: 6 months of commercial operation (1 year in
  SP15-405 only; OP tightened to 6 months from SP15-406 onward).
- Decommissioning security: quantified only on Oahu — $4,000,000 flat
  (SP15-405, SP15-406), $6,830/acre (SP21-412); Kauai leaves the amount to the
  county planning department (no dollar figure in any Kauai record); security
  runs to the *landowner* on Oahu, to the *county* on Kauai.
- Permit terms: 35 years is the norm (405, 406, 407, 408, 416); 29 years
  (411); 25+10 (412); 30 requested (417). A recurring quiet fight: counties
  drafting extension authority to themselves and the LUC/OPSD restoring "LUC
  approval required for extensions" (SP17-408, SP26-416 — explicit staff
  amendments).

## The selection margin: why so few dockets (key statutory finding)

Current **§205-2(d)(6)** (verified via Wayback snapshot of capitol.hawaii.gov
hrscurrent, 2026-04-10; identical structure in the 2020 snapshot): solar is a
permitted ag-district use on soils **B, C, D, or E**; the 10%-of-parcel/20-acre
cap — and therefore the §205-6 SUP — applies **only to B and C soils**. On D/E
soils there is no state-level cap and no SUP requirement at all. §205-6(d)
(same snapshots: no solar carve-out, amendment line shows no 2014 change to
§205-6) routes any special permit >15 acres to the LUC.

Consequences, all visible in the data:
1. **The county-only §205-6 window for solar is empty by construction.** A
   solar SUP is needed only above the 20-acre cap, but ≤15-acre permits are the
   only ones counties decide alone. We found **no verified county-only §205-6
   solar SUP** in any county (Hawaii County's searchable Laserfiche archive:
   none; the only real candidate is pre-2011 La Ola on Lanai, unresolved
   because Maui archives are script-blocked). Essentially all §205-6 solar
   flows through the LUC.
2. **The Maui/Big Island "county-only" utility-scale projects are not §205-6
   SUPs.** Kūihelani Ph1 (60 MW, ~450 ac, county CUP 2021/0003), Paeahu,
   Pūlehu, Hale Kuawehi, Waikoloa cleared with county-code permits (e.g., MCC
   19.30A.060(A)(12) county SUP for solar >15 ac in county ag zoning) —
   consistent with siting on D/E soils where state law imposes no cap.
   (Soil-class basis per project: UNVERIFIED — worth confirming from county
   files; the Kūihelani Ph1-vs-Ph2 contrast on adjacent Mahi Pono land, where
   Ph2's 365 ac of class B soils forced it to the LUC in 2026, is the clean
   illustration.)
3. **Selection into the LUC tier = "wants >20 acres of B/C (prime-adjacent)
   soils."** That is why the LUC docket list reads as a roster of legacy
   landholders: only large owners of good ag land ever need the permit. The
   zero-denial, zero-intervenor, unanimous record then says the *screening*
   is not happening at the LUC — the binding constraints are upstream (the
   cap itself, county stage-length, PPA procurement) — while the SUP process
   adds conditions (below-market ag co-use, decommissioning security, term
   limits) that function as a tax on above-cap solar paid partly to landowners'
   own grazing affiliates.

## Dogs that didn't bark (announced ag-land projects with no SUP docket)

| Project | Island | Landowner | Route around the SUP | Status |
|---|---|---|---|---|
| Hoʻohana Solar 1 (52 MW) | Oahu | Robinson Kunia Land | **Urban district** via motions to amend old boundary-amendment docket A92-683 (2020–2024) — Farm Bureau, Sierra Club, OP, HDOA opposed in 2019 (testimony trail for Phase 4) | operating (COD notice 2025-07-29) |
| Kupono Solar (42 MW) | Oahu | US Navy (JBPHH) | Federal land — ch. 205 inapplicable | operating 2024 |
| Clearway Mililani I (39 MW, 131 ac) | Oahu | Castle & Cooke (Mililani Ag Park) | No SP docket; mechanism UNRESOLVED (D/E soils or parcel structuring) — flagged | operating ~2021-22 |
| Clearway Waiawa (36 MW, 180 ac) | Oahu | **Kamehameha Schools** | No SP docket; district UNVERIFIED (possibly Urban master-plan lands) | operating ~2023 |
| AES Mountain View (7 MW) | Oahu | UNVERIFIED | No SP docket | construction 2023→ |
| Kūihelani Ph1, Pūlehu, Paeahu, Hale Kuawehi, Waikoloa | Maui/Hawaii | Mahi Pono, —, Ulupalakua, Parker Ranch, — | County permits only (see selection margin above) | various |
| Barbers Point Solar (15 MW) | Oahu | DHHL (Kalaeloa) | cancelled May 2022 (Innergex pullout) | dead |
| Kahana Solar (20 MW) | Maui | UNVERIFIED | cancelled May 2022 | dead |
| Waiawa Ph2 / AES (30–60 MW) | Oahu | UNVERIFIED (KS?) | delayed; no SP docket | UNVERIFIED |

Pattern: on Oahu, big ag-land solar goes through the LUC SUP or an urban DBA;
on the neighbor islands 2019–2023, everything cleared at county level. The one
documented organized-opposition episode against solar land-use permits
(Farm Bureau/Sierra Club/OP/HDOA vs Hoʻohana, 2019) happened in a *boundary
amendment* docket, not an SUP docket — and the one successful legal challenge
(Paeahu) happened in a county forum. The LUC SUP track itself has never been
contested.

## Coverage and gaps

- **LUC tier: complete.** Full docket index enumerated 1963–2026; titles
  inspected 2005–2026; old-docket amendments checked. **Docket #410 is missing
  from the numbering sequence** (SP17-409 → SP21-411; all sp{18,19,20,21}-410
  URL guesses 404) — plausibly a withdrawn/never-perfected application in
  2017–2021; worth an email to LUC staff. LUC standalone FY annual reports
  could not be located online (docket "annual reports" are permittee compliance
  filings); the docket index is a stronger source anyway.
- **files.hawaii.gov/luc/dockets/ directory listing is 403** (previously an
  open tree); individual files still download with a browser UA.
- **capitol.hawaii.gov is Cloudflare-blocked** to scripts; statute text
  verified via Wayback snapshots (§205-6: 2026-06-25 and 2020-04-24 captures;
  §205-2: 2026-04-10 capture).
- **Maui County ArchiveCenter (all three planning commissions) returns 403**
  even with a browser UA — the biggest gap; all four small county-tier
  candidates (La Ola, Kuʻia, SMRR, Molokai NEP) and the Maui CUP records sit
  behind it. A UIPA request or manual browser session would resolve them.
- **Honolulu DPP** SUP case files are not full-text searchable online (records
  request required). **Hawaii County** Laserfiche is searchable (best
  coverage; no county-only solar found). **Kauai** PC agendas accessible;
  nothing county-only found.
- SP26-417 is mid-stream: pull the Maui PC written D&O (adoption set
  2026-07-14), the county testimony record on transmittal, and the LUC
  2026-08-19 agenda/decision when posted.
- County-stage *filing* dates for the county-tier rows are unpopulated
  (records inaccessible); those rows carry explicit UNVERIFIED flags.

## What the selection pattern shows (for the paper)

The 10%/20-acre cap does not operate as a project-size screen at the LUC — it
operates upstream as a *soil-class and landowner* screen. Every above-cap
project that reached the LUC sat on B/C soils held by a large legacy
landholder or institution, arrived lawyered (usually by the same firm), faced
no intervenors, and passed unanimously in ≤45 days with boilerplate
(a)(21) conditions. Meanwhile comparable projects on D/E soils (or Urban/
federal land) skipped the state process entirely. The permitting friction the
statute creates is therefore not "opposition venue" friction — it is a
compliance tax (ag co-use at ≥50% below FMR, decommissioning security, term
limits, annual reporting) whose incidence favors host landowners (security
runs to the landowner on Oahu; ag co-use is typically a zero-rent license to
a landowner-affiliated grazier). A null on the astroturf hypothesis at the
LUC: the only coordinated activity in these dockets is *pro*-solar (unions,
HECO, HSEO). The scarcity-rent hypothesis, by contrast, gets mechanical
support: the cap binds only on prime-soil land, and the SUP relief valve has
been used exclusively by — and its conditions negotiated with — the state's
largest landholders.
