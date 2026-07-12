"""Step 8: economic-viability classification of non-ag solar candidates.

Classes (documented in notes/oahu-nonag-solar.md):
- durable: public owners (State/DLNR/DHHL/HCDA/UH/HTDC/HHFDC/county) unless
  assessed land >= $2M/ac (urban-park/high-amenity guard -> uncertain);
  quarry/landfill/brownfield sites unless owned by a named pipeline developer;
  private low-improvement parcels with assessed land < $50k/ac and not a
  pipeline owner.
- higher_value_development: named entitled-pipeline owners (D.R. Horton,
  Makaiwa Hills, Haseko/Hoakalei, North Shore Bay/Turtle Bay, Castle & Cooke,
  Gentry, Ko Olina, Aina Nui) regardless of assessed value (master-planned
  land is often assessed near ag rates pre-subdivision), OR private parcels
  with assessed land >= $500k/ac.
- uncertain: everything else in the headline candidate tier (private,
  $50k-$500k/ac, non-pipeline; missing-value parcels; high-value public).
Only headline-tier candidates (low-improvement, >=10 ac <=15% slope,
non-military, non-airport/harbor/golf/cemetery) and special sites are
classified; other rows keep viability_class = "".
"""
from pathlib import Path
import geopandas as gpd
import numpy as np
import pandas as pd

SCRATCH = Path("/private/tmp/claude-503/-Users-michaelroberts-Research-solar-wind-landuse/d73405a1-d30d-4ac4-8a47-d64b30b982a9/scratchpad")
PROJECT = Path("/Users/michaelroberts/Research/solar-wind-landuse")

LOW_VAL, HIGH_VAL, PUB_GUARD = 50_000, 500_000, 2_000_000
PIPE = (r"D R HORTON|MAKAIWA HILLS|HASEKO|HOAKALEI|NORTH SHORE BAY|TURTLE BAY"
        r"|CASTLE & COOKE|GENTRY|KO OLINA|AINA NUI")
PUB_STR = (r"^S OF H|STATE OF HAWAII|CITY AND COUNTY|CTY & CTY|HAWAIIAN HOME"
           r"|UNIVERSITY OF HAWAII|HAWAII COMM DEV|HAWAII TECHNOLOGY DEV"
           r"|HOUSING FINANCE|HAWAII PUBLIC HOUSING")

cand = gpd.read_parquet(SCRATCH / "urban_candidates_enriched.parquet")
cand = cand.drop_duplicates(subset="tmk9txt").reset_index(drop=True)

def tag(o):
    o = (o if isinstance(o, str) else "").upper()
    for kw, t in [("AIRPORT", "airport"), ("HARBOR", "harbor"),
                  ("GOLF", "golf"), ("COUNTRY CLUB", "golf"),
                  ("CEMETERY", "cemetery"), ("MEMORIAL PARK", "cemetery")]:
        if kw in o:
            return t
    return ""

cand["use_tag"] = cand.own1.map(tag)
cand["lvpa"] = (cand.landvalue / cand.urban_acres).replace([np.inf, -np.inf], np.nan)
own_u = cand.own1.fillna("").str.upper()
cand["pipeline"] = own_u.str.contains(PIPE)
cand["public"] = cand.govtype.notna() | own_u.str.contains(PUB_STR)
cand["strict"] = (~cand.military & cand.low_improvement & (cand.acres_le15 >= 10)
                  & ~cand.use_tag.isin(["airport", "harbor", "golf", "cemetery"]))

def classify(r):
    if not r.strict:
        return ""
    if r.public and not r.pipeline:
        if r.lvpa == r.lvpa and r.lvpa >= PUB_GUARD:
            return "uncertain"
        return "durable"
    if r.pipeline:
        return "higher_value_development"
    if r.lvpa == r.lvpa and r.lvpa < LOW_VAL:
        return "durable"
    if r.lvpa == r.lvpa and r.lvpa >= HIGH_VAL:
        return "higher_value_development"
    return "uncertain"

cand["viability_class"] = cand.apply(classify, axis=1)

