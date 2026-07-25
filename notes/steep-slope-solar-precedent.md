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
evidence comes from South Korea and Japan, where it repeatedly landslided, and
**no single project on the record pairs a verified >20%-grade average slope with
a published capex.** The two things never travel together.

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
sited PV has slid, killed people, and been re-regulated down.

---

## Projects and programs (every number sourced)

Tiers: **[gov]** government/primary, **[peer]** peer-reviewed, **[trade]** trade
press (usually relaying developer/vendor), **[vendor]** vendor case study,
**[press]** general press. "Grade" = percent; "°" = degrees.

| Location / site | MW | Verified slope | Terrain / climate | Mounting | Cost | Outcome | Source (tier) |
|---|---|---|---|---|---|---|---|
| **Korea — mountain-solar fleet** (1,235 plants surveyed) | fleet | **665 of 1,235 (48.6%) > 15° (27% grade)**; 425 at 15-20°, 120 at 20-25° (36-47%) | Forest/mountain, monsoon, granitic | ground-mount fixed | none published | ~half exceed post-2018 legal limit; several landslided | besteco.kr [press, KFS-sourced] http://www.besteco.kr/news/articleView.html?idxno=6114 |
| **Korea — Hoengseong plant** | plant-scale | slope built above pre-2018 standard | Gangwon forest slope | ground-mount | none | **Landslide 9 Aug 2022: 1.5×10⁴ m³, 330 m runout, 60 m drop, 1 dead, 2 houses destroyed**, debris + panels reached Route 6 | Nam et al. 2023, *Landslides* [peer] https://link.springer.com/article/10.1007/s10346-023-02112-9 |
| **Korea — 2020 monsoon cluster** | 12 sites | on slopes; 5 of 12 built 2017-2019 | forest slopes | ground-mount | none | **12 solar farms triggered landslides** in Aug 2020 (of 667 landslides that month); KFS inspected 2,180 plants | koreaherald.com [press, KFS] https://www.koreaherald.com/view.php?ud=20200810000926 |
| **Japan — Sakura-no-Sato, Nagasaki** | ~part of ~21 MW (4 sites) | **30° face (58% grade), measured** | Volcanic city road embankment (法面) | fixed, panels parallel to face; monorail construction | not published | Operating 2015; road-slope RFP | Nikkei BP Mega-Solar [trade] https://project.nikkeibp.co.jp/ms/article/FEATURE/20150803/430502/ |
| **Japan — forest-permitted solar (national)** | ~21,000 ha, ~15,000 permits FY2013-22 | fleet on graded forest slopes | humid, seismic, high-rainfall | ground-mount | land-prep line **¥11,000-19,000/kW ($73-127/kW)** for ground-mount, **¥0 rooftop**; tail sites >¥40,000/kW ($267/kW) | operating; ~10% had construction-phase sediment/turbid runoff | METI FIT cost committee, Dec 2024 [gov] https://www.meti.go.jp/shingikai/santeii/ (資本費内訳, 土地造成費 line); Forestry Agency [gov] https://www.enecho.meti.go.jp/category/saving_and_new/saiene/community/dl/07_05.pdf |
| **Japan — Atami / Izusan** | adjacent solar site (not the failure) | site on cut ridge, stable ground | Volcanic hillside, Shizuoka | n/a | n/a | **3 July 2021 debris flow: 26-28 dead, >130 homes**; caused by an illegal ~54,000 m³ fill mound (~50 m vs 15 m legal limit), **not** the solar site (Shizuoka Pref + Forestry Agency: "not a direct cause") | Springer [peer] https://link.springer.com/article/10.1007/s10346-021-01788-1 ; kankyo-business.jp [gov/trade] https://www.kankyo-business.jp/news/028838.php |
| **Japan — 2018 West Japan rains** | 11 plants | on slopes | — | ground-mount | none | **11 PV plants damaged by landslides (10 ≥500 kW)**; 782 of 9,250 mapped sites (8.5%) in sediment-hazard zones | Frontiers in Sustainability 2021 [peer] https://www.frontiersin.org/articles/10.3389/frsus.2021.815986/full |
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
   grade forest slopes at scale. Both then suffered rainfall-triggered landslides
   at those plants (Hoengseong 2022: 1 dead; 12 Korean sites in 2020; 11 Japanese
   plants in 2018) and re-regulated slope down (Korea to 15°/27% grade; Japan
   retaining walls above 30°/58%). For Hawaii's wet, erodible, seismic uplands the
   directly relevant fact is that the one place utility PV climbed to 27-47% grade
   is the one place it slid. This corroborates `slope-15-30-challenges.md` §3 and
   §6 (the geotechnical/erosion constraint binds above ~15-20%).
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
   evidence that >20%-grade utility PV has been built — but they are the sites
   that landslided, and no cost attaches.
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
