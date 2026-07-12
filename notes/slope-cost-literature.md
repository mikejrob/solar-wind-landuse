# Utility-scale solar PV: cost and feasibility vs. terrain slope
## Literature and engineering-spec review

Compiled 2026-07-12 (web research; all URLs live as of that date).
Purpose: ground a cost-vs-slope discussion for the Hawaii ag-land solar paper.
Convention: slopes in **percent grade** unless noted. Conversions used below:
5% = 2.9°, 10% = 5.7°, 15% = 8.5°, 20% = 11.3°, 25% = 14.0°, 30% = 16.7°,
37% = 20.3°. (Percent = 100·tan(degrees); arithmetic mine.)

Headline: the engineering literature supports a three-regime story —
(i) 0–10%: standard practice, near-baseline cost; (ii) 10–20%: buildable with
terrain-following trackers or fixed tilt at a real but mostly *unpublished*
cost premium (grading, erosion control, or specialty racking); (iii) >20%:
technically demonstrated in a handful of projects up to ~25–30% with
zero-grading terrain-following racking, but outside standard developer
screens; >30–37% is beyond every mainstream ground-mount spec.
**No published continuous cost-vs-slope curve exists in the public
literature.** Anyone (including us) presenting per-5-pp cost increments is
interpolating; flagged below.

---

## 1. Slope limits in actual practice

### 1.1 Developer screening / siting-model thresholds

- **EPA (2022), Best Practices for Siting Solar PV on Municipal Solid Waste
  Landfills** (p. 28): "Most solar developers place an upper limit of **5–10
  percent grades** in considering the feasibility of installing a PV system on
  a slope. Steep slopes represent system design challenges associated with
  wind loading, erosion and foundation stability and associated higher system
  installation costs." Landfill top decks of 2–3% called "ideal"; perimeter
  side slopes of "3:1 slope or 30+ percent grade" treated as requiring
  alternatives (e.g., PV-integrated geomembranes).
  https://www.epa.gov/system/files/documents/2022-05/best-practices-siting-solar-photovoltaics-municipal-solid-waste-landfills_051722-pub.pdf
  (verified against PDF text, §4.2.2.3)
- **NREL reV siting regimes** (as documented in NREL/TP-6A20-87524, Feb 2024,
  pp. 9–10, which applies the standard reV utility-PV regimes): *Reference
  Access* uses "a **10% slope restriction** ... to prevent complicated racking
  needs"; *Limited Access* applies "stricter slope requirements (**0%–5%**)."
  *Open Access* (technical-potential ceiling) has no slope screen.
  https://www.nrel.gov/docs/fy24osti/87524.pdf (verified against PDF text).
  Same regimes underlie the U.S. Utility-Scale PV Supply Curves 2023/2024
  datasets: https://data.openei.org/submissions/6001 ,
  https://data.openei.org/submissions/8319
