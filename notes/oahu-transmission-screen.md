# Oahu ag land × distance to transmission: cross-tabs and "unlock" candidates

Run date: 2026-07-11. Script: `analysis/transmission_screen.py` (re-runs
offline from `data/gis/` cache). Map: `analysis/figs/oahu_transmission_screen.png`.

## Line data: sources, cross-check, classification

No public HECO or State GIS layer carries Oahu line routes (checked HECO
2018 AGOL service = service-area polygon only; state Infrastructure
MapServer has no electric layers). Two public sources used, cached in
`data/gis/`:

1. **HIFLD Open** "US Electric Power Transmission Lines"
   (services2.arcgis.com/FiaPA4ga0iQKduv3, source dates 2017–2020): 91 Oahu
   features, all owner = Hawaiian Electric. VOLTAGE/VOLT_CLASS: 40 features
   classifiable as 138 kV (`VOLTAGE==138` or class 100–161), 36 "UNDER
   100", 15 unknown.
2. **OpenStreetMap** power=line/minor_line ways (Overpass API, fetched
   2026-07-11): 87 ways; 30 tagged 138000 V, 14 tagged 46000 V, 43 untagged.

**Cross-check**: HIFLD 138 kV and OSM 138 kV agree exactly (median
separation 0 m) → the 138 kV network (~325 km of routes) is reliable.
The 46 kV picture is poor in both sources: HIFLD "UNDER 100" (53 km) and
OSM 46 kV (25 km) barely overlap each other (median mutual distance
~6.7 km) — each maps different fragments of HECO's several-hundred-km
46 kV system. **Classification used**: 138 kV = HIFLD/OSM 138-tagged;
"46 kV+" = union of everything mapped in either source (138 kV + all
sub-transmission fragments). Distances to the 46 kV+ network are therefore
**upper bounds** (true distances are shorter wherever real 46 kV lines are
unmapped); far-from-grid acreage at the 46 kV tier is overstated,
especially near the urban fringe. 138 kV-based numbers are the solid ones.

## Method

- CRS EPSG:26904; acres from projected geometry (as in cap analysis).
- Ag-district LSB polygons (Oahu) from the cap-analysis cache
  (`lsb_ag.parquet`).
- Class × band cross-tab computed polygon-accurately (LSB polygons ∩
  1/3/5 km buffer rings of the network) — not by parcel assignment.
- Parcel distances: boundary (not centroid) distance from each of the 6,274
  ag-district Oahu parcels to nearest 46 kV+ feature and nearest 138 kV
  feature (0 if a line crosses the parcel).
- Eligible-acres-by-band uses the parcel's minimum distance (a large parcel
  spans bands; its whole eligibility is assigned to its nearest band —
  slight near-grid bias, noted).
- Clusters: connected components of ag-district LSB land minus the 3-km
  buffer of the 46 kV+ network, components >100 ac; per-cluster LSB-class
  acreage, distance/bearing from cluster edge to nearest mapped line,
  nearest HIFLD corridor (substation endpoint names), and acres per km of
  new ROW (cluster acres ÷ extension length to cluster edge).

## Cross-tab: ag-district acres by LSB class × distance band

To the **46 kV+ (all mapped) network**:

| LSB class | 0–1 km | 1–3 km | 3–5 km | >5 km |
|---|---|---|---|---|
| A (banned) | 8,497 | 4,916 | 1,063 | 630 |
| B | 11,690 | 7,876 | 2,551 | 1,060 |
| C | 2,254 | 4,402 | 3,596 | 1,448 |
| D | 2,762 | 2,441 | 1,586 | 1,679 |
| E | 17,597 | 17,762 | 10,490 | 10,758 |

To the **138 kV network only**:

| LSB class | 0–1 km | 1–3 km | 3–5 km | >5 km |
|---|---|---|---|---|
| A | 2,922 | 2,211 | 378 | 9,594 |
| B | 2,059 | 3,055 | 5,364 | 12,698 |
| C | 574 | 1,080 | 2,186 | 7,860 |
| D | 1,328 | 989 | 716 | 5,435 |
| E | 7,496 | 5,652 | 3,810 | 39,650 |

Readings:

- **B/C (the capped resource)**: 13,944 ac within 1 km of a mapped 46 kV+
  line; 26,222 ac (75%) within 3 km. Grid access is not the binding
  constraint for most B/C land — the statutory cap is.
- **D/E near grid — the zero-legal-friction resource**: 20,359 ac of D/E
  ag-district land lies within 1 km of a mapped 46 kV+ line (40,562 ac
  within 3 km). At 5–7 ac/MW that is ~4,100–2,900 MW of siting envelope
  with **no acreage cap and no SUP requirement** (§ 205-4.5(a)(20) does not
  constrain D/E). Even the pessimistic 138 kV-only screen leaves 8,824 ac
  of D/E within 1 km (~1,750 MW @5). Caveat: E includes steep
  gulch/mountain land — no slope screen applied, so these are upper bounds
  on physically usable land.
- Under current law (S0) only 3,601 ac of B/C is as-of-right eligible
  island-wide; 2,306 ac of that (64%) is already within 1 km of a mapped
  line, 82% within 3 km. Under S3 (20%, no hard cap): 11,234 of 15,657 ac
  within 1 km (72%), 89% within 3 km. **Liberalizing the cap
  disproportionately unlocks near-grid land** — the far bands hold little
  B/C.

