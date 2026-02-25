# NetGarden Proxy 🌱

NetGarden is a modern TCP/BSON proxy and packet inspector with a real-time graphical interface.

It allows developers, researchers, and enthusiasts to visualize, inspect, and analyze network traffic in a clean, structured, and intuitive environment.

Currently in Beta.

---

## Overview

NetGarden provides a powerful proxy and inspection system designed for clarity, usability, and extensibility. It enables real-time traffic analysis with structured packet decoding and visual inspection tools.

It currently supports Pixel Worlds protocol analysis and is designed to support additional protocols in future releases.

---

## Features

- Real-time TCP proxy  
- Full BSON packet decoding  
- NetStrings decoding support  
- Live packet inspector with structured visualization  
- Separate Client and Server packet streams  
- Request ↔ Response packet linking  
- Packet highlighting and color coding  
- Spam and heartbeat packet filtering  
- Built-in console and error viewer  
- Auto-scroll and live updates  
- Modern GUI built with PySide6  

---

## Pixel Worlds Support

NetGarden currently supports analysis of the Pixel Worlds protocol, including:

- Length-prefixed BSON packets  
- NetStrings packet identifiers  
- Real-time traffic inspection  

Support for additional protocols is planned.

---

## Installation

### Option 1 — Recommended (Executable)

Download the latest executable from the Releases section and run:

NetGardenProxy.exe

No Python installation is required.

---

### Option 2 — Run from source

Requirements:

- Python 3.10+
- PySide6
- pymongo

Install dependencies:

pip install PySide6 pymongo

Run the proxy:

python -m NetGarden.Main

---

## Project Structure

NetGarden/
├── CORE/
├── GUI/
└── Main.py

---

## Current Status

NetGarden is currently in Beta.

Core proxy and packet inspection systems are stable.

Planned features include:

- Protocol plugin system  
- Packet editing and injection  
- Advanced filtering tools  
- Traffic recording and replay  
- Multi-protocol support  

---

## Tech Stack

- Python  
- PySide6 (GUI)  
- TCP sockets  
- BSON decoding  
- pymongo BSON utilities  

---

## Purpose

NetGarden was created as a modern, clean, and extensible alternative to traditional packet proxy tools.

It focuses on:

- Clarity  
- Performance  
- Usability  
- Extensibility  

---

## Warning

This tool is intended for educational, debugging, and research purposes only.

Use responsibly.

---

## Author

Created by Pedrin 🌱
