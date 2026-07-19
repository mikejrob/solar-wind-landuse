> **Snapshot note:** grid-thread work lives in the `oahu-grid` repository; this is a periodic copy kept here because the paper's transmission section cites it, and it may lag the live version.

# Oahu Transmission Network — What the Public Record Reveals

Research note for the solar/wind land-use project. Question: what do public and
ancillary documents disclose about Oahu's actual transmission system — voltages,
circuit routes, thermal/transfer limits, and planned upgrades — especially the
north/central-to-south corridors — given that HECO treats current ratings as
confidential?

**Evidentiary discipline:** every fact below carries a source + page/line
locator. Vintage is flagged because a 2011 rating may be superseded. Where a
number is inferred rather than stated, it is marked [INFERENCE]. Where a doc was
not obtained, it is marked [UNVERIFIED — not pulled].

Cached PDFs live in `data/raw/grid/` (filenames given per source).

---

## Headline structural facts (high confidence, multiple sources)

- **138 kV is the maximum operating voltage on Oahu today.** Every line in
  HECO's 2022 FERC Form 1 transmission inventory operates and is designed at
  138 kV; the sub-transmission tier is 46 kV; distribution is 12/4 kV. No 230 kV
  or 345 kV exists in service. (FERC Form 1 2022; HECO Power Delivery fact
  sheet.) **230 kV and 345 kV appear only as study proposals**, never built
  (OWITS 2011 proposed 230 kV *undersea AC cable*; 2021 REZ study proposed a
  *345 kV* Kahe–Wahiawa–Waiau loop — see below).
- **Two primary 138 kV corridors, both anchored at Kahe (west):** a **Northern
  Corridor** (Kahe → Halawa → Koolau → Pukele) and a **Southern Corridor**
  (Kahe → Waiau → Iwilei / School Street / Archer, extended to Kamoku). The two
  are tied together in West Oahu; historically NOT closed on the east side (the
  never-built Kamoku–Pukele "East Oahu" line was the missing link). (PUC D&O
  23747, 2004; HECO Power Delivery fact sheet.)
- **North Shore / central-north Oahu has NO 138 kV.** It is served only by
  46 kV sub-transmission radiating from Wahiawa and Koolau substations, and those
  46 kV feeders are "already at their capacity limits." This is the core
  transmission constraint on moving north-shore renewables south. (HECO PSIP
  2014, p.5-42/K-3; 2021 REZ study; 2023 IGP.)

---

## Source family 1 — NREL / GE integration studies (2009–2014)

### 1a. Oahu Grid Study: Validation of Grid Models (HNEI + GE, Sept 2009)
File: `hnei_oahu_grid_study_validation.pdf`. DOE Award DE-FC26-06NT42847.
- Built and validated the **GE MAPS™ (production cost) and GE PSLF™ (dynamic
  stability) models of the entire Oahu system**, calibrated against 2007 HECO
  historical generation/fuel data via a HECO Technical Review Committee. This is
  the ancestor model reused by every later GE/HNEI Oahu study. (p.1–7.)
- Does **not** publish a bus/branch table or one-line; it documents model
  fidelity. Value: establishes that a full validated
  Oahu network model exists and has been shared HNEI↔GE↔HECO since 2009.

### 1b. Oahu Wind Integration Study — final report (HNEI/HECO/GE, Feb 2011)
File: `owis_final_2011.pdf` (hawaiianelectric.com DOE version).
- System baseline (2014 planning case): **total generating capacity 1,756 MW**;
  daytime min load studied down to ~600 MW. (Exec summary, lines 100–103.)
- Studied 400 MW off-island wind (Lanai/Molokai via HVDC) + 100 MW Oahu wind +
  100 MW Oahu solar to reach 25% renewable.
- **North Shore wind interconnects at 46 kV:** the "100 MW Oahu wind" = two
  50 MW plants, modeled on the **Waialua–Kahuku 46 kV circuit (Wahiawa–Waialua
  46 kV circuit #2)** and the **Wahiawa–Wailua #1 46 kV feeder**. (lines
  3737–3750.) Confirms Wahiawa as the 138/46 kV gateway for north-shore wind.
- Down-reserve requirement raised to **90 MW for loss of a 138 kV line** event.
  (line 7193.) Reserve/dynamic study, not a thermal rating.
