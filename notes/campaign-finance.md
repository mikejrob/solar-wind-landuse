# Campaign finance: contributions to legislators who controlled solar/wind siting bills

Date: 2026-07-11. Documents money FLOWS only. Correlation ≠ influence; no motive
claims are made or implied. Nulls reported explicitly.

## Data source and provenance (important — the archive moved)

The Hawaii Campaign Spending Commission (CSC) contributions microdata formerly at
`data.hawaii.gov/resource/jexd-xbcg` is no longer there: data.hawaii.gov is now a
WordPress site. The live Socrata instance is **hicscdata.hawaii.gov** (Tyler Data
& Insights), same dataset ID:

- Live: https://hicscdata.hawaii.gov/resource/jexd-xbcg.json
  ("Campaign Contributions Received By Hawaii State and County Candidates") —
  but in 2025 CSC **truncated it to Jan 1 2015 forward** (only ~6.6k pre-2015
  rows survive, from amended reports). Same truncation on the CKAN mirror
  (opendata.hawaii.gov, resource 443bd998-1ef3-47da-9170-c2c376b2e41c). The
  2006–2014 archive is not published anywhere official as of 2026-07.

- **2006–2024 recovery**: Internet Archive capture (2025-03-31) of the CKAN
  datastore dump taken BEFORE truncation:
  `https://web.archive.org/web/20250331165634id_/https://opendata.hawaii.gov/datastore/dump/443bd998-1ef3-47da-9170-c2c376b2e41c`
  → saved as `data/raw/csc/wayback_contrib_dump_20250331.csv`.
  218,392 rows, transactions 2006-11-08 → late 2024, alphabetically complete
  (A "Abbett" → Z "Zibakalam"). This is official CSC data (Schedule A filings),
  merely retrieved via the Archive; cite as CSC data, IA capture 2025-03-31.

- Top-up for post-capture dates: live SODA API pulls per candidate reg-no,
  cached as `data/raw/csc/live_<REGNO>.json`; deduped against the dump on
  (reg_no, contributor, date, amount).

Pipeline: `analysis/campaign_finance_extract.py` (rerunnable; polite 1s delay).

## Target candidates (CSC registrant numbers)

SB631/Act 217 era, window 2006-11-01 → 2014-12-31:
Gabbard, Mike CC10279 (Sen ENE chair 2011) · Nishihara, Clarence CC10159 (Sen AGL
chair) · Dela Cruz, Donovan CC10171 (Sen WLH chair) · Solomon, Malama CC10802 ·
Ige, David CC10147 (Sen; 2014 Governor run included) · Kahele, Gilbert CC10801 ·
Kidani, Michelle CC10494 · Kim, Donna CC10254 (Donna Mercado Kim) · Slom, Sam
CC10287 · Coffman, George CC10359 (House EEP chair — CSC lists Denny Coffman
under legal first name George; confirmed by Kona donor geography and 2008–2014
House election periods; flag: name-match, high confidence) · Chang, Jerry CC10168
(House WLO chair) · Tsuji, Clifton CC10217 (House AGR chair).

Honolulu Council (wind-setback bills), window 2012-01-01 → 2024-12-31:
Tsuneyoshi, Heidi CC11195 · Kiaaina, Esther CC11549 (also her OHA reg CC11363,
office column disambiguates) · Waters, Tommy CC11024 · Tupola, Andria CC10995
(one reg spans House/Governor/Council — office column disambiguates).

11,834 contribution rows in-window across all targets; 730 classified
($778,572; 675 high-confidence, 55 medium).

## Donor classification (regex on committee/contributor name + employer field)

- `hei_utility`: Hawaiian Electric CEG (fka HEI CEG — HEI's registered
  noncandidate committee, per CSC NCC registry) + employees of HEI/HECO/MECO/HELCO.
- `hei_person`: HEI directors/named executive officers matched by personal name
  (roster from HEI DEF 14A proxies in data/raw/edgar/): Lau, Watanabe, Rosenblum,
  Ajello, Alm, Fargo, Taniguchi, Taketa, etc. Confidence medium unless employer
  field corroborates.
- `hei_asb`: American Savings Bank (HEI subsidiary) — none found in-window.
- `utility_other`: NextEra (cable proponent 2012; HEI acquirer-bid 2014) —
  deliberately NOT counted as solar/wind.
- `landholder_dev`: KS/Bishop Estate, A&B (HIPAC), Castle & Cooke Legislative
  Committee, D.R. Horton/Schuler, James Campbell Co, Grove Farm, Parker Ranch,
  Maui Land & Pine, LURF, Ulupono, Kobayashi Group, Stanford Carr, Hunt Cos, etc.
