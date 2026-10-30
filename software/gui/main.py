# main.py
import os
import sys
import asyncio
import qasync
from PyQt5 import QtGui, QtWidgets

from config import APP_NAME, get_resource_path
from hoover_logic import HooverTronWindow

# import pyi_splash #uncomment this line and execution in main when creating distributable with a splash screen


def _set_taskbar_app_id():
    """Tell Windows this is a distinct app so the taskbar shows our icon."""
    if sys.platform != "win32":
        return
    try:
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            "Hoovertron.AntiGravity.App"
        )
    except Exception:
        pass


def _load_app_icon():
    icon_path = get_resource_path(os.path.join("images", "hoovertron_ico_file.ico"))
    if not os.path.exists(icon_path):
        return QtGui.QIcon()
    return QtGui.QIcon(icon_path)


if __name__ == "__main__":
    _set_taskbar_app_id()

    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationDisplayName(APP_NAME)

    app_icon = _load_app_icon()
    if not app_icon.isNull():
        app.setWindowIcon(app_icon)

    # Create event loop for async BLE operations
    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)

    MainWindow = HooverTronWindow()
    if not app_icon.isNull():
        MainWindow.setWindowIcon(app_icon)
    MainWindow.show()
    # pyi_splash.close()

    with loop:
        loop.run_forever()