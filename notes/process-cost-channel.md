# The Cost Channel: What Procurement Friction Adds to the Price of Oʻahu Solar

Compiled 2026-07-20. Synthesis note. Assembles the price consequences of the
process facts documented in `notes/heco-solar-procurement.md`,
`notes/heco-ppa-terms.md`, `notes/project-pipeline-mortality.md`, and
`notes/procurement-comparison-kiuc-ercot.md`. Verification vocabulary per
`docs/NOTES_INDEX.md`: [V] primary-sourced, [P] plausible awaiting evidence,
UNVERIFIED flagged.

**The finding.** Process friction shows up in three measurable places: award
prices that roughly doubled in real terms between Stage 1 and Stage 3 while
mainland benchmarks rose far less; a delivered-capacity rate near a quarter of
what a 2045-compliant buildout requires; and a class of land (as-of-right B/C
parcels) with no route to a power purchase agreement at all. Each is
quantified below with its evidence tier.

**Attribution, stated carefully.** The friction lives in a machinery with
several authors: the legislature drew the 5 MW waiver (2006 Framework
statute era; HSCR1152 2011), the PUC wrote and approved the Framework, the
RFP rules, and every PPA price, and HECO administers the auctions,
interconnection studies, and contracts — and bids its own projects into
them. HECO operates the machinery; the design predates and exceeds any one
operator, and the incentive structure (a single offtaker that earns its
return on owned rate base, none on purchased power) would push any firm in
the same seat the same way. The clean evidence for design-over-operator is
KIUC: same state, same regulator, same statute, different ownership and
procurement structure, ~18-month PPA-to-COD. Reform aimed at the design
(study clocks, price re-openers, symmetric delay penalties, sub-5-MW
offtake) does not require a villain.

**The counterfactual, and why it matters despite being unprovable.** Stage 1
priced Oʻahu solar+storage at $0.08–0.10/kWh in 2018–19. Had 1–2 GW
connected at those prices by ~2021 — plausible under a connect-and-manage
interconnection regime and larger solicitations, though no counterfactual
can be proven — the arithmetic is large: each GW of solar+storage delivers
roughly 2.2 TWh/yr, displacing oil-fired generation whose fuel alone costs
$160–190/MWh at reference oil (LSFO $16–18/MMBtu × ~10.5 MMBtu/MWh steam
heat rates), against a ~$90/MWh contract price. That is on the order of
$150–250M/yr of fuel savings per GW, more during the 2022 and 2026 oil
shocks — roughly $1B cumulative by 2026 for a 1.5 GW counterfactual
cohort. The state also would have entered the LNG debate with a third of
its load already contracted at single-digit prices. This is illustrative
arithmetic, flagged as such; its purpose is to size what the process
friction plausibly cost, and it is conservative in one respect — it counts
only fuel, none of the risk-premium feedback of §3.

**No published ceiling below ~3 GW exists.** HECO's IGP Base Plan integrates
"nearly 3,000 MW of solar and storage" by 2050 and its Land-Constrained
variant retains most of it; HSEO's scenarios keep 93–100% of their solar
when LNG is added; the companion capacity-expansion analysis builds ~5 GW
against a 5.45 GW screen. The lowest utility-scale figure in any official
mix (~2 GW-equivalent, HSEO) is a chosen portfolio with offshore wind and
imported biofuel filling the difference — a preference, never a feasibility
claim. The disagreement on the record is entirely about pace and route.

---

## 1. The price record

