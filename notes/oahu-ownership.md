# Oahu ag-district parcel ownership (TMK-keyed)

Date: 2026-07-11. Output: `data/oahu_ag_owners.csv` (6,239 rows). Scripts:
`analysis/fetch_ownall.py` (download), `analysis/resolve_owners.py` (resolution +
CSV write; contains the full manual mapping table).

## Method

1. **Bulk source found — no scraping needed.** The City & County of Honolulu
   publishes its RPAD cadastral tables as hosted ArcGIS feature services on the
   Honolulu open-geodata hub (honolulu-cchnl.opendata.arcgis.com). The owner
   table is **OWNALL** (583,721 rows islandwide, tax year 2027):
   `https://services.arcgis.com/tNJpAOha4mODLkXz/arcgis/rest/services/CadastralTables/FeatureServer/5`
   Companion tables: OWNDAT (6, taxbill owner+address), ASMTGIS (9, assessed
   values), LEGDAT (11). Queried with batched `tmk IN (...)` requests (100
   TMKs/request, 0.6 s pause) for the 6,274 Oahu ag-district parcels in
   `data/cap_scenarios_by_parcel.csv`. RPAD `tmk` is 8-digit (our 9-digit TMK
   minus the leading county digit "1"); `parid` = tmk + 4-digit CPR suffix.
2. **Per-parcel owner rule:** rows with parid suffix `0000` (the fee parcel),
   primary owner = `ownseq` 0 `own1`; co-owners (ownseq>0) not in the CSV but
   recoverable from the raw pull. One fully-CPR'd parcel (Kunia Loa Ridge)
   uses the modal unit owner.
3. **Government layers** (geodata.hawaii.gov ParcelsZoning/19 Government Lands
   – Detailed; DHHL layers): used as cross-check and to attribute 1 parcel
   (TMK 187010030, DHHL) missing from RPAD. RPAD itself already names
   state/county/federal/DHHL owners, so the layer added little.
4. **qPublic (Schneider) is Cloudflare-blocked** to non-browser clients (403
   on direct fetch and via WebFetch). Not needed given OWNALL, except for the
   35 residual parcels below, which qPublic could not be used for either.
5. **Unmatched:** 35 parcels (2,011 ac, 1.0% of acreage) are in the GIS parcel
   fabric but have **no RPAD assessment record** under any parid (checked
   OWNALL and OWNDAT by tmk and by `parid LIKE`) — likely newly created,
   retired, or non-taxable TMKs (several are `...999` dummy plats). Left
   unattributed. Largest, with same-plat neighbor hints (UNVERIFIED, not in CSV):
   - 165005004 (669 ac; plat neighbors: Dole, ADC, Pioneer — Waialua)
   - 195003017 (342 ac, 333 B/C; neighbors: Castle & Cooke Homes, Waipio Land Holdings — Kunia)
   - 194006212, 194006045, 194006182 (Waipio/Waiawa; neighbors: Castle & Cooke, Bishop Estate)
   - 166027010 (142 ac; small-holder plat, Haleiwa), 195003019 (137 ac),
     194003002 (135 ac; neighbors: Robinson Kunia), 165001039 (108 ac)

## Coverage

- **Parcels: 6,239 / 6,274 = 99.4%. Acreage: 208,119 / 210,130 = 99.0%.**
- Source mix: 6,238 `bulk` (RPAD OWNALL), 1 `govlayer`. No owner in the CSV is
  websearch-sourced. Confidence: 5,122 high / 757 med / 360 low (med/low =
  heuristic type assignment or UNVERIFIED affiliation, flagged in `note`).

## Entity resolution

Manual mapping for all raw names ≥50 ac (160 names, 95% of acreage) + regex
heuristics for the tail (SURNAME,FIRST → individual; family-trust patterns →
individual; LLC/INC with FARM/RANCH → corporate_ag, with
DEVELOPMENT/HOMES/GOLF → developer, else corporate_other; church/assn →
nonprofit). Full mapping = `MAP` dict in `analysis/resolve_owners.py`; every
row keeps `owner_raw` verbatim. Key merges:

- "B P BISHOP TRUST ESTATE" + "ESTATE OF BERNICE PAUAHI BISHOP" → **Kamehameha
  Schools**. ("BISHOP TRUST CO LTD" is a corporate trustee; it is not KS.)
