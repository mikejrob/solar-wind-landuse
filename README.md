# Land, Rules, and Process for Solar and Wind on Oʻahu

This repository documents where utility-scale solar and wind can be built on
Oʻahu, the rules and processes that govern it, and the political economy behind
those rules. It answers four questions with primary sources and GIS data:

1. How much land is available, where, and under what rules (soil class,
   ownership, grid distance, terrain).
2. What process a project passes through to get built (procurement, power
   purchase agreement, interconnection, permitting) and where projects die.
3. Who wrote the land-use restrictions and who defends them.
4. What reforms would let more projects get built at competitive rates.

Solar's binding land restriction is the state agricultural-district statute
(HRS §§ 205-4.5, 205-2). Wind's binding restriction is county setback zoning
(Honolulu Ordinance 25-2 / Bill 64 (2023), the revision of the Land Use
Ordinance, ROH ch. 21). The state statute permits wind on agricultural land
without an acreage cap.

This is a living reference. It grows as investigations are added. The style
guide is `docs/STYLE.md`. Findings are tiered verified / plausible / unverified
(`docs/ACCURACY_REVIEW.md` and per-note `UNVERIFIED` flags). Git history is the
changelog.

**Find an investigation:** `docs/INVESTIGATIONS.md` is the master index (every
investigation with its question, finding, note, and data). `docs/NOTES_INDEX.md`
has prose annotations per note. The roadmap below groups notes by theme.

## Headline findings

*Oʻahu figures. Full sourcing and caveats in the notes. Acreages are GIS
estimates, not survey.*

**Land availability**
- The state agricultural district covers ~120,800 ac (~32% of Oʻahu). Solar
  rules key off Land Study Bureau soil rating: class A excludes solar as a
  permitted use; class B/C permits it up to min(10% of parcel, 20 ac), or a
  special use permit above that; class D/E permits it with no cap and no
  permit (`notes/cap-quantification.md`).
- Under current law, ~3,600 ac of B/C land is eligible by right. Removing the
  20-acre hard cap raises it toward ~15,700 ac (~4.3×). The 20-acre ceiling is
  the binding element (`notes/cap-quantification.md`).
- 75% of B/C acreage sits within 3 km of a mapped 46 kV+ line. ~20,400 ac of
  uncapped D/E land sits within 1 km; 6,100–11,100 ac of that is also buildable
  by slope (`notes/oahu-transmission-screen.md`, `notes/oahu-slope-screen.md`).
- Government owns ~50% of the district. Kamehameha Schools owns ~13% (a quarter
  of private ag land) (`notes/oahu-ownership.md`).
- Non-agricultural supply is small. ~11,900 ac of low-improvement urban land is
  physically suitable; the durable slice is ~5,700 ac. Military land and closed
  golf courses add ~0 new near-grid buildable acreage
  (`notes/oahu-nonag-solar.md`, `notes/military-land-solar.md`,
  `notes/golf-course-solar.md`).

**Process and why projects die**
- The Land Use Commission approved every utility-scale solar special use permit
  it received (8 dockets, 2014–2026), unanimously, with no intervenors, median
  ~6 months (`notes/sup-census.md`).
- Oʻahu solar projects die inside the procurement and interconnection
  machinery — designed under the PUC's 2006 Competitive Bidding Framework,
  administered by HECO — and at no other stage. Land-use permitting kills
  nothing. Median award-to-COD is ~5–5.5 years. Cancellation causes:
  supply chain, developer credit, interconnection cost/delay, PPA price rigidity
  (`notes/project-pipeline-mortality.md`, `notes/heco-solar-procurement.md`).
- Community resistance was the operative cause of death for 0 Oʻahu utility-scale
  solar projects. It killed 1 Maui solar project (Paeahu), 2 wind projects, and
  1 biomass project (`notes/hawaii-project-census.md`,
  `notes/community-resistance-cases.md`).
- The friction is priced: Oʻahu award prices roughly doubled (Stage 1
  $0.08–0.10/kWh, 2018–19 → Stage 3 ~$0.21–0.23, 2024–25) while mainland
  benchmarks rose far less; realized deployment runs ~25–45 MW/yr against the
  ~200 MW/yr a 2045-compliant buildout needs; and as-of-right B/C parcels
  (≤20 ac ≈ 4–5 MW) fall below the RFP's >5 MW floor, leaving them no route
  to a PPA (`notes/process-cost-channel.md`).
