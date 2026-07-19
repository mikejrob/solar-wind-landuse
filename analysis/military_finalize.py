#!/usr/bin/env python3
"""Add constraint / viability coding to data/oahu_military_land.csv and print
the tenure x viability summary. Coding is a SCREEN-LEVEL judgment from the
research memo (DoD rules + the Aug-2025 Army ROD), NOT a DoD determination;
flagged UNVERIFIED in the note column."""
from pathlib import Path
import pandas as pd

PROJECT = Path("/Users/michaelroberts/Research/solar-wind-landuse")
df = pd.read_csv(PROJECT / "data" / "oahu_military_land.csv")

# ---- 2029 state-lease parcels: outcome per Army ROD (7 Aug 2025) ----
LEASE = {
 # tmk : (viability_flag, note)
 "172001006": ("returns_2029_steep_conservation",
    "Kawailoa-Poamoho: ROD=No Action, lease EXPIRES 2029, returns to State. Mostly steep Conservation-district training land; ~197 ac flat, 2.3km to 46kV+."),
 "158002002": ("retained_army_rod",
    "Kahuku TA: ROD=modified retention (~450 ac). This flat, Ag-district, grid-adjacent (0.07km) parcel is the land the Army KEEPS - NOT returning."),
 "159006026": ("partial_return_steep",
    "Kahuku TA: portion beyond the ~450-ac modified-retention footprint returns 2029; steep Conservation, 2.7km to grid."),
 "182001024": ("returns_2029_uxo_remote",
    "Makua Military Reserve: ROD=No Action, lease EXPIRES 2029. Dense UXO, live-fire ended; ~72 ac flat but 12km to 46kV+."),
 "181001007": ("returns_2029_uxo_remote",
    "Makua Military Reserve: ROD=No Action, expires 2029; UXO, remote, 11km to grid."),
 "169003005": ("returns_2029_remote_tiny",
    "Kaena Pt Satellite Tracking (Air Force): Conservation, 13km to grid, remote NW point."),
 "167003023": ("returns_2029_remote_tiny",
    "Kaala Air Station (Air Force): 1.9 ac summit site, Conservation, remote."),
}

# ---- fee/other installations: dominant DoD constraint (keyword on name) ----
def fee_flag(name):
    n = name.lower()
    if "west loch" in n:
        return ("precedent_built",
                "ESQD-restricted magazine annex, but hosts Kupono Solar (42MW+168MWh, Navy EUL, COD 2024) and earlier ~20MW HECO array - the one proven Oahu military-solar site.")
    if any(k in n for k in ["lualualei","kipapa ammo","puuloa range","red hill","waikane","laulaunui"]):
        return ("excluded_ordnance_esqd",
                "Ordnance/magazine or live-fire range; ESQD arcs and UXO restrict occupied use (UNVERIFIED at parcel level).")
    if any(k in n for k in ["makua","east range","kahuku training","poamoho","dillingham","helemano","schofield east","training area bellows"]):
        return ("excluded_active_training_uxo",
                "Active/former maneuver or impact-range land; training tempo + UXO (UNVERIFIED at parcel level).")
    if any(k in n for k in ["wheeler","jbphh","marine corp","marine corps","mcbh","kaala","kalaeloa","bellow"]):
        return ("excluded_airfield_airspace",
                "Active airfield / airspace / glint-glare screening zone (SGHAT + DoD Siting Clearinghouse; UNVERIFIED).")
    if any(k in n for k in ["schofield barracks","fort shafter","tripler","aliamanu","camp smith","wahiawa annex","waipio peninsula","pearl city peninsula","ford island"]):
        return ("plausibly_usable_eul",
                "Developed cantonment / underused fee land where an EUL (10 USC 2667) is mechanically plausible; NOT a DoD-vetted site - scalability beyond West Loch is UNPROVEN.")
    return ("excluded_developed_or_small",
            "Housing, cemetery, storage, beach, comms, or sub-parcel; not a utility-scale candidate.")

for i, r in df.iterrows():
    if r.tenure == "state_lease_2029":
        f, note = LEASE.get(str(r.tmk).split(".")[0], ("returns_2029_other", ""))
    else:
        f, note = fee_flag(r["name"])
    df.at[i, "primary_constraint"] = f.split("_")[0] if f.startswith("excluded") else ""
    df.at[i, "viability_flag"] = f
    df.at[i, "notes"] = note

cols = ["name","tenure","branch","tmk","acres","acres_le15","acres_le30",
        "dist_46kv_km","dist_138kv_km","slud","lease_state_owned",
        "viability_flag","notes","owner","source"]
df = df[cols].sort_values(["tenure","acres"], ascending=[True, False])
df.to_csv(PROJECT / "data" / "oahu_military_land.csv", index=False)

print("=== VIABILITY x TENURE (acres <=15% slope) ===")
piv = df.groupby(["tenure","viability_flag"]).agg(
    n=("name","size"), ac=("acres","sum"), flat=("acres_le15","sum")).round(0)
print(piv.to_string())
print("\n2029 state-lease parcels (the return question):")
print(df[df.tenure=="state_lease_2029"][["name","tmk","acres","acres_le15","dist_46kv_km","slud","viability_flag"]].to_string(index=False))
print("\nwrote data/oahu_military_land.csv")
