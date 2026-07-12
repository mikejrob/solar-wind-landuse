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
`wind_viable_map.py` (map of wind-viable land under Ord. 25-2).

Scripts hardcode the repo root path (`ROOT`/`PROJECT` constants) and re-run
offline from `data/gis/` caches. Figures land in `figs/` (screen figures) and
`figs/paper/` (paper figures F1–F9). Note: `f_nonag_map.png` and
`f_expansion_map.png` inputs were partly built in research sessions — see
`docs/METHODS.md` for provenance.
