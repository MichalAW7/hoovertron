@echo off
echo ========================================
echo HooverTron BLE Setup
echo ========================================
echo.
echo Installing Python dependencies...
echo.

pip install --upgrade pip
pip install -r requirements.txt

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Upload HVR_code_BLE_V1.ino to your Arduino Nano 33 BLE
echo 2. Ensure ArduinoBLE library is installed in Arduino IDE
echo 3. Run: python main.py
echo.
echo For detailed instructions, see README_BLE.md
echo.
pause
