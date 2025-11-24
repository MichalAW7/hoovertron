# hoover_logic.py
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox
from ui_layout import Ui_Layout
from add_ble_device import AddBleDevice
from hoover_backend.ble_mixin import BleMixin
from hoover_backend.serial_mixin import SerialMixin
from hoover_backend.file_mixin import FileMixin
from hoover_backend.data_mixin import DataMixin
from hoover_backend.settings_mixin import SettingsMixin

class HooverTronWindow(QtWidgets.QMainWindow, Ui_Layout, BleMixin, SerialMixin, FileMixin, DataMixin, SettingsMixin):
    def __init__(self):
        super().__init__()
        
        # Initialize state variables
        self.ble_device = None
        self.ble_client = None
        self.is_connected = False
        self.is_recording = False
        self.data_buffer = ""
        self.currentFrequency = 10  # Default frequency
        
        # File paths
        self.patientDataFile = ''
        self.dataBaseFile = ''
        self.testNumber = 1
        self.isNewDatabase = True
        
        # Data arrays for steps
        self.timeData = [0]
        self.hsS1RForce = [0]
        self.hsS2RForce = [0]
        self.hsS2RAverage = [0]
        self.hsS3RForce = [0]
        self.hsS3RAverage = [0]
        
        # Setup UI
        self.setupUi(self)
        
        # Setup Serial
        self.setup_serial()
        
        # Load configuration
        self.load_config()
        
    def valgAfComport(self, port_name):
        """Handle Serial Port selection"""
        # If BLE is connected, disconnect it? Or just switch?
        if self.is_connected and self.connection_type == 'BLE':
             reply = QMessageBox.question(self, 'Switch Connection', 
                                          "BLE is currently connected. Disconnect BLE and switch to Serial?",
                                          QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
             if reply == QMessageBox.Yes:
                 self.disconnect_ble_persistent()
             else:
                 return

        self.connect_serial(port_name)

    def set_filter_frequency(self, frequency):
        if self.connection_type == 'BLE':
            BleMixin.set_filter_frequency(self, frequency)
        elif self.connection_type == 'Serial':
            self.set_filter_frequency_serial(frequency)
        else:
            QMessageBox.warning(self, "Connection Error", "Please connect to a device first.")

    @QtCore.pyqtSlot(bool)
    def on_toggled(self, checked):
        self.pushButton_4.setText("Stop" if checked else "Record")
        self.pushButton_3.setText("Stop" if checked else "Record")
        self.pushButton_2.setText("Stop" if checked else "Record")

        if checked:
            if not self.is_connected:
                QMessageBox.warning(self, "Connection Error", "Please connect to a device first (BLE or Serial).")
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

            try:
                self.extensionForceLineEdit.setText(str(max(self.hsS1RForce)))
                self.strongLegAverageStrengthLineEdit_2.setText(str(max(self.hsS2RAverage)))
                self.strongLegPeakStrengthLineEdit_2.setText(str(max(self.hsS2RForce)))
                self.weakLegPeakStrengthLineEdit_3.setText(str(max(self.hsS3RForce)))
            except ValueError:
                pass # Handle empty arrays
