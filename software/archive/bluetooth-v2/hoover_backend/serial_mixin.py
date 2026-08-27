# hoover_backend/serial_mixin.py
import serial
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMessageBox

class SerialMixin:
    def setup_serial(self):
        self.serial_port = None
        self.serial_timer = QtCore.QTimer()
        self.serial_timer.timeout.connect(self.read_serial_data)
        self.connection_type = None # 'BLE' or 'Serial'

    def connect_serial(self, port_name):
        try:
            if self.serial_port and self.serial_port.is_open:
                self.serial_port.close()
            
            self.serial_port = serial.Serial(port_name, 115200, timeout=0.1)
            self.is_connected = True
            self.connection_type = 'Serial'
            self.statusbar.showMessage(f"Connected to {port_name}", 5000)
            print(f"Connected to Serial: {port_name}")
            
            # Start polling
            self.serial_timer.start(10) # 10ms polling
            
            # Update UI state if needed
            # self.ble_manager.update_connection_state(True) # Re-use BLE manager for UI updates?
            
        except Exception as e:
            print(f"Serial connection error: {e}")
            QMessageBox.critical(self, "Error", f"Failed to connect to Serial port: {str(e)}")
            self.is_connected = False
            self.connection_type = None

    def disconnect_serial(self):
        if hasattr(self, 'serial_timer') and self.serial_timer.isActive():
            self.serial_timer.stop()
            
        if hasattr(self, 'serial_port') and self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
            
        if self.connection_type == 'Serial':
            self.is_connected = False
            self.connection_type = None
            self.statusbar.showMessage("Disconnected", 3000)
            print("Disconnected from Serial")

    def read_serial_data(self):
        if not self.is_recording or not self.serial_port or not self.serial_port.is_open:
            return

        try:
            while self.serial_port.in_waiting:
                line = self.serial_port.readline().decode('utf-8', errors='ignore').strip()
                if line:
                    if line.startswith("Frequency updated to:"):
                        print(f"ARDUINO CONFIRMATION >> {line}")
                        continue
                    
                    self.process_incoming_data(line)
        except Exception as e:
            print(f"Serial read error: {e}")

    def set_filter_frequency_serial(self, frequency):
        if self.serial_port and self.serial_port.is_open:
            try:
                command = f"F{frequency}\n"
                self.serial_port.write(command.encode())
                self.currentFrequency = frequency
                self.statusbar.showMessage(f"Filter frequency set to {frequency} Hz", 3000)
                print(f"Filter frequency changed to {frequency} Hz (Serial)")
            except Exception as e:
                print(f"Error setting frequency via Serial: {e}")
