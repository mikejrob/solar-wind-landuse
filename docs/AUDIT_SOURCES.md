> **STATUS (superseded 2026-07-17):** This report was written 2026-07-12 and
> lists paper errors that have SINCE BEEN FIXED. All B1/B2/B3/B5/B6/B7/B8
> corrections were applied to `paper/land-restrictions-paper.html` and
> `-final.html`. See `docs/ACCURACY_REVIEW.md` (2026-07-17) for the current
> state — the fixes are confirmed propagated there. Retained as a record of
> what was found and changed.

# Source & Number Audit — paper/land-restrictions-paper.html

Audit date: 2026-07-12. Auditor: Claude (adversarial source audit; no paper or
notes files were edited). Scope: (1) every quantitative claim and factual
assertion in `paper/land-restrictions-paper.html` traced to `data/` CSVs,
`notes/*.md` primary-source citations, or an explicit UNVERIFIED/derived flag;
(2) cross-check of ~40 headline numbers among paper, notes, and CSVs;
(3) resolution check of a stratified sample of URLs from `notes/*.md` and the
docket/bill CSVs, with content verification of the most load-bearing.

---

## A. Verified clean (summary)

Roughly 90 quantitative claims and factual assertions were traced. The large
majority verify exactly against the repository data and notes, including every
number checked in the following groups:

- **Cap scenarios** (`data/cap_scenarios_results.csv`,
  `notes/cap-quantification.md`): Oahu S0 3,601 ac / 720 MW; S1 9,410;
  S2 4,743; S3 15,657 / 3,131 MW; Fig. 8 statewide 33,978 → 157,213. Exact.
- **Expansion curve** (`data/gis/expansion_curve.csv`,
  `notes/oahu-transmission-screen.md`): baseline 16,328 of 40,870 (40%);
  L = 10/25/50/100 km → 20,185 / 24,195 / 29,481 / 36,103 (paper values are
  linear interpolations of the step log — all match); first three spurs
  ~2.2 + ~2.9 + ~0.6 km, +2,252 ac; ~400–480 ac/km plateau to ~11 km. Exact.
- **Wind screen** (`data/gis/wind_viable_areas.csv`, `wind_setback_oahu.csv`,
  `notes/wind-setbacks.md`): 39,386 ac; 36.3% of 108,417 AG/C acres; prior
  rule 84.7% ("85%"); 26,023 ac ≤30% slope; Waialua ~21,200 (39% >30%);
  Kunia ~7,800 (89% ≤30%); 18 of 20 Kahuku turbines nonconforming (Civil Beat,
  cited); retirement 2031–2040. All match (one exception, §B7).
- **Ownership** (`notes/oahu-ownership.md`, `data/oahu_ag_owners.csv`):
  government 50.1% (state 25.8, federal 19.6, county 2.7, DHHL 2.0);
  KS 12.8% of district / 26.1% of private; top-20 private 71.2%; 99% acreage
  attribution; 118 cap-bound parcels (>200 ac with B/C), 25,200 B/C ac, led by
  US / KS / Dole / State. All match.
- **Table 3 (parcel size × owner scale)**: every cell reproduces exactly from
  `data/oahu_land_transmission.csv` × `data/oahu_ag_owners.csv` (independent
  recomputation, this audit): 118 cap-bound parcels = 49 government + 43
  large/major private + 26 mid-size private; exposed set 26 owners / 3,674 B/C
  ac; zero small owners. Correct — but see §D1 (no notes file documents this
  table).
- **SUP census** (`data/sup_census.csv`, `notes/sup-census.md`): 8 dockets,
  docket IDs, 7 approved / 1 pending / 0 denied / 0 withdrawn, all unanimous;
  0/8 intervenors; medians 141.5 d county / 34 d LUC / ~181 d ≈ 6 months;
  AES 4/8; Matsubara Kotake & Tabata 5/8; earliest filing 2014-09-05
  ("since 2014" ✓); landowner roster matches.
