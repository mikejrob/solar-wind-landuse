# Oahu north→south bulk delivery: screenlines, capacity guesses, and the storage-shaped requirement

Run date: 2026-07-12. Script: `analysis/screenline_analysis.py` (re-runs
offline from `data/gis/` cache). Outputs:
`data/gis/screenline_analysis.csv` (counts + capacity guesses),
`data/gis/screenline_requirements.csv` (full 648-row scenario grid, tidy for
R), map `analysis/figs/paper/f_screenlines.png`.

**Status of every capacity and cost number in this note: ASSUMPTION
(planning-typical ranges), not HECO data.** HECO thermal ratings, conductor
types, and contingency limits are confidential; the public HIFLD/OSM line
maps carry no ampacity fields; and a line drawn once may be a double-circuit
tower. Follows `docs/ASSUMPTIONS.md` conventions; treat everything below the
crossing counts as an educated screen, not engineering.

## Question

Oahu's load is concentrated in the south (Pearl Harbor–downtown–east side);
the historic thermal fleet sits on the southern/southwest coast (Kahe
~650 MW, Waiau ~470 MW, Campbell Industrial Park/Kalaeloa CTs ~400 MW). The
138 kV backbone was built to move power **west→east along the southern
coast**. Utility-scale solar under our siting screens sits **central/north**
(Kunia, Waialua, Wahiawa, Kahuku). How much north→south transfer capacity
exists across the necks in between, what do 1–4 GW of northern solar (with
co-located storage) require, and what would closing the gap cost? Distances
are modest (~10–25 km), so the question is thermal capacity of existing
corridors, not new voltage classes.

## Method

Three east–west screenlines cut ridge-to-ridge across the island
(EPSG:26904; endpoints in the script):

- **SL-A** — Waipahu–Pearl City–Aiea band: central plateau vs the Pearl
  Harbor load pocket (Waianae crest → Koolau crest).
- **SL-B** — mid-plateau, between Wahiawa and Waipio.
- **SL-C** — North Shore neck, between Waialua/Kahuku and Wahiawa (coast to
  coast).

For each screenline, every geometric crossing of the HIFLD+OSM classified
line layer (`oahu_lines_classified.parquet`, 138 kV vs "46 kV+") is
extracted; crossing points within 500 m along the screenline are clustered
into **corridors**; per corridor the **circuit count** is
max(HIFLD features, OSM ways weighted by `circuits=` tags), with a mod-2
collapse of features that wiggle across the same cluster twice.
Parallel-circuit ambiguity is handled by reporting both corridor and circuit
counts; OSM `circuits=` tags exist on only 4 of 87 Oahu ways, so **a single
drawn line can hide a double circuit — circuit counts are lower bounds.**

One structural subtlety: the Kahe 2–Halawa and Kahe 2–Waiau 138 kV circuits
**loop up through the Kunia/Waipio bench** and cross SL-A twice each (once
climbing at Kunia ~lon −158.05, once descending at Waipio/Waiau ~−157.93).
For net N→S flow those loops are pass-throughs *unless tapped north of the
line* — and they are exactly where Kunia-area utility solar would (and does)
interconnect. So SL-A gets two readings: **parity-net** (loops untapped,
conservative) and **geometric** (loops tapped, central).

## Screenline counts (mapped public data)

| Screenline | 138 kV circuits (corridors) | parity-net 138 | 46 kV circuits (corridors) | What crosses |
|---|---|---|---|---|
| SL-A | **8 (5)** | 2 | 0 (0) — *artifact* | Kunia bundle: Kahe 2–Halawa ×2, Kahe 2–Waiau, Kahe 2–TAP (4 ckts); Waipio/Waiau side: Kahe–Waiau return, **Wahiawa–Waiau**, Kahe–Halawa returns ×2 |
| SL-B | **2 (2)** | 2 | 1 (1) | **Wahiawa–Waiau 138 kV** (19.6 km) and **Wahiawa–Kunia-junction 138 kV** (8.1 km, continues to Kahe); one mapped Kunia-road 46 kV chain |
| SL-C | **0 (0)** | 0 | 2 (2) | Waialua↔Wahiawa-area 46 kV (12.2 km branch) and a Helemano-area 46 kV branch. **No 138 kV exists north of Wahiawa.** |

