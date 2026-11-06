"""Airplanes.live ADS-B API client and aircraft selection."""
import math
from datetime import datetime
import requests

API_URL = "https://api.airplanes.live/v2/point/{lat}/{lon}/{radius_nm}"
SESSION = requests.Session()
SESSION.headers.update({"User-Agent": "OverheadAircraftTracker/1.0"})

def haversine_km(lat1, lon1, lat2, lon2):
    earth = 6371.0088
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = math.radians(lat2-lat1), math.radians(lon2-lon1)
    a = math.sin(dp/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return 2*earth*math.asin(math.sqrt(a))

def fetch_aircraft(latitude, longitude, radius_km):
    # API radius is nautical miles.
    radius_nm = radius_km / 1.852
    url = API_URL.format(lat=latitude, lon=longitude, radius_nm=radius_nm)
    response = SESSION.get(url, timeout=12)
    response.raise_for_status()
    aircraft = response.json().get("ac", [])
    if not isinstance(aircraft, list):
        raise ValueError("Unexpected aircraft API response.")
    return aircraft

def enrich_aircraft(records, latitude, longitude):
    result = []
    for item in records:
        try:
            lat, lon = float(item["lat"]), float(item["lon"])
        except (KeyError, TypeError, ValueError):
            continue
        item = dict(item)
        item["distance_km"] = haversine_km(latitude, longitude, lat, lon)
        result.append(item)
    return sorted(result, key=lambda plane: plane["distance_km"])

def select_aircraft(records, overhead_radius_km):
    if not records:
        return None, False
    nearest = records[0]
    return nearest, nearest["distance_km"] <= overhead_radius_km

def altitude(value):
    if value == "ground":
        return "ON GROUND"
    try:
        return f"{int(float(value)):,} FT"
    except (TypeError, ValueError):
        return "N/A"

def number(value, suffix=""):
    try:
        return f"{float(value):.0f}{suffix}"
    except (TypeError, ValueError):
        return "N/A"

def make_summary(plane, overhead):
    updated = datetime.now().astimezone().strftime("%H:%M:%S")
    if plane is None:
        return dict(status="NO AIRCRAFT FOUND", callsign="No aircraft detected",
                    aircraft_type="Waiting for ADS-B data", registration="N/A",
                    altitude="N/A", speed="N/A", heading="N/A",
                    distance="N/A", updated=updated)
    return dict(
        status="AIRCRAFT OVERHEAD" if overhead else "NEARBY AIRCRAFT",
        callsign=(plane.get("flight") or plane.get("hex") or "UNKNOWN").strip(),
        aircraft_type=plane.get("t") or plane.get("desc") or "Type unavailable",
        registration=plane.get("r") or "N/A",
        altitude=altitude(plane.get("alt_baro", plane.get("alt_geom"))),
        speed=number(plane.get("gs"), " KTS"),
        heading=number(plane.get("track"), "°"),
        distance=f'{plane["distance_km"]:.1f} KM',
        updated=updated
    )
