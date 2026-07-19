# Oahu military land and utility-scale solar (tenure, constraints, the 2029 question)

Date: 2026-07-19. Neutral reference. This examines the blanket EXCLUSION of
military land from the non-ag urban solar screen (`notes/oahu-nonag-solar.md`,
which noted ~16,000 flat urban military acres but excluded them). It documents
tenure, constraints, precedent, and the 2029 state-lease return question as a
GOVERNING CONSIDERATION — it advocates nothing and takes no side on land
return, sovereignty, or the active lease dispute. Ceded/Crown-lands status is
treated as a governing legal fact, not an obstacle to "solve."

Outputs: `data/oahu_military_land.csv` (59 rows), `analysis/figs/paper/
f_military_land.png`. Scripts: `analysis/military_land_screen.py`,
`military_finalize.py`, `military_golf_figs.py`. GIS: ParcelsZoning MapServer
layer 34 (DoD Lands) + layer 35 (DoD Leases Expiring 2029), cached slope band
raster and classified transmission lines. EPSG:26904. Sources cached under
`data/raw/military-golf/` (see MANIFEST.md).

## 1. Tenure map

Total Oahu military-associated footprint (layer 34, dissolved): **65,012 ac**
(~17% of Oahu). Two tenure classes:

| tenure | polys | total ac | ac <=15% | ac <=30% |
|---|---:|---:|---:|---:|
| **state land leased to military, expiring 2029** (layer 35) | 7 | 6,288 | 586 | 1,438 |
| **fee / other** (federal fee or ceded-land tenure; layer 34 minus the leases) | 52 | 58,724 | 32,619 | 40,651 |

The **6,288 ac** of 2029-expiring state leases validate the well-documented
~6,322-ac Army figure within 0.5%. These are the analytically important
parcels: they are STATE land (public land trust) leased to the U.S. under
1964 65-year leases at $1 total, and on expiry could return to State control,
making any future use a **state-land siting decision**.

"Fee / other" is NOT deed-resolved here (flagged): much of it is federal fee,
but a large share is **ceded Government/Crown land** the U.S. controls under
other instruments — see §4. Distinguishing fee from ceded at the parcel level
is UNVERIFIED and would require a title/BOC review.

### The 2029 state-lease parcels (the return question)

| installation (TMK) | branch | total ac | ac <=15% | km to 46kV+ | SLUD | 2025 ROD outcome |
|---|---|---:|---:|---:|---|---|
| Kawailoa-Poamoho (172001006) | Army | 4,368 | 197 | 2.3 | Conservation | No Action — **lease expires 2029, returns to State** |
| Kahuku TA (159006026) | Army | 720 | 34 | 2.7 | Conservation | portion beyond ~450-ac retention returns |
| **Kahuku TA (158002002)** | Army | 451 | **230** | **0.07** | **Ag** | **modified retention — Army RETAINS ~450 ac** |
| Makua MR (181001007) | Army | 438 | 38 | 11.5 | Conservation | No Action — expires 2029, returns |
| Makua MR (182001024) | Army | 232 | 72 | 12.0 | Conservation | No Action — expires 2029, returns |
| Kaena Pt Satellite Tracking (169003005) | Air Force | 77 | 14 | 13.0 | Conservation | remote NW point |
| Kaala Air Station (167003023) | Air Force | 2 | 1 | 6.4 | Conservation | summit site |

**Key finding, cutting against a simple "return unlocks solar"
story:** the one 2029-lease parcel that is flat, grid-adjacent (0.07 km), and
in the Ag district — Kahuku TA 158002002, ~230 flat acres — is exactly the
~450 acres the Army **RETAINS** under the Aug-2025 Record of Decision. The
land that actually returns (Kawailoa-Poamoho and Makua, ~5,800 ac) is
overwhelmingly **steep Conservation-district training range**: only ~355 flat
acres total, and of those only ~197 (Poamoho) sit within 3 km of grid; Makua's
flat acres are 11-12 km from the network and carry dense UXO. So the returning
parcels offer on the order of **~200 flat, near-grid acres** — not thousands.

## 2. Constraints (DoD's own screens)

