# Accuracy Review — cross-file consistency & verification audit

Review date: 2026-07-17. Reviewer: Claude (adversarial internal-consistency
audit; **no source files, notes, CSVs, or paper were edited** — this document
is the only output). Scope: propagation of the late "surgical" paper
corrections into `notes/`, `docs/`, and `data/`; internal contradictions
between files; README/docs-vs-reality checks; consolidation of every
self-flagged verification item.

**Headline:** the surgical corrections **did propagate**. Both paper HTML files
and every substantive note carry the corrected ag-district figures. The old
(wrong) numbers now survive **only inside the two prior audit documents**
(`docs/AUDIT_SOURCES.md`, `docs/AUDIT_REPRO.md`), which were written *before*
the corrections and now describe an already-fixed paper. That inversion — audit
docs stale relative to the artifact they audit — is the main thing to fix.

---

## A. Stale-number propagation — status (highest priority)

**Result: no stale ag-district numbers in notes or data CSVs.** The searched
old values (276,000 / 47% / 16,031 / 40,812 / 219,163) appear in prose in only
two places, neither a propagation failure:

- **A1. `docs/AUDIT_SOURCES.md:104–122` — the old numbers persist here, but as
  *quoted paper errors that are now fixed*.** This file (dated 2026-07-12)
  flags "276,000 acres … 47%" (§B1) and Table 1 "A 16,031; B/C 40,812; D/E
  219,163" (§B2) as live paper defects and recommends the fix to
  120,789 / ~32% and 15,106 / 34,877 / 65,076. The paper subsequently adopted
  exactly those fixes (see §E), so the audit doc now misrepresents the current
  paper. **Not a data error, but for a public reference it reads as if the
  paper still carries the error.** Recommend adding a resolved/superseded
  banner or moving it to an `archive/` note.

- **A2. `notes/cap-quantification.md:59` — "| A | 16,023 | 16,031 |" is
  legitimate, not stale.** It sits in the "Sanity check vs Office of Planning
  2011 LSB figures" table (lines 53–66), explicitly labeled as the *island-wide
  OP-2011 LSB total* against which the analysis's full-coverage LSB count is
  validated. The in-district totals in the same file (lines 77–84:
  A 15,106 / B/C 34,877 / D/E 65,076; district 120,789 ac) are the corrected
  values and match the paper. **Clean — do not touch.**

**Confirmed-correct propagation (spot-checked):**
- `paper/land-restrictions-paper.html:114` and `…-final.html`: "120,800 acres
  of Oʻahu (roughly 32% …; statewide … ~47%)". ✓
- Paper Table 1 (`…-paper.html:124–126`): A 15,106 / B/C 34,877 / D/E 65,076. ✓
- `notes/oahu-nonag-solar.md:47`: ag-district reference row = **120,789 ac**. ✓
- `docs/ASSUMPTIONS.md`, `docs/METHODS.md`, `docs/NOTES_INDEX.md`: contain **no**
  ag-district-total framing at all — nothing to go stale. ✓
- Downstream in-district GIS results (S0 3,601 / S3 15,657; distance bands;
  slope; wind) were computed in-district and are internally consistent — not
  affected, per the task scoping. ✓

---

## B. Internal contradictions

- **B1. C04 "Property Reserve" share: note says 33%, CSV & paper say 32%.**
  `notes/oahu-transmission-screen.md:206` (C04 row) reads "Property Reserve
  (LDS) 33%"; `data/gis/oahu_corridor_candidates.csv:5` has **32%**, and the
  corrected paper Table 4 uses 32%. The acreage in the note (5,618) is already
  correct — only the ownership % lags. (Flagged in AUDIT_SOURCES §B6/§E.)

- **B2. Cap-bound parcel count: three different denominators, never
  reconciled.** `notes/cap-quantification.md:109–111` states the 20-ac cap
  binds on "**85 Oahu parcels**" and, one sentence later, "Those **176
  parcels** above 200 ac"; `notes/oahu-ownership.md` and the paper use
  "**118** parcels" (>200 ac with any B/C). Adjacent concepts, three numbers,
  no reconciliation in the note. (Flagged in AUDIT_SOURCES §E.)

- **B3. 2008 act number: "Act 231" vs "Act 31".** `notes/sb631-2011.md:142`
  refers to the 2008 D/E-opening act as "Act 231" with a "TO VERIFY" flag;
  `notes/pre2011-solar-bills.md` establishes it as **Act 31 (HB 2502)**, which
  the paper uses. The sb631 note was never back-corrected.

