# Oʻahu Land Use Explorer (static web map)

Deployed at https://mikejrob.github.io/solar-wind-landuse/ (GitHub Pages, from `site/`).

Interactive Leaflet map of Oʻahu agricultural land: parcels with compiled
attributes, LSB soil classes, state land-use districts, HDOA 2020 crop
polygons, USDA/UH Cropland Data Layer rasters (2024, 2025), transmission
lines, existing solar, military land, wind turbines. All Oʻahu parcels load
live from the state GIS service at zoom 15+.

- Data: `data/` (built by `analysis/build_webmap.py`; ~13 MB total).
- App: `index.html`, `app.js`, `style.css` (Leaflet 1.9.4 + esri-leaflet from CDNs).
- Deploy: `.github/workflows/pages.yml` publishes `site/` on pushes to `main`.
  In the repository settings, set Pages → Source → "GitHub Actions". The
  map then serves at `https://mikejrob.github.io/solar-wind-landuse/`.
  The repository is public, so the site and everything in `site/data/`
  (including owners of record) are world-readable by design.
- Local preview: `python3 -m http.server -d site 8000` then open
  http://localhost:8000/.

Rebuild after changing any input table: `.venv/bin/python analysis/build_webmap.py`.