Constraint tiers below are a SCREEN-LEVEL reading of DoD rules applied by
installation; they are NOT DoD determinations, and no document was found
stating "constraint X blocked solar at site Y" (all parcel-level exclusions
flagged UNVERIFIED). Governing rules ARE well-sourced (MANIFEST.md):

- **Explosive-safety quantity-distance (ESQD) arcs** — DESR 6055.09. Buffers
  around magazines restrict *occupied/inhabited* structures. Binds at
  Lualualei Naval Magazine, West Loch Annex, Pearl Harbor, Kipapa/Puuloa.
  Nuance: an unoccupied PV array can be compatible where buildings cannot —
  Kupono itself sits on ESQD-restricted West Loch land (§3).
- **Active training tempo / impact ranges** — Schofield East Range, Kahuku TA,
  Kawailoa-Poamoho maneuver land; impact areas are inherently incompatible
  with permanent civilian infrastructure.
- **Unexploded ordnance (UXO)** — Makua Valley (dense, incl. cluster
  submunitions; storm re-exposure) and Waikane Valley; ground-disturbing
  construction requires clearance-first, raising cost/hazard.
- **Airfield glint/glare & airspace** — Wheeler, JBPHH/Hickam, MCBH Kaneohe;
  screened via SGHAT/ForgeSolar and the DoD Siting Clearinghouse (10 USC 183a,
  DoDI 4180.02), not FAA airport forms. No public determination found.
- **Security/access for civilian O&M** and **encroachment/readiness doctrine**
  — DoD Sustainable Ranges lists "renewable energy effects" as an encroachment
  factor; energy leases need a SecDef mission-compatibility certification.

Applying these (viability tier x flat acres, fee land):

| viability tier (fee) | installations | ac <=15% |
|---|---:|---:|
| precedent_built (West Loch Annex) | 1 | 3,273* |
| plausibly_usable_eul (developed cantonment / underused fee) | 9 | 4,661 |
| excluded — ordnance/ESQD | 6 | 5,581 |
| excluded — active training/UXO | 6 | 4,724 |
| excluded — airfield/airspace | 6 | 7,616 |
| excluded — developed/small (housing, cemetery, storage, beach, comms) | 24 | 7,577 |

*The 3,273 "flat" acres are the whole West Loch Annex footprint; only **~131
ac** actually host built solar (Kupono). Do not read 3,273 ac as available.

**Unavailable:** Lualualei, West Loch magazine areas, Kipapa,
Puuloa Range, Red Hill, Waikane (ordnance/UXO); Makua, Schofield East Range,
Kahuku TA, Kawailoa-Poamoho, Dillingham, Helemano (training/UXO); Wheeler,
JBPHH runway, MCBH, Kalaeloa CG (airfield/airspace). **Plausibly usable
(mechanically, via EUL — not DoD-vetted):** developed/underused fee land at
Schofield Barracks cantonment, Fort Shafter, Tripler, Aliamanu, Camp Smith,
Waipio Peninsula, Pearl City Peninsula. Even here, scalability is UNPROVEN.

## 3. Precedent + scalability

- **Kupono Solar** — West Loch Annex (Navy), **42 MW PV + 42 MW/168 MWh
  battery** on **131.36 ac** under an **Enhanced Use Lease (10 USC 2667)**,
  37-yr term, Navy landlord; Ameresco + Bright Canyon Energy JV (Bright Canyon
  = Pinnacle West subsidiary, NOT an HEI entity); 20-yr HECO PPA; COD Jun 2024.
  AC/DC split UNVERIFIED.
- **Earlier West Loch array** — ~20 MW-AC, **HECO-owned** (rate base), ~100 ac,
  built ~2019. Clean ownership contrast to the IPP-JV Kupono.
- **Schofield Generating Station** — Army land, **50 MW dispatchable
  BIOFUEL/diesel** (six Wartsila engines), **HECO-owned**, 8-ac Army lease,
  35-yr term, online 2018. **NOT solar** — a firm-generation contrast; shows
  the EUL/lease mechanism works on Army cantonment land.
- **Pu'uloa Microgrid (Ameresco)** — 99 MW firm renewable + 46 kV backbone at
  JBPHH; DOE GRIP (2024). Not solar-only.