- **Transmission cross-tab** (`notes/oahu-transmission-screen.md`,
  `data/gis/oahu_class_by_band.csv`): Fig. 2 within-1-km values 20,359 D/E,
  13,944 B/C, 8,497 A; 75% of B/C within 3 km; ~325 km 138 kV; ~80 km mapped
  46 kV. All match the note.
- **Corridors and ring** (`data/gis/oahu_corridor_candidates.csv`,
  `oahu_ring_1_3km_summary.csv`): ring ≈24,000 ac ≤30% / ≈18,000 ≤15%,
  28 owners; C01 14,210/2,842 MW/18 owners; C03 5,697/1,139/5 owners/74% B/C/
  ~2 km; C02 8,749/1,750/majority federal. Match (C04 exception, §B6).
- **Slope** (`data/gis/oahu_de_neargrid_by_slope.csv`, `oahu_s3_by_slope.csv`,
  `notes/oahu-slope-screen.md`): Table 7 D/E and B/C-S3 band acreages exact;
  D/E ≤15% 6,083 / ≤30% 11,110; S3 89% ≤15%, 97% ≤30%; 45% of near-grid D/E
  >30%; raster/vector reconcile 20,360 vs 20,359 ("within one acre" ✓);
  LSB totals vs OP 2011 within +0.2% (`lsb_sanity_totals.csv`).
- **Non-ag screen** (`notes/oahu-nonag-solar.md`,
  `data/oahu_nonag_solar_candidates.csv`, `data/gis/nonag_top_parcels.csv`):
  290 parcels / 11,319 ac ≤15% / 13,557 ≤30%; ~600 net special-site ac;
  ~11,900 total; durable 143 parcels + 12 sites ≈ 5,660 ac / 810–1,130 MW;
  uncertain 58 / 2,446; pipeline 89 / 3,749; median $124k/ac, p75 $1.2M;
  military ~16,000 flat ac; conservation 158,668 ac; urban 104,231 ac; all
  Table 9 site rows (Waiawa 598 @ $43k, Heʻeia 222 @ $19k, etc.). The "~1,080
  flat acres" KS Waiawa block = TMKs 196005013 + 196004031 (598 + 479 =
  1,077) — derivable from the CSV though not stated in the note.
- **Legislative history** (`notes/sb631-2011.md`, `pre2011-solar-bills.md`,
  `wind-statutory-entry.md`, `acts-2014-2022.md`): 1976 Act 199; 1980 Act 24
  wind entry with "small footprint" rationale; 2008 Act 31 (HB 2502) D/E
  opening; 2011 Act 217 with 10% term from Senate SD1 and 20-acre term from
  House HD1 sized to the 5 MW competitive-bid waiver (HSCR1152, quoted in the
  note); 2014 Acts 52/55 SUP path; seven 2015–2025 amendments (Acts 228, 173,
  49, 77, 131, 182, 255) none touching solar text; §11's characterization of
  who asked for the caps (OP, DOA, DPP, Farm Bureau) vs who wanted width
  (Castle & Cooke, solar industry) is supported by the testimony tables in
  the notes.
- **State land** (`notes/state-land-solar.md`): §171-95 (Act 102, 2002,
  65 yr); §171-95.3 (Act 19, Sp 2009); Act 53 (2024) dropped the
  sell-to-utility requirement; ADC auction exemption; Kalaeloa Solar Two 2013;
  UH West Oʻahu 12.5 MW (2024); Eurus Olai ~20 MW BLNR Jan 2026; ADC Audit
  21-01 "more than 1,700 acres idle"; Kupono ~42 MW; OHA PLT share; HECO REZ
  workshops July 2026.
- **Slope-cost / engineering** (`notes/slope-cost-literature.md`): NREL
  benchmarks flat-site only; supply-curve binary screens (10% reference /
  5% restrictive); 15% N–S tracker spec; ~20% built precedent, 25% planned;
  one vendor's 37% spec; Honolulu grading code engineer's-soils-report
  threshold. All present with URLs in the note.
