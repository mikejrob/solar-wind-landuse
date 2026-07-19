# Oahu golf courses and utility-scale solar

Date: 2026-07-19. Reference examining the blanket golf-course EXCLUSION in the
non-ag urban solar screen (`notes/oahu-nonag-solar.md`, which netted out all
golf/country-club acreage by owner keyword regardless of operating status).
This inventories every Oahu golf course, flags operating status and
redevelopment trajectory, and quantifies the viable solar subset. Treated as
data; sources cached under `data/raw/military-golf/` (MANIFEST.md).

Outputs: `data/oahu_golf_courses.csv` (36 courses), `analysis/figs/paper/
f_golf_courses.png`. Scripts: `analysis/golf_course_screen.py`,
`golf_finalize.py`. GIS: OSM leisure=golf_course (Overpass), cached slope
raster + transmission lines, SLUD, Honolulu zoning layer 3, RPAD OWNALL owners.

## 1. Inventory

**36 golf-course polygons mapped in OSM; 5,838 ac total, 5,230 ac at <=15%
slope.** Three OSM-unnamed polygons identified via TMK owner + location:
Barbers Point GC (Navy/Kalaeloa), Mid-Pacific CC (KS land, Lanikai —
UNVERIFIED exact polygon), Olomana Golf Links (State land, Waimanalo). The
research memo lists ~41 courses incl. small/military and historically closed
ones (Kalakaua-Army closed 2004→housing; Ford Island-Navy defunct→housing)
that predate or fall outside the OSM polygon set — noted, not in the CSV.

Per-course rows (name, status, solar_side, acres, acres_le15/le30,
dist_46kv/138kv, SLUD, Honolulu zone_class, owner, redevelopment,
viability_flag, TMK, note, source) are in `data/oahu_golf_courses.csv`.

**Operating status: 34 open, 2 closed.**

| CLOSED course | ac | ac<=15% | solar side | km to 46kV+ | SLUD / zone | owner | trajectory |
|---|---:|---:|---|---:|---|---|---|
| Ko'olau Golf Club | 221 | 111 | windward/wet (poor) | 0.0 | Conservation / P-1 | First Presbyterian Church | closed 9/30/2020; plan farming/native habitat/cultural-ed via CDUP; **NO housing** |
| Makaha Valley CC | 158 | 131 | leeward/sunny (good) | **6.7** | Urban / P-2 | Makaha Golf & Resort LLC (KH Group) | Championship course closed ~2011; 664-ac resort sold Aug 2022 $20.7M; **~494 homes + 152 condos planned**; East course still open |

Insolation proxy (leeward-sunny vs windward-wet) is location-based
(rain-shadow leeward = Waianae/Ewa/Kapolei/Kalaeloa/Kunia/south Honolulu;
orographic-wet windward = Kaneohe/Kailua/Waimanalo/Maunawili/upper Nuuanu;
north-shore Kahuku marginal). Confirmed via NWS/WRCC; use NREL NSRDB for
citable irradiance if this becomes load-bearing.

Notable ownership/land-use (institutional-landholder thread):
**Kamehameha Schools** took Pearl Country Club back in-house at ground-lease
expiry (2020) and reinvested to KEEP it in golf (reopened 2024, Troon-run) —
a landholder choosing golf over both solar and redevelopment on a large,
grid-adjacent parcel. Several courses under Korean/Japanese ownership (Makaha,
Waikele, 360 Ewa Beach, Mililani, Hoakalei, Hawaii Prince). **Ala Wai** (open,
C&C muni) faces the USACE Ala Wai flood-control project that would convert the
ENTIRE course to a detention basin (~$1-11B, under review) — a non-solar
land-use claim on the biggest flat close-in golf parcel.

## 2. Screen correction and viable subset

How much golf acreage the non-ag screen subtracted, by district:

| SLUD district | courses | acres | ac <=15% |
|---|---:|---:|---:|
| Urban (netted out of the non-ag screen) | 26 | 4,074 | 3,753 |
| Ag (inside the ag universe already) | 7 | 1,247 | 1,085 |
| Conservation (Ko'olau, Pali, Honolulu CC) | 3 | 517 | 392 |
| **total** | **36** | **5,838** | **5,230** |

The non-ag urban screen's golf exclusion removed **~4,074 urban ac (3,753
flat)** — but 26 of those 26 courses are **OPEN and operating**; removing
operating golf is defensible (it is not fallow land available for solar).

**Viable subset = closed + leeward/sunny + flat (>=10 ac <=15%) + near-grid
(<=3 km 46kV+) + NOT in a housing/flood/military pipeline = ZERO courses.**
The two closed courses each fail on a different axis:
- **Ko'olau** is windward/wet and cliff-shadowed (poor insolation) and
  Conservation-zoned (P-1); its owner is converting it to farming/conservation,
  not solar. Physically near-grid (0 km) but low-value solar land.
- **Makaha** is leeward/sunny and flat — the one closed course with good solar
  physics — but it is **6.7 km from the nearest mapped 46 kV+ line** (grid-cost
  prohibitive) AND is in an active **housing-redevelopment pipeline** (~646
  planned units). Housing contests it; it is not idle land.

**Closed courses on Oahu churn toward housing (or conservation). They do not
become idle land a solar developer could take.** Kalakaua
(Army, 2004) and Ford Island (Navy) both became housing; Makaha is following;
Ko'olau went to conservation. A closed AG-zoned course would be legally fallow
ag land, but no such case exists on Oahu today (the closed courses are
Conservation- and Urban/P-2-zoned).

## 3. Overlap with existing screens — how much NEW acreage?

- The **26 Urban-district courses (3,753 flat ac)** were already inside the
  non-ag screen's universe and explicitly netted out by owner keyword — **not
  new supply**; this note confirms the subtraction was justified (they are
  operating).
- The **7 Ag-district courses (1,085 flat ac)** are inside the paper's ag
  parcel universe (`notes/oahu-ownership.md`) — **double-count with the ag
  screen**, not additional.
- **Net NEW near-grid flat acreage golf adds beyond the paper: ~0.** The
  actionable increment is the viable subset, which is **zero acres** today:
  the only closed leeward-flat course (Makaha) is grid-distant and
  housing-bound.

## Viable-acreage estimate

**~0 acres** of golf land are a utility-scale solar candidate on Oahu
today. If Makaha's grid distance and housing plan are both set aside — a strong
counterfactual — it offers ~131 flat leeward acres (~20-25 MW), but that
competes directly with ~646 planned homes. Golf
courses, closed or open, do not add meaningful new solar supply and are
contested by housing where the solar physics is good.

## Caveats

- OSM polygon completeness: 36 of ~41 known courses; small/military/defunct
  courses (Kalakaua, Ford Island, some par-3s) not in the polygon set.
- Per-course acreage from OSM geometry (relation holes handled); status,
  ownership, and redevelopment from web reporting — several acreages and
  entities remain UNVERIFIED against primary TMK/BOC records (flagged in CSV).
- Owner = RPAD OWNALL assessment owner (tax year 2027), not beneficial owner.
- 46 kV distances are UPPER bounds (network under-mapped); 138 kV solid.
- Three OSM-unnamed polygons identified by TMK owner + location; Mid-Pacific CC
  match is UNVERIFIED.
