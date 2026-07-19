#!/usr/bin/env python3
"""Merge status/solar-side/viability coding onto the golf GIS table and write
the final data/oahu_golf_courses.csv + district-overlap summary."""
from pathlib import Path
import pandas as pd

PROJECT = Path("/Users/michaelroberts/Research/solar-wind-landuse")
df = pd.read_csv(PROJECT / "data" / "oahu_golf_courses_gis.csv", dtype={"tmk": str})

# rename the three OSM-unnamed polygons (identified via TMK owner + location)
RENAME = {
    "__noname_221300526": "Barbers Point Golf Course",
    "__noname_8987946": "Mid-Pacific Country Club",
    "__noname_1094652470": "Olomana Golf Links",
}
df["name"] = df["name"].replace(RENAME)

# hand-coded from the research memo (sources carried in note); keyed by name.
# status: open / closed ; solar_side: leeward_sunny / windward_wet / north_marginal
# redevelopment: housing_pipeline / conservation_reuse / flood_basin / none / military
CODE = {
 "Turtle Bay Golf":        ("open","north_marginal","none","Palmer+Fazio; Fazio reopened after 2020 COVID closure; Arete 99-yr golf lease 2024; resort Host Hotels"),
 "Hoakalei Country Club":  ("open","leeward_sunny","none","Ernie Els course; Hirakawa Shoji ($25M 2014); inside Hoakalei master community"),
 "Hawaii Prince Golf Club":("open","leeward_sunny","watch","Prince/Seibu asset-light watch; no HI sale ordered"),
 "Barbers Point Golf Course":("open","leeward_sunny","military","Navy MWR, Kalaeloa; retained federal after 1999 BRAC"),
 "Ko'olau Golf Club":      ("closed","windward_wet","conservation_reuse","CLOSED 9/30/2020; First Presbyterian Church; plan farming/native habitat/cultural-ed via CDUP; NO housing; cliff-shadowed poor solar"),
 "Coral Creek Golf Course":("open","leeward_sunny","none","public, 1999"),
 "Pearl Country Club":     ("open","leeward_sunny","none","Pearl at Kalauao; KS regained control 2020, reinvested to keep golf; Troon"),
 "Leilehua Golf Course":   ("open","leeward_sunny","military","Army DFMWR; civilian walk-on"),
 "Royal Hawaiian Golf Club":("open","windward_wet","none","Luana Hills, Maunawili valley; financially unstable history"),
 "Kapolei Golf Course":    ("open","leeward_sunny","none","DAITO US INC; public; adjacent Gentry homes NOT a course conversion"),
 "Ko Olina Golf Club":     ("open","leeward_sunny","none","Ko Olina Resort; Jeff Stone/Resort Group; LPGA host"),
 "Mamala Bay Golf Course": ("open","leeward_sunny","military","Hickam/JBPHH Navy MWR"),
 "Ewa Villages Golf Course":("open","leeward_sunny","none","C&C muni, 1996"),
 "West Loch Golf Course":  ("open","leeward_sunny","none","C&C muni, 1990"),
 "Hawaii Kai Golf Course": ("open","leeward_sunny","none","Championship+Executive; KS master-lease history"),
 "Pali Golf Course":       ("open","windward_wet","none","C&C muni, 1953; Conservation zoned"),
 "Makaha Valley Country Club":("closed","leeward_sunny","housing_pipeline","Resort 664ac sold Aug 2022 $20.7M to KH Group; Championship course CLOSED ~2011; plan ~494 homes+152 condos+2 courses; East course still open; grid-distant"),
 "Mililani Golf Course":   ("open","leeward_sunny","none","central plateau; LA-Korean investor"),
 "Navy Marine Golf Course":("open","leeward_sunny","military","JBPHH Navy MWR, military-only"),
 "Royal Kunia Country Club":("open","leeward_sunny","none","opened 2003; 'Meadows at Royal Kunia' is a SEPARATE never-built parcel"),
 "Mid-Pacific Country Club":("open","windward_wet","none","Lanikai/Kailua private member club; Bishop Estate/KS land (UNVERIFIED exact polygon)"),
 "Ewa Beach Golf Club":    ("open","leeward_sunny","none","360 Ewa Beach CC; LA Koreana 2022 (sale, not closure)"),
 "Ted Makalena Golf Course":("open","leeward_sunny","none","C&C muni, Waipahu, 1971"),
 "Waiʻalae Country Club":  ("open","leeward_sunny","none","private, Sony Open host; Kahala"),
 "Klipper Golf Course":    ("open","windward_wet","military","MCBH Kaneohe Bay, Mokapu; USMC"),
 "Waikele Golf Club":      ("open","leeward_sunny","none","Hoban Group (Korea)"),
 "Honolulu Country Club":  ("open","leeward_sunny","none","Salt Lake; sold 2022 undisclosed buyer; Conservation zoned"),
 "Ala Wai Golf Course":    ("open","leeward_sunny","flood_basin","C&C muni, Waikiki; USACE Ala Wai flood project would convert ENTIRE course to detention basin (~$1-11B, under review)"),
 "Olomana Golf Links":     ("open","windward_wet","none","Waimanalo; STATE land General Lease S-4095; DLNR revitalization master plan Nov 2025"),
 "Hawaii Country Club":    ("open","leeward_sunny","none","Kunia Rd/Wahiawa; public par-71 1957; poorly maintained but operating"),
 "Oʻahu Country Club":     ("open","windward_wet","none","Nuuanu valley (wetter); member club owns land fee-simple"),
 "Bayview":                ("open","windward_wet","none","Bay View Golf Park, Kaneohe; public 1963"),
 "Kahuku Golf Course":     ("open","north_marginal","none","C&C muni 9-hole, oceanfront, 1937"),
 "Fort Shafter Golf Course":("open","leeward_sunny","military","Walter Nagorski GC, Army DFMWR, 9-hole"),
 "Moanalua Golf Club":     ("open","leeward_sunny","none","oldest HI course, 1898, S.M. Damon; 9-hole semi-private"),
 "Bellows Golf Course":    ("open","windward_wet","military","Bellows AFS, Waimanalo"),
}

