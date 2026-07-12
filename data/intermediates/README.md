# data/intermediates/

Session-produced intermediate files, committed so downstream scripts re-run
without the original agent sessions:

- `ownall_rows.csv` — raw Honolulu RPAD OWNALL pull (analysis/fetch_ownall.py output)
- `merged_oahu.csv` — OWNALL joined to ag-district TMKs (input to analysis/resolve_owners.py)
- `urban_candidates_enriched.parquet`, `osm_sites.parquet`, `site_tmk_values.csv` —
  urban-district non-ag screen intermediates (inputs to analysis/nonag_classify.py);
  the upstream screen (urban parcels x slope x RPAD values, OSM special sites) was
  session-built; method documented in notes/oahu-nonag-solar.md and docs/METHODS.md
- `class_by_tmk.csv`, `class_by_site.csv` — viability classifications
  (nonag_classify.py outputs, consumed by nonag_fig.py)

Provenance and caveats: docs/DATA_DICTIONARY.md and notes/oahu-nonag-solar.md.
