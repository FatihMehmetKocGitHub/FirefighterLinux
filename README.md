# Firefighter Linux

Offline-first disaster response and field coordination Linux distribution.

## About

Firefighter Linux is an Ubuntu/Xubuntu-based Linux distribution developed by Fatih Mehmet Koç.

The project focuses on:

- Disaster response
- Offline-first communication
- Field coordination
- Mesh / LoRa communication systems
- Incident reporting
- Local + central synchronization
- Lightweight emergency infrastructure

The goal is to provide a usable operating system for crisis situations such as:

- Earthquakes
- Wildfires
- Floods
- Search and rescue operations
- Communication outages

---

# Features

## Firefighter Central Dashboard

- Live incident map
- PostgreSQL central database
- LXC API infrastructure
- Marker-based incident tracking
- Web dashboard
- Click-to-add incidents from map

## Offline-first Architecture

- Local SQLite storage
- Auto sync system
- Offline map infrastructure
- Local reporting tools
- Internet-independent workflows

## Mesh / LoRa Ready

- Meshtastic CLI integration
- LoRa helper commands
- Mesh node monitoring
- SOS messaging infrastructure

## Firefighter Linux Commands

- `ffl-bora`
- `ffl-info`
- `ffl-report`
- `ffl-map`
- `ffl-map-add`
- `ffl-auto-sync`
- `ffl-mesh-status`
- `ffl-mesh-send`
- `ffl-mesh-sos`

---

# Technologies

- Ubuntu / Xubuntu 24.04 LTS
- Python
- Flask
- PostgreSQL
- SQLite
- Leaflet.js
- OpenStreetMap
- LXC / LXD
- Meshtastic
- systemd

---

# Current Status

Current version:

```text
V0.1 DEV
