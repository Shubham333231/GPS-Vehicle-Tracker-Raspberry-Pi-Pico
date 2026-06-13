# 📡 GPS Vehicle Tracker using Raspberry Pi Pico



![MicroPython](https://img.shields.io/badge/MicroPython-3.4%2B-green)




![Platform](https://img.shields.io/badge/Platform-Raspberry%20Pi%20Pico-red)




![GSM](https://img.shields.io/badge/GSM-SIM800L-blue)




![GPS](https://img.shields.io/badge/GPS-Neo--6M-orange)




![Status](https://img.shields.io/badge/Status-Completed-brightgreen)



> Real-time GPS Vehicle Tracking System with SMS-based remote monitoring
> and Google Maps integration — built under $30.

---

## 🎯 Project Overview

A complete IoT-based vehicle tracking system built on the **RP2040
microcontroller (Raspberry Pi Pico)**. The system acquires real-time
GPS coordinates via Neo-6M module, parses NMEA sentences using
MicropyGPS library, and transmits location data via SIM800L GSM module
through SMS — including a clickable Google Maps link.

**Key Achievement:** Full working system delivered under $30 vs
$100+ commercial trackers.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| Real-time GPS | Neo-6M with ±2.5m accuracy |
| SMS Commands | LOCATION, STATUS, HELP |
| Google Maps Link | Auto-generated in every SMS |
| LED Indicators | GPS lock + GSM network status |
| No Internet Required | Works on cellular network only |
| Low Cost | Complete build under $30 |

---

## 🔧 Hardware Components

| Component | Specification |
|-----------|--------------|
| Raspberry Pi Pico | RP2040, Dual-core ARM Cortex-M0+, 133MHz |
| Neo-6M GPS Module | u-blox, ±2.5m accuracy, NMEA protocol |
| SIM800L GSM Module | Quad-band 850/900/1800/1900MHz |
| Power Supply | 5V 2A |
| Jumper Wires | 20+ |

---

## 📌 Pin Configuration

Raspberry Pi Pico
│
├── UART0 (GPS Neo-6M)
│   ├── GP0 (TX) ──→ GPS RX
│   └── GP1 (RX) ←── GPS TX
│
├── UART1 (SIM800L GSM)
│   ├── GP4 (TX) ──→ GSM RX
│   └── GP5 (RX) ←── GSM TX
│
├── GP14 ──→ GPS Lock LED
├── GP15 ──→ GSM Network LED
└── VBUS ──→ VCC (GPS + GSM)

---

## 💬 SMS Commands

| Command | Response |
|---------|----------|
| `LOCATION` | Lat, Lng + Google Maps link |
| `STATUS` | GPS fix, satellites, speed, uptime |
| `HELP` | List of all commands |

### Example SMS Response:
GPS LOCATION
Lat: 19.998453
Lng: 73.789621
Satellites: 8
Maps: https://maps.google.com/?q=19.998453,73.789621

---


## 🏗️ System Architecture
GPS Satellites
↓
Neo-6M Module → UART0 → RP2040 (MicropyGPS Parser)
↓
Format Coordinates
↓
SIM800L GSM ← UART1
↓
SMS to Admin Phone
↓
Google Maps Link


---

## 🚀 How to Run

### 1. Install MicroPython on Pico
- Download `.uf2` from micropython.org
- Hold BOOTSEL, connect to PC
- Drag `.uf2` to Pico drive

### 2. Install Thonny IDE
- Download from thonny.org
- Tools → Options → Interpreter
- Select **MicroPython (Raspberry Pi Pico)**

### 3. Upload 
Upload to Pico:
├── main.py
└── micropygps.py  (from MicropyGPS library)
### 4. Configure
```python
# Edit in main.py
ADMIN_NUMBER = "+91XXXXXXXXXX"
GPS_UPDATE_INTERVAL = 10
LOCATION_INTERVAL_MS = 60 * 1000

5. Run
Click Run in Thonny
GPS LED blinks → searching satellites
GPS LED solid → fix acquired
GSM LED blinks → network connected


📊 Results
✅ Real-time GPS tracking with ±2.5m accuracy
✅ SMS delivery under 10 seconds
✅ Google Maps link generation working
✅ Remote commands (LOCATION, STATUS, HELP) functional
✅ Non-blocking multitasking — GPS + GSM concurrent
✅ Full system cost under 2.5k₹


📚 Reference
Project reference:
ShahbazCoder1/GPS-Vehicle-Tracker

👥 Team
Name
Roll No
Shubham Sharma
50
Rohan Thok
54
Parth Wagh
56
Sahil Kurzekar
31


👤 Author
Shubham Sharma
B.Tech Electronics and Communication Engineering
Matoshri College of Engineering, Nashik | CGPA: 7.91

(https://linkedin.com/in/shubham-sharma-192b32341)
