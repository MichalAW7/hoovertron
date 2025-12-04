# hoover_backend/constants.py
import os

# Define the config file name/path directly here. 
# This assumes 'config.ini' is located in the folder where you run main.py
CONFIG_FILE_PATH = 'config.ini'

# BLE UUIDs (must match Arduino firmware)
SERVICE_UUID = "180D"
CHARACTERISTIC_UUID = "2A37"