- **B4. `docs/AUDIT_SOURCES.md` contradicts the current paper throughout.**
  §§B1, B2, B3, B5, B6, B7, B8 are all described as unfixed paper errors; every
  one has since been corrected in `paper/land-restrictions-paper.html` and
  `…-final.html` (§E). The audit doc is internally fine but externally stale.

- **B5. `docs/AUDIT_REPRO.md:17` md5 is stale.** It certifies
  `land-restrictions-paper-final.html` as byte-identical with md5
  `70543cd1…`. The file on disk today is md5 **`b84f5230…`** — it was
  regenerated after the surgical corrections. The "byte-identical on re-run"
  verdict (lines 12–17, 95–99) predates those corrections and no longer holds
  for the final HTML/PDF.

---

## C. README / docs vs. reality

**Verified TRUE (no discrepancy):**
- **C1. `data/raw/dockets/lobbyist_registrations.csv` exists** (597 KB). ✓
  (README data-source table + DATA_DICTIONARY:313.)
- **C2. RPAD "taxyr 2027" is correct for OWNALL.** Raw
  `data/raw/rpad/ownall_oahu_ag_rows.csv` is predominantly **taxyr 2027**
  (19,762 of ~21,700 rows; scattered 2020–2029 tails). DATA_DICTIONARY:214,
  ASSUMPTIONS F1, `oahu_ag_owners.csv` source_url, and `resolve_owners.py:8`
  all say 2027 — consistent. ASMTGIS (the *vacancy* proxy, a different table)
  is consistently labeled taxyr **2026** in METHODS:149, ASSUMPTIONS G1,
  `notes/oahu-nonag-solar.md:27`. The two vintages are correctly distinguished.
- **C3. Reproduction script list matches actual filenames + args.** Every
  script named in README's quick-start exists in `analysis/`. The one CLI with
  arguments, `cap_scenarios.py`, takes `analyze [oahu|statewide]`
  (`cap_scenarios.py:33–34, 336–337`) — README's `analyze statewide` is
  correct. `nonag_classify.py`/`nonag_fig.py` are listed (README:130).
- **C4. All 31 documented row counts match** (`wc -l` minus header) — verified
  for a 20-CSV sample spanning `data/` and `data/gis/`:
  bills 12, pre2011_bills 13, sup_census 16, hei_board_interlocks 37,
  legal_edges 37, wind_setback_bills 12, campaign_contributions_siting 730,
  campaign_contrib_summary 59, cap_scenarios_by_parcel 115,856,
  cap_scenarios_results 35, oahu_land_transmission 6,274, oahu_ag_owners 6,239,
  oahu_owner_class_transmission 6,274, oahu_parcel_slope 6,274,
  oahu_nonag_solar_candidates 827; gis: lsb_sanity_totals 6,
  lsb_in_ag_district_totals 6, scenario_by_size_decile 10, oahu_class_by_band
  10, oahu_corridor_candidates 16, wind_viable_areas 10, wind_setback_oahu 2,
  nonag_top_parcels 20, expansion_curve 154, oahu_unlock_clusters 13. **All
  exact.**
- **C5. Named cache dirs exist:** `data/raw/{capitol,csc,dockets,edgar,lurf,
  rpad,wind-setbacks}` all present; `data/gis/` layers present.

**Discrepancies / caveats to surface:**
- **C6. "Re-run offline from cache" overstates reproducibility.** README:140–144
  says scripts are resume-safe and re-run offline from `data/gis/` cache. Per
  `docs/AUDIT_REPRO.md:30–59, 79–105`, four scripts (`nonag_classify.py`,
  `nonag_fig.py`, `fetch_ownall.py`, `resolve_owners.py`) read from an
  **ephemeral `/private/tmp/claude-503/…/scratchpad/`** that will vanish on tmp
  purge, and steps 1–7 of the non-ag screen + the owner×transmission join have
  no committed producer. The non-ag CSV, `oahu_owner_class_transmission.csv`,
  and the ownership build are therefore **not** end-to-end reproducible. This
  is honestly documented in AUDIT_REPRO and DATA_DICTIONARY, but the README
  quick-start does not carry the caveat.
- **C7. AUDIT_REPRO §5's "README claims transmission_screen/slope_screen fetch
  on first run" no longer applies** — the current README makes no such claim
  (it says re-download recipes live in METHODS.md). That AUDIT_REPRO finding
  appears to have been addressed by a README rewrite; worth reconciling the two
  docs.

---

## D. Consolidated UNVERIFIED / needs-verification list

Self-flagged in the notes (compiled verbatim from `UNVERIFIED`/`PLAUSIBLE`/
`Tier-3`/`TO VERIFY` tags) plus items surfaced by prior audits. These are the
honest verification-needed items to expose in a public reference.