- **Kalaeloa** (former Barbers Point NAS, closed 1999) is **former** military
  land under DHHL/HCDA/Hunt jurisdiction — cite separately, not as active
  military land (already partly in the non-ag screen).

**Scalability:** the built precedent is ONE ~131-ac solar site
(Kupono) plus one HECO array and one biofuel plant, all on flat, cleared,
grid-adjacent federal fee land outside HRS Ch. 205 districting. Asserting that
utility-scale solar scales to thousands of military acres beyond West Loch is
**UNPROVEN**: the large flat military acreage is dominated by ordnance,
training, airfield, or developed uses that DoD's own screens treat as
incompatible. The federal EUL is the parallel land mechanism (to the ag-land
statute) that let solar site where the state cap would restrict it.

## 4. Political / procedural context (documented, no side taken)

- **The 2029 lease renewal is actively contested.** Army retention EIS
  (EISX-007-21-001): NOI Aug 2021, Draft Jun 2024, Final May 2025, **ROD 7 Aug
  2025** selecting modified retention (~450 ac Kahuku) and No Action (lease
  expiry) at Kawailoa-Poamoho and Makua. **BLNR declined to accept** the Oahu
  FEIS on 27 Jun 2025 (data gaps). Organized participants: OHA, Malama Makua +
  Earthjustice, the Governor's Military-Leased Lands Advisory Committee
  (opposing/negotiating); U.S. Army Garrison Hawaii and an FY2027 NDAA
  provision (supporting renewal). Documented as conduct; no position taken.
- **Ceded / Crown lands (governing consideration).** The Oahu training leases
  sit on former Crown and Government lands of the Hawaiian Kingdom, seized
  1893/1898, returned to the State in 1959 (Admission Act §5(f)) to hold in a
  public trust including "betterment of the conditions of native Hawaiians";
  OHA receives 20% of trust revenue. Their disposition is a core Native
  Hawaiian grievance (Apology Resolution 1993; *Hawaii v. OHA* 2009; *Ching v.
  Case* 2019 found the State breached its trust duty over military-leased ceded
  land at Pohakuloa). **Commercial energy development on this land engages the
  land-return / trust-revenue question directly.** This is a governing legal
  fact for any post-return use — not a hurdle to engineer around.
- **Post-return framing (offered factually, urged not at all).** IF the
  Kawailoa-Poamoho and Makua leases expire and the land returns to the State,
  solar becomes **one candidate post-return use competing with conservation,
  Native-Hawaiian homestead/DHHL, agriculture, cultural access, and remediation
  obligations** — and, as §1 shows, the returning land is mostly steep, remote,
  and UXO-affected, so its solar suitability is limited regardless. For fee
  land that does NOT return, the **EUL (10 USC 2667)** is the only realistic
  mechanism, exercised at DoD's discretion. This note presents solar as one
  option among many and advocates none.

## 5. Overlap with existing screens — how much NEW acreage?

Military land is NOT cleanly "additional." Intersecting the footprint with the
State Land Use Districts:

| military x district | total ac | flat <=15% | flat & <=3 km 46kV+ |
|---|---:|---:|---:|
| fee x **Ag** | 23,812 | 14,335 | 8,467 |
| fee x **Urban** | 17,467 | **16,045** | 12,621 |
| fee x **Conservation** | 17,310 | 2,113 | 1,158 |
| lease x Ag (Kahuku retained) | 454 | 231 | 231 |
| lease x Conservation (returning) | 5,834 | 354 | 19 |

- The **fee x Ag** land (14,335 flat ac) is already inside the paper's ag
  universe as "United States 38,563 ac" (`notes/oahu-ownership.md`). It is
  excluded as new solar supply for the reasons in §5a below.
- The **fee x Urban** flat land (16,045 ac) is the ~16,155-ac flat urban
  military figure the non-ag screen **already noted and excluded** —
  re-characterized by constraint, not new supply.
- The only not-previously-enumerated flat land is **Conservation-district**
  (~2,100 fee + 354 lease flat ac), which is legally unavailable anyway.

### 5a. Why federal agricultural-district land is excluded

Federal land is exempt from state agricultural-district rules, and a private
developer cannot lease it on the open market. Four facts govern the 14,335 flat
"fee x Ag" acres:

