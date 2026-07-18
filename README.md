# Land for Solar and Wind Development on Oʻahu

A reference on two questions: **(1) the physical availability of land** for
utility-scale solar and wind development on Oʻahu — how much, where, under what
rules, at what grid distance and on what terrain — and **(2) the political
economy** of Hawaiʻi's land-use restrictions on renewables: who wrote the
rules, who defends them, and how much land they actually put in or out of
reach. Solar's binding restriction is the state agricultural-district statute
(HRS § 205-4.5 and § 205-2); wind's is county setback zoning (Honolulu
Ordinance 25-2 / Bill 64 (2023), the comprehensive revision of the city's Land
Use Ordinance, Revised Ordinances of Honolulu Chapter 21 — the first LUO
overhaul since 1990), because the state statute permits wind on agricultural
land without a cap. The project pairs the full legislative and documentary record
(bills, testimony, LUC dockets, lobbying, campaign finance, board interlocks)
with a quantitative GIS analysis of land-use rules, ownership, grid proximity,
and terrain.

**This is a living reference, not a finished paper.** The analysis and notes
are meant to evolve as data improves and questions get answered. Findings are
tiered (verified / plausible / unverified — see below), and known open items
are tracked in `docs/ACCURACY_REVIEW.md` and the per-note `UNVERIFIED` flags.
Corrections are welcome; the git history is the changelog.

## What the analysis finds

*Oʻahu figures; full sourcing and caveats in the paper and `notes/`. Acreages
are GIS estimates (parcel × soil × slope × line-distance intersections), not
field survey.*

- **The rules, by soil class.** The state agricultural district (~120,800 ac,
  ~32% of Oʻahu) treats solar differently by Land Study Bureau soil rating:
  class A excludes solar as a permitted use (and grants for class-A solar have
  not been the norm, though it is not an absolute bar in practice); class B/C
  allows it up to the lesser of 10% of the parcel or 20 acres, or a special use
  permit above that; class D/E allows it with **no cap and no permit**. Wind
  has been a permitted use on agricultural land of every soil class since 1980,
  with no acreage cap.
- **The cap, quantified.** Under current law, roughly **3,600 acres** of B/C
  land is eligible by right; deleting the 20-acre hard cap (keeping 10%) about
  triples it, and a 20%-of-parcel, no-hard-cap rule reaches **~15,700 acres**
  (~4.3×). The binding element is the flat 20-acre ceiling, which bites on ~85
  large parcels.
- **Grid proximity is mostly not the constraint.** ~75% of B/C acreage lies
  within 3 km of a mapped 46 kV+ line; ~20,400 acres of the uncapped D/E land
  sit within 1 km of a line — of which roughly 6,100 (≤15% slope) to 11,100
  (≤30% slope) acres are also flat enough to build.
- **Ownership is concentrated.** Government owns about half the district;
  Kamehameha Schools holds ~13% of the district (about a quarter of all
  *private* agricultural land).
- **The permit path, in practice.** Every utility-scale solar special use
  permit that reached the Land Use Commission (8 dockets, 2014–2026) was
  approved, unanimously, with no intervenors, in a median of ~6 months.
- **Wind's binding constraint is county setbacks, not the state statute.**
  Honolulu Ordinance 25-2 (2025) leaves ~36% of AG/Country-zoned land (~39,400
  ac) geometrically eligible for large turbines and bars repowering of the
  existing fleet.
- **Non-agricultural land exists but is costly.** ~11,900 acres of
  low-improvement urban-district land is physically suitable; the durable
  slice (public land, quarries, landfills, brownfields) is ~5,700 acres.

On the political economy: the record indicates the caps were written by the
agricultural-preservation establishment (planning agencies, the Farm Bureau,
environmental groups defending against sprawl), not by the utility or large
landholders — who generally testified *for* liberalization or stayed silent.
The popular "astroturf" story does not survive four independent evidentiary
traces (legal representation, campaign finance, testimony coordination, the
wind record). Utility–landholder ties are real but appear as board and
trade-association interlocks, not manufactured opposition. See the paper for
the full argument.

