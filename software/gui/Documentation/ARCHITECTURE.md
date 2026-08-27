# HooverTron BLE Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    HooverTron BLE System                     │
└─────────────────────────────────────────────────────────────┘

┌──────────────────────┐         WIRELESS          ┌──────────────────────┐
│   Arduino Nano 33    │◄────────  BLE  ──────────►│   Python Application │
│        BLE           │      (~10-30 meters)       │      (PyQt5)         │
└──────────────────────┘                            └──────────────────────┘
         │                                                      │
         │ Reads Sensors                                       │ Displays
         ▼                                                      ▼
┌──────────────────────┐                            ┌──────────────────────┐
│  Force Sensors       │                            │  Real-time Graphs    │
│  - Sensor 1 (A0)     │                            │  - Extension Force   │
│  - Sensor 2 (A1)     │                            │  - Voluntary Force   │
└──────────────────────┘                            │  - Involuntary Force │
                                                     │  - Data Analysis     │
                                                     │  - Database          │
                                                     └──────────────────────┘
```

## Data Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                          Data Processing Pipeline                    │
└─────────────────────────────────────────────────────────────────────┘

ARDUINO SIDE:
─────────────
1. Analog Read (A0, A1)
   ▼
2. 12-bit ADC Conversion (0-4095)
   ▼
3. Voltage Scaling (5V equivalent)
   ▼
4. Force Calibration (Exponential formula)
   ▼
5. Digital Filtering (Alpha/Beta filter)
   ▼
6. Format as CSV String
   ▼
7. BLE Transmission (Notify)
   │
   │  <<< WIRELESS BLUETOOTH >>>
   │
   ▼

PYTHON SIDE:
────────────
8. BLE Notification Received
   ▼
9. Data Buffering
   ▼
10. Parse CSV String
    ▼
11. Update Data Arrays
    ▼
12. Update Real-time Graphs
    ▼
13. Calculate Statistics
    ▼
14. Save to Database/File
```

## BLE Communication

```
┌─────────────────────────────────────────────────────────────────────┐
│                      Bluetooth Low Energy (BLE)                      │
└─────────────────────────────────────────────────────────────────────┘

SERVICE: "180D"
├── CHARACTERISTIC: "2A37"
    ├── Properties: READ | NOTIFY
    ├── Max Size: 64 bytes
    ├── Data Format: "Time,Force1,Force2,FilteredForce1"
    └── Update Rate: ~100 Hz (every 10ms)

CONNECTION FLOW:
─────────────────
Arduino                             Python App
   │                                    │
   │ 1. BLE.begin()                     │
   │ 2. Set name "HooverTron"           │
   │ 3. Advertise service               │
   │                                    │
   │              ◄─────────────── 4. Scan for devices
   │              ──────────────► 5. Device found!
   │              ◄─────────────── 6. Connect request
   │ 7. Connection accepted             │
   │              ──────────────► 8. Start notifications
   │                                    │
   │ 9. Loop: read sensors              │
   │ 10. Send data via BLE              │
   │              ──────────────► 11. Receive notification
   │                                 12. Process & display
   │                                    │
   │ (continuous data stream...)        │
   │              ──────────────►       │
   │              ──────────────►       │
   │                                    │
   │              ◄─────────────── 13. Disconnect request
   │ 14. Close connection               │
```

## Component Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                           Arduino Firmware                           │
└─────────────────────────────────────────────────────────────────────┘

LIBRARIES:
- ArduinoBLE.h          → Bluetooth communication

MAIN COMPONENTS:
- BLEService            → Container for characteristics
- BLECharacteristic     → Data channel
- Sensor Reading        → analogRead() from A0, A1
- Digital Filter        → First-order filter implementation
- Data Formatting       → CSV string builder

LOOP CYCLE (every 10ms):
1. Check for BLE connection
2. Read sensors
3. Apply calibration
4. Apply filtering
5. Format data
6. Transmit via BLE


┌─────────────────────────────────────────────────────────────────────┐
│                        Python Application                            │
└─────────────────────────────────────────────────────────────────────┘

LIBRARIES:
- PyQt5                 → GUI framework
- bleak                 → BLE communication
- qasync                → Async/await with PyQt5
- numpy                 → Data processing
- matplotlib            → Plotting

MAIN COMPONENTS:
- HooverTronWindow      → Main application class
- BleakClient           → BLE connection handler
- BleakScanner          → Device discovery
- UI Layout             → PyQt5 GUI elements
- Data Arrays           → Force and time data storage
- File I/O              → CSV and config management
- Database Manager      → Patient data storage

