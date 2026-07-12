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

## Strategic corridor analysis (added 2026-07-12, slope- and owner-aware)

Script: `analysis/corridor_candidates.py`. Outputs:
`data/gis/oahu_corridor_candidates.csv`, `oahu_ring_1_3km_summary.csv`,
map `analysis/figs/paper/f_corridors.png`.

Method: buildable = slope ≤30% (≤15% also reported), **excluding LSB class
A** (banned for solar with no SUP path — revised 2026-07-12 per Mike;
class-A land can never be unlocked); "unserved" = ag-district land >1 km
from any mapped 46 kV+ line; clusters = 8-connected components on the 10 m
grid, kept if ≥250 buildable ac (16 clusters). Because every
cluster's edge sits ~1 km from the network by construction, ranking uses the
**mean buildable-cell distance to the network** (`km_new_row_46kv`) as the
new-ROW denominator — a spur to the cluster edge does not serve its far
side; the edge (min) distance is also in the CSV. Owner mix joins
`data/oahu_ag_owners.csv` (RPAD-resolved); `n_owners_100ac` counts distinct
resolved owners with ≥100 buildable ac (excluding "Various owners"
aggregates). Rationale: a corridor that unlocks many owners' land increases
PPA-bid competition more than one serving a single estate.

### Top candidates, acres per km of new ROW (buildable ≤30%)

(Class-A exclusion trimmed the big candidates: C01 lost ~3,570 ac (A on its
Schofield/Waialua fringe), C03 Waialua lost ~1,610 ac — 22% of its
previously counted resource was A — and the old Kunia/Bayer cluster shrank
from 963 to 303 buildable ac (mostly A) and fell to the bottom of the
table. C04 Kahuku was essentially unaffected (~12 A ac). Cluster IDs below
are the re-ranked, post-exclusion IDs in the current CSV.)

| Rank | ID | Locality (approx) | Buildable ac ≤15/≤30 | MW@5 | %D/E | mean ROW km | ac/km | owners ≥100ac | Top owners |
|---|---|---|---|---|---|---|---|---|---|
| 1 | C01 | Waianae Range mauka + central plateau fringe | 9,742/14,210 | 2,842 | 55 | 3.9 | 3,644 | 18 | US Govt 26%, Island Palm (Army PPP) 12%, Corteva 10% |
| 2 | C03 | Waialua | 4,835/5,697 | 1,139 | 26 | 2.0 | 2,781 | 5 | Laukiha'a ag CPR 34%, Dole 26%, Kamehameha Schools 19% |
| 3 | C02 | Lualualei | 6,479/8,749 | 1,750 | 94 | 3.6 | 2,423 | 5 | **US 55% (majority federal)**, State 10%, DHHL 5% |
| 4 | C04 | Kahuku | 3,132/5,618 | 1,124 | 48 | 2.5 | 2,237 | 4 | US 36%, Property Reserve (LDS) 33%, State 15% |
| 5 | C06 | Pupukea/Waimea | 1,318/1,700 | 340 | 45 | 2.1 | 797 | 1 | Kamehameha Schools 99% |

### Top candidates, distinct-owners-unlocked per km (competition metric)

C01 (4.6 owners/km), C03 (2.4), C04 (1.6), C13 Waipio/Waiawa (1.5),
C02/C10 (1.4). **C03 (Waialua) remains the standout commercially
competitive unlock**: ~2 km of new/upgraded ROW from the Waialua 46 kV
corridor reaches ~5,700 buildable ac split across five substantial owners
(Dole, Kamehameha Schools, an ag-CPR community, plus state parcels), now
74% B/C after removing its class-A core — i.e. it is even more clearly the
cluster whose value depends on cap reform (S3). C01's owner count (18)
overstates commercial competition: it merges Schofield-plateau fringe land
where the owner list is heavily military/federal-adjacent and where
unmapped 46 kV likely already exists.

Majority-federal clusters (flagged in CSV, not commercially leasable in
practice): C02 Lualualei (Navy), C07 Ewa/Puuloa (Navy), C08
Pearl City/Waiau mauka (US 93%), C10 Kahuku point (FWS), C15
Helemano (US).

### The cheap upgrades: buildable land in the 1–3 km ring

Land servable by short 46 kV spurs / in-ROW reconductoring (Mike's
premise), by soil group:

| Group | Buildable ac ≤15% | Buildable ac ≤30% |
|---|---|---|
| B/C (capped; S3-relevant) | 10,686 | 11,842 |
| D/E (uncapped) | 7,341 | 12,177 |

(Class A — 4,762/4,866 ac in the ring — is excluded from "buildable"
throughout; it can host no solar under any path. The B/C and D/E rows were
already A-free and are unchanged by the revision.)

**28 distinct resolved owners** hold ≥100 buildable (≤30%) ac in the ring
(was 31 before excluding class-A acreage from the ≥100 ac test).
The ring contains ~24,000 buildable acres (~4,800 MW @5 ac/MW envelope) —
more than any single new-corridor cluster — and it is dispersed across
many owners, supporting the view that incremental 46 kV work dominates
greenfield corridors on both cost and competition before any big new ROW
is justified.

### Caveats specific to this section

- 46 kV under-mapping cuts BOTH ways here: it inflates "unserved" clusters
  (parts of C01's plateau fringe and the Ewa/Pearl City-fringe clusters are
  probably already within 1 km of a real line) AND understates the 1–3 km
  ring. Treat the urban-fringe clusters (C07, C08, C14) as likely
  artifacts; C02/C03/C04/C05/C06/C09/C11 are robust (far even from the
  reliable 138 kV network).
