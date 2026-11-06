"""Main application loop."""
import time
import pygame
import requests
from aircraft_api import fetch_aircraft, enrich_aircraft, select_aircraft, make_summary
from config import load_settings
from display import AircraftDisplay

def main():
    try:
        settings = load_settings()
    except (ValueError, TypeError) as exc:
        print(f"Configuration error: {exc}")
        print("Copy .env.example to .env and enter your coordinates.")
        return 1

    display = AircraftDisplay(settings.display_width, settings.display_height,
                              settings.fullscreen)
    current = make_summary(None, False)
    next_update = 0.0
    running = True
    print("Tracker running. Press Esc or Q to quit.")
    try:
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_q):
                    running = False
            now = time.monotonic()
            if now >= next_update:
                try:
                    raw = fetch_aircraft(settings.latitude, settings.longitude,
                                         settings.search_radius_km)
                    planes = enrich_aircraft(raw, settings.latitude, settings.longitude)
                    target, overhead = select_aircraft(planes, settings.overhead_radius_km)
                    current = make_summary(target, overhead)
                    print(f'Updated: {current["callsign"]} at {current["distance"]}')
                except (requests.RequestException, ValueError, KeyError) as exc:
                    current = dict(current)
                    current["status"] = "DATA CONNECTION ISSUE"
                    current["updated"] = "RETRYING"
                    print(f"Aircraft request failed: {exc}")
                next_update = now + settings.refresh_seconds
            display.draw(current, max(0, int(next_update-time.monotonic())))
            display.tick()
    finally:
        display.close()
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
