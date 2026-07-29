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

## 6. Energy security as a driver — what it does and does not produce

The military wants on-site solar-plus-storage on Oahu, and federal law directs
it to build it. This is a driver for MORE generation on military land. It is a
weak driver for military land supplying the civilian grid. Both hold, for the
reason in §6c.

### 6a. The mandate and the authorities

DoD energy resilience is a statutory requirement, not a preference. "Energy
resilience" is defined at 10 U.S.C. §101(f)(6) as "the ability to avoid,
prepare for, minimize, adapt to, and recover from ... energy disruptions ...
sufficient to provide for mission assurance and readiness"; "energy security"
at §101(f)(7) as "assured access to reliable supplies of energy and the ability
to protect and deliver sufficient energy to meet mission essential
requirements" ([10 U.S.C. §101](https://www.law.cornell.edu/uscode/text/10/101)).

- **10 U.S.C. §2920** (energy resilience and energy security policy) requires
  that by FY2030, 100% of the energy load for each installation's critical
  missions carry "a minimum level of availability of 99.9 percent per fiscal
  year," directs installation planning to "promote the use of ... energy
  resources originating on the installation," to "promote installing microgrids
  to ensure the energy security and energy resilience of critical missions,"
  and to run "black start exercises" testing operation "without access to
  off-installation energy resources"
  ([10 U.S.C. §2920, uscode.house.gov](https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title10-section2920&num=0&edition=prelim)).