**Load-bearing for the paper (verify or tag before public use):**
1. **80% renewable property-tax exemption / Bill 39 (2021).**
   `notes/property-tax-wedge.md:3,23,26,47` self-flag ordinance number/status
   as UNVERIFIED. Paper hedges once ("reported as 80%", `…-paper.html:136`) but
   Table 8 (line 655) states "80% renewable exemption" flatly. Verify ROH §8-10
   amendment or tag.
2. **MISO transmission unit costs (Table 5).** No source anywhere in the repo
   (AUDIT_SOURCES §D2); `notes/oahu-bulk-delivery.md:230` flags the Hawaii
   multiplier UNVERIFIED but the mainland base values ($/km, substation $,
   transfer capacities) are untraceable. Feeds Fig. 5, the $30–75k/MW spur
   math, and Table 6's $500M allocation.
3. **5–6 GW Oʻahu decarbonization build (§4).** Asserted without a source
   (AUDIT_SOURCES §D4); underlies the "~30,000 acres needed" figure.
4. **~155 MW existing wind (§9).** Na Pua Makani component is nameplate
   *potential* (~55 MW) per `notes/wind-setbacks.md`; installed is commonly
   ~24–27 MW, implying a ~125 MW fleet (AUDIT_SOURCES §B10).
5. **Table 3 / "exposed set" cross-tab (§3).** Numbers reproduce from the CSVs
   but no note or script documents the 49/43/26 parcel split or the owner-scale
   thresholds (AUDIT_SOURCES §D1).
6. **HB 778 (2025) characterization** — "state-lands renewable study" vs the
   note's "integrated ag-district land-use study" (AUDIT_SOURCES §B9;
   `notes/state-land-solar.md`).

**Legislative / documentary (notes self-flag):**
7. Wind's 1980 permitted-use origin (Act 24 / HB 2418-80) sponsors & testimony:
   PLAUSIBLE BUT UNDOCUMENTED until the paper 1980 House/Senate Journals are
   pulled (`notes/wind-statutory-entry.md:207`); HEI/Kahuku-wind role unverified.
8. Pre-2011 failed-bill details: numerous UNVERIFIED act-number mappings and
   unpulled testimony (`notes/pre2011-solar-bills.md:33,38,159,161,164,171,
   203–216`).
9. State-land solar thread: many UNVERIFIED items — Act 19 bill no.,
   HB 2188/SB 957 details, IAL designations, several project statuses, and a
   "Tier-3/possibly confabulated" flag at `notes/state-land-solar.md:251`
   (also :70,79,94,118,136,156,201,217,236,240,245,272,304,308,350,352,366,
   378,435).
10. HEI board/trust interlocks: several term-date and overlap flags UNVERIFIED
    (`notes/hei-interlocks.md:37,78,134,155`) — the CLAUDE.md Tier-3 interlock
    hypothesis is only partially resolved.
11. Sierra Club / food-security personnel and founding-year details UNVERIFIED
    (`notes/sierra-club-food-security.md:27,53,58,178,185,190,193,206`).
12. Slope-cost literature: Tier-3 single-source premiums and the Korea
    slope-tightening claim UNVERIFIED (`notes/slope-cost-literature.md:165,171,
    176,187,351`).
13. Wind-setback specifics: former section numbers and neighbor-island 1:1
    rules UNVERIFIED (`notes/wind-setbacks.md:54,63,182,187,223`).
14. SUP census: soil-class basis of the neighbor-island "county-only" projects,
    and several "dogs that didn't bark" landowner/mechanism cells UNVERIFIED
    (`notes/sup-census.md:159,179,181,184`).
15. Legal-representation map: firm attributions and 2021+ lobbyist-registry
    (JS-portal) checks UNVERIFIED (`notes/legal-representation-map.md:62,188`).
16. Bulk-delivery inferences: unmapped 46 kV MVA and North Shore curtailment
    causation flagged inference/UNVERIFIED (`notes/oahu-bulk-delivery.md:73,92`).

**Dead/blocked links (from AUDIT_SOURCES §C, still open):** all nrel.gov cites
(DNS-dead at audit; Wayback rescues listed), scheme-less Wayback URLs in
`notes/hei-interlocks.md`, Cloudflare-blocked live capitol.hawaii.gov cites,
and the missing Act 278 study URL.

---

## E. Verified clean (confirmations)

