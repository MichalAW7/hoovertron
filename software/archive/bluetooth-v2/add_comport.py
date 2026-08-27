# add_comport.py
import serial
from PyQt5.QtWidgets import QMainWindow, QAction
from PyQt5.QtSerialPort import QSerialPortInfo
from PyQt5.QtCore import pyqtSignal

class AddComport(QMainWindow):
    porttnavn = pyqtSignal(str)

    def __init__(self, parent, menu):
        super().__init__(parent)

        menuComPort = menu.addMenu("COM Port")

        info_list = QSerialPortInfo()
        serial_list = info_list.availablePorts()
        serial_ports = [port.portName() for port in serial_list]
        if (len(serial_ports) > 0):
            antalporte = len(serial_ports)
            antal = 0
            while antal < antalporte:
                txt = serial_ports[antal]
                portinfo = QSerialPortInfo(txt)
                buttoninfotxt = " No Info"
                if portinfo.hasProductIdentifier():
                    buttoninfotxt = ("Product Specification = " + str(portinfo.vendorIdentifier()))
                if portinfo.hasVendorIdentifier():
                    buttoninfotxt = buttoninfotxt + (" Manufacturer ID = " + str(portinfo.productIdentifier()))
                button_action = QAction(txt, self)
                button_action.setStatusTip(buttoninfotxt)
                button_action.triggered.connect(lambda checked, txt=txt: self.valgAfComportClick(txt))
                menuComPort.addAction(button_action)
                antal = antal + 1
        else:
            print("No COM Ports Found")

    def valgAfComportClick(self, port):
        # Brief open/close to test or reset
        try:
            arduino = serial.Serial(port=port, baudrate=19200, timeout=0.1)
            arduino.close()
        except Exception as e:
            print(f"Error checking port {port}: {e}")

        self.porttnavn.emit(port)

    def closeEvent(self, event):
        self.close()