# What Makes Solar Procurement Fast: KIUC and ERCOT as Contrasts to HECO's Monopsony RFP

Compiled 2026-07-19. Companion data: `data/procurement_speed_benchmarks.csv`;
cached primary sources in `data/raw/procurement/` (see MANIFEST).
Builds on `notes/project-pipeline-mortality.md` — which established that Oahu
utility-scale solar dies overwhelmingly *upstream* of any land-use permit, inside
**HECO's staged competitive RFP** (docket 2017-0352), as economic cancellation, with
award-to-COD routinely 3–7 years and the RFP-launch-to-COD cycle commonly 5–8 years.

**Purpose.** Isolate *what* makes procurement fast by benchmarking two structures that
are not HECO: (A) **KIUC** — same state, same PUC, but a member-owned cooperative that
negotiates bilateral deals; and (B) **ERCOT/Texas** — a competitive merchant market with
no utility-procurement monopsony. The payoff is a ranked list of speed drivers and an
honest split of which Hawaii could adopt vs. which the island physics forbid.

**Evidentiary discipline.** Every figure carries a source URL or an UNVERIFIED flag.
Revealed conduct: dates, PPA prices, filings, completion rates. Motive stays out of scope. Two caveats
run through the whole note and are stated up front so no claim overreaches:
1. **Scale vs. structure.** KIUC is roughly one-tenth to one-fifteenth of HECO's Oahu
   system. A skeptic will say KIUC is just small. That objection is partly right and is
   engaged directly in §A.4 — the honest finding is that scale and structure are
   *entangled* and both real, and the clean citable contrast is a *timing* fact (KIUC
   contracted the first U.S. dispatchable solar+storage five years before HECO's first
   Oahu equivalent). Structure alone does not explain speed.
2. **Island non-transferables.** ERCOT's pure-merchant model cannot be transplanted onto
   an isolated island grid (§B.3). Only specific *process* elements transfer.

---

## PART A — KIUC (Kaua'i Island Utility Cooperative)

### A.1 The procurement model: negotiated bilateral PPAs under a member-owned coop

**Ownership / governance.** KIUC is a member-owned, not-for-profit electric cooperative —
the only electric cooperative in Hawaii — with ~38,695 member-owners governed by a
**nine-member elected board** (three-year terms, ~three seats up each March). It has **no
shareholders and pays no dividends**; net margins return to members as capital credits.
KIUC was created by purchasing the investor-owned Kauai Electric (a Citizens Utilities
subsidiary) on **2002-11-01 for $215M** — a documented conversion of an IOU into a coop.
Sources: https://en.wikipedia.org/wiki/Kaua%CA%BBi_Island_Utility_Cooperative ;
https://kiuc.coop/election ;
https://www.canarymedia.com/articles/clean-energy/kauai-is-a-clean-energy-leader-its-secret-a-publicly-owned-grid

**PUC oversight still applies — this is the key control.** KIUC remains a **regulated
utility under Hawaii PUC jurisdiction**: it files rate cases (Docket **2022-0208**, filed
2022-12-28; interim D&O 2023-11-27, interim rates effective 2024-01-11, affirmed in the
final D&O May 2025) and its solar PPAs are approved by the PUC exactly as HECO's are
(e.g., AES Lāwaʻi PPA PUC-approved July 2017; LUC special permit SP17-408). So the
comparison **holds the regulator constant** — same PUC, same state, same RPS statute —
and varies only ownership structure and procurement method. (One secondary source
characterizes KIUC as receiving *lighter* PUC direction than HECO; treat the *degree* as
PLAUSIBLE-not-quantified — the *fact* of PUC PPA/rate approval is confirmed by dockets.)
Sources: https://puc.hawaii.gov/public-notice/notice-of-public-hearing-for-kauai-island-utility-cooperative-rate-case-docket-no-2022-0208/ ;
https://kiuc.coop/2023-rate-case-information ;
https://luc.hawaii.gov/completed-dockets/special-permits/kauai/sp17-408/ ;
http://www.ililani.media/2014/12/regulation-and-control-of-kauai-island.html (lighter-oversight claim, secondary)