# ---- special sites: host-parcel assessed value ----
sites = gpd.read_parquet(SCRATCH / "osm_sites.parquet")
sites = sites[sites.acres >= 5].reset_index(drop=True)
sv = pd.read_csv(SCRATCH / "site_tmk_values.csv", dtype={"tmk": str})
parc = gpd.read_parquet(PROJECT / "data/gis/parcels_oahu.parquet")
pac = parc.groupby("tmk9txt").gisacres.sum()
sites["tmk8"] = sites.site_tmk.astype(str).str[1:]
sites = sites.merge(sv.rename(columns={"tmk": "tmk8"}), on="tmk8", how="left")
sites["host_acres"] = sites.site_tmk.astype(str).map(pac)
sites["lvpa"] = sites.landvalue / sites.host_acres
sites["pipeline"] = sites.owner_true.fillna("").str.upper().str.contains(PIPE)
sites["viability_class"] = np.where(
    (sites.landuse == "brownfield") & sites.pipeline,
    "higher_value_development", "durable")

print("=== urban-parcel classes (strict tier) ===")
st = cand[cand.strict]
print(st.groupby("viability_class").agg(
    n=("tmk9txt", "count"), ac15=("acres_le15", "sum"),
    ac30=("acres_le30", "sum")).round(0))
print("=== special-site classes ===")
print(sites.groupby("viability_class").agg(
    n=("osm_id", "count"), ac_tot=("acres", "sum"),
    ac15=("acres_le15", "sum"), ac30=("acres_le30", "sum")).round(0))
for vc, g in st.groupby("viability_class"):
    a = g.acres_le15.sum()
    print(f"{vc}: MW range {a/7:,.0f}-{a/5:,.0f}")

# ---- rewrite candidates CSV in place ----
csvp = PROJECT / "data/oahu_nonag_solar_candidates.csv"
d = pd.read_csv(csvp, dtype={"tmk_or_site": str})
d = d.drop(columns=["land_value_per_ac", "viability_class"], errors="ignore")
lv_map = cand.set_index("tmk9txt").lvpa
vc_map = cand.set_index("tmk9txt").viability_class
s_lv = sites.set_index("osm_id").lvpa
s_vc = sites.set_index("osm_id").viability_class
d["land_value_per_ac"] = d.tmk_or_site.map(lv_map).fillna(d.tmk_or_site.map(s_lv)).round(0)
d["viability_class"] = d.tmk_or_site.map(vc_map).fillna(d.tmk_or_site.map(s_vc)).fillna("")
d.loc[d.type == "military_note", "viability_class"] = ""
# order: insert after owner
cols = list(d.columns[:-2])
i = cols.index("owner") + 1
cols = cols[:i] + ["land_value_per_ac", "viability_class"] + cols[i:]
d = d[cols]
d.to_csv(csvp, index=False)
print(f"wrote {csvp} ({len(d)} rows)")

