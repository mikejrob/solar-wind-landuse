# Inside HECO's Solar+Storage PPA: What the Contract Requires, How It Compares, and What Could Be Softened

Compiled 2026-07-17. Companion data: `data/ppa_terms_comparison.csv` (25 rows).
Complements the procurement-**process** notes (`notes/heco-solar-procurement.md`,
`notes/procurement-comparison-kiuc-ercot.md`); this note is the contract-**term** layer.

**Evidentiary discipline.** Every term is quoted from a primary source or flagged
**UNVERIFIED**. Revealed conduct (contract language, filings), not motive. The two
governing instruments are HECO's **Model Renewable Dispatchable Generation PPA
(RDG PPA)** and, for standalone storage, the **ESPPA** — both attached to the RFPs
under **PUC Docket 2017-0352**. Primary docs used:

- **Model RDG PPA (PV+BESS), All Islands** — pulled and text-extracted this session
  from hawaiianelectric.com (`.../20221121_RFP_appx_j_model_RDG_PPA_PV_BESS.pdf`).
  Article/section numbers below are from this document.
- **Final Stage 2 Oahu Variable RFP** (2019-08-22), cached
  `data/raw/procurement/stage2_oahu_variable_rfp.txt` — the RFP body that points to
  the PPA appendices and sets the eligibility/pricing/security rules.
- PA Consulting Act 201 interconnection studies (cached); Stoel Rives *Law of Solar*
  and LBNL for mainland norms; KIUC/AES press + Utility Dive for KIUC (much of KIUC's
  contract detail is **not public** — flagged).

**The one structural fact that frames everything.** HECO does not buy solar energy the
way a mainland IOU does. It buys **dispatchability and availability**. Under the RDG
PPA the variable resource is treated as a **fully dispatchable** unit: HECO holds
"exclusive rights to fully direct dispatch of the Facility" (Stage 2 RFP §1.2.8) and
of the battery's charge/discharge (§1.2.9), and pays a single monthly **Lump Sum
Payment** for (i) actual output *on dispatch*, (ii) the *availability* of Net Energy
Potential for dispatch, and (iii) BESS availability (RDG PPA §2.1). This is a
tolling/capacity structure, not an as-generated energy PPA. It has a large,
counter-intuitive consequence for the "onerous?" question (see Part 2): because the
payment is for **availability**, ordinary economic **curtailment is not a developer
revenue loss** — the lump sum is reduced only for **Force Majeure** unavailability
(§2.3). HECO effectively absorbs curtailment risk. What the developer surrenders is
**all dispatch control and all merchant/arbitrage upside**, and what it takes on is
**availability/performance risk, rigid pricing, and full-term security**.

---

## PART 1 — Term-by-term anatomy

Onerous? = more burdensome than the mainland norm. Island-justified? = defensible for
a small isolated grid (dispatchability/reliability) vs. pure risk-shifting.

