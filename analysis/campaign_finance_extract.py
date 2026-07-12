#!/usr/bin/env python3
"""
Extract and classify campaign contributions to legislators/council members who
controlled Hawaii solar/wind siting legislation.

Sources:
 A. data/raw/csc/wayback_contrib_dump_20250331.csv
    = CKAN datastore dump of CSC resource 443bd998-1ef3-47da-9170-c2c376b2e41c
      ("Campaign Contributions Received By Hawaii State and County Candidates"),
      captured by the Internet Archive 2025-03-31, when it still covered
      Nov 8 2006 - late 2024. 218,392 rows. Official CSC data; the live portals
      (hicscdata.hawaii.gov jexd-xbcg; opendata.hawaii.gov) were truncated to
      2015+ in 2025.
 B. Live SODA API https://hicscdata.hawaii.gov/resource/jexd-xbcg.json for rows
    dated after the Wayback capture (top-up for council members), cached under
    data/raw/csc/live_<regno>.json.

Outputs:
  data/campaign_contributions_siting.csv  (classified donor rows only)
  data/campaign_contrib_summary.csv       (per candidate x election period:
                                            totals overall + by donor class)
"""
import csv, json, re, sys, time, os, urllib.request, urllib.parse
from collections import defaultdict

ROOT = "/Users/michaelroberts/Research/solar-wind-landuse"
DUMP = f"{ROOT}/data/raw/csc/wayback_contrib_dump_20250331.csv"
RAWDIR = f"{ROOT}/data/raw/csc"

# ---------------------------------------------------------------- targets ---
# group: sb631 -> window 2006-11-01 .. 2014-12-31 ; council -> 2012-01-01 .. 2024-12-31
TARGETS = {
    "CC10279": ("Gabbard, Mike",       "sb631"),   # Senate ENE chair 2011
    "CC10159": ("Nishihara, Clarence", "sb631"),   # Senate AGL chair 2011
    "CC10171": ("Dela Cruz, Donovan",  "sb631"),   # Senate WLH chair 2011
    "CC10802": ("Solomon, Malama",     "sb631"),   # SB631 introducer
    "CC10147": ("Ige, David",          "sb631"),   # introducer (Sen; Gov 2014)
    "CC10801": ("Kahele, Gilbert",     "sb631"),   # introducer
    "CC10494": ("Kidani, Michelle",    "sb631"),   # introducer
    "CC10254": ("Kim, Donna",          "sb631"),   # introducer (Donna Mercado Kim)
    "CC10287": ("Slom, Sam",           "sb631"),   # introducer
    "CC10359": ("Coffman, George",     "sb631"),   # House EEP chair (Denny Coffman;
                                                   # CSC lists legal name George)
    "CC10168": ("Chang, Jerry",        "sb631"),   # House WLO chair
    "CC10217": ("Tsuji, Clifton",      "sb631"),   # House AGR chair
    "CC11195": ("Tsuneyoshi, Heidi",   "council"),
    "CC11549": ("Kiaaina, Esther",     "council"), # Honolulu Council reg
    "CC11363": ("Kiaaina, Esther",     "council"), # earlier OHA reg (kept, office col disambiguates)
    "CC11024": ("Waters, Tommy",       "council"),
    "CC10995": ("Tupola, Andria",      "council"), # House/Gov/Council all under one reg
}
WINDOWS = {"sb631": ("2006-11-01", "2014-12-31"),
           "council": ("2012-01-01", "2024-12-31")}

# ------------------------------------------------------------ classifiers ---
def rx(*pats): return re.compile("|".join(pats), re.I)

HEI_ORG = rx(r"hawaiian\s+elec", r"hawaii\s+electric\s+light", r"maui\s+electric",
             r"\bheco\b", r"\bhelco\b", r"\bmeco\b",
             r"\bHEI\b(?:\s+(?:inc|industries))?")
ASB_ORG = rx(r"american\s+savings\s+bank", r"\bASB\b")
# HEI directors & named executive officers, 2006-2015 proxies (data/raw/edgar/):
HEI_PEOPLE = rx(r"^lau,\s*constance", r"^watanabe,\s*jeff", r"^rosenblum,\s*richard",
                r"^ajello,\s*james", r"^richardson,\s*chester", r"^alm,\s*rob",
                r"^may,\s*t\.?\s*michael", r"^oshima,\s*alan", r"^sekimura,\s*tayne",
                r"^seu,\s*scott", r"^kimura,\s*shelee", r"^fargo,\s*thomas",
                r"^taniguchi,\s*barry", r"^taketa,\s*kelvin", r"^plotts,\s*diane",
                r"^carroll,\s*don", r"^fowler,\s*peggy", r"^myers,\s*(a\.?\s*)?maurice")

