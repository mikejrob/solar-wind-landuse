# data/

Tidy, analysis-ready CSVs (TMK-keyed where parcel-level), designed for direct
use in R/Julia. `docs/DATA_DICTIONARY.md` documents every file
column-by-column with sources, vintages, and caveats.

- Top-level `*.csv` — tracked outputs: bill inventories, cap-scenario tables,
  ownership/transmission/slope parcel tables, SUP census, campaign finance,
  interlocks, legal-representation edges.
- `gis/` — cached geospatial layers (parquet/GeoTIFF/GeoJSON, **gitignored**)
  plus derived summary CSVs (tracked via the `!data/gis/*.csv` gitignore
  exception). Layers re-download via `analysis/cap_scenarios.py download`,
  `transmission_screen.py`, and `slope_screen.py`.
- `raw/` — primary-source caches (**gitignored**, ~390 MB): `capitol/`
  (bill pages, committee reports, testimony via Wayback), `csc/` (campaign-
  finance dumps), `dockets/` (LUC SUP dockets, court opinions, lobbyist
  registrations), `edgar/` (HEI proxies), `lurf/` (LURF wayback captures),
  `rpad/` (Honolulu ownership tables), `wind-setbacks/` (ordinances, DPP
  memos).

Hand-curated CSVs (built from documents, not scripts) mark unconfirmed cells
`UNVERIFIED` and carry per-row `source`/`source_urls` columns.
