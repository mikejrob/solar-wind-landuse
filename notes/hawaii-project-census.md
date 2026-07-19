# Hawaii Utility-Scale Renewable Project Census: Pipeline Timing, Interconnection, and Cause of Death/Delay

Compiled 2026-07-19. Master data: `data/hawaii_solar_project_census.csv` (60 projects,
one row each). This note is the authoritative empirical record that adjudicates a specific
dispute: **HECO and some observers cite community resistance / permitting as the obstacle to
Hawaii solar; our prior work found that for OAHU utility-scale SOLAR the mortality is in
procurement + interconnection, while community resistance is real
for WIND (Oahu/Lanai/Molokai) and for SOLAR on MAUI.** The census below makes that precise
across every island and technology and reports what the full record shows.

## Lineage (this dataset supersedes/absorbs five overlapping ones)

`hawaii_solar_project_census.csv` consolidates and dedupes, one row per physical project:
- `data/oahu_solar_project_pipeline.csv` (Oahu pipeline mortality)
- `data/heco_procurement_timeline.csv` (37 rows; the HECO Stage 1/2/3 spine — dates,
  dockets, CODs, cancellations)
- `data/sup_census.csv` (LUC special-permit tier; landowner/counsel/soil detail)
- `data/community_resistance_cases.csv` (the resistance episodes, by forum/group/effect)
- `data/procurement_speed_benchmarks.csv` (KIUC/Kauai bilateral timing)
Plus gap-fill for Kauai (KIUC), Molokai, Lanai, and the wind/biomass fleet.
Those five remain as-is for provenance; the census is the single master. Source notes behind
them: `project-pipeline-mortality.md`, `heco-solar-procurement.md`, `sup-census.md`,
`community-resistance-cases.md`, `legal-representation-map.md`,
`neighbor-opposition-and-interconnection.md`.

**Evidentiary discipline.** Every row is primary/secondary-sourced or flagged UNVERIFIED.
We report **revealed conduct** (who terminated, who intervened, what the filing states), not
intent. Interconnection dates are largely **confidential** (per-project IRS/SIS live in HECO
filings and CDMS docket 2021-0024); we flag those rows "confidential" and record only what is
public.

---

## Census size by island (60 projects total)

| Island | Projects | Of which solar / solar+storage | Wind | Biomass | Storage-only / firm |
|---|---|---|---|---|---|
| Oahu | 23 | 15 | 3 | 0 | 5 (2 storage, 2 biofuel-firm self-build, incl. 1 storage) |
| Maui | 13 | 7 | 3 | 0 | 1 (Waena BESS self-build) + La Ola counted under Lanai |
| Hawaii Island | 12 | 7 | 3 | 1 (Hu Honua) | 1 (Keahole BESS self-build) |
| Kauai | 8 | 8 | 0 | 0 | 0 |
| Lanai | 2 | 1 (La Ola 1.2 MW) | 1 (Big Wind) | 0 | 0 |
| Molokai | 2 | 1 (MNEP) | 1 (Big Wind) | 0 | 0 |

Solar / solar+storage projects statewide: **43**. Wind: 11. Biomass: 1. Storage-only: 3.
Firm biofuel (HECO self-build): 2 (Waiau Repower 253 MW, Kalaeloa Partners 208 MW). Note the
census counts projects that **entered a public process** (RFP award, PPA filing, LUC/county
permit, or docketed cancellation); it can miss projects abandoned before any public filing.

---

## The cause-of-death / delay tally (the crux)

Controlled vocabulary (single primary cause per project; contributing cause noted separately):
`procurement/RFP-process, interconnection-cost-or-delay, supply-chain/cost-inflation,
developer-credit, PPA-price-rigidity, community-resistance/permitting-litigation,
cultural-resources, land/lease, utility-termination, other`.

### Solar / solar+storage projects that DIED or were re-procured, by primary cause