Eligible acres by band (S0/S3): `data/gis/oahu_eligible_by_band.csv`.
Parcel-level output (TMK-keyed, joins to `data/oahu_ag_owners.csv`):
`data/oahu_land_transmission.csv` (tmk, parcel_acres, a–e acres,
s0/s3 eligible acres, dist_46kv_km, dist_138kv_km).

## "Unlock" candidates: far clusters ranked by acres per km of new line

Full table: `data/gis/oahu_unlock_clusters.csv` (13 clusters >100 ac;
`ext_km` = new-ROW length from the nearest existing corridor to the
cluster edge; MW computed on B/C + D/E acres at 5 ac/MW).

Top by acres/km:

| # | Cluster (approx locality) | Acres (A/BC/DE) | MW @5 | Ext | Dir | Nearest corridor |
|---|---|---|---|---|---|---|
| 1 | Waianae Range mauka (Makaha–Waianae Kai–Kaena side) | 14,368 (1,551/2,789/10,029) | 2,563 | 3.0 km | NE | Wahiawa 46 kV+ |
| 2 | Lualualei–Nanakuli valleys | 6,950 (126/225/6,599) | 1,365 | 3.0 km | W | Kahe 1 – Kahe 2 138 kV |
| 3 | Koolauloa mauka (Laie/Malaekahana) | 2,763 (9/747/2,007) | 551 | 3.0 km | N | Mauka FIT One 46 kV+ |
| 4 | Central plateau mauka (Helemano/Poamoho) | 1,536 (0/695/842) | 307 | 3.0 km | S | Helemano-area 46 kV+ tap |
| 5 | Windward Waiahole/Waikane mauka | 2,852 (0/983/1,869) | 570 | 5.6 km | S | Halawa ("HAIAWA") 138 kV |

Interpretation, with the data-quality caveat applied:

- **Cluster 1 (Waianae Range)** is the largest by far but is mostly class E
  mountain land — much of it likely too steep; treat its MW ceiling as
  nominal. The B/C fringe (2,789 ac) on its Waialua/Schofield edge is the
  realistic target and is close to the Wahiawa sub-transmission corridor.
- **Cluster 2 (Lualualei)** is flat valley floor D/E — physically
  attractive, ~3 km of new ROW from the Kahe 138 kV corridor; but a large
  share of Lualualei is U.S. Navy land (check against the owners file
  before ranking it as commercially unlockable).
- **Cluster 3 (Koolauloa)** and **cluster 5 (Waiahole/Waikane)** are
  windward; #5 needs the longest extension (5.6 km) but contains ~1,000 ac
  of B/C — under S3 it becomes a meaningful unlock; under current S0 the
  cap makes the extension pointless (a 20-ac ration cannot pay for km of
  new 46/138 kV line — the cap and the grid screen interact).
- Two Ewa-plain pockets (Kalaeloa–Ewa Nui, ~1,345 ac with 1,282 B/C; Ewa
  Nui–Waiau, ~1,065 ac with 908 B/C) rank high on paper but sit in the
  urban fringe where the mapped-46 kV gap is most likely spurious — these
  are probably already-served land, i.e. artifacts of source
  incompleteness, not real unlock candidates.

## Caveats

- **Public line data lacks capacity/amperage** — a "near a line" screen says
  nothing about hosting capacity, conductor rating, or substation bay
  availability. Mike's premise (in-ROW upgrades are relatively easy) is the
  justification for using route proximity at all.
- Routes are approximate (HIFLD digitized from imagery; OSM volunteer
  data); vintages 2017–2020 (HIFLD) / live (OSM).
- **46 kV network is materially under-mapped** in both sources; 46 kV+
  distances are upper bounds and the far-cluster list at the 46 kV tier is
  over-inclusive (see Ewa pockets above). 138 kV results are robust
  (two sources agree).
- Distribution-level (12 kV) interconnection for CBRE-scale projects is out
  of scope.
- No flood/military/conservation-overlay screening. Parcel ≠ project; SUP
  path above the cap exists since 2014.
- **Slope screen added 2026-07-12** (`notes/oahu-slope-screen.md`): the
  20,359 ac of near-grid D/E falls to 6,083 ac at ≤15% slope and 11,110 ac
  at ≤30%; S3-eligible B/C land is ~90% ≤15% slope, so the cap-reform
  result is essentially slope-robust.
- Eligible-by-band table assigns whole parcels to their nearest band
  (near-grid bias for very large parcels); the class × band cross-tab is
  polygon-accurate and does not have this issue.

## Files

- `analysis/transmission_screen.py` — full pipeline (lines → cross-tabs →
  parcel distances → clusters → figure)
- `data/oahu_land_transmission.csv` — parcel level, TMK-keyed
- `data/gis/oahu_class_by_band.csv` — class × band, both networks
- `data/gis/oahu_eligible_by_band.csv` — S0/S3 eligible acres by band
- `data/gis/oahu_unlock_clusters.csv` — ranked cluster table
- `data/gis/oahu_lines_classified.parquet`, `hifld_lines_oahu.geojson`,
  `osm_power_oahu.json` — line data cache
- `analysis/figs/oahu_transmission_screen.png` — map
