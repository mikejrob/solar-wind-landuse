/* Oʻahu Land Use Explorer — Leaflet app. Data in ./data (built by analysis/build_webmap.py). */
const D = 'data/';
const map = L.map('map', { preferCanvas: true, zoomControl: true }).setView([21.48, -158.0], 11);
const canvas = L.canvas({ padding: 0.3 });

// basemaps
const bases = {
  'Light (CARTO)': L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', { maxZoom: 20, attribution: '&copy; OpenStreetMap, &copy; CARTO' }),
  'Imagery (Esri)': L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', { maxZoom: 19, attribution: 'Esri, Maxar, Earthstar Geographics' }),
  'Topo (USGS)': L.tileLayer('https://basemap.nationalmap.gov/arcgis/rest/services/USGSTopo/MapServer/tile/{z}/{y}/{x}', { maxZoom: 16, attribution: 'USGS' })
};
bases['Light (CARTO)'].addTo(map);
const bm = document.getElementById('basemaps');
Object.keys(bases).forEach((k, i) => {
  const id = 'bm' + i; const row = document.createElement('div'); row.className = 'row';
  row.innerHTML = `<input type="radio" name="bm" id="${id}" ${i === 0 ? 'checked' : ''}><label for="${id}">${k}</label>`;
  row.querySelector('input').onchange = () => { Object.values(bases).forEach(b => map.removeLayer(b)); bases[k].addTo(map); };
  bm.appendChild(row);
});

// palettes
const PAL = {
  owner_type: { state: '#1f78b4', federal: '#6a3d9a', county: '#a6cee3', dhhl: '#b15928', private_estate_trust: '#e31a1c', corporate_ag: '#33a02c', developer: '#ff7f00', corporate_other: '#fdbf6f', nonprofit: '#cab2d6', individual: '#b2df8a', utility: '#000000', unknown: '#bbbbbb' },
  use2020: { diversified_crop: '#33a02c', seed_production: '#ffd300', pineapple: '#b5705b', pasture: '#e8ffbf', flowers_foliage_landscape: '#fb9a99', banana: '#d1ff00', aquaculture: '#4d70a3', tropical_fruits: '#ff2626', coffee: '#702600', papaya: '#336600', taro: '#a05989', commercial_forestry: '#007777', macadamia_nuts: '#54ff00', none_mapped: '#e0e0e0' },
  lsb_dom: { A: '#7f0000', B: '#d7301f', C: '#fc8d59', D: '#fdcc8a', E: '#fef0d9', unrated: '#dddddd' },
  elig: { 'banned (class A only)': '#7f0000', 'by right, ≤5 ac': '#c7e9c0', 'by right, 5–20 ac': '#41ab5d', 'by right, 20 ac cap': '#00441b', 'D/E only (uncapped)': '#fdd49e', 'no B/C or D/E': '#eeeeee' },
  flags: { flagged: '#e6550d', none: '#e8e8e8' },
  chg: { hdoa_crop_now_noncrop_3yr: '#d95f0e', hdoa_unmapped_now_crop_3yr: '#1b9e77', none: '#e8e8e8' }
};
const RAMP = ['#f7fbff', '#deebf7', '#c6dbef', '#9ecae1', '#6baed6', '#4292c6', '#2171b5', '#08519c', '#08306b'];
const ramp = v => RAMP[Math.min(8, Math.max(0, Math.floor(v * 9)))];
const eligClass = p => {
  const bc = (p.lsb_b || 0) + (p.lsb_c || 0), de = (p.lsb_d || 0) + (p.lsb_e || 0);
  if (p.s0_ac >= 19.9) return 'by right, 20 ac cap';
  if (p.s0_ac >= 5) return 'by right, 5–20 ac';
  if (p.s0_ac > 0) return 'by right, ≤5 ac';
  if (de > 0) return 'D/E only (uncapped)';
  if ((p.lsb_a || 0) > 0 && bc === 0) return 'banned (class A only)';
  return 'no B/C or D/E';
};
function parcelColor(p, mode) {
  switch (mode) {
    case 'owner_type': return PAL.owner_type[p.owner_type] || '#bbb';
    case 'use2020': return PAL.use2020[p.use2020] || '#e0e0e0';
    case 'lsb_dom': return PAL.lsb_dom[p.lsb_dom] || '#ddd';
    case 'elig': return PAL.elig[eligClass(p)];
    case 's3_share': return p.acres ? ramp(p.s3_ac / p.acres) : '#eee';
    case 'slope': return p.acres ? ramp(p.slope_le15 / p.acres) : '#eee';
    case 'hcdl': return p.acres ? ramp(p.hcdl24_crop_ac / p.acres) : '#eee';
    case 'flags': return p.flags ? PAL.flags.flagged : PAL.flags.none;
    case 'chg': return PAL.chg[p.chg] || PAL.chg.none;
    default: return null;
  }
}
function legendFor(mode) {
  const el = document.getElementById('legend'); el.innerHTML = '';
  const add = (c, t) => { const d = document.createElement('div'); d.className = 'lg'; d.innerHTML = `<span class="sw" style="background:${c}"></span>${t}`; el.appendChild(d); };
  if (PAL[mode]) Object.entries(PAL[mode]).forEach(([k, c]) => add(c, k.replace(/_/g, ' ')));
  else if (mode !== 'none') { add(RAMP[0], '0%'); add(RAMP[4], '~50%'); add(RAMP[8], '100%'); }
}

