# Steep-slope utility PV outside Hawaii: built precedent and cost

Compiled 2026-07-24 (web research; all URLs live as of that date). This note
answers a question the Hawaii-specific notes could not: is there real-world
precedent for utility-scale (≥1 MW) solar PV built on 20-30%+ average slopes in
geographies like Hawaii — tropical/subtropical, island, volcanic, steep, high
rainfall — and at what cost? It extends `notes/slope-15-30-challenges.md` (which
found no completed Hawaii project above ~20% average slope, and only vendor
Nevados claiming 37%) and `notes/slope-cost-literature.md` (the "no published
cost-vs-slope curve" gap). Do not re-read those for the vendor tracker specs or
the Ulupono/Fripp +$0.06-0.07/W Hawaii number; they are covered there.

**Unit warning.** Hawaii notes use percent grade; the Asian programs regulate in
degrees. Both appear below. Conversions (percent = 100·tan°): 15° = 27%,
20° = 36%, 25° = 47%, 30° = 58%. So Korea's "15° slope limit" is a **27% grade**,
and Japan's "30° retaining-wall trigger" is a **58% grade** — both far steeper in
grade terms than the 20-30% grade the Hawaii question frames.

## Headline

Yes, utility-scale PV has been built well above 20-30% grade — but the firmest
evidence comes from South Korea and Japan, where slopes hosting solar plants
repeatedly failed in monsoon rainfall, and **no single project on the record
pairs a verified >20%-grade average slope with a published capex.** The two
things never travel together.

**Causation caveat up front (see the dedicated section below).** "Solar-site
slopes failed" is well documented; "solar *caused* the failures" is only
partly established. The land-clearing/earthworks mechanism is textbook-solid
and two governments re-regulated on it, but there is **no comparative study
showing solar slopes fail at higher rates than matched non-solar slopes**, and
the most-cited events are co-location or single-site forensics, not attribution
against a counterfactual. Do not write that "solar farms landslide"; write that
solar development on cleared, cut-and-filled steep wet slopes carries a
landslide mechanism that has repeatedly manifested where standards were loose.

1. **Steepest verifiably-built average slope, non-vendor source: South Korea,
   ~15-25° (27-47% grade).** A Korea Forest Service survey of 1,235 mountain
   solar plants permitted 2014-2018 found **665 (48.6%) sat on slopes steeper
   than 15° (27% grade)** — 425 at 15-20° (27-36%), 120 at 20-25° (36-47%)
   (http://www.besteco.kr/news/articleView.html?idxno=6114). These are regulatory-
   survey averages, not vendor claims. **No capex attaches to any of them.**
2. **Best cost-with-capacity pairing on a tropical hillside: ~$0.85/W EPC
   (Cayanga, Philippines, 94 MWp, ₱4.5B EPC)** — but its slope is never
   quantified in any accessible source, so it is a cost anchor without a verified
   slope (https://www.pv-magazine.com/press-releases/aboitizpower-begins-work-on-94-mw-solar-park/).
3. **The vendor ceiling (Nevados/terrain-following trackers to 37%) rests on the
   same case studies already in `slope-cost-literature.md`;** the steepest
   *built* Nevados number is ~20% grade (Sarish, PA), developer-reported, capex
   undisclosed.
4. **Tropical volcanic islands (Reunion, Canaries, Madeira, Caribbean) offer no
   steep-slope utility PV.** Land-scarce islands retreat to coastal flats, ex-
   dumps, and mid-slope terraces; Reunion explicitly sites solar "between the
   coast and mid-slopes" and excludes the steep volcanic interior
   (https://www.pv-magazine.fr/2021/06/30/serie-dom-tom-la-reunion-veut-plus-que-doubler-sa-capacite-solaire-dici-2028/).
   The only *measured* hillside utility PV on a tropical volcanic island in the
   corpus is Hawaii's own AES West Oahu at ~15% grade (`slope-15-30-challenges.md` §6).

The transferable lesson for Hawaii is a hazard lesson, not a cost lesson: the
places that actually built utility PV on 27-47%-grade slopes (Korea, Japan) are
humid, steep, high-rainfall, seismic analogs, and they are exactly where slope-
sited PV has seen its slopes fail (Hoengseong 2022, 1 dead) and been re-regulated
down. (The larger death tolls often cited alongside — Atami's 26-28 — were NOT
solar failures; see the causation section.)

---

## Did solar cause the landslides? (causation assessment)

**Bottom line.** The *mechanism* by which solar development can trigger shallow
landslides on steep wet slopes is well established and old — but *rigorous causal
attribution to solar specifically* is thin. What the record supports, ranked from
strongest to weakest evidence: (1) the general land-clearing/earthworks mechanism
is textbook geoscience; (2) two governments acted on it by re-regulating slope-
sited solar; (3) individual solar-site failures have been reverse-engineered as
single-site forensics, some initiating in the plant's own cut-and-fill embankment;
(4) **no comparative or statistical study anywhere shows that slopes with solar
fail at a higher rate than comparable slopes without solar**, controlling for
grade, rainfall, and geology. Claim (4) is the causation crux and it is missing.
So the honest statement is: *the mechanism is sound and governments acted on it,
but a rigorous causal test against a counterfactual has not been published.*

### The four confounds, ranked by how well the evidence supports them

For any observed failure at a solar site, four non-exclusive explanations
compete. Ranked by evidentiary support:

- **(c) Illegal or substandard grading/fill — best supported where failures were
  actually investigated.** The paradigm is Atami/Izusan (3 Jul 2021, 26-28 dead):
  Shizuoka Prefecture and the Forestry Agency found the cause was an illegal
  ~54,000 m³ (>50 kt) fill mound with no drainage, and Vice-Governor Namba stated
  plainly that "solar energy and residential development are not the cause of the
  incident, as indicated by the available geological data"
  (https://m.energytrend.com/news/20210810-22918.html). Atami is thus a
  **counter-example to solar causation**, yet it was the political trigger for
  Japan's re-regulation. Korea's mountain-solar failures likewise cluster at
  sites built to loose pre-2018 standards with cut-fill embankments and
  inadequate drainage — an earthworks-quality story, not a "PV hardware" story.
- **(b) Deforestation for solar (root-cohesion loss) — strongest MECHANISTIC
  basis, not isolated empirically at solar sites.** Clearing forest on steep
  slopes removes root reinforcement and is one of the best-documented
  anthropogenic landslide drivers (see root-cohesion literature below). Solar
  inherits this mechanism at the land-clearing step, independent of the racking.
  Highly plausible for cleared forest-solar sites; but no study isolates the
  deforestation contribution at solar sites from the earthworks or the rainfall.
- **(d) Exposure of pre-existing hazard slopes — well documented as co-location.**
  Hao, Ialnazov & Yamashiki (2021) find 8.5% of mapped Japanese PV sites sit
  inside designated sediment-hazard zones; siting on already-hazardous ground
  produces failures at solar sites without solar having caused anything
  (https://www.frontiersin.org/articles/10.3389/frsus.2021.815986/full).
- **(a) Properly-engineered PV on a steep slope failing because it is PV — least
  supported.** The failures on record are associated with loose-standard
  construction and cut-fill embankments, not with well-engineered, well-drained
  installations. Nothing in the record shows that competent steep-slope PV
  inherently slides.

Net: the evidence best supports that failures were driven by **land clearing +
earthworks/drainage on already-marginal steep wet slopes** — the site-preparation
of solar, not the panels. This is a real hazard and it transfers to Hawaii's wet
erodible uplands, but it is a construction-and-siting hazard, not a property of
generating electricity from sunlight.

### The authoritative studies and what each actually establishes

Verified to exist; each read for whether it shows CAUSATION (mechanism +
counterfactual) or only exposure/damage/single-site forensics.

- **Nam, K., Wang, F., Dai, Z. et al. 2023, "Kinetic characteristics and runout
  behavior of the rainfall-induced Hoengseong landslide at a solar power plant on
  9 August 2022," *Landslides* 20:1905-1923** (https://link.springer.com/article/10.1007/s10346-023-02112-9).
  Single-site forensic of ONE failure. The abstract states the slope "failed at
  the embankment of the solar power plant and subsequently transited to a high-
  mobilized debris flow" — i.e., initiation in the plant's engineered embankment,
  which is the closest thing in the peer-reviewed record to attributing a failure
  to solar earthworks. But it is a runout/kinematics model (PFC3D), n = 1, **no
  counterfactual and no comparison to non-solar slopes.** Establishes: co-location
  + failure located in a constructed feature. Does NOT establish a causal rate.
- **Lee et al. 2023, "Preliminary analysis of a heavy rainfall-induced landslide
  on a slope with a photovoltaic power station in Hoengseong County," *Landslides*
  20:1763-1767** (https://link.springer.com/article/10.1007/s10346-023-02077-9).
  A 4-page "Landslide News" short communication on the same 2022 event, not a full
  research study; its reference list cites a KBS News (2022) item titled "The
  Hoengseong landslide caused by solar power plant" — i.e., it relays MEDIA
  attribution. Weak as causal evidence.
- **Hao, K., Ialnazov, D. & Yamashiki, Y. 2021, "GIS Analysis of Solar PV
  Locations and Disaster Risk Areas in Japan," *Frontiers in Sustainability*
  2:815986** (https://www.frontiersin.org/articles/10.3389/frsus.2021.815986/full).
  EXPOSURE study only. Its own framing treats plants as vulnerable entities; the
  "11 plants damaged by landslides" and "782/9,250 (8.5%) in hazard zones" are
  co-location and damage counts. **Explicitly not a causal claim.** This is the
  source the earlier note leaned on; it does not support "solar triggered
  landslides."
- **Cheon, E., Yu, J.Y., Lim, H.H., Lee, S.R., Kwon, T.H. & Song, K.I. 2025,
  "Physics-based landslide susceptibility machine learning model for mountainous
  solar power plants," *Natural Hazards* 121:19967-19992** (https://link.springer.com/article/10.1007/s11069-025-07579-4).
  A physics-informed ML model built from 136,262 rainfall-infiltration/slope-
  stability simulations that "account for the presence of solar panels," validated
  at one real solar site (Jangsu-gun). This is the most mechanistic solar-specific
  work, but it is **simulation-based susceptibility mapping, not an empirical
  comparison of solar vs bare-slope failure rates**; its sensitivity analysis
  finds soil-strength properties dominate the factor of safety. It does not
  isolate a "panels present raises failure rate" result.
- **Kim et al. 2023, "Landslide risk on photovoltaic power stations under climate
  change," *Geomatics, Natural Hazards and Risk* 14(1):2286904** (https://www.tandfonline.com/doi/full/10.1080/19475705.2023.2286904).
  Susceptibility + physical hazard model projecting risk to PV stations under RCP
  scenarios; ~**$60 million/yr** expected loss under RCP6.0. A forward risk
  projection AT PV sites, not a causal attribution against non-solar controls.
  (Companion susceptibility studies: Gangwon-do PV susceptibility, *Geomatics NH&R*
  2021, https://www.tandfonline.com/doi/abs/10.1080/19475705.2021.1950219; and a
  dynamic-rainfall PV risk model, *Water* 2023, https://doi.org/10.3390/w15152832.
  All map/rank susceptibility at solar sites; none is a matched-control comparison.)

### The comparative/statistical test (the causation crux) — MISSING

No located study asks the decisive question: **do slopes hosting solar fail at a
higher rate than comparable slopes without solar, holding grade, rainfall, and
geology fixed?** The Korean and Japanese solar-landslide papers are single-site
forensics (Nam; Lee), exposure/co-location maps (Hao et al.), or simulation-based
susceptibility models (Cheon; Kim) — none constructs a matched non-solar control
group. The nearest thing to a rate statement is the Korean government's own
denial: MTIE noted the 12 landslide-hit solar sites were 0.1% of 12,721 solar
facilities (https://www.koreatimes.co.kr/www/opinion/2020/12/202_294318.html) —
but that is a raw fleet rate on an ill-chosen denominator (most of the fleet is
not on steep forest slopes) with no matched control, so it neither confirms nor
refutes causation. **State this gap plainly wherever the paper uses Korea/Japan.**

### Government attributions — regulatory action, not per-site forensics

- **Korea 2020:** the Korea Forest Service reported 12 solar sites among ~1,100
  monsoon landslides; opposition parties blamed the Moon administration's mountain-
  solar push, and the Ministry of Trade, Industry and Energy publicly rejected the
  causal claim (0.1%-of-fleet argument above). Korea nonetheless tightened the
  average-slope limit from <25° to <15° and cut the REC multiplier in 2018. The
  regulatory action reflects precautionary concern and politics; it is **not a
  government finding that solar construction mechanically caused each failure.**
- **Japan 2018/2021:** the "11 plants" figure is damage/co-location (Hao et al.);
  the Forestry Agency/METI tightened forest-development permit criteria (retaining
  walls ≥30°, permit trigger cut 1 ha → 0.5 ha) as prevention. For Atami — the
  event that actually drove Japan's re-regulation — the government finding was
  **explicitly that solar was not the cause** (illegal fill). So Japan re-regulated
  solar off the back of a failure it had itself attributed to something else.

### Root-cohesion / deforestation literature (the transferable mechanism)

The general, non-solar evidence that clearing forest on steep slopes raises
shallow-landslide risk is strong and decades old, and it is the mechanism that
transfers to solar via land clearing — independent of the racking:

- **Sidle, R.C. & Ochiai, H. 2006, *Landslides: Processes, Prediction, and Land
  Use*, AGU Water Resources Monograph 18** (https://agupubs.onlinelibrary.wiley.com/doi/book/10.1029/WM018)
  — the standard synthesis; documents that timber harvest, forest conversion, and
  road building drive shallow landslides, with root reinforcement often more
  important than hydrologic effects.
- **Sidle, R.C. 1992, "A theoretical model of the effects of timber harvesting on
  slope stability," *Water Resources Research* 28(7):1897-1910** (https://agupubs.onlinelibrary.wiley.com/doi/10.1029/92WR00804)
  — the root-decay/regrowth model. Field syntheses report **2- to 10-fold
  increases in mass-erosion rates in the 3-15 years after clearing**, the window
  when decayed roots no longer reinforce and regrowth has not yet compensated
  (root cohesion <3 kPa for ~7 years; >10 kPa only after ~9 years).
- **Lehmann et al. 2019, "Deforestation Effects on Rainfall-Induced Shallow
  Landslides," *Water Resources Research* 55** (https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2019WR025233)
  — physically-based modeling: simulated cumulative landslide area rose from
  ~8,000 m² with root regrowth to ~40,000 m² with zero root strength after
  deforestation, a ~5× effect from clearing alone.

This literature is the reason the solar mechanism is credible even though solar-
specific causal tests are thin: a solar project that clears forest on a steep wet
slope inherits a well-quantified landslide mechanism at the clearing step. The
gap is empirical isolation of solar's marginal contribution, not doubt about the
underlying physics.

---

## Projects and programs (every number sourced)

Tiers: **[gov]** government/primary, **[peer]** peer-reviewed, **[trade]** trade
press (usually relaying developer/vendor), **[vendor]** vendor case study,
**[press]** general press. "Grade" = percent; "°" = degrees.

| Location / site | MW | Verified slope | Terrain / climate | Mounting | Cost | Outcome | Source (tier) |
|---|---|---|---|---|---|---|---|
| **Korea — mountain-solar fleet** (1,235 plants surveyed) | fleet | **665 of 1,235 (48.6%) > 15° (27% grade)**; 425 at 15-20°, 120 at 20-25° (36-47%) | Forest/mountain, monsoon, granitic | ground-mount fixed | none published | ~half exceed post-2018 legal limit; several landslided | besteco.kr [press, KFS-sourced] http://www.besteco.kr/news/articleView.html?idxno=6114 |
| **Korea — Hoengseong plant** | plant-scale | slope built above pre-2018 standard | Gangwon forest slope | ground-mount | none | **Landslide 9 Aug 2022: 1.5×10⁴ m³, 330 m runout, 60 m drop, 1 dead, 2 houses destroyed**, debris + panels reached Route 6 | Nam et al. 2023, *Landslides* [peer] https://link.springer.com/article/10.1007/s10346-023-02112-9 |
| **Korea — 2020 monsoon cluster** | 12 sites | on slopes; 5 of 12 built 2017-2019 | forest slopes | ground-mount | none | **12 solar sites experienced landslides** during the 2020 monsoon (KFS counted them among ~1,100 landslides / 667 in Aug); attribution CONTESTED — opposition parties blamed mountain-solar policy, MTIE noted the 12 = **0.1% of 12,721 solar facilities** and denied a causal role; KFS inspected 2,180 plants. Co-location + political dispute, NOT a forensic causal finding | koreaherald.com [press, KFS] https://www.koreaherald.com/view.php?ud=20200810000926 ; koreatimes.co.kr [press] https://www.koreatimes.co.kr/www/opinion/2020/12/202_294318.html |
| **Japan — Sakura-no-Sato, Nagasaki** | ~part of ~21 MW (4 sites) | **30° face (58% grade), measured** | Volcanic city road embankment (法面) | fixed, panels parallel to face; monorail construction | not published | Operating 2015; road-slope RFP | Nikkei BP Mega-Solar [trade] https://project.nikkeibp.co.jp/ms/article/FEATURE/20150803/430502/ |
| **Japan — forest-permitted solar (national)** | ~21,000 ha, ~15,000 permits FY2013-22 | fleet on graded forest slopes | humid, seismic, high-rainfall | ground-mount | land-prep line **¥11,000-19,000/kW ($73-127/kW)** for ground-mount, **¥0 rooftop**; tail sites >¥40,000/kW ($267/kW) | operating; ~10% had construction-phase sediment/turbid runoff | METI FIT cost committee, Dec 2024 [gov] https://www.meti.go.jp/shingikai/santeii/ (資本費内訳, 土地造成費 line); Forestry Agency [gov] https://www.enecho.meti.go.jp/category/saving_and_new/saiene/community/dl/07_05.pdf |
| **Japan — Atami / Izusan** | adjacent solar site (not the failure) | site on cut ridge, stable ground | Volcanic hillside, Shizuoka | n/a | n/a | **3 July 2021 debris flow: 26-28 dead, >130 homes**; caused by an illegal ~54,000 m³ fill mound (~50 m vs 15 m legal limit), **not** the solar site (Shizuoka Pref + Forestry Agency: "not a direct cause") | Springer [peer] https://link.springer.com/article/10.1007/s10346-021-01788-1 ; kankyo-business.jp [gov/trade] https://www.kankyo-business.jp/news/028838.php |
| **Japan — 2018 West Japan rains** | 11 plants | on slopes | — | ground-mount | none | **11 PV plants DAMAGED BY landslides (10 ≥500 kW)** — the paper measures EXPOSURE, framing plants as vulnerable, not causal; 782 of 9,250 mapped sites (8.5%) sit in sediment-hazard zones. No claim solar triggered any failure | Hao, Ialnazov & Yamashiki 2021, *Frontiers in Sustainability* 2:815986 [peer] https://www.frontiersin.org/articles/10.3389/frsus.2021.815986/full |
| **Cayanga-Bugallon, Pangasinan, Philippines** | **94 MWp** | **UNVERIFIED** — "hillside/sloping" per engineer Arup's project title only; pv-magazine release gives no slope | Tropical, 196 ha, non-arable | ground-mount | **₱4.5B EPC ≈ $0.85/W** (EPC-only, JGC) | Energized ~2024 | pv-magazine [trade] https://www.pv-magazine.com/press-releases/aboitizpower-begins-work-on-94-mw-solar-park/ |
| **Sarish Solar, Burgettstown PA** | 26 | **20% grade built; 30% max site condition** — developer/vendor, no independent survey | Reclaimed coal-waste mine, rock ledges | Nevados TRACE terrain-following tracker, zero grading | **not disclosed** (IRA credits "up to 55%") | Operating Q2 2025 | powermag.com [trade] https://www.powermag.com/reclaimed-coal-mine-shines-spotlight-on-innovative-solar-system/ ; nevados.solar [vendor] |
| **Iris Solar, Washington Parish LA** | 13 (of 50) | **capability claim only**: Nevados "rated to 37% (20°)"; no as-built average | Louisiana, hurricane-exposed | Nevados ATT | none; cites Primoris ~$0.75/W SWPPP industry figure | Operating | pv-tech.org [trade] https://www.pv-tech.org/the-end-of-mass-grading-for-solar-projects/ |
| **Reunion Island (Akuo, EDF, Albioma, TotalEnergies)** | 3-5.4 MW each | flat / **UNVERIFIED**; steep interior explicitly excluded | Tropical volcanic; sites on ex-dump, coastal, agrivoltaic | fixed / agrivoltaic | island (ZNI) ground-mount cleared **~92 €/MWh** in France's CRE 2023 PV ZNI tender (not slope-specific) | operating | pv-magazine.fr [press] link above; CRE [gov] https://www.cre.fr/actualites/toute-lactualite/la-cre-publie-la-deliberation-relative-a-son-instruction-de-la-4e-periode-de-lao-2023-pv-zni.html |
| **Canary Islands (Naturgy, Gran Canaria)** | 44 (auction) | flat (ex-farmland → cleaned landfill) | Volcanic island, degraded land | ground-mount | press €-figure internally inconsistent — UNVERIFIED | operating | naturgy.com [press] https://www.naturgy.com/en/press-release/naturgy-strengthens-canary-islands-energy-infrastructure-with-its-first-photovoltaic-plant-reaching-100-mw-of-renewable-energy-now-operational-across-the-islands/ |
| **Puerto Rico (Adjuntas, Casa Pueblo)** | 0.22 (<1 MW) | rooftop microgrid; not a hillside field | Volcanic | rooftop | not disclosed | operating | honnoldfoundation.org [press] https://www.honnoldfoundation.org/news/press-release-casa-pueblo-and-small-business-owners-advance-their-vision-of-transforming-the-town-of-adjuntas-into-the-first-pueblo-solar |
| **AES West Oahu (Hawaii reference)** | 30 | **~15% grade, measured** on 2/3 of site | Volcanic, Waianae slope | tracker/fixed | not stated | operating | civilbeat.org — see `slope-15-30-challenges.md` §6 |

---

## Regulatory slope thresholds (the natural experiments)

Two governments re-regulated slope-sited solar after failures. Both thresholds
are documented primary-source; both are far steeper in grade than Hawaii's rules.

- **South Korea: average-slope limit cut from < 25° to < 15° (47% → 27% grade),
  effective 4 December 2018**, via the Enforcement Decree of the Mountainous
  Districts Management Act (산지관리법 시행령), which also reclassified solar as a
  temporary use requiring restoration to forest. The 25°→15° figure is confirmed
  verbatim in peer-reviewed English: Nam et al. 2023, *Landslides* — "the design
  standard of the average slope was reduced from less than 25° to less than 15°
  following the Act of Mountainous Areas in Korea in 2018"
  (https://link.springer.com/article/10.1007/s10346-023-02112-9). This upgrades
  the item flagged UNVERIFIED in `slope-cost-literature.md` §2.3 and §6.4 to
  **verified**. Effect: forest-solar permit **area** fell 2,443 ha (2018) → 1,024
  (2019) → 112 (2020), ~95% in two years; permit **count** fell from a 5,553 peak
  (2018) to 119 (2022) (https://news.mt.co.kr/mtview.php?no=2020091710088238178;
  https://www.khan.co.kr/article/202307191342001). A REC-multiplier cut to 0.7 in
  2018 compounded the collapse. 2.32 million trees were cut for 4,902 ha of
  mountain solar 2017-2019 before the tightening (koreaherald link above).
- **Japan: natural slope ≥ 30° (58% grade) mandates retaining walls or drainage
  disaster-prevention works** under the Forestry Agency's Dec-2019 solar forest-
  development permit criteria (林地開発許可基準); ≥ 30° with height ≥ 5 m is the
  statutory "steep slope land" (急傾斜地) definition
  (https://www.enecho.meti.go.jp/category/saving_and_new/saiene/community/dl/07_05.pdf).
  The forest-permit trigger for solar was tightened from > 1 ha to > 0.5 ha
  (FY2023), justified because a 0.57 ha solar site sheds the sediment of a 1 ha
  conventional development. ~250 municipalities (≥175 confirmed) now restrict
  "mega-solar" by ordinance; Itō City designated its entire jurisdiction a
  controlled area; FIT/FIP support for non-rooftop commercial solar ends FY2027
  (https://www.japantimes.co.jp/environment/2024/05/26/energy/megasolar-opposition-solutions/).

## Cost evidence for slope

The record yields two usable cost facts and one strong null.

- **Japan land-preparation (土地造成費) is a broken-out capex line:** ground-mount
  runs **¥11,000-19,000/kW ($73-127/kW at ¥150/$)** across 2013-2024 install
  years, versus **¥0 for rooftop**, with a right-skewed tail of difficult sites
  above ¥40,000/kW ($267/kW). Verified against the METI FIT cost committee's
  資本費内訳 tables (Dec 2024, https://www.meti.go.jp/shingikai/santeii/). For
  scale, 2024 ground-mount total DC system cost averaged ¥147,000/kW (~$980/kW),
  so land prep is ~7-13% of capex on average and the tail is the grading penalty.
  This is the closest thing to a government-published slope/grading cost premium
  found anywhere, but it is a land-prep line, not a slope-indexed curve.
- **Cayanga (Philippines): ₱4.5B EPC for 94 MWp ≈ $0.85/W EPC-only** — a tropical
  hillside cost anchor, undercut by an unquantified slope (link above).
- **Null result:** no source pairs a verified >20%-grade average slope with a
  project capex. Korea's steep plants (27-47% grade) have no cost data; the
  cost-bearing projects (Cayanga, Japan fleet averages, Nevados case studies)
  either lack a verified slope or disclose no capex. The `slope-cost-literature.md`
  finding — no public continuous cost-vs-slope curve — holds worldwide, not just
  for Hawaii.

---

## Hawaii-relevance assessment

Which analogs transfer, ranked.

1. **Korea and Japan transfer as hazard analogs, not cost analogs.** Both are
   humid, steep, high-rainfall, seismic, and both built utility PV on 27-47%-
   grade forest slopes at scale. Both then saw rainfall-triggered landslides at or
   damaging those plants (Hoengseong 2022: 1 dead; 12 Korean sites in 2020; 11
   Japanese plants damaged in 2018) and re-regulated slope down (Korea to 15°/27%
   grade; Japan retaining walls above 30°/58%). For Hawaii's wet, erodible,
   seismic uplands the directly relevant fact is that the one place utility PV
   climbed to 27-47% grade is a place its slopes repeatedly failed. **But see the
   causation section: "solar-site slopes failed" is documented; "solar caused the
   failures" rests on a sound land-clearing/earthworks mechanism, not on any
   matched-control comparison — do not overstate the attribution.** This
   corroborates `slope-15-30-challenges.md` §3 and §6 (the geotechnical/erosion
   constraint binds above ~15-20%).
2. **Tropical volcanic islands transfer as a null.** Reunion — the closest analog
   (French tropical volcanic, land-scarce, high grid cost) — does not climb its
   steep interior; it sites solar on coastal flats, ex-dumps, and mid-slope
   agrivoltaics, and formally excludes the steep zone. Canaries, Madeira, Azores,
   and Caribbean volcanic islands show the same pattern. The island response to
   steep volcanic terrain is retreat to flat/degraded land, not steep-slope
   engineering. This is itself a finding: land-scarce volcanic islands have not
   demonstrated a steep-slope utility-PV path Hawaii could copy.
3. **Nevados/US mainland (Sarish, Iris, Bartonsville) transfer weakly.** They show
   terrain-following racking can build to ~20% grade (and claim 37%), but the
   numbers are vendor/developer-sourced, the sites are dry-to-temperate reclaimed
   mines and farmland (not tropical volcanic), and none discloses capex. Already
   covered in `slope-cost-literature.md` §1.3.
4. **Cayanga (Philippines) is the best tropical cost anchor** ($0.85/W EPC) but
   its slope is unverified, so it cannot fix a steep-slope cost premium.

## Caveats

1. **No project pairs a verified >20%-grade average slope with a capex.** Every
   headline number is either a verified slope with no cost (Korea, Japan Nagasaki)
   or a cost with an unverified slope (Cayanga, Japan fleet). Do not construct a
   steep-slope $/W from this record.
2. **Degrees vs percent grade is a trap.** Korea's "15°" and Japan's "30°" sound
   moderate but are 27% and 58% grade. When comparing to Hawaii's percent-grade
   notes, convert first.
3. **The steepest Korean averages (20-25° = 36-47% grade) are peer-reviewed/
   regulatory-survey data** (Nam et al.; KFS survey), the strongest non-vendor
   evidence that >20%-grade utility PV has been built — but they are among the
   sites whose slopes later failed, and no cost attaches. (On whether solar
   *caused* those failures, see the causation-assessment section — the honest
   answer is "sound mechanism, thin causal test.")
4. **Nagasaki's 30° (58% grade) is a road-embankment special case**, not a field
   average, built with monorail haulage and spray foundations; no capex published.
5. **Atami did not fail because of solar.** Shizuoka Prefecture and the Forestry
   Agency found the adjacent PV site "not a direct cause"; the failure was an
   illegal fill mound. Cite it as the political trigger for re-regulation, not as
   a solar-slope failure. (Consistent with `slope-cost-literature.md` §2.3.)
6. **Reunion and Canaries figures rest partly on French/Spanish press snippets**
   (pv-magazine.fr, Naturgy) that resisted automated fetch; the Naturgy €5.2M/44
   MW pairing is internally inconsistent — do not cite it as a cost. Worth a manual
   pull before use.
7. **Cayanga's "hillside" descriptor comes from engineer Arup's project title**,
   not the pv-magazine release, which gives no slope. Treat the hillside claim as
   weakly sourced and the slope as UNVERIFIED.
8a. **UNVERIFIED — the causation crux:** no located study compares failure rates
   of solar vs matched non-solar slopes (grade/rainfall/geology held fixed). The
   solar-landslide papers are single-site forensics, exposure maps, or simulation-
   based susceptibility models. The land-clearing/earthworks mechanism is solid
   (Sidle & Ochiai 2006; Sidle 1992; Lehmann et al. 2019) but solar's marginal
   contribution has not been empirically isolated. See the causation section.
8. **UNVERIFIED / gaps:** any project's verified >20%-grade average slope with a
   published capex; a Korean or Japanese slope-vs-flat construction cost premium
   (only Japan's land-prep line and a projected ~$60M/yr Korean landslide-loss
   figure under RCP6.0 exist, not a grading premium); per-plant Korean slopes
   behind paywalls; and the exact Cayanga site slope.

## Cross-links

- `notes/slope-15-30-challenges.md` — Hawaii-specific 15-30% band: tracker limits
  (§1), aspect at 21°N (§2), civil/geotechnical (§3), the Ulupono/Fripp
  +$0.06-0.07/W Hawaii cost factor (§4), hazards and the AES West Oahu ~15% built
  precedent (§6). This note supplies the outside-Hawaii built precedent it lacked.
- `notes/slope-cost-literature.md` — the general ≤15 / 15-30 / >30 framing, the
  "no published cost-vs-slope curve" gap (§2.1), Nevados vendor specs (§1.3), and
  the Korea/Japan landslide references this note verified and deepened (§2.3, §6).
- `docs/ASSUMPTIONS.md` E2 — the ≤15 / 15-30 / >30 slope convention this evidence
  informs.
