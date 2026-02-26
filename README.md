# NetGarden Proxy 🌱

NetGarden is a modern **TCP/BSON proxy** and **real-time packet inspector** with a clean GUI focused on clarity, speed, and usability.

It helps developers, researchers, and enthusiasts **visualize, inspect, and analyze** network traffic in a structured and intuitive way.

> Status: **Beta** (actively evolving)

---

## Overview

NetGarden acts as a TCP proxy between a client and a server and provides a live inspection interface where you can:

- See **Client** and **Server** packet streams side-by-side
- Inspect decoded BSON in **tree view** or **decoded view**
- Highlight and filter packets for easier debugging
- Hide spam/heartbeat noise and restore it anytime
- Save important packets and jump to them instantly

NetGarden currently targets **Pixel Worlds protocol analysis**, and the project is built to support more protocols in the future.

---

## Features

### Proxy & Decoding
- Real-time **TCP proxy**
- **Length-prefixed BSON** decoding
- **NetStrings decoding (BETA)** to display readable identifiers

### Inspector & UI
- Separate **Client** and **Server** packet streams
- Built-in inspector with **two modes**:
  - **Tree mode** (structured/expandable)
  - **Decode mode** (pretty JSON “full view”)
- Right-click actions:
  - **View decoded**
  - **Save packet**
  - **Mark as spam/heartbeat**
  - **Color tag** by packet ID (applies to future packets with same ID)
- **Saved Packets window** (jump to any saved packet instantly)
- Built-in **console/log viewer** for errors and runtime logs
- **Auto-scroll** and live updates

### Filtering & Anti-noise
- Filter by packet ID
- Manual spam/heartbeat hiding
- **Auto-hide spam** (rate-based)
- **Restore hidden packets** anytime

### Launcher & Quality-of-life
- Launcher screen to configure:
  - Client IP/Port
  - Server IP/Port
- “Local (127.0.0.1)” quick button
- **Recent connections** list (click-to-fill)
- **Language switch (PT-BR / EN)** saved across restarts
- When the proxy stops/closes, it returns to the launcher automatically

---

## Pixel Worlds Support

NetGarden currently supports Pixel Worlds traffic inspection including:

- Length-prefixed BSON packets
- NetStrings-based packet identifiers (BETA)
- Real-time decode and inspection in GUI

More protocols are planned.

---

## Installation

### Option 1 — Recommended (Executable)

Download the latest Windows executable from **Releases** and run:

`NetGarden.exe`

No Python installation required.

---

### Option 2 — Run from Source

#### Requirements
- Python **3.10+**
- PySide6
- pymongo (BSON utilities)

#### Install dependencies
```bash
pip install PySide6 pymongo