| Cohort | Price | Year | Tier |
|---|---|---|---|
| Stage 1 bids (Oʻahu + neighbor islands) | $0.08–0.12/kWh | 2018 | [V] CleanTechnica 2019-01-14; pv-magazine-usa 2019-03-28 |
| Stage 1 PUC-approved cohort (6 projects, 247 MW / 998 MWh) | $0.08–0.10/kWh | 2019 | [V] pv-magazine-usa 2019-03-28 ("Hawaii's new reality of solar plus storage: under 10 cents") |
| Oil-fired generation cost, same period | ~$0.15/kWh | 2019 | [V] same source |
| Molokai first solar+storage PPA | $0.17/kWh (22-yr) | ~2024 | [V] Energy-Storage.News / PV Tech |
| Stage 3 Oʻahu solar awards (Mahi re-procured, Puʻuloa Solar) | ~$0.21–0.23/kWh | 2024–25 | [P] — companion capacity-expansion analysis; pull the PPA sub-dockets (Mahi: 2025-0414) for the approved figures |
| Mainland utility-scale solar+storage medians, same window | $0.04–0.07/kWh, flat to modestly rising | 2018–2024 | [P] LBNL *Utility-Scale Solar 2024* (emp.lbl.gov/pv-ppa-prices); LevelTen North America index $61.67/MWh in 2024 (pv-tech.org) |

Read across the rows: Oʻahu's award price roughly doubled in nominal terms
(2018 → 2024) over a window when the mainland index rose by a fraction of
that, and hardware, which both markets buy from the same suppliers, cheapened.
The residual is the price of everything local: procurement cycle time, contract
risk allocation, interconnection exposure, and the attrition premium described
in §3. The companion capacity-expansion analysis prices the same residual from
the other direction: holding deployment costs at the Stage-3-implied level
(~1.8× the mainland benchmark) costs Oʻahu ratepayers ~$2.1 billion (2027–2050
NPV) relative to the achievable-cost baseline.

## 2. How process enters the bid before anything goes wrong (ex ante)

Every row below is a contract term verified in `notes/heco-ppa-terms.md`
against the Model RDG PPA / Stage 2 RFP. Each shifts a quantifiable risk to
the seller. A seller prices risk; the price returns in the bid.

- **No escalation, 20-year fixed nominal price** (RFP §3.9.2). The seller
  bears all inflation risk for two decades. At 2.5%/yr expected inflation a
  flat nominal price loses ~22% of real value by year 10; a rational bidder
  adds the expectation to the opening price.
- **Guaranteed COD fixed at proposal, non-adjustable** (RFP §1.2.15), with
  daily delay damages (~0.2%/day of the monthly lump sum) drawn from posted
  security — while interconnection study timelines the utility controls ran
  21–24 months (PA Consulting [V]) and utility-caused delay carried no
  symmetric penalty. The bidder prices the asymmetry.
- **$75/kW operating letter of credit held at full value for the entire
  20-year term, A-rated issuing bank throughout** (§14.4–14.5). LOC carrying
  cost is a running charge a mainland step-down structure avoids.
- **Developer pays all interconnection costs plus an overage LOC**
  (RFP §1.2.16), against a study process that serializes clusters and
  restudies on any change (PA Consulting [V]).
- **No degradation may be proposed** over 20 years (RFP §2.1): the seller
  oversizes the array to hold capacity flat, a real capital adder.
- **State tax credits must be pursued and remitted to the utility**, with
  liquidated damages for failure (§1.2.18); the price is set without them.
- **$10,000 non-refundable proposal fee**, non-negotiable NDA (§3.12).

The willing-buyer test: a buyer seeking volume keeps the terms that buy
island reliability (dispatchability, ride-through, grid-forming, storage
control — the `heco-ppa-terms.md` "island-justified" column) and relaxes the
terms that only shift risk (escalation prohibition, non-adjustable GCOD,
full-term LOC, delay asymmetry). The observed contract keeps both sets.

## 3. How process kills after award (ex post), and what the kills cost

The mechanism, on the record ([V] throughout, from
`notes/heco-solar-procurement.md` §4–5):

1. Award-to-COD for the built Oʻahu cohort ran a median ~5–5.5 years against
   ~3-year PPA targets; RFP-issue-to-COD ran 4–7.4 years.
2. Input costs spiked mid-queue (module prices +57% in 2021; AD/CVD freeze
   2022) while the approved price could not move: HECO filed two Stage-2
   price amendments 2022-02-15; the PUC denied both 2022-03-02; the developer
   declared the PPAs null and void and walked.