- "km of new ROW" is straight-line; real routes follow roads/terrain.
- Owner shares are of buildable ≤30% acres, from the RPAD owner file
  (confidence flags in `oahu_ag_owners.csv`); unparceled cluster area is
  unattributed.
- No hosting-capacity, substation, or land-use-entitlement information.

## Budget-constrained expansion curve (added 2026-07-12, greedy heuristic)

Question: given a budget of L km of NEW line, branching off the existing
mapped 46 kV+ network or off previously built expansion, where should it go
to maximize B/C/D ag-district acreage (class A excluded — solar banned;
class E excluded per spec) brought within 1 km of a line, counting only
land passing the ≤30% slope screen (≤15% variant also tracked)?

Script: `analysis/transmission_expansion.py`. Outputs:
`data/gis/expansion_curve.csv` (per-step log with segment WKT, EPSG:26904),
`data/gis/expansion_segments.parquet`,
`analysis/figs/paper/f_expansion_curve.png`,
`analysis/figs/paper/f_expansion_map.png`.

### Method (an approximation — stated plainly)

- Eligibility raster: 10 m LSB class ∈ {B,C,D} within the ag district ×
  slope band, aggregated to eligible-acres per 100 m cell. Total eligible:
  40,870 ac at ≤30% slope; 35,042 ac at ≤15%.
- Coverage function: 100 m cells within a 10-cell (1 km) disk of any
  network cell. Network = mapped 46 kV+ lines (HIFLD+OSM, rasterized,
  all_touched) ∪ built expansion. Coverage is evaluated on the 100 m
  lattice, so acreages differ slightly (<~1%) from the 10 m
  polygon-buffer numbers elsewhere in this file.
- Greedy growth, ≤1 km committed per step: each iteration scores every
  reachable cell q by [uncovered eligible acres in the 1 km disk at q] /
  [slope-aware shortest-path length from the current network to q]
  (multi-source Dijkstra, 8-connected; entering a cell that is >30% steep
  over >30% of its area costs 6× its geometric length — the router avoids
  steep ground but may cross it). The top ~15 candidates are re-scored
  exactly (full path tube stamped against the uncovered map) and the best
  path is committed in a ≤1.0 km increment. Budget charged = geometric km,
  not penalized cost. Branching and spur extension are automatic (every
  network cell is a Dijkstra source).
- Long approach runs therefore appear as several near-zero-gain steps
  followed by a jump when a far cluster comes into range — the marginal
  series is mostly non-increasing with occasional local jumps (the clearest:
  reaching the Waiawa cluster at cum ≈ 37 km, +406 ac/km).

### Results

Baseline (L=0): **16,328 ac** of B–D ≤30% land within 1 km of the mapped
46 kV+ network (14,171 ac at ≤15%) — 40% of all eligible land.

| L (km) | ac ≤30% | added | avg ac/km | ac ≤15% | share of eligible |
|---|---|---|---|---|---|
| 0 | 16,328 | — | — | 14,171 | 40% |
| 10 | 20,185 | +3,857 | 386 | 17,833 | 49% |
| 25 | 24,195 | +7,868 | 315 | 21,374 | 59% |
| 50 | 29,481 | +13,153 | 263 | 26,150 | 72% |
| 75 | 33,278 | +16,950 | 226 | 29,190 | 81% |
| 100 | 36,103 | +19,775 | 198 | 31,507 | 88% |

Knee: **≈5.7 km** (18,580 ac), the maximum of the 5-step (~3–4 km)
centered moving average of marginal ac/km (434 ac/km); the best single
committed segments (476–483 ac/km) also sit at km 4.7–5.2. Justification:
marginal payoff holds a ~400 ac/km plateau from 0 to ~11 km, then declines
— it never again sustainably exceeds the plateau (the km-37 Waiawa jump
peaks at 406 ac/km for ~5 km). So the practical knee budget is ~6–11 km;
**L=10 km is the round-number knee** (+3,857 ac at 386 ac/km average).
No mid-curve jump beats the early spurs: the best opportunities are short
spurs off the existing network, not long new corridors.

Geography of the first ~6 km (see f_expansion_map.png): three short spurs —
(1) ~2.2 km at **Waialua**, pushing mauka/south from the Waialua 46 kV
loop (the C03 unlock from the corridor analysis above); (2) ~2.9 km down
the **Kunia / central-plateau** spine south of Schofield; (3) ~0.6 km at
**Kahuku**. Together +2,252 eligible ac over baseline. The 10–25 km range
keeps thickening Waialua/Kunia and the plateau fringe toward the Waianae
Range (C01); ~35–42 km reaches **Waiawa/Waipio** (C13); the 75–100 km tail
buys Mokuleia and progressively worse remnants.

### Caveats (prominent, repeat wherever used)

- **Electrical realism: none.** Line capacities, substation headroom, and
  interconnection engineering are unknown; these are geometric routes only.
- **The public 46 kV map is incomplete**, so baseline coverage is
  understated and some "expansion" km may duplicate real unmapped lines —
  especially the urban-fringe and plateau segments. The curve is best read
  as an upper bound on what new geometry can add.
- **Greedy is approximate** (no look-ahead, no segment swaps); the true
  optimum for a given L can only be (weakly) better.
- **The 1 km service radius is a simplification** of interconnection cost;
  results scale with that assumption.
- Routing avoids >30%-slope cells via a 6× cost penalty rather than a hard
  ban; committed routes may still clip steep ground.