- The bus model references named 138 kV buses (Iwilei bus 130, Koolau bus 150,
  Kahe AB bus 140). (lines 3624–3709.) Bus numbers are handles into the PSLF
  model, not public ratings.

### 1c. OWITS — Oahu Wind Integration & Transmission Study (NREL/Electranix, Feb 2011)
Files: `owits_energy_hawaii_2011-02.pdf` = `owits_summary...` (NREL/SR-5500-50411).
- This is the **undersea-cable / inter-island** study. Key public numbers:
  - Proposed **AC cable rating 230 kV, 250 MW max, 3-core XLPE** (~4.8 MVAR/mile
    charging). (line 2102.) This is the only place 230 kV appears — a *proposed*
    submarine AC option, never built.
  - **Max single (N-1) contingency the Oahu system was rated to absorb = 200 MW**
    (loss of one HVDC pole / cable). Cable + converter ratings were explicitly
    sized so N-1 stays ≤200 MW. (lines 302, 616, 2085, 2799.)
  - HVDC landing options: north-shore/windward option lands at MCBH with **two
    138 kV circuits to Koolau + a third 138 kV circuit to Pukele**; south-shore
    option lands at Honolulu Harbor with **one 138 kV circuit each to Iwilei,
    Archer, and Kamoku**. (lines 3900–3903.) Corroborates the named 138 kV
    substation set.
- Vintage caveat: 200 MW N-1 limit is a 2011 figure tied to then-current system
  strength/inertia; superseded as generation mix changed.

### 1d. Hawaii Solar Integration Study — Oahu final technical report (GE/HNEI, 2012–13)
File: `hsis_oahu_final.pdf` (NREL fy13osti/56311 = summary; HNEI hosts full).
- Continues the GE PSLF/MAPS Oahu model. Covers reserves, thermal-unit
  minimums, PV ramp — **not** a transmission-ratings document. Named plant buses
  (Kahe, Waiau) and 46 kV distribution circuits (Kahe–Standard Oil #2,
  Koolau–Kailua) modeled. (lines 3292–3722.) Useful mainly to confirm the
  network model's continuity, not to extract line ratings.

### 1e. Stage 2 Oahu–Maui Interconnection Study (GE/HNEI, May 2013) and
"Interconnection of Grid Systems for Maui and Oahu Counties" (GE/HNEI, Feb 2014)
File: `hnei_interconnection_maui_oahu.pdf`.
- Explicitly reuses the **GE MAPS Oahu production model from OWITS** as the
  starting database, merged with Maui. (lines 800–810.) Full security-constrained
  economic dispatch model but transmission *outage contingencies were out of
  scope* — so it optimizes dispatch on the network but does not publish thermal
  limits. Detailed curtailment-by-scenario tables (source of curtailment framing).

---

## Source family 2 — HECO PSIP / IGP public filings

### 2a. HECO PSIP (Aug 2014 draft, docket 2011-0206 → consolidated 2014-0183)
File: `heco_psip_2014.pdf`. **Best single public inventory of the Oahu grid.**
- **System-size baseline, end-2013 (p.4-2, lines ~2917–2922):**
  - 1,298 MW utility generation + 457 MW firm IPP + 110 MW variable IPP.
  - **215 circuit-miles overhead 138 kV + 8 miles underground 138 kV.**
  - **537 circuit-miles of 46 kV sub-transmission.**
  - **21 transmission substations, 131 distribution substations.**
