#!/bin/bash
# Chunked commit+push: get ~900MB of sources/GIS into GitHub over HTTPS without
# the HTTP 408 that killed the single 485MB pack. Each chunk <=75MB.
set -e
cd ~/Research/solar-wind-landuse
git config http.postBuffer 524288000

pushret () {
  if ! git push -q origin main 2>/dev/null; then
    echo "  push failed; fetch+rebase+retry"
    git fetch -q origin && git rebase -q origin/main && git push -q origin main
  fi
}
cp () { git commit -q -m "$1"; echo ">>> $1"; pushret; echo "    ok"; }

git add .gitignore notes data/*.csv sources chunked_push.sh \
        data/raw/neighbor-interconnection data/raw/rpad data/raw/lurf \
        data/raw/ord25-44.pdf data/raw/bill4_2022_cd1.pdf 2>/dev/null || true
cp "Archive in-repo (01): analysis notes, CSVs, curated sources/"

git add data/raw/csc;                     cp "Archive (02): CSC campaign-finance dump"
git add data/raw/edgar;                   cp "Archive (03): SEC EDGAR proxies"
git add data/raw/capitol;                 cp "Archive (04): capitol bill/testimony caches"
git add data/raw/wind-setbacks data/raw/military-golf 2>/dev/null || true
cp "Archive (05): wind-setback records"
git add data/raw/dockets/sp15-405;        cp "Archive (06): LUC docket SP15-405"
git add data/raw/dockets/sp21-412 data/raw/dockets/sp21-412-DO-2021.pdf
cp "Archive (07): LUC docket SP21-412"
git add data/raw/dockets/sp21-411;        cp "Archive (08): LUC docket SP21-411"
git add data/raw/dockets;                 cp "Archive (09): remaining LUC dockets + court opinions"
git add data/gis/dem/USGS_13_n22w158.tif; cp "Archive (10): DEM tile n22w158 (regenerable)"
git add data/gis/dem;                     cp "Archive (11): DEM tile n22w159 (regenerable)"
git add data/gis/parcels_hawaii.parquet data/gis/parcels_oahu.parquet
cp "Archive (12): Oahu+Hawaii parcel layers (regenerable)"
git add data/gis/parcels_maui.parquet data/gis/parcels_kauai.parquet data/gis/slud.parquet
cp "Archive (13): Maui+Kauai parcels, SLUD (regenerable)"
git add data/gis/lsb.parquet;             cp "Archive (14): LSB soils layer (regenerable)"
git add -A;                               cp "Archive (15): remaining GIS layers (regenerable)"

echo "DONE. .git=$(du -sh .git|cut -f1); ahead=$(git rev-list --count origin/main..HEAD)"