**Deal structure — negotiated bilateral, third-party-owned.** KIUC does **not** self-build
via a generation subsidiary; its utility-scale solar is **built and owned by third-party
developers** (SolarCity/Tesla, REC Solar, AES Distributed Energy) selling to KIUC under
long-term PPAs. The revealing episode: for the Kapaia/KRS-1 project KIUC **issued an RFP in
March 2014 and got 40+ responses, but "none of them met the co-op's requirements in a cost
effective way"; SolarCity then negotiated bilaterally** until the terms worked (a
first-of-its-kind dispatchable design). For Lāwaʻi, AES and KIUC **co-designed** a custom
DC-coupled, load-following "PV Peaker." KIUC did not buy an off-the-shelf bid. KIUC
runs a recurring, multi-project relationship with AES (Lāwaʻi → West Kauai → Mānā,
Kaahanui). This is the structural opposite of HECO's serial, formalized, multi-year RFP
rounds with PUC-approved bid frameworks and an independent observer.
Sources: https://www.utilitydive.com/news/inside-the-first-fully-dispatchable-utility-solar-storage-project-in-hawaii/408208/ ;
https://www.aes-hawaii.com/new-clean-energy-kauai ;
https://www.utilitydive.com/news/hawaii-kiuc-puc-solar-plus-storage-aes/742965/
Contrast document (cached): HECO's **Code of Conduct for the Oahu Firm RFP** under the
2006 Framework for Competitive Bidding (D&O 23121, Docket 03-0372) —
`data/raw/procurement/code_of_conduct_oahu_firm.pdf`; the **Stage 2 Oahu RFP** (2019-08-22,
Docket 2017-0352) — `stage2_oahu_variable_rfp.pdf`.

### A.2 Flagship project timelines (PPA/announcement → COD)

| Project | MW (solar) | Storage | Developer / land | PPA / announce | COD | Elapsed |
|---|---|---|---|---|---|---|
| **Koloa** | 12 | — | SolarCity / Grove Farm | groundbreak ~2013 | 2014-09 | ~12–15 mo |
| **Anahola** | 12 AC (14.53 DC) | 6 MW battery | REC Solar / **DHHL** (Hawaiian Home Lands) | groundbreak 2014-06 | ~2015-11 | ~17 mo |
| **Kapaia / KRS-1** | 13 | 13 MW / **52 MWh** (Tesla) | SolarCity→Tesla / Grove Farm | **PPA 2015-09-09** (20-yr) | 2017-03 | **~18 mo** |
| **Lāwaʻi** | ~20 AC (~28 DC) | **100 MWh** (5-hr) | AES DE / former sugar land | **PUC-approved 2017-07** (25-yr) | **2019-01-08** | **~18 mo** |
| **West Kauai (WKEP)** | 35 | 240 MWh + pumped hydro | AES | PPA filed 2020-12-31 | reconfigured (see A.3) | — |
| **Mānā** | 35 | 4-hr | AES (WKEP replacement) | PPA ~2024, PUC 2025–26 | ~2028 target | pending |
| **Kaahanui** | 43 | 4-hr | AES (WKEP replacement) | PPA ~2024, PUC 2025–26 | ~2028 target | pending |

**PPA prices** (revealed): Kapaia **13.9–14.5¢/kWh** (blended vs. evening-peak, source
discrepancy — flag both); Lāwaʻi **11¢/kWh** (cheapest source on Kauai bar legacy hydro at
5–6¢); Mānā **$127/MWh (12.7¢)**, Kaahanui **$133.40/MWh (13.34¢)**, each potentially
lower with a USDA PACE loan (−$13.50/MWh) or IRA energy-community credit (−$10/MWh).
The two headline projects — **Kapaia and Lāwaʻi — each went from PPA to commercial
operation in ~18 months.** Sources: https://ir.tesla.com/press-release/kauai-utility-signs-deal-solarcity-first-dispatchable-solar ;
https://www.civilbeat.org/2019/01/kauai-worlds-biggest-solar-power-plant-relies-on-a-flock-of-sheep/ ;
https://www.utilitydive.com/news/hawaii-kiuc-puc-solar-plus-storage-aes/742965/ ;
https://www.businesswire.com/news/home/20140626005440/en/REC-Solar-and-KIUC-Break-Ground-on-12-MW-Anahola-Solar-Array
DATA FLAGS: Lāwaʻi MW reported as both 20 MW (AES page) and 28 MW (Civil Beat) — most
consistent reading ~20 MW AC / ~28 MW DC. Exact **PPA-execution** dates for Koloa/Anahola
were not pinned (used groundbreaking); the individual PUC PPA dockets would settle them.