- **Paper corrections fully propagated to BOTH HTML files** (`…-paper.html` and
  `…-paper-final.html`, md5 b84f5230): ag district 120,800 / 32%; Table 1
  15,106 / 34,877 / 65,076; abstract "about 42,800 acres"; HARC "Kunia research
  station" (not "230-acre Mililani"); "Kahuku hills (~4,100 ac, majority steep)
  and Kawailoa/Pūpūkea (~4,000 ac, mostly ≤30% slope)"; C04 corridor at
  5,618 ac. All old values absent from both files.
- **Class-A SUP claim is consistent with the record.** The paper no longer
  asserts an absolute bar; `data/sup_census.csv` and `notes/sup-census.md:38`
  correctly document **SP15-406 (Kawailoa Solar, 2015, KS land)** as a granted
  SUP spanning class A/B/C/E. No note asserts "no class-A solar SUP ever."
- **Notes carry the corrected in-district totals** (`cap-quantification.md:77–84`,
  `oahu-nonag-solar.md:47`); the only island-wide LSB figures present are
  explicitly labeled OP-2011 sanity checks.
- **Cross-checked headline numbers agree** across paper ↔ note ↔ CSV: cap
  scenarios S0 3,601 / S3 15,657 (`cap-quantification.md`,
  `cap_scenarios_results.csv`); SUP census 8 dockets / 7 approved / 0
  intervenors (`sup-census.md`, `sup_census.csv`); wind 39,386 / 36.3% of
  108,417 and 26,023 ≤30% slope; non-ag 11,319 ≤15% and ~5,660 durable;
  near-grid D/E 6,083 (≤15%) / 11,110 (≤30%); ownership government 50.1% /
  KS 12.8%.
- **All 31 documented CSV row counts exact; all named cache dirs and the
  lobbyist CSV exist; RPAD taxyr 2027 and ASMTGIS taxyr 2026 correctly
  distinguished; cap_scenarios.py CLI matches README.**

---

*Method note: old-number search via `rg` over `notes/`, `docs/`, `data/`,
`paper/`; row counts via `wc -l`; RPAD vintage from the raw OWNALL dump; md5
via `md5 -q`. The two prior audits (`AUDIT_SOURCES.md`, `AUDIT_REPRO.md`,
both 2026-07-12) were treated as inputs, not ground truth — several of their
findings have since been fixed in the paper and are marked resolved above.*

---

## F. Resolution log (2026-07-17)

Fixes applied in the repositioning-to-living-reference pass:

- **B1 (C04 33%→32%)** — fixed in `notes/oahu-transmission-screen.md`.
- **B2 (85/176/118 parcel counts)** — reconciled in `notes/cap-quantification.md`:
  85 = parcels where the 20-ac cap actively binds; 176 = all Oahu parcels
  >200 ac; 118 = those with B/C soil (paper's count). Recomputed from
  `cap_scenarios_by_parcel.csv`; the 88.6% gain share holds for all three groupings.
- **B3 (Act 231→Act 31)** — corrected in `notes/sb631-2011.md`; "Act 231"
  identified as an OCR artifact; cross-referenced to `pre2011-solar-bills.md`.
- **B4/A1 (AUDIT_SOURCES stale)** — superseded banner added to `docs/AUDIT_SOURCES.md`.
- **B5 (AUDIT_REPRO stale md5 + scratchpad)** — banner added to `docs/AUDIT_REPRO.md`;
  the scratchpad-dependency finding is now RESOLVED (scripts repointed to
  committed `data/intermediates/`; verified via system rebuild after the tmp
  scratchpad was purged).
- **C6 (README repro overstatement)** — reproducibility caveat added to `README.md`.
- **Paper wind fleet** — "~155 MW" corrected to **~127 MW** (Kahuku 30 + Na Pua
  Makani 27.6 + Kawailoa 69; computed from `osm_wind_turbines_oahu.csv`);
  `notes/wind-setbacks.md` "Na Pua Makani ~55 MW" corrected to 27.6 MW.
- **Paper Table 80% exemption** — softened to "partial (reported ~80%),
  ordinance text unverified," consistent with the §5 hedge and the note flag.
- Paper reassembled and PDF regenerated after the two content edits.

**Still open (needs external verification — surfaced, not resolved):**

- Bill 39 (2021) exact renewable-exemption percentage and ROH section (tagged
  in paper + note, not yet confirmed against ordinance text).
- MISO per-km base cost values (the MTEP guides are now cited; the specific
  values remain "planning-typical," inherently approximate).
- 1980 wind act (HB 2418-80) sponsors/testimony — paper archives only.
- The broader legislative/documentary UNVERIFIED items catalogued in §D
  (7–16), which are the standing research to-do list for this living reference.
