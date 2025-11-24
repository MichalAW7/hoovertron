# add_ble_device.py
import asyncio
from PyQt5.QtWidgets import QMainWindow, QAction, QActionGroup
from PyQt5.QtCore import pyqtSignal, QObject
from bleak import BleakScanner

class AddBleDevice(QMainWindow):
    device_selected = pyqtSignal(object)  # Signal emits the selected BLE device
    connect_requested = pyqtSignal()
    disconnect_requested = pyqtSignal()
    
    def __init__(self, parent, menu):
        super().__init__(parent)
        self.parent_window = parent
        self.ble_devices = []
        self.hoovertron_device = None  # Store hoovertron device if found
        self.menuBLE = menu.addMenu("Bluetooth")
        
        # Add Scan action
        self.actionScanBLE = QAction("Scan for Devices", self)
        self.actionScanBLE.setStatusTip("Scan for available BLE devices")
        self.actionScanBLE.triggered.connect(self.scan_devices)
        self.menuBLE.addAction(self.actionScanBLE)
        
        self.menuBLE.addSeparator()
        
        # Add Connect/Disconnect actions
        self.actionConnectBLE = QAction("Connect", self)
        self.actionConnectBLE.setStatusTip("Connect to selected BLE device")
        self.actionConnectBLE.setEnabled(False)
        self.actionConnectBLE.triggered.connect(self.request_connect)
        self.menuBLE.addAction(self.actionConnectBLE)
        
        self.actionDisconnectBLE = QAction("Disconnect", self)
        self.actionDisconnectBLE.setStatusTip("Disconnect from BLE device")
        self.actionDisconnectBLE.setEnabled(False)
        self.actionDisconnectBLE.triggered.connect(self.request_disconnect)
        self.menuBLE.addAction(self.actionDisconnectBLE)
        
        self.menuBLE.addSeparator()
        
        # Device list section
        self.device_action_group = QActionGroup(self)
        self.device_action_group.setExclusive(True)
        
        # Initial automatic scan for hoovertron device
        asyncio.ensure_future(self.auto_scan_and_connect())
    
    def scan_devices(self):
        """Trigger device scan"""
        asyncio.ensure_future(self.scan_devices_async())
    
    async def scan_devices_async(self):
        """Scan for BLE devices asynchronously"""
        try:
            # Clear previous devices
            for action in self.device_action_group.actions():
                self.menuBLE.removeAction(action)
                self.device_action_group.removeAction(action)
            
            self.ble_devices = []
            
            # Update status
            if hasattr(self.parent_window, 'statusbar'):
                self.parent_window.statusbar.showMessage("Scanning for BLE devices...", 2000)
            
            # Scan for devices
            devices = await BleakScanner.discover(timeout=5.0)
            
            if devices:
                for device in devices:
                    # Only show devices with a name (filter out unnamed devices)
                    if device.name:
                        self.ble_devices.append(device)
                        
                        # Create menu item for this device
                        device_action = QAction(f"{device.name} ({device.address})", self)
                        device_action.setCheckable(True)
                        device_action.setStatusTip(f"Select {device.name}")
                        device_action.triggered.connect(
                            lambda checked, dev=device: self.select_device(dev)
                        )
                        
                        self.device_action_group.addAction(device_action)
                        self.menuBLE.addAction(device_action)
                
                if hasattr(self.parent_window, 'statusbar'):
                    self.parent_window.statusbar.showMessage(
                        f"Found {len(self.ble_devices)} BLE device(s)", 3000
                    )
            else:
                if hasattr(self.parent_window, 'statusbar'):
                    self.parent_window.statusbar.showMessage(
                        "No BLE devices found", 3000
                    )
                    
        except Exception as e:
            print(f"Error scanning for BLE devices: {e}")
            if hasattr(self.parent_window, 'statusbar'):
                self.parent_window.statusbar.showMessage(
                    f"Error scanning: {str(e)}", 5000
                )
    
    def select_device(self, device):
        """Handle device selection"""
        print(f"Selected BLE device: {device.name} ({device.address})")
        self.device_selected.emit(device)
        self.actionConnectBLE.setEnabled(True)
        
        if hasattr(self.parent_window, 'statusbar'):
            self.parent_window.statusbar.showMessage(
                f"Selected: {device.name}", 3000
            )
    
    def request_connect(self):
        """Request connection to selected device"""
        self.connect_requested.emit()
    
    def request_disconnect(self):
        """Request disconnection from device"""
        self.disconnect_requested.emit()
    
    def update_connection_state(self, connected):
        """Update menu state based on connection status"""
        self.actionConnectBLE.setEnabled(not connected)
        self.actionDisconnectBLE.setEnabled(connected)
        self.actionScanBLE.setEnabled(not connected)
        
        # Disable device selection when connected
        for action in self.device_action_group.actions():
            action.setEnabled(not connected)
    
    async def auto_scan_and_connect(self):
        """Automatically scan for and connect to hoovertron device"""
        try:
            # Update status
            if hasattr(self.parent_window, 'statusbar'):
                self.parent_window.statusbar.showMessage("Searching for HooverTron device...", 3000)
            
            # Scan for devices
            devices = await BleakScanner.discover(timeout=5.0)
            
            # Look for hoovertron device (case insensitive)
            hoovertron_found = False
            if devices:
                for device in devices:
                    if device.name and 'hoovertron' in device.name.lower():
                        self.hoovertron_device = device
                        hoovertron_found = True
                        
                        # Automatically select this device
                        self.select_device(device)
                        
                        # Add to device list but mark it as the auto-connected one
                        device_action = QAction(f"★ {device.name} ({device.address})", self)
                        device_action.setCheckable(True)
                        device_action.setChecked(True)
                        device_action.setStatusTip(f"Auto-detected device: {device.name}")
                        device_action.triggered.connect(
                            lambda checked, dev=device: self.select_device(dev)
                        )
                        
                        self.device_action_group.addAction(device_action)
                        self.menuBLE.addAction(device_action)
                        self.ble_devices.append(device)
                        
                        if hasattr(self.parent_window, 'statusbar'):
                            self.parent_window.statusbar.showMessage(
                                f"Found HooverTron: {device.name}. Auto-connecting...", 3000
                            )
                        
                        # Automatically trigger connection
                        self.request_connect()
                        break
            
            # If no hoovertron device found, perform regular scan
            if not hoovertron_found:
                if hasattr(self.parent_window, 'statusbar'):
                    self.parent_window.statusbar.showMessage(
                        "HooverTron device not found. Please scan and connect manually.", 5000
                    )
                # Perform regular scan to populate device list
                await self.scan_devices_async()
                        
        except Exception as e:
            print(f"Error in auto-scan: {e}")
            if hasattr(self.parent_window, 'statusbar'):
                self.parent_window.statusbar.showMessage(
                    f"Auto-scan failed: {str(e)}. Please connect manually.", 5000
                )
            # Fall back to regular scan
            await self.scan_devices_async()