**The HECO contrast in one number:** KIUC's Kapaia (first U.S. utility-scale *dispatchable*
solar+storage) reached COD in **March 2017**; **Hawaiian Electric did not energize its first
large-scale solar-plus-battery project on Oahu until 2022** — ~5 years later — and its
Stage-1 Oahu solar cohort (RFP 2018, PPAs 2019) reached COD between 2021 and **2025-07-11**
(Hoʻohana, ~6–7 years award-to-COD). KIUC's PPA-to-COD ~18 months vs. HECO's ~3–7 years.
Source: https://www.canarymedia.com/articles/clean-energy/kauai-is-a-clean-energy-leader-its-secret-a-publicly-owned-grid ;
`notes/project-pipeline-mortality.md`

### A.3 Outcomes: renewable share, and near-zero solar cancellations

**Renewable trajectory (annual energy) — climbed fast, but NOT monotonically:** ~8% (2011)
→ **52.8% (2019)** → ~67% reported (2020) → ~60% (2022) → **52.8% (2025)**. KIUC leads the
state and hit its 50%-by-2023 board goal ~4 years early; target is **100% renewable by
2033** (vs. the 2045 state mandate). **Caveat:** the annual number swings with **hydro
(rainfall) and biomass** availability year to year — do NOT present a clean monotonic climb.
For a definitive year-by-year series use KIUC annual reports and the PUC RPS annual reports
(Docket 2007-0008). **Daytime/instantaneous:** on most sunny days KIUC runs the grid at
**~100% renewable during daylight** (fossil units spinning as synchronous condensers, no
fuel burned). Solar is ~32% of *annual* energy (2019), much higher midday; a single clean
"daytime solar %" figure is UNVERIFIED. KIUC also ranked **first nationally in battery
storage per customer**. Sources: https://kiuc.coop/renewable-portfolio ;
https://www.electric.coop/hawaii-kauai-island-utility-cooperative-hits-100-percent-renewable ;
https://en.wikipedia.org/wiki/Kaua%CA%BBi_Island_Utility_Cooperative ;
https://kauainownews.com/2026/05/25/kauai-island-utility-cooperative-among-the-highest-in-state-for-renewable-energy-generation-in-2025/

**Cancellations — the contrast holds, with one honest caveat.** No completed or contracted
KIUC **solar PV** plant in the record was cancelled. The only material retrenchment is the
**West Kauai Energy Project scale-down (2023)**: KIUC dropped the **pumped-storage-hydro /
flow-through** component after an Earthjustice-backed lawsuit over water diversion (settled
2024) and cost increases, **replacing it with the Mānā + Kaahanui solar+storage PPAs**. So
the one KIUC "setback" was (i) the *hydro/water* piece, not the PV, and (ii) resolved by
re-contracting more solar — the opposite of HECO's Oahu/Maui solar
cancellations. (Note the parallel to `project-pipeline-mortality.md`: on Kauai, as on Maui,
the litigation targeted **water/hydro**, not the panels.) Sources:
https://earthjustice.org/press/2023/community-leaders-support-kiucs-decision-to-scale-down-the-west-kauai-energy-project ;
https://www.civilbeat.org/2024/04/opponents-of-kauai-hydro-plan-drop-lawsuit-but-project-is-still-in-limbo/

### A.4 Why faster — structure vs. scale

**Structure (documented):**
- **No shareholder profit motive / no dividends**; a locally **elected member board**. No firm
  balances decarbonization against quarterly investor returns (Canary Media
  frames it exactly this way). No rate-base incentive to prefer utility-owned capex over an
  IPP PPA — the Averch-Johnson channel central to this project's rate-base hypothesis is
  **absent** at a coop.
- **Negotiated bilateral dealmaking:** when a competitive RFP failed to yield a
  cost-effective bid (Kapaia 2014), KIUC negotiated directly to workable terms — faster than
  HECO's staged, framework-bound, multi-year RFP rounds.
- **Single vertically-integrated planning/balancing entity** for one island; PPA approval
  and system planning are not fragmented.
- **Cost outcome consistent with the structural story:** Kauai rates were ~70% *above*
  Oahu's at 2002 formation; today Kauai has among the **lowest rates statewide** and its high
  renewable share buffered members through the 2022 oil-price spike.