- HECO uses **Siemens PSS/E** for transmission planning (note: GE studies used
  PSLF; HECO's in-house tool is PSS/E). (line 12628.)
- Planning criterion stated: no transmission component may exceed emergency
  rating with one unit on overhaul + one line out for maintenance + loss of a
  second line (an **N-1-1 / effectively N-2 emergency criterion**). (echoed in
  D&O 23747 below and IGP.)
- **THE north→south upgrade, first public proposal — "138 kV Transmission Loop"
  (Appendix K, lines 28469–28480):** a new **138 kV line from Koolau Substation
  to Wahiawa Substation** along the windward/north/central rim, **~55 miles**,
  requiring **≥1 new transmission substation** (ultimate design: six 138 kV
  breakers breaker-and-a-half, two 138–46 kV 80 MVA transformers, 46 kV ring bus,
  four 46 kV feeder breakers). Rationale: existing **46 kV feeders from Wahiawa
  and Koolau serving North Shore/Kahuku are already at capacity**; the loop adds
  46 kV headroom and reliability. **No cost estimate given in this draft.**
- Generation-station 138 kV bay/line detail (existing-site analysis,
  lines 10028–10071):
  - **Kahe Generating Station: six 138 kV transmission lines**, able to
    accommodate ≥650 MW of generation "as it does now."
  - **Waiau: six breaker-and-a-half 138 kV bays; eight 138 kV lines + six
    generators (Units 5–10) — all bays fully used.** Plus a separate 46 kV
    substation (Units 3–4). ~100 MW could connect at 46 kV after Units 3&4
    retire (end-2016).
  - **AES/CIP Substation: three 138 kV breaker-and-a-half bays, room for 2–3
    more; three lines + three generators (CIP CT-1, AES, HPower) — bays full.**
    +100 MW would not trigger a new 138 kV line out of AES.

### 2b. Grid Modernization Strategy (Aug 2017) — [UNVERIFIED — not pulled]
Public PDF exists: hawaiianelectric.com .../final_august_2017_grid_modernization_strategy.pdf.
Trade press (T&D World) notes GEMS/DVC pilots at **three Oahu substations** that
raised solar hosting capacity (e.g., 1→3 MW at one, 10.34→14.3 MW at another).
Distribution-hosting, not transmission ratings. Pull if hosting-capacity detail
is needed.

### 2c. Transmission REZ Study (HECO, Nov 2021) — docket 2018-0165 IGP working group
File: `heco_rez_study_2021.pdf`. **The most detailed public transmission-capacity doc.**
Steady-state power-flow study (HECO planning criteria, normal + N-1 + N-2) of how
much renewable each area can host and what it costs. All Oahu grid-scale REZ
except Group 7 interconnect at **138 kV substations**; Group 7 at 46 kV.
- **Named 138 kV substations used as REZ hosts:** Kahe, Waiau, Halawa, Koolau,
  Wahiawa, Iwilei, Ewa Nui, Hoohana, Makalapa, plus CEIP/AES. Off-shore wind
  interconnection candidates: Kahe, Halawa, Iwilei, Koolau (138 kV). (§5.1, 5.4.)
- **Single Point of Failure limit on Oahu = 135 MW** — the max single injection
  increment used for step-wise costing (cost tables use 135 MW steps). (§5.4.8.)
  This is a concrete, publicly stated planning limit.
- **REZ Group 8 = Wahiawa / North Shore, >1 GW potential (1,160–1,166 MW)** — the
  binding constraint. Wahiawa today is "a non-major-load-center substation with
  only **one BAAH bay** and 2 line connections"; hosting Group 8 requires
  rebuilding it to **6 BAAH bays / 11 line connections**. (§5.3–5.4.3.)
- **Interconnecting REZ Groups 1–7 (West/Central/East/SE) requires NO existing
  138 kV line upgrades** — only local "REZ enablement." Only **Group 8 (north
  shore) + off-shore wind** trigger network expansion. (§5.4.1, exec summary.)
- **Three studied north→south network-expansion options (to export Wahiawa/N.
  Shore power):**
  - **Option 1 — new 138 kV Kahe–Wahiawa line:** three new circuits (1950 AAC) +
    reconductor/new Wahiawa–Waiau circuits (double-bundled 795 AAC). **$1,281.5 M.**
  - **Option 2 — reconductor + add 138 kV circuits** (Kahe–Akau–Hema–Wahiawa,
    Wahiawa–Kahe, Wahiawa–Waiau, Waiau–Makalapa). **$1,258.8 M.**
  - **Option 3 — new 345 kV loop Kahe–Wahiawa–Waiau** (the only 345 kV proposal
    on record): three 138/345 kV transformers (Kahe & Wahiawa 450/600 MVA
    cont/emerg; Waiau 600/700 MVA), 345 kV lines double-bundled 795 AAC, 2 new
    345 kV BAAH bays per station. Eliminates all 138 kV line upgrades for REZ 1–8.
    **$1,215.0 M.** Report warns 345 kV is "unchartered territory for the
    Company." (§5.4.4, Table 5-4, 5-14.)
- **Off-shore wind:** 600 MW feasible **only at Koolau 138 kV** (Kahe/Halawa/
  Iwilei interconnection found infeasible due to Hoohana/Makalapa/space limits).
  600 MW @ Koolau adds **$583.5 M** (Option 1). 400 MW @ Koolau needs no network
  expansion beyond REZ 1–8: **$50.6 M**. (§5.4.5, Tables 5-15/5-16.)
- **Existing named 138 kV lines disclosed (appendix upgrade tables):**
  Kahe–Wahiawa, Wahiawa–Waiau, Makalapa–Waiau #1/#2, Halawa–Makalapa,
  Halawa–Iwilei, Halawa–School, Halawa–Koolau, Koolau–Waiau #1/#2,
  Kahe–Akau–Hema–Wahiawa. (Tables 10-1 to 10-4.) These corroborate the FERC
  Form 1 line list.
- Per-MW REZ enablement costs (indicative): Group 1 $0.21 M/MW … north-shore
  Group 8 $1.25–1.26 M/MW. (Table 5-8.) Costs in 2025 dollars.
- Companion public workshop deck: `heco_rez_workshop_10175.pdf` (hawaiianelectric.com/a/10175)
  gives per-group targets and host substations (Wahiawa 138 kV 1,160 MW; Kahe
  138 kV 588 MW; Halawa 608 MW; Koolau 147 MW at 138 kV + 66 MW at 46 kV; Ewa Nui
  324 MW; Hoohana 120 MW).

### 2d. July 2022 Oahu Near-Term Grid Needs Assessment (IGP)
File: `heco_oahu_near_term_grid_needs_2022.pdf` (hawaiianelectric.com/a/11166), 152 pp.
- Near-term reliability framing: need 300–500 MW new firm renewable by 2029 +
  200 MW by 2033, enabling deactivation of up to 930 MW fossil. Reuses the REZ
  study's Oahu REZ groups (Fig 7). Transmission ratings not re-published; cross-
  references the 2021 REZ study for network-expansion needs.

### 2e. IGP Report — final (2023, docket 2018-0165)
File: `heco_igp_report_2023.pdf` (hawaiipowered.com), ~250 pp.
- Confirms 2021 REZ findings: **full north-shore REZ (Zone 8) overloads the
  138 kV lines at Wahiawa; mitigated by cutting Wahiawa interconnection by
  220 MW.** (lines 11969–11970.) A concrete, publicly stated transfer limit
  proxy.
- Urban-core constraint: reducing load at **Kamoku/Kewalo/Archer 138 kV
  substations by 37 MW avoids replacing the Archer–School and Archer–Iwilei
  138 kV underground cables** — i.e., those UG cables are the south-side
  bottleneck. (line ~11960.)
- **Oahu Transmission Capital Costs (Table 8-13), nominal $MM:** REZ Enablement
  2029 $114, 2030 $942, 2040 $799, 2045 $2,241, 2050 $1,112; Base Network
  Expansion 2045 $3,482, 2050 $1,018. One network-expansion line item = **$1,208.9 M**
  (matches REZ-study north-shore option). (lines ~11960, 13129.)
- Named near-term REZ enablement projects w/ cost (Track tables): Wahiawa 3
  138 kV new substation transformer + circuit **$15.0 M** (2026); CEIP 3 46 kV
  reconductor $3.93 M; etc. (lines 12480–12560.)
- REZ maps eventually narrowed (July 8 2026 announcement) to two prioritized
  zones — **Zone 1 Kunia/Schofield and Zone 6 Koolaupoko** — chosen partly
  because they "involve a relatively contained level of transmission upgrades."
  MW targets not published in the announcement. (hawaiianelectric.com press
  release, 2026-07-08.) The heavy-lift Zone 8 (north shore, >1 GW) was NOT
  prioritized — consistent with its ~$1.2 B transmission cost.

---

## Source family 3 — Historical / engineering / interconnection records

### 3a. FERC Form 1 (HECO 2022 Annual Financial Report, filed w/ PUC 2023)
File: `heco_afr_2022_ferc_form1.pdf`, "Transmission Line Statistics" p.422 (PDF
pp.168–171). **The most concrete public circuit inventory.** Lists every
line ≥132 kV individually. All 35 listed segments **operate and are designed at
138 kV**, **31 circuits total**, **158.51 pole-miles on own structures +
42.90 on shared** ≈ 201 route-miles of 138 kV. Named 138 kV segments (From–To):

  Archer–Kewalo #1 (0.54 mi); Waiau–Koolau #1 (13.73); Waiau–Koolau #2 (13.67);
  Waiau–Wahiawa (2.51 + 10.20, 2 entries); Kahe–Hema (8.79); Koolau–Pukele 1
  (6.41); Koolau–Pukele 2 (6.04); Halawa–Kahe 1 (14.07 + 6.34); Kahe–Waiau
  (4.98+2.32 and 11.88, two circuits); Kahe–Halawa 2 (13.06 + 7.82);
  Halawa–Iwilei (6.34); Halawa–School (5.25); Iwilei–School (0.57);
  Halawa–Koolau (9.70); Waiau–Makalapa 1 (4.69); Halawa–Makalapa (4.23);
  Kahe–CEIP #1 (4.27); Makalapa–Airport (1.71); Kalaeloa–AES (0.74);
  AES–CEIP #1 (2.15); School–Archer (1.88); Iwilei–Archer (1.84); AES–HRRV
  (0.18); Waiau–Makalapa 2 (4.95); Airport Sw.Sta.–Airport #1 (0.43);
  CEIP–Ewa Nui (6.78); Kalaeloa–Ewa Nui (2.71+5.77); Waiau–Ewa Nui 2 (7.56);
  Waiau–Ewa Nui 1 (2.06+5.17); Iwilei–Iwilei 1/2-138 (0.03/0.04).

  46 kV sub-transmission totals: **533.50 pole-miles** (458.08 + 56.03 + shared),
  9 group entries.

  NOTE: FERC Form 1 discloses **route/pole miles, conductor, circuit counts, and
  book cost — but NOT thermal ampacity/MVA ratings.** Cost columns here are $0
  (HECO reports transmission plant cost in aggregate elsewhere / redacted per-line).
  Vintage: exactly current (year-end 2022). Older AFRs (2006, 2015, 2017) are on
  puc.hawaii.gov and would give a time series of 138 kV vs 46 kV mileage growth
  — [UNVERIFIED — not pulled].

### 3b. East Oahu Transmission Project — PUC D&O 23747 (docket 03-0417, 2004)
File: `puc_23747_east_oahu.pdf`. Documents corridor topology + the emergency-
rating criterion (all vintage ~2002–2005 load forecasts):
- Defines the two corridors verbatim (see headline facts). Southern Corridor was
  "recently extended to Kamoku via **two 138 kV lines Archer→Kewalo + one 138 kV
  Kewalo→Kamoku**." (lines 922–964.)
- **Koolau/Pukele Overload Situation:** **three 138 kV lines feed Koolau; two
  138 kV lines Koolau→Pukele; together Koolau+Pukele serve ~30% of Oahu load.**
  Criterion: with one Koolau line out for maintenance + loss of a second, the
  **third line exceeds its emergency current-carrying rating at daytime peak**
  (projected 2005/2006). (lines 1015–1330.)
- **Downtown Overload Situation:** **Iwilei + School Street substations fed by
  three 138 kV lines from Halawa & Makalapa; serve ~25% of load; overload
  projected 2024** on loss of two of three. (lines 1330–1450.)
- Confirms the **planning criterion = component must not exceed emergency rating
  with 1 unit on overhaul + 1 line on maintenance + loss of a 2nd line.**
- Windward + East Oahu = **>50% of HECO total load** (justifies redundancy push).

### 3c. Kahuku / Na Pua Makani / Kawailoa interconnection voltages (press + EIS)
- **Kahuku Wind (30 MW, First Wind):** interconnects near the **end of a 46 kV
  HECO line**; the remote 46 kV location is *why* it needed the 15 MW battery
  (that burned Aug 2012). (Star-Advertiser / Civil Beat, Aug 2012.)
- **Kawailoa Wind (69 MW):** "did **not** require a battery because of its
  proximity to one of HECO's main **138 kV** transmission lines." (Civil Beat
  2012.) BUT the EISPN says the collection system ties into the **Kuilima and
  Waialua–Kahuku 46 kV lines** via two 23/46 kV substations — so field
  interconnection is 46 kV even though a 138 kV line is nearby. Treat the "138 kV
  proximity" claim as the reason storage was waived, not the POI voltage.
  [PARTIAL CONFLICT — worth pinning from the PPA/EIS.]
