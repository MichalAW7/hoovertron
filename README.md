# Hoovertron: A Device for the Quantitative Measurement of Hoover's Sign

This repository contains the complete design files and software for the Hoovertron, a portable, floor-based device for the standardised, quantitative measurement of Hoover's sign. It provides a reliable, objective tool to aid diagnosis of functional leg weakness, a common feature of Functional Neurological Disorder (FND).

Based on: *Quantitative Measurement of Hoover's sign: development of a standardised sensor, interface procedure and testing in healthy individuals*.

## Repository Structure

```
hoovertron/
├── hardware/
│   ├── mechanical/          # SolidEdge source + STL/3MF/GCODE exports
│   │   ├── source/v1-main-part/
│   │   ├── source/v2-revised/
│   │   └── exports/{stl,3mf,gcode}/
│   └── pcb/
│       ├── src/             # Altium Designer source (SchDoc, PcbDoc, SchLib, PcbLib, PrjPcb)
│       └── outputs/         # Gerbers / CAM (generated, gitignored)
├── firmware/
│   ├── HVR_code_BLE_V3/     # Canonical Arduino Nano 33 BLE firmware (latest, with dummy-load fix)
│   └── archive/
│       ├── HVR_code_BLE_V2/ # Previous BLE version
│       ├── HVR_code_BLE_V1/
│       ├── HVR_code_v5/
│       └── FND_code_v4/
├── software/
│   ├── gui/                 # Canonical desktop GUI (Python + PyQt5 + bleak)
│   │   ├── main.py
│   │   ├── hoover_logic.py, ui_layout.py, config.py
│   │   ├── hoover_backend/  # ble_mixin, data_mixin, file_mixin, serial_mixin
│   │   ├── ui_components/   # menu_bar, patient_tab, results_tab, step_tabs
│   │   ├── images/
│   │   ├── Documentation/   # ARCHITECTURE, QUICK_START, etc.
│   │   ├── requirements.txt
│   │   └── HooverTron.spec / compile_app.bat
│   └── archive/
│       ├── bluetooth-v1/    # Legacy single-file BLE prototype
│       ├── bluetooth-v2/    # Pre-stylesheet modular version
│       └── gui-monolith/    # HooverTron.py monolith (pre-modular)
├── docs/
│   ├── manual/              # hoovertron_manual.md/.tex, canva_prompt.md
│   ├── images/              # Consolidated screenshots/infographics
│   └── screenshots/
├── .gitignore
└── LICENSE.md
```

## Hardware

### Mechanical
Custom 3D-printed housing isolates the heel on the sensor. Source in `hardware/mechanical/source/` (SolidEdge `.par`), printable exports in `hardware/mechanical/exports/` (`stl/` for printing, `3mf` for project, `gcode/` for slicer). See `hardware/mechanical/README.md` for print settings.

### Electronics
Custom PCB (Altium) in `hardware/pcb/src/`:
- **MCU:** Arduino Nano 33 BLE (or Nano Every for wired) - data acquisition & BLE/Serial
- **Sensor:** Ohmite FSR01CE force sensing resistor in voltage divider with 180 Ω, buffered via MCP6002 voltage follower, 3x 100nF decoupling/filter
- **Power:** USB or battery pack (V3 firmware pulses D2 with 100-220Ω dummy load to keep pack awake)

Gerber/BOM outputs are in `hardware/pcb/outputs/` (regenerable, ignored by git).

## Firmware

Canonical: `firmware/HVR_code_BLE_V3/HVR_code_BLE_V3.ino` (ArduinoBLE, 12-bit ADC 0-4095, dual-channel A0/A1, exponential force calibration `0.8259*exp(0.8623*V)...`, bilinear LPF `alpha=(2-2π0.001f)/(2+2π0.001f)`, BLE service `180D` char `2A37`, serial `F<freq>` command).

Upload with Arduino IDE (board: Nano 33 BLE, baud 115200).

Legacy versions in `firmware/archive/`.

## Software

### Requirements
```bash
pip install -r software/gui/requirements.txt
# PyQt5>=5.15.0, bleak>=0.20.0, qasync, numpy, matplotlib, pyqtgraph
```

### Run
```bash
python software/gui/main.py
# or build exe:
software/gui/compile_app.bat   # uses HooverTron.spec
```

Features: BLE/Serial connect, real-time force plot (N vs s), region select for max voluntary/involuntary, IV/V ratio, CSV logging.

### Documentation
- `software/gui/Documentation/QUICK_START.md` - install & run
- `software/gui/Documentation/ARCHITECTURE.md` - backend mixins + UI components
- `docs/manual/hoovertron_manual.md` - full manual

## Data Privacy
`patient data.csv` is gitignored. Do not commit patient data. Use anonymized examples only.

## License
MIT - see [LICENSE.md](LICENSE.md)