**Scale (must be weighted):** KIUC serves one small island (~38,700 members; system
peak on the order of **~80 MW**) vs. HECO's Oahu (**~1,100–1,200 MW** peak) — very roughly
**1/10 to 1/15**. Small scale means (i) a single small project moves the renewable % a lot;
(ii) one balancing area simplifies integration; (iii) 100% instantaneous penetration is far
easier to reach; (iv) negotiating one bilateral deal is administratively lighter than
running a GW-scale multi-round RFP. (The exact peak-MW ratio is a characterization; pin to
EIA-860 / utility load data before publishing — UNVERIFIED as a precise ratio.)

**Bottom line:** structure and scale are **entangled and both real**; the sources support
that cooperative structure *contributes* to speed but do **not** isolate it from scale.
The clean, defensible contrast is the **timing fact** — KIUC contracted the first U.S.
dispatchable solar+storage (PPA 2015 / COD 2017) roughly **five years ahead** of HECO's
first Oahu equivalent — plus the **~18-month PPA-to-COD** on Kapaia and Lāwaʻi against
HECO's **3–7-year** award-to-COD. Do not assert structure *alone* explains it.

---

## PART B — ERCOT / Texas (competitive merchant market)

### B.1 The model, element by element against Hawaii's single-offtaker RFP

| Element | ERCOT / Texas | HECO / Hawaii |
|---|---|---|
| Market | **Energy-only, no capacity market**; generators paid for energy + ancillary services actually produced | Vertically integrated; no wholesale spot market; utility is sole buyer |
| Offtake | **Merchant** or **bilateral corporate PPA** (many buyers); deregulated retail (since 2002-01-01) | **Single offtaker (HECO)**; developer must win a utility RFP to reach a buyer |
| Interconnection | **"Connect and manage"** (ERIS-like): study only *local* connection upgrades, manage congestion via redispatch/curtailment | **"Invest and connect"**-style study on a small islanded grid; interconnection cost/delay a documented Stage-1/2 killer (PUC built the IDRP, Order 39163, 2023) |
| Cost allocation | Generator pays limited direct-connect cost; network cost socialized to the wire company/ratepayers | Interconnecting customer pays Total Estimated Interconnection Cost (HECO Rule 14H) |
| Jurisdiction | **Outside FERC** (no synchronous ties); PUCT + Texas Legislature set market design | Hawaii PUC |
| Land | Abundant, cheap, flat, cleared; **no statutory acreage caps** | HRS §205 10%/20-acre cap on ag land (the land thesis) |

Sources: https://www.ercot.com/files/docs/2019/09/17/Market_Structure_OnePager_FINAL_Revised.pdf ;
https://comptroller.texas.gov/economy/fiscal-notes/archive/2020/august/ogelman.php ;
https://www.ferc.gov/industries-data/electric/electric-power-markets/ercot ;
https://www.utilitydive.com/news/connect-and-manage-grid-interconnection-ferc-ercot-transmission-planning/698949/ ;
https://www.utilitydive.com/news/ercot-connect-and-manage-spp-miso-eris/749083/
The **cost-allocation contrast quantified:** average PJM interconnection network-upgrade
costs jumped to **~$240/kW (2020–22)** from **~$29/kW** in the prior two years — costs an
ERCOT generator largely avoids (it accepts **curtailment risk** instead). The LBNL 2024
edition confirms ERCOT "is not FERC jurisdictional, but uses a 'connect and manage'
interconnection service that is more similar to **ERIS**" — while 87% of active capacity
*outside* ERCOT is studied for the heavier NRIS. Source (cached):
`data/raw/procurement/lbnl_queued_up_2024.pdf`.

### B.2 Speed evidence (quantified)

**Interconnection queue duration (LBNL "Queued Up").** System-wide, median time from
interconnection request (IR) to commercial operation **doubled from <2 years (2000–07) to
>4 years (2018–24), approaching ~5 years for projects completed 2022–23**. Within that,
**ERCOT and the West "typically have relatively shorter durations"** (ERCOT was 39% of the
2023 sample). Sources (cached PDFs): `lbnl_queued_up_2024.pdf`, `lbnl_queued_up_2025.pdf`,
`lbnl_seel_interconnection_slides_2025.pdf`;
https://www.publicpower.org/periodical/article/backlog-power-plants-seeking-transmission-grid-connection-eased-somewhat-2025-lbnl