- **Na Pua Makani (~24 MW, AES, energized Aug 2020):** overhead lines along
  Kamehameha Hwy to the grid near Kahuku — 46 kV area. EIS: `files.hawaii.gov/
  dbedt/erp/.../Na-Pua-Makani`. [Voltage not yet pinned — 46 kV [INFERENCE] from
  Kahuku-area context.]
- Takeaway: **all north-shore/Kahuku wind interconnects at 46 kV off Wahiawa/
  Koolau**, corroborating the "no 138 kV north of the central spine" constraint.

### 3d. Koolau–Pukele line-structure replacement (ASCE / 2026 storm repair)
- The Koolau→Pukele 138 kV line over the Koolaus (Moanalua ridge) is repeatedly
  cited as one of "three high-voltage lines delivering power to Windward Oahu,
  Waimanalo, and East Honolulu," with N-1/N-2 redundancy. Feb 2026 storm
  destroyed steel structures; repaired 2026-04-30. (Star-Advertiser 2026-04-30.)
  Confirms 3-line windward feed still current in 2026.

---

## Source family 4 — HSEO / DBEDT / recent RFP interconnection guidance

### 4a. IGP RFP Appendix H — Interconnection Facilities Cost & Schedule (rev. 2025)
File: `igp_rfp_appx_h_interconnection.pdf`. Published bidder guidance = live
snapshot of **which Oahu 138 kV substations have spare termination capacity:**
- Oahu transmission interconnection is **138 kV** (Hawaii Island is 69 kV). Cost
  to add a 138 kV BAAH bay/termination: ~$3.34 M; reuse existing termination
  $0.61 M. (2026 $.)