- Kualoa Ranch Inc/Incorporated/Incorport ed (3 RPAD spellings) → Kualoa Ranch.
- 7 ADC spelling variants → State of Hawaii – ADC; DLNR divisions → DLNR.
- Castle & Cooke Homes/Inc/Properties → Castle & Cooke Hawaii (kept distinct
  from Dole Food Co per project convention; both Murdock-affiliated).
- "PROPERTY RESERVE INC" = LDS Church real-estate arm (typed nonprofit, noted).
- **`owner_type` addition:** `corporate_other` (corporate, sector neither ag
  nor real-estate: Grace Pacific, Intelsat, IES Downstream, PVT, HRT Ltd…).
- **Caveat — ag CPRs:** several large "owners" are condominium masters whose
  land is really many small unit owners (Laukiha'a Mauka/Farms 4,671 ac —
  development by Pomaika'i Partners LLC, med confidence, web-sourced; Kunia
  Section 6; Ohana Farm Parcels; Kunia Heritage; Waikele Storage Park). Typed
  `unknown` with a CPR note. Treating each as one owner OVERSTATES private
  concentration; excluding them understates it.

## Concentration results

Totals (Oahu ag district): 210,130 ac; 34,370 LSB B/C ac; S0 (current
10%/20 ac cap) eligible 3,601 ac; S3 (20%, no cap) eligible 15,657 ac.

### Top 20 owners by ag-district acreage

| # | Owner (resolved) | Type | Acres | Share |
|---|---|---|---:|---:|
| 1 | State of Hawaii (agency unspecified) | state | 39,331 | 18.7% |
| 2 | United States of America | federal | 38,563 | 18.4% |
| 3 | Kamehameha Schools (B.P. Bishop Estate) | private_estate_trust | 26,839 | 12.8% |
| 4 | State of Hawaii - DLNR | state | 9,213 | 4.4% |
| 5 | Property Reserve Inc (LDS Church real-estate arm) | nonprofit | 6,294 | 3.0% |
| 6 | City & County of Honolulu | county | 5,588 | 2.7% |
| 7 | Laukiha'a ag CPR (multiple unit owners) | unknown | 4,671 | 2.2% |
| 8 | DHHL | dhhl | 4,257 | 2.0% |
| 9 | Dole Food Co Inc | corporate_ag | 4,107 | 2.0% |
| 10 | Kualoa Ranch (Morgan family) | corporate_ag | 3,687 | 1.8% |
| 11 | Castle & Cooke Hawaii (Murdock) | developer | 2,753 | 1.3% |
| 12 | Dillingham Ranch Holdings LLC | corporate_ag | 2,738 | 1.3% |
| 13 | Corteva Agriscience (Pioneer Hi-Bred) | corporate_ag | 2,642 | 1.3% |
| 14 | State of Hawaii - ADC | state | 2,569 | 1.2% |
| 15 | Robinson family (Robinson Kunia Land LLC) | private_estate_trust | 2,427 | 1.2% |
| 16 | Island Palm Communities LLC (Army housing PPP / Lendlease) | developer | 2,403 | 1.1% |
| 17 | Bayer (ex-Monsanto) | corporate_ag | 2,150 | 1.0% |
| 18 | Kaukonahua Ranch LLC | corporate_ag | 2,115 | 1.0% |
| 19 | (UNATTRIBUTED — no RPAD record) | — | 2,011 | 1.0% |
| 20 | Makaiwa Hills LLC (Kapolei project) | developer | 1,855 | 0.9% |

### Top 20 by LSB B/C acreage (the land the statute fights over)