| Primary cause | # | Island × project |
|---|---|---|
| supply-chain/cost-inflation | 5 | Oahu: Barbers Point. Maui: Kahana, Kamaole. Hawaii: Waikoloa Village. (+ Pulehu S2, re-procured) |
| developer-credit (HECO below-investment-grade post-wildfire) | 3 | Oahu: Makana La. Hawaii: Puako-Clearway, Kaiwiki (Clearway trio, 2024-10-29) |
| interconnection-cost-or-delay | 2 | Maui: **Puu Hao** (AES "unable to secure the land to interconnect"). Hawaii: **Puako-ENGIE** ("high interconnection costs" cited first) |
| utility-termination | 2 | Oahu: Lanikuhana (2016 SunEdison trio); Molokai: MNEP (MECO default 2020) |
| PPA-price-rigidity | 1 | Oahu: Mahi (S2; amendment denied 2022-03-02, re-procured S3) |
| cultural-resources (on-site, not organized) | 1 | Oahu: Kupehau |
| **community-resistance / permitting-litigation** | **1** | **Maui: Paeahu** (killed by delay; developer won every merits contest) |
| other / UNVERIFIED | 2 | Oahu: Kaukonahua, Mehana (vanished from active list; cause dark) |

Contributing (not primary) community-resistance: **Kahana** (Maui) — opposition *monetized*
via a $1.375M community-benefits agreement, then economics finished the project.

### Community-resistance as the operative cause, isolated by island × technology

| Island | Technology | Project | Effect of resistance | Notes |
|---|---|---|---|---|
| Oahu | **solar** | — | **NONE** | **Zero** organized opposition, intervention, contested case, or lawsuit vs any Oahu utility-scale solar project. The one Oahu solar stopped by anything permit-like (Kupehau) was on-site cultural resources, not a group. |
| Oahu | wind | Na Pua Makani / Kahuku | delayed (not blocked) on the project; WON island-wide via Ord 25-2 | ~165-200 arrests 2019; community lost every merits ruling; turbines operate. But the ordinance drive (Bill 64 -> Ord 25-2, 2025) will retire the Oahu wind fleet 2031-2040. |
| Maui | **solar** | Paeahu | **killed** (by delay) | Only solar land-use permit ever vacated by a HI court (2nd Circuit, Jan 2022). Developer won PUC + Hawaii Supreme Court; delay + cost shock killed it. |
| Maui | solar | Kahana | monetized (CBA), then economics | Opposition bought off, not a block. |
| Hawaii | biomass | Hu Honua / Honua Ola | **killed** | Biggest NGO-litigation win vs a HI renewable (Life of the Land; two Supreme Court appeals; PPA denied on remand, affirmed 2023). Not solar/wind. |
| Kauai | solar+hydro | West Kauai Energy Project | delayed/scaled-down | Resistance (Earthjustice/Poai Wai Ola) targeted the **hydro/water-diversion** component; the **PV survived**. |
| Lanai | wind | Big Wind - Lanai | contributed to death | Also died on interisland-cable-law repeal + economics. |
| Molokai | wind | Big Wind - Molokai | killed | Opposition + landowner (Molokai Ranch) refusal to host. |

**Headline count.** Community resistance blocked/killed **0 Oahu utility-scale solar
projects**, **1 Maui solar (Paeahu, by delay)**, **2 wind (Big Wind Lanai + Molokai)**, and
**1 Hawaii-Island biomass (Hu Honua)**; it delayed/scaled-down **1 Kauai solar+hydro (WKEP —
the PV lived)** and monetized **1 Maui solar (Kahana)**. By contrast, **procurement +
interconnection + finance causes** (supply-chain, developer-credit, interconnection cost/
gen-tie land, PPA-price-rigidity, utility-termination) account for **~14 solar
deaths/re-procurements** across all islands, and **every Oahu solar loss without exception**.

---

## By-island sections

### Oahu (23 projects; 15 solar / 3 wind / 2 storage / 2 firm self-build)

**Solar mortality is 100% economic/procurement.** Stage-1: 0 of 4 Oahu solar lost (all
reached COD; Hoohana last, 2025-07-11, ~7.4 yr from RFP issue). Stage-2 was the kill zone:
of 8 Oahu solar awards, 2 built (Kupono on Navy land; + Kapolei storage), 2 delayed-alive
(Mountain View, Waiawa Ph2, ~4 yr late), ~5 cancelled (Mahi[re-procured], Kupehau,
Barbers Point, Kaukonahua, Mehana). Stage-3: Makana La cancelled 2024-10-29 (HECO credit).
The 2016 precursor is the purest revealed-conduct datum: HECO **unilaterally terminated three
fully-financed Oahu solar farms at once** (Waiawa/Kawailoa/Lanikuhana, 112 MW; PUC staff
called it "premature," "summarily issued"; SunEdison had sunk >$42M site + $31.4M
interconnection) — all later revived and built by Clearway.
- Community resistance vs Oahu solar: **strong null.** Only individual testimony ever
  appeared (~10-16 near-identical emails + Dr. Kioni Dudley at AES West Oahu SP21-411; LUC
  approved 8-0). No group, no intervention, no lawsuit, no contested case.
