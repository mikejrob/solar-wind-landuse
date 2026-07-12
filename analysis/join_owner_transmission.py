"""Reproduce data/oahu_owner_class_transmission.csv from committed inputs.

Joins the parcel-level transmission-distance table (analysis/transmission_screen.py)
with the entity-resolved ownership table (analysis/resolve_owners.py) and adds
soil-group aggregates and 46kV distance bands. This is the table behind the
paper's Figure 1 and Table 3.
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
tx = pd.read_csv(ROOT / "data/oahu_land_transmission.csv", dtype={"tmk": str})
ow = pd.read_csv(ROOT / "data/oahu_ag_owners.csv", dtype={"tmk": str})

m = tx.merge(ow[["tmk", "owner_resolved", "owner_type", "confidence"]], on="tmk", how="left")
m["owner_resolved"] = m["owner_resolved"].fillna("UNATTRIBUTED")
m["owner_type"] = m["owner_type"].fillna("unknown")
m["band46"] = pd.cut(m["dist_46kv_km"], [-0.01, 1, 3, 5, 1e9],
                     labels=["0-1km", "1-3km", "3-5km", ">5km"])
m["bc_acres"] = m["b_acres"] + m["c_acres"]
m["de_acres"] = m["d_acres"] + m["e_acres"]

out = ROOT / "data/oahu_owner_class_transmission.csv"
m.to_csv(out, index=False)
print(f"wrote {out} ({len(m)} rows)")
