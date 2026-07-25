"""Annual plane-of-array insolation vs ground-slope aspect at Oahu latitude.

Quantifies the aspect (compass-direction) effect of a 10-30% ground slope on a
fixed-tilt PV plane at Oahu's latitude (21.35N). A module laid flat on the
ground inherits the ground's tilt and azimuth; this script transposes clear-sky
global horizontal irradiance to the plane of array for that geometry, facing
south / north / east, and sums it over a year.

Method: pvlib clear-sky Ineichen (default Linke-turbidity climatology) at
30-min resolution, Perez transposition, 0.2 albedo. Clear-sky (no clouds), so
the ABSOLUTE kWh/m2 are upper bounds; use only the RATIOS between orientations.
Real Oahu has substantial cloud cover (higher diffuse fraction), which damps the
aspect swing below these clear-sky figures.

Output: data/oahu_poa_aspect_slope.csv and a printed table.
Feeds notes/slope-15-30-challenges.md sec. 2. Requires: pvlib, pandas, numpy.
"""
import numpy as np
import pandas as pd
import pvlib

LAT, LON, ALT, TZ = 21.35, -157.9, 100.0, "Pacific/Honolulu"
loc = pvlib.location.Location(LAT, LON, tz=TZ, altitude=ALT)

times = pd.date_range("2025-01-01", "2025-12-31 23:59", freq="30min", tz=TZ)
cs = loc.get_clearsky(times, model="ineichen")
sp = loc.get_solarposition(times)
dni_extra = pvlib.irradiance.get_extra_radiation(times)
airmass = loc.get_airmass(times)["airmass_relative"]


def annual_poa(tilt_deg, azimuth_deg, albedo=0.2):
    poa = pvlib.irradiance.get_total_irradiance(
        surface_tilt=tilt_deg, surface_azimuth=azimuth_deg,
        solar_zenith=sp["apparent_zenith"], solar_azimuth=sp["azimuth"],
        dni=cs["dni"], ghi=cs["ghi"], dhi=cs["dhi"],
        dni_extra=dni_extra, airmass=airmass, albedo=albedo, model="perez")
    return poa["poa_global"].fillna(0).sum() * 0.5 / 1000.0  # kWh/m2/yr


pct_to_deg = lambda p: np.degrees(np.arctan(p / 100.0))
horiz = annual_poa(0.0, 180.0)

rows = []
for p in [0, 10, 15, 20, 25, 30]:
    t = pct_to_deg(p)
    s, n, e = annual_poa(t, 180.0), annual_poa(t, 0.0), annual_poa(t, 90.0)
    rows.append(dict(slope_pct=p, tilt_deg=round(t, 2),
                     poa_south=round(s), poa_north=round(n), poa_east=round(e),
                     south_vs_horiz_pct=round(s / horiz * 100 - 100, 1),
                     north_vs_horiz_pct=round(n / horiz * 100 - 100, 1),
                     east_vs_horiz_pct=round(e / horiz * 100 - 100, 1),
                     south_vs_north_pct=round(s / n * 100 - 100, 1)))

df = pd.DataFrame(rows)
df.to_csv("data/oahu_poa_aspect_slope.csv", index=False)
print(f"clear-sky horizontal POA = {horiz:.0f} kWh/m2/yr; "
      f"lat-optimal 21S = {annual_poa(21.0,180.0):.0f} "
      f"({annual_poa(21.0,180.0)/horiz*100-100:+.1f}%)")
print(df.to_string(index=False))