- **10 U.S.C. §2911** sets a facility-energy renewable goal of ≥25% by FY2025
  (§2911(g)) and authorizes energy-security demonstration projects featuring
  on-installation production and "microgrids, to ensure that energy remains
  available to the installation even when the installation is not connected to
  energy sources located off the installation" (§2911(h))
  ([10 U.S.C. §2911](https://www.law.cornell.edu/uscode/text/10/2911)).
- **DoD Instruction 4170.11** (Installation Energy Management) requires DoD
  Components to identify critical energy requirements and ensure primary and
  emergency generation serve those critical loads
  ([DoDI 4170.11, ESD/WHS](https://www.esd.whs.mil/Portals/54/Documents/DD/issuances/dodi/417011p.pdf)).
- **NDAA FY2020 §2801** and the installation-resilience-planning regime require
  each department to plan for energy resilience and security, favoring
  installed on-site sources and microgrids over emergency generation
  ([PL 116-92, govinfo](https://www.govinfo.gov/content/pkg/PLAW-116publ92/html/PLAW-116publ92.htm)).

Financing/land mechanisms that let installations build without appropriations:
enhanced-use lease, **10 U.S.C. §2667** (lease of non-excess land; the Kupono
mechanism, §3); energy savings performance contracts / utility agreements,
**10 U.S.C. §2913** (Secretary "shall permit and encourage" participation in
utility demand/conservation programs and may accept utility incentives, with
title to installed devices vesting in the United States)
([10 U.S.C. §2913](https://www.law.cornell.edu/uscode/text/10/2913)).
Taken together these direct installations toward on-site generation plus storage
plus islanding for critical loads.

### 6b. What the Oahu projects are for (stated purpose)

Every built Oahu military energy project is described by its sponsor as
resilience/islanding first. Grid export is a byproduct of two of them.

- **Kupono Solar** (42 MW PV + 42 MW/168 MWh, Navy West Loch EUL, COD Jun 2024).
  The Navy states the project will "ensure full-base resilience in the event of
  a grid outage, maintain Navy operational capability in the event of widespread
  power outages, provide the Navy with the ability to 'island' the JBPHH grid
  from the larger HECO grid, provide power for HECO to purchase and deliver to
  both the installation and the community, and improve island wide power
  reliability"
  ([DVIDS / Navy Region Hawaii, 2022](https://www.dvidshub.net/news/431866/solar-project-breaks-ground-west-loch);
  cached `data/raw/military-golf/navy_kupono_dvids.html`). Kupono both islands
  the base AND sells to HECO under a 20-yr PPA — the one Oahu project that does
  both.
- **Pu'uloa / JBPHH microgrid** (Ameresco, 99 MW firm renewable + 46 kV
  backbone, DOE GRIP 2024). A resilience microgrid for JBPHH, not a
  grid-export solar farm
  ([Ameresco IR](https://ir.ameresco.com/); cached
  `ameresco_puuloa_grip.html`; §3).
- **Schofield Generating Station** (50 MW biofuel/diesel, HECO-owned, on an
  8-ac Army EUL, online 2018). Built to power Army critical missions and to
  provide **black-start** and microgrid service to Oahu: it can isolate and
  power Schofield Barracks, Wheeler Army Airfield, and Field Station Kunia
  during an island-wide outage, and provides black-start to restart the HECO
  grid ([U.S. Army, "Garrison Hawaii and HECO showcase energy security"](https://www.army.mil/article/281189/garrison_hawaii_and_heco_showcase_energy_security_and_sustainability);
  [Army EIS page](https://home.army.mil/hawaii/index.php/garrison/dpw/schofield-plant),
  cached `army_schofield_generating_station.html`). Firm generation, not solar,
  but the clearest islanding/black-start case on Oahu.
- **Earlier West Loch array** (~20 MW-AC, HECO-owned, ~100 ac, ~2019). A
  HECO rate-base grid-supply array on Navy land — the one Oahu military site
  built primarily for civilian supply rather than base resilience (§3).

### 6c. What determines whether the land supplies the civilian grid

Distinguish two outcomes. They are governed by different facts.

**(a) Military solar+storage for the military's own energy security.** This is
happening, is DoD policy, and is not prevented. Kupono islands JBPHH; Schofield
black-starts three installations; Pu'uloa is a resilience microgrid. Resilience
solar sized to base critical load, behind the fence, is exactly what §2920 and
§2911 direct, and no ordnance/airspace/ceded-land constraint stops a base from
building it on its own developed ground. The energy-security motive cuts toward
more of this.

**(b) Military LAND as a source of solar for the civilian (HECO) grid.** This is
governed by four gates, all of which can block scale supply even while (a)
proceeds:

1. **EUL discretion (§2667).** A civilian developer reaches the land only
   through a lease the Secretary "may" grant when it promotes national defense
   or the public interest. One Oahu solar EUL exists to date (Kupono). The land
   is not on the private or state lease market (§5a).
2. **Mission-compatibility certification.** Energy leases require a
   mission-compatibility determination; DoD's Sustainable Ranges program lists
   "renewable energy effects" as an encroachment factor (§2). Land held for
   training, ordnance buffer, or airspace does not clear it.
3. **Project configuration: base load vs export.** A resilience project supplies
   the civilian grid only to the extent it is oversized beyond base critical
   load and PPA'd to HECO. Kupono was configured that way (islands the base and
   exports ~10,000 homes' worth to HECO); Pu'uloa was not. The default for a
   resilience microgrid is to serve the base, not to wholesale power.
4. **Physical constraints already documented (§§1–2, 5).** The large flat
   military acreage is dominated by ordnance/ESQD, active training/UXO,
   airfield/airspace, or developed uses. The returning 2029 state-lease land is
   mostly steep Conservation range; the one flat grid-adjacent parcel (Kahuku
   158002002) is retained by the Army.

What **prevents** scale civilian supply from military land: gates 1–4 above —
discretionary and rarely exercised lease access, mission certification, the
base-load default, and the physical constraints. What does **not** prevent
on-base resilience solar: none of those, because behind-the-fence generation
for the base's own critical load needs no EUL to a third party, exports nothing
the grid depends on, and sits on the base's own cleared ground.

**The tension, resolved.** The energy-security mandate expands generation ON
military land for the military's benefit (islanding, black-start, 99.9%
critical-load availability). The same land stays mostly closed to civilian IPPs
because the mandate attaches to serving the base, not to opening the land
market. The EUL is the hinge between the two: the identical §2667 instrument
that DoD exercises for a mission purpose can incidentally yield civilian supply
when the project is oversized and sold to HECO — as Kupono was, and as the
default resilience microgrid is not. Civilian grid supply from military land is
therefore a discretionary byproduct of a mission decision, not a supply source a
developer or the State can count on.

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
  ACTIONABLE solar resource for the civilian grid it is small. Scaling beyond
  the West Loch/Kupono precedent is unproven, and the category adds ~0 new
  near-grid flat acreage to the paper's tallies. The energy-security buildout
  for DoD's own load is a separate question (§6d).

### 6d. Scale — DoD load versus DoD generation

DoD electricity load on Oahu exceeds DoD on-site generation by a wide margin.
Public data does not state DoD's share of island demand. The military is "among
the largest consumers" of Oahu electricity and controls ~20% of the land
([The Diplomat, 2025-01](https://thediplomat.com/2025/01/hawaiis-role-in-the-us-indo-pacific-energy-security-dilemma/)).
Army Garrison Hawaii runs 85 MW of on-site DER and 45 GWh/yr of renewable
generation
([DOE FEMP](https://energy.gov/femp/us-army-garrison-hawaii-energy-resiliency-program-wins-femp-award)).
An estimate of 20–35% of island demand for total DoD load is **UNVERIFIED and
likely confidential**; no public source confirms it.

Arithmetic bounds the point regardless of the exact share. Oahu net energy for
system is ~6,495 GWh/yr and peak ~1,074 MW (FERC Form 1 CY2022,
`notes/oahu-node-profiles.md`). At a 20–35% share, DoD load is ~1,300–2,270
GWh/yr and ~215–375 MW of coincident peak. DoD-associated generation on Oahu is
~110 MW nameplate: Kupono 42 MW PV, ~20 MW West Loch PV, 50 MW Schofield firm
biofuel, plus 45 GWh/yr Army renewable (§3, §6b). Generation supplies a small
fraction of that load.

Self-supplying DoD load with solar would require several hundred MW of PV plus
storage. At a ~21% Oahu solar capacity factor, 1,300–2,270 GWh/yr implies
~700–1,235 MW of PV, before storage for night and resilience. The FY2030
mandate (§6a) sets a floor below this: it requires 99.9% availability for
critical-mission load, which islanding microgrids meet with a mix of solar,
storage, and firm backup (Schofield). The energy-security buildout the mandate
could drive ranges from the critical-load floor to a full-self-supply ceiling
near ~1 GW. Both bounds are estimates; the exact DoD load is UNVERIFIED.

### 6e. The DS tariff and the rate-base question (open — no conclusion drawn)

DEEPENED AND CORRECTED 2026-07-28: see `notes/heco-military-relationship.md`,
which verifies the DLA utilities-privatization contract, the Schedule DS terms,
and the generation ownership below against primary sources. Two earlier claims
here were corrected: Schedule DS carries no minimum contract term (the tariff's
threshold is loads ≥300 kW served directly from a substation; an earlier "at
least five years" statement was wrong), and the DLA contract sits outside the
general rate base (below).

The military buys power under HECO Schedule DS (Large Power Directly Served
Service), applicable to loads ≥300 kW served directly from a substation
([HECO Schedule DS](https://www.hawaiianelectric.com/Documents/my_account/rates/hawaiian_electric_rates/heco_rates_sch_ds.pdf);
HECO Docket 2016-0328, Order 35721, 2018). DoD is a large HECO ratepayer.

Whether HECO's rate-base interest shapes military generation outcomes is an open
question. No conclusion is drawn here. This requires careful scrutiny that the
public record may not support. Revealed conduct on the record:

- HECO owns two military-serving generation assets in its general rate base: the
  ~20 MW West Loch PV array and the 50 MW Schofield Generating Station on an
  Army lease (§3). Utility ownership adds these to HECO's rate base. An IPP
  military self-build would not.
- HECO holds a 50-year, $638.5M Defense Logistics Agency utilities-privatization
  contract (10 U.S.C. §2688) under which it OWNS and operates the on-base
  electric distribution systems at 12 Army installations — billed to the Army
  separately and walled off from the general rate base by PUC condition (PUC
  Docket 2019-0349, D&O 37413; ownership transferred 2022-03-01; the contract
  RFP obliges HECO to facilitate interconnection of government- or third-party-
  owned renewable generation on the bases — no exclusivity (§C.3.4);
  [Army Technology](https://www.army-technology.com/news/dla-hawaiian-electric-us-army-system/);
  full sourcing in `notes/heco-military-relationship.md`).
- Kupono is a Navy enhanced-use lease with an IPP developer (Ameresco / Bright
  Canyon) and a HECO PPA; HECO does not own it (§3).

These facts are consistent with a HECO interest in keeping military load and
generation within its rate base. They do not establish it. HECO's motive is not
observable from these documents. Whether HECO has opposed or constrained
military self-generation in any proceeding is **UNVERIFIED** and would require
review of PUC dockets and EUL/interconnection records. Draw no conclusion until
that review is done.

## 7. Current plans and the 2025-26 policy environment (compiled 2026-07-28)

Extends §§3, 6, 6d, 6e. Scope: what DoD is ANNOUNCING or building for added
solar / storage / microgrid resilience in Hawaii for 2024-2027, whether the
2025 change of administration cut or reframed it, and what is knowable from
open sources. Reports revealed conduct (awards, NEPA, dockets, published
policy); asserts no intent. Tiers: **[V]** verified w/ primary or strong
secondary source + URL; **[P]** plausible / awaiting confirmation; **[U]**
unverified.

### 7a. The 2024-2027 project pipeline (added / planned)

New or in-progress since the note's §3 baseline (Kupono, West Loch, Schofield,
Pu'uloa microgrid). Nothing here changes the §5 finding that military land adds
~0 near-grid flat acres to the *civilian* solar supply — these are on-base
resilience assets (§6c-a), except Pu'uloa Solar's small export.

| project | service / site | capacity | mechanism | status (2026-07) | tier |
|---|---|---|---|---|---|
| **Pu'uloa Energy** (firm) | Navy, JBPHH, ~10 ac (TMK 1-9-9-001-008) | ~99 MW firm, 11 dual-fuel (biofuel-capable) recip engines, 14-day fuel, black-start | Ameresco 30-yr operating term; HECO grid interconnect; DOE **GRIP** grant (BIL) | online 2027-2033; GRIP selected Oct 2024 | [V] |
| **Pu'uloa Solar** | Navy, JBPHH | **6 MW PV + 30 MWh storage** | HECO Amended/Restated PPA; overhead 46 kV line ext. **PUC Docket 2025-0436** | active PUC proceeding, public hearing 2026-03-09 | [V] |
| **H2MG hydrogen microgrid** (expands PEARL) | Air Force / HI Air National Guard, 154th Wing, JBPHH-Hickam | adds 1 MW electrolyzer + 600 kg H2 storage + 600 kW PEM fuel cells to the existing **1.5 MW PV / 500 kWh** PEARL microgrid | Global Connective Center prime, BWR Innovations sub, 2-yr subcontract; AFRL / HCATT / NAVFAC / INDOPACOM / NGB | subcontract awarded ~May 2024 | [V] |
| **Holu Hou / Lendlease residential** | Army (privatized housing), Island Palm Communities, Aliamanu Mil. Res. + others | **10 kW PV + 25 kWh storage per home**, ~200 homes phase, 6-home "EnergyShare" networks; meets 75-80% of home load, **no grid export** | military housing-privatization ground lease (Lendlease), Holu Hou HoluPower | construction from summer 2023, expanding through 2026 | [V] |
| **PMRF Kauai microgrid** (existing, context) | Navy, Barking Sands, Kauai | ~14-19.3 MW PV + 70 MWh storage, 100% clean islanding | Navy land lease w/ KIUC; AES built | operational since 2021 (not new) | [V] |
| **MCBH Kaneohe resilience microgrid** | Marine Corps, Kaneohe Bay | not public (RFI 2023, RFP to HECO ~Feb 2024) | HECO utility-agreement path | RFI/RFP stage; award not confirmed | [P] |
| INDOPACOM / PDI installation resilience | Indo-Pacific bases (Hawaii among) | not itemized | FY2026 PDI infrastructure line | budget request stage | [P] |

Sources: Pu'uloa Energy specs — [puuloaenergy.com/projects](https://www.puuloaenergy.com/projects/);
Pu'uloa Solar 6 MW/30 MWh + docket — [PUC Docket 2025-0436 notice](https://puc.hawaii.gov/public-notice/notice-of-public-hearing-hawaiian-electric-overhead-line-extension-for-puuloa-solar-at-joint-base-pearl-harbor-hickam-docket-no-2025-0436/),
[puuloasolar.com](https://www.puuloasolar.com/); GRIP selection —
[Ameresco / BusinessWire 2024-10-18](https://www.businesswire.com/news/home/20241018683144/en/The-U.S.-Department-of-Energy-Selected-Amerescos-Puuloa-Microgrid-Energy-Asset-for-the-Grid-Resilience-and-Innovation-Partnerships-Program),
GRIP federal grant for Oahu military+civilian grid reported ~$40M by
[Rep. Case](https://case.house.gov/news/documentsingle.aspx?DocumentID=3454)
(exact Pu'uloa allocation and post-2025 obligation status **[U]**);
H2MG — [Microgrid Knowledge 2024-05](https://www.microgridknowledge.com/generation-fuels/article/55036626/bwr-innovations-chose-to-deliver-pem-fuel-cells-for-hawaii-base-microgrid-h2-integration);
Holu Hou/Lendlease — [Lendlease media release](https://www.lendlease.com/us/media-center/media-releases/lendlease-and-holu-hou-energy-sign-contract/),
[Army 2026](https://www.army.mil/article/281977/) (title verified via search;
page 403 to bot fetch); PMRF — [AES](https://www.aes.com/energy-insights/first-its-kind-clean-energy-microgrid-us-navy-and-kiuc);
MCBH RFI/RFP — [DVIDS 2023-12](https://www.dvidshub.net/news/458123/marine-corps-base-hawaii-seeks-enhance-energy-resiliency),
[HECO IGP RFP appx F](https://www.hawaiianelectric.com/documents/clean_energy_hawaii/selling_power_to_the_utility/competitive_bidding/igp_rfp/appx_f.pdf);
PDI — [FY2026 PDI budget](https://comptroller.war.gov/Portals/45/Documents/defbudget/FY2026/FY2026_Pacific_Deterrence_Initiative.pdf).

Notes: the biggest 2024-27 items are firm/microgrid (Pu'uloa Energy 99 MW
dual-fuel; H2 storage; residential storage), not new utility-scale PV. Net new
military solar in the pipeline is modest — Pu'uloa Solar 6 MW is the only new
grid-tied PV array found, and it is small. This is consistent with §6c: the
mandate drives *islanding/firm* capacity for base critical load, not export PV.
Pu'uloa Solar (small) and Pu'uloa Energy (via HECO interconnect) are the only
new pieces that touch the civilian grid; both run through HECO (cross-ref §6e:
HECO stays the interconnection/PPA counterparty — rate-base implication still
**[U]**, unexamined in dockets here). FY2026 **ERCIP** ($722.9M DoD-wide) lists
no Hawaii project in the returned budget tables **[P]** (CA, Guam, Japan, etc.
appear; Hawaii absent) — [FY2026 ERCIP MILCON](https://comptroller.war.gov/Portals/45/Documents/defbudget/FY2026/budget_justification/pdfs/07_Military_Construction/14-Energy_Resilience_and_Conservation_Investment_Program.pdf).

### 7b. Red Hill aftermath and JBPHH resilience

The 2021 Red Hill fuel spill and the completed 2024 defueling reoriented JBPHH
toward energy (not fuel) resilience, but no document was found that *ties a named
solar/storage project to Red Hill closure as cause*. What is on the record:

- Red Hill defueling completed ~June 2024; permanent closure targeted 2027;
  Navy Closure Task Force-Red Hill leads decommissioning/aquifer cleanup **[V]**
  ([EPA Red Hill closure](https://www.epa.gov/red-hill/closure);
  [Navy Times 2023](https://www.navytimes.com/news/your-navy/2023/05/17/pentagon-accelerates-timeline-to-defuel-red-hill-facilities/)).
- The JBPHH energy-resilience buildout (Pu'uloa Energy/Solar microgrid, PEARL
  H2MG, Kupono islanding) is the electricity-side analogue to losing bulk fuel
  storage, but sponsors frame these as grid-outage resilience / mission
  assurance, **not** explicitly as Red Hill replacements **[P]**. Treat "Red
  Hill drove the microgrid push" as plausible narrative, not documented
  causation — the microgrid program (PEARL 2016, Pu'uloa GRIP 2024) predates and
  postdates Red Hill and rests on the §6a statutory mandate.

### 7c. The Trump-era policy effect: reframed, not (visibly) cancelled

The clearest finding: **climate-labeled DoD work was cut; energy-resilience /
mission-assurance work for Indo-Pacific bases continued and was re-branded under
the "warfighting" and "unleashing American energy" banners.** No specific Hawaii
military solar/microgrid project was found cancelled; the flagship JBPHH project
shows revealed conduct of *continuation*.

Policy actions (revealed conduct):
- **"Unleashing American Energy" EO (Jan 2025)** paused IRA/IIJA disbursements
  ~90 days — the funding stream behind GRIP (BIL) that backs Pu'uloa **[V]**
  ([Canary Media](https://www.canarymedia.com/articles/policy-regulation/trump-orders-freeze-on-inflation-reduction-act-infrastructure-law-funding);
  [Microgrid Knowledge](https://www.microgridknowledge.com/microgrid-policy/article/55262952/president-trumps-eo-to-freeze-the-ira-how-will-it-impact-microgrids-and-ders)).
- **March 2025:** Trump rescinded the Defense Production Act §303 determinations
  (2022-15/-18) that had labeled solar PV modules critical to national defense
  **[V]** ([Columbia Climate Law](https://climate.law.columbia.edu/content/president-trump-issues-executive-order-rescinding-additional-biden-era-presidential-actions)).
- **OBBBA + EO 14315 (July 2025)** repealed/curtailed wind & solar tax credits
  **[V]** ([Columbia Climate Law](https://climate.law.columbia.edu/content/president-trump-orders-swift-implementation-budget-bill-end-renewable-tax-credits)).
- **Hegseth SecDef memo (Mar 17 2025):** eliminate "climate change"-framed
  programs/mission-statement references; DOGE/DoD cancelled ~90 studies, ~$800M
  cuts (~$100M climate-related). **Carve-out kept:** hardening installations
  against extreme weather, mission assurance, weather-risk mitigation **[V]**
  ([Scientific American](https://www.scientificamerican.com/article/hegseth-orders-elimination-of-pentagon-climate-planning-but-wants-extreme/);
  [E&E News](https://www.eenews.net/articles/hegseth-ditch-climate-distraction-but-prepare-for-extreme-weather/)).
  DoDI 4715.28 (Military Installation Resilience) reissued to comply while
  retaining energy-hardening requirements **[V]**
  ([DoDI 4715.28](https://www.esd.whs.mil/Portals/54/Documents/DD/issuances/dodi/471528p.PDF)).

The reframing, in DoD's own new words:
- **Navy energy-resilience solicitation (Aug 7 2025)** — issued THROUGH the CEED
  Consortium (OTA), seeking execution-ready prototypes (small modular nuclear,
  geothermal, battery storage, generation) to power Navy/Marine Corps
  installations at **99.9% availability** "even if the public grid goes dark."
  Explicitly "about warfighting readiness, mission assurance, and making sure
  our bases remain operational," framed under **"President Trump's commitment to
  unleashing American energy innovation."** Same 99.9% §2920 target as before,
  new vocabulary **[V]** ([Navy.mil press release](https://www.navy.mil/Press-Office/Press-Releases/display-pressreleases/Article/4268360/department-of-the-navy-announces-solicitation-for-innovative-energy-resilience/);
  [Seapower](https://seapowermagazine.org/department-of-the-navy-announces-solicitation-for-innovative-energy-resilience-solutions-to-power-navy-and-marine-corps-installations/)).
- **Pacific Deterrence Initiative FY2026** = $10.0B request; infrastructure
  $2.7B, which OSD says covers energy-resilience improvements at Indo-Pacific
  bases — a China-deterrence budget line surviving the climate cuts **[V/P]**
  ([FY2026 PDI](https://comptroller.war.gov/Portals/45/Documents/defbudget/FY2026/FY2026_Pacific_Deterrence_Initiative.pdf);
  itemization to Hawaii not public — **[P]**).
- The 2025 **Military Installation Resilience Report to Congress** (May 2025)
  continued under the new administration **[V]**
  ([2025 report](https://www.acq.osd.mil/eie/imr/mc/Downloads/2025-Report-to-Congress-on-Military-Installation-Resilience.pdf)).

Revealed conduct that the Hawaii flagship CONTINUED, not cancelled:
- Pu'uloa Solar's HECO PPA/line-extension is in an **active PUC proceeding with
  a public hearing set for March 2026** (Docket 2025-0436) — the project is
  advancing, not shelved **[V]**.
- Ameresco's Hawaii (Pu'uloa) infrastructure project was named to **Fortune's
  2025 "Change the World" list (Oct 2025)** — sponsor-side signal of an
  ongoing, not paused, project **[V/P]**
  ([BusinessWire 2025-10-08](https://www.businesswire.com/news/home/20251008868412/en/Ameresco-Named-to-Fortunes-2025-Change-the-World-List-for-Energy-Infrastructure-Project-in-Hawaii)).
- **May 2026:** joint Army/State "Energy Cluster" resilience showcase (Lt. Gov.
  Luke, USAG-HI Cdr Col. Sullivan, State CEO Glick) — the on-base resilience
  program still publicly active in 2026 **[V/P]** (Army release via search).

**What is NOT verifiable:** whether the Jan-2025 IRA/IIJA pause delayed the GRIP
obligation for Pu'uloa, or reduced its federal share, is **[U]** — the funding
freeze was national and litigated; the project's own filings continue, but no
document confirms its GRIP dollars were released, cut, or restructured. Do not
assert either "Trump killed it" or "fully funded as planned." State the freeze,
state the continued project conduct, and mark the reconciliation unverified.

### 7d. Confidentiality — what open sources can and cannot show

The "what is the military planning" question is **substantially, but not fully,
answerable from open sources.**

Public (used above): contract/OT awards and consortium solicitations (Navy CEED,
Ameresco/GRIP), enhanced-use leases (10 USC 2667), NEPA EAs/EISs, PUC dockets
and PPAs (interconnection is a civilian-regulated act, so it surfaces),
congressional press releases, service energy-office and DVIDS releases, and
budget line items (PDI, ERCIP, MILCON justification books). Nameplate capacity,
site, developer, and mechanism are generally disclosed because a grid-tied
military project must interconnect through HECO/KIUC and clear NEPA — both open
processes.

Withheld / not in open sources (OPSEC): the **critical-load lists** (which
specific missions must stay powered), the **resilience architecture** (islanding
switchgear topology, black-start sequencing, cyber design), **specific mission
dependencies**, and any classified requirement driving sizing. DoD guidance
(UFC 3-550-04; PNNL/Lincoln Lab microgrid studies) discusses critical-vs-
noncritical load classification in the abstract but installation-specific lists
are not published **[V]** ([UFC 3-550-04](https://www.wbdg.org/FFC/DOD/UFC/ufc_3_550_04_2024.pdf)).
DoD total electricity load on Oahu and its share of island demand remain
UNVERIFIED / likely sensitive (§6d).

Bottom line for the research question: the *existence, location, size, and
commercial mechanism* of DoD Hawaii energy projects are open-source knowable
(this note's tables are built entirely from public records). The *why-this-size,
which-missions, how-hardened* layer is deliberately withheld, so any inference
about the true resilience target beyond the published 99.9% §2920 floor is
speculation. The land-availability question this repo cares about is answerable;
the mission-dependency question is not.

## Branch-level rollup

Installed-to-date by branch (grid-scale vs rooftop, ownership decomposition)
and potential-by-branch tables: `notes/dod-solar-installed-by-branch.md`.
Short version: all ~77 MW of grid-scale solar on Hawaii military land is on
NAVY land; the Army has zero grid-scale and ~27-35 MW of housing/rooftop PV;
the services themselves own ~6% of the ~130-137 MW total.

## Caveats

- §7 tiers as marked; the reframed-not-cancelled finding is a documented
  PATTERN (climate cut + resilience/mission-assurance carve-out kept + Navy Aug
  2025 solicitation language + continued Pu'uloa PUC proceeding), not a project
  memo saying "continued because reframed." No Hawaii DoD energy project was
  found affirmatively cancelled; absence of a cancellation record is not proof
  none occurred.
- Tenure not deed-resolved (fee vs ceded); constraint tiers are screen-level,
  not DoD findings; every parcel-level exclusion is UNVERIFIED.
- Layer-34 polygons include some internal overlap (~1,093 ac); dissolved totals
  used for tenure sums, per-installation rows kept for the CSV.
- 46 kV distances are UPPER bounds (network under-mapped); 138 kV solid.
- Slope from 10 m DEM band raster; whole-installation majority-district labels
  in the CSV, but district splits in §5 use actual intersected area.
