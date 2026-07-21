# Data deposit (Zenodo)

The large data files supporting this repository live in a Zenodo deposit, not
in Git. Git holds the code, notes, tidy CSVs, and the paper. The deposit holds
the GIS layers and primary-source document caches that are too large to push
and, for the GIS layers, regenerable from public sources.

DOI: _pending upload — add here after the Zenodo deposit is published._

## Archives

Built by the maintainer with `tar czf`; checksums below. Extract each into a
repository clone as noted.

| Archive | Size | Extract into | Contents |
|---|---:|---|---|
| `oahu-gis-layers.tar.gz` | 192 MB | `data/` (creates `data/gis/`) | LSB soil polygons, State Land Use Districts, county parcels (Oʻahu/Hawaiʻi/Maui/Kauaʻi), DoD land layers, USGS 3DEP DEM tiles, HIFLD + OSM transmission lines, and derived summary parquet/CSV. EPSG:26904. |
| `oahu-procurement-sources.tar.gz` | 80 MB | `data/raw/` (creates `data/raw/procurement/`) | HECO RFP documents, PA Consulting Act 201 interconnection studies, LBNL "Queued Up" interconnection reports, PUC/procurement materials behind `notes/heco-solar-procurement.md` and `notes/procurement-comparison-kiuc-ercot.md`. |

Checksums (MD5):

```
a3df8ab8be367cdb420d51d5f8df5491  oahu-gis-layers.tar.gz
7527b7b60ebd447aaa0db5beaa6d9667  oahu-procurement-sources.tar.gz
```

File-by-file contents: `deposit/MANIFEST.txt` (local, not committed).

## Not in the deposit

- `data/gis/pages_*` (~240 MB): raw ArcGIS REST pagination dumps. Regenerable by
  the download scripts; excluded to keep the deposit lean.
- `cache/`: scratch downloads.
- Everything already in Git (`data/*.csv`, `data/raw/{capitol,csc,dockets,edgar,
  lurf,rpad,military-golf,neighbor-interconnection}`, notes, code, paper).

## Use

```sh
git clone https://github.com/mikejrob/solar-wind-landuse
cd solar-wind-landuse
# download the two archives from the Zenodo DOI, then:
tar xzf oahu-gis-layers.tar.gz -C data/
tar xzf oahu-procurement-sources.tar.gz -C data/raw/
```

The analysis scripts in `analysis/` then run against the local cache. See
`docs/METHODS.md` for each pipeline and `docs/AUDIT_REPRO.md` for what
reproduces from committed inputs.

## Upload steps (maintainer)

1. Go to https://zenodo.org, sign in, "New upload."
2. Upload `deposit/oahu-gis-layers.tar.gz` and
   `deposit/oahu-procurement-sources.tar.gz`.
3. Metadata: the fields in `.zenodo.json` (title, description, creators,
   keywords, license CC-BY-4.0, related identifier = this repo). Zenodo can
   also read `.zenodo.json` automatically if the deposit is created through the
   GitHub–Zenodo integration on a repository release.
4. Publish, then copy the DOI into the "DOI" line above and into `README.md`.

License: CC-BY-4.0 for the compilation and derived layers. Included U.S. and
Hawaiʻi government documents are public records.