- Oahu's mass mobilization went to **wind** (Kahuku/Na Pua Makani, arrests) — protesters said
  they'd have supported solar instead. The wind fight then won at the ordinance level
  (Ord 25-2), a future island-wide wind block.
- Why solar draws none: Oahu utility-scale solar sits on **large interior parcels held by
  institutional owners** (KS, Castle & Cooke, UH, Monsanto/Hartung/Fat Law's, Robinson Kunia)
  who **monetize siting rights as lessors**. None is a neighbor, so no abutting owner with the
  proximity injury that confers HRS §91-14 standing (contrast Paeahu, directly mauka of Maui
  Meadows). Several projects route *around* Chapter 205 entirely: Kupono on federal Navy land,
  Hoohana via urban-district boundary amendment. (`neighbor-opposition-and-interconnection.md`)

### Maui (13; 7 solar / 3 wind / self-build storage)

**Both mortality layers present.** Of 5 MECO-side grid-scale solar+storage projects
PUC-approved 2018-2023, **4 died, 1 built** (AES Kuihelani Ph1, COD 2024). Dead: Paeahu
(opposition-delay + cost), Kahana (economics after CBA), Pulehu (economics, re-procured),
Kamaole (economics). Stage-3 added Puu Hao, cancelled 2024-05-31 because **AES could not
secure the gen-tie land to interconnect** — a clean interconnection/land-rights kill.
Kuihelani Ph2 (Stage 3, SP26-417) is advancing. Maui is the one island where **organized,
professionalized community-legal opposition** (Pono Power Coalition, West Maui Preservation
Assn; attorneys Collins/Isaki/Lizzi/Hurley) actually bites — via county-PC contested-case
intervention working as a **delay weapon**. It does not win on the merits (Paeahu).

### Hawaii Island (12; 7 solar / 3 wind / 1 biomass / self-build storage)

Solar mortality is economic + interconnection: AES Waikoloa (first Big Island utility-scale
solar, COD 2023) and Hale Kuawehi (Parker Ranch, COD 2025) built; Puako-ENGIE cancelled 2021
citing **high interconnection costs first**; Waikoloa Village (EDF) cancelled ~2023; the
Clearway trio's Puako + Kaiwiki cancelled 2024-10-29 (HECO credit); Keamuku (86 MW) in
negotiation. The island's marquee opposition case is **biomass**: Hu Honua/Honua Ola, killed
outright by Life of the Land litigation (PPA denied on remand, affirmed 2023) — the biggest
NGO-opposition win against any HI utility-scale renewable, but not solar/wind. The organic
solar fight here is the D/E-land Ocean View residential-subdivision matter (residents wanting
*more* regulation — different in kind from utility-scale-on-farmland).

### Kauai (8 solar; KIUC member-owned coop)

**A clean contrast case: bilateral coop procurement, near-zero mortality, zero solar
opposition.** KIUC negotiates fixed-price bilateral PPAs (no serial RFP monopsony auction):
Koloa (2014), Port Allen (~2012), Anahola (2015), Kapaia/KRS-1 (2017), Lawai (2019) all
built in ~12-18 months PPA-to-COD; Mana (35 MW) and Kaawanui (43 MW, SP26-416) in
development for ~2028. Kauai's solar SUPs drew **zero intervenors** (6-0 to 8-0 votes). The
one resistance episode (WKEP) targeted the **pumped-hydro/water-diversion** component (a
plantation-era water-rights fight); the **PV survived** and was reconfigured. Kauai shows
that when the offtaker is a coop buying bilaterally, projects neither die in a procurement
auction nor draw solar opposition.

### Lanai & Molokai (4)

Small-island solar is tiny (La Ola 1.2 MW, Lanai, 2009; MNEP 4.88 MW, Molokai — MECO
terminated on default 2020). The salient records are the **Big Wind** cable projects
(~200 MW Lanai, ~100 MW Molokai), both dead. Molokai's died on **community opposition +
Molokai Ranch's refusal to host**; Lanai's on the **interisland-cable-law repeal + economics
+ opposition** (Friends of Lanai; Lanaians for Sensible Growth). These are the neighbor-island
"shoulder the burden for Oahu" equity fights — genuine, sustained community resistance
against **wind-for-export**. It did not target solar.

---

## HECO's stated position vs the record

The task asks for HECO's OWN stated position on what obstructs solar, represented at its
strongest, then tested. There are two distinct HECO postures on the record.

**(A) HECO does invoke community/siting concerns — in a policy-alignment framing.** Its
strongest on-record statement is Corporate Energy Planning Manager **Chris Lau**, written
legislative testimony, **2020-02-04** (opposing HB 1864/SB 2317):

> "We see growing issues concerning alignment of key energy, land use, and other policies,
> especially as communities have voiced concerns about siting of certain renewable energy
> projects."
> — Chris Lau, Hawaiian Electric (written legislative testimony, quoted in Civil Beat,
> 2020-02: "Hawaii's Push For Renewable Energy Could Stall Over Public Opposition To
> Facilities," https://www.civilbeat.org/2020/02/hawaiis-push-for-renewable-energy-could-stall-over-public-opposition-to-facilities/
> — quote verbatim VERIFIED 2026-07-19)

Contemporary observers put this more sharply. Sen. **Glenn Wakai** (2020-02-04): "If you
don't want it in your backyard, and you don't want it offshore, then we're not going to get
to 100%." And developers, per reporting, say "regulations that allow community groups to
essentially kill projects after they've been approved are the biggest hurdles," citing
**Paeahu**. This is the strongest version of the "community resistance is the obstacle"
claim, and it is not a strawman: for **Maui solar** and for **wind** it is corroborated by
the record (Paeahu, Kahana, Na Pua Makani, Big Wind, Kahuku Ord 25-2).

**(B) But when HECO explains its OWN project delays/cancellations, it does NOT cite
community resistance — it cites supply chain, interconnection, and developer-side model
deficiencies.** On cancellations, HECO's SEC filings attribute the Stage-2 die-off to
"supply-chain disruption," CBP solar-product port detentions, and site conditions (Q2-2022
10-Q: four null-and-void PPAs; FY2022 10-K: five + one mutual). On delay, HECO's PUC filings
put much of the interconnection delay on developers:

> "developers and their consultants have important responsibilities to facilitate timely
> initiation of the process" (by avoiding last-minute changes and providing adequate facility
> models). — Hawaiian Electric PUC filing (Utility Dive, 2021)

