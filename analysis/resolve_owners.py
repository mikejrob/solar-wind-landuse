"""Entity resolution + owner_type for Oahu ag-district parcel owners (OWNALL bulk)."""
import re
import pandas as pd

SP = "/private/tmp/claude-503/-Users-michaelroberts-Research-solar-wind-landuse/d73405a1-d30d-4ac4-8a47-d64b30b982a9/scratchpad"
PROJ = "/Users/michaelroberts/Research/solar-wind-landuse"
OWNALL_URL = "https://services.arcgis.com/tNJpAOha4mODLkXz/arcgis/rest/services/CadastralTables/FeatureServer/5 (City & County of Honolulu RPAD OWNALL table, taxyr 2027)"
GOV_URL = "https://geodata.hawaii.gov/arcgis/rest/services/ParcelsZoning/MapServer/19 (Government Lands - Detailed)"

m = pd.read_csv(f"{SP}/merged_oahu.csv", dtype={"tmk": str})

# ---------------- manual mapping: raw -> (resolved, type, confidence, note) ----------------
CPR_NOTE = "CPR/condominium master or subdivision common name - many individual unit owners; treating as one 'owner' overstates concentration"
MAP = {
    # --- state ---
    "STATE OF HAWAII": ("State of Hawaii (agency unspecified)", "state", "high", ""),
    "STATE OF HAWAII (DOT)": ("State of Hawaii - DOT", "state", "high", ""),
    "S OF H DLNR": ("State of Hawaii - DLNR", "state", "high", ""),
    "S OF H DLNR FORESTRY AND WILDLIFE DIV": ("State of Hawaii - DLNR", "state", "high", ""),
    "S OF H DLNR LAND DIV": ("State of Hawaii - DLNR", "state", "high", ""),
    "S OF H DLNR STATE PARKS DIV": ("State of Hawaii - DLNR", "state", "high", ""),
    "SOH,AGRIBUSINESS DEVELOPMENT CORPORATION": ("State of Hawaii - ADC", "state", "high", ""),
    "AGRIBUSINESS DEV CORP": ("State of Hawaii - ADC", "state", "high", ""),
    "AGRIBUSINESS DEVELOPMENT CORP": ("State of Hawaii - ADC", "state", "high", ""),
    "AGRIBUSINESS DEVELOPMENT CORPORATION": ("State of Hawaii - ADC", "state", "high", ""),
    "THE SOH AGRIBUSINESS DEVELOPMENT CORP": ("State of Hawaii - ADC", "state", "high", ""),
    "STATE OF HAWAII AGRIBUSNESS DEV CORP": ("State of Hawaii - ADC", "state", "high", ""),
    "S OF H, AGRIBUSINESS DEV CORP": ("State of Hawaii - ADC", "state", "high", ""),
    "STATE OF HAWAII/DEPARTMENT OF AGRICULTUR": ("State of Hawaii - Dept of Agriculture", "state", "high", ""),
    "STATE OF HAWAII/DEPT OF AGRICULTURE": ("State of Hawaii - Dept of Agriculture", "state", "high", ""),
    "HAWAII HOUSING FINANCE AND DEV. CORP.": ("State of Hawaii - HHFDC", "state", "high", ""),
    "HAWAII HOUSING FIN AND DEV ADMIN": ("State of Hawaii - HHFDC", "state", "high", ""),
    "HAWAII PUBLIC HOUSING AUTHORITY": ("State of Hawaii - HPHA", "state", "high", ""),
    "HAWAII TECHNOLOGY DEVELOPMENT CORP": ("State of Hawaii - HTDC", "state", "high", ""),
    "UNIVERSITY OF HAWAII": ("University of Hawaii", "state", "high", ""),
    "OFFICE OF HAWAIIAN AFFAIRS": ("Office of Hawaiian Affairs", "state", "high", ""),
    "DEPARTMENT OF EDUCATION": ("State of Hawaii - DOE", "state", "high", ""),
    "STATE OF HAWAII/CITY & COUNTY": ("State of Hawaii / C&C Honolulu (joint)", "state", "high", ""),
    "HAWAII COMM DEV AUTHORITY": ("State of Hawaii - HCDA", "state", "high", ""),
    # --- dhhl ---
    "HAWAIIAN HOME LANDS": ("DHHL", "dhhl", "high", ""),
    "DEPT OF HAWAIIAN HOME LANDS": ("DHHL", "dhhl", "high", ""),
    # --- county ---
    "CITY AND COUNTY OF HONOLULU": ("City & County of Honolulu", "county", "high", ""),
    "BOARD OF WATER SUPPLY": ("C&C Honolulu - Board of Water Supply", "county", "high", ""),
    # --- federal ---
    "UNITED STATES OF AMERICA": ("United States of America", "federal", "high", ""),
    "U S NAVAL RESERVATION": ("United States - Navy", "federal", "high", ""),
    "U S FISH AND WILDLIFE SERVICE": ("United States - FWS", "federal", "high", ""),
    "U S FISH & WILDLIFE SERVICE": ("United States - FWS", "federal", "high", ""),
    "UNITED STATES OF AMERICA FISH & WILDLIFE": ("United States - FWS", "federal", "high", ""),
    "U S POSTAL SERVICE": ("United States - USPS", "federal", "high", ""),
    # --- large private estates / trusts ---
    "B P BISHOP TRUST ESTATE": ("Kamehameha Schools (B.P. Bishop Estate)", "private_estate_trust", "high", ""),
    "ESTATE OF BERNICE PAUAHI BISHOP": ("Kamehameha Schools (B.P. Bishop Estate)", "private_estate_trust", "high", ""),
    "LILIUOKALANI TRUST": ("Liliuokalani Trust", "private_estate_trust", "high", ""),
    "OLSON,EDMUND C TRUST NO. 2": ("Edmund C. Olson Trust", "private_estate_trust", "high", ""),
    "ROBINSON KUNIA LAND LLC": ("Robinson family (Robinson Kunia Land LLC)", "private_estate_trust", "high", ""),
    "CASTLE,JAMES C JR TR": ("James C. Castle Jr. Trust (Castle family)", "private_estate_trust", "med", "family trust; distinct from Castle & Cooke Inc and from Harold K.L. Castle Foundation"),
    "CASTLE,H K L TRUST ESTATE ART 8": ("Harold K.L. Castle Trust Estate", "private_estate_trust", "high", ""),
    # --- LDS church family ---
    "PROPERTY RESERVE INC": ("Property Reserve Inc (LDS Church real-estate arm)", "nonprofit", "high", "for-profit arm wholly owned by LDS Church; Laie/Kahuku lands managed by Hawaii Reserves Inc"),
    "CHURCH OF JESUS CHRIST LDS": ("LDS Church", "nonprofit", "high", ""),
    "BYU-HAWAII CAMPUS": ("BYU-Hawaii (LDS Church)", "nonprofit", "high", ""),
    # --- corporate ag ---
    "DOLE FOOD CO INC": ("Dole Food Co Inc", "corporate_ag", "high", "Castle & Cooke Inc / Dole (Murdock) affiliated but kept distinct per project convention"),
    "PIONEER HI-BRED INTERNATIONAL INC": ("Corteva Agriscience (Pioneer Hi-Bred)", "corporate_ag", "high", "seed-corn research"),
    "BAYER RESEARCH&DEVELOPMENT SERVICES LLC": ("Bayer (ex-Monsanto)", "corporate_ag", "high", "seed-corn research"),
    "MONSANTO COMPANY": ("Bayer (ex-Monsanto)", "corporate_ag", "high", ""),
    "KUALOA RANCH INCORPORATED": ("Kualoa Ranch (Morgan family)", "corporate_ag", "high", ""),
    "KUALOA RANCH INC": ("Kualoa Ranch (Morgan family)", "corporate_ag", "high", ""),
    "KUALOA RANCH INCORPORTED": ("Kualoa Ranch (Morgan family)", "corporate_ag", "high", "RPAD spelling variant"),
    "KUALOA LAND CORP": ("Kualoa Ranch (Morgan family)", "corporate_ag", "med", "assumed affiliate by name"),
    "KAUKONAHUA RANCH LLC": ("Kaukonahua Ranch LLC", "corporate_ag", "high", ""),
    "DILLINGHAM RANCH HOLDINGS LLC": ("Dillingham Ranch Holdings LLC", "corporate_ag", "high", "Mokuleia; ranch + equestrian estate development"),
    "GILL EWA LANDS LLC": ("Gill family (Gill Ewa Lands LLC)", "corporate_ag", "high", ""),
    "PALEHUA PARTNERS JOINT VENTURE": ("Palehua Partners JV (Gill-Olson)", "corporate_ag", "med", "Gill-Olson JV purchased Palehua lands from Campbell Estate successors - UNVERIFIED affiliation, name-based"),
    "PP MCCANDLESS RANCH LLC": ("PP McCandless Ranch LLC", "corporate_ag", "med", "ex-McCandless ranch lands; 'PP' prefix suggests Pono Pacific - UNVERIFIED"),
    "G TREE RANCH LLC": ("G Tree Ranch LLC", "corporate_ag", "high", ""),
    "MAHIKO FARMS LLC": ("Mahiko Farms LLC", "corporate_ag", "high", ""),
    "VILLA ROSE LLC": ("Villa Rose LLC (egg farm, Waialua)", "corporate_ag", "med", "sector from name/news - UNVERIFIED"),
    "LAW TIENG'S FARM INC": ("Law Tieng's Farm Inc", "corporate_ag", "high", ""),
    "MOUNTAIN VIEW DAIRY, INC": ("Mountain View Dairy Inc", "corporate_ag", "high", ""),
    "SOUTHERN TURF HAWAII INC": ("Southern Turf Hawaii Inc", "corporate_ag", "high", ""),
    "MANANA FARMS": ("Manana Farms", "corporate_ag", "med", "may be CPR/subdivision name"),
    "KAWAIHAPAI FARMS I": ("Kawaihapai Farms I", "corporate_ag", "med", "may be CPR/subdivision name"),
    "KAENA FARM CORPORATION": ("Kaena Farm Corporation", "corporate_ag", "high", ""),
    "POOHALA FARMS, LLC": ("Poohala Farms LLC", "corporate_ag", "high", ""),
    "NSR FARMS LLC": ("NSR Farms LLC", "corporate_ag", "high", ""),
    "MAILI KAI AGRICULTURAL PARK LLC": ("Maili Kai Agricultural Park LLC", "corporate_ag", "high", ""),
    "ALI'I TURF CO. LLC": ("Ali'i Turf Co LLC", "corporate_ag", "high", ""),
    "HANOHANO ENTERPRISES INC": ("Hanohano Enterprises Inc", "corporate_ag", "high", ""),
    "KA'ALA RANCH": ("Ka'ala Ranch", "corporate_ag", "med", "may be CPR/subdivision name"),
    "KA'ALA RANCH LLC": ("Ka'ala Ranch LLC", "corporate_ag", "high", ""),
    "KA'ALA RANCH 2 LLC": ("Ka'ala Ranch 2 LLC", "corporate_ag", "high", ""),
    "MOUNT KA'ALA RANCH": ("Mount Ka'ala Ranch", "corporate_ag", "med", "may be CPR/subdivision name"),
    "WAHIAWA WATER CO INC": ("Wahiawa Water Co Inc", "corporate_other", "high", "irrigation water utility (Dole-associated historically) - affiliation UNVERIFIED"),
    # --- developers ---
    "CASTLE & COOKE HOMES HAWAII INC": ("Castle & Cooke Hawaii (Murdock)", "developer", "high", ""),
    "CASTLE & COOKE INC": ("Castle & Cooke Hawaii (Murdock)", "developer", "high", ""),
    "CASTLE & COOKE PROPERTIES INC": ("Castle & Cooke Hawaii (Murdock)", "developer", "high", ""),
    "D R HORTON - SCHULER HOMES LLC": ("D.R. Horton Hawaii", "developer", "high", ""),
    "D R HORTON HAWAII LLC": ("D.R. Horton Hawaii", "developer", "high", ""),
    "GENTRY HOMES LTD": ("Gentry Homes Ltd", "developer", "high", ""),
    "ISLAND PALM COMMUNITIES LLC": ("Island Palm Communities LLC (Army housing PPP / Lendlease)", "developer", "high", ""),
    "MAKAIWA HILLS LLC": ("Makaiwa Hills LLC (Kapolei project)", "developer", "med", "ex-Campbell Estate Makaiwa Hills project lands - ultimate parent UNVERIFIED"),
    "SAVIO WAIALUA FARMLAND LLC": ("Savio (Peter Savio) entities", "developer", "med", "ag-lot CPR developer"),
    "SAVIO WAIKELE CANYON CO LLC": ("Savio (Peter Savio) entities", "developer", "med", "ag-lot CPR developer"),
    "KAPOLEI PROPERTIES LLC": ("Kapolei Properties LLC", "developer", "med", "possibly James Campbell Co-related - UNVERIFIED"),
    "CAMPBELL HAWAII INVESTOR LLC": ("Campbell Hawaii Investor LLC", "developer", "med", "possibly James Campbell Co-related - UNVERIFIED"),
    "HAWAII PRINCE HOTEL WAIKIKI LLC": ("Hawaii Prince Hotel Waikiki LLC (golf course)", "developer", "high", ""),
    "YHB MILILANI GC LLC": ("YHB Mililani GC LLC (golf course)", "developer", "high", ""),
    "KO OLINA GC LLC": ("Ko Olina GC LLC (golf course)", "developer", "high", ""),
    "WAIPIO LAND HOLDINGS LLC": ("Waipio Land Holdings LLC", "developer", "low", "sector inferred from name - UNVERIFIED"),
    "MILILANI GROUP INC": ("Mililani Group Inc", "developer", "low", "sector inferred from name - UNVERIFIED"),
    "MILILANI I LAND HOLDINGS LLC": ("Mililani I Land Holdings LLC", "developer", "low", "sector inferred from name - UNVERIFIED"),
    "NORTH SHORE BAY TRS FARM LLC": ("North Shore Bay entities", "developer", "low", "related-name entities near Turtle Bay - affiliation UNVERIFIED"),
    "NORTH SHORE BAY OWNER LLC": ("North Shore Bay entities", "developer", "low", "related-name entities near Turtle Bay - affiliation UNVERIFIED"),
    "TURTLE BAY VILLA LLC": ("Turtle Bay Resort entities", "developer", "med", ""),
    "TURTLE BAY WASTEWATER TREATMENT LLC": ("Turtle Bay Resort entities", "developer", "med", ""),
    "KUILIMA MAUKA LLC": ("Turtle Bay Resort entities", "developer", "med", "Kuilima = Turtle Bay; affiliation name-based"),
    # --- utility / energy ---
    "HAWAIIAN ELECTRIC CO INC": ("Hawaiian Electric Co (HECO)", "utility", "high", ""),
    "HAWAIIAN ELECTRIC COMPANY INC": ("Hawaiian Electric Co (HECO)", "utility", "high", ""),
    "KAHUKU WIND POWER LLC": ("Kahuku Wind Power LLC (IPP wind project)", "utility", "high", "independent power producer project company"),
    "EE WAIANAE SOLAR LLC": ("EE Waianae Solar LLC (IPP solar project)", "utility", "med", "'EE' consistent with Eurus Energy - UNVERIFIED"),
    # --- nonprofit ---
    "HI'IPAKA LLC": ("Hi'ipaka LLC (OHA subsidiary - Waimea Valley)", "nonprofit", "high", ""),
    "KUNIA LOA RIDGE FARMLANDS": ("Kunia Loa Ridge Farmlands (farm-lot association)", "nonprofit", "med", "nonprofit farm-lot association; many member farmers"),
    "WAIANAE COMMUNITY RE-DEV CORP": ("Waianae Community Redevelopment Corp (MA'O Farms-affiliated)", "nonprofit", "med", "affiliation from public reporting - UNVERIFIED"),
    "GIRL SCOUTS OF HAWAI'I": ("Girl Scouts of Hawaii", "nonprofit", "high", ""),
    "BOY SCOUTS OF AMERICA, ALOHA COUNCIL": ("Boy Scouts of America Aloha Council", "nonprofit", "high", ""),
    "QUEEN'S MEDICAL CENTER THE": ("Queen's Medical Center", "nonprofit", "high", ""),
    "THE QUEEN'S MEDICAL CENTER": ("Queen's Medical Center", "nonprofit", "high", ""),
    "RELIGIOUS CORPORATION HONBUSHIN": ("Honbushin (religious corporation)", "nonprofit", "high", ""),
    "OUR LADY OF KEEAU": ("Our Lady of Keeau (Catholic)", "nonprofit", "high", ""),
    "BENEDICTINE MONASTERY OF HI": ("Benedictine Monastery of Hawaii", "nonprofit", "high", ""),
    "ASIA PACIFIC EDUCATIONAL FOUNDATION": ("Asia Pacific Educational Foundation", "nonprofit", "high", ""),
    "LOC 675 OF UNITED ASSOC": ("UA Local 675 (plumbers union)", "nonprofit", "high", ""),
    "LAUNANI VALLEY COMMUNITY ASSN": ("Launani Valley Community Assn", "nonprofit", "high", ""),
    "WAI KALOI AT MAKAKILO COMMUNITY ASSOC": ("Wai Kaloi at Makakilo Community Assoc", "nonprofit", "high", ""),
    "KAHIWELO AT MAKAKILO COMMUNITY ASSN": ("Kahiwelo at Makakilo Community Assn", "nonprofit", "high", ""),
    "OHULEHULE FOREST CONSERVANCY LLC": ("Ohulehule Forest Conservancy LLC", "nonprofit", "med", "conservation entity - status UNVERIFIED"),
    # --- corporate other ---
    "GRACE PACIFIC LLC": ("Grace Pacific LLC (construction materials/quarry)", "corporate_other", "high", ""),
    "INTELSAT US LLC": ("Intelsat US LLC (satellite ground station)", "corporate_other", "high", ""),
    "IES DOWNSTREAM LLC": ("IES Downstream LLC (Island Energy Services)", "corporate_other", "high", ""),
    "PVT LAND COMPANY LTD": ("PVT Land Co (Nanakuli landfill)", "corporate_other", "high", ""),
    "PVT DEVELOPMENT INC": ("PVT Land Co (Nanakuli landfill)", "corporate_other", "med", "assumed affiliate by name"),
    "LEEWARD LAND COMPANY LTD": ("Leeward Land Company Ltd", "corporate_other", "low", ""),
    "HRT, LTD": ("HRT Ltd (Heeia/Kaneohe lands)", "corporate_other", "low", "ultimate ownership UNVERIFIED; parcels in TMK zone 4-2 Heeia"),
    "HRT REALTY LLC": ("HRT Ltd (Heeia/Kaneohe lands)", "corporate_other", "low", "assumed affiliate of HRT Ltd by name - UNVERIFIED"),
    "BISHOP TRUST CO LTD TRS": ("Bishop Trust Co Ltd as trustee", "corporate_other", "med", "corporate trustee; NOT Kamehameha Schools/Bishop Estate"),
    # --- CPR masters / multi-owner aggregates ---
    "LAUKIHA'A MAUKA CONDOMINIUM": ("Laukiha'a ag CPR (multiple unit owners; developed by Pomaika'i Partners LLC)", "unknown", "med", CPR_NOTE),
    "LAUKIHA'A FARMS CONDOMINIUM": ("Laukiha'a ag CPR (multiple unit owners; developed by Pomaika'i Partners LLC)", "unknown", "med", CPR_NOTE),
    "KUNIA SECTION 6 CONDOMINIUM": ("Kunia Section 6 ag CPR (multiple unit owners)", "unknown", "med", CPR_NOTE),
    "KUNIA HERITAGE FARMS CONDOMINIUM": ("Kunia Heritage Farms ag CPR (multiple unit owners)", "unknown", "med", CPR_NOTE),
    "OHANA FARM PARCELS CONDOMINIUM": ("Ohana Farm Parcels ag CPR (multiple unit owners)", "unknown", "med", CPR_NOTE),
    "MARCONI POINT CONDOMINIUM": ("Marconi Point CPR (multiple unit owners)", "unknown", "med", CPR_NOTE),
    "WAIKELE STORAGE PARK": ("Waikele Storage Park CPR (multiple unit owners)", "unknown", "med", CPR_NOTE),
    "KALUANUI ACRES": ("Kaluanui Acres (subdivision aggregate)", "unknown", "med", CPR_NOTE),
    "VARIOUS OWNERS": ("Various owners (RPAD aggregate)", "unknown", "low", "RPAD placeholder"),
    "KAALA AINALANI ESTATES": ("Kaala Ainalani Estates (subdivision aggregate)", "unknown", "med", CPR_NOTE),
    "KAALA VIEW FARM LOTS #2": ("Kaala View Farm Lots #2 (subdivision aggregate)", "unknown", "med", CPR_NOTE),
    "POAMOHO CAMP": ("Poamoho Camp (aggregate)", "unknown", "med", CPR_NOTE),
    "WAIALUA MILL CAMP": ("Waialua Mill Camp (aggregate)", "unknown", "med", CPR_NOTE),
    "PUNALUU OCEANVIEW": ("Punaluu Oceanview (aggregate)", "unknown", "med", CPR_NOTE),
    "PAUMALU MAUKA RANCHES": ("Paumalu Mauka Ranches (aggregate)", "unknown", "med", CPR_NOTE),
    "KIPAPA ACRES": ("Kipapa Acres (aggregate)", "unknown", "med", CPR_NOTE),
    "RANCH 1": ("Ranch 1 (aggregate)", "unknown", "low", CPR_NOTE),
    "MANAGER'S RANCH": ("Manager's Ranch (aggregate)", "unknown", "low", CPR_NOTE),
    "KAUKONAHUA": ("Kaukonahua (aggregate)", "unknown", "low", CPR_NOTE + "; possibly Kaukonahua Ranch-related"),
    "KMA CENTER": ("KMA Center (aggregate)", "unknown", "low", ""),
    "KALOKO PLANTATION": ("Kaloko Plantation (aggregate)", "unknown", "med", CPR_NOTE),
    "92-1700 KUNIA ROAD": ("92-1700 Kunia Road (address placeholder)", "unknown", "low", "RPAD shows situs address as owner name"),
}

