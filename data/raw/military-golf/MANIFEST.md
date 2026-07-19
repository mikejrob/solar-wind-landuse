# Source manifest — military & golf solar reference (2026-07-19)

Cached primary/secondary sources for `notes/military-land-solar.md` and
`notes/golf-course-solar.md`. Files fetched with curl; 403/CAPTCHA sources are
listed as link-only (open in a browser to quote verbatim).

## Cached (in this directory)

| file | source | what it supports |
|---|---|---|
| army_oahu_eis_overview.html | home.army.mil/hawaii/OahuEIS/project-overview | 2029 lease acreages (6,322 full / 4,192 modified), retention alternatives |
| army_rod_fedreg_2025.html | federalregister.gov 2025-15034 (ROD, 7 Aug 2025) | ROD: modified retention ~450 ac Kahuku; No Action (lease expiry) Kawailoa-Poamoho + Makua |
| blnr_oahu_feis_nonaccept_2025.html | dlnr.hawaii.gov/blog/2025/06/30/nr25-94 | BLNR declined to accept Oahu FEIS, 27 Jun 2025 |
| kupono_dedication_heco_2024.pdf | hawaiianelectric.com news 2024-06-13 | Kupono Solar 42 MW + 168 MWh, COD Jun 2024, HECO 20-yr PPA |
| concourse_kupono_eul.html | theconcoursegroup.com/23-may-2022 | Kupono: 131.36 ac West Loch, Navy EUL (10 USC 2667), 37-yr lease |
| ameresco_kupono_groundbreaking.html | ir.ameresco.com/.../544 | Ameresco+Bright Canyon JV; Bright Canyon = Pinnacle West subsidiary |
| ameresco_puuloa_grip.html | ir.ameresco.com/.../653 | Pu'uloa Microgrid 99 MW firm renewable, JBPHH, DOE GRIP |
| koolau_close_2020.html | staradvertiser.com 2020-09-25 | Ko'olau Golf Club closed 9/30/2020 |
| koolau_reuse_civilbeat.html | civilbeat.org 2022-05 | Ko'olau owner (First Presbyterian), farming/conservation reuse, no housing |
| makaha_sale_2022.html | golfincmagazine.com | Makaha resort 664 ac sold Aug 2022 $20.7M to KH Group; ~494 homes+152 condos planned |
| navy_kupono_dvids.html | dvidshub.net/news/431866 (Navy Region Hawaii, 2022; public domain) | Kupono stated purpose verbatim: full-base resilience, "island" JBPHH from HECO grid, provide power for HECO to purchase/deliver to installation AND community, island-wide reliability (§6b) |
| army_schofield_generating_station.html | home.army.mil/hawaii/.../schofield-plant | Schofield Generating Station 50 MW biofuel-capable, Army land leased to HECO (§6b) |

Note: §6 (energy-security driver) also cites statutes/policy quoted live via
WebFetch/WebSearch, not cached as files: 10 U.S.C. §101(f)(6)-(7) (energy
resilience/security definitions), §2920 (99.9% critical-load availability by
FY2030; on-site emphasis; black-start exercises), §2911(g)-(h) (25% renewable
FY2025; microgrid/islanding demo projects), §2913 (ESPC/utility-agreement
authority), DoDI 4170.11 (esd.whs.mil/.../417011p.pdf), NDAA FY2020 §2801
(PL 116-92, govinfo). Schofield black-start/three-installation islanding:
army.mil/article/281189 and /273205; hawaiinewsnow.com 2021-06-19 (all 403 to
fetcher — verify in browser).

## Link-only (fetch blocked or not attempted; verify in browser)

- Army FEIS Q&A (scanned PDF): home.army.mil/hawaii/6617/4742/8993/Oahu_ATLR_FEIS_QA.pdf
- Federal Register: NOI 2021-16807 · Draft EIS 2024-12573 · FEIS 2025-08697 · Pohakuloa FEIS 2025-06686
- Schofield Generating Station 50 MW/8 ac/35-yr biofuel: home.army.mil/hawaii/index.php/garrison/dpw/schofield-plant ; hawaiianelectric.com microgrid page
- Ala Wai flood-basin conversion (~$1-11B): poh.usace.army.mil Ala-Wai-Flood-Risk-Management-Project (403 to fetcher); staradvertiser.com 2025-03-30
- Hoakalei $25M sale: staradvertiser.com 2014-10-01 · Honolulu CC 2022 sale: kitv.com
- Turtle Bay expansion (Areté/Host Hotels): staradvertiser.com 2024-09-08
- Olomana state lease S-4095: dlnr.hawaii.gov/wp-content/uploads/2025/11/D-15T-11-11-25.pdf
- Kalakaua Army course→housing (2004): golfcourseindustry.com; 2011 EA files.hawaii.gov
- 10 USC 2667 (EUL): uscode.house.gov · Admission Act §5(f) ceded-lands trust: capitol.hawaii.gov
- Ching v. Case (2019) ceded-land public-trust duty: courts.state.hi.us SCAP-18-0000432
- City muni courses: honolulu.gov/des/golf-courses (Pali, Ted Makalena, West Loch, Ewa Villages, Ala Wai, Kahuku)

## GIS layers pulled (cached under data/gis/military/)

- dod_lands.geojson — ParcelsZoning MapServer layer 34 (DoD Lands), 76 features statewide
- dod_leases_2029.geojson — layer 35 (DoD Leases Expiring 2029), 21 features statewide
- honolulu_zoning.geojson — layer 3 (C&C Honolulu zoning), 1,965 features
- osm_golf_oahu.json — OSM leisure=golf_course, Oahu bbox (Overpass, out geom)
