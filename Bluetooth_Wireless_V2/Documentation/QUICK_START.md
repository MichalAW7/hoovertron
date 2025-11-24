# Quick Start Guide - HooverTron BLE

## For First-Time Setup

### Step 1: Arduino Setup (5 minutes)

1. **Open Arduino IDE**

2. **Install ArduinoBLE Library:**
   - Click: `Sketch` → `Include Library` → `Manage Libraries...`
   - Search: "ArduinoBLE"
   - Click: Install on "ArduinoBLE by Arduino"
   - Wait for installation to complete

3. **Select Your Board:**
   - Click: `Tools` → `Board` → `Arduino Mbed OS Nano Boards` → `Arduino Nano 33 BLE`
   - Click: `Tools` → `Port` → Select your COM port

4. **Upload the Firmware:**
   - Open: `HVR_code_BLE_V1/HVR_code_BLE_V1.ino`
   - Click: Upload button (→)
   - Wait for "Done uploading" message

5. **Verify It Works:**
   - Open: `Tools` → `Serial Monitor`
   - Set baud rate: 115200
   - You should see: "BLE device active, waiting for connections..."

### Step 2: Python Setup (2 minutes)

1. **Install Dependencies:**
   - Double-click: `install_dependencies.bat`
   - OR run in terminal: `pip install -r requirements.txt`
   - Wait for installation to complete

### Step 3: Run the Application (30 seconds)

1. **Power the Arduino:**
   - Connect Arduino to USB or battery
   - Blue LED should be on

2. **Start the Application:**
   - Double-click or run: `python main.py`
   - The HooverTron window will open

3. **Connect and Record:**
   - Click the **Record** button
   - Wait 2-5 seconds for BLE connection
   - Button changes to **Stop** when connected
   - Data should appear on the graph

4. **When Finished:**
   - Click **Stop** to disconnect
   - Close the application

## Troubleshooting

### "HooverTron device not found"
- ✅ Check Arduino is powered on
- ✅ Check Arduino uploaded successfully (look for Serial Monitor output)
- ✅ Make sure Bluetooth is enabled on your computer
- ✅ Move Arduino closer to your computer
- ✅ Try restarting the Arduino (unplug and replug)

### "Starting BLE failed!" in Serial Monitor
- ✅ Make sure you selected **Arduino Nano 33 BLE** (not other boards)
- ✅ Re-upload the sketch
- ✅ Try a different USB cable

### Python Import Errors
- ✅ Run: `pip install -r requirements.txt`
- ✅ Make sure you're using Python 3.7+
- ✅ Try: `python --version` to check

### No Data on Graphs
- ✅ Check sensor connections to A0 and A1
- ✅ Verify sensors are powered
- ✅ Check Serial Monitor for raw data output

## Daily Use (After Initial Setup)

1. Power on Arduino
2. Run: `python main.py`
3. Click **Record**
4. Perform tests
5. Click **Stop**
6. Save data if needed

## Features Available

- ✅ Real-time data visualization
- ✅ Three test protocols (Extension, Voluntary, Involuntary)
- ✅ Peak and average force calculations
- ✅ IVVR (Involuntary/Voluntary Ratio) calculation
- ✅ Patient database management
- ✅ Save/Load test data (CSV format)
- ✅ Time period selection for analysis
- ✅ Filter frequency adjustment

## File Structure

```
AntiGravity/
├── HVR_code_BLE_V1/
│   └── HVR_code_BLE_V1.ino    ← Arduino firmware
├── main.py                     ← Run this to start app
├── hoover_logic.py             ← Application logic
├── ui_layout.py                ← UI definition
├── config.py                   ← Configuration
├── requirements.txt            ← Python dependencies
├── install_dependencies.bat    ← Setup script
├── README_BLE.md              ← Full documentation
├── CHANGES_SUMMARY.md         ← What changed
└── QUICK_START.md             ← This file
```

## Getting Help

1. **Check README_BLE.md** - Full documentation with detailed troubleshooting
2. **Check CHANGES_SUMMARY.md** - Understanding what changed from serial version
3. **Check Serial Monitor** - Arduino debugging output at 115200 baud
4. **Check Console Output** - Python debugging information

## System Requirements

**Hardware:**
- Arduino Nano 33 BLE (required)
- Computer with Bluetooth 4.0+ support
- Force sensors connected to A0 and A1

**Software:**
- Windows 10+, macOS 10.15+, or Linux with BlueZ
- Python 3.7 or higher
- Arduino IDE 1.8.10 or higher

## Quick Reference

**BLE Connection:**
- Device Name: "HooverTron"
- Service UUID: 180D
- Characteristic UUID: 2A37
- Typical Range: 10-30 meters

**Data Format:**
- CSV: `Time,Force1,Force2,FilteredForce1`
- Update Rate: ~100 Hz (every 10ms)
- ADC Resolution: 12-bit (0-4095)

**Sensors:**
- Input Pins: A0 (Sensor 1), A1 (Sensor 2)
- Voltage Range: 0-3.3V
- Calibration: Exponential formula applied

## That's It!

You're ready to use the HooverTron BLE system. The wireless connection provides freedom of movement while maintaining all the functionality of the original system.

**Happy Testing! 🔬📊**
