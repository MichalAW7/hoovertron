# main.py
import sys
import asyncio
import qasync
from PyQt5 import QtWidgets
from hoover_logic import HooverTronWindow

# import pyi_splash #uncomment this line and execution in main when creating distributable with a splash screen

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    
    # Create event loop for async BLE operations
    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)
    
    MainWindow = HooverTronWindow()
    MainWindow.show()
    # pyi_splash.close()
    
    with loop:
        loop.run_forever()