- **Spare 138 kV terminations by substation (as of 2025):**
  - **Ewa Nui:** 2 terminations available (but new-line routing "difficult").
  - **Kahe 5-8:** 3 terminations available.
  - **Hoohana:** add termination to existing bay.
  - **CEIP:** 1 available (routing difficult).
  - **Koolau:** 1 available (routing "difficult due to permitting").
  - **AES:** 1 available (replace existing).
- This is the closest public proxy for **where the 138 kV system still has
  physical headroom** — leeward/central (Kahe, Ewa Nui, Hoohana) has the most;
  windward (Koolau) is nearly full and permit-constrained. Consistent with the
  REZ study's "Groups 1–7 easy, Group 8 hard" conclusion.

### 4b. HECO curtailment data (performance scorecards)
- HECO publishes Oahu curtailment charts + downloadable history, categorized by
  cause: **Oversupply / System Constraint / Facility Requested.** "System
  Constraint" is the transmission-linked bucket. Files
  `historical_03_curtailment.xlsx` and `..._cat.xlsx` exist but the direct-link
  attempts returned HTML (login/redirect), so the numeric series was **not
  captured** — [UNVERIFIED — not pulled; retrieve via the scorecards page UI].
  URL: hawaiianelectric.com/about-us/performance-scorecards-and-metrics/renewable-energy.

