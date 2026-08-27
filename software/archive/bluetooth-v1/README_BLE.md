# HooverTron BLE Implementation

## Overview
This project has been updated to use **Bluetooth Low Energy (BLE)** for wireless communication between the Arduino Nano 33 BLE and the Python application, replacing the previous serial (COM port) communication.

## Changes Made

### Arduino Firmware (`HVR_code_BLE_V1.ino`)
- **Added BLE Support**: Integrated the ArduinoBLE library for wireless communication
- **BLE Service**: Custom service UUID `180D` for sensor data
- **BLE Characteristic**: Custom characteristic UUID `2A37` with Read and Notify properties
- **Data Transmission**: Sensor data is now transmitted via BLE notifications instead of Serial
- **Device Name**: The Arduino advertises as "HooverTron" for easy identification
- **Maintained Functionality**: All sensor reading, filtering, and data processing logic remains unchanged

### Python Application (`hoover_logic.py`)
- **Removed Serial Communication**: Replaced `QtSerialPort` with BLE using the `bleak` library
- **Async/Await Pattern**: Implemented asynchronous BLE operations for non-blocking communication
- **BLE Scanner**: Automatically scans and connects to "HooverTron" device
- **Notification Handler**: Receives data from Arduino via BLE notifications
- **Data Buffer**: Implements buffering to handle fragmented BLE packets
- **Maintained UI**: All existing UI functionality remains exactly the same
- **Error Handling**: Added robust error handling for BLE connection issues

### Main Entry Point (`main.py`)
- **Event Loop**: Integrated `qasync` to enable async operations within PyQt5
- **BLE Support**: Set up proper async event loop for BLE operations

## Installation

### 1. Arduino Setup
1. Open `HVR_code_BLE_V1/HVR_code_BLE_V1.ino` in Arduino IDE
2. Install the **ArdulinoBLE** library:
   - Go to `Sketch` → `Include Library` → `Manage Libraries`
   - Search for "ArduinoBLE"
   - Install the library by Arduino
3. Select your **Arduino Nano 33 BLE** board:
   - Go to `Tools` → `Board` → `Arduino Mbed OS Nano Boards` → `Arduino Nano 33 BLE`
4. Upload the sketch to your Arduino Nano 33 BLE

### 2. Python Setup
Install the required dependencies:
```bash
pip install -r requirements.txt
```

The main dependencies are:
- **bleak**: Python BLE library for cross-platform Bluetooth communication
- **qasync**: Integration layer for asyncio and PyQt5
- **PyQt5**: GUI framework
- **numpy & matplotlib**: Data processing and visualization

## Usage

### 1. Power On the Arduino
- Connect the Arduino Nano 33 BLE to a power source (USB or battery)
- The device will start advertising as "HooverTron"
- The onboard LED may blink to indicate BLE is active

### 2. Run the Python Application
```bash
python main.py
```

### 3. Connect to the Device
1. Click the **Record** button in the application
2. The app will automatically scan for the "HooverTron" device
3. Once found, it will connect and start receiving data
4. The button will change to **Stop** when connected
5. Click **Stop** to disconnect

### 4. If Connection Fails
- Ensure the Arduino is powered on and nearby (within BLE range, ~10 meters)
- Make sure no other application is connected to the Arduino
- Check that Bluetooth is enabled on your computer
- Try restarting both the Arduino and the Python application

## Technical Details

### BLE UUIDs
- **Service UUID**: `180D` (Heart Rate Service - repurposed for sensor data)
- **Characteristic UUID**: `2A37` (Heart Rate Measurement - repurposed for sensor data)

### Data Format
Data is transmitted in the same CSV format as before:
```
Time,Force1,Force2,FilteredForce1
```

Example:
```
10523,2.456,1.234,2.123
```

### BLE Data Transmission
- **Packet Size**: Up to 64 bytes per notification
- **Update Rate**: Approximately every 10ms (100 Hz)
- **Range**: Typical BLE range is 10-30 meters depending on environment

## Advantages of BLE over Serial

1. **Wireless**: No USB cable required
2. **Mobility**: The Arduino can be battery-powered and portable
3. **Multiple Connections**: Potentially connect to multiple devices (future enhancement)
4. **Lower Power**: BLE is designed for low power consumption
5. **Modern Standard**: BLE is widely supported across devices

## Troubleshooting

### Arduino Won't Upload
- Make sure you've selected the correct board: `Arduino Nano 33 BLE`
- Ensure the USB cable supports data transfer (not power-only)
- Try pressing the reset button twice quickly to enter bootloader mode

### Python App Can't Find Device
- Check that the Arduino sketch is uploaded and running
- Verify Bluetooth is enabled on your computer
- Ensure you're within BLE range (~10 meters)
- Try running the scan with elevated privileges (admin/sudo)

### Data Not Appearing
- Check the sensor connections to pins A0 and A1
- Verify the calibration formulas are appropriate for your sensors
- Monitor the Arduino Serial output (115200 baud) for debugging info

### BLE Connection Drops
- Reduce distance between Arduino and computer
- Minimize interference from other wireless devices
- Ensure Arduino has stable power supply

## Future Enhancements

Potential improvements for future versions:
- Add battery level monitoring
- Implement automatic reconnection
- Support multiple simultaneous sensor units
- Add data encryption for secure transmission
- Implement configuration via BLE (e.g., filter frequency)

## Notes

- The Serial communication in the Arduino code is kept for debugging purposes
- The Python app maintains backward compatibility with the file format
- All existing features (file save/load, database, graphs) work exactly as before
- Only the communication layer has changed from Serial to BLE

## Support

For issues or questions, please ensure:
1. You're using Arduino Nano 33 BLE (not other Nano variants)
2. The ArduinoBLE library is properly installed
3. Python dependencies are installed: `pip install -r requirements.txt`
4. Your operating system supports BLE (Windows 10+, macOS 10.15+, Linux with BlueZ)
