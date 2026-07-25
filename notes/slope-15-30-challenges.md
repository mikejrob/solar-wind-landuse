# Utility-scale solar on 15-30% slopes: engineering, cost, and Hawaii permitting

Compiled 2026-07-24. Web research; all URLs live as of that date. Percent grade
throughout (15% = 8.5°, 20% = 11.3°, 25% = 14.0°, 30% = 16.7°; percent = 100·tan°).
This note extends `notes/slope-cost-literature.md` (the general ≤15 / 15-30 /
>30 framing and its "no published continuous cost curve" gap) to the 15-30%
band specifically, with an Oahu emphasis, and supplies the aspect quantification
that note flagged as a to-do (its §3). It connects to the map bands in
`notes/available-land-map.md` (the 15-30% increment: +12,239 ac non-military
D/E, +2,325 ac B/C, plus military/durable increments) and the slope screen in
`notes/oahu-slope-screen.md`.

## Headline

The 15-30% band is a real marginal supply carrying a high, aspect-dependent,
permitting-heavy cost premium. Three findings pin it down.

1. The single hardest Hawaii-specific number comes from the SWITCH model
   (Fripp/Ulupono 2021): building solar on 15-20% slope was modeled at a capital
   adder of **+$0.06/W for 15-17.5% and +$0.07/W for 17.5-20%** over flat ground,
   and even with that adder, letting developers use ≤20% slope produced a
   **lower** system cost than a ≤15% limit (11.7 vs 12.3 ¢/kWh in one pairing;
   NPV $26.1B the lowest of any scenario). The premium is small relative to a
   ~$2/W Hawaii plant. Evidence stops at 20%; 20-30% has no Hawaii cost basis.
   https://www.ulupono.com/media/5eclolht/switching-the-paradigm-12-06-21.pdf (p.6 fn.6, p.9)
2. Aspect swings the yield of a 15-30% slope by 10-21 percentage points
   (own clear-sky calc at 21.35°N, `analysis/poa_aspect_slope.py`): a
   south-facing 30% slope gains ~+7% over flat, a north-facing 30% slope loses
   ~-12%. The repo screens grade only; a 15-30% acre's value depends on which
   way it faces.
3. Above ~15% the binding constraint stops being racking and becomes civil,
   geotechnical, and regulatory: foundation length/refusal, cut-and-fill,
   erosion control on erodible ground, and Honolulu's 15%-slope soils-report
   line. Hawaii's rock, rain, and NPDES load compound each.

---

## 1. Racking and tracker limits across 15-30%

Standard single-axis trackers (SAT) run rows N-S and rotate E-W. Two slope
directions bind differently, and this is why "15-30% slope" is not one number.