EVENT LOOP:
- QEventLoop (qasync)   → Handles both GUI and async BLE events
```

## File Organization

```
AntiGravity/
├── Arduino Firmware
│   └── HVR_code_BLE_V1/
│       └── HVR_code_BLE_V1.ino      ← BLE-enabled firmware
│
├── Python Application
│   ├── main.py                       ← Entry point (async event loop)
│   ├── hoover_logic.py               ← BLE logic + data processing
│   ├── ui_layout.py                  ← GUI definition
│   └── config.py                     ← Configuration paths
│
├── Setup & Dependencies
│   ├── requirements.txt              ← Python packages
│   └── install_dependencies.bat      ← Windows installer
│
└── Documentation
    ├── README_BLE.md                 ← Full documentation
    ├── QUICK_START.md                ← Getting started guide
    ├── CHANGES_SUMMARY.md            ← What changed
    └── ARCHITECTURE.md               ← This file
```

## Key Design Decisions

### Why These UUIDs?
- **Service 180D**: Standard "Heart Rate" service UUID
  - Chosen for compatibility and simplicity
  - Repurposed for sensor data transmission
  
- **Characteristic 2A37**: Standard "Heart Rate Measurement"
  - READ | NOTIFY properties
  - Perfect for continuous data streaming

### Why bleak Library?
- Cross-platform (Windows, macOS, Linux)
- Modern async/await API
- Well-maintained and documented
- Native OS BLE stack integration

### Why qasync?
- Bridges asyncio and PyQt5
- Allows async BLE operations without blocking GUI
- Clean integration of both event loops

### Why Keep Serial?
- Debugging during development
- Firmware verification
- Troubleshooting sensor issues
- Future diagnostics

## Performance Characteristics

**Latency:**
- BLE notification delay: ~10-20ms
- Processing time: <1ms
- GUI update rate: ~100 Hz
- Total system latency: ~20-30ms

**Throughput:**
- Data packet size: ~30 bytes
- Update frequency: 100 Hz
- Bandwidth usage: ~3 KB/s
- BLE capacity: Up to 1 MB/s

**Range:**
- Indoor: 10-15 meters
- Outdoor: 20-30 meters
- Through walls: 5-10 meters

**Power Consumption:**
- BLE transmission: ~15 mA
- Sensor reading: ~5 mA
- Microcontroller: ~10 mA
- **Total: ~30 mA** (can run on battery)

## Security Considerations

**Current Implementation:**
- No encryption (open connection)
- No authentication required
- Any device can connect

**Future Enhancements:**
- Pairing/bonding support
- Encrypted characteristic
- Password protection
- MAC address filtering

## Comparison: Serial vs BLE

```
┌──────────────────┬────────────────────┬────────────────────┐
│    Feature       │    Serial/USB      │        BLE         │
├──────────────────┼────────────────────┼────────────────────┤
│ Connection       │ Wired (USB cable)  │ Wireless (BLE)     │
│ Range            │ <5 meters          │ 10-30 meters       │
│ Mobility         │ Tethered           │ Free movement      │
│ Power            │ USB powered        │ Battery possible   │
│ Latency          │ <5ms               │ ~20ms              │
│ Bandwidth        │ 115200 baud        │ ~1 Mbps            │
│ Setup            │ COM port selection │ Auto-discovery     │
│ Reliability      │ Very high          │ High               │
│ Interference     │ None               │ Possible (rare)    │
│ Multiple devices │ Complex            │ Easier             │
└──────────────────┴────────────────────┴────────────────────┘
```

## Future Expansion Possibilities

1. **Multiple Sensors:**
   - Connect multiple Arduino units
   - Synchronized data collection
   - Comparative analysis

2. **Mobile App:**
   - iOS/Android application
   - Tablet-based interface
   - Cloud data sync

3. **Data Analytics:**
   - Machine learning integration
   - Pattern recognition
   - Automated diagnostics

4. **Remote Monitoring:**
   - WiFi gateway
   - Internet connectivity
   - Remote expert consultation

5. **Enhanced Features:**
   - Battery level indicator
   - Signal strength display
   - Automatic reconnection
   - Data logging on Arduino

## Conclusion

The BLE implementation provides a modern, wireless solution while maintaining 100% functional compatibility with the original serial-based system. The modular architecture allows for easy future enhancements and expansions.