// popups
const LBL = { tmk: 'TMK', acres: 'Parcel acres', owner: 'Owner (RPAD 2027)', owner_type: 'Owner type', lsb_a: 'LSB A ac', lsb_b: 'LSB B ac', lsb_c: 'LSB C ac', lsb_d: 'LSB D ac', lsb_e: 'LSB E ac', lsb_dom: 'Dominant class', s0_ac: 'Solar by right, current cap (ac)', s3_ac: '20%-no-cap counterfactual (ac)', use2020: 'HDOA 2020 dominant use', use2020_ac: 'HDOA 2020 ag use (ac)', crop2020_ac: '…of which cropped', past2020_ac: '…of which pasture', hcdl24_crop_ac: 'HCDL 2024 crop cover (ac)', hcdl24_corn_ac: '…seed corn', hcdl24_grass_ac: 'HCDL 2024 grassland (ac)', slope_le15: 'Slope ≤15% (ac)', slope_15_30: 'Slope 15–30% (ac)', slope_gt30: 'Slope >30% (ac)', d46_km: 'Dist. to mapped 46 kV+ (km)', d138_km: 'Dist. to 138 kV (km)', flags: 'Reviewer issue flags', bc_sel: 'In modeled B/C 10% draw', chg: 'HDOA→HCDL change candidate', chg_ac: '…acres (UNVERIFIED)' };
function popupHTML(p) {
  const rows = Object.keys(LBL).filter(k => p[k] !== undefined && p[k] !== null && p[k] !== '' && !(k === 'bc_sel' && !p[k]))
    .map(k => `<tr><td>${LBL[k]}</td><td>${k === 'bc_sel' ? 'yes' : p[k]}</td></tr>`).join('');
  return `<b>Ag-district parcel ${p.tmk}</b><table>${rows}</table>`;
}
const simplePopup = (title, p, keys) => `<b>${title}</b><table>${keys.filter(k => p[k] !== undefined && p[k] !== '').map(k => `<tr><td>${k}</td><td>${p[k]}</td></tr>`).join('')}</table>`;

