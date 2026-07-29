# DoD solar by branch: installed to date and potential (compiled 2026-07-29)

Companion to `notes/military-land-solar.md` (land screen, energy-security
driver, 2024-27 pipeline) and `notes/heco-military-relationship.md` (who owns
the wires). Installed inventory from web/document research; potential from the
repo's own GIS screen (`data/oahu_military_land.csv`).

Headline: **~76–83 MW of grid-scale solar sits on DoD land in Hawaii (Navy land
entirely: Kupono 42 + West Loch 20 + PMRF 14 + Pearl City Peninsula 1.2), and
~53–60 MW of rooftop/distributed PV** — but almost none of either is owned by
the military. The grid-scale MW are HECO-owned (20) or IPP-owned under
lease/EUL (56); the rooftop MW are overwhelmingly owned by privatized-housing
partners' solar financiers (SolarCity/Tesla, Hunt, Holu Hou/Lendlease-Ameresco
JV ≈ 43–50 MW). Government-appropriated PV across all branches is ~8 MW.
The Army has **zero grid-scale solar** — its 50 MW Schofield plant is
HECO-owned biofuel/diesel, not solar. The Marine Corps has under ~1 MW of
documented base-side PV. No Coast Guard PV was found. No DoD solar on Hawaii
Island or Maui was found.

Tiers: [V] verified w/ primary/contemporaneous source; [P] plausible,
single-source or reconciliation needed; [U] unverified/unfindable.
MW are as stated by source; AC/DC basis noted only where a source states it.

## 1. Summary table (installed as of mid-2026)

| Branch | Grid-scale (≥1 MW ground) | Rooftop / distributed | Notes |
|---|---|---|---|
| Army | **0 MW** | **~27–35 MW** (IPC housing ~23 MW [V] + ESS +6.45 MW [P, overlap risk] + Holu Hou ~2 MW [V] + Army-sited 3.6 MW [P]) | Schofield 50 MW = biofuel, NOT solar |
| Navy (Oahu) | **~63 MW** (Kupono 42 [V]; West Loch 20 [V]; Pearl City Peninsula 1.23 [V]) | **~14–17 MW** (OMC rooftop ≈14.5 MW less MCBH share [P]; 2.4 MW gov't bldgs [V]; Ford I. B54 0.31 MW [V]) | |
| Navy (Kauai, PMRF) | **14 MW** (AC; 19.3 MW per AES) [V] | — (Barking Sands OMC housing in OMC total) | AES-owned, KIUC PPA |
| Air Force (incl. HI ANG) | 0 MW | **~6.2 MW** (Hickam Communities 4.7 [V] + PEARL 1.5 [V]) | |
| Marine Corps (MCBH) | 0 MW | **~0.6 MW documented base-side** (2012) [P] + unquantified share of OMC housing [U] | current base-side total unpublished |
| Coast Guard | 0 MW | **0 documented** (solar hot water only, historic) | absence finding |
| **DoD total** | **~77 MW** | **~53–60 MW** | |

**Ownership decomposition (the row that matters):**

| Owner class | MW | Which |
|---|---|---|
| HECO-owned (rate base) | ~20 | West Loch Annex array (Navy land) |
| IPP-owned via EUL/lease + utility PPA | ~56 | Kupono 42 (HECO PPA), PMRF 14 AC (KIUC PPA) |
| Privatized-housing-partner / third-party financier | ~43–50 | IPC ~23–29.5, OMC 15.7 (incl. 1.23 ground), Hickam Communities 4.7 |
| Government-appropriated/owned | ~8 | Pearl Harbor 2.4 (ARRA), Ford I. B54 0.31, PEARL 1.5, MCBH ~0.6, Army rooftop 3.6 (funding [U]) |

So of ~130-137 MW of PV on military land, the services themselves own ~6%.
Every grid-scale electron reaches the civilian grid through a HECO or KIUC
PPA or HECO's own rate base; the housing PV is behind-the-meter (Holu Hou
systems by design do not export).

