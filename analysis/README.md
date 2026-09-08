# analysis/

Reproducible Python scripts. Each script's docstring documents sources,
parameters, and caveats; `docs/METHODS.md` summarizes them.

Core GIS pipeline (run in this order):
`cap_scenarios.py` → `transmission_screen.py` → `slope_screen.py` →
`transmission_expansion.py` → `make_paper_figs.py` →
`make_expansion_fig_cost.py` → `assemble_paper.py`.

Supporting: `corridor_candidates.py` (corridor "unlock" ranking),
`fetch_ownall.py` + `resolve_owners.py` (RPAD ownership build),
`campaign_finance_extract.py` (CSC donor classification),
`wind_setback_oahu.py` (Ord. 25-2 wind setback geometry),
`wind_viable_map.py` (map of wind-viable land under Ord. 25-2),
`plantation_footprint.py` (1978-80 ALUM footprint vs zoning/district/LSB;
`--parcel` mode for single-parcel composition),
`osm_footprint_check.py` (OSM solar-array footprints vs SLUD/LSB),
`ag_baseline_overlay.py` (HDOA 2020 ag-use layer × district/soil/parcel/
owner/cap scenarios), `review_area_screen.py` (reviewer-named area screen,
per-parcel size bins, OSM existing-solar footprints), `hcdl_overlay.py`
(NASS Hawaiʻi CDL 2023–25 warped to the repo grid, crossed with HDOA 2020,
soils, parcels; change candidates), `waianae_screen_map.py` (map + elevation
table for the reviewer's Waiʻanae item; `figs/waianae_screen_map.png`),
`build_webmap.py` (exports the `site/data/` layers for the interactive map).

Scripts hardcode the repo root path (`ROOT`/`PROJECT` constants) and re-run
offline from `data/gis/` caches. Figures land in `figs/` (screen figures) and
`figs/paper/` (paper figures F1–F9). Note: `f_nonag_map.png` and
`f_expansion_map.png` inputs were partly built in research sessions — see
`docs/METHODS.md` for provenance.
