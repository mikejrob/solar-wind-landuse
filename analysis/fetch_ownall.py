"""Fetch OWNALL (Honolulu RPAD owner table) rows for Oahu ag-district TMKs."""
import json, time, urllib.parse, urllib.request, sys
import pandas as pd

BASE = "https://services.arcgis.com/tNJpAOha4mODLkXz/arcgis/rest/services/CadastralTables/FeatureServer/5/query"
OUT = "/private/tmp/claude-503/-Users-michaelroberts-Research-solar-wind-landuse/d73405a1-d30d-4ac4-8a47-d64b30b982a9/scratchpad/ownall_rows.csv"

df = pd.read_csv("/Users/michaelroberts/Research/solar-wind-landuse/data/cap_scenarios_by_parcel.csv", dtype={"tmk": str})
oa = df[df.island == "Oahu"].copy()
tmks9 = sorted(oa.tmk.unique())
tmks8 = sorted({t[1:] for t in tmks9 if t.startswith("1") and len(t) == 9})
print(f"{len(tmks9)} parcels, {len(tmks8)} 8-digit tmks", flush=True)

rows = []
B = 100
for i in range(0, len(tmks8), B):
    batch = tmks8[i:i+B]
    where = "tmk IN ({})".format(",".join(f"'{t}'" for t in batch))
    params = {
        "where": where,
        "outFields": "tmk,parid,suffix,taxyr,own1,own2,pctowned,ownseq,owntype1,owntype2",
        "returnGeometry": "false",
        "f": "json",
        "resultRecordCount": "2000",
    }
    url = BASE + "?" + urllib.parse.urlencode(params)
    for attempt in range(4):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                d = json.load(r)
            break
        except Exception as e:
            print(f"batch {i}: retry {attempt} ({e})", flush=True)
            time.sleep(5 * (attempt + 1))
    else:
        print(f"batch {i}: FAILED", flush=True)
        continue
    feats = d.get("features", [])
    if d.get("exceededTransferLimit"):
        print(f"batch {i}: EXCEEDED transfer limit ({len(feats)})", flush=True)
    rows.extend(f["attributes"] for f in feats)
    if (i // B) % 10 == 0:
        print(f"batch {i}: total rows {len(rows)}", flush=True)
    time.sleep(0.6)

out = pd.DataFrame(rows)
out.to_csv(OUT, index=False)
print("saved", len(out), "rows;", out.tmk.nunique(), "unique tmks")