IND_RE = re.compile(r"^[A-Z'\-\. ]+,[A-Z]")
CORP_RE = re.compile(r"\b(LLC|INC|LTD|CORP|CORPORATION|COMPANY|CO|LP|LLP|PARTNERSHIP|PARTNERS|VENTURE|HOLDINGS|ENTERPRISES|INVESTMENTS?|PROPERTIES|GROUP)\b")
AG_RE = re.compile(r"\b(FARM|FARMS|RANCH|RANCHES|NURSERY|ORCHARD|ORCHARDS|DAIRY|AGRICULT\w*|AG|TARO|FLOWERS?|PLANTATION|GARDENS?|AQUACULTURE|LIVESTOCK|TURF)\b")
DEV_RE = re.compile(r"\b(DEVELOPMENT|DEVELOPERS?|HOMES|REALTY|RESORT|GOLF|BUILDERS?|CONSTRUCTION)\b")
NP_RE = re.compile(r"\b(CHURCH|TEMPLE|MISSION|MINISTR\w*|CONGREGATION|ASSN|ASSOC\w*|FOUNDATION|FDN|SOCIETY|CLUB|SCOUTS|HUI|CHARIT\w*|MONASTERY|SHRINE|CATHOLIC|LUTHERAN|BAPTIST|BUDDHIST|HONGWANJI|YMCA|YWCA|LEGACY LAND|CONSERVANCY|TRUST FOR PUBLIC|UNIVERSITY|COLLEGE|SALVATION ARMY|JEHOVAH|CHRIST|ADVENTIST|HONBUSHIN|RESEARCH CENTER)\b")
FAMTR_RE = re.compile(r"\b(FAMILY (TR|TRUST|LTD PTP|LIMITED PTP|PARTNERSHIP|LP|JOINT)|JOINT TR(UST)?|REV(OCABLE)? (LIVING )?TR(UST)?|LIVING TR(UST)?)\b")

