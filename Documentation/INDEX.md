# 📡 HooverTron BLE - Documentation Index

Welcome to the HooverTron Bluetooth Low Energy implementation! This index will guide you to the right documentation for your needs.

---

## 🚀 Getting Started (First Time Users)

**Start Here → [QUICK_START.md](QUICK_START.md)**
- Step-by-step setup instructions
- Arduino firmware upload guide
- Python installation
- First connection tutorial
- Basic troubleshooting

**Estimated Time:** 10-15 minutes

---

## 📚 Documentation Guide

### For Users

| Document | Purpose | When to Read |
|----------|---------|--------------|
| **[QUICK_START.md](QUICK_START.md)** | Quick setup & usage | First time setup |
| **[README_BLE.md](README_BLE.md)** | Complete user manual | Detailed information needed |
| **Troubleshooting** (in README_BLE.md) | Fix common issues | When things don't work |

### For Developers

| Document | Purpose | When to Read |
|----------|---------|--------------|
| **[ARCHITECTURE.md](ARCHITECTURE.md)** | System design & data flow | Understanding the system |
| **[CHANGES_SUMMARY.md](CHANGES_SUMMARY.md)** | What changed from serial | Migration from old version |
| **Code files** | Implementation details | Modifying the code |

---

## 📁 File Structure & Purpose

### Arduino Firmware
```
HVR_code_BLE_V1/
└── HVR_code_BLE_V1.ino         Arduino code with BLE support
```

### Python Application
```
main.py                          Entry point - run this to start
hoover_logic.py                  BLE communication & data processing  
ui_layout.py                     GUI interface definition
config.py                        Configuration file paths
add_comport.py                   Legacy COM port utilities
```

### Setup Scripts
```
requirements.txt                 Python dependencies list
install_dependencies.bat         Windows installer script
```

### Documentation
```
INDEX.md                         This file - start here
QUICK_START.md                   Fast setup guide
README_BLE.md                    Complete documentation
ARCHITECTURE.md                  Technical design details
CHANGES_SUMMARY.md               Migration guide
```

---

## 🎯 Common Tasks

### "I want to set this up for the first time"
→ Read **[QUICK_START.md](QUICK_START.md)**

### "Something isn't working"
→ Check **Troubleshooting** section in **[README_BLE.md](README_BLE.md)**

### "I need to understand how BLE communication works"
→ Read **[ARCHITECTURE.md](ARCHITECTURE.md)**

### "I'm upgrading from the serial version"
→ Read **[CHANGES_SUMMARY.md](CHANGES_SUMMARY.md)**

### "I want to modify the code"
→ Read **[ARCHITECTURE.md](ARCHITECTURE.md)** first, then examine the code files

### "I need installation help"
→ Run **install_dependencies.bat** OR see Setup sections in **[QUICK_START.md](QUICK_START.md)**

### "I want to know what's different from before"
→ Read **[CHANGES_SUMMARY.md](CHANGES_SUMMARY.md)**

---

## ⚡ Quick Reference

### System Requirements
- **Hardware:** Arduino Nano 33 BLE + Bluetooth 4.0+ computer
- **Software:** Python 3.7+ | Arduino IDE 1.8.10+
- **OS:** Windows 10+, macOS 10.15+, or Linux with BlueZ

### Key Information
- **Device Name:** HooverTron
- **BLE Service UUID:** 180D
- **BLE Characteristic UUID:** 2A37
- **Data Format:** `Time,Force1,Force2,FilteredForce1`
- **Update Rate:** ~100 Hz (every 10ms)
- **Range:** 10-30 meters

### Installation Commands
```bash
# Python dependencies
pip install -r requirements.txt

# Or use the batch script (Windows)
install_dependencies.bat
```

### Running the Application
```bash
python main.py
```

---

## 📖 Reading Order Recommendations

### For First-Time Users:
1. **QUICK_START.md** - Get up and running
2. **README_BLE.md** - Learn all features
3. **CHANGES_SUMMARY.md** - See what's new (if coming from serial version)