| # | Owner (resolved) | Type | B/C acres | Share |
|---|---|---|---:|---:|
| 1 | United States of America | federal | 5,128 | 14.9% |
| 2 | State of Hawaii (agency unspecified) | state | 3,581 | 10.4% |
| 3 | Kamehameha Schools (B.P. Bishop Estate) | private_estate_trust | 3,466 | 10.1% |
| 4 | Dole Food Co Inc | corporate_ag | 2,688 | 7.8% |
| 5 | Laukiha'a ag CPR (multiple unit owners) | unknown | 1,750 | 5.1% |
| 6 | Island Palm Communities LLC (Army housing PPP) | developer | 1,553 | 4.5% |
| 7 | Property Reserve Inc (LDS Church) | nonprofit | 1,153 | 3.4% |
| 8 | State of Hawaii - DLNR | state | 1,134 | 3.3% |
| 9 | United States - Navy | federal | 1,024 | 3.0% |
| 10 | State of Hawaii - ADC | state | 910 | 2.6% |
| 11 | Corteva Agriscience (Pioneer Hi-Bred) | corporate_ag | 569 | 1.7% |
| 12 | (UNATTRIBUTED) | — | 565 | 1.6% |
| 13 | City & County of Honolulu | county | 497 | 1.4% |
| 14 | Office of Hawaiian Affairs | state | 491 | 1.4% |
| 15 | Ohana Farm Parcels ag CPR | unknown | 478 | 1.4% |
| 16 | Bayer (ex-Monsanto) | corporate_ag | 435 | 1.3% |
| 17 | Kualoa Ranch (Morgan family) | corporate_ag | 403 | 1.2% |
| 18 | Law Tieng's Farm Inc | corporate_ag | 381 | 1.1% |
| 19 | Kahuku Wind Power LLC (IPP wind) | utility | 347 | 1.0% |
| 20 | United States - FWS | federal | 333 | 1.0% |

### Top 10 by cap-scenario eligible acres

S0 (current law, 10%/20 ac): State of Hawaii 440 (12.2%), USA 279 (7.7%),
Kamehameha Schools 273 (7.6%), Property Reserve 138, C&C Honolulu 128,
ADC 119, Dole 111, (unattributed 108), Kualoa Ranch 103, Castle & Cooke 88.
Under the binding cap, eligible acreage is nearly proportional to *parcel
count*. It does not track acreage — the cap flattens the distribution.

S3 (20%, no acreage cap): USA 3,618 (23.1%), Kamehameha Schools 2,293
(14.6%), State of Hawaii 1,136 (7.3%), Laukiha'a CPR 811, Dole 719, Property
Reserve 486, Island Palm 481, DLNR 391, Bayer 372, ADC 317. Removing the cap
re-concentrates eligibility onto the large holders: **KS's share of eligible
private-relevant acreage roughly doubles (7.6% → 14.6%) moving S0 → S3.**

### Acreage share by owner_type

| Owner type | Ag acres | Share | B/C acres | Share | S0 | Share | S3 | Share |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| state | 54,260 | 25.8% | 6,567 | 19.1% | 781 | 21.7% | 2,242 | 14.3% |
| federal | 41,096 | 19.6% | 6,485 | 18.9% | 386 | 10.7% | 3,929 | 25.1% |
| private_estate_trust | 30,993 | 14.7% | 3,742 | 10.9% | 386 | 10.7% | 2,558 | 16.3% |
| corporate_ag | 25,012 | 11.9% | 5,565 | 16.2% | 565 | 15.7% | 2,161 | 13.8% |
| nonprofit | 11,292 | 5.4% | 1,751 | 5.1% | 250 | 6.9% | 802 | 5.1% |
| developer | 10,651 | 5.1% | 2,563 | 7.5% | 224 | 6.2% | 1,009 | 6.4% |
| unknown (mostly ag CPRs) | 9,636 | 4.6% | 3,303 | 9.6% | 233 | 6.5% | 1,363 | 8.7% |
| individual | 7,060 | 3.4% | 1,613 | 4.7% | 250 | 7.0% | 508 | 3.2% |
| corporate_other | 7,051 | 3.4% | 1,310 | 3.8% | 252 | 7.0% | 450 | 2.9% |
| county | 5,612 | 2.7% | 497 | 1.4% | 128 | 3.5% | 258 | 1.6% |
| dhhl | 4,257 | 2.0% | 55 | 0.2% | 17 | 0.5% | 31 | 0.2% |
| unattributed | 2,011 | 1.0% | 565 | 1.6% | 108 | 3.0% | 242 | 1.5% |
| utility | 1,200 | 0.6% | 353 | 1.0% | 21 | 0.6% | 104 | 0.7% |

Government (state+federal+county+DHHL) holds **50.1%** of Oahu's ag district.
Private land is ~103,000 ac.

### Lorenz / top-k (resolved owners)