def heuristic(raw: str):
    r = raw.upper().strip()
    if "STATE OF HAWAII" in r or r.startswith("S OF H") or r.startswith("SOH"):
        return ("State of Hawaii (agency unspecified)", "state", "med", "heuristic")
    if "HAWAIIAN HOME" in r:
        return ("DHHL", "dhhl", "med", "heuristic")
    if "CITY AND COUNTY" in r or "CITY & COUNTY" in r:
        return ("City & County of Honolulu", "county", "med", "heuristic")
    if r.startswith("UNITED STATES") or r.startswith("U S ") or r.startswith("USA "):
        return ("United States of America", "federal", "med", "heuristic")
    if NP_RE.search(r):
        return (raw.title(), "nonprofit", "med", "heuristic type")
    if FAMTR_RE.search(r):
        return (raw.title(), "individual", "med", "family trust/partnership name pattern")
    if IND_RE.match(r) and not CORP_RE.search(r):
        return (raw.title(), "individual", "high", "SURNAME,FIRST pattern (incl. family trusts)")
    if CORP_RE.search(r):
        if AG_RE.search(r):
            return (raw.title(), "corporate_ag", "med", "heuristic type from name")
        if DEV_RE.search(r):
            return (raw.title(), "developer", "med", "heuristic type from name")
        return (raw.title(), "corporate_other", "med", "corporate entity, sector not identified")
    if IND_RE.match(r):
        return (raw.title(), "individual", "med", "heuristic")
    return (raw.title(), "unknown", "low", "unclassified name pattern")