- `ag_seed`: Monsanto, Syngenta, DuPont/Pioneer, Dow Agro/Dow Chemical PAC,
  BASF, Hawaii Farm Bureau, HC&S, HARC.
- `solar_wind`: HSEA (+ its PAC), First Wind, RevoluSun, SunPower PAC, The
  Alliance for Solar Choice, SunEdison, SolarCity, Sunrun, Eurus, Sempra
  (Auwahi Wind developer; medium), Solar Hub Utilities, generic "solar" employer
  (medium).
- `union_construction`: Carpenters (HRCC/Local 745), Laborers, Ironworkers 625,
  Operating Engineers Local 3 (+ industry "stabilization funds" — note these are
  joint labor-management funds), IBEW 1186, Plumbers & Fitters, Painters 1791,
  Masons 630, Sheet Metal 293, Tapers 1944, Glaziers.

Excluded on purpose: non-construction unions (ILWU 142, HGEA, UPW, UNITE HERE 5,
HSTA, Teamsters) — present in the data in volume but not in scope; generic
commercial/resort developers (MacNaughton, Ko Olina) unless on the landholder
list; law firms (e.g., Alston Hunt, Watanabe Ing appear only via flagged
individuals); BioEnergy Hawaii and Innovations Development Group (biomass/
geothermal — not solar/wind).

## Headline findings (classified $ per candidate, whole window)

| Candidate (window) | Total raised | HEI all | Landholder/dev | Ag/seed | Solar/wind | Constr. unions |
|---|--:|--:|--:|--:|--:|--:|
| Ige (06–14, incl. 2014 Gov run) | 2,142,597 | 9,350 | 30,900 | 3,500 | 13,100 | 70,400 |
| Tupola (12–24) | 1,076,432 | 0 | 11,000 | 0 | 0 | 24,000 |
| Waters (12–24) | 1,048,223 | 1,250 | 47,250 | 0 | 2,000 | 95,500 |
| Dela Cruz (06–14) | 386,051 | 225 | 22,300 | 8,075 | 750 | 40,950 |
| Kiaaina (12–24) | 364,528 | 1,250 | 18,000 | 0 | 250 | 60,250 |
| Kidani (06–14) | 360,426 | 100 | 4,700 | 7,500 | 250 | 55,300 |
| Tsuneyoshi (12–24) | 342,332 | 0 | 7,951 | 0 | 0 | 23,000 |
| Kim (06–14) | 295,650 | 400 | 9,500 | 2,750 | 1,200 | 19,400 |
| Solomon (06–14) | 209,184 | 375 | 2,850 | 4,850 | 150 | 31,350 |
| Kahele (06–14) | 201,156 | 300 | 600 | 3,150 | 0 | 27,650 |
| Nishihara (06–14) | 199,934 | 500 | 1,900 | 6,750 | 0 | 28,350 |
| Tsuji (06–14) | 162,195 | 200 | 3,350 | 9,550 | 0 | 9,000 |
| Gabbard (06–14) | 119,003 | 325 | 3,000 | 0 | 3,000 | 28,422 |
| Chang (06–14) | 74,806 | 0 | 2,650 | 1,500 | 0 | 3,600 |
| Coffman (06–14) | 67,713 | 50 | 800 | 150 | 250 | 9,400 |
| Slom (06–14) | 65,627 | 0 | 0 | 700 | 0 | 0 |

(Per-cycle breakdown in data/campaign_contrib_summary.csv.)

Classified interests are a SMALL share of most
war chests (typically 2–10%; construction unions are the largest classified
block for nearly everyone).

### 1. HEI money is minimal — a headline NULL
- HEI's PAC ("HEI CEG", now "Hawaiian Electric CEG") gave only token sums:
  $100–$500 per gift, and to only 6 of 16 targets in-window.
- **Around the 2011 session (2010-11-01 → 2011-12-31), HEI-affiliated money to
  the three Senate chairs who handled SB 631 (Gabbard, Nishihara, Dela Cruz)
  was ZERO.** Total HEI-affiliated flow to all 12 SB631-era legislators in that
  window: $250 (HEI CEG $150 + Robbie Alm $100, both to Ige).
- Largest HEI-affiliated total anywhere: Ige's 2014 gubernatorial run, $9,350
  (HEI CEG $150/$250-scale gifts plus executives: C. Lau $1,000, R. Rosenblum
  $1,000, J. Watanabe $2,500 [medium confidence — employer "Watanabe Ing"],
  T. Sekimura $100, and small employee gifts).
- The rate-base hypothesis gets NO support from candidate-level campaign money.

