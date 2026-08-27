from PyQt5 import QtCore, QtWidgets
from add_comport import AddComport
from add_ble_device import AddBleDevice

class MenuBar:
    def setup_ui(self, main_ui, MainWindow):
        main_ui.menubar = QtWidgets.QMenuBar(MainWindow)
        main_ui.menubar.setGeometry(QtCore.QRect(0, 0, 1200, 26))
        main_ui.menubar.setObjectName("menubar")
        
        main_ui.menuFile = QtWidgets.QMenu(main_ui.menubar)
        main_ui.menuFile.setObjectName("menuFile")
        
        main_ui.menuEdit = QtWidgets.QMenu(main_ui.menubar)
        main_ui.menuEdit.setObjectName("menuEdit")
        
        # Filter Frequency remains in Edit
        main_ui.menuFilterFrequency = QtWidgets.QMenu(main_ui.menuEdit)
        main_ui.menuFilterFrequency.setObjectName("menuFilterFrequency")
        
        main_ui.menuDatabase = QtWidgets.QMenu(main_ui.menubar)
        main_ui.menuDatabase.setObjectName("menuDatabase")
        
        # Connection menu
        main_ui.menuConnection = QtWidgets.QMenu(main_ui.menubar)
        main_ui.menuConnection.setObjectName("menuConnection")
        
        main_ui.menuHelp = QtWidgets.QMenu(main_ui.menubar)
        main_ui.menuHelp.setObjectName("menuHelp")
        
        MainWindow.setMenuBar(main_ui.menubar)
        main_ui.statusbar = QtWidgets.QStatusBar(MainWindow)
        main_ui.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(main_ui.statusbar)

        # --- Actions ---
        main_ui.actionNew = QtWidgets.QAction(MainWindow)
        main_ui.actionNew.setShortcut("Ctrl+N")
        main_ui.actionNew.setObjectName("actionNew")
        main_ui.actionNew.triggered.connect(main_ui.file_new)

        main_ui.actionOpen = QtWidgets.QAction(MainWindow)
        main_ui.actionOpen.setShortcut("Ctrl+O")
        main_ui.actionOpen.setObjectName("actionOpen")
        main_ui.actionOpen.triggered.connect(main_ui.file_open)

        main_ui.actionSave = QtWidgets.QAction(MainWindow)
        main_ui.actionSave.setShortcut("Ctrl+S")
        main_ui.actionSave.setObjectName("actionSave")
        main_ui.actionSave.triggered.connect(main_ui.file_save)

        main_ui.actionSave_As = QtWidgets.QAction(MainWindow)
        main_ui.actionSave_As.setObjectName("actionSave_As")
        main_ui.actionSave_As.triggered.connect(main_ui.file_new)

        main_ui.actionCreateDatabase = QtWidgets.QAction(MainWindow)
        main_ui.actionCreateDatabase.setObjectName("actionCreateDatabase")
        main_ui.actionCreateDatabase.triggered.connect(main_ui.file_new_database)

        main_ui.actionOpenDatabase = QtWidgets.QAction(MainWindow)
        main_ui.actionOpenDatabase.setObjectName("actionOpenDatabase")
        main_ui.actionOpenDatabase.triggered.connect(main_ui.file_open_database)

        main_ui.actionUpdateDatabase = QtWidgets.QAction(MainWindow)
        main_ui.actionUpdateDatabase.setObjectName("actionUpdateDatabase")
        main_ui.actionUpdateDatabase.triggered.connect(main_ui.file_update_database)

        # --- Connection Menu Items ---
        
        # 1. Bluetooth (AddBleDevice adds "Bluetooth" submenu)
        main_ui.ble_manager = AddBleDevice(main_ui, main_ui.menuConnection)
        main_ui.ble_manager.device_selected.connect(main_ui.on_ble_device_selected)
        main_ui.ble_manager.connect_requested.connect(main_ui.connect_ble_persistent)
        main_ui.ble_manager.disconnect_requested.connect(main_ui.disconnect_ble_persistent)
        
        # 2. USB Connection Submenu
        main_ui.menuUSB = main_ui.menuConnection.addMenu("USB Connection")
        main_ui.menuUSB.setObjectName("menuUSB")
        
        # Baud Menu (now under USB)
        main_ui.menuBaud = QtWidgets.QMenu(main_ui.menuUSB)
        main_ui.menuBaud.setObjectName("menuBaud")
        
        # COM Port (AddComport adds "COM Port" submenu)
        # We pass menuUSB as the parent menu
        main_ui.actionPort = AddComport(main_ui, main_ui.menuUSB)
        main_ui.actionPort.porttnavn.connect(main_ui.valgAfComport)

        # Baud Actions
        main_ui.action19200 = QtWidgets.QAction(MainWindow)
        main_ui.action19200.setObjectName("action19200")
        main_ui.action42069 = QtWidgets.QAction(MainWindow)
        main_ui.action42069.setObjectName("action42069")
        
        main_ui.menuBaud.addAction(main_ui.action19200)
        
        main_ui.menuUSB.addMenu(main_ui.menuBaud)

        # --- Filter Frequency Actions ---
        main_ui.actionHeavy5Hz = QtWidgets.QAction(MainWindow)
        main_ui.actionHeavy5Hz.setObjectName("actionHeavy5Hz")
        main_ui.actionHeavy5Hz.setCheckable(True)

        main_ui.actionStandard10Hz = QtWidgets.QAction(MainWindow)
        main_ui.actionStandard10Hz.setObjectName("actionStandard10Hz")
        main_ui.actionStandard10Hz.setCheckable(True)
        main_ui.actionStandard10Hz.setChecked(True)

        main_ui.actionResponsive20Hz = QtWidgets.QAction(MainWindow)
        main_ui.actionResponsive20Hz.setObjectName("actionResponsive20Hz")
        main_ui.actionResponsive20Hz.setCheckable(True)

        main_ui.frequencyActionGroup = QtWidgets.QActionGroup(MainWindow)
        main_ui.frequencyActionGroup.addAction(main_ui.actionHeavy5Hz)
        main_ui.frequencyActionGroup.addAction(main_ui.actionStandard10Hz)
        main_ui.frequencyActionGroup.addAction(main_ui.actionResponsive20Hz)

        main_ui.menuFilterFrequency.addAction(main_ui.actionHeavy5Hz)
        main_ui.menuFilterFrequency.addAction(main_ui.actionStandard10Hz)
        main_ui.menuFilterFrequency.addAction(main_ui.actionResponsive20Hz)
        
        main_ui.actionHeavy5Hz.triggered.connect(lambda: main_ui.set_filter_frequency(5))
        main_ui.actionStandard10Hz.triggered.connect(lambda: main_ui.set_filter_frequency(10))
        main_ui.actionResponsive20Hz.triggered.connect(lambda: main_ui.set_filter_frequency(20))

        # --- Help Actions ---
        main_ui.actionGetting_Started = QtWidgets.QAction(MainWindow)
        main_ui.actionGetting_Started.setObjectName("actionGetting_Started")
        main_ui.actionTroubleshooting = QtWidgets.QAction(MainWindow)
        main_ui.actionTroubleshooting.setObjectName("actionTroubleshooting")
        main_ui.actionFAQs = QtWidgets.QAction(MainWindow)
        main_ui.actionFAQs.setObjectName("actionFAQs")
        
        main_ui.menuHelp.addAction(main_ui.actionGetting_Started)
        main_ui.menuHelp.addAction(main_ui.actionTroubleshooting)
        main_ui.menuHelp.addAction(main_ui.actionFAQs)
        
        # --- Assemble Menu Bar ---
        main_ui.menuFile.addAction(main_ui.actionNew)
        main_ui.menuFile.addAction(main_ui.actionOpen)
        main_ui.menuFile.addAction(main_ui.actionSave)
        main_ui.menuFile.addAction(main_ui.actionSave_As)
        
        main_ui.menuDatabase.addAction(main_ui.actionCreateDatabase)
        main_ui.menuDatabase.addAction(main_ui.actionOpenDatabase)
        main_ui.menuDatabase.addAction(main_ui.actionUpdateDatabase)
        
        # Edit Menu (Only Filter Frequency now)
        main_ui.menuEdit.addAction(main_ui.menuFilterFrequency.menuAction())

        # Add menus to menubar
        main_ui.menubar.addAction(main_ui.menuFile.menuAction())
        main_ui.menubar.addAction(main_ui.menuEdit.menuAction())
        main_ui.menubar.addAction(main_ui.menuDatabase.menuAction())
        main_ui.menubar.addAction(main_ui.menuConnection.menuAction())
        main_ui.menubar.addAction(main_ui.menuHelp.menuAction())

    def retranslate_ui(self, main_ui):
        _translate = QtCore.QCoreApplication.translate
        main_ui.menuFile.setTitle(_translate("MainWindow", "File"))
        main_ui.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        main_ui.menuBaud.setTitle(_translate("MainWindow", "Baud"))
        main_ui.menuDatabase.setTitle(_translate("MainWindow", "Database"))
        main_ui.menuConnection.setTitle(_translate("MainWindow", "Connection"))
        main_ui.menuUSB.setTitle(_translate("MainWindow", "USB Connection"))
        main_ui.menuHelp.setTitle(_translate("MainWindow", "Help"))
        
        main_ui.actionCreateDatabase.setText(_translate("MainWindow", "Create Database"))
        main_ui.actionOpenDatabase.setText(_translate("MainWindow", "Open Database"))
        main_ui.actionUpdateDatabase.setText(_translate("MainWindow", "Update Database"))
        main_ui.actionNew.setText(_translate("MainWindow", "New"))
        main_ui.actionNew.setShortcut(_translate("MainWindow", "Ctrl+N"))
        main_ui.actionOpen.setText(_translate("MainWindow", "Open..."))
        main_ui.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))
        main_ui.actionSave.setText(_translate("MainWindow", "Save"))
        main_ui.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
        main_ui.actionSave_As.setText(_translate("MainWindow", "Save As..."))

        main_ui.action19200.setText(_translate("MainWindow", "19200"))
        main_ui.action42069.setText(_translate("MainWindow", "42069"))

        main_ui.actionGetting_Started.setText(_translate("MainWindow", "Getting Started"))
        main_ui.actionTroubleshooting.setText(_translate("MainWindow", "Troubleshooting"))
        main_ui.actionFAQs.setText(_translate("MainWindow", "FAQs"))

        main_ui.menuFilterFrequency.setTitle(_translate("MainWindow", "Filter Frequency"))
        main_ui.actionHeavy5Hz.setText(_translate("MainWindow", "Heavy (5 Hz)"))
        main_ui.actionHeavy5Hz.setStatusTip(_translate("MainWindow", "Recommended for noisy environments"))
        main_ui.actionStandard10Hz.setText(_translate("MainWindow", "Standard (10 Hz)"))
        main_ui.actionStandard10Hz.setStatusTip(_translate("MainWindow", "Default setting"))
        main_ui.actionResponsive20Hz.setText(_translate("MainWindow", "Responsive (20 Hz)"))
        main_ui.actionResponsive20Hz.setStatusTip(_translate("MainWindow", "For analysing rapid movements"))