# hoover_backend/ble_mixin.py
import asyncio
from bleak import BleakClient
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMessageBox
from .constants import CHARACTERISTIC_UUID

class BleMixin:
    def on_ble_device_selected(self, device):
        self.ble_device = device
        print(f"Device selected in logic: {device.name}")

    def connect_ble_persistent(self):
        asyncio.ensure_future(self.connect_ble())

    def disconnect_ble_persistent(self):
        asyncio.ensure_future(self.disconnect_ble())

    async def connect_ble(self):
        """Connect to the BLE device"""
        if not self.ble_device:
            QMessageBox.warning(self, "Error", "No device selected. Please scan and select a device first.")
            return

        try:
            print(f"Connecting to {self.ble_device.name}...")
            
            # Connect to the device
            self.ble_client = BleakClient(self.ble_device)
            await self.ble_client.connect()
            
            if self.ble_client.is_connected:
                print(f"Connected to {self.ble_device.name}")
                self.is_connected = True
                self.ble_manager.update_connection_state(True)
                self.statusbar.showMessage(f"Connected to {self.ble_device.name}", 5000)
                
                # Start notifications
                await self.ble_client.start_notify(CHARACTERISTIC_UUID, self.notification_handler)
                print("Notifications started")
            else:
                QMessageBox.critical(self, "Error", "Failed to connect to HooverTron")
                self.ble_manager.update_connection_state(False)
                
        except Exception as e:
            print(f"BLE connection error: {e}")
            QMessageBox.critical(self, "Error", f"Failed to connect to BLE device: {str(e)}")
            self.ble_manager.update_connection_state(False)

    async def disconnect_ble(self):
        """Disconnect from the BLE device"""
        try:
            if self.ble_client and self.ble_client.is_connected:
                # Stop notifications
                await self.ble_client.stop_notify(CHARACTERISTIC_UUID)
                await self.ble_client.disconnect()
                print("Disconnected from BLE device")
                self.is_connected = False
                self.is_recording = False # Ensure recording stops
                self.ble_manager.update_connection_state(False)
                self.statusbar.showMessage("Disconnected", 3000)
                
                # Reset buttons if they were recording
                self.pushButton_2.setChecked(False)
                self.pushButton_3.setChecked(False)
                self.pushButton_4.setChecked(False)
        except Exception as e:
            print(f"BLE disconnection error: {e}")

    def notification_handler(self, sender, data):
        """Handle BLE notifications from the Arduino"""
        if not self.is_recording:
            return

        try:
            text = data.decode('utf-8', errors='ignore').strip()
            
            # Add to buffer
            self.data_buffer += text
            
            # Process complete lines (ending with newline or complete data packet)
            if ',' in self.data_buffer:
                # Extract complete message
                text_to_process = self.data_buffer
                self.data_buffer = ""
                
                if not text_to_process:
                    return

                if text_to_process.startswith("Frequency updated to:"):
                    print(f"ARDUINO CONFIRMATION >> {text_to_process}")
                    return

                self.process_incoming_data(text_to_process)

        except (ValueError, IndexError) as e:
            print(f"Error processing BLE data: {e}")
            pass

    @QtCore.pyqtSlot(bool)
    def on_toggled(self, checked):
        self.pushButton_4.setText("Stop" if checked else "Record")
        self.pushButton_3.setText("Stop" if checked else "Record")
        self.pushButton_2.setText("Stop" if checked else "Record")

        if checked:
            if not self.is_connected:
                QMessageBox.warning(self, "Connection Error", "Please connect to a BLE device first via the Edit -> BLE Device menu.")
                # Uncheck buttons to reset state
                self.pushButton_2.setChecked(False)
                self.pushButton_3.setChecked(False)
                self.pushButton_4.setChecked(False)
                return
            
            print("Starting recording...")
            self.is_recording = True
        else:
            print("Stopping recording...")
            self.is_recording = False

            self.extensionForceLineEdit.setText(str(max(self.hsS1RForce)))
            self.strongLegAverageStrengthLineEdit_2.setText(str(max(self.hsS2RAverage)))
            self.strongLegPeakStrengthLineEdit_2.setText(str(max(self.hsS2RForce)))
            self.weakLegPeakStrengthLineEdit_3.setText(str(max(self.hsS3RForce)))

    def valgAfComport(self, nyport):
        """Legacy COM port selection - now used for BLE device selection"""
        print(f"BLE device selection: {nyport}")

    async def set_filter_frequency_async(self, frequency):
        """Send filter frequency update via BLE"""
        if self.ble_client and self.ble_client.is_connected:
            try:
                command = f"F{frequency}\n"
                await self.ble_client.write_gatt_char(CHARACTERISTIC_UUID, command.encode())
                self.currentFrequency = frequency
                self.statusbar.showMessage(f"Filter frequency set to {frequency} Hz", 3000)
                print(f"Filter frequency changed to {frequency} Hz")
            except Exception as e:
                print(f"Error setting frequency: {e}")
        else:
            QMessageBox.warning(self, "Connection Error", 
                            "Please connect to BLE device before changing filter frequency")

    def set_filter_frequency(self, frequency):
        """Wrapper for async frequency setting"""
        asyncio.ensure_future(self.set_filter_frequency_async(frequency))