**Completion rates — ERCOT near the top.** Of projects requesting interconnection 2000–2018,
**only ISO-NE (31%) and ERCOT (30%) exceeded 30% completion**; system-wide only ~13–14% of
capacity requesting since 2000 has reached COD, with ~72–75% withdrawn. Being an ISO does
**not** by itself confer speed — CAISO and SPP are among the *slowest* IA-to-COD regions.
Source: `lbnl_seel_interconnection_slides_2025.pdf`; https://www.osti.gov/biblio/2335720

**Developer-attributed time-to-COD (not LBNL):** ERCOT interconnection study **~1–2 years**
and **~3.5 years total** to bring a project online, vs. **6+ years** elsewhere (PJM, SPP
longest). Attributed to developers at Pine Gate Renewables and Enel. **UNVERIFIED** as an
exact LBNL median-in-years for ERCOT specifically — cite as the industry "~3.5 vs 6+ yr"
contrast alongside LBNL's "ERCOT/West shorter" and the completion-rate ranking. Source:
https://www.utilitydive.com/news/connect-and-manage-grid-interconnection-ferc-ercot-transmission-planning/698949/

**Buildout pace (EIA).** Texas utility-scale solar added ~2.5 GW (2020) → ~4.6 (2021) →
~5.4 (2022); ~16 GW installed end-2023; **~30 GW by end-2024, overtaking California as #1**;
**11.6 GW planned in 2025 alone** (with California, ~half the national total). ERCOT
utility-scale solar generated **45 TWh in the first nine months of 2025 — 50% more than
2024 and ~4× 2021.** Texas is expected to host ~40% of *all* U.S. solar additions in 2026.
This is a scale of annual solar build (single-year GW exceeding HECO's entire multi-decade
utility-scale fleet) that no single-offtaker RFP has ever produced. Sources:
https://www.eia.gov/todayinenergy/detail.php?id=61783 ;
https://www.eia.gov/todayinenergy/detail.php?id=47636 ;
https://www.eia.gov/todayinenergy/detail.php?id=66464 ;
https://www.eia.gov/todayinenergy/detail.php?id=64586
DATA FLAG: cumulative end-2024 total is reported ~22 GW (mid-2024) to ~30 GW (end-2024
secondary); reconcile against EIA-860 before publishing one number (Tier 2).

**Why fast (revealed drivers):** connect-and-manage (no upfront network-upgrade payment);
no single-offtaker RFP gate (merchant + many corporate-PPA buyers); abundant cheap flat land
with no acreage caps; standardized intrastate process outside FERC's cluster-study regime.

### B.3 Tradeoffs — do NOT oversell ERCOT

- **Winter Storm Uri (Feb 2021): reliability collapse.** ≥210 Texas deaths; ERCOT ordered
  ~20,000 MW of rolling blackouts (largest manual load-shed in U.S. history); ~69% of Texans
  lost power at some point Feb 14–20; the grid came minutes from uncontrolled collapse.
  Freezing (44.2%) + fuel issues (31.4%) drove 75.6% of unplanned outages; post-2011 NERC
  winterization advice went unimplemented on cost grounds. Prices held at the **$9,000/MWh
  cap for ~2 days** (~$16B in unnecessary charges per the market monitor). The
  energy-only / no-capacity-market design plus weak weatherization is the core critique.
  Sources: https://en.wikipedia.org/wiki/2021_Texas_power_crisis ;
  https://www.ferc.gov/news-events/news/final-report-february-2021-freeze-underscores-winterization-recommendations
- **No capacity payments → merchant price/revenue risk.** Lower baseline cost but high
  scarcity-price volatility; developers generally won't build without a PPA or large tax
  credit. https://www.rff.org/publications/explainers/us-electricity-markets-101/
- **Curtailment is the flip side of connect-and-manage.** ERCOT curtailed ~9% of solar and
  ~5% of wind (2022); **>8 TWh of wind+solar in 2024**, concentrated in west-Texas
  congestion. Fast/cheap interconnection is "paid for" via curtailment risk borne by
  generators. https://www.eia.gov/todayinenergy/detail.php?id=57100