// layers
const layers = {}; const status = document.getElementById('status');
const say = t => { status.textContent = t; };
async function gj(name) { const r = await fetch(D + name); if (!r.ok) throw new Error(name); return r.json(); }
let colorMode = 'owner_type';
function parcelStyle(f) {
  const c = parcelColor(f.properties, colorMode);
  return c ? { color: '#444', weight: 0.4, fillColor: c, fillOpacity: 0.65 } : { color: '#444', weight: 0.6, fillOpacity: 0 };
}
(async () => {
  say('Loading layers…');
  const [parcels, slud, lsb, hdoa, lines, solar, mil, wind, bounds, hlegend] = await Promise.all([
    gj('ag_parcels.geojson'), gj('slud.geojson'), gj('lsb.geojson'), gj('hdoa2020.geojson'), gj('lines.geojson'), gj('solar_osm.geojson'), gj('military.geojson'), gj('wind_turbines.geojson'), gj('hcdl_bounds.json'), gj('hcdl_legend.json')]);
  layers.parcels = L.geoJSON(parcels, { renderer: canvas, interactive: false, style: parcelStyle });
  const SLUDC = { A: '#8dd3a0', U: '#fb8072', C: '#80b1d3', R: '#fdb462' };
  layers.slud = L.geoJSON(slud, { renderer: canvas, interactive: false, style: f => ({ color: SLUDC[f.properties.ludcode], weight: 1.2, fillColor: SLUDC[f.properties.ludcode], fillOpacity: 0.18 }), onEachFeature: (f, l) => l.bindPopup(simplePopup('State land-use district', { district: { A: 'Agricultural', U: 'Urban', C: 'Conservation', R: 'Rural' }[f.properties.ludcode], acres: f.properties.acres }, ['district', 'acres'])) }).addTo(map);
  layers.lsb = L.geoJSON(lsb, { renderer: canvas, interactive: false, style: f => ({ color: '#333', weight: 0.3, fillColor: PAL.lsb_dom[f.properties.cls] || '#ddd', fillOpacity: 0.55 }), onEachFeature: (f, l) => l.bindPopup(simplePopup('LSB productivity class', f.properties, ['cls', 'acres'])) });
  layers.hdoa = L.geoJSON(hdoa, { renderer: canvas, interactive: false, style: f => ({ color: '#2b2b2b', weight: 0.5, fillColor: PAL.use2020[f.properties.crop.toLowerCase().replace(/ \/ /g, '_').replace(/ /g, '_')] || '#999', fillOpacity: 0.7 }), onEachFeature: (f, l) => l.bindPopup(simplePopup('HDOA 2020 baseline', f.properties, ['crop', 'acreage'])) });
  layers.lines = L.geoJSON(lines, { style: f => ({ color: f.properties.kv === '138' ? '#4a3aa7' : '#2a78d6', weight: f.properties.kv === '138' ? 2.4 : 1.3 }), onEachFeature: (f, l) => l.bindPopup(simplePopup('Transmission line', f.properties, ['kv', 'src'])).on('click', L.DomEvent.stopPropagation) }).addTo(map);
  layers.solar = L.geoJSON(solar, { interactive: false, style: { color: '#b3261e', weight: 1.2, fillColor: '#f2c94c', fillOpacity: 0.6 }, onEachFeature: (f, l) => l.bindPopup(simplePopup('Solar plant (OSM)', f.properties, ['name', 'mw', 'operator', 'acres', 'osm'])) }).addTo(map);
  layers.military = L.geoJSON(mil, { renderer: canvas, interactive: false, style: f => ({ color: '#555', weight: 0.8, fillColor: f.properties.tenure && f.properties.tenure.includes('lease') ? '#bdbdbd' : '#737373', fillOpacity: 0.35, dashArray: '3 3' }), onEachFeature: (f, l) => l.bindPopup(simplePopup('Military land', f.properties, ['name', 'tenure', 'acres'])) });
  layers.wind = L.geoJSON(wind, { pointToLayer: (f, ll) => L.circleMarker(ll, { radius: 4, color: '#1b1b1b', fillColor: '#ffffff', fillOpacity: 1, weight: 1.2 }), onEachFeature: (f, l) => l.bindPopup(simplePopup('Wind turbine (OSM)', f.properties, ['farm', 'output', 'manufacturer'])).on('click', L.DomEvent.stopPropagation) }).addTo(map);
  const bb = [[bounds.south, bounds.west], [bounds.north, bounds.east]];
  layers.hcdl24 = L.imageOverlay(D + 'hcdl_2024.png', bb, { opacity: 0.8, attribution: 'USDA NASS / UH Mānoa HCDL' });
  layers.hcdl25 = L.imageOverlay(D + 'hcdl_2025.png', bb, { opacity: 0.8 }).addTo(map);
  layers.allparcels = L.esri.featureLayer({ url: 'https://geodata.hawaii.gov/arcgis/rest/services/ParcelsZoning/MapServer/11', minZoom: 15, simplifyFactor: 0.3, precision: 6, style: { color: '#6b4c9a', weight: 0.7, fillOpacity: 0.03 }, onEachFeature: (f, l) => l.bindPopup(() => simplePopup('Parcel (state GIS, live)', f.properties, ['tmk9txt', 'gisacres'])) }).addTo(map);
  // HCDL legend
  const hl = document.getElementById('hcdl-legend');
  Object.values(hlegend).forEach(v => { const d = document.createElement('div'); d.className = 'lg'; d.innerHTML = `<span class="sw" style="background:${v.color}"></span>${v.name}`; hl.appendChild(d); });
  legendFor(colorMode);
  ['hcdl24', 'hcdl25'].forEach(k => map.hasLayer(layers[k]) && layers[k].bringToBack());
  const ll = document.getElementById('lsb-legend');
  [['A', 'A — highest productivity (solar banned)'], ['B', 'B (solar capped 10%/20 ac)'], ['C', 'C (capped)'], ['D', 'D (uncapped)'], ['E', 'E — lowest (uncapped)']].forEach(([k, t]) => { const d = document.createElement('div'); d.className = 'lg'; d.innerHTML = `<span class="sw" style="background:${PAL.lsb_dom[k]}"></span>${t}`; ll.appendChild(d); });
  document.getElementById('chk-lsb').addEventListener('change', e => { ll.style.display = e.target.checked ? 'grid' : 'none'; });

  // order: rasters under vectors
  const order = () => { ['hcdl24', 'hcdl25'].forEach(k => map.hasLayer(layers[k]) && layers[k].bringToBack()); };
  const bind = (id, key) => { const c = document.getElementById(id); c.onchange = () => { c.checked ? layers[key].addTo(map) : map.removeLayer(layers[key]); order(); }; };
  bind('chk-parcels', 'parcels'); bind('chk-slud', 'slud'); bind('chk-lsb', 'lsb'); bind('chk-hdoa', 'hdoa'); bind('chk-lines', 'lines'); bind('chk-solar', 'solar'); bind('chk-military', 'military'); bind('chk-wind', 'wind'); bind('chk-hcdl24', 'hcdl24'); bind('chk-hcdl25', 'hcdl25'); bind('chk-allparcels', 'allparcels');
  document.getElementById('hcdl-op').oninput = e => { const o = e.target.value / 100; layers.hcdl24.setOpacity(o); layers.hcdl25.setOpacity(o); };
  // ---- click-anywhere card: point-in-polygon over the loaded layers ----
  const pip = (pt, feat) => {            // pt = [lon, lat]; ray casting over Polygon / MultiPolygon rings
    const g = feat.geometry; if (!g) return false;
    const geoms = g.type === 'GeometryCollection' ? g.geometries : [g];
    const polys = []; geoms.forEach(x => { if (x.type === 'Polygon') polys.push(x.coordinates); else if (x.type === 'MultiPolygon') x.coordinates.forEach(c => polys.push(c)); });
    const inRing = (ring) => { let inside = false; for (let i = 0, k = ring.length - 1; i < ring.length; k = i++) { const [xi, yi] = ring[i], [xk, yk] = ring[k]; if ((yi > pt[1]) !== (yk > pt[1]) && pt[0] < (xk - xi) * (pt[1] - yi) / (yk - yi) + xi) inside = !inside; } return inside; };
    return polys.some(rings => inRing(rings[0]) && !rings.slice(1).some(inRing));
  };
  const withBbox = fc => { fc.features.forEach(f => { const bb = [Infinity, Infinity, -Infinity, -Infinity]; const walk = c => { if (typeof c[0] === 'number') { if (c[0] < bb[0]) bb[0] = c[0]; if (c[1] < bb[1]) bb[1] = c[1]; if (c[0] > bb[2]) bb[2] = c[0]; if (c[1] > bb[3]) bb[3] = c[1]; } else c.forEach(walk); }; const g = f.geometry; if (g && g.type === 'GeometryCollection') g.geometries.forEach(x => x.coordinates && walk(x.coordinates)); else if (g && g.coordinates) walk(g.coordinates); f._bb = bb; }); return fc; };
  [parcels, slud, lsb, hdoa, mil, solar].forEach(withBbox);
  const hit = (fc, pt) => fc.features.find(f => pt[0] >= f._bb[0] && pt[0] <= f._bb[2] && pt[1] >= f._bb[1] && pt[1] <= f._bb[3] && pip(pt, f));
  const DIST = { A: 'Agricultural', U: 'Urban', C: 'Conservation', R: 'Rural' };
  const nice = s => (s || '').replace(/_/g, ' ');
  function card(latlng, Pgiven) {
    const pt = [latlng.lng, latlng.lat];
    const P = Pgiven || hit(parcels, pt), S = hit(slud, pt), Lb = hit(lsb, pt), H = hit(hdoa, pt), M = hit(mil, pt), So = hit(solar, pt);
    let html = '';
    const row = (k, v) => `<tr><td>${k}</td><td>${v}</td></tr>`;
    html += `<b>${P ? 'Ag-district parcel ' + P.properties.tmk : 'Point ' + latlng.lat.toFixed(5) + ', ' + latlng.lng.toFixed(5)}</b><table>`;
    html += row('State land-use district', S ? DIST[S.properties.ludcode] : 'none mapped');
    html += row('LSB soil class at point', Lb ? Lb.properties.cls : 'unrated');
    if (P) {
      const p = P.properties;
      html += row('Predominant soil class (parcel)', `${p.lsb_dom}${p.lsb_dom !== 'unrated' ? ' (' + p['lsb_' + p.lsb_dom.toLowerCase()] + ' of ' + p.acres + ' ac)' : ''}`);
      html += row('HDOA 2020 at point', H ? H.properties.crop : 'no mapped commercial use (fallow, non-commercial, or unused in 2018–20 imagery)');
      html += row('HDOA 2020, parcel', p.use2020 === 'none_mapped' ? 'no mapped commercial use' : `${nice(p.use2020)} dominant; ${p.crop2020_ac} ac cropped, ${p.past2020_ac} ac pasture`);
      html += row('CDL 2024, parcel', `${p.hcdl24_crop_ac} ac crop cover (${p.hcdl24_corn_ac} ac corn); ${p.hcdl24_grass_ac} ac grassland`);
      html += row('Owner', `${p.owner} <i>(${nice(p.owner_type)})</i>`);
      html += row('Solar by right, current cap', `${p.s0_ac} ac; 20%-no-cap: ${p.s3_ac} ac`);
      html += row('Slope', `${p.slope_le15} ac ≤15%, ${p.slope_15_30} ac 15–30%, ${p.slope_gt30} ac >30%`);
      html += row('Grid', `${p.d46_km} km to mapped 46 kV+, ${p.d138_km} km to 138 kV`);
      if (p.flags) html += row('<b>Issue flags</b>', `<b>${p.flags}</b>`);
      if (p.chg) html += row('Change candidate', `${nice(p.chg)} (${p.chg_ac} ac, UNVERIFIED)`);
      if (p.bc_sel) html += row('Modeled B/C draw', 'yes');
    } else {
      if (H) html += row('HDOA 2020 at point', H.properties.crop);
    }
    if (M) html += row('Military land', `${M.properties.name} (${nice(M.properties.tenure)})`);
    if (So) html += row('Solar plant (OSM)', `${So.properties.name || So.properties.osm} ${So.properties.mw}`);
    html += '</table>';
    const pop = L.popup({ maxWidth: 420 }).setLatLng(latlng).setContent(html + (P ? '' : '<div id="live-tmk" style="color:#666">looking up parcel…</div>')).openOn(map);
    if (!P) L.esri.query({ url: 'https://geodata.hawaii.gov/arcgis/rest/services/ParcelsZoning/MapServer/11' }).contains(latlng).fields(['tmk9txt', 'gisacres']).returnGeometry(false).run((err, fc) => {
      const el = document.getElementById('live-tmk'); if (!el) return;
      el.innerHTML = err || !fc.features.length ? 'no parcel at this point' : fc.features.map(f => `Parcel (state GIS): TMK ${f.properties.tmk9txt}, ${Number(f.properties.gisacres).toFixed(1)} ac (outside the ag-district table)`).join('<br>');
    });
  }
  map.on('click', e => card(e.latlng));
  const goTmk = tmk => { const f = parcels.features.find(x => x.properties.tmk === tmk); if (!f) return false; const b = L.latLngBounds([[f._bb[1], f._bb[0]], [f._bb[3], f._bb[2]]]); map.fitBounds(b, { maxZoom: 16 }); card(b.getCenter(), f); return true; };
  document.getElementById('color-by').onchange = e => { colorMode = e.target.value; layers.parcels.setStyle(parcelStyle); legendFor(colorMode); };
  const go = () => { const t = document.getElementById('tmk').value.replace(/\D/g, ''); if (!goTmk(t)) say(`TMK ${t} not among ag-district parcels`); };
  document.getElementById('tmk-go').onclick = go; document.getElementById('tmk').onkeydown = e => { if (e.key === 'Enter') go(); };
  map.on('zoomend', () => { if (map.getZoom() < 15 && document.getElementById('chk-allparcels').checked) say('Zoom in to 15+ for all parcels'); else say(''); });
  say(`Loaded ${parcels.features.length.toLocaleString()} ag-district parcels, ${hdoa.features.length} HDOA polygons, ${lsb.features.length.toLocaleString()} LSB polygons.`);
})().catch(e => { say('Load error: ' + e.message); console.error(e); });
document.getElementById('about-link').onclick = e => { e.preventDefault(); showAbout(); };
const aboutEl = document.getElementById('about');
const showAbout = () => { aboutEl.style.display = 'flex'; };
const hideAbout = () => { aboutEl.style.display = 'none'; };
document.getElementById('about-close').addEventListener('click', hideAbout);
aboutEl.addEventListener('click', e => { if (e.target === aboutEl) hideAbout(); });
document.addEventListener('keydown', e => { if (e.key === 'Escape') hideAbout(); });
