# Land for Solar and Wind Development on Oahu

Research compilation on the political economy of Hawaii's agricultural-land
restrictions on utility-scale solar (HRS § 205-4.5 and § 205-2): who wrote the
rules, who defends them, and how much land they actually put in or out of
reach. The project pairs the full legislative/documentary record (bills,
testimony, LUC dockets, lobbying, campaign finance, board interlocks) with a
quantitative GIS analysis of Oahu land-use rules, ownership, grid proximity,
and terrain.

## The paper

- **`paper/land-restrictions-paper-final.html`** — the assembled paper, fully
  self-contained (all ten figures embedded as base64 data-URIs). This is the
  file to read or share.
- **`paper/land-restrictions-paper.pdf`** — PDF render of the same.
- `paper/land-restrictions-paper.html` is the *template* (figure placeholders
  `__F1__`…`__F9__`); `analysis/assemble_paper.py` produces the final HTML
  from it. The paper is also published as a Claude web artifact.

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
│   └── raw/       Primary-source caches: capitol.hawaii.gov bill pages and
│                  testimony, LUC dockets, SEC EDGAR proxies, CSC campaign-
│                  finance dumps, LURF wayback captures (gitignored)
├── docs/          DATA_DICTIONARY.md, METHODS.md, NOTES_INDEX.md
├── notes/         Per-thread research notes; every factual claim carries a
│                  primary-source citation or an explicit UNVERIFIED flag
├── paper/         Paper template, assembled HTML, and PDF
├── testimony/     Curated testimony PDFs + extracted text, by bill
└── cache/         Scratch downloads (gitignored)
```

Per-directory READMEs give more detail; `docs/DATA_DICTIONARY.md` documents
every CSV column-by-column and `docs/METHODS.md` documents each pipeline.

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
python analysis/make_paper_figs.py                 # figures F1–F3
python analysis/make_expansion_fig_cost.py         # expansion curve w/ cost lines
python analysis/join_owner_transmission.py         # ownership x transmission join (Fig 1/Table 3 input)
python analysis/nonag_classify.py && python analysis/nonag_fig.py   # non-ag viability classes + Figure 9
python analysis/wind_viable_map.py                 # wind viability map (Figure 10)
python analysis/assemble_paper.py                  # embed figures -> final HTML
```

Supporting scripts: `corridor_candidates.py` (corridor ranking, figure F6),
`fetch_ownall.py` + `resolve_owners.py` (ownership build),
`campaign_finance_extract.py` (donor classification),
`wind_setback_oahu.py` + `wind_viable_map.py` (wind setback geometry and map).

All scripts are **resume-safe and re-run offline** from the local cache in
`data/gis/` once the layers are downloaded. `data/raw/` and the large
`data/gis/` layers are **gitignored**; on a fresh clone, re-download them via
the scripts themselves (`python analysis/cap_scenarios.py download statewide`
fetches the LSB/SLUD/parcel layers; `transmission_screen.py` and
`slope_screen.py` read cached line and DEM layers from `data/gis/`; the caches
were downloaded by the original sessions — sources and re-download endpoints are
documented in `docs/METHODS.md`). Scripts hardcode
the project root path — edit `ROOT`/`PROJECT` at the top of each script if
the repo lives elsewhere.

## Data sources and access caveats

| Source | Used for | Caveat |
|---|---|---|
| capitol.hawaii.gov session archives | Bill texts, committee reports, testimony | **Cloudflare-blocked to scripted access.** Retrieved via Wayback Machine; recipes documented in `notes/` (see `notes/pre2011-solar-bills.md`, `notes/sb631-2011.md`). Cached in `data/raw/capitol/`. |
| Hawaii Campaign Spending Commission | Contributions to siting-bill legislators | Live portals were **truncated to 2015+ in 2025**; pre-2015 rows recovered from a pre-truncation Internet Archive capture (2025-03-31) of the CKAN datastore dump (218,392 rows, 2006–2024). See `analysis/campaign_finance_extract.py` docstring. |
| geodata.hawaii.gov (State GIS portal) | LSB soil classes, State Land Use Districts, TMK parcels | Cached to `data/gis/`; scripts re-download. |
| Honolulu RPAD OWNALL (ArcGIS REST) | Parcel ownership (taxyr 2027) | Fee-owner of record only; leaseholds, CPRs, and entity families need manual resolution (done in `resolve_owners.py`). |
| HIFLD Open + OpenStreetMap | Transmission lines | Both **under-map the 46 kV system** (~80–140 km mapped vs several hundred circuit-km real); 138 kV coverage is reliable. |
| USGS 3DEP 1/3″ DEM | Slope screen | — |
| luc.hawaii.gov / files.hawaii.gov/luc | SUP dockets | Cached in `data/raw/dockets/`. |
| SEC EDGAR (HE) | HEI proxy statements, board interlocks | Cached in `data/raw/edgar/`. |
| Hawaii State Ethics Commission | Lobbyist registrations | Cached in `data/raw/dockets/lobbyist_registrations.csv`. |

## Evidentiary discipline

Every factual claim in the notes and paper is tiered: **(1) verified** against
a primary source (session law, committee report, testimony PDF, docket filing,
proxy statement — cited by URL), **(2) plausible hypothesis awaiting
evidence**, or **(3) unverified** — flagged `UNVERIFIED` in the CSVs and notes
until confirmed. The project documents *revealed conduct* (who testified, who
intervened, who donated, who sits on which board), not inferred intent. Null
results are reported.

## Citation

> Roberts, Michael J. (2026). *Land for Solar and Wind Development on Oahu:
> Hawaii's Agricultural-Land Restrictions and Who Shaped Them.* Working paper
> and data repository, University of Hawaiʻi at Mānoa.
> https://github.com/mikejrob/solar-wind-landuse

```bibtex
@misc{roberts2026solarland,
  author = {Roberts, Michael J.},
  title  = {Land for Solar and Wind Development on Oahu: Hawaii's
            Agricultural-Land Restrictions and Who Shaped Them},
  year   = {2026},
  note   = {Working paper and data repository, University of Hawai`i at
            M\=anoa},
  url    = {https://github.com/mikejrob/solar-wind-landuse}
}
```
