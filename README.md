# Overhead Aircraft Tracker

A Raspberry Pi application that finds the closest aircraft to your configured location using live ADS-B data and displays its information on an LCD. It refreshes every 30 seconds.

## Features
- Live aircraft positions from the public [Airplanes.live ADS-B API](https://airplanes.live/)
- Closest-aircraft selection and distance calculation
- Callsign, aircraft type, registration, altitude, ground speed, heading and distance
- Full-screen aviation-style interface for HDMI/desktop displays
- Handles missing aircraft and temporary network/API errors

## Setup
1. Clone this repository: `git clone https://github.com/altem80s/Overhead-Aircraft-Tracker.git`
2. Install system packages: `sudo apt update && sudo apt install -y python3-venv python3-pip python3-pygame`
3. Create a virtual environment: `python3 -m venv --system-site-packages .venv && source .venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and enter your own decimal-degree latitude and longitude. Keep `.env` private; it is ignored by Git.
6. Run `python main.py`. Press Esc or Q to quit.

## Settings
- LATITUDE / LONGITUDE: required coordinates for the display location
- SEARCH_RADIUS_KM: API search radius (default 15 km)
- OVERHEAD_RADIUS_KM: maximum horizontal distance to label a plane overhead (default 5 km)
- REFRESH_SECONDS: update interval (default 30 seconds)
- DISPLAY_WIDTH / DISPLAY_HEIGHT: display resolution (default 800x480)
- FULLSCREEN: full-screen mode (default true)

## Display compatibility
The current display uses Pygame and targets an HDMI-connected display in a graphical Raspberry Pi OS session. SPI/GPIO LCDs need a model-specific driver; identify the exact screen before wiring or choosing that driver.

## Data limitations
ADS-B coverage and aircraft broadcasts vary. Some aircraft may not appear, and callsigns or aircraft details may be unavailable. The app does not invent airline, origin, or destination information. It is informational only, not for navigation or aviation safety.