# ---- top-parcels table ----
NAMES = {
    "196005013": "Waiawa (Kamehameha Schools)",
    "146016001": "He'eia CDD (HCDA)",
    "139011002": "Waimanalo (State of Hawaii)",
    "191182009": "Kapolei mauka (C&C Honolulu)",
    "191016179": "UH West O'ahu lands",
    "191013061": "Kalaeloa (DHHL)",
    "195002057": "Whitmore Village (HTDC)",
    "191031001": "Kalaeloa/Barbers Pt (State DOA)",
    "191013038": "East Kapolei (DHHL)",
    "162001001": "Kawailoa/Haleiwa (Kamehameha Schools)",
    "156002055": "Kahuku (C&C Honolulu)",
    "191016222": "UH West O'ahu lands",
    "184002058": "Makaha Valley (HRT Kili Drive)",
    "185002052": "Waianae (EE Waianae Solar)",
    "191018014": "Honouliuli (DLNR)",
    "191016126": "East Kapolei (HHFDC)",
    "141015015": "Waimanalo Gulch side/Ewa? (C&C)",
    "115041006": "Sand Island (DLNR)",
    "146016032": "Kaneohe (C&C Honolulu)",
    "192050001": "Makaiwa Hills (Kapolei mauka)",
    "192050003": "Makaiwa Hills (Kapolei mauka)",
    "191014095": "Kalaeloa (Kapolei Properties/Hunt)",
    "156003062": "Turtle Bay area (North Shore Bay Owner)",
    "191018054": "Ho'opili area (D.R. Horton)",
    "191017213": "Ho'opili area (D.R. Horton)",
    "way/1354424725": "Pacific Aggregate quarry (Wahiawa)",
    "way/239954711": "Kapaa Quarry (Kailua)",
    "way/267608678": "Makakilo Quarry (Grace Pacific)",
    "way/396515036": "Halawa Quarry (Queen Emma)",
    "way/446606190": "Waimanalo Gulch landfill (C&C)",
}
top = d[d.viability_class == "durable"].sort_values("acres_le15", ascending=False).head(15)
hv = d[d.viability_class == "higher_value_development"].sort_values("acres_le15", ascending=False).head(5)
SITE_NOTE = {
    "196005013": "largest single durable parcel; KS trust land assessed near ag rates; adjacent Waiawa solar precedent",
    "146016001": "He'eia community development district; flat but includes wetland/ag-park uses - field check needed",
    "139011002": "state land in Waimanalo; far from 138kV (11.8 km) - 46kV-scale projects only",
    "191182009": "county land mauka of Kapolei, on the 138kV corridor",
    "191016179": "UH West O'ahu surplus lands, on the 138kV corridor; UH has solicited development here",
    "way/1354424725": "active quarry, host parcel assessed ~$7k/ac; 7 km to 138kV",
    "115041006": "Sand Island; high-value ($1.7M/ac) industrial/park land - weakest of the durable set",
    "191013061": "DHHL Kalaeloa; durable vs development depends on homestead pipeline timing",
    "195002057": "HTDC Whitmore Village ag-tech park lands, adjacent 138kV",
    "191031001": "State DOA land at Kalaeloa/Barbers Point, 0.3 km to 138kV",
    "191013038": "DHHL East Kapolei; homestead pipeline caveat as above",
    "162001001": "KS Kawailoa/Haleiwa; 14 km from 138kV - North Shore 46kV only",
    "way/239954711": "active quarry complex (+2 pits, 43 ac same owner); 138kV crosses site",
    "156002055": "county land at Kahuku; 21 km from 138kV grid",
    "191016222": "UH West O'ahu; higher assessed value ($1.25M/ac) than sibling parcel",
    "192050001": "Makaiwa Hills master-planned community (entitled); assessed near zero pending subdivision",
    "191014095": "Hunt land at Kalaeloa; $622k/ac; active development area with some existing solar",
    "192050003": "Makaiwa Hills master-planned community (entitled)",
    "156003062": "Turtle Bay resort expansion lands; remote from 138kV (22 km)",
    "191018054": "Ho'opili (D.R. Horton) entitled residential; assessed near zero pending subdivision",
}
rows = []
for _, r in pd.concat([top, hv]).iterrows():
    rows.append({
        "site_name": NAMES.get(r.tmk_or_site, ""),
        "tmk_or_site": r.tmk_or_site, "owner": r.owner, "type": r.type,
        "acres_le15": r.acres_le15,
        "land_value_per_ac": r.land_value_per_ac,
        "dist_138kv_km": r.dist_138kv_km,
        "viability_class": r.viability_class,
        "note": SITE_NOTE.get(r.tmk_or_site, ""),
    })
tp = pd.DataFrame(rows)
print(tp.to_string())
tp.to_csv(PROJECT / "data/gis/nonag_top_parcels.csv", index=False)

# stash classification for the figure
cand[["tmk9txt", "viability_class", "strict", "lvpa"]].to_csv(
    SCRATCH / "class_by_tmk.csv", index=False)
sites[["osm_id", "viability_class"]].to_csv(SCRATCH / "class_by_site.csv", index=False)