HECO spokesperson **Peter Rosegg**: "Improving the interconnection process is work that
involves everyone — the utility, developers, regulators." HECO's IGP Action Plan frames
interconnection-process improvement and tariff complexity (not community opposition) as the
levers. The PUC's own commissioned diagnostic — **PA Consulting's Act 201 studies** — locates
the delay in the interconnection machinery (SIS run in serialized clusters; one deficient
developer model delays the whole cluster; any post-SIS change triggers a re-study; IRS alone
ran ~24 mo Stage 1 / ~21 mo Stage 2), and recommends HECO track self-build interconnection
costs comparably to IPPs — never in community opposition. (`heco-solar-procurement.md`)

**Does the record support HECO's stated position?**
- **For Oahu solar: NO.** Not one Oahu utility-scale solar project in the census was blocked,
  delayed, or killed by community resistance or a permitting fight. Every Oahu solar loss is
  procurement/finance (utility-termination, supply-chain, PPA-price-rigidity, developer-credit)
  or on-site cultural resources (Kupehau, not an organized group). The "communities voice
  siting concerns" framing, applied to Oahu solar, is **unsupported** by the project record.
- **For Maui solar and for wind: YES, partially.** Paeahu (Maui solar, killed by delay),
  Kahana (monetized), Na Pua Makani/Kahuku (Oahu wind), and Big Wind (Lanai/Molokai wind) do
  show community resistance operating — but note the **mechanism**: except for Hu Honua and
  Big Wind-Molokai, resistance rarely defeats a project on the merits; it **injects delay**
  (via county-PC contested-case intervention) that becomes fatal only when it collides with a
  cost shock. Paeahu's developer won the PUC and the Hawaii Supreme Court and still died.