46 kV under-mapping (both sources map only ~80–140 of several hundred
circuit-km) cuts against SL-A and SL-C: zero mapped 46 kV crossings at SL-A
is certainly wrong (Waipahu/Pearl City sub-transmission crosses there), and
a windward-coast 46 kV path toward Kahuku likely exists but is unmapped at
SL-C's latitude (mapped windward features stop ~12 km south of it)
[UNVERIFIED]. Unmapped 46 kV plausibly adds ~100–300 MVA at SL-A and one
more ~30–60 MVA path at SL-C; **not counted below.**

## Capacity guesses (flagged: educated guesses)

Per-circuit planning-typical thermal ratings, ambient-derated for island
heat: **138 kV single circuit 150–250 MVA; 46 kV 30–60 MVA.** Conductor
types unknown; HECO's actual normal/emergency ratings confidential.

| Screenline | Low (parity-net × low rating) | Central (geometric × 200/45) | High (geometric × 250/60) |
|---|---|---|---|
| SL-A | 300 MVA | **1,600 MVA** | 2,000 MVA |
| SL-B | 330 MVA | **445 MVA** | 560 MVA |
| SL-C | 60 MVA | **90 MVA** | 120 MVA |

Sanity anchor for SL-C: existing North Shore generation (Kawailoa wind
69 MW + Kawailoa solar 49 MW + Kahuku-area wind ~54 MW ≈ **~170 MW
nameplate**, project figures from prior notes, approximate) already sits
north of SL-C against a guessed 60–120 MVA neck — consistent with the North
Shore's documented curtailment/queue problems [inference, UNVERIFIED].

## Requirement model

Transparent scenario arithmetic, no power flow (grid in
`screenline_requirements.csv`; all parameter combinations included):

- S = installed northern/central solar ∈ {1, 2, 3, 4} GW, split
  **Kunia 50% / Wahiawa 25% / Waialua+Kahuku 25%** across the cuts
  (f-shares: SL-A 1.0, SL-B 0.5, SL-C 0.25) — illustrative ASSUMPTION.
- Co-located storage, 4–6 h duration, power ρ·S with ρ ∈ {0.5, 0.75, 1.0}.
- Southern load share σ ∈ {0.70, 0.775, 0.85}; Oahu peak L ∈ {1.2 (today),
  1.75, 2.0 (2045 electrified)} GW; midday load = 0.85·L (assumption).
- Load north of SL-B / SL-C: 5% / 2.5% of island load (population-share
  assumption).
- Southern firm generation at evening peak G_s ∈ {0, 400} MW (0 = thermal
  fleet fully retired; 400 ≈ CTs/Kalaeloa retained). Today G_s ≈ 1.5 GW and
  nothing binds — the whole issue is the retirement endgame.
- **Evening requirement** = min(σ·L − G_s, ρ·S·f): what the north-of-cut
  storage can send vs what the south still needs.
- **Midday requirement** = min(max(f·S − f·ρ·S − load north of cut, 0),
  σ·0.85·L): direct delivery while charging, capped by southern absorption.
- Requirement = max(evening, midday); **N-1** adds the largest single
  circuit crossing the cut (250 MVA at A/B; 250 used for post-upgrade C).

### Required N→S transfer (MW), σ = 0.775, G_s = 0

| Cut | Case | S=1 | S=2 | S=3 | S=4 |
|---|---|---|---|---|---|
| SL-A | today (L=1.2), ρ=0.5 | 500 | 930 | 930 | 930 |
| SL-A | today (L=1.2), ρ=1.0 | 930 | 930 | 930 | 930 |
| SL-A | 2045 (L=2.0), ρ=0.5 | 500 | 1,000 | 1,500 | 1,550 |
| SL-A | 2045 (L=2.0), ρ=1.0 | 1,000 | 1,550 | 1,550 | 1,550 |
| SL-B | 2045 (L=2.0), ρ=0.5 | 250 | 500 | 750 | 1,000 |
| SL-B | 2045 (L=2.0), ρ=1.0 | 500 | 1,000 | 1,500 | 1,550 |
| SL-C | 2045 (L=2.0), ρ=0.5 | 125 | 250 | 375 | 500 |
| SL-C | 2045 (L=2.0), ρ=1.0 | 250 | 500 | 750 | 1,000 |