## 2. Per-branch inventories

### Army (USAG-HI: Schofield, Wheeler, Shafter, Tripler, AMR, HMR, Kunia)

Grid-scale: none. The 50 MW Schofield Generating Station (2018) is
HECO-owned dispatchable biofuel/diesel — the largest item in the Army's
"85 MW DER" claim is the utility's own firm plant
([DOE FEMP award](https://www.energy.gov/cmei/femp/us-army-garrison-hawaii-energy-resiliency-program-wins-femp-award)). [V]

| Project | MW | COD | Owner / mechanism | Tier |
|---|---|---|---|---|
| IPC (Island Palm Communities, Lendlease) housing rooftop, SolarCity buildout | "nearly 23 MW" total; SolarCity tranche announced at 12.8 MW / up to 7,500 homes; +8 MW HECO-approved Dec 2015 toward a stated "25 MW goal" | 2011–~2016 | SolarCity(Tesla)-owned, PPA to IPC; housing ground lease | [V] |
| ESS JV energy-security program (Lendlease + Ameresco 50/50, 2018, $150M, 5,800 homes) | +6.45 MW rooftop "to add to existing systems" | 2018–~2022 | ESS JV / housing partner | [P] — whether the 6.45 is inside or on top of the "nearly 23" is not stated; treat 23 vs 29.5 as the honest range |
| Holu Hou / Lendlease EnergyShare clusters | ~2 MW (200 homes × 10 kW PV + 25 kWh) at AMR, celebrated 2024-12-10; expanding through 2026; **no grid export** | 2023– | Holu Hou/housing partner | [V] |
| Army-sited rooftop PV (FEMP decomposition) | 3.6 MW | by 2019 | ownership/funding **[U]** — no source names buildings or appropriation | [P] (single source) |
| FEMP "18 MW existing PV" | see reconciliation below | — | — | [P] |

Sources: [Better Buildings showcase](https://betterbuildingssolutioncenter.energy.gov/showcase-projects/lendlease-island-palm-communities)
(cached `betterbuildings_ipc_showcase.html`): "Solar installations across the
community – totaling nearly 23 MW. The ESS program will provide an additional
6.45 MW of rooftop solar"; [SolarCity/Tesla IR release](https://ir.tesla.com/press-release/solarcity-provide-solar-electricity-7500-military-homes-island)
(12.8 MW, 7,500 homes; page 403s to bots — figure via search index [P]);
[army.mil 2015-12-14](https://www.army.mil/article/159595/ipc_expands_solar_effort)
(cached `armymil_159595.html`): "approval from Hawaiian Electric Company to
install an additional eight megawatts of PV, which will help us reach our
current goal of 25 megawatts" — Kalakaua Ph. 3, Wiliwili, Rainbow Village
(Tripler), Castner Village, Mendonca Park; Holu Hou —
[army.mil 281977](https://www.army.mil/article/281977/) /
[Holu Hou release](https://holuhou.com/press/holu-hou-energy-and-lendlease-bring-resilient-renewable-energy-to-military-homes-lightens-load-on-energy-grid/)
(cached in `data/raw/heco-military/federal/`);
[Stars & Stripes 2023-05-08](https://www.stripes.com/branches/army/2023-05-08/solar-energy-army-housing-hawaii-10055234.html).

**Reconciling the FEMP "18 MW PV":** sources give the USAG-HI PV line as
18 MW ([FEMP](https://www.energy.gov/cmei/femp/us-army-garrison-hawaii-energy-resiliency-program-wins-femp-award)),
17 MW ([Knowledge Online case study](https://knowledge-online-defense-communities.knowledgeowl.com/help/innovative-partnership-to-increase-energy-resilience-us-army-garrison-hawaii-and-hawaiian-electric-company)),
and 15 MW (army.mil resilience-test variant, via search index). No source
itemizes it. The only PV fleet of that size on Army installations is the
IPC housing portfolio (SolarCity-owned), so the best reading is that the
Army's "existing 18 MW PV" **is largely the housing partner's PV counted as
garrison DER**, not a separate Army-owned fleet — i.e., do NOT add 18 to the
23. [P] Nothing found supports any Army-appropriated ground array; FY2026
ERCIP lists no Hawaii project (see military-land-solar.md §7a).

### Navy

Grid-scale (all on Navy fee land):

| Project | MW | COD | Owner / mechanism | Tier |
|---|---|---|---|---|
| Kupono Solar, West Loch Annex, JBPHH | 42 MW PV + 42 MW/168 MWh (AC/DC basis unstated) | Jun 2024 | IPP (Ameresco + Bright Canyon JV), 37-yr EUL (10 USC 2667), 20-yr HECO PPA | [V] |
| West Loch array, JBPHH | ~20 MW (AC) | 2019 | **HECO-owned, rate base**, on Navy land (HECO + REC Solar + Navy) | [V] |
| Pearl City Peninsula Solar Park | 1.23 MW ground-mount, 7 ac (ex-warehouse land) | Dec 2012 (dedicated) | Forest City Hawaii (now Hunt/OMC) — housing partner; serves Navy housing (~250 homes), $13M | [V] |
| PMRF Barking Sands (Kauai), "AES Kekaha / AES PMRF" | **14 MW AC** (PPA basis) / **19.3 MW** per AES (DC implied); 70 MWh 5-hr BESS; 100% clean islanding for the base | in service Mar 2021 | **AES-owned**; Navy leases 140 ac to KIUC, KIUC subleases 138 ac to AES; 25-yr KIUC PPA at 10.85¢/kWh (PUC Docket 2017-0443) | [V] |

Sources: Kupono/West Loch — repo baseline (military-land-solar.md §3);
Pearl City Peninsula — [Hawaii News Now 2012](https://www.hawaiinewsnow.com/story/20251848/oahus-largest-solar-farm-goes-online/)
(cached `hnn_pearl_city_peninsula_2012.html`),
[cleanview listing](https://cleanview.co/solar-farms/hawaii/58676/pearl-city-peninsula-solar-park) (cached);
PMRF — [AES case study](https://www.aes.com/energy-insights/first-its-kind-clean-energy-microgrid-us-navy-and-kiuc)
("19.3 MW of solar with 70 MWh"; completed March 2021; cached
`aes_pmrf_microgrid.html`), [KIUC/AES PPA docket 2017-0443](https://cca.hawaii.gov/dca/kiuc-and-aes-kekaha-solar-file-application-for-ppa-docket-no-2017-0443/),
[NREL feature](https://www.nrel.gov/news/detail/features/2021/us-navy-kiuc-aes-and-nrel-innovate-and-collaborate-for-resilience-and-cost-effective-clean-energy-project-on-kauai),
[electric.coop](https://www.electric.coop/kauai-co-op-works-with-neighbors-to-keep-the-power-on-during-wildfire) (14 MW/70 MWh).
The 14 vs 19.3 discrepancy resolves as AC (PPA/utility basis) vs DC (AES
nameplate) [P — neither source labels its basis explicitly]. A 2024 RESET
report's "30 MW PV at PMRF" ([Converge Strategies PDF](https://convergestrategies.com/wp-content/uploads/2024/02/ConsiderationsforRetrofittingExistingSolarWithEmergingTechnologiesRESET.pdf),
cached) is an outlier matching no other source — treat as error.

Rooftop/distributed:

| Project | MW | COD | Owner / mechanism | Tier |
|---|---|---|---|---|
| OMC (Ohana Military Communities, Hunt) housing rooftop, 15 communities | **15.7 MW total incl. the 1.23 MW ground array** → ~14.5 MW rooftop; "27% of OMC's total Hawaii residential electricity" | buildout through Nov 2017 (last project: NCTAMS PAC Wahiawa); figure as of Aug 2020 | Hunt/OMC housing partner (Forest City-era SolarCity partnership) | [V] |
| Pearl Harbor five-building rooftop (SolarWorld) | 2.4 MW | 2011 | **Government-owned**, $15M ARRA-funded; DRI Energy under contract to Niking Corp. | [V] |
| Ford Island Bldg 54 rooftop | 309 kW ("largest federal PV array in Hawaii" at the time, 31,000 sq ft, >400 MWh/yr) | mid-2000s | Government (Commander Navy Region Hawaii) | [V] |

OMC communities in the 15.7: Halsey, Radford, McGrew, Hokulani, Hale Moku,
Ford Island, Catlin Park, Hele Mai, Doris Miller, Pa Honua, Mololani, Waikulu,
Heleloa, Ulupau + Pearl City Peninsula ground —
[Hunt PR 2020-08-25](https://www.prnewswire.com/news-releases/hunt-military-communities-expands-on-leading-solar-initiatives-in-hawaii-301117702.html)
(cached `hunt_omc_15.7MW_2020.html`). Mololani/Waikulu/Heleloa/Ulupau (and
likely Pa Honua) are MCBH Kaneohe — **the Navy/Marine split of the 15.7 MW is
not published [U]**. OMC also spans Wheeler AAF and Barking Sands.
Pearl Harbor 2.4 MW — [BusinessWire 2011-06-02](https://www.businesswire.com/news/home/20110602005630/en/Key-Buildings-of-Historic-Pearl-Harbor-Naval-Base-Host-2.4-Megawatts-of-SolarWorld-Solar-Panels);
Ford Island B54 — archived [Navy sustainability page](https://web.archive.org/web/20210621215246/https://navysustainability.dodlive.mil/environment/land-based-efforts/solar-wind-and-geothermal-power/)
(cached `navysustainability_solar_page.html`). Possible small overlap if B54
is one of the five 2011 buildings — full building list not retrieved [U].

Not PV (exclude from PV totals): Ford Island 140 homes + Radford Terrace 30
homes got **solar water heating** (SunEarth), not PV
([SunEarth case study](https://sunearthinc.com/case-studies/2018/06/11/140-systems-installed-on-ford-island-navy-residential-project/)). [V]

Documented non-event: a 2012 Navy proposal to put PV on Ford Island's historic
runway drew opposition from the Pacific Aviation Museum ("like putting a water
park in Gettysburg") and was never built
([Hawaii News Now 2012-11-21](https://www.hawaiinewsnow.com/story/20163079/struggle-over-powering-ford-island-with-solar-panels/)). [V]
Pu'uloa Solar (6 MW + 30 MWh, PUC Docket 2025-0436) is **pending, not
installed** (repo baseline). Recurring "Pearl Harbor 20 MW solar farm" claims
(e.g. [greenmatters 2018](https://www.greenmatters.com/news/2018/04/18/p9xe2/us-navy-solar-farm-pearl-harbor))
all refer to the West Loch HECO array — nothing else of that size exists.

### Air Force (incl. Hawaii Air National Guard)

| Project | MW | COD | Owner / mechanism | Tier |
|---|---|---|---|---|
| Hickam Communities housing rooftop (Lendlease AF housing, JBPHH) | **4.7 MW** (announced at ~4 MW, >2,000 homes) | completed 2013 | SolarCity-owned under PPA; Lendlease off-taker; HECO interconnection | [V] |
| PEARL microgrid (HI ANG 154th Wing F-22 campus, JBPHH-Hickam) | **1.5 MW PV** + 500 kWh BESS; first of six planned JBPHH microgrids | construction complete ~Aug 2020 (program from 2016) | Government (AFRL/NGB/HCATT/NAVFAC); H2MG hydrogen expansion underway | [V] |

Sources: [Lendlease project page](https://www.lendlease.com/us/projects/hickam-communities-rooftop-solar/)
(cached `lendlease_hickam_rooftop.html`): "installation of 4.7MW of rooftop
photovoltaic systems... Through a power purchase agreement (PPA), SolarCity
engineered, installed and will maintain";
[Star-Advertiser 2011-07-16](https://www.staradvertiser.com/2011/07/16/business/solar-panels-going-up-on-hickam/);
[154th Wing PEARL article](https://www.154wg.ang.af.mil/News/Article-Display/Article/2070358/project-pearl-sustainable-microgrid-to-deliver-energy-assurance/);
[HTDC HCATT](https://www.htdc.org/programs/hcatt/hcatt-pearl-microgrid/).
Bellows AFS: no PV found [U — absence]. No non-housing hangar-scale AF PV
found beyond PEARL.

### Marine Corps (MCBH Kaneohe Bay)

Documented base-side PV (2012 MCBH energy office inventory, the only
itemization found):

| Item | kW | Tier |
|---|---|---|
| BEQ 7022 polycrystalline solar **carports** | 471 kW | [V] |
| Bldgs 1045, 1033, 1027 amorphous BIPV | ~32 kW each (~96 kW) | [V] |
| Bldg 268 BIPV solar shingles | 26 kW | [V] |
| Planned then: 230 kW-DC "net zero" + up to 655 kW-DC FIT projects | built? | [U] |

Source: MCBH energy manager W. Nuttling, Aug 2012 presentation
([energy.hawaii.gov PDF](https://energy.hawaii.gov/wp-content/uploads/2012/04/WilliamNuttling.pdf),
cached `mcbh_nuttling_2012.pdf`). ≈0.6 MW documented; **no later public
itemization of MCBH base-side PV exists** — 2024 base messaging says only
"equipped with solar panels, generating a substantial amount"
([DVIDS 484155](https://www.dvidshub.net/news/484155/reducing-energy-consumption-marine-corps-base-hawaii-celebrating-energy-conservation-month)). [U — current total unfindable]
A 2013 report of "24 MW planned at MCBH and Navy housing" (SolarCity,
[Star-Advertiser 2013-05-09](https://www.staradvertiser.com/2013/05/09/business/solar-panels-going-up-atop-military-housing/))
is the program that became the Hunt/OMC 15.7 MW housing buildout — not a
separate base array [P]. MCBH housing PV (Mololani, Waikulu, Heleloa, Ulupau)
sits inside the OMC 15.7 MW; MCBH share unpublished [U]. The MCBH resilience
microgrid (RFP to HECO ~Feb 2024) is not awarded/built (repo baseline).

### Coast Guard

**No PV found** at Air Station Barbers Point, Base Honolulu/Sand Island, or
CG housing — only historic solar *hot water* for aircraft washing at Barbers
Point ([USCG history](https://www.history.uscg.mil/browse-by-topic/Aviation/Article/3061930/air-station-barbers-point-hawaii/)).
CG families largely use other services' privatized housing (IPC etc.), so any
"CG solar" is inside the Army/Navy housing totals. [V as absence-of-record]

### Hawaii Island / Maui

- Pohakuloa Training Area: **no solar project found** (searches of Army,
  budget, and EIS material; the ATLR DEIS returned nothing on PV). [U — absence]
- MHPCC Kihei (AFRL/Air Force): a 1.5 MW solar farm on 13 ac leased from
  Haleakala Ranch was **proposed in 2013**
  ([HPCwire](https://www.hpcwire.com/2013/09/24/maui_high_performance_computing_center_plans_solar_farm/));
  no evidence it was built. The 2.87 MW Kihei Solar Farm that came online 2018
  on Haleakala Ranch land is a civilian MECO/Kenyon project, not DoD and not
  on military land ([Lahaina News](https://www.lahainanews.com/real-estate-features/2018/05/24/maui-s-first-large-scale-solar-project-comes-online-in-kihei/)). [P]
- Kilauea Military Camp: nothing found. [U — absence]

## 3. Gaps / UNVERIFIED (ranked)

1. **Navy vs Marine split of OMC's 15.7 MW** — Hunt publishes one number for
   15 communities spanning JBPHH, MCBH, Wheeler, Barking Sands. Per-community
   MW would need Hunt/NAVFAC PPV documents or HECO interconnection records.
2. **IPC total: 23 vs 29.5 MW** — whether ESS's 6.45 MW is inside "nearly
   23 MW"; and whether Holu Hou's ~2 MW (through 2026) is the ESS program's
   delivery vehicle or additive. Lendlease sustainability reports would settle.
3. **Army-sited 3.6 MW rooftop PV** — which buildings, which appropriation
   (ERCIP/ESPC/UESC), single FEMP source. And the floating 15/17/18 MW
   "existing PV" line — no itemization anywhere; best-read as housing PV.
4. **MCBH current base-side PV total** — last itemized 2012 (~0.6 MW);
   whether the 230/655 kW FIT projects were built is unknown.
5. **AC/DC basis** — stated nowhere for Kupono (42), West Loch (20), IPC/OMC
   housing totals; PMRF 14 AC/19.3 DC is inferred, not labeled.
6. Whether Ford Island B54 (309 kW) is inside the 2011 2.4 MW five-building
   count (full building list not retrieved; businesswire fetch timed out).
7. Hickam Communities: 4 MW (2011 announcement) vs 4.7 MW (Lendlease
   completion page) — used 4.7 as-built.

Cached: `data/raw/heco-military/installed/` — betterbuildings_ipc_showcase.html,
armymil_159595.html, armymil_248301.html, armymil_215494.html,
hunt_omc_15.7MW_2020.html, lendlease_hickam_rooftop.html,
navysustainability_solar_page.html, hnn_pearl_city_peninsula_2012.html,
cleanview_pearl_city_peninsula.html, aes_pmrf_microgrid.html,
doe_omc_solar_showcase.html, mcbh_nuttling_2012.pdf,
converge_RESET_retrofit_existing_solar.pdf.

## 4. Potential by branch (Oahu, from the repo's land screen)

Computed 2026-07-29 from `data/oahu_military_land.csv` (fee tenure; 10 m DEM;
near-grid = within 3 km of a mapped 46 kV+ line; tiers per
`notes/military-land-solar.md` §2).

| Branch | Total acres | Flat ≤15% | Flat near-grid |
|---|---:|---:|---:|
| Navy | 19,721 | 15,681 | 15,523 |
| Army | 34,113 | 12,981 | 11,889 |
| Marine Corps | 3,230 | 2,633 | 2,615 |
| Air Force | 2,658 | 2,045 | 2,044 |
| Coast Guard | 95 | 92 | 92 |

Constraint tiers (flat ≤15% acres):

| Branch | Precedent-built | Plausibly usable (EUL) | ESQD (unoccupied-PV-compatible) | Excluded (training/UXO + airfield + developed) |
|---|---:|---:|---:|---:|
| Navy | 3,273 | 2,365 | 5,363 | 4,680 |
| Army | 0 | 2,296 | 200 | 10,485 |
| Marine Corps | 0 | 0 | 17 | 2,615 |
| Air Force | 0 | 0 | 0 | 2,045 |
| Coast Guard | 0 | 0 | 0 | 93 |

Reading: **the Navy holds most of the usable potential and all of the built
record.** It has the most flat land, nearly all of it near-grid, the only
precedent-built tier (West Loch, hosting Kupono and the HECO array), and the
large Lualualei/Kipapa ESQD buffers where unoccupied PV can be compatible. The
Army is second (~2,300 plausibly-usable EUL acres plus the 231-flat-acre
retained Kahuku lease parcel, lease tenure, not in the fee table above), but
most of its footprint is developed, training/UXO, or steep. Marine Corps and
Air Force flat land is almost entirely airfield/airspace-excluded (Kaneohe,
Hickam). Two structural facts reinforce the Navy tilt: Navy land keeps
Navy-owned wires (never privatized — `notes/heco-military-relationship.md`
§6(d)), while Army projects would interconnect on HECO-owned UP distribution;
and the installed record matches — every grid-scale array on Hawaii military
land sits on Navy land (§1). Caveats: screen-level acreage, not DoD-vetted;
availability is at DoD discretion throughout (§5a of the military note);
potential here is physical land, not a projection.