- **GIS siting literature**: typical recommendation is flat or gently
  south-facing terrain **<5%** for large plants (e.g., Gacu et al.-type
  territory analyses; see Springer, Environ. Monit. Assess. 2019,
  https://link.springer.com/article/10.1007/s10661-019-7871-8 ).
  Individual studies use 3–11% cutoffs; 5% is modal. (Characterization mine
  from the search sweep; individual thresholds vary.)

**Implication for the paper:** the standard *screening* envelope (≤5–10%) is
much tighter than the *engineering* envelope (≤15% standard trackers, ≤37%
specialty; §1.2–1.4). The gap between the two is exactly where a cost
gradient, not a feasibility cliff, lives.

### 1.2 Standard single-axis trackers (SAT)

Rows run N–S and rotate E–W. Two distinct slope directions matter:
- **Axis (N–S) slope** — tilts the torque tube; limited by drive/bearing spec.
- **Cross-axis (E–W) slope** — rows step down the hill independently; more
  forgiving structurally but complicates backtracking/shading (§3).

Specs (manufacturer claims, not independent tests):
- **Array Technologies DuraTrack HZ v3**: up to **15% slope in the N–S
  (axis) plane** and up to 40° combined E–W articulation at driveline joints.
  One vendor page cites up to 26% N–S "grades" — sources conflict; 15% is the
  datasheet-consistent number. (Datasheet via NY DPS filing:
  https://documents.dps.ny.gov/public/Common/ViewDoc.aspx?DocRefId=%7B16EDED2C-4CBA-4199-BA7E-448D67909D74%7D ;
  https://arraytechinc.com/products/duratrack/ ;
  https://arraytechinc.com/blog/terrain-flexibility-with-duratrack/ )
- **Nextracker NX Horizon (standard)**: designed for "flat and relatively
  flat" sites; conventional SATs "require that the torque tube extend north
  and south along a single plane" (PV Tech interview with Nextracker,
  https://www.pv-tech.org/terrain-following-tracker-nextrackers-revolutionary-nx-horizon-xtr-is-key-to-unlocking-challenging-sites/ ).
  Industry shorthand of "~8–15% N–S tolerance" for standard SATs is
  consistent with these specs but is not a single citable datasheet number —
  treat the 15% DuraTrack figure as the documented upper end.

### 1.3 Terrain-following trackers

- **Nextracker NX Horizon-XTR** (launched 2022): undulation tolerance
  **0.75° between piles**, total slope tolerance **8.5° (= 15% grade)**;
  claims 30–90% less cut-and-fill vs. standard SAT on undulating sites,
  1,000–3,000 yd³/MW grading avoided, 5,000–9,000 lb/MW foundation-steel
  savings, piers up to 36 in. shorter, up to 5 acres/MW less land
  disturbance; >3 GW deployed by 2023.
  (Solar Power World 2023-01:
  https://www.solarpowerworldonline.com/2023/01/single-axis-trackers-upgrade-to-handle-uneven-land-sites/ ;
  PV Tech: https://www.pv-tech.org/terrain-following-tracker-nextrackers-revolutionary-nx-horizon-xtr-is-key-to-unlocking-challenging-sites/ ;
  press release: https://www.nextracker.com/press-release/nextracker-unveils-nx-horizon-xtr-terrain-following-solar-tracker/ )
- **Array Technologies OmniTrack**: post-to-post slope change 1° (2023
  version) doubled to **2° post-to-post** in the June 2026 update; marketed
  as minimizing grading. (GlobeNewswire 2026-06-01:
  https://www.globenewswire.com/news-release/2026/06/01/3304438/0/en/ARRAY-Technologies-Announces-OmniTrack-Update-with-Greater-Terrain-Following-Capability.html )
- **Nevados All Terrain Tracker / TRACE**: the aggressive end of the market —
  **maximum slopes up to 37% (20°) in any direction**, pile-to-pile
  articulation up to **15° (26%)**, designed for **zero grading**.
  (https://nevados.solar/ ; product page https://nevados.solar/product/ ;
  datasheet https://nevados.solar/wp-content/uploads/2023/12/Nevados_Structure_Controls_Combined_120723_updated.pdf ;
  PV Tech: https://www.pv-tech.org/the-end-of-mass-grading-for-solar-projects/ )
- Built precedents (Nevados case studies — vendor-reported, so treat as
  favorable-case): **Sarish Solar**, Burgettstown PA, on a former coal-waste
  mine with "highly erosive 30% slopes, rock ledges"; installer "conquered
  20% slopes"; follow-on PA projects planned at **25% slopes with zero
  grading** except roads. (https://nevados.solar/featured-projects/sarish-case-study/ ;
  https://nevados.solar/wp-content/uploads/2025/05/Sarish-Case-Study-1.pdf ).
  **Iris Solar**, Louisiana: 13 MW of Nevados trackers within a 50 MW plant
  cut grading and disturbed acreage by 95% vs. conventional 1P trackers
  (PV Tech link above).

### 1.4 Fixed tilt, ballasted, and specialty systems

- **Fixed tilt** tolerates steeper ground than SAT because there is no
  torque tube to keep aligned; no single industry-wide max-slope datasheet
  number surfaced. Documented bounds: ballasted (non-penetrating) racking is
  "only suitable for slopes up to about a **15 percent** incline"
  (Waste360, landfill-solar engineering discussion,
  https://www.waste360.com/landfill-operations/are-there-solutions-landfill-slopes-challenge-solar-projects );
  landfill side slopes of **3:1 (33%)** have been panelized only with
  specialty solutions (PV-integrated geomembranes, per EPA 2022 above;
  ICEG 2023 case studies:
  https://www.issmge.org/uploads/publications/116/117/ICEG2023-235.pdf ).
- **Alpine/extreme demonstrations** (existence proofs, not cost-relevant
  comparators): AlpinSolar — ~5,000 panels bolted to the Muttsee dam face at
  2,500 m, components flown in by helicopter (Axpo,
  https://www.axpo.com/ch/en/energy/generation-and-distribution/solar-power/alpinsolar.html );
  Gondosolar — 4,500 panels on ~10 ha of steep alpine hillside, viable only
  with Swiss federal subsidies of up to 60% of investment cost
  (https://www.swissinfo.ch/eng/sci-tech/mountaintop-solar-farms-spark-tensions-in-switzerland/47968044 ).
  Useful rhetorical bound: panels can be mounted on near-vertical faces —
  slope is a *cost* variable, not a hard feasibility wall, until machinery
  access and geotechnical limits bind.

---

## 2. Cost gradients: what is actually published

### 2.1 NREL bottom-up cost benchmarks do NOT include a slope/terrain axis

NREL's U.S. Solar PV System Cost Benchmark (Q1 2022, NREL/TP-7A40-83586;
same structure in later editions) itemizes utility-scale site preparation
(geotechnical investigation; clearing and grubbing; soil stripping and
stockpiling; **grading**; compaction) for a single reference project, and
explicitly treats "additional land grading" due to "site irregularities" as a
*market-price distortion to be removed* from its minimum-sustainable-price
benchmark. I found **no terrain or slope multiplier anywhere in the NREL
benchmark or ATB structure** — the benchmark is a flat-reference-site number.
(https://docs.nrel.gov/docs/fy22osti/83586.pdf , verified against PDF text;
ATB: https://atb.nrel.gov/electricity/2024/utility-scale_pv ).
Likewise, NREL's supply-curve work handles slope as a binary *exclusion*
(§1.1), not a cost adder. **Consequence: the flagship U.S. public cost models
are silent on the cost-vs-slope gradient** — a genuine gap worth stating in
the paper.

### 2.2 Site-work and grading cost magnitudes (fragmentary, mostly gray literature)

- Site work (clearing, grading, roads, erosion control) **$12,000–$40,000/acre**;
  grading alone for "a sloped 30-acre site" **$150,000–$400,000**; costs driven
  by slope, drainage, and interconnection distance (Renpro, NY-focused
  contractor guide, 2025–26: https://renpro.org/solar-farm-site-work-cost-new-york/ ).
  DERIVED (mine): at ~5–7 acres/MWac, the grading figure is roughly
  **$25,000–$90,000/MW ≈ $0.03–$0.09/Wac**, i.e., ~2–8% of a ~$1.1/W plant —
  for a *moderately* sloped site. UNVERIFIED beyond the single source;
  use as order-of-magnitude only.
- Land clearing $1,500–$8,000+/acre depending on vegetation (OWNR OPS guide:
  https://www.ownrops.com/guides/land-clearing-for-solar-farms ); the same
  guide attributes to NREL the claim that civil construction incl. grading is
  "15–20% of total solar project costs" — I could not trace that to a primary
  NREL document; treat as Tier-3/UNVERIFIED.
- Grading volumes on rolling terrain are enormous: a University of Michigan
  study of six California projects reportedly found none below 1,000,000 yd³
  of earthwork, max >8,000,000 yd³ (cited in PVfarm blog:
  https://www.pvfarm.io/blog/integrated-solar-grading-optimization-software —
  secondary; primary study not located; UNVERIFIED).
- Grading-optimization example (software vendor, favorable case): site with
  44% hard rock and local slopes of 40–45% — full-terrain smoothing 118,225 m³
  vs. pile-adaptive grading 34,819 m³ of cut: **70% less earthwork, $727k
  saved** (PVX/PVcase comparison writeup:
  https://pvx.ai/blog/solar-design-software-comparison/ ; also
  https://pvcase.com/blog/advancing-solar-projects-with-ground-grading ).
- Terrain-following tracker savings (vendor claims, §1.3): XTR 1,000–3,000
  yd³/MW avoided; "savings in the millions" on select projects. DERIVED
  (mine): at typical bulk-earthwork rates of $5–15/yd³ this is
  ~$5,000–$45,000/MW (**$0.005–$0.045/W**) of avoided grading — the unit rate
  is my assumption, UNVERIFIED; Hawaii rock excavation would sit above the
  top of that range.
- Stormwater compliance: "US solar projects subject to Stormwater Pollution
  Prevention Plan requirements average an additional cost of **$0.75 per
  watt**" — attributed to EPC firm Primoris in PV Tech
  (https://www.pv-tech.org/the-end-of-mass-grading-for-solar-projects/ ).
  This figure looks implausibly high as a pure-SWPPP increment (it is ~2/3 of
  total plant capex); likely includes broad civil scope or is a misquote.
  FLAGGED — do not use without corroboration.
- Peer-reviewed grading-optimization literature exists but reports volumes,
  not $/W-vs-slope: e.g., quadratic-programming field leveling (Results in
  Physics/Heliyon-family, 2024:
  https://www.sciencedirect.com/science/article/pii/S2211379724004753 );
  patents on tracker cost-optimization vs. terrain (US 11,301,790;
  US 12,249,951). None yields a usable cost-vs-slope curve.

### 2.3 O&M and lifecycle implications of slope (qualitative only)

- Erosion control on slopes steeper than 3:1 (33%) requires erosion-control
  blankets; steep sites need clearing sequencing, micro-terracing, rapid
  re-seeding; "reactive cleanup is often 5 to 10 times the cost" of upfront
  vegetation management (OWNR OPS; GreenLancer:
  https://www.greenlancer.com/post/erosion-control-solar-farms ; NREL
  vegetation-management cost study, NREL/TP-85418:
  https://docs.nrel.gov/docs/fy23osti/85418.pdf — the NREL study costs ground
  covers, not slope per se).
- Korea's mountainside plants (installed on graded forest slopes) suffered
  repeated rainfall-triggered landslides 2018–2020, spawning a
  landslide-susceptibility literature specific to PV-on-slopes (Landslides,
  2023: https://link.springer.com/article/10.1007/s10346-023-02077-9 ;
  Nat. Hazards 2025: https://link.springer.com/article/10.1007/s11069-025-07579-4 ).
  Korea reportedly tightened its forestland-solar slope standard from 25° to
  15° average slope in Dec. 2018 (Enforcement Decree, Mountainous Districts
  Management Act) — consistent with the NABO setback-regulation review
  (https://korea.nabo.go.kr/naboEng/cmmn/file/fileDown.do?atchFileId=6526604f2d194900b93f00cfee651fbb&fileSn=1 )
  but the 25°→15° figure itself is UNVERIFIED (not confirmed in an
  English-language primary source in this sweep).
- Japan: the July 2021 Atami debris flow (27 dead) — caused by an improper
  fill mound upslope of, not by, an adjacent hillside solar site — triggered
  national re-regulation of slope-sited solar and ≥175 municipal ordinances
  restricting "mega-solar," many keyed to landslide-warning zones.
  (EnergyTrend 2021-08: https://m.energytrend.com/news/20210810-22918.html ;
  Japan Times 2024-05-26:
  https://www.japantimes.co.jp/environment/2024/05/26/energy/megasolar-opposition-solutions/ ;
  Renewable Energy Institute recommendation:
  https://www.renewable-ei.org/pdfdownload/activities/REI_Recommendation_SustainableSolarDevelopment_EN.pdf )
  Lesson for the paper: above ~15–20%, the binding constraint shifts from
  racking engineering to **geotechnical risk and social license**.

---

## 3. Direction/aspect effects (relevant at 21°N)

- **Which slope direction matters**: for SAT, the *axis* (N–S) slope is the
  hard spec (§1.2); *cross-axis* (E–W) slope is absorbed row-by-row but
  degrades standard backtracking — rows on cross-axis slopes shade each other
  unless slope-aware backtracking is used. Closed-form corrections exist and
  are now standard in pvlib/SAM (Anderson & Mikofski, *Slope-Aware
  Backtracking for Single-Axis Trackers*, NREL/TP-5K00-76626, 2020:
  https://www.osti.gov/biblio/1660126 ; SAM forum discussion:
  https://sam.nrel.gov/forum/forum-general/3747-photovoltaic-system-design-terrain-slope.html ).
  With the correction, residual yield loss from moderate cross-axis slope is
  small; without it, shading losses are material (paper derives geometry;
  percent-loss magnitudes are configuration-specific — no single number to
  quote).
- **Aspect (fixed tilt)**: developers prefer slopes facing "south, or within
  20–30 degrees of due south" (EPA 2022, §4.2.2.3, link above). North-facing
  fixed arrays produce roughly 60–80% of equivalent south-facing output in
  U.S. mid-latitudes (rooftop evidence: Solar Power World 2016:
  https://www.solarpowerworldonline.com/2016/06/much-less-efficient-north-facing-solar-modules/ ;
  SolarReviews: https://www.solarreviews.com/blog/best-direction-orientation-solar-panels ).
- **Hawaii-specific inference (REASONED, not sourced)**: at 21°N the sun is
  high year-round (max winter-solstice noon elevation ≈ 45°), so the yield
  penalty of a given north-facing ground slope is smaller than the
  mid-latitude figures above, and a south-facing slope adds effective tilt
  toward the ~21° latitude optimum. A 10–20% (5.7–11.3°) south-facing slope
  is a mild yield *benefit* for fixed tilt; the same slope north-facing costs
  single-digit to low-teens percent for fixed tilt (PVWatts-type modeling
  needed to pin down — flag as to-do; do not cite numbers yet).

---

## 4. Hawaii construction and permitting specifics

- **Built practice (Oahu/Big Island, Goodfellow Bros. via Solar Builder)**:
  Kawailoa Solar (49 MW, 2019): ~110 acres cleared, **130,000 yd³ moved**,
  4 mi rock driveways, 1.5 mi of swales — i.e., ~2,650 yd³/MW on ordinary
  rolling ag land, comparable to the *entire* savings XTR claims per MW.
  Waianae (2016, 198 ac): coral/boulder subsurface, ~20% pile refusals until
  pre-drilling adopted. Waikoloa (300 ac): rock-laden terrain.
  (https://solarbuildermag.com/mounting-solutions-guide/constructing-solar-farms-in-hawaii-is-not-easy-heres-how-goodfellow-bros-gets-it-done/ ;
  https://www.ecmweb.com/renewables/article/21139333/high-profile-green-projects-power-america-kawailoa-solar-waipio-solar-and-mililani-solar-ii-projects )
  Note: these are *benign-slope* sites; Hawaii's cost premium there is rock
  and labor, not slope. No Hawaii utility-scale project on >15% average
  slope surfaced in this sweep.
- **Kauai SP26-416 (Ka'awanui Solar, 2026 special-permit application)**
  states design "focus on minimizing the extent of grading" given site
  topography — an example of slope shaping Hawaii project design within the
  SUP record the project is already mining.
  (https://files.hawaii.gov/luc/dockets/sp26-416/2026-05-04-COK-SP-Exhibit-03.pdf )
- **Honolulu grading rules (ROH ch. 14 / DPP Grading Permit Procedures,
  rev. July 2024 — verified against the DPP PDF)**:
  - Grading permit generally required; **engineer's soils report required
    when grading is on land with existing slopes exceeding 15 percent** (also
    for cut/fill >15 ft single-family / >7.5 ft other uses, fill over
    gullies/wetlands, plastic-clay fill, or structural fill).
  - **Engineering slope-hazard report** required for cuts >15 ft on grades
    **steeper than 40 percent**.
  - Erosion & Sediment Control Plan required per the city "Rules Relating to
    Water Quality" (eff. 2018-12-24); **NPDES NOI to the State DOH for ≥1
    acre of disturbance** (any utility-scale project qualifies); maximum
    cut/fill slope ratios per Table A; grading bond for >500 yd³ or cut/fill
    >15 ft.
  (https://www.honolulu.gov/dpp/wp-content/uploads/sites/56/2024/07/grading_permit_procedures.pdf ;
  code: https://codelibrary.amlegal.com/codes/honolulu/latest/honolulu/0-0-0-9472 )
  So on Oahu, **15% existing slope is a bright regulatory line** (soils
  report → cost/time adder) and **40% a second line** (slope-hazard report);
  neither is a prohibition.

---

## 5. Summary table: feasibility and cost premium by slope band

Feasibility codes: Y = standard practice; C = conditional/at spec limit;
S = specialty equipment only; N = no documented utility-scale practice.
"Std SAT" = conventional single-axis tracker; "TF SAT" = terrain-following
tracker (XTR/OmniTrack at the mild end, Nevados at the steep end); "FT" =
fixed tilt (driven pile; ballasted is stricter, ≤~15%).
Cost premiums are vs. an equivalent flat site, **capex basis**; the
literature does not support precise increments — entries marked (D) are my
derived order-of-magnitude readings of §2, not published numbers.

| Slope band | Std SAT | TF SAT | FT | Indicative capex premium vs. flat | Binding constraints / notes |
|---|---|---|---|---|---|
| 0–5% | Y | Y | Y | ~0 (reference-site conditions; NREL benchmarks assume this) | None; NREL "Limited" siting screen confines to here (0–5%) |
| 5–10% | Y (within DuraTrack 15% N–S spec) | Y | Y | Low single digits % of capex (D): grading/site work $12–40k/ac at the low end; slope-aware backtracking needed on cross-axis slopes | Upper edge of typical developer screens (EPA: "most developers cap at 5–10%"); NREL "Reference" screen cuts at 10% |
| 10–15% | C (at/near spec limit: DuraTrack 15% N–S; XTR total 8.5° = 15%) | Y | Y | Mid single digits % (D): either mass grading (~$0.03–0.09/W grading alone, per §2.2, UNCERTAIN) or TF-racking premium (unpublished) | Honolulu: >15% existing slope triggers soils report; erosion-control intensity rises |
| 15–20% | N (beyond std specs) | Y (Nevados spec 37%; built at 20% — Sarish PA) | C (site-specific geotech) | Not published. Components: TF racking premium (unpublished), +erosion/stormwater, +access roads; grading largely avoided by design | Feasibility now vendor-specific; aspect matters more for FT (south-facing favorable at 21°N) |
| 20–25% | N | C (planned PA projects at 25%, zero grading — vendor-reported) | S | Not published; single-project anecdotes only | Construction access, erosion (blankets required >3:1 nearby band), geotechnical review |
| 25–30% | N | C (within Nevados 37% spec; no completed utility-scale precedent found at >25% average) | S (landfill 3:1 = 33% side slopes done only w/ specialty systems) | Not published; expect premium dominated by civil/erosion/O&M, not racking | Korea landslide record is the cautionary case for graded slopes in this band; social license/permitting risk |
| >30% | N | N (beyond all specs except Nevados max-37% edge) | S (niche: geomembrane PV, alpine dam-face/heli-build) | Effectively unbounded (alpine builds needed ~60% subsidies) | Treat as infeasible for cost modeling of utility-scale PV; existence proofs only |

Reading for the paper: a defensible econometric treatment is a **step
function** — near-zero premium to ~10%, a modest and rising premium 10–20%
(the literature cannot separate 10–15 from 15–20 with published numbers),
a large and uncertain premium 20–30% resting on one vendor's technology,
and a wall above ~30%. Mike's "viable to ~30% with sharply rising cost"
prior is *consistent with* the engineering record (Nevados spec 37%, built
20%, planned 25%), but the *standard-practice* envelope that disciplines
land-supply calculations is 0–10%, extending to ~15% with current
mainstream terrain-following trackers.

---

## 6. Caveats and gaps

1. **No public cost-vs-slope curve exists**; all premium figures above are
   assembled from contractor guides, vendor claims, and one software-vendor
   case study. NREL/LBNL benchmarks are flat-site by construction.
2. Steep-slope feasibility claims ≥20% rest heavily on **one vendor
   (Nevados) and its own case studies**; independent performance/cost data
   not found.
3. The Primoris "$0.75/W SWPPP" figure and the "civil = 15–20% of project
   cost (NREL)" claim are **uncorroborated** — do not cite without tracing.
4. Korea's 25°→15° forestland slope tightening is **UNVERIFIED** in primary
   English sources; the landslide events themselves are peer-review
   documented.
5. Hawaii-specific: no utility-scale project on >15% average slope found;
   Hawaii's documented premia are rock/pile-refusal and labor, which would
   **compound** any slope premium. PVWatts/SAM modeling of aspect effects at
   21°N is a cheap, doable next step to replace the reasoned inference in §3.
