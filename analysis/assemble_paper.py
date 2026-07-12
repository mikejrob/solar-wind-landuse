"""Substitute base64 figure data-URIs into the paper HTML template."""
import base64
from pathlib import Path

ROOT = Path("/Users/michaelroberts/Research/solar-wind-landuse")
SRC = ROOT / "paper" / "land-restrictions-paper.html"
OUT = ROOT / "paper" / "land-restrictions-paper-final.html"

FIGS = {
    "__F1__": ROOT / "analysis/figs/paper/f1_cap_scenarios.png",
    "__F2__": ROOT / "analysis/figs/paper/f2_distance_bands.png",
    "__F3__": ROOT / "analysis/figs/paper/f3_ownership.png",
    "__F4__": ROOT / "analysis/figs/oahu_transmission_screen.png",
    "__F5__": ROOT / "analysis/figs/oahu_slope_bands.png",
    "__F6__": ROOT / "analysis/figs/paper/f_corridors.png",
    "__F7__": ROOT / "analysis/figs/paper/f_expansion_curve.png",
    "__F8__": ROOT / "analysis/figs/paper/f_expansion_map.png",
}

html = SRC.read_text()
for key, path in FIGS.items():
    if key in html:
        b64 = base64.b64encode(path.read_bytes()).decode()
        html = html.replace(key, f"data:image/png;base64,{b64}")
        print(f"embedded {path.name} ({path.stat().st_size//1024} KB)")
    else:
        print(f"WARNING: {key} not found in template")
OUT.write_text(html)
print("wrote", OUT, f"({OUT.stat().st_size//1024} KB)")