3. Result: ~5 of 8 Oʻahu Stage-2 solar projects died. The utility terminated
   almost none of them; the structure did.
4. Re-procurement restarts the clock at the new price level. Mahi is the
   controlled experiment: awarded Stage 2 (2020-05) in a ~$0.09–0.10/kWh
   cohort, cancelled 2022-05, re-awarded Stage 3 (2023-12), PPA signed
   2025-11 — ~3.5 years lost on the same site, same developer. **Follow-up:**
   the approved Stage-3 Mahi price (Docket 2025-0414) against its Stage-2
   cohort price is the single cleanest number for "what the process delay
   cost"; pull it when the D&O issues.

Attrition also feeds back into §2: bidders who watched Stage 2 price the
observed hazard into Stage 3 bids. A pipeline that kills half its cohort
raises the price of the surviving half.

## 4. The deployment-rate consequence

RFP-era utility-scale solar actually in service on Oʻahu ([V] status board
data in `notes/heco-solar-procurement.md`): Stage 1 delivered 139.5 MW across
four projects (2022-07 through 2025-07); Stage 2 has delivered Kupono (42 MW,
2024), with Mountain View and Waiawa Ph. 2 targeting 2026. Call it ~180 MW
in service seven and a half years after the first RFP issued — roughly 25
MW/yr from RFP issue, or ~45 MW/yr measured from first COD.

A 2045-compliant Oʻahu buildout requires ~200 MW/yr of utility solar
sustained through 2050 (companion capacity-expansion analysis: ~5,050 MW by
2050). The realized process rate is a quarter or less of the required rate.
The land screen is 27,000+ acres; the process has delivered ~1,000 acres'
worth of projects per five years.

## 5. The land with no route to market

`notes/heco-solar-procurement.md` §2c establishes that the 20-acre as-of-right
cap was sized to the ~5 MW competitive-bidding waiver (HSCR1152, 2011). The
RFP floor ("projects must be greater than 5 MW," Stage 2 RFP §1.2.7 [V])
completes the trap: a parcel developed within the as-of-right cap (≤20 ac ≈
4–5 MW) is too small to enter the auction that is the only utility-scale
route to a PPA. The feed-in tariff that once served the sub-5-MW segment is
closed to new enrollment — UNVERIFIED; confirm current FIT/standard-offer
status before citing. CBRE is a separate subscriber program with its own
queue and does not absorb this segment at scale. Net: the ~3,600 acres of
as-of-right B/C land (`notes/cap-quantification.md`) are stranded by
procurement design independent of land-use law. Reforming the cap without a
sub-5-MW standard-offer contract changes little; reforming both changes the
map.

## 6. What fast looks like (comparators, from the dedicated note)

`notes/procurement-comparison-kiuc-ercot.md` [V]: KIUC reaches PPA-to-COD in
~18 months through negotiated bilateral PPAs under the same PUC and the same
RPS statute; its flagship dispatchable solar+storage contracts (Lāwaʻi 2017,
$0.11/kWh) predate HECO's first Oʻahu equivalent by five years. ERCOT's
connect-and-manage interconnection avoids the deep-network study stack
(PJM network-upgrade costs spiked $29→$240/kW; ERCOT's stayed an order of
magnitude lower) at the cost of curtailment risk the generator manages. The
transferable elements for Oʻahu are process elements: study clocks with
consequences for the utility, standardized sub-5-MW offtake, price re-opener
formulas for documented commodity shocks, and security structures that step
down after proven performance.

## Follow-ups

1. Pull the Mahi Stage-3 approved price (Docket 2025-0414) and its Stage-2
   cohort price; publish the pair.
2. Confirm current FIT/standard-offer status for sub-5-MW projects (§5).
3. Pull LBNL PPA-index series directly for the mainland comparison row.
4. Pull Docket 2021-0024 monthly delay filings for dollar figures on
   interconnection delay.
5. Bates White Independent Observer reports (all stages) from CDMS
   2017-0352 — the fairness/self-build findings are Tier 2 until then.