| Term | HECO requirement | Mainland norm | KIUC | Onerous? | Island-just.? | Softening option (lever) |
|---|---|---|---|---|---|---|
| **Term** | 20 Contract Years post-COD; Company option to purchase at end (§12.1) | 15–25 yr, 20 common | 20–25 yr | N | Y | none |
| **Development security** | **$50/kW** of Contract Capacity, standby LOC from A-rated US bank; 50% at execution, 50% at IRS amendment; replenish to 3× cap (§14.2) | No universal std; sized to per-diem delay damages; LOC or parent guaranty | not public | N | Y | accept invest-grade parent guaranty; smaller pre-IRS tranche (**PUC**) |
| **Operating security** | **$75/kW** of Contract Capacity LOC held the **entire 20-yr term**, no step-down (§14.4) | Delivery security common but usually steps down after COD or ~6 mo cover-damages | not public | **Y** | partial | step down after proven performance; parent guaranty (**PUC**) |
| **Issuing-bank rating** | LOC bank must keep **S&P A-** for full term; replace in 30 days if downgraded (§14.5) | Investment-grade issuer typical; A- for 20 yr is stringent | not public | **Y** | N | relax to BBB+/IG; longer cure (**PUC**) |
| **Interconnection cost** | Developer pays **all** Total Estimated Interconnection Cost (Rule 14H) + LOC for overages (RFP §1.2.16, §3.13.3) | Varies; ERCOT connect-and-manage socializes network upgrades; PJM upgrades spiked $29→$240/kW | simpler Kauai grid; not public | **Y** | partial | connect-and-manage / socialize deep upgrades; cap exposure (**PUC**) |
| **Price escalation** | **Prohibited** — fixed nominal $ (RFP §3.9.2); price can't be ITC-contingent (§3.9.1) | Many fixed, but escalators (~1.5–2.5%/yr) & indexed products exist | fixed-price (Māná $127, Kaahanui $133.40/MWh); escalation UNVERIFIED | **Y** | N | add CPI/commodity index or re-opener band (**PUC**) |
| **Price re-opener** | Approved price effectively **not re-openable**; 2022 amendments denied → Longroad walked | Fixed but bilateral renegotiation feasible off-auction | KIUC renegotiated bilaterally (Kapaia 2014) | **Y** | N | pre-agreed re-price formula for commodity/AD-CVD shocks (**PUC**) |
| **Payment structure** | Single Lump Sum for output-on-dispatch + NEP availability + BESS availability (§2.1, §2.3) | Energy $/MWh as-generated most common | dispatchable capacity+energy | N | Y | none |
| **Curtailment risk** | Lump Sum paid for **availability regardless of dispatch**; down-adjusted only for FM (§2.3) | "Deemed-generated"/economic-curtailment comp increasingly standard; buyers cap uncompensated curtailment | absorbed by battery | N | Y | none (structurally developer-favorable) |
| **Storage dispatch control** | Company holds **exclusive** charge/discharge control; 100% grid-chargeable after 5-yr ITC; no developer arbitrage (RFP §1.2.9–1.2.11) | Merchant/hybrid PPAs increasingly leave arbitrage to developer | KIUC also dispatches battery (Lāwaʻi PV-peaker) | **Y** | Y | keep control; allow shared-value credit (**PUC**) |
| **No-degradation** | "**may not propose any degradation** for capacity or efficiency" over 20 yr (RFP §2.1) | Guarantees a degradation curve (~0.5%/yr) + 90–95% output guaranty | not public | **Y** | partial | allow realistic degradation curve / oversizing credit (**PUC**) |
| **PV availability guaranty** | **PV EAF ≥ 98%** (12-mo), LDs below (§2.5(b)) | Output guaranty 90–95% of P50/P99 | not public | **Y** | partial | lower to ~95–97% or energy-basis (**PUC**) |
| **BESS performance** | Capacity(4-hr)/EAF/EFOF/RTE metrics each w/ LDs; FFR ≥5 MW/30 min (RFP §1.2.10–12; §2.4) | 4-hr & RTE guarantees standard; FFR less common | 4-hr storage | partial | Y | none (genuine reliability need) |
| **Grid-forming / ride-through** | Grid-forming when directed; full LVRT/HVRT/UFRT/OFRT + transient stability; reactive power at 0 real power; black-start preferred (RFP §2.1, Appx B) | Grid-following historically std; ride-through per IEEE 1547; grid-forming emerging | black-start + advanced inverters | **Y** | Y | none (essential on isolated grid) |
| **Telemetry/SCADA** | Real-time available-energy telemetry for dispatch; sample-rate specs (§3.8.5, Appx B) | Standard | required | N | Y | none |
| **GCOD / delay LD** | GCOD fixed at proposal, **non-adjustable** (RFP §1.2.15); Guaranteed Milestone; daily delay LDs (~0.2%/day of monthly lump sum) drawn from Dev Security | Per-diem delay damages std; but extensions for buyer/interconnection delay usual | not public | **Y** | N | GCOD relief / no LD for HECO-caused delay (**PUC**) |
| **Delay symmetry** | Penalized developer delay, not utility interconnection delay; PA Consulting urged a utility-delay PIM | Interconnection-caused delay usually excused for seller | n/a | **Y** | N | utility-delay PIM + auto GCOD tolling (**PUC**) |
| **State-tax-credit remittance** | Must pursue max state credit & **remit proceeds to Company** for customers; LD if fails; price set w/o state credits (§1.2.18) | Not a standard mainland term | n/a | **Y** | N | keep ratepayer benefit, drop LD asymmetry (**PUC**) |
| **Decommissioning** | Seller solely responsible for decommissioning + restoration (§1.2.17, Attach G §7) | Decommission bonds $15–75k/MW increasingly required | not public | N | Y | none |
| **Change in law** | Proposal can't rely on proposed law change (§1.2.19); change-in-tax risk largely developer-borne | Change-in-law relief clauses common, often shared | not public | **Y** | partial | change-in-law cost-sharing for post-execution federal shocks (**PUC**) |
| **Force majeure** | FM excuses performance; Lump Sum down-adjusted for FM unavailability (§2.3, Art 21) | Standard | not public | N | Y | none |
| **Assignment / financing** | Art 19 collateral assignment to Facility Lender; lender step-in/cure | Financeable lender-consent standard | 3rd-party financed (AES/SolarCity) | N | Y | none (already financeable) |
| **Self-build asymmetry** | HECO self-build **not required to sign a PPA**; may adjust ops w/ PUC approval; LDs from shareholder funds via PPAC; interconnection costs "not comparable" to IPPs (RFP §3.8.4, §1.9) | IOU self-build vs IPP asymmetry a general concern; some states ring-fence it | n/a (coop doesn't self-build gen) | **Y** | N | symmetric proforma; comparable cost accounting (**PUC**) |
| **>5 MW floor** | Projects must be >5 MW (RFP §1.2.7), sized to competitive-bid waiver | No comparable floor | none | partial | N | standardized ≤5 MW standard-offer proforma (**PUC + legislature**) |
| **Proposal fee / NDA** | $10,000 non-refundable per proposal; non-negotiable NDA (§3.12) | Bid fees smaller/uncommon | n/a (bilateral) | **Y** | N | reduce/refundable for small projects (**PUC**) |

*Verification: all HECO rows = primary (Model RDG PPA / Stage 2 RFP). Mainland = Stoel
Rives* Law of Solar*, LBNL, ERCOT sources (secondary). KIUC contract specifics beyond
term/price/dispatch are **not public → UNVERIFIED**.*

---

## PART 2 — Comparison

### 2.1 Against mainland utility-scale solar+storage norms

**Where HECO is standard (do not overclaim onerousness):**
- **Term** (20 yr), **decommissioning** on seller, **financeability** (Art 19 lender
  collateral assignment + step-in) are all mainstream.
- **Security *levels* are not the outlier.** $50/kW development + $75/kW operating LOC
  is comparable to, not far above, mainland practice (there is "no universal standard";
  Stoel Rives). The onerous wrinkle is **structure, not size**: the operating LOC is
  held at full value for the **entire 20-yr term with no step-down** and demands an
  **A-rated issuing bank throughout** — both tighter than the mainland pattern of
  post-COD step-downs and investment-grade (not A-) issuers.
- **BESS 4-hr duration, RTE, grid-forming, ride-through, black-start, FFR** — these
  *look* onerous next to a mainland grid-following energy PPA, but they are genuine
  small-island reliability functions, not risk-shifting (see 2.3).

**Where HECO is genuinely more onerous (risk-shifting):**
1. **Price rigidity.** Escalation is *prohibited* (§3.9.2) and the approved price is
   effectively un-re-openable. Mainland PPAs are often fixed too, but escalators and
   bilateral renegotiation exist. This is the term the record shows actually **killing
   projects**: 2021–22 input inflation + AD/CVD, HECO's price-amendment requests denied
   by the PUC 2022-03-02, Longroad declared Mahi/Pulehu null-and-void and walked
   (`notes/heco-solar-procurement.md` §4).
2. **Zero-degradation guarantee.** "May not propose any degradation" over 20 years
   (§2.1) contradicts physics (panels degrade ~0.5%/yr) and the mainland norm of a
   priced degradation curve — it forces oversizing and prices in a permanent cushion.
3. **PV availability ≥98%** with LDs (§2.5) is tighter than the mainland 90–95% output
   guaranty.
4. **Full interconnection cost on the developer** (Rule 14H) — the opposite of ERCOT
   connect-and-manage, and a documented Stage-1/2 cost killer (Puakō-ENGIE).
5. **Self-build asymmetry** — HECO's own projects need no PPA, can adjust operational
   requirements with PUC approval, pay LDs from shareholder funds, and (per PA
   Consulting) report interconnection costs on a non-comparable basis. No IPP gets that.
6. **State-tax-credit remittance + LD-for-failure** and a **non-refundable $10k/proposal
   fee** are HECO-specific frictions with no clean mainland analog.

### 2.2 Against KIUC

KIUC's utility-scale solar is **third-party-owned** (AES, SolarCity/Tesla) under
**negotiated bilateral** PPAs — 20–25 yr, **fixed-price** ($127–133.40/MWh on
Māná/Kaahanui; ~11¢ Lāwaʻi; ~14¢ Kapaia). Crucially, **KIUC also takes full dispatch
control of the battery** (the Lāwaʻi "PV Peaker" is load-following under KIUC direction)
— so *utility dispatch control is what an isolated island
grid does*, not a HECO peculiarity — which **corroborates the island-justified label** on that term. KIUC's
detailed **security, availability, LD, and change-in-law terms are not public
(UNVERIFIED)**, so a term-by-term security comparison can't be made. The defensible
contrast is *process*, not clause text: KIUC **renegotiated bilaterally when a
competitive RFP failed** (Kapaia 2014); it did not lock in a rigid auction price — the
exact pressure-relief valve HECO's structure lacks. (Scale caveat from
`procurement-comparison-kiuc-ercot.md` applies: KIUC is ~1/10–1/15 of Oahu.)