- **Property tax** (`notes/property-tax-wedge.md`): 1–5% assessment under ag
  dedication; $12.40/$1,000 industrial; ~25× reclassification shock (2021,
  Star-Advertiser cited). Match (Bill 39 exception, §B4).

The paper's use of the `U`/derived tags is generally honest: the Hawaiʻi
construction multiplier, the slope-cost "derived" premiums, and the pending
SP26-417 are all flagged in the paper itself.

---

## B. Discrepancies found (paper vs repository record)

**B1. MAJOR — §1 first paragraph: size of the agricultural district.**
Paper: "the agricultural district covers about 276,000 acres of Oʻahu
(roughly 47% of the island)." The repository's own SLUD layer
(`notes/cap-quantification.md` §"LSB class acreage WITHIN the State Ag
District"; `notes/oahu-nonag-solar.md` context table) puts the Oʻahu
agricultural district at **120,789 acres (~31–32% of the island)**. The
276,006-acre figure is the island-wide LSB-rated total (A+B+C+D+E across all
districts), and 47% appears to be the *statewide* ag-district share. Note the
internal contradiction: §8 gives conservation 158,668 + urban 104,231 acres;
adding a 276,000-acre ag district exceeds the area of Oʻahu.
*Fix: "about 121,000 acres (roughly a third of the island)."*

**B2. MAJOR — Table 1, "Oʻahu ag-district acres" column.** The column values
(A 16,031; B/C 40,812; D/E 219,163) are the **island-wide** OP-2011 LSB
totals (`data/gis/lsb_sanity_totals.csv`), not ag-district acreage. The
in-district values per `data/gis/lsb_in_ag_district_totals.csv` and
`notes/cap-quantification.md` are **A 15,106; B/C 34,877; D/E 65,076**.
Everything else in the paper (Fig. 2, §5, §6, the cap scenarios) uses the
in-district figures, so Table 1 is inconsistent with the paper's own later
numbers (e.g., Fig. 2's bands for B/C sum to 34,877, not 40,812).
*Fix: replace the column with the in-district totals, or relabel the column
"Oʻahu LSB-rated acres, all districts (OP 2011)" — the former is what the
table caption promises.*

**B3. Abstract: "about 40,600 acres of agricultural-district land lie within
1 km of a mapped 46 kV+ line."** The class×band cross-tab
(`notes/oahu-transmission-screen.md`) sums to **42,800 acres within 1 km**
(8,497 A + 13,944 B/C + 20,359 D/E) — the same components Figure 2's caption
lists. 40,600 matches no repository figure (nearest candidates: 40,870 =
island-wide eligible B–D ≤30% acres; 40,565 = D/E within 3 km). *Fix: "about
42,800" (or "~34,300 excluding class A" if class A was meant to be omitted —
but then the abstract's next sentence must not say "of that" for the A-class
component).*

**B4. §1 and Table 8 (2021 row): the 80% renewable property-tax exemption is
stated as enacted.** `notes/property-tax-wedge.md` explicitly flags Bill 39's
"ordinance number/current status **UNVERIFIED — follow up**". The paper
asserts "an 80% exemption for renewable projects was subsequently enacted"
with no U tag. *Fix: verify Bill 39 (2021) enactment (ROH §8-10 amendment) or
tag the sentence U.*

**B5. §7: "HARC's 230-acre Mililani agrisolar site has cultivated crops under
panels since 2022."** No notes file contains this claim, the acreage, the
location, or the date. The only HARC agrivoltaics statements in the notes
place HARC's visible trial "on its own **Kunia Research Station** land"
(`notes/state-land-solar.md` §5.3) and reference planned HARC agrivoltaics in
SP21-412 (Kunia). "Mililani" appears in the notes only as Clearway's Mililani
I solar farm. Location, acreage, and start date are all unsourced and the
location conflicts with the notes. *Fix: source it (HARC/Clearway Mililani
agrisolar press material, if that is what was meant) or cut/tag U.*

**B6. Table 4, C04 Kahuku row: 5,630 ac / 1,126 MW / PRI 33%.**
`data/gis/oahu_corridor_candidates.csv` has **5,618 ac ≤30% / 1,124 MW /
Property Reserve 32%**. The paper's 5,630 equals the pre-class-A-exclusion
value (the note records C04 losing ~12 A acres in the 2026-07-12 revision).
Small, but the paper mixes revisions within one table (C01/C02/C03 use
post-revision values). *Fix: 5,618 / 1,124 / 32%.*

**B7. §9: "the Kahuku and Kawailoa hills (~8,100 acres, majority steep)."**
`data/gis/wind_viable_areas.csv`: Kahuku 4,136 ac (53% >30% — majority steep)
but Kawailoa 4,012 ac (only 25% >30%). Combined: 39% >30% — **not** majority
steep. *Fix: "Kahuku hills (~4,100 ac, majority steep) and Kawailoa hills
(~4,000 ac, mostly gentle)" or drop "majority steep" for the combined figure.*

**B8. Table 1, class A row: "No solar SUP on A-rated land has ever been
granted; applicants carve A soils out of project areas."** Contradicted by
the repository's own census: SP15-406 (Kawailoa Solar, **granted** 2015) is
described in the cached DPP D&O (`data/raw/dockets/sp15-406/
SP15-406-DPP-LTR-FOF-COL-DO1.pdf`, FOF 1) as an SEF "on Land Study Bureau …
Class 'A', 'B', 'C', and 'E' lands", and `data/sup_census.csv` codes SP15-406
soil as "A/B/C/E (majority B; panel areas on A and B)". The carve-out pattern
is documented only for the later dockets (411/412/416/417 are "no A").
*Fix: qualify — e.g., "since 2021 applicants have carved A soils out of
project areas; the one earlier Oʻahu SUP (SP15-406, 2015) included class-A
land" — or reconcile with the docket record.*

**B9. §10: HB 778 (2025) described as "a state-lands renewable study."**
`notes/state-land-solar.md` describes HB 778 as an OPSD **integrated ag-district
land-use study** reconciling housing/food/RPS targets — which "could put state
parcels on the solar map" — not a state-lands renewable study per se. Minor
characterization drift. *Fix: "commissioned an integrated ag-lands use study
(HB 778, 2025) that bears on state parcels."*

**B10. §9: "~155 MW of existing wind."** Derived from
`notes/wind-setbacks.md` (Kahuku ~30 + Na Pua Makani "up to ~55 MW nameplate
potential" + Kawailoa ~69). The NPM figure is flagged in the note as
nameplate *potential* for 8 turbines; NPM's installed capacity is commonly
reported at ~24–27 MW, which would put the fleet nearer ~125 MW. Not checked
against a primary source in the repo. *Fix: verify NPM installed MW or tag.*

---

## C. Dead / wrong / problematic links

Inventory: **280 unique URLs** (notes/: 212 unique — acts-2014-2022 100,
wind-setbacks 50, slope-cost-literature 49, sierra-club-food-security 29,
wind-statutory-entry 19, others ≤5; CSVs: sup_census 48, bills 20,
pre2011_bills 12, wind_setback_bills 12). **59 sampled** (curl, browser UA,
GET retry on HEAD failure), covering every notes file with URLs plus the four
CSVs. **10 load-bearing sources content-fetched and read against the citing
sentence.**

**C1. DEAD — all NREL links (slope-cost-literature.md lines 42, 150, 151,
plus ~3 more untested).** The entire nrel.gov domain failed DNS at audit time
(no .gov NS delegation per DoH; the site was alive per an April 2026 Wayback
capture — possibly a federal-web outage, but currently every NREL citation in
the note is unreachable). Wayback rescues verified available:
`web.archive.org/web/20250504143930/` (83586.pdf, Q1-2022 cost benchmark),
`/20250322184808/` (87524.pdf, reV siting regimes), `/20260428012312/` (ATB
utility-scale PV page). *Fix: add the Wayback URLs alongside the live ones.*

**C2. Malformed Wayback citations in `notes/hei-interlocks.md` (~lines 92,
97, 103, 106).** The Wayback URLs are written scheme-less
("web.archive.org/web/2008…/http://www.lurf.org/docs/exec.pdf"), so link
extraction and markdown autolinking pick up only the embedded *original*
lurf.org URL — which is 404 live. The Wayback captures themselves were
verified available. *Fix: prepend `https://` to the archive URLs.*

**C3. BLOCKED (bot walls — cannot be verified from a script; check in a
browser): capitol.hawaii.gov** — uniform Cloudflare 403 for all 10 live URLs
tested. Most load-bearing capitol citations are Wayback copies (fine), but
live-capitol URLs are relied on in `pre2011-solar-bills.md` (4),
`state-land-solar.md` (4), `wind-setbacks.md` (~8, incl. HB 2188
text/testimony), and `data/wind_setback_bills.csv`. Also blocked:
codelibrary.amlegal.com (property-tax-wedge.md:11), legiscan.com
(pre2011_bills.csv), ksbe.edu (sup_census.csv), nextracker.com (429).
*Fix where load-bearing: add Wayback captures for the live-capitol citations
(a capture of HB2188_.HTM was confirmed to exist).*

**C4. Unstable citation form:** `acts-2014-2022.md:22` cites the SB631 CD1
text via a `web/*/` Wayback *calendar* wildcard rather than a dated snapshot;
direct snapshots exist (e.g., 20201020164428). *Fix: cite a dated snapshot.*

**C5. Missing URL:** the Act 278 (2019) DBEDT/OP study — cited in CLAUDE.md
and cached as `cache/act278.pdf` — has **no URL anywhere in notes/ or the
CSVs**. *Fix: add the files.hawaii.gov/dbedt/op/lud/ URL where it is cited.*

**All other sampled links resolved correctly (OK 200), including:** every
sampled Wayback URL served the *exact* requested snapshot (no silent
redirects); hicscdata.hawaii.gov API; the RPAD/OWNALL ArcGIS endpoint
(oahu-ownership.md:13); realproperty.honolulu.gov; Star-Advertiser 2021 tax
story; hnldoc.ehawaii.gov measure pages and document downloads (Ord 25-2
record, Hurley testimony, Res 19-305); files.amlegal.com ORD25-002.pdf
(281 pp); Civil Beat and wind-watch stories; archive.org SLH 1980 scan;
files.hawaii.gov and luc.hawaii.gov docket PDFs from sup_census.csv;
Nevados/ARRAY vendor pages; NY DPS doc server (GET only).

**Content verification (10 deep checks — all SUPPORT the citing text):**
1. SB631 CD1 Wayback snapshot: 10%/20-acre "whichever is lesser" present,
   "special use permit" absent — exactly the note's Act 217 claim.
2. SSCR2607 Wayback: is the Senate AGL/ENE committee report on SB 2775 SD1.
3. SLH 2005 Act 205 PDF: HB 109, amends §205-2 — matches the note's
   "context, not a solar bill".
4. SB 942 (2021) introduced PDF: contains the Board-of-Agriculture
   "letter of attestation" PPA-chokepoint language.
5. HRS §205-4.5 Wayback (2025-03-11): (a)(20) cap text verbatim as quoted.
6. ORD25-002.pdf: enrolled Bill 64 (2023) CD2 FD2 LUO overhaul with the
   tiered wind-setback provisions.
7. NREL 83586.pdf (via Wayback): Q1-2022 benchmark; contains the exact
   "additional land grading" phrase quoted in the note.
8. Nevados datasheet: "37% max N–S and E–W slope", ±26% articulation —
   matches the note.
9. LUC SP15-405 D&O (2017-08-14): LUC order bearing docket number, Waipiʻo,
   2017 dates (scanned; OCR-limited but consistent with the CSV row).
10. DBEDT/OP Food Security Strategy PDF: title and 85–90%-imported figure as
    cited (the note's "Oct 2012" date not visible in extracted text).

---

## D. Claims lacking any repository source

**D1. Table 3 and the §3 "exposed set" bullets have no notes documentation.**
The numbers are correct — this audit reproduced every cell exactly from
`data/oahu_land_transmission.csv` × `data/oahu_ag_owners.csv` — but no notes
file or analysis script documents the cross-tab, the 49/43/26 parcel counts,
or the owner-scale definitions (major >5,000 ac etc.). A reader cannot find
the derivation anywhere. *Fix: add the cross-tab and definitions to
`notes/oahu-ownership.md` (or commit the generating script).*

**D2. Table 5 transmission unit costs (MISO) have no source anywhere in the
repo.** The paper cites "MISO transmission cost estimation guides (MTEP24/25)"
and §12 repeats it, but no notes file, script, or cached document contains the
MISO guide URL, title, or the extracted base values ($0.6–2.5M/km 46–69 kV,
$1.5–4M/km 138 kV, $10–30M substations, transfer capacities). Only the Hawaiʻi
multiplier is tagged U — the mainland base numbers are presented as sourced
but are untraceable. Downstream dependents: Fig. 5 cost gridlines, the
$30–75k/MW spur arithmetic, the "3–5× the power for modestly more cost" claim,
and the entire Table 6 $500M program allocation. *Fix: add a notes file with
the MISO TCEG citation/URL and the specific table values used, or tag all of
Table 5 U.*

**D3. §1 bullet "Zoning": "The Honolulu LUO permits solar in AG districts
subject to ordinary development standards; solar faces no county setback
regime comparable to wind's."** No notes file documents the LUO's solar
treatment; `notes/oahu-nonag-solar.md` explicitly lists it as an open
follow-up ("Honolulu LUO treats utility-scale solar differently across county
zones — a follow-up if this becomes load-bearing"). It is now load-bearing.
*Fix: pull the Ord. 25-2 solar-facility standards (the ordinance PDF is
already cached in `data/raw/ord25-44.pdf` / amlegal) and note them.*

**D4. §4: the "5–6 GW decarbonization build" scale (and hence "~30,000 acres
… needed at current densities").** The acreage arithmetic is transparent
(5–6 GW × 5 ac/MW), but the 5–6 GW Oʻahu requirement itself is asserted
without a source anywhere in the repo. *Fix: cite the source (e.g., a HECO
IGP/RESOLVE scenario or UHERO estimate) or tag U.*

**D5. §1 bullet "Procurement": "In practice land is optioned and permits filed
after an award."** Directionally consistent with the SUP census (award dates
precede filings for the projects there), but stated as a general practice with
no documented source. Minor. *Fix: attribute to the census pattern.*

---

## E. Notes-internal flags encountered (not paper errors, for awareness)

- `notes/cap-quantification.md` states both "the 20-ac hard cap binds on only
  **85 Oahu parcels**" and "Those **176 parcels** above 200 ac capture 88.6%
  of the S0→S3 gain" in adjacent sentences, while `notes/oahu-ownership.md`
  (and the paper) use **118** parcels (>200 ac with any B/C). Three different
  denominators for adjacent concepts; the note never reconciles them.
- `notes/sb631-2011.md` refers to the 2008 act as "Act 231" (from DOA
  testimony) with a TO-VERIFY flag; `notes/pre2011-solar-bills.md`
  subsequently verified it as **Act 31 (HB 2502)** — the paper correctly uses
  Act 31, but the sb631 note was never updated.
- `notes/oahu-transmission-screen.md`'s corridor table row for C04 says PRI
  33% vs the CSV's 32% (see B6).