**Storage changes everything.** With 4–6 h co-located storage at 50–100% of
solar power, midday export need collapses (charging soaks up the surplus)
and the binding hour moves to the evening — so the island-level requirement
**saturates at σ × evening load (≈ 0.84–1.7 GW across the σ and L ranges),
not at installed solar MW (up to 4 GW)**. The corridor problem is an
evening-peak delivery problem roughly the size of southern load, whatever
the solar build. (Six-hour storage discharged across the whole evening
rather than at full power would cut the required MW further; the table's
ρ·S evening term is conservative for the sub-cuts.)

### Requirement vs guessed capacity: the gaps (central capacity, N-0 / N-1, MW)

2045 load (L=2.0), σ=0.775, G_s=0. Negative = headroom.

| Cut | Capacity (central) | S=2, ρ=0.5 | S=2, ρ=1.0 | S=4, ρ=0.5 | S=4, ρ=1.0 |
|---|---|---|---|---|---|
| SL-A | 1,600 | −600 / −350 | −50 / +200 | −50 / +200 | −50 / +200 |
| SL-B | 445 | +55 / +305 | **+555 / +805** | +555 / +805 | **+1,105 / +1,355** |
| SL-C | 90 | +160 / +220 | **+410 / +470** | +410 / +470 | **+910 / +970** |

Readings:

- **SL-C is the hard wall**: ~90 MVA guessed vs 250–1,000 MW required. Any
  utility-scale Waialua/Kahuku build beyond ~100–200 MW needs new wires —
  there is no 138 kV north of Wahiawa to reconductor.
- **SL-B binds next**: two 138 kV circuits (~445 MVA central) vs
  0.5–1.55 GW. Binding already at ~2 GW total northern solar.
- **SL-A is roughly adequate under the central reading** (1,600 MVA vs a
  requirement that saturates at ~1,550), *because* of the storage
  saturation effect — but only if the Kahe-loop circuits through the bench
  are usable for southbound delivery (they are tappable; Kunia projects
  interconnect there), and N-1 leaves it ~200 MW short. Under the
  conservative parity reading (300 MVA) SL-A would show a 0.7–1.25 GW gap;
  the truth is much closer to the central reading for bench-sited solar.
- With G_s = 400 MW retained in the south, every evening requirement drops
  by 400 MW: SL-A clears entirely, SL-B's 2-GW gap roughly halves. Keeping
  a few hundred MW of southern firm capacity (or siting storage south of
  SL-A and charging it midday) is worth ~$100M+ of wires.

## Upgrade options and planning-level costs (ASSUMPTIONS)

Unit costs are Hawaii-adjusted planning guesses consistent with
`docs/ASSUMPTIONS.md` C5–C8 (mainland benchmarks × 1.5–2.5 HI multiplier,
flagged [U] there); no repo citation to utility actuals.

| Option | Thermal gain | Unit cost | Notes |
|---|---|---|---|
| HTLS reconductor existing 138 kV | ×1.5–2 per circuit (+75–250 MVA) | $0.5–1.5M/ckt-km | fastest; existing towers/ROW; outage scheduling on a 2-circuit corridor is the real constraint |
| Second circuit on existing towers/ROW | +150–250 MVA | $1–2.5M/km | where structures were built double-circuit-ready [unknown for HECO] |
| New double-circuit 138 kV in existing ROW | +300–500 MVA | $2–4M/km | the workhorse option north of Wahiawa (46 kV ROWs exist Waialua–Wahiawa and toward Kahuku) |
| 230 kV overlay (new voltage class for Oahu) | +400–800 MVA/ckt | $3–5M/km **+** 2–3 transformer stations at $20–40M each | step change: new transformer class, spares, breaker standards. **Not needed at these distances**: at 10–25 km thermal, not stability/SIL, governs — N parallel 138 kV circuits are viable and modular |

Corridor lengths (HIFLD-measured / planning): Waialua→Wahiawa ~10 km;
Kahuku→Wahiawa ~18 km; Wahiawa→Waiau 19.6 km (existing 138 kV ROW);
Wahiawa→Kunia junction 8.1 km.

### Program sketch to close the gaps (2045 load, σ=0.775, ρ=0.75, G_s=0)

**~2 GW northern solar** (needs: SL-B ≈750 N-0 / 1,000 N-1; SL-C ≈375 / 625):