### 2.3 Island-justified vs. risk-shifting — the honest split

**Island-justified (keep):** full dispatch control of PV *and* battery; grid-forming
mode; the LVRT/HVRT/UF/OF and transient-stability ride-through suite; 4-hr storage
duration; Fast Frequency Response contingency storage; RTE/black-start; real-time
telemetry. On a grid with **no synchronous ties and no external reserves**, these are
reliability necessities — and KIUC imposes the functional equivalents. The
availability-payment structure that comes with dispatch control is even
**developer-favorable** on curtailment.

**Risk-shifting (not reliability-driven):** the escalation ban + un-re-openable price;
the zero-degradation guarantee; the 98% availability LD; the full-term/no-step-down
$75/kW A-rated LOC; the full Rule 14H interconnection cost on the developer; the
self-build asymmetry; the non-adjustable GCOD with one-sided delay LDs; the
state-credit-remittance LD; the $10k proposal fee. These transfer market/inflation/
interconnection risk onto the party least able to price it over 20 fixed years, and
none of them is required by island physics.

---

## PART 3 — What could be softened (ranked, with lever)

Ranked by how much relaxation would lower developer barriers/cost **without**
compromising a small-island grid. **PUC** = the Commission can order it by approving a
revised proforma / interconnection tariff / PIM (no statute needed). **Legislature** =
needs a bill.