1. State agricultural rules do not apply. The state map labels this land
   "Ag district," but HRS ch. 205 does not govern federal land. The Supremacy
   Clause and the Property Clause (U.S. Const. art. IV, §3) exempt federal
   installations from state and county land-use regulation
   ([LII, Supremacy Clause](https://www.law.cornell.edu/wex/supremacy_clause);
   [Justia, preempted state/local laws](https://law.justia.com/constitution/us/state-local-laws-held-preempted.html)).
   Hawaii's 1959 Admission Act reserves to Congress exclusive legislation over
   land the United States holds for defense. The ag-district label carries no
   legal force over the land's use.
2. Access runs through a discretionary DoD lease. A developer can reach this
   land only via an enhanced-use lease under 10 U.S.C. §2667, which the
   Secretary "may" grant when it promotes national defense or the public
   interest — discretionary, not a right
   ([10 U.S.C. §2667, LII](https://www.law.cornell.edu/uscode/text/10/2667);
   [CRS IF11309, DoD outleasing/EUL](https://www.congress.gov/crs_external_products/IF/PDF/IF11309/IF11309.2.pdf)).
   The land is not on the private or state lease market that the paper's
   ownership screen measures.
3. Mission use constrains it. This acreage sits inside active installations
   (Schofield, Wheeler, Lualualei, Waianae). Training areas, flight corridors,
   and buffer zones limit development
   ([Hawaii military presence overview](https://hawaiistateauthority.com/hawaii-military-presence/)).
   Much "fee x Ag" federal ground is training-range buffer or agricultural
   grazing lease inside a base, held for defense purposes.
4. Counting it would double-count. These 14,335 acres are already inside the
   paper's ownership tally as "United States 38,563 ac"
   (`notes/oahu-ownership.md`). Adding them as new solar supply would count the
   same acres twice and would assume a DoD availability the lease record does
   not support: one Oahu solar enhanced-use lease exists to date (Kupono,
   ~131 ac; §3).

Exclusion reason, stated plainly: the ag classification is not the barrier.
Federal control, discretionary EUL access, and mission use are. The soil rating
is irrelevant to whether a developer can build there.

**Net NEW near-grid flat acreage beyond what the paper counts: ~0.** The
military category's contribution is analytic, not additive: it re-characterizes
the ~16,000 noted-excluded flat urban acres by DoD constraint (most are
ordnance/airfield/training/developed), documents the one proven site (Kupono,
~131 ac), and surfaces the 2029 return question — which itself adds only
~200 flat near-grid acres of genuinely state-decidable land, since the flat
grid-adjacent Kahuku parcel is the piece the Army keeps.

## Viable-acreage estimate (heavy caveats)

- **Built today:** ~131 ac (Kupono) + ~100 ac (earlier HECO West Loch) of
  solar; ~50 MW biofuel (Schofield); ~99 MW microgrid (Pu'uloa).
- **Mechanically plausible additional (EUL, fee land, NOT DoD-vetted):** the
  ~4,660 flat "plausibly_usable" acres are an UPPER bound; realistic
  availability is a small fraction after ESQD/airspace/security/mission
  screening — order of magnitude **hundreds, not thousands, of acres**, and
  entirely at DoD discretion.
- **Post-return state land (2029):** ~200 flat near-grid acres (Poamoho), on
  ceded land, competing with conservation/homestead/cultural uses; the flat
  grid-adjacent Kahuku parcel is retained by the Army.
- **Bottom line:** military land is a large PHYSICAL footprint. As an
  ACTIONABLE solar resource it is small. Scaling beyond the West Loch/Kupono
  precedent is unproven, and the category adds ~0 new near-grid flat acreage to
  the paper's tallies.

## Caveats

- Tenure not deed-resolved (fee vs ceded); constraint tiers are screen-level,
  not DoD findings; every parcel-level exclusion is UNVERIFIED.
- Layer-34 polygons include some internal overlap (~1,093 ac); dissolved totals
  used for tenure sums, per-installation rows kept for the CSV.
- 46 kV distances are UPPER bounds (network under-mapped); 138 kV solid.
- Slope from 10 m DEM band raster; whole-installation majority-district labels
  in the CSV, but district splits in §5 use actual intersected area.