- KIUC (Kauaʻi coop) reaches PPA-to-COD in ~18 months via negotiated bilateral
  deals. ERCOT builds via connect-and-manage interconnection. FPL (regulated
  monopoly) self-builds fast. Procurement speed tracks process design
  (`notes/procurement-comparison-kiuc-ercot.md`).

**Political economy**
- The solar caps were requested by the agricultural-preservation coalition
  (planning agencies, the Farm Bureau, environmental groups) across 2008, 2011,
  and 2014. Landholders and the utility did not request them
  (`notes/sb631-2011.md`, `notes/pre2011-solar-bills.md`,
  `notes/acts-2014-2022.md`).
- The astroturf hypothesis fails on four independent traces: legal
  representation, campaign finance, testimony coordination, the wind record
  (`notes/legal-representation-map.md`, `notes/campaign-finance.md`,
  `notes/sierra-club-food-security.md`).
- Utility–landholder ties exist as board and trade-association interlocks
  (`notes/hei-interlocks.md`).

## Investigation roadmap

Each note is a self-contained investigation with its own sources.

**Land rules and statutory history**
- `notes/sb631-2011.md` — the 2011 cap (Act 217): who inserted the 10% and
  20-acre limits.
- `notes/pre2011-solar-bills.md` — 2003–2010 solar-siting bills; the 2008 D/E
  opening (Act 31).
- `notes/acts-2014-2022.md` — the 2014 SUP overlay (Acts 52/55) and the
  2015–2025 amendment series.
- `notes/wind-statutory-entry.md` — wind's 1980 permitted-use entry (Act 24).
- `notes/wind-setbacks.md` — Honolulu Ordinance 25-2 setback regime.

**Land quantification (GIS)**
- `notes/cap-quantification.md` — cap-scenario acreage.
- `notes/oahu-transmission-screen.md` — distance-to-grid and corridor unlocks.
- `notes/oahu-slope-screen.md` and `notes/slope-cost-literature.md` — terrain.
- `notes/oahu-ownership.md` — parcel ownership and concentration.
- `notes/oahu-nonag-solar.md` — urban-district and damaged-land supply.
- `notes/military-land-solar.md` — DoD land, the 2029 lease question.
- `notes/golf-course-solar.md` — golf-course acreage.
- `notes/state-land-solar.md` — state-land leasing authority and history.

**Process to build**
- `notes/sup-census.md` — every solar special use permit and its outcome.
- `notes/project-pipeline-mortality.md` — where projects die, by stage.
- `notes/hawaii-project-census.md` — every project, all islands, cause of
  death.
- `notes/heco-solar-procurement.md` — the RFP machinery, delays, cancellations.
- `notes/procurement-comparison-kiuc-ercot.md` — KIUC, ERCOT, FPL benchmarks.
- `notes/heco-ppa-terms.md` — PPA terms vs mainland and KIUC; what to soften.
- `notes/process-cost-channel.md` — the cost channel: prices, deployment
  rate, and the stranded sub-5-MW segment.
- `notes/neighbor-opposition-and-interconnection.md` — how neighbors oppose
  projects; the gen-tie easement chokepoint.
- `notes/community-resistance-cases.md` — resistance cases by island.

**Political economy**
- `notes/hei-interlocks.md` — HEI board and trust interlocks.
- `notes/campaign-finance.md` — donations to siting-bill legislators.
- `notes/legal-representation-map.md` — intervenor counsel across dockets.
- `notes/sierra-club-food-security.md` — the food-security frame's origin.
- `notes/property-tax-wedge.md` — county tax treatment of solar land.

