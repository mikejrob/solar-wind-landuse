> **STATUS (updated 2026-07-17):** Two findings here are now RESOLVED:
> (1) the four scratchpad-dependent scripts (`nonag_classify.py`, `nonag_fig.py`,
> `fetch_ownall.py`, `resolve_owners.py`) were repointed to committed
> `data/intermediates/`, and `join_owner_transmission.py` was added — the non-ag
> and ownership builds now re-run from committed inputs (not from the ephemeral
> tmp scratchpad, which has since been purged). (2) The certified final-HTML md5
> below (`70543cd1…`) is STALE: the paper was regenerated after the accuracy
> corrections; current md5 differs. The byte-identical-on-rerun property still
> holds for a *given* paper state, but the specific hash predates the fixes.
> See `docs/ACCURACY_REVIEW.md`.

# Reproducibility Audit — 2026-07-12

Adversarial audit of `analysis/` against what is committed, gitignored-but-
documented, and actually on disk. Companion register of modeling assumptions:
`docs/ASSUMPTIONS.md`.

## What was verified

- **Row counts:** all 31 CSVs in `docs/DATA_DICTIONARY.md` re-counted with a
  real CSV parser — **all 31 match exactly** (including the quoted-prose
  hand-curated tables and the 115,856-row parcel file).
- **Dry-run reproduction (offline, from cache):** `make_paper_figs.py`,
  `make_expansion_fig_cost.py`, and `assemble_paper.py` were re-run in a
  clean venv. All regenerated outputs are **byte-identical** to the committed
  versions (`f1_cap_scenarios.png`, `f2_distance_bands.png`,
  `f3_ownership.png`, `f_expansion_curve.png`; `land-restrictions-paper-
  final.html` md5 unchanged: `70543cd1…`).
- **Heavy-pipeline caches:** all statically-verified present in `data/gis/`:
  `lsb.parquet`, `slud.parquet`, `lsb_ag.parquet`, `parcels_{oahu,hawaii,
  maui,kauai}.parquet`, `hifld_lines_oahu.geojson`, `osm_power_oahu.json`,
  `oahu_lines_classified.parquet`, `dem/USGS_13_n22w15{8,9}.tif`,
  `dem/oahu_slope_bands.tif`, `pages_*` dumps with `_COMPLETE` markers.
  Output mtimes are consistent with their input chains (no stale outputs
  detected). Working tree is clean vs HEAD.
- **Pipeline order in README:** the 7-step core order is dependency-correct
  (cap_scenarios → transmission_screen → slope_screen →
  transmission_expansion → make_paper_figs → make_expansion_fig_cost →
  assemble_paper).

## Findings — scripts that CANNOT re-run from committed + documented inputs

1. **`nonag_classify.py` / `nonag_fig.py` (steps 8–9 only).** Both read
   session-scratchpad files with **no committed producing script**:
   `urban_candidates_enriched.parquet`, `osm_sites.parquet`,
   `site_tmk_values.csv`, `class_by_tmk.csv` under
   `/private/tmp/claude-503/…/scratchpad/`. Steps 1–7 of the non-ag screen
   (SLUD∩parcel build, slope tabulation, ASMTGIS pull, OSM site pull) exist
   only as prose in `notes/oahu-nonag-solar.md`. So
   `data/oahu_nonag_solar_candidates.csv`, `data/gis/nonag_top_parcels.csv`,
   and `f_nonag_map.png` remain **not reproducible end-to-end**; the two new
   scripts cover only classification and the figure. These scratchpad files
   will disappear on tmp cleanup — copy them into `data/gis/` (they are
   small) or commit the step-1–7 code.
2. **`resolve_owners.py`** reads scratchpad `merged_oahu.csv` (the
   OWNALL×parcel merge), which no committed script produces.
   **`fetch_ownall.py`** writes only to the scratchpad
   (`ownall_rows.csv`), not to `data/raw/rpad/ownall_oahu_ag_rows.csv` —
   that cached file was copied by hand. The merge/copy step is undocumented
   as code.
3. **`data/oahu_owner_class_transmission.csv`** (consumed by
   `make_paper_figs.py` for Figure 3) has **no producing script** — the DATA
   DICTIONARY correctly flags it as a session-built merge and gives the
   recipe (merge the two parents on `tmk` + derive `band46`, `bc_acres`,
   `de_acres`). A 10-line script would close this gap.
4. **`wind_setback_oahu.py` / `wind_viable_map.py`** depend on
   `data/gis/pages_zoning_oahu/`, but **no downloader exists**:
   `cap_scenarios.py`'s `LAYERS` dict has no zoning entry, contradicting
   `wind_setback_oahu.py`'s docstring claim that the layer is "cached by
   cap_scenarios workflow." The download was session-run.

## Findings — README inaccuracies

5. README claims *"`transmission_screen.py` and `slope_screen.py` fetch
   lines and DEM tiles on first run"* — **false**. Neither script contains
   any download code; both hard-require `hifld_lines_oahu.geojson`,
   `osm_power_oahu.json`, and the two `USGS_13_*.tif` tiles to pre-exist in
   `data/gis/`. On a fresh clone these four files (and the zoning pages,
   item 4) must be fetched manually; only `cap_scenarios.py download` is a
   real downloader.
6. README says the final paper embeds *"all nine figures"* — the template
   has **ten** placeholders (`__F1__`–`__F10__`) and ten figures embed.
7. README's core-pipeline list is sufficient only because the figure PNGs
   are committed: `assemble_paper.py` also needs `f_corridors.png`
   (`corridor_candidates.py`), `f_nonag_map.png` (`nonag_fig.py`, see item
   1), and `f_wind_map.png` (`wind_viable_map.py`). README lists the first
   and last as "supporting" but omits `nonag_classify.py`/`nonag_fig.py`
   entirely.

## Findings — portability

8. Every script hardcodes `/Users/michaelroberts/Research/solar-wind-landuse`
   (README discloses this). Four scripts additionally hardcode the
   **ephemeral agent-session scratchpad**
   `/private/tmp/claude-503/-Users-michaelroberts…/scratchpad/`:
   `nonag_classify.py`, `nonag_fig.py`, `fetch_ownall.py`,
   `resolve_owners.py`. These break for any other user *and for this user
   after a tmp purge*.
9. `data/gis/expansion_curve.csv` (09:53) predates the last edit of
   `transmission_expansion.py` (12:35 — the "remove knee framing" figure
   edit). The committed curve was produced by a slightly earlier script
   version; re-running the multi-hour greedy step was not attempted. Figure
   outputs are current (the cost figure re-derives from the CSV,
   byte-identical on re-run).

## Verdict

The core Oahu GIS pipeline (cap scenarios → transmission → slope →
expansion → figures → paper) re-runs offline from cache and reproduces
byte-identically at the figure/paper stage; documentation row counts are
exact. The non-reproducible perimeter is: the non-ag screen's build steps
1–7, the ownership merge inputs, the owner×transmission join, and the
zoning-layer download — all session artifacts. Each is honestly flagged in
the data dictionary, but four of them currently live only in a deletable
`/private/tmp` scratchpad, which is the single most fragile thing in the
repository.