## The paper

- **`paper/land-restrictions-paper-final.html`** — the assembled paper, fully
  self-contained (all figures embedded as base64 data-URIs). The file to read
  or share.
- **`paper/land-restrictions-paper.pdf`** — PDF render of the same.
- `paper/land-restrictions-paper.html` is the *template* (figure placeholders
  `__F1__`…); `analysis/assemble_paper.py` produces the final HTML from it.

The paper is one snapshot of the reference; the notes and data below are the
living substrate it draws on.

## Companion repository

Grid and electricity-system modeling — bulk-delivery/transfer analysis, the
interface graph, demand and DER geography, and Switch-Oahu nodal inputs —
continues in [`oahu-grid`](https://github.com/mikejrob/oahu-grid). A few
grid-thread notes and tables are mirrored here (they are cited by the paper's
transmission section); those copies are periodic snapshots and may lag the
live versions in `oahu-grid`.

## Repository map

```
.
├── CLAUDE.md      Project instructions + running verified-findings record
├── README.md      This file
├── analysis/      Reproducible Python scripts (GIS screens, optimization,
│                  figures, paper assembly) and generated figures (figs/)
├── data/          Tidy analysis-ready CSVs, TMK-keyed where applicable
│   ├── gis/       Cached GIS layers (parquet/tif/geojson, gitignored) and
│   │              derived summary CSVs (tracked)
│   ├── intermediates/  Session-built intermediates committed for reproducibility
│   └── raw/       Primary-source caches (gitignored): capitol.hawaii.gov bill
│                  pages and testimony, LUC dockets, SEC EDGAR proxies, CSC
│                  campaign-finance dumps, RPAD pulls, wayback captures
├── docs/          DATA_DICTIONARY.md, METHODS.md, NOTES_INDEX.md, ASSUMPTIONS.md,
│                  AUDIT_*.md, ACCURACY_REVIEW.md (living verification log)
├── notes/         Per-thread research notes; every factual claim carries a
│                  primary-source citation or an explicit UNVERIFIED flag
├── paper/         Paper template, assembled HTML, and PDF
└── testimony/     Curated testimony PDFs + extracted text, by bill
```

Per-directory READMEs give more detail; `docs/DATA_DICTIONARY.md` documents
every CSV column-by-column, `docs/METHODS.md` documents each pipeline, and
`docs/ASSUMPTIONS.md` registers every exogenous parameter with its
justification and disclosure status.

## Reproduction quick start

```sh
python3 -m venv .venv && source .venv/bin/activate
pip install geopandas rasterio shapely pyproj matplotlib pandas numpy scipy pyarrow
```

The GIS pipeline, in dependency order:

```sh
python analysis/cap_scenarios.py analyze statewide  # S0–S4 cap scenarios per parcel
python analysis/transmission_screen.py             # distance-to-grid screen
python analysis/slope_screen.py                    # DEM slope banding
python analysis/transmission_expansion.py          # greedy expansion frontier
python analysis/join_owner_transmission.py         # ownership × transmission join
python analysis/make_paper_figs.py                 # figures F1–F3
python analysis/make_expansion_fig_cost.py         # expansion curve w/ cost lines
python analysis/nonag_classify.py && python analysis/nonag_fig.py   # non-ag viability + map
python analysis/wind_viable_map.py                 # wind viability map
python analysis/assemble_paper.py                  # embed figures → final HTML
```

Supporting scripts: `corridor_candidates.py` (corridor ranking),
`fetch_ownall.py` + `resolve_owners.py` (ownership build),
`campaign_finance_extract.py` (donor classification),
`wind_setback_oahu.py` (wind setback geometry).

Scripts are **resume-safe and re-run offline** from the local cache in
`data/gis/` once the layers are downloaded. `data/raw/` and the large
`data/gis/` layers are **gitignored**; re-download endpoints and methods are in
`docs/METHODS.md`. Scripts hardcode the project root — edit `ROOT`/`PROJECT` at
the top of each script if the repo lives elsewhere.

*Reproducibility caveat:* most of the pipeline re-runs end-to-end, and the
core figure/paper assembly reproduces byte-for-byte. Two builds — the non-ag
viability screen and the ownership×transmission join — depend on committed
intermediate files in `data/intermediates/` (their upstream fetch/screen steps
were built interactively and are captured as those intermediates rather than as
a single re-runnable script). `docs/AUDIT_REPRO.md` documents exactly which
steps are and are not reconstructible from raw sources.

## Data sources and access caveats

| Source | Used for | Caveat |
|---|---|---|
| capitol.hawaii.gov session archives | Bill texts, committee reports, testimony | **Cloudflare-blocked to scripted access.** Retrieved via Wayback Machine; recipes in `notes/` (`pre2011-solar-bills.md`, `sb631-2011.md`). Cached in `data/raw/capitol/`. |
| Hawaii Campaign Spending Commission | Contributions to siting-bill legislators | Live portals **truncated to 2015+ in 2025**; pre-2015 recovered from a 2025-03-31 Internet Archive capture of the CKAN dump (218,392 rows, 2006–2024). See `analysis/campaign_finance_extract.py`. |
| geodata.hawaii.gov (State GIS portal) | LSB soil classes, State Land Use Districts, TMK parcels | Cached to `data/gis/`; scripts re-download. |
| Honolulu RPAD (ArcGIS REST) | Parcel ownership and assessed values | Fee-owner of record only; leaseholds, CPRs, and entity families need manual resolution (`resolve_owners.py`). Assessment vintage noted in `docs/DATA_DICTIONARY.md`. |
| HIFLD Open + OpenStreetMap | Transmission lines | Both **under-map the 46 kV system**; 138 kV coverage is reliable, so distance-to-line figures are conservative (true distances shorter). |
| USGS 3DEP 1/3″ DEM | Slope screen | 10 m grid; smooths microterrain. |
| luc.hawaii.gov / files.hawaii.gov/luc | SUP dockets | Cached in `data/raw/dockets/`. |
| SEC EDGAR (HE) | HEI proxy statements, board interlocks | Cached in `data/raw/edgar/`. |
| Hawaii State Ethics Commission | Lobbyist registrations | 2013–2020 machine-readable; 2021+ in a JS portal (manual). |
| MISO MTEP cost guides | Transmission cost benchmarks | Mainland values × an inferred Hawaiʻi multiplier, flagged UNVERIFIED. |

## Evidentiary discipline

Every factual claim in the notes and paper is tiered: **(1) verified** against
a primary source (session law, committee report, testimony PDF, docket filing,
proxy statement — cited by URL), **(2) plausible hypothesis awaiting
evidence**, or **(3) unverified** — flagged `UNVERIFIED` in the CSVs and notes
until confirmed. The project documents *revealed conduct* (who testified, who
intervened, who donated, who sits on which board), not inferred intent. Null
results are reported.

## Citation

> Roberts, Michael J. (2026). *Land for Solar and Wind Development on Oʻahu:
> Availability, Rules, and the Political Economy of Hawaiʻi's Agricultural-Land
> Restrictions.* Working paper and data repository, University of Hawaiʻi at
> Mānoa. https://github.com/mikejrob/solar-wind-landuse

```bibtex
@misc{roberts2026solarland,
  author = {Roberts, Michael J.},
  title  = {Land for Solar and Wind Development on Oʻahu: Availability, Rules,
            and the Political Economy of Hawai`i's Agricultural-Land Restrictions},
  year   = {2026},
  note   = {Working paper and data repository, University of Hawai`i at M\=anoa},
  url    = {https://github.com/mikejrob/solar-wind-landuse}
}
```