**Grid (companion repository)**
- `notes/oahu-bulk-delivery.md`, `notes/oahu-grid-public-record.md` — snapshots
  from [`oahu-grid`](https://github.com/mikejrob/oahu-grid), where
  electricity-system modeling continues.

**Synthesis and audit**
- `notes/synthesis-2026-07-11.md` — cross-thread synthesis.
- `docs/ACCURACY_REVIEW.md` — internal-consistency and verification audit.
- `docs/ASSUMPTIONS.md` — every exogenous parameter with its justification.

## The paper

`paper/land-restrictions-paper-final.html` is the assembled paper with figures
embedded. `paper/land-restrictions-paper.pdf` is the PDF. The template is
`paper/land-restrictions-paper.html`; `analysis/assemble_paper.py` builds the
final HTML. The paper covers the land half of the project. The process and
procurement investigations extend beyond it and live in the notes.

## Repository map

```
CLAUDE.md      Project instructions and running findings record
README.md      This file
analysis/      Reproducible Python scripts and generated figures
data/          Analysis-ready CSVs, TMK-keyed where applicable
  gis/         Derived summary CSVs (large layers regenerable via scripts)
  intermediates/  Session-built intermediates committed for reproducibility
  raw/         Primary-source caches (some large caches -> data deposit)
docs/          DATA_DICTIONARY, METHODS, ASSUMPTIONS, STYLE, ACCURACY_REVIEW
notes/         Per-investigation research notes with primary-source citations
paper/         Paper template, assembled HTML, PDF
sources/       Curated primary-source archive (court opinions, ordinances)
testimony/     Legislative testimony PDFs and text, by bill
```

## Reproduction

```sh
python3 -m venv .venv && source .venv/bin/activate
pip install geopandas rasterio shapely pyproj matplotlib pandas numpy scipy pyarrow
```

GIS pipeline in dependency order:

```sh
python analysis/cap_scenarios.py analyze statewide
python analysis/transmission_screen.py
python analysis/slope_screen.py
python analysis/transmission_expansion.py
python analysis/join_owner_transmission.py
python analysis/make_paper_figs.py
python analysis/make_expansion_fig_cost.py
python analysis/nonag_classify.py && python analysis/nonag_fig.py
python analysis/wind_viable_map.py
python analysis/assemble_paper.py
```

Scripts read cached layers from `data/gis/` and hardcode the project root
(edit `ROOT`/`PROJECT` if the repo moves). `docs/METHODS.md` documents each
pipeline and its data sources. `docs/AUDIT_REPRO.md` documents which steps
reproduce from committed inputs.

The large GIS layers and primary-source document caches are in a Zenodo data
deposit, not in Git. `docs/DATA_DEPOSIT.md` lists the two archives, their
checksums, and where to extract them. Download them from the deposit DOI (see
that file) to run the full GIS pipeline.

## Data sources

| Source | Used for | Access note |
|---|---|---|
| capitol.hawaii.gov | Bills, committee reports, testimony | Cloudflare-blocked; retrieved via Wayback (`notes/` recipes) |
| Hawaii Campaign Spending Commission | Donations to legislators | Live portal truncated to 2015+; pre-2015 from a 2025-03-31 archive |
| geodata.hawaii.gov | Soils, districts, parcels | Scripts re-download |
| Honolulu RPAD | Ownership, assessed values | Fee-owner of record; entity resolution in `resolve_owners.py` |
| HIFLD + OpenStreetMap | Transmission lines | 46 kV under-mapped; distance figures conservative |
| USGS 3DEP | Slope | 10 m grid |
| luc.hawaii.gov, PUC CDMS | Dockets | CDMS is JS-only; PDFs linked where not fetchable |
| SEC EDGAR | HEI proxies | Cached |
| MISO MTEP guides | Transmission costs | Mainland values × Hawaiʻi multiplier (flagged UNVERIFIED) |

## Evidentiary discipline

Every factual claim ties to a primary source or carries an `UNVERIFIED` flag.
The project documents revealed conduct (who testified, intervened, donated, sat
on which board), not inferred motive. Null results are reported. GIS acreages
are model estimates and carry the screening caveats in each note.

## Citation

> Roberts, Michael J. (2026). *Land, Rules, and Process for Solar and Wind on
> Oʻahu.* Working paper and data repository, University of Hawaiʻi at Mānoa.
> https://github.com/mikejrob/solar-wind-landuse

```bibtex
@misc{roberts2026solarland,
  author = {Roberts, Michael J.},
  title  = {Land, Rules, and Process for Solar and Wind on O`ahu},
  year   = {2026},
  note   = {Working paper and data repository, University of Hawai`i at M\=anoa},
  url    = {https://github.com/mikejrob/solar-wind-landuse}
}
```