---

## Source family 5 — HNEI (UH Mānoa — Mike's own institution) [PRIORITY LEAD]

HNEI (Hawai'i Natural Energy Institute, SOEST) is a **partner/co-owner of the
GE Oahu grid models**. This is likely the single best route
to non-confidential Oahu network detail *as a UH colleague*.

- **HNEI co-commissioned and co-owns the validated GE Oahu model.** The 2009
  "Oahu Grid Study: Validation of Grid Models" (`hnei_oahu_grid_study_validation.pdf`),
  OWIS 2011, HSIS 2012-13, and the 2013–14 Oahu–Maui interconnection studies were
  all "prepared by GE Energy Consulting / GE Global Research, **submitted by
  HNEI**." The MAPS + PSLF Oahu databases were built under HNEI DOE cooperative
  agreements (DE-FC26-06NT42847, DE-EE0003507). HNEI therefore holds (or
  co-holds) a **full production-cost + dynamic Oahu network model** — buses,
  branches, thermal units — even if the published PDFs redact per-line ratings.
- **GridSTART group (PI Leon R. Roose)** — HNEI's grid-modeling team, funded by
  ONR via **APRISES / APRESA**. Roose is ex-HECO (former chief grid-modernization
  engineer), so GridSTART has direct working knowledge of the HECO PSS/E network.
  GridSTART runs Oahu hosting-capacity, short-circuit, and stability studies.
- **Oahu Distributed PV Grid Stability Study, Part 3 (GE/HNEI, July 2016)** —
  `hnei_oahu_dpv_grid_stability.pdf`. Uses the Oahu load-flow model to compute
  weighted short-circuit ratio (grid strength) **by high-voltage bus**, naming
  the transmission buses and grouping them geographically:
  - **West (strongest): KAHE, CEIP, AES, HRRP** (large synchronous thermal).
  - **East (weaker): IWILEI, SCHOOL, ARCHER, KEWALO, KOOLAU, KOMOKO [Kamoku],
    PUKELE** (load + DPV center).
  - **North (weakest): AKU [Akau], WAHIAWA** — "electrically distant from the
    thermal plants," the utility-scale wind/solar interconnection area.
  - Finding: buses **east of Halawa/School and north of Hema** have the lowest
    grid strength — exactly the corridors of interest. This is a *public* HNEI
    document that reveals relative electrical distance/weakness along the N and E
    corridors without publishing MVA ratings.
- **APRISES annual reports to ONR** (hnei.hawaii.edu/publications/project-reports/,
  APRISES-11 through APRISES-23) contain multi-year Oahu grid-modeling task
  write-ups. Spot-checked APRISES-21 exec summary — that year's grid tasks were
  resource-adequacy/microgrid framed, not a published Oahu one-line; but the full
  technical reports (not just exec summaries) span many years and are the place to
  mine for PSS/E/PSCAD Oahu model descriptions, transfer studies, and any
  published network diagrams. [UNVERIFIED — full APRISES technical reports not
  yet mined line-by-line.]
- **1 MW BESS demonstration:** HNEI's first utility-scale Oahu battery was sited
  at **Campbell Industrial Park generating station** (2012), an HNEI–HECO
  partnership. (Note: the well-documented "1 MW / 250 kWh BESS" MDPI/ResearchGate
  papers are the **Hawaii Island / HELCO** unit — do not conflate. The Oahu CIP
  unit is separate.) Interconnection-voltage detail for the CIP unit
  [UNVERIFIED — pull the HNEI demonstration report].

**→ Best actionable lead:** Mike can approach **Leon Roose / GridSTART at HNEI**
directly. They hold (or can access) the validated PSS/E-equivalent
Oahu network model with buses, branches, and — internally — thermal ratings.
As a UH Mānoa colleague this is almost certainly the fastest path to concrete
N→S transfer numbers that HECO redacts publicly.

---

## Synthesis — what we can responsibly infer about existing N→S transfer capacity

1. **Topology (high confidence, current):** Oahu's bulk grid is a **138 kV
   system, ~200 route-miles, 31 circuits, 21 transmission substations**, arranged
   as two west-anchored corridors (Northern: Kahe–Halawa–Koolau–Pukele; Southern:
   Kahe–Waiau–Iwilei/School/Archer–Kamoku), tied in the west, with the east side
   only recently/partially closed (Archer–Kewalo–Kamoku). Generation is
   concentrated at Kahe (6×138 kV lines) and Waiau (8×138 kV lines) in the
   west/south. [Sources: FERC Form 1 2022; PSIP 2014; D&O 23747.]

2. **The binding N→S / central-north constraint (high confidence):** there is
   **no 138 kV north of the central spine.** North Shore, Wahiawa, and Kahuku
   renewables reach the grid only via **46 kV feeders off Wahiawa and Koolau,
   which are at capacity.** Wahiawa 138 kV substation is a minimal one-bay station
   not built to export power. So the >1 GW of north-shore solar/wind potential
   (REZ Zone 8) **cannot be moved south without major new transmission.**
   [Sources: PSIP 2014; REZ 2021; IGP 2023; OWIS 2011 46 kV wind modeling.]

3. **Quantified limits that ARE public (mind the vintage):**
   - **Single Point of Failure = 135 MW** max single injection increment (2021).
   - **N-1 contingency the system was rated for = 200 MW** (2011 OWITS, likely
     superseded).
   - **Down-reserve = 90 MW** for loss of a 138 kV line (2011).
   - Full north-shore (Zone 8) injection **overloads Wahiawa 138 kV lines unless
     interconnection is cut by 220 MW** (2023 IGP) — i.e., the *incremental*
     N→S export headroom at Wahiawa before overload is on the order of ~900 MW
     of the 1,160 MW potential, [INFERENCE from the 220 MW mitigation figure — do
     not quote as a firm rating].
   - Urban-core south side: **Archer–School & Archer–Iwilei 138 kV UG cables**
     overload without ~37 MW of load relief (2023).
   - **Actual thermal ampacity/MVA ratings of individual 138 kV lines remain
     confidential** in every public source obtained. FERC Form 1 gives geometry
     and cost, never ampacity.

4. **The upgrade menu and its price (2021–2023, current):** moving north/central
   renewables south costs **~$1.2–1.3 B** for the Kahe–Wahiawa–Waiau reinforcement
   (whether via new 138 kV lines, reconductoring, or a novel 345 kV loop — all
   three price within ~5% of each other, ~$1.21–1.28 B). 600 MW off-shore wind
   (only feasible at Koolau) adds ~$0.58 B. These are the concrete cost anchors
   for the paper's "who pays / who benefits from siting friction" argument: the
   transmission wall gates north-shore development. Land-use law is not the only
   barrier.

5. **Where headroom exists now:** leeward/central 138 kV substations (Kahe 5-8,
   Ewa Nui, Hoohana) have spare terminations and host REZ Groups 1–7 with **no
   line upgrades**; windward Koolau is nearly full/permit-constrained. HECO's
   July 2026 prioritization of **Kunia/Schofield + Koolaupoko** (contained
   upgrades) over the north shore is fully consistent with this. [Appendix H
   2025; REZ 2021; 2026 press release.]

---

## Further-investigation list

**Pull manually from PUC dockets (CDMS / puc.hawaii.gov):**
- Docket **2014-0183** final PSIP (Dec 2016) transmission chapter — check whether
  the 138 kV Koolau–Wahiawa loop got a cost estimate the 2014 draft lacked.
- Docket **2018-0165** IGP: the full 2021 REZ study appendices (single-line
  diagrams per substation — Figs 6–41 are in the cached PDF but as images;
  worth OCR/vector extraction if bus configs are needed).
- **Older HECO FERC Form 1 AFRs** (2006, 2015, 2017 on puc.hawaii.gov) →
  time-series of 138 kV vs 46 kV circuit-miles and substation count; shows when
  the Southern Corridor / Ewa Nui build-out happened.
- **Kawailoa Wind PPA** and **Na Pua Makani** dockets/EIS → pin exact POI voltage
  (resolve the 138-vs-46 kV Kawailoa ambiguity).
- HECO **curtailment scorecard Excel files** (System-Constraint category) — grab
  via the scorecards page UI; ties curtailment MWh to transmission cause by year.

**UIPA / public-records angle:**
- Thermal line ratings are the confidential piece. A UIPA request to HECO/PUC is
  unlikely to reach live ratings (claimed CEII/competitive). BUT **non-confidential
  planning inputs** — REZ study bus/branch assumptions, IGP "Grid Needs
  Assessment methodology point books" (one is already public:
  20211105_grid_needs_assessment_methodology_review_point_book_2.pdf) — may be
  obtainable. Target the *methodology* filings, not the ratings.

**IGP working-group participation (best non-adversarial route):**
- The **Stakeholder Technical Working Group (STWG)** and Solution Evaluation &
  Optimization working group receive the detailed transmission decks. UH/HNEI can
  participate; Mike could get current constraint maps through that channel.

**HNEI direct (top priority — see §5):**
- Contact **Leon Roose / GridSTART**. They co-own the validated GE/PSS-E Oahu
  network model and run Oahu transfer/hosting studies. As UH Mānoa colleagues this
  is the most likely source of concrete, current N→S transfer numbers HECO
  redacts. Also mine the **full APRISES technical reports** (not just exec
  summaries) for Oahu network-model write-ups and any published one-lines.