- **The honest synthesis:** HECO's own operational explanations (supply chain,
  interconnection, developer models) match the census far better than the "community siting
  concerns" framing does. Community resistance is real but **island- and technology-specific**:
  it is a **Maui-solar** and **wind** phenomenon (plus one Big-Island biomass case), and is
  **absent from the Oahu utility-scale solar record entirely.** The claim that community
  resistance/permitting is *the* obstacle to Hawaii solar is true only if you (a) restrict to
  Maui, or (b) conflate wind and biomass with solar. For the largest solar market — Oahu — the
  binding constraint is HECO's monopsony procurement + interconnection, exactly as the prior
  work found. The census does not revise that finding; it generalizes it and bounds the
  community-resistance exception precisely.

---

## Interconnection (emphasized) — what is public vs confidential

Per-project interconnection timelines are **largely confidential** (IRS/SIS numbers live in
HECO filings and CDMS docket 2021-0024; the census marks these rows "confidential"). What the
public record does establish:
- **Systemic delay diagnosis (PA Consulting, Act 201).** IRS alone ~24 mo (Stage 1) / ~21 mo
  (Stage 2); HECO targets ~12 mo for Stage 3. Most IPP projects rated "red," ~6 mo
  interconnection slip. Serialized cluster SIS + mandatory re-study on post-SIS change are the
  named drivers. The PUC built the **IDRP (Order 39163, 2023-04-18)** in response.
- **Interconnection as a named kill cause — 2 projects:** **Puu Hao** (Maui, AES could not
  secure the **gen-tie land/easement** to interconnect — the anticommons chokepoint of
  `neighbor-opposition-and-interconnection.md` Part B, biting in the open) and **Puako-ENGIE**
  (Hawaii, "high interconnection costs" cited first). SunEdison's 2016 trio had already sunk
  **$31.4M in interconnection payments to HECO** before termination.
- **Structural (Oahu):** North Shore/Wahiawa renewables reach the grid only via 46 kV feeders
  at capacity; no 138 kV north of the central spine; moving REZ Zone 8 south costs ~$1.2-1.3B
  (`oahu-grid-public-record.md`). This gates *where* projects can even be proposed — an
  upstream filter more than a per-project kill stage.
- **Self-build asymmetry:** PA Consulting flags that HECO self-build and IPP interconnection
  costs are "not comparable" and recommends separate tracking — relevant to the rate-base
  reading, given self-build grew to the largest Oahu Stage-3 award (Waiau Repower, 253 MW).

---

## Explicit caveats

- **Interconnection dates are often confidential** — the census records "confidential" rather
  than guess; the interconnection *mortality* role is the thinnest quantitatively (inferred
  from IDRP rationale + 2 explicit cancellations, not from an Oahu project killed solely by it).
- **The census counts projects that entered a public process** (RFP award, PPA filing,
  LUC/county permit, docketed cancellation). It can **miss projects abandoned before any
  public filing** — the true denominator of "attempted" solar is unobservable; a community
  objection that deterred a developer pre-filing would leave no trace. The Oahu
  community-resistance null is therefore "absence of evidence in the searched public record,"
  strong but not a proof of universal absence.
- **UNVERIFIED rows:** Kaukonahua and Mehana (Oahu Stage-2 cancellations — date/cause dark);
  Port Allen MW; several landowner fields; La Ola/Kuia/SMRR permit paths (county-tier, Maui
  archives blocked to scripts). Big Wind Lanai/Molokai MW are approximate. HECO self-build
  Kalaeloa Partners detail is partial.
- **The ~63% Stage-2 Oahu attrition and "4 of 5 Maui" figures** are reconstructions from
  award-vs-active lists / named-project reporting, not figures HECO or the PUC published.
- **Two distinct "Puako" projects** (ENGIE Stage 2, 2021, interconnection; Clearway Stage 3,
  2024, credit) — do not conflate. Kahana cancelled 2022-12-30 (not May 2022).

---

## Bottom line for the adjudication

**Community resistance blocked/killed 0 Oahu utility-scale solar projects, 1 Maui solar
(Paeahu, by delay), 2 wind (Big Wind Lanai + Molokai), and 1 Hawaii biomass (Hu Honua) — and
delayed/scaled-down 1 Kauai solar-hydro and monetized 1 Maui solar. Procurement +
interconnection + finance account for every Oahu solar loss and ~14 solar deaths/re-procurements
statewide.** HECO's own operational explanations (supply chain, interconnection process,
developer models) fit the census; its "communities voice siting concerns" framing fits Maui
solar and wind but **not** Oahu solar. The prior finding stands and is now bounded: the
"community blocks solar" story is a **Maui** (and **wind**/**biomass**) story. It is not an Oahu
utility-scale-solar story.