LAND_ORG = rx(r"kamehameha\s+schools", r"bishop\s+estate", r"\bKSBE\b",
              r"castle\s*(&|and)\s*cooke", r"alexander\s*(&|and)\s*baldwin",
              r"\bA\s*&\s*B\b", r"a&b\s+properties",
              r"d\.?\s*r\.?\s*horton", r"horton[- ]?schuler", r"schuler\s+(homes|division)",
              r"james\s+campbell", r"campbell\s+estate",
              r"grove\s+farm", r"parker\s+ranch", r"dole\s+food",
              r"land\s+use\s+research\s+foundation", r"\bLURF\b",
              r"ulupono", r"kobayashi\s+group", r"stanford\s+carr",
              r"gay\s*(&|and)\s*robinson", r"robinson\s+family\s+partners",
              r"hoakalei", r"haseko", r"gentry\s+(homes|companies|investment)",
              r"kukui[ʻ']?ula", r"maui\s+land\s*(&|and)\s*pine",
              r"s[at]an?d?ford\s+carr", r"hunt\s+companies")
LAND_PEOPLE = rx(r"^carr,\s*stanford", r"^hunt,\s*woody")

AG_ORG = rx(r"monsanto", r"syngenta", r"pioneer\s+hi[- ]?bred", r"du\s*pont",
            r"dow\s+agro", r"dow\s+chemical", r"\bBASF\b", r"farm\s+bureau",
            r"hawaii\s+crop\s+improvement", r"hawaiian\s+commercial\s*(&|and)\s*sugar",
            r"\bHC&S\b", r"hawaii\s+cattlemen", r"hawaii\s+agriculture\s+research",
            r"\bHARC\b", r"mycogen", r"BASF\s+plant\s+science")

RE_ORG = rx(r"sopogy", r"first\s+wind", r"sun\s*edison", r"\bAES\b(?:\s|$)",
            r"clearway", r"174\s+power", r"longroad", r"na\s+pua\s+makani",
            r"champlin", r"kahuku\s+wind", r"eurus\s+energy", r"sunpower",
            r"sunrun", r"revolusun", r"hawaii\s+pacific\s+solar",
            r"hawaii\s+solar\s+energy\s+association", r"\bHSEA\b",
            r"pattern\s+energy", r"terraform", r"innergex",
            r"onyx\s+renew", r"plus\s+power", r"scatec", r"bright\s*night",
            r"solar", r"photovolt", r"wind\s+(energy|power|farm)")
RE_NAMED = rx(r"sopogy", r"first\s+wind", r"sun\s*edison", r"clearway", r"174\s+power",
              r"longroad", r"na\s+pua\s+makani", r"champlin", r"eurus", r"sunpower",
              r"sunrun", r"revolusun", r"pattern\s+energy", r"innergex",
              r"plus\s+power", r"\bAES\b")
# Sempra Generation developed Auwahi Wind (Maui, 2012): classified solar_wind, medium.
SEMPRA = rx(r"sempra")
# NextEra: mainland utility; interisland-cable proponent, then would-be HEI acquirer
# (2014 merger bid). Own class so it is not conflated with solar/wind developers.
UTIL_OTHER = rx(r"nextera")

UNION_CONSTR = rx(r"laborers", r"carpenters", r"\bIBEW\b", r"electrical\s+workers",
                  r"operating\s+eng", r"plumbers", r"pipefitters",
                  r"painters", r"masons", r"iron\s*workers", r"sheet\s*metal",
                  r"local\s+union\s+293", r"tapers\s+local", r"glaziers",
                  r"elevator\s+constructors", r"bricklayers", r"cement\s+(masons|finishers)",
                  r"building\s*(&|and)\s*construction\s+trades", r"\bHRCC\b",
                  r"regional\s+council\s+of\s+carpenters", r"drywall", r"roofers",
                  r"boilermakers", r"insulators", r"plasterers")

def classify(contributor, employer, ctype):
    """Return (donor_class, confidence) or (None, None)."""
    c = (contributor or "").strip()
    e = (employer or "").strip()
    is_cmte = ctype in ("Noncandidate Committee", "Political Party", "Other Entity",
                        "Business Entity", "Organization")
    # committees / entity names first (high confidence: name IS the org)
    if HEI_ORG.search(c):  return ("hei_utility", "high")
    if ASB_ORG.search(c) and "american savings" in c.lower(): return ("hei_asb", "high")
    if UNION_CONSTR.search(c): return ("union_construction", "high")
    if LAND_ORG.search(c): return ("landholder_dev", "high")
    if AG_ORG.search(c):   return ("ag_seed", "high")
    if RE_NAMED.search(c): return ("solar_wind", "high")
    if UTIL_OTHER.search(c) or UTIL_OTHER.search(e): return ("utility_other", "high")
    if SEMPRA.search(c) or SEMPRA.search(e): return ("solar_wind", "medium")
    if RE_ORG.search(c) and is_cmte: return ("solar_wind", "medium")
    # employer field (individuals)
    if HEI_ORG.search(e):  return ("hei_utility", "high")
    if ASB_ORG.search(e):  return ("hei_asb", "medium")   # HEI subsidiary, not utility ops
    if LAND_ORG.search(e): return ("landholder_dev", "high")
    if AG_ORG.search(e):   return ("ag_seed", "high")
    if RE_NAMED.search(e): return ("solar_wind", "high")
    if RE_ORG.search(e):   return ("solar_wind", "medium") # generic 'solar' etc.
    if UNION_CONSTR.search(e): return ("union_construction", "medium")
    if LAND_PEOPLE.search(c):  return ("landholder_dev", "medium")
    # HEI directors/execs by personal name (employer often blank/other firm)
    if HEI_PEOPLE.search(c):
        conf = "medium" if not e or not HEI_ORG.search(e) else "high"
        return ("hei_person", conf)
    return (None, None)