- **N-S (axis) grade is the hard limit.** The torque tube runs down the row;
  axis grade is set by drive, bearing, and pile-height spec. Array Technologies
  DuraTrack is marketed at **up to 26% N-S grade and up to 40° combined E-W
  articulation** (vendor blog: https://arraytechinc.com/blog/terrain-flexibility-with-duratrack/);
  the datasheet-consistent N-S figure elsewhere is 15%, and the sources conflict
  (`notes/slope-cost-literature.md` §1.2). Conventional Nextracker NX Horizon is
  designed for "flat and relatively flat" sites
  (https://www.pv-tech.org/terrain-following-tracker-nextrackers-revolutionary-nx-horizon-xtr-is-key-to-unlocking-challenging-sites/).
  Take ~15% as the standard-SAT N-S working envelope, ~26% as one vendor's
  aggressive claim.
- **E-W (cross-axis) grade is more forgiving** because rows step down the hill
  independently; the cost is shading. Standard backtracking assumes a level
  E-W plane, so on cross-axis slopes rows self-shade unless slope-aware
  backtracking is used (Anderson & Mikofski, NREL/TP-5K00-76626, 2020:
  https://www.osti.gov/biblio/1660126; conference companion:
  https://www.osti.gov/biblio/1769834). Slope-aware backtracking is now standard
  in pvlib/SAM, so cross-axis loss is largely recoverable in design; the residual
  is configuration-specific.
- **Terrain-following trackers** absorb undulation pile-to-pile and push the
  buildable envelope up without mass grading, at a racking premium:
  - Nextracker NX Horizon-XTR: 0.75° between piles, **8.5° total = 15% grade**
    (https://www.solarpowerworldonline.com/2023/01/single-axis-trackers-upgrade-to-handle-uneven-land-sites/).
  - Array OmniTrack: **2° post-to-post** (June 2026 update, doubled from 1°:
    https://www.globenewswire.com/news-release/2026/06/01/3304438/0/en/ARRAY-Technologies-Announces-OmniTrack-Update-with-Greater-Terrain-Following-Capability.html).
  - GameChange Genius Tracker TF (launched July 2025): **1.7° between posts**
    (https://www.pv-magazine.com/2025/07/03/gamechange-solar-introduces-terrain-following-tracker-designed-to-reduce-land-grading/;
    https://www.solarpowerworldonline.com/2025/07/gamechange-solar-updates-genius-tracker-for-uneven-project-sites/).
  - Nevados All Terrain Tracker: **maximum ~37% (20°) in any direction,
    15° (26%) pile-to-pile, zero grading** — the aggressive end, resting on one
    vendor's case studies (`notes/slope-cost-literature.md` §1.3;
    https://nevados.solar/product/).
- **Fixed tilt tolerates steeper ground than a standard SAT** (no torque tube to
  keep aligned) and is the likely choice on 15-30% ground, especially
  south-facing slopes where the ground tilt does useful work (§2). Ballasted
  (non-penetrating) racking is stricter, "only suitable for slopes up to about a
  15 percent incline"
  (https://www.waste360.com/landfill-operations/are-there-solutions-landfill-slopes-challenge-solar-projects).

**Yield penalty of dropping trackers for fixed tilt.** SAT lifts annual yield
~15-25% over fixed tilt on flat ground in high-DNI sites; the gain is smaller in
cloudy, high-diffuse Hawaii (UNVERIFIED for Hawaii specifically — no local
side-by-side found). On a 15-30% slope the trade is not clean: a south-facing
slope recovers part of the fixed-tilt gap by adding effective tilt (§2), while a
tracker on the same ground is limited by the ~15% N-S envelope. The band
15-30% is where fixed tilt and terrain-following SAT overlap and standard SAT
drops out.

Buildability by band (extends the summary table in `notes/slope-cost-literature.md` §5):

| Band | Standard SAT | Terrain-following SAT | Fixed tilt |
|---|---|---|---|
| 15-20% | Out (beyond ~15% N-S) | In (XTR/OmniTrack/GameChange to 15%; Nevados to 37%) | In (site-specific geotech) |
| 20-25% | Out | Conditional (Nevados spec; PA projects planned at 25%, vendor-reported) | Specialty/site-specific |
| 25-30% | Out | Conditional (within Nevados 37% spec; no completed utility-scale >25% avg found) | Specialty |

---

## 2. Aspect at 21°N: south-facing gains, north-facing loses

At Oahu's latitude the compass direction of a 15-30% slope swings annual
plane-of-array (POA) insolation by 10-21 percentage points. A module laid at the
ground slope inherits the ground's tilt and azimuth; the latitude-optimal fixed
tilt at 21°N is ~21° facing south, so a south-facing 15-30% slope (8.5-16.7° of
tilt) climbs toward that optimum while a north-facing slope tilts away from the sun.

Own clear-sky calc at 21.35°N, Perez transposition, `analysis/poa_aspect_slope.py`
(→ `data/oahu_poa_aspect_slope.csv`). Values are annual POA relative to a flat
(horizontal) surface at the same site:

| Slope | Tilt | South vs flat | North vs flat | East vs flat | South-minus-North |
|---|---|---:|---:|---:|---:|
| 10% | 5.7° | +3.2% | -3.3% | -0.0% | 6.7 pp |
| 15% | 8.5° | +4.4% | -5.2% | -0.3% | 10.1 pp |
| 20% | 11.3° | +5.5% | -7.2% | -0.8% | 13.7 pp |
| 25% | 14.0° | +6.2% | -9.5% | -1.4% | 17.3 pp |
| 30% | 16.7° | +6.8% | -11.8% | -2.1% | 21.1 pp |

Reference: lat-optimal 21°-south fixed tilt is +7.3% over flat, so a south-facing
30% slope (+6.8%) captures nearly the full fixed-tilt tilt bonus for free.
East/west-facing slopes are near-neutral (-0.3% to -2.1%). The numbers are
clear-sky (no clouds), so absolute magnitudes are upper bounds; Oahu's heavy
trade-wind cloud raises the diffuse fraction, and diffuse light is far less
aspect-sensitive, so real-world swings are somewhat smaller. The direction of
the effect is robust; the magnitude is a clear-sky ceiling.

Two consequences for the repo:

- **A 15-30% acre's value is aspect-dependent.** The slope screen
  (`notes/oahu-slope-screen.md`) bins grade only. A north-facing 30% acre yields
  ~12% less than flat before any cost premium; a south-facing 30% acre yields
  more than flat. Screening the 15-30% band by grade alone treats these as
  identical. An aspect overlay is a cheap, high-value addition (§ follow-on).
- **Aspect also moves land-use density (GCR).** Row pitch is set to avoid
  self-shading. A south-facing slope reduces the pitch needed for a given tilt,
  raising ground-coverage ratio and energy per acre; a north-facing slope forces
  wider spacing, lowering density (reasoned geometry from effective-tilt; no
  single Hawaii number). So north-facing 15-30% ground is penalized twice: lower
  yield per module and fewer modules per acre.

---

## 3. Civil and geotechnical challenges above 15%

- **Foundations.** Modest slope is absorbed by varying pile length ("reveal")
  rather than grading, up to roughly 10-15° before site prep dominates
  (https://soeasypv.com/key-design-considerations-for-ground-screw-foundations-in-solar-projects/;
  https://pvrack.com/foundations/). Driven piles are cheapest but hit refusal in
  rock — a Hawaii-endemic problem: Kawailoa and Waianae saw pile refusals until
  pre-drilling was adopted (`notes/slope-cost-literature.md` §4). Ground screws
  and helical piles handle difficult and variable ground and install with less
  disturbance, at higher unit cost on utility scale
  (https://pilebuck.com/foundations-solar-farms-choosing-right-piles-installation-techniques/;
  https://www.anernstore.com/blogs/diy-solar-guides/screw-piles-driven-posts-rocky).
  On 15-30% slope, longer downhill piles, taller reveals, and refusal risk all
  raise foundation cost above a flat site; the exact adder is site-specific and
  unpublished.
- **Grading and earthwork.** Terrain-following racking exists to avoid mass
  grading, but access roads, pads, and drainage still require cut-and-fill, and
  volume scales sharply with slope. Common excavation runs **$3-8/yd³**, rock
  excavation **$15-50+/yd³**, import fill $8-20/yd³
  (https://constructestimates.com/cutting-and-filling-in-earthwork/). Grading a
  sloped 30-acre site "easily runs **$150,000-$400,000** before the solar
  contractor mobilizes" (https://renpro.org/solar-farm-site-work-cost-new-york/,
  NY contractor guide). Hawaii's rock pushes every yard toward the top of the
  excavation range.
- **Slope stability and erosion.** Cut slopes and graded fills on steep ground
  are the failure surface; the panels ride on top of it. Korea's mountainside PV plants
  suffered repeated rainfall-triggered landslides 2018-2020, prompting a tighter
  forestland-slope standard (`notes/slope-cost-literature.md` §2.3); Japan's 2021
  Atami debris flow drove national re-regulation of slope-sited solar. Above
  ~15-20% the binding constraint shifts from racking to geotechnical risk and
  social license.
- **Stormwater.** Any utility-scale project disturbs ≥1 acre and needs an NPDES
  construction permit and SWPPP (§5); erosion-control intensity (blankets,
  micro-terracing, rapid re-seeding, sequenced clearing) rises with slope, and
  reactive washout cleanup runs "5 to 10 times the cost" of upfront control
  (`notes/slope-cost-literature.md` §2.3).

---

## 4. Cost premium for 15-30%, quantified as far as the record allows

The one Hawaii-calibrated, model-embedded number is Fripp/Ulupono's SWITCH slope
cost factor. It covers 15-20% only:

- **+$0.00/W up to 15% slope; +$0.06/W for 15-17.5%; +$0.07/W for 17.5-20%**,
  described as accounting for "additional costs to develop a solar facility on
  steeper slopes," derived from discussions with solar developers
  (https://www.ulupono.com/media/5eclolht/switching-the-paradigm-12-06-21.pdf,
  p.6 fn.6; p.5 on provenance). On a ~$2/W Hawaii plant this is a ~3-4% capex
  adder for 15-20% ground. It is a modeled input informed by developer
  interviews, not a measured EPC delta — treat as a documented planning
  assumption (verified as such), not an empirical cost curve.
- The system-level payoff dwarfs the adder. Allowing ≤20% slope let SWITCH reach
  the lowest-cost plan (NPV **$26.1B** 2021-2054), below every ≤15% scenario;
  the production-cost gap between unrestricted and current-use land at 20% slope
  was **0.6 ¢/kWh** (11.7 vs 12.3), versus 1.1 ¢/kWh at 15% slope
  (same source, p.3, p.8, p.9). Reason: pushing solar onto ≤20% slope keeps prime
  flat ag land available and defers costly offshore wind and biofuels. This is
  the repo's cost-lowering-liberalization thesis (MEMORY: solar-wind-framing) in
  a utility planning model, and it uses the Switch engine that anchors the
  companion `~/Research/oahu-grid` repo — Fripp is Switch's author.
- **20-30% has no published cost basis, Hawaii or otherwise.** NREL ATB/benchmark
  and LBNL benchmarks are flat-reference by construction (no terrain axis;
  `notes/slope-cost-literature.md` §2.1). Above 20% the premium is dominated by
  civil, erosion, and O&M rather than racking, and rests on vendor case studies
  (Nevados). Bound it, do not curve-fit it.

Cost components that rise across 15-30% (none with a clean Hawaii $/W):
grading/roads/pads (earthwork §3), foundations (longer piles, refusal risk §3),
erosion and stormwater control (§3, §5), reduced GCR / energy per acre on
non-south aspects (§2), and O&M (mowing and washout on slopes). The Ulupono
+$0.06-0.07/W factor is the only figure that rolls these into one number, and
only to 20%.

---

## 5. Hawaii permitting and regulatory friction keyed to slope

- **Honolulu grading code — 15% is a bright line.** A grading permit requires an
  engineer's soils report when grading is on land with **existing slopes
  exceeding 15 percent** (also for large cut/fill), and an engineering
  slope-hazard report for cuts >15 ft on grades **steeper than 40 percent**
  (DPP Grading Permit Procedures, rev. July 2024:
  https://www.honolulu.gov/dpp/wp-content/uploads/sites/56/2024/07/grading_permit_procedures.pdf;
  verified in `notes/slope-cost-literature.md` §4). Neither is a prohibition;
  each is a cost/time adder that switches on at 15%. The grading, soil-erosion,
  and sediment-control ordinance was reorganized from ROH ch.14 into **ROH
  Chapter 18A** (https://codelibrary.amlegal.com/codes/honolulu/latest/honolulu/0-0-0-17460);
  an Erosion and Sediment Control Plan is required and a grading bond attaches
  above the volume/height thresholds.
- **NPDES construction permit (State DOH).** Any project disturbing **≥1 acre**
  (every utility-scale site) needs coverage under Hawaii's NPDES Construction
  Storm Water General Permit (HAR ch.11-55, App. C) and a SWPPP; land
  disturbance includes clearing, grubbing, grading, and staging
  (https://health.hawaii.gov/cwb/files/2020/10/NPDES-Construction-Storm-Water-General-Permit-FAQs.pdf;
  https://health.hawaii.gov/cwb/general-permits/). Hawaii's low-erosivity waiver
  (R < 5) is unavailable in the state's wet, high-erosivity zones (§6), so the
  full SWPPP applies. Erosion-control scope, and thus cost, scales with slope.
- **State land use.** The 15-30% band sits inside the Agricultural district
  (the repo's screen), so the chapter 205 cap/SUP regime governs (not slope
  per se). Conservation-district land (treated as unavailable, `docs/ASSUMPTIONS.md`
  B6) is a separate matter; slope is one of the factors that pushed steep upland
  into that district historically. SMA review applies only near shore.
- **Cultural and archaeological.** Ground disturbance triggers historic-
  preservation review (HRS ch.6E). Earthwork volume, and therefore the surface
  area disturbed and the chance of encountering iwi or sites, rises with slope,
  so the 15-30% band carries higher archaeological/cultural exposure than flat
  ground (reasoned; no slope-keyed statute — HRS 6E is triggered by disturbance,
  which grading multiplies).

---

## 6. Hawaii physical hazards that compound slope

- **Erosive rainfall.** Windward and upland Oahu are among the wetter, more
  rainfall-erosive places in the U.S.; the low-erosivity construction waiver
  (R < 5) does not reach them. A specific Hawaii R-factor value for a given
  candidate zone is UNVERIFIED here (use the EPA rainfall-erosivity calculator
  per site: https://www.epa.gov/waterdata/rainfall-erosivity-factor-calculator).
  Intense convective bursts drive rill and gully erosion on freshly graded cut
  slopes during construction — the window Korea's and Japan's failures occurred in.
- **Volcanic soils, with nuance.** Hawaiian Oxisols are highly aggregated and
  "exhibited a very high resistance to splash detachment" in rainfall-simulation
  work (https://www.sciencedirect.com/science/article/abs/pii/S0933363096000037),
  so intact vegetated Oxisol resists sheet erosion. The risk on a solar cut is
  different: disturbed, unaggregated subsoil and concentrated flow paths on
  graded slopes, where silt fractions detach readily (Oahu erodibility work:
  https://agupubs.onlinelibrary.wiley.com/doi/abs/10.1029/WR003i003p00785). The
  hazard concentrates in construction-phase channelized flow over disturbed subsoil.
- **Seismic.** Hawaii carries real seismic loading (Big Island especially);
  racking and foundations on slope must carry combined seismic-plus-slope load
  cases. No Oahu-specific slope-seismic PV design figure found (UNVERIFIED).
- **Hawaii precedent on slope.** Oahu already builds on 15%+ ground.
  **Two-thirds of the AES West Oahu (~30 MW) project and ~10% of the EE Waianae
  project sit on slopes of at least 15%**, on the lower Waianae mountain slopes
  (Civil Beat 2021:
  https://www.civilbeat.org/2021/12/how-solar-farms-on-mountain-slopes-could-help-hawaii-meet-food-sustainability-goals/).
  Developers in that reporting put the "maximum industry standard" at ~10-15%
  slope and describe willingness to go to <20% at higher per-project cost — the
  same envelope as the Ulupono/Fripp model. No Oahu utility-scale project on a
  **>20% average** slope surfaced in this sweep (UNVERIFIED that any exists);
  the built precedent tops out where the cost record does.

---

## 7. Bottom line for the repo

15-30% land is a genuine marginal supply carrying a high, aspect-dependent cost
tail. State it this way:

- **15-20% is buildable today in Hawaii** at a modeled ~$0.06-0.07/W premium
  (Ulupono/Fripp), demonstrated on the ground (AES West Oahu, EE Waianae), and
  under a modeling framework that finds the extra ground **lowers** total system
  cost by keeping prime ag flat land free. The repo can defend counting 15-20%
  D/E as real supply.
- **20-30% is a speculative tail.** Feasible on paper with terrain-following
  racking (Nevados spec to 37%), but with no Hawaii cost basis, no completed
  Hawaii project, rising geotechnical/erosion/social-license risk, and the
  Honolulu 15% soils-report and NPDES loads applying throughout. Count it as a
  caveated upper bound on supply.
- **Aspect should qualify the whole 15-30% band.** A north-facing 30% acre is
  double-penalized (yield -12%, lower GCR) and a poor candidate; a south-facing
  30% acre nearly matches flat-ground yield. Grade alone overstates the usable
  15-30% resource on north aspects and understates it on south aspects.

This refines `docs/ASSUMPTIONS.md` E2 (the ≤15 / 15-30 / >30 convention): the
15-30% band is better modeled as 15-20% (firm, small premium) plus 20-30%
(speculative, unbounded premium), and the whole band should carry an aspect flag.

---

## 8. Results: aspect overlay and fine slope bins (computed)

The aspect screen shrinks the 15-30% supply by ~1%, not more: south-facing gains
cancel north-facing losses across a band that is 46% E/W-neutral. The spread is
per-acre, not aggregate. `analysis/aspect_slope_bins.py` computes a per-cell
aspect on the same 10 m grid as the slope screen (compass azimuth of steepest
descent from `np.gradient` of the reprojected DEM; South 135-225°, North 315-45°,
Neutral E/W), splits 15-30% into 15-20% (band 4) and 20-30% (bands 5-6), and
POA-weights each (bin x aspect) group by
`data/oahu_poa_aspect_slope.csv` at the bin midpoint (17.5%, 25%). Full table:
`data/oahu_slope_aspect_bins.csv`; figure `analysis/figs/paper/f_slope_aspect_bins.png`.
All-tenure D/E and B/C slope-bin acres reconcile to `data/gis/oahu_lsb_by_slope.csv`
to within 0.1 ac.

POA-vs-flat factors applied (clear-sky, 21.35°N): 15-20% South 1.049 / Neutral
0.994 / North 0.938; 20-30% South 1.062 / Neutral 0.986 / North 0.905.

**Non-military D/E, 15-30% increment (acres):**

| Slope | South | Neutral | North | Total | POA-weighted |
|---|---:|---:|---:|---:|---:|
| 15-20% | 1,139 | 1,996 | 1,158 | 4,294 | 4,267 |
| 20-30% | 2,044 | 3,659 | 2,243 | 7,946 | 7,811 |
| **15-30%** | **3,183** | **5,655** | **3,401** | **12,239** | **12,078** |

**Non-military B/C, 15-30% increment (acres):**

| Slope | South | Neutral | North | Total | POA-weighted |
|---|---:|---:|---:|---:|---:|
| 15-20% | 317 | 617 | 341 | 1,276 | 1,267 |
| 20-30% | 296 | 482 | 271 | 1,049 | 1,035 |
| **15-30%** | **613** | **1,099** | **612** | **2,325** | **2,302** |

Findings (`data/oahu_slope_aspect_bins.csv`):

- **The steeper half dominates.** Of the 12,239 ac non-military D/E increment,
  7,946 ac (65%) is 20-30% slope — the band with no Hawaii cost basis (sec. 4) —
  and 4,294 ac (35%) is the firmer 15-20% band. B/C is more even: 1,276 ac 15-20%,
  1,049 ac 20-30%.
- **Aspect is near-symmetric.** Non-military D/E 15-30% splits South 3,183 ac
  (26%) / Neutral 5,655 ac (46%) / North 3,401 ac (28%). North slightly exceeds
  South. B/C: South 613 ac / Neutral 1,099 ac / North 612 ac. The band is not
  tilted toward good aspect.
- **POA-weighting is close to a wash in aggregate.** Yield-weighting drops the
  non-military D/E 15-30% increment from 12,239 to 12,078 flat-equivalent acres
  (-1.3%); B/C from 2,325 to 2,302 (-1.0%). South gains (+5 to +6%) offset North
  losses (-6 to -9%) because Neutral (near-flat-equivalent) is the largest class.
- **The per-acre penalty is real where it lands.** The ~3,401 ac of north-facing
  D/E 15-30% land is double-marginal: steeper than 15% and facing away from the
  sun (a north-facing 25% acre yields ~9% below flat before any cost premium,
  sec. 2). The ~3,183 ac south-facing fraction is the genuinely attractive tail
  (a south-facing 25% acre roughly matches flat yield). Grade-only screening
  treats these as identical; they are not.

Bottom line: aspect refines but does not overturn the 15-30% supply. It flags
~3,400 ac of north-facing D/E as the weakest acres and ~3,200 ac of south-facing
D/E as the strongest, but the aggregate flat-equivalent supply is within ~1% of
the grade-only figure. The larger qualifier stays the 15-20 vs 20-30 split: two
of every three marginal D/E acres sit in the 20-30% band that carries no Hawaii
cost basis.

## Caveats

1. The Ulupono/Fripp +$0.06-0.07/W factor is a modeling input from developer
   interviews, not a measured EPC cost, and covers only 15-20%. No public
   continuous cost-vs-slope curve exists (inherited from `slope-cost-literature.md`).
2. The aspect table is clear-sky (`analysis/poa_aspect_slope.py`); real Oahu
   cloud cover damps the swings. Magnitudes are ceilings; direction is robust.
   The table is a fixed-tilt geometry; trackers respond via N-S axis grade and
   slope-aware backtracking (§1).
3. 20-30% feasibility leans on one vendor (Nevados) and its own case studies;
   no independent Hawaii cost or performance data.
4. A Hawaii-specific rainfall-erosivity R value per candidate zone, any Oahu
   project on >20% average slope, and a Hawaii fixed-vs-tracker yield delta all
   stayed UNVERIFIED in this sweep.
5. DuraTrack N-S limit sources conflict (15% datasheet vs 26% blog); the
   standard-SAT working envelope is ~15% N-S.

## Follow-on work

1. RESOLVED 2026-07-24 (sec. 8; `analysis/aspect_slope_bins.py`,
   `data/oahu_slope_aspect_bins.csv`, `analysis/figs/paper/f_slope_aspect_bins.png`).
   Per-cell aspect on the 10 m grid splits the 15-30% increment into
   south / neutral / north. Non-military D/E 15-30% = 3,183 S / 5,655 neutral /
   3,401 N (near-symmetric); POA-weighting nets -1.3% (12,239 -> 12,078
   flat-equivalent ac). North-facing ~3,400 ac is the weakest tail, south-facing
   ~3,200 ac the strongest. Reconciles to `oahu_lsb_by_slope.csv` within 0.1 ac.
2. **Soil-erodibility / rainfall-erosivity overlay.** Join NRCS SSURGO K-factor
   and a Hawaii R-factor grid to the 15-30% band to flag acres where
   construction-phase erosion and slope stability, not racking, bind.
3. PARTLY RESOLVED 2026-07-24 (sec. 8). The 15-20% / 20-30% split is now
   quantified per land category: non-military D/E splits 4,294 ac (15-20%) +
   7,946 ac (20-30%), so two of three marginal D/E acres carry no Hawaii cost
   basis; B/C splits 1,276 + 1,049 ac. Remaining: fold the split into
   `docs/ASSUMPTIONS.md` E2 with the Ulupono/Fripp premium on 15-20% and a
   "speculative, no Hawaii basis" flag on 20-30%.
4. **Cross-check with the Switch-Oahu build** in `~/Research/oahu-grid`: the
   Fripp slope cost factors and the ≤15 vs ≤20 slope scenarios are directly
   portable as a sensitivity on land supply and system cost.
5. **PVWatts/SAM validation** of the clear-sky aspect table against a Honolulu
   TMY to replace the clear-sky ceiling with expected-cloud yields.