| Element | Km | Cost | Adds |
|---|---|---|---|
| New double-circuit 138 kV Waialua–Wahiawa (existing 46 kV ROW) | ~10 | $20–40M | +300–500 MVA at SL-C |
| Continue it Wahiawa–Waiau in the existing 138 kV ROW | ~20 | $40–80M | +300–500 MVA at SL-B (and SL-A) |
| HTLS the two existing Wahiawa 138 kV circuits | ~25 ckt-km | $13–38M | +150–500 MVA at SL-B |
| Substations: Waialua collector, Wahiawa 138 kV expansion, Waiau bays | — | $20–90M | — |
| **Total ≈ $90–250M** | | | SL-C → ~390–620 MVA; SL-B → ~900–1,450 MVA |

**~4 GW northern solar** (needs: SL-B ≈1,500 / 1,750; SL-C ≈750 / 1,000) —
add to the above:

| Element | Km | Cost | Adds |
|---|---|---|---|
| New double-circuit 138 kV Kahuku–Wahiawa (along existing 46 kV/highway corridor; some new ROW) | ~18 | $36–72M | +300–500 MVA at SL-C |
| Second Wahiawa–Waiau double circuit (or rebuild existing to double) | ~20 | $40–80M | +300–500 MVA at SL-B |
| Kahuku collector + additional bays | — | $20–60M | — |
| **Increment ≈ $96–212M; cumulative ≈ $190–460M** | | | SL-C → ~690–1,120; SL-B → ~1,200–1,950 |

At the low end of the rating assumptions the 4 GW program still runs
~100–300 MW short of strict N-1 at both cuts — one more double-circuit run
(~$40–80M) covers it; at the high end it clears with margin. **Order of
magnitude: closing the north→south gap costs ~$0.1–0.25B for 2 GW and
~$0.2–0.5B for 4 GW — roughly 2–5% of the corresponding $4–10B solar+storage
capex** (solar capex ~$2–2.5M/MWac, ASSUMPTIONS C9). The wires are
second-order to the land question, same conclusion as the corridor and
expansion-curve notes — but they are *lumpy and slow* (ROW, permitting,
outage windows), which is where siting friction and transmission interact.

## Caveats (beyond the global ASSUMPTION flag)

- No power-flow, stability, or voltage analysis; screenline arithmetic
  only. Real deliverability depends on substation topology, transformer
  capacity (138/46 kV), and contingency dispatch, none public.
- Public line maps: 138 kV reliable (two sources agree, ~325 km); 46 kV
  badly under-mapped; a drawn line may be a double-circuit tower (counts
  are lower bounds); HIFLD vintage 2017–2020.
- The f-share portfolio split (50/25/25) and load-north-of-cut fractions
  are invented for transparency, not derived from our parcel screens.
- Storage dispatch is stylized (full-power evening discharge); duration
  (4–6 h) enters only through the "charging absorbs midday surplus" logic.
- Costs: mainland planning benchmarks × an UNVERIFIED Hawaii multiplier;
  no HECO actuals; substation costs dominate short runs and are the
  loosest numbers here.

## Further investigation

1. **HECO Integrated Grid Plan (IGP) transmission analyses** (PUC Docket
   2018-0165 / IGP docs): HECO's own N-1 transfer limits for the
   Wahiawa/North Shore area — would replace the guessed ratings outright.
2. **Interconnection queue + RFP deliverability disclosures** (Stage 1/2/3
   RFP appendices sometimes name constrained substations/circuits): test
   the SL-C/SL-B wall against revealed developer behavior — do bids cluster
   south of SL-B?
3. **Curtailment records for Kawailoa/Kahuku projects** (PUC filings, PPA
   amendment dockets): direct evidence on today's North Shore neck.
4. FERC Form 1 / HECO rate-case plant records: conductor types and any
   public ampacity for the Wahiawa–Waiau and Kahe circuits.
5. OSM/HIFLD ground-truthing of the 46 kV system from imagery along the
   windward coast (does a Kahuku-bound 46 kV path cross SL-C's latitude?).
6. Whether the Wahiawa 138/46 kV substation has spare bay capacity — it is
   the hinge of every upgrade path above [unknown].
7. Paper hook: if the state liberalizes the ag-land cap (S3), the unlocked
   acreage concentrates in Waialua/Kunia — precisely the areas behind
   SL-B/SL-C. The binding constraint sequence (statute → wires) and who
   pays for the wires (ratepayers vs developers via interconnection
   upgrades) is a political-economy question of its own.