- **Even Texas concluded energy-only needs a reliability supplement.** PUCT adopted the
  Performance Credit Mechanism concept (Jan 2023, capped ~$1B/yr) then **shelved it
  Dec 2024**, finding it would add only ~780 MW against a ~10,000 MW reliability gap.
  https://www.texastribune.org/2024/12/19/texas-public-utility-commission-performance-credit-power-grid/
  (cached: `puct_pcm_adoption_2023.pdf`)

**Hawaii non-transferables (why the pure-merchant model can't be copied on an island):**
1. Each Hawaiian island is **its own isolated balancing area with no synchronous
   interconnection** — no import/export, no external reserves. ERCOT at least has DC ties and
   vast internal geographic diversity; Oahu has neither.
2. The market is **tiny** (Oahu peak ~1.2 GW), far below the scale at which a competitive
   wholesale market with many generators and many retail buyers is feasible; there is **no
   deregulated retail and no wholesale spot market** to give a merchant plant a price to sell
   into.
3. Therefore the ERCOT package — merchant plants + energy-only spot + curtail-instead-of-
   upgrade — **cannot be transplanted.** What *can* transfer: standardized/streamlined
   interconnection studies, standardized contract terms (standard-offer / feed-in style), and
   connect-and-manage-style curtailment provisions in lieu of gold-plated upfront upgrades.
   (This is the paper's *argument* from ERCOT structural facts + island physics, not an
   external cited claim.)

### B.4 Third comparator — separating "market vs. monopsony" from "fast process vs. slow RFP"

A **regulated, vertically integrated monopoly with no merchant market** can still procure
solar fast **when it self-builds on a standardized program**. Serial RFPs are the slow path.
**Florida Power & Light** — regulated, no retail competition — launched "30-by-30"
(30 million panels by 2030) and is building toward **>11,700 MW of utility-owned solar by
2030**, self-constructing (e.g., the ~1,490 MW SolarTogether tranche). Implication: speed is
**not** purely "merchant vs. regulated." The binding difference is **standardized/
programmatic procurement vs. Hawaii's slow serial RFP-plus-PPA-plus-study**. Combined with
CAISO/SPP being slow *despite* ISO membership, this pins the causal variable to **process
design**. Market structure per se is not the driver. Sources:
https://www.prnewswire.com/news-releases/fpl-announces-groundbreaking-30-by-30-plan-to-install-more-than-30-million-solar-panels-by-2030-make-florida-a-world-leader-in-solar-energy-300779381.html ;
https://www.utilitydive.com/news/florida-signs-off-on-fpls-15-gw-community-solar-program-despite-lack-of-c/573428/
(Caveat: FPL is also under a supportive state regulator and self-builds into its own
rate base — a channel Hawaii's rate-base hypothesis would flag; the transferable lesson is
the *standardized program*. FPL's specific incentive is not the lesson.)

---

## SYNTHESIS — ranked drivers of procurement speed, and Hawaii transferability

The three cases vary the same handful of levers. Ranking by how much each moves
**award/PPA-to-COD** time, and whether Hawaii can realistically adopt it:

| # | Speed driver | Fast case | Slow case (HECO) | Transferable to Hawaii? |
|---|---|---|---|---|
| 1 | **Single-offtaker monopsony vs. many buyers** | ERCOT: merchant + many corporate PPAs | One utility RFP is the only door | **NO (structurally)** — island has no wholesale/retail market. *But* a **standard-offer / feed-in tariff** replicates "a standing open door" without a merchant market → **partial YES** |
| 2 | **Interconnection process** (serial study + full upgrade cost vs. connect-and-manage) | ERCOT connect-and-manage; ~3.5 yr | HECO serial study, customer pays full cost; IDRP built to fix delays | **YES (highest-value adoptable)** — faster/standardized studies, published queue, connect-and-manage-style curtailment terms |
| 3 | **Contract standardization** (standard terms vs. bespoke multi-round RFP) | KIUC bilateral; FPL programmatic | HECO framework-bound multi-year RFP rounds | **YES** — standard-offer contract templates; a **self-build check** so the utility isn't the only builder |
| 4 | **Procurement cadence** (rolling/negotiated vs. staged rounds) | KIUC negotiates when needed | HECO Stages 1→2→3, years apart | **YES** — rolling/continuous procurement |
| 5 | **Governance / incentive** (coop no-dividend vs. IOU rate-base) | KIUC coop | HECO IOU (Averch-Johnson) | **HARD** — ownership change is a political non-starter; PBR (Docket 2018-0088) is the partial in-place substitute |
| 6 | **Scale** (small single balancing area) | KIUC ~80 MW | HECO Oahu ~1.2 GW | **NO** — cannot shrink Oahu; this is the honest limit on the KIUC analogy |
| 7 | **Land availability** (no caps vs. §205 caps) | ERCOT / Texas | Hawaii ag-land 10%/20-ac cap | **YES via reform** — the land thesis; but see closing point |

**Ranked transferable reforms for Hawaii (what the record says would actually help):**
1. **Faster, standardized interconnection** — published queue, standard study timelines,
   connect-and-manage-style curtailment terms replacing gold-plated upfront network
   upgrades. Highest-value, already the subject of the PUC's IDRP (Order 39163, 2023).
2. **Standard-offer / feed-in contracts** — a standing open procurement door that mimics
   "many buyers" without needing a merchant market (the only piece of the ERCOT advantage an
   island can import).
3. **A self-build / competition check** — KIUC and FPL show that *someone other than a
   framework-bound serial RFP* building to standard terms moves fast; ensure the utility is
   not the sole gatekeeper of pace (PBR should reward throughput, not just capex).
4. **Rolling procurement cadence** replacing years-apart staged RFP rounds.

**What Hawaii cannot adopt:** a genuine merchant market (no wholesale/retail market on an
isolated ~1.2 GW island); ERCOT-scale geographic diversity and imports; or KIUC's small
single-balancing-area scale. These are the honest non-transferables.

### Tie-back to the land thesis

The land-restriction story (HRS §205 10%/20-acre cap) is **necessary but not sufficient.**
Even with unlimited eligible acreage, Oahu solar would still bottleneck at **HECO's
monopsony RFP and the interconnection queue** — the stages where `project-pipeline-mortality.md`
shows projects actually die. KIUC (same land law, same PUC) built fast anyway via negotiated
bilateral deals; ERCOT built ~30 GW largely because **interconnection and offtake are
frictionless there** — land is not the constraint. So **procurement/interconnection design is a co-binding
constraint** sitting alongside land reform. The policy implication is joint: liberalizing
§205 raises the *ceiling* on where solar can go, but **standardized interconnection + a
standing contract path** is what determines whether projects actually get built at speed.
Land reform without procurement reform relaxes a constraint that isn't the binding one on
Oahu; the two must move together.

---

## Evidence-quality caveats (consolidated)
- **KIUC renewable %** is non-monotonic (hydro/rainfall variance); the 67%/60%/52.8% figures
  come from different secondary sources — use KIUC annual reports + PUC RPS reports (Docket
  2007-0008) for a definitive series. "Daytime solar %" as a single number: UNVERIFIED.
- **Lāwaʻi MW** (20 AC vs 28 DC) and **Kapaia PPA price** (13.9 vs 14.5¢): source
  discrepancies, flagged in-line.
- **KIUC/HECO peak-MW ratio** (~1/10–1/15): characterization, pin to EIA-860 before
  publishing.
- **ERCOT median IR-to-COD "in years"** from LBNL's own text: UNVERIFIED as one figure; use
  the "~3.5 vs 6+ yr" developer contrast + LBNL "ERCOT/West shorter" + completion-rate rank.
- **Texas cumulative solar** end-2024 (~22–30 GW range): reconcile against EIA-860.
- The **synthesis transferability table** rows 1–4 are the paper's analytic argument built on
  the cited structural facts; rows 5–7 (governance/scale/land) restate this project's other
  findings. Non-transferability of the merchant model is an argument from island physics, not
  an external citation.

## Follow-ups worth a manual pull
- KIUC PUC PPA dockets for exact Koloa/Anahola PPA-execution dates and prices; KIUC annual
  reports + PUC RPS Docket 2007-0008 for the definitive year-by-year renewable series.
- EIA-860 for Lāwaʻi AC/DC reconciliation, KIUC vs HECO system-peak MW, and Texas cumulative
  solar.
- FPL Ten-Year Site Plan for a precise self-build GW/yr rate.
- HECO Stage 1/2/3 RFP schedules (cached RFP PDFs) to compute exact RFP-launch-to-award and
  award-to-COD intervals for a clean side-by-side with KIUC's ~18-month PPA-to-COD.