1. **Price indexing / cost-adjustment / a defined re-opener band.** *Highest value.*
   The escalation ban + rigid approved price is the single term the record shows
   *killing* projects (Mahi/Pulehu 2022). A CPI/commodity index or a pre-agreed
   re-pricing formula for pre-COD commodity/tariff shocks would have saved them.
   **Lever: PUC** (approve a revised RDG-PPA proforma; it already vets the price).
2. **Interconnection cost sharing / connect-and-manage.** Move deep network upgrades
   off the developer's balance sheet (socialize or connect-and-manage-with-curtailment),
   cap developer exposure. Directly attacks a documented cost killer and pairs with the
   PUC's existing interconnection/IDRP work. **Lever: PUC** (Rule 14H / interconnection
   tariff; some cost-recovery mechanics could touch the legislature).
3. **Realistic availability & degradation.** Replace the zero-degradation guarantee with
   a normal degradation curve and drop PV availability from 98% toward ~95–97% (or an
   energy basis). Removes a physically impossible guarantee that just inflates bid
   prices. **Lever: PUC** (proforma performance standards — note these are currently
   *non-negotiable* Performance Standards, so only the PUC/HECO can change them).
4. **Standardized, step-down security; accept parent guaranties.** Step the $75/kW
   operating LOC down after a proven-performance period, relax the A-rated-issuer
   requirement to investment-grade, and accept investment-grade parent guaranties in
   lieu of LOCs. Frees working capital without reducing real protection. **Lever: PUC**
   (Article 14 of the proforma).
5. **Symmetric delay accountability.** A utility-caused-delay PIM plus automatic GCOD
   tolling / LD relief when HECO's interconnection process is the cause. PA Consulting
   already recommended this. **Lever: PUC** (PIM under PBR Docket 2018-0088 / IDRP).
6. **Symmetric self-build treatment.** Hold HECO self-build to the same PPA-equivalent
   terms and comparable interconnection-cost accounting (PA Consulting's exact
   recommendation). **Lever: PUC** (Framework/Code of Conduct, Docket 03-0372).
7. **A standardized ≤5 MW standard-offer proforma** tied to the §205-4.5 by-right
   20-acre land threshold — a standing, template-contract door for small projects that
   avoids the full RFP/IRS machinery (mirrors KIUC/FPL speed). **Lever: PUC** for the
   standard-offer tariff; **legislature** only if the 5 MW/20-acre linkage in HRS §205
   is to be moved (see `notes/sb631-2011.md`).

Not recommended for softening (prudent grid protection): dispatch control, grid-forming,
ride-through, 4-hr duration, FFR, telemetry. Storage-arbitrage rights conflict with
island dispatch needs — at most add a **shared-value credit**, not developer control.

---

## Evidence-quality caveats
- HECO terms are **primary** (Model RDG PPA PV+BESS + Stage 2 RFP, both quoted). The
  ESPPA (standalone storage) was not separately pulled — assumed parallel; verify if a
  standalone-storage claim becomes load-bearing.
- The Model RDG PPA pulled is the **All-Islands PV+BESS** template (Stage 3-era);
  Stage-1/Stage-2 executed PPAs (in the individual approval sub-dockets) may differ in
  the exact $/kW and 98% figures — **spot-check an executed Oahu PPA on CDMS** before
  publishing a specific number as universal.
- **KIUC** security/availability/LD/change-in-law terms are **not public → UNVERIFIED**;
  only term length, fixed-price nature, and dispatch control are confirmed.
- Mainland "norm" rows are **secondary** (Stoel Rives, LBNL, ERCOT reporting), not a
  single authoritative model PPA. The **EEI model PPA** was not obtained this session —
  a targeted pull would firm up the security/curtailment "norm" columns.
- The delay-LD "~0.2%/day of monthly lump sum" is from a worked **example** in the
  proforma, not a stated rate — treat as illustrative.