# ------------------------------------------------------------------ load ----
def norm_date(d):  # '2014-09-17T08:23:02' -> '2014-09-17'
    return (d or "")[:10]

rows = []
seen = set()
with open(DUMP) as f:
    for r in csv.DictReader(f):
        reg = r["Reg No"]
        if reg not in TARGETS: continue
        rec = dict(reg=reg, candidate=TARGETS[reg][0], group=TARGETS[reg][1],
                   office=r["Office"].strip(), period=r["Election Period"].strip(),
                   donor=(r["Contributor Name"] or "").strip(),
                   ctype=(r["Contributor Type"] or "").strip(),
                   employer=(r["Employer"] or "").strip(),
                   occupation=(r["Occupation"] or "").strip(),
                   amount=float(r["Amount"] or 0), date=norm_date(r["Date"]),
                   source="CSC via IA wayback 20250331 (CKAN 443bd998)")
        key = (reg, rec["donor"].lower(), rec["date"], rec["amount"])
        seen.add(key); rows.append(rec)

# live API top-up (rows after Wayback capture, council group mainly)
API = "https://hicscdata.hawaii.gov/resource/jexd-xbcg.json"
for reg, (name, grp) in sorted(TARGETS.items()):
    cache = f"{RAWDIR}/live_{reg}.json"
    if not os.path.exists(cache):
        q = urllib.parse.urlencode({"reg_no": reg, "$limit": 50000})
        with urllib.request.urlopen(f"{API}?{q}", timeout=60) as u:
            data = json.load(u)
        json.dump(data, open(cache, "w"))
        time.sleep(1.0)
    else:
        data = json.load(open(cache))
    for r in data:
        rec = dict(reg=reg, candidate=name, group=grp,
                   office=(r.get("office") or "").strip(),
                   period=(r.get("election_period") or "").strip(),
                   donor=(r.get("contributor_name") or "").strip(),
                   ctype=(r.get("contributor_type") or "").strip(),
                   employer=(r.get("employer") or "").strip(),
                   occupation=(r.get("occupation") or "").strip(),
                   amount=float(r.get("amount") or 0), date=norm_date(r.get("date")),
                   source="CSC live SODA jexd-xbcg (hicscdata.hawaii.gov)")
        key = (reg, rec["donor"].lower(), rec["date"], rec["amount"])
        if key in seen: continue
        seen.add(key); rows.append(rec)

# window filter
def in_window(rec):
    lo, hi = WINDOWS[rec["group"]]
    return lo <= rec["date"] <= hi
rows = [r for r in rows if in_window(r)]

# classify
for r in rows:
    dc, conf = classify(r["donor"], r["employer"], r["ctype"])
    r["donor_class"], r["confidence"] = dc, conf

# ------------------------------------------------------------- outputs ------
out1 = f"{ROOT}/data/campaign_contributions_siting.csv"
with open(out1, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["candidate","office","election_period","donor","donor_type","employer",
                "occupation","amount","date","donor_class","confidence","group","source"])
    for r in sorted(rows, key=lambda x: (x["candidate"], x["date"])):
        if r["donor_class"]:
            w.writerow([r["candidate"], r["office"], r["period"], r["donor"], r["ctype"],
                        r["employer"], r["occupation"], f'{r["amount"]:.2f}', r["date"],
                        r["donor_class"], r["confidence"], r["group"], r["source"]])

# summary: per candidate x election period, total + by class
agg = defaultdict(lambda: defaultdict(float))
cnt = defaultdict(int)
classes = ["hei_utility","hei_person","hei_asb","utility_other","landholder_dev",
           "ag_seed","solar_wind","union_construction"]
for r in rows:
    k = (r["candidate"], r["office"], r["period"])
    agg[k]["total"] += r["amount"]; cnt[k] += 1
    if r["donor_class"]:
        agg[k][r["donor_class"]] += r["amount"]
out2 = f"{ROOT}/data/campaign_contrib_summary.csv"
with open(out2, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["candidate","office","election_period","n_contributions","total_raised"]
               + [f"amt_{c}" for c in classes])
    for k in sorted(agg):
        a = agg[k]
        w.writerow([k[0], k[1], k[2], cnt[k], f'{a["total"]:.2f}']
                   + [f'{a[c]:.2f}' for c in classes])

n_class = sum(1 for r in rows if r["donor_class"])
print(f"target rows in window: {len(rows)}; classified: {n_class}")
from collections import Counter
print(Counter((r['donor_class']) for r in rows if r['donor_class']))
print("wrote", out1); print("wrote", out2)