- All owners (n=3,457): top 1 = 18.7%, top 5 = 57.2%, top 10 = 67.8%,
  top 20 = 79.1%, top 50 = 89.9%, top 100 = 94.6%. Gini = 0.978.
- B/C acreage: top 1 = 14.9%, top 5 = 48.3%, top 10 = 65.1%, top 20 = 78.2%.
- Private owners only (102,893 ac): top 1 (KS) = 26.1%, top 5 = 44.3%,
  top 10 = 56.9%, top 20 = 71.2%.

### Who owns the parcels where the 20-acre hard cap binds (>200 ac, any B/C)

118 parcels; 114,296 ac; 25,198 B/C ac. Current S0 eligibility 1,825 ac vs
7,633 ac under S1 (10%, no 20-ac cap) — i.e. **the hard cap removes ~5,800
eligible acres, and 76% of all cap-bound land sits with just the entities
below.** Top holders of cap-bound B/C acreage:

| Owner | Type | Parcels | B/C ac | S0 elig | S1 elig |
|---|---|---:|---:|---:|---:|
| United States of America | federal | 14 | 4,649 | 172 | 2,197 |
| Kamehameha Schools | private_estate_trust | 12 | 3,210 | 221 | 1,402 |
| Dole Food Co Inc | corporate_ag | 2 | 2,308 | 40 | 324 |
| State of Hawaii | state | 13 | 1,984 | 192 | 381 |
| Laukiha'a ag CPR (many unit owners) | unknown | 2 | 1,750 | 40 | 467 |
| Island Palm Communities (Army housing) | developer | 1 | 1,549 | 20 | 240 |
| State of Hawaii - DLNR | state | 7 | 1,098 | 63 | 184 |
| Property Reserve Inc (LDS) | nonprofit | 4 | 816 | 80 | 281 |
| United States - Navy | federal | 3 | 800 | 41 | 82 |
| State of Hawaii - ADC | state | 6 | 651 | 80 | 145 |
| Corteva (Pioneer Hi-Bred) | corporate_ag | 4 | 534 | 62 | 171 |
| Bayer (ex-Monsanto) | corporate_ag | 2 | 431 | 40 | 213 |
| Law Tieng's Farm Inc | corporate_ag | 1 | 381 | 20 | 43 |
| Kahuku Wind Power LLC (IPP) | utility | 1 | 347 | 20 | 51 |
| Robinson family (Robinson Kunia Land) | private_estate_trust | 3 | 179 | 60 | 167 |

Interpretation for the scarcity-rent hypothesis: the 20-ac hard cap binds
hardest on federal/state land (not developable for IPP solar in practice) and
then on **Kamehameha Schools and Dole** — KS alone forgoes ~1,180 eligible
acres (S1−S0) on its cap-bound parcels. Consistent with the verified finding
that KS hosts ~40% of commercial renewable capacity: KS is the largest
private *loser* from the per-parcel cap on Oahu ag land. KS is not a
beneficiary. The cap's private beneficiaries are owners of mid-size (≤200 ac) B/C parcels
whose eligibility is unaffected while big-parcel supply is suppressed.

## Provenance / verification flags

- `owner_raw` is verbatim RPAD OWNALL text (tax year 2027 roll); high
  confidence as *assessment* owner. Assessment owner ≠ beneficial owner for
  LLCs; DCCA business-registry cross-referencing is a Phase-4 task.
- All med/low-confidence resolutions and UNVERIFIED affiliations are flagged
  per-row in the `note` column (e.g., Palehua Partners JV = Gill-Olson,
  PP McCandless = Pono Pacific, EE Waianae = Eurus, Makaiwa Hills parent,
  Kapolei Properties/Campbell link, HRT Ltd ultimate owner, Laukiha'a
  developer = Pomaika'i Partners).
- No websearch-attributed owners in the CSV (bulk coverage made it moot); the
  only web-sourced item is the Laukiha'a→Pomaika'i Partners note (med).
- Raw pulls archived: `data/raw/rpad/ownall_oahu_ag_rows.csv` (19,730 OWNALL
  rows incl. co-owners and CPR units) and
  `data/raw/rpad/govlands_detailed_oahu.csv` (state Government Lands layer
  attributes, 11,075 rows).
