"""Load local application settings."""
import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

def number(name, default=None):
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return default
    try:
        return float(raw)
    except ValueError as exc:
        raise ValueError(f"{name} must be numeric") from exc

@dataclass(frozen=True)
class Settings:
    latitude: float
    longitude: float
    search_radius_km: float
    overhead_radius_km: float
    refresh_seconds: int
    display_width: int
    display_height: int
    fullscreen: bool

def load_settings():
    lat, lon = number("LATITUDE"), number("LONGITUDE")
    if lat is None or lon is None:
        raise ValueError("Set LATITUDE and LONGITUDE in your .env file.")
    if not -90 <= lat <= 90 or not -180 <= lon <= 180:
        raise ValueError("Coordinates are outside valid latitude/longitude ranges.")
    search = number("SEARCH_RADIUS_KM", 15.0)
    overhead = number("OVERHEAD_RADIUS_KM", 5.0)
    refresh = int(number("REFRESH_SECONDS", 30))
    if not 1 <= search <= 250:
        raise ValueError("SEARCH_RADIUS_KM must be between 1 and 250.")
    if not 0 < overhead <= search:
        raise ValueError("OVERHEAD_RADIUS_KM must be positive and <= SEARCH_RADIUS_KM.")
    if refresh < 10:
        raise ValueError("REFRESH_SECONDS must be at least 10.")
    return Settings(
        lat, lon, search, overhead, refresh,
        int(number("DISPLAY_WIDTH", 800)),
        int(number("DISPLAY_HEIGHT", 480)),
        os.getenv("FULLSCREEN", "true").lower() in ("1", "true", "yes", "on")
    )
