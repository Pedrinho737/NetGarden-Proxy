# NetGarden-Proxy
Modern TCP/BSON proxy with GUI, packet inspection, spam filtering, and NetStrings decoding. Currently supports Pixel Worlds (Beta).

# NetGarden 🌱

NetGarden is a modern TCP/BSON proxy and packet inspector with a real-time graphical interface.

It allows developers and researchers to visualize, inspect, and analyze network traffic in a clean and intuitive environment.

Currently in Beta.

---

## Features

• Real-time TCP proxy  
• Full BSON packet decoding  
• Live packet inspector with structured view  
• Client and Server packet separation  
• Packet linking (request ↔ response matching)  
• Packet coloring and highlighting system  
• Spam / heartbeat packet filtering  
• NetStrings decoding mode (Beta)  
• Built-in console and error viewer  
• Auto-scroll and live packet updates  
• Modern GUI built with PySide6  

---

## Pixel Worlds Support

NetGarden currently supports Pixel Worlds protocol analysis.

It correctly handles:

• Length-prefixed BSON packets  
• NetStrings packet identifiers  
• Real-time traffic inspection  

Future versions will support additional protocols.

---

## Current Status

NetGarden is in Beta.

Core proxy and inspection systems are stable.

More features are planned, including:

• Protocol plugins  
• Packet editing and injection  
• Advanced filtering  
• Traffic recording and replay  
• Multi-game support  

---

## Purpose

NetGarden was designed as a clean and powerful alternative to traditional packet proxies.

It focuses on:

• Clarity  
• Performance  
• Usability  
• Extensibility  

---

## Tech Stack

Python  
PySide6  
TCP sockets  
BSON decoding  

---

## Warning

This tool is intended for educational, debugging, and research purposes only.

You need to install the PySide6 and PyMongo libraries (pip install pymongo) (pip install PySide6)

---

## Author

Created by Pedrin 🌱