df["status"] = df.name.map(lambda n: CODE.get(n, ("open","",""," "))[0])
df["solar_side"] = df.name.map(lambda n: CODE.get(n, ("","","",""))[1])
df["redevelopment"] = df.name.map(lambda n: CODE.get(n, ("","","",""))[2])
df["note"] = df.name.map(lambda n: CODE.get(n, ("","","",""))[3])

# viability: closed + leeward_sunny + flat(>=10ac<=15%) + near-grid(<=3km46kV)
#            + not military + not housing/flood pipeline
def viab(r):
    if r.status == "closed":
        if r.solar_side == "leeward_sunny" and r.acres_le15 >= 10 \
           and r.dist_46kv_km <= 3 and r.redevelopment not in ("housing_pipeline","flood_basin","military"):
            return "closed_viable"
        if r.solar_side != "leeward_sunny":
            return "closed_low_solar"
        return "closed_contested"       # leeward but housing/grid-distant
    return "open_operating"
df["viability_flag"] = df.apply(viab, axis=1)
df["owner"] = df["owner_rpad"]
df["source"] = "OSM leisure=golf_course (geom); RPAD OWNALL owner; status/solar-side from research memo (data/raw/military-golf/MANIFEST.md)"

cols = ["name","status","solar_side","acres","acres_le15","acres_le30",
        "dist_46kv_km","dist_138kv_km","slud","zone_class","owner",
        "redevelopment","viability_flag","tmk","lon","lat","note","source"]
df = df[cols].sort_values(["status","acres"], ascending=[True, False])
df.to_csv(PROJECT / "data" / "oahu_golf_courses.csv", index=False)

# ---- summaries ----
print("=== STATUS COUNTS ===")
print(df.status.value_counts().to_dict())
print("\nCLOSED courses:")
print(df[df.status=="closed"][["name","solar_side","acres","acres_le15","dist_46kv_km","slud","zone_class","redevelopment","viability_flag"]].to_string(index=False))
print("\n=== golf acreage by SLUD district (screen-correction) ===")
g = df.groupby("slud").agg(n=("name","size"), acres=("acres","sum"),
                           acres_le15=("acres_le15","sum")).round(0)
print(g)
print(f"\nTOTAL: {len(df)} courses, {df.acres.sum():,.0f} ac, {df.acres_le15.sum():,.0f} ac <=15%")
urb = df[df.slud=="Urban"]
print(f"Urban-district golf (what the non-ag screen netted out): {len(urb)} courses, "
      f"{urb.acres.sum():,.0f} ac, {urb.acres_le15.sum():,.0f} ac <=15%")
agd = df[df.slud=="Ag"]
print(f"Ag-district golf (inside ag universe / double-count with ag screen): {len(agd)} courses, "
      f"{agd.acres.sum():,.0f} ac, {agd.acres_le15.sum():,.0f} ac <=15%")
print("\nwrote data/oahu_golf_courses.csv")