### For Developers:
1. **CHANGES_SUMMARY.md** - Understand modifications
2. **ARCHITECTURE.md** - Learn system design
3. **Code files** - Examine implementation
4. **README_BLE.md** - User perspective

### For Troubleshooting:
1. **QUICK_START.md** - Basic troubleshooting
2. **README_BLE.md** - Detailed troubleshooting
3. **ARCHITECTURE.md** - Technical debugging

---

## 🔧 Technical Specifications

### Arduino Side
- **Board:** Arduino Nano 33 BLE
- **Library:** ArduinoBLE (by Arduino)
- **ADC Resolution:** 12-bit (0-4095)
- **Sampling Rate:** 100 Hz
- **BLE Role:** Peripheral (server)

### Python Side
- **Framework:** PyQt5
- **BLE Library:** bleak
- **Async Integration:** qasync
- **Data Processing:** numpy, matplotlib
- **BLE Role:** Central (client)

---

## 📞 Support Resources

### Included Documentation
- All troubleshooting steps in README_BLE.md
- Architecture diagrams in ARCHITECTURE.md
- Setup procedures in QUICK_START.md
- Change details in CHANGES_SUMMARY.md

### Code Comments
- Arduino firmware has inline comments
- Python code has docstrings and comments
- Both explain key algorithms and BLE operations

### Serial Debugging
- Arduino Serial Monitor (115200 baud)
- Python console output
- Both provide real-time debugging information

---

## ✨ What Makes This Special

### Key Features
✅ **Wireless Freedom** - No USB cables required  
✅ **Real-time Data** - 100 Hz update rate  
✅ **Long Range** - Up to 30 meters  
✅ **Low Power** - Battery operation possible  
✅ **Auto-Discovery** - No manual device selection  
✅ **Full Compatibility** - All original features preserved  

### What Changed
🔄 Communication: Serial → BLE  
🔄 Connection: Wired → Wireless  

### What Stayed The Same
✓ All data processing  
✓ All UI elements  
✓ All file operations  
✓ All graphing features  
✓ All patient management  
✓ All calculations  

---

## 📝 Version Information

**Version:** BLE v1.0  
**Date:** November 2025  
**Hardware:** Arduino Nano 33 BLE  
**Communication:** Bluetooth Low Energy 4.0+  

**Previous Version:** Serial/USB based  
**Migration Path:** See CHANGES_SUMMARY.md  

---

## 🎓 Learning Path

### Beginner
1. ✅ Setup (QUICK_START.md)
2. ✅ Basic usage (README_BLE.md - Usage section)
3. ✅ Troubleshooting basics (QUICK_START.md)

### Intermediate
1. ✅ Full features (README_BLE.md)
2. ✅ Understanding changes (CHANGES_SUMMARY.md)
3. ✅ Basic modifications (code files)

### Advanced
1. ✅ System architecture (ARCHITECTURE.md)
2. ✅ BLE protocol details (ARCHITECTURE.md)
3. ✅ Code modifications (all source files)
4. ✅ Custom enhancements (extend the system)

---

## 🚦 Status Indicators

### Arduino
- **Serial Output:** "BLE device active, waiting for connections..."
  - ✅ BLE initialized successfully
  
- **Serial Output:** "Connected to central: [MAC]"
  - ✅ Python app connected

### Python Application
- **Console:** "Scanning for HooverTron device..."
  - 🔍 Searching for Arduino
  
- **Console:** "Connected to HooverTron"
  - ✅ Connection established
  
- **Console:** "Notifications started"
  - ✅ Data streaming active

---

## 🎯 Remember

**👉 Start with [QUICK_START.md](QUICK_START.md) if this is your first time!**

**👉 Check [README_BLE.md](README_BLE.md) for comprehensive documentation!**

**👉 Read [ARCHITECTURE.md](ARCHITECTURE.md) to understand the system design!**

---

Happy Testing! 🔬📊🚀