### 2. Seed/ag money tracked the ag-committee gatekeepers
Monsanto, Syngenta, DuPont/Pioneer and Dow gave steadily and almost exclusively
to the legislators controlling ag-land bills: Tsuji (House AGR chair) $9,550,
Dela Cruz $8,075, Kidani $7,500, Nishihara (Sen AGL chair) $6,750, Solomon
$4,850, Kahele $3,150. In the 2011-session window alone: $7,500 across 8 of the
12 legislators (e.g., Monsanto to Nishihara 2011-04-26, to Chang 2011-04-29, to
Dela Cruz 2011-07-05). CAVEAT: seed companies were then major lessees of prime
ag land, but 2011–2014 was also the GMO-labeling/pesticide fight era — these
flows cannot be attributed to Chapter 205 siting rather than GMO politics.
Document only: the ag-land committee chairs were funded by ag-land lessees.

### 3. Landholders/developers: steady, modest, broad
A&B's HIPAC and Castle & Cooke's Legislative Committee gave small amounts
($100–$500) to nearly every target (A&B HIPAC appears for 15 of 16). Largest
landholder/dev totals sit with Honolulu Council members (Waters $47k — much of
it a Kobayashi Group family/executive cluster — and Kiaaina $18k) and Dela Cruz
($22.3k, incl. $4.5k from three Kobayashi Group donors on 2011-07-05).
Kamehameha Schools: only 2 employee gifts found ($ small); its execs are
NOT visible funders of these legislators.

### 4. Solar/wind industry money: small and mostly 2014, to Ige
$13.1k of Ige's $2.14M (0.6%) — TASC, RevoluSun, SunPower PAC, First Wind,
SunEdison, Eurus, SolarCity — nearly all Sep–Nov 2014 (gubernatorial). Around
the 2011 session: First Wind $1,000 to Gabbard (2010-11-06), HSEA PAC $200 to
Kim, HSEA $500 to Ige. Wind developer money to the 2011 chairs otherwise absent.

### 5. Construction unions dwarf every other classified interest
$316k of the $779k classified. Waters $95.5k, Ige $70.4k, Kiaaina $60.3k,
Kidani $55.3k, Dela Cruz $41k. Relevant context for renewables politics
(project labor), but not specific to siting restrictions.

### Explicit NULLS
- No HEI PAC/exec money at all in-window: Chang, Coffman*, Kahele, Nishihara*,
  Slom, Solomon*, Tsuji, Tsuneyoshi, Tupola (*except trivial hei_person gifts
  ≤$500: Alm→Coffman $50, Fargo→Nishihara $500, Alm→Solomon $375).
- No American Savings Bank (HEI) contributions found to any target.
- No seed/ag money: Gabbard, Kiaaina, Tsuneyoshi, Tupola, Waters.
- No solar/wind money: Chang, Kahele, Nishihara, Slom, Tsuji, Tsuneyoshi, Tupola.
- Slom (R, sole SB631 Republican introducer): zero in every classified class
  except $700 DuPont.
- No Kamehameha Schools PAC exists in the data; no KS-executive cluster found.

## Outputs
- data/campaign_contributions_siting.csv — 730 classified rows (candidate,
  office, election_period, donor, donor_type, employer, occupation, amount,
  date, donor_class, confidence, group, source).
- data/campaign_contrib_summary.csv — candidate × election period: n
  contributions, total raised (denominator), and $ by donor class.
- data/raw/csc/ — wayback dump + per-candidate live API caches.
- analysis/campaign_finance_extract.py — rerunnable pipeline.

## Caveats
1. Employer/occupation fields are self-reported and often blank pre-2012;
   individual-donor classification therefore UNDERCOUNTS interest-affiliated
   money (an unknown number of executives appear with blank employer).
2. Name matches marked "medium" (e.g., "Alm, Robert", "Taniguchi, Barry",
   "Taketa, Kelvin", Watanabe) rest on distinctive-name + role consistency,
   not documentary linkage. Same-name false positives possible.
3. "Coffman, George" = Denny Coffman is a legal-name identification (Kona donor
   base, correct chamber/periods); no CSC document in hand states the alias.
4. CSC data begins 2006-11-08; earlier cycles (relevant to pre-2011 failed
   liberalization bills) are not in any CSC electronic dataset.
5. Council window capped at 2024-12-31 per scope; live top-up rows to 2026
   exist in data/raw/csc/live_*.json if needed.
6. Non-candidate spending (independent expenditures, ads) NOT covered here —
   would require the NCC expenditure datasets (riiu-7d4b etc., 2015+ only).
7. The 2006–2014 microdata now exists officially only offline at CSC; our copy
   is the IA-archived CKAN dump (checksummed URL above). Recommend citing both
   CSC and the capture URL.