rows = []
for _, p in m.iterrows():
    raw = p.owner_raw
    if pd.isna(raw):
        continue
    if raw in MAP:
        res, typ, conf, note = MAP[raw]
    else:
        res, typ, conf, note = heuristic(raw)
    rows.append(dict(tmk=p.tmk, owner_raw=raw, owner_resolved=res, owner_type=typ,
                     source="bulk", source_url=OWNALL_URL, confidence=conf, note=note))

# govlayer addition: DHHL parcel absent from RPAD
rows.append(dict(tmk="187010030", owner_raw="HAWAIIAN HOME LANDS", owner_resolved="DHHL",
                 owner_type="dhhl", source="govlayer", source_url=GOV_URL, confidence="high",
                 note="not in RPAD OWNALL; attributed via state Government Lands - Detailed layer"))

out = pd.DataFrame(rows)
out.to_csv(f"{PROJ}/data/oahu_ag_owners.csv", index=False)
print("wrote", len(out), "rows to data/oahu_ag_owners.csv")

# coverage
oa = m
cov = out.merge(oa[["tmk", "parcel_acres"]], on="tmk")
print(f"parcels covered: {len(out)}/{len(oa)} = {len(out)/len(oa):.2%}")
print(f"acreage covered: {cov.parcel_acres.sum():.0f}/{oa.parcel_acres.sum():.0f} = {cov.parcel_acres.sum()/oa.parcel_acres.sum():.2%}")
print("\ntype counts:", out.owner_type.value_counts().to_dict())
print("confidence:", out.confidence.value_counts().to_dict())
