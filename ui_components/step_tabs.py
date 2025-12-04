from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg
from config import get_resource_path

class StepTabs:
    def setup_step_1(self, main_ui, parent_widget):
        self.mainLayout = QtWidgets.QHBoxLayout(parent_widget)
        self.mainLayout.setContentsMargins(20, 20, 20, 20)
        self.mainLayout.setSpacing(20)

        # Left Side: Instructions / Image
        self.leftLayout = QtWidgets.QVBoxLayout()
        # Align to top to prevent floating in the center
        self.leftLayout.setAlignment(QtCore.Qt.AlignTop) 
        self.leftLayout.setSpacing(10)
        
        main_ui.label = QtWidgets.QLabel()
        main_ui.label.setPixmap(QtGui.QPixmap(get_resource_path("images/infographic1.drawio.png")))
        main_ui.label.setScaledContents(True)
        
        # FIX 1: Change SizePolicy to 'Ignored' for Horizontal. 
        # This tells the layout "Don't look at the image size, just force it to the layout size."
        main_ui.label.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Expanding)
        
        self.leftLayout.addWidget(main_ui.label)
        
        # FIX 2: Reduce Left Layout stretch factor from 2 to 1
        self.mainLayout.addLayout(self.leftLayout, 2)

        # Right Side: Graph and Controls
        self.rightLayout = QtWidgets.QVBoxLayout()
        self.rightLayout.setSpacing(20)

        # Graph
        main_ui.graphWidget_hs1 = pg.PlotWidget()
        main_ui.graphWidget_hs1.setBackground('w')
        main_ui.graphWidget_hs1.addLegend()
        main_ui.graphWidget_hs1.setLabel('left', "Force (N)", **{'font-size': '12pt', 'color': '#333'})
        main_ui.graphWidget_hs1.setLabel('bottom', "Time (seconds)", **{'font-size': '12pt', 'color': '#333'})
        pen = pg.mkPen(color=(255,0,0), width=2)
        main_ui.hsS1RForceLine = main_ui.graphWidget_hs1.plot(main_ui.timeData, main_ui.hsS1RForce, name="Extension Sensor", pen=pen)
        self.rightLayout.addWidget(main_ui.graphWidget_hs1, 3)

        # Controls Group
        self.controlsGroupBox = QtWidgets.QGroupBox("Controls")
        self.controlsLayout = QtWidgets.QHBoxLayout(self.controlsGroupBox)
        
        main_ui.pushButton_2 = QtWidgets.QPushButton("Record")
        main_ui.pushButton_2.setCheckable(True)
        main_ui.pushButton_2.toggled.connect(main_ui.on_toggled)
        main_ui.pushButton_2.setStyleSheet("background-color: #28a745; color: white;")
        
        main_ui.pushButton_21 = QtWidgets.QPushButton("Clear Data")
        main_ui.pushButton_21.setCheckable(True)
        main_ui.pushButton_21.toggled.connect(main_ui.clear_data)
        main_ui.pushButton_21.setStyleSheet("background-color: #dc3545; color: white;")

        self.controlsLayout.addWidget(main_ui.pushButton_2)
        self.controlsLayout.addWidget(main_ui.pushButton_21)
        
        main_ui.horizontalLayout_s1 = QtWidgets.QHBoxLayout()
        self.controlsLayout.addLayout(main_ui.horizontalLayout_s1)

        self.rightLayout.addWidget(self.controlsGroupBox)

        # Notes and Measurements
        self.infoLayout = QtWidgets.QHBoxLayout()
        
        # Notes
        self.notesGroupBox = QtWidgets.QGroupBox("Notes")
        self.notesLayout = QtWidgets.QVBoxLayout(self.notesGroupBox)
        main_ui.label_4 = QtWidgets.QLabel("Notes:")
        main_ui.label_4.setVisible(False)
        main_ui.textEdit = QtWidgets.QTextEdit()
        main_ui.textEdit.setPlaceholderText("Enter specific observations here...")
        self.notesLayout.addWidget(main_ui.textEdit)
        self.infoLayout.addWidget(self.notesGroupBox, 2)

        # Measurements
        self.measureGroupBox = QtWidgets.QGroupBox("Measurements")
        self.measureLayout = QtWidgets.QFormLayout(self.measureGroupBox)
        
        main_ui.label_5 = QtWidgets.QLabel("Measurements:") 
        main_ui.label_5.setVisible(False)

        main_ui.label_16 = QtWidgets.QLabel("Unaffected or strong leg extension")
        main_ui.label_16.setStyleSheet("font-style: italic; color: gray;")
        self.measureLayout.addRow(main_ui.label_16)

        main_ui.extensionForceLabel = QtWidgets.QLabel("Extension force:")
        main_ui.extensionForceLineEdit = QtWidgets.QLineEdit()
        main_ui.extensionForceLineEdit.setReadOnly(True)
        self.measureLayout.addRow(main_ui.extensionForceLabel, main_ui.extensionForceLineEdit)
        
        self.infoLayout.addWidget(self.measureGroupBox, 1)
        
        self.rightLayout.addLayout(self.infoLayout, 2)
        
        # FIX 3: Increase Right Layout stretch factor from 3 to 4
        # This creates a 1:4 ratio (Image gets 20% width, Graph gets 80%)
        self.mainLayout.addLayout(self.rightLayout, 3)

    def setup_step_2(self, main_ui, parent_widget):
        self.mainLayout = QtWidgets.QHBoxLayout(parent_widget)
        self.mainLayout.setContentsMargins(20, 20, 20, 20)
        self.mainLayout.setSpacing(20)

        # Left Side
        self.leftLayout = QtWidgets.QVBoxLayout()
        self.leftLayout.setSpacing(10)
        
        main_ui.label_2 = QtWidgets.QLabel()
        main_ui.label_2.setPixmap(QtGui.QPixmap(get_resource_path("images/infographic2.drawio.png")))
        main_ui.label_2.setScaledContents(True)

        # FIX 1: Change SizePolicy to 'Ignored' for Horizontal. 
        # This tells the layout "Don't look at the image size, just force it to the layout size."
        main_ui.label_2.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Expanding)
        
        self.leftLayout.addWidget(main_ui.label_2)
        
        self.mainLayout.addLayout(self.leftLayout, 2)

        # Right Side
        self.rightLayout = QtWidgets.QVBoxLayout()
        self.rightLayout.setSpacing(20)

        # Graph
        main_ui.graphWidget_hs2 = pg.PlotWidget()
        main_ui.graphWidget_hs2.setBackground('w')
        main_ui.graphWidget_hs2.addLegend()
        main_ui.graphWidget_hs2.setLabel('left', "Force (N)", **{'font-size': '12pt', 'color': '#333'})
        main_ui.graphWidget_hs2.setLabel('bottom', "Time (seconds)", **{'font-size': '12pt', 'color': '#333'})
        pen = pg.mkPen(color=(255, 0, 0), width=2)
        main_ui.hsS2RForceLine = main_ui.graphWidget_hs2.plot(main_ui.timeData, main_ui.hsS2RForce, name="Extension Sensor", pen=pen)
        pen_avg = pg.mkPen(color=(0,0,0), width=2, style=QtCore.Qt.DashLine)
        main_ui.hsS2RAverageLine = main_ui.graphWidget_hs2.plot(main_ui.timeData, main_ui.hsS2RAverage, name="Extension Force Average", pen=pen_avg)
        self.rightLayout.addWidget(main_ui.graphWidget_hs2, 3)

        # Controls
        self.controlsGroupBox = QtWidgets.QGroupBox("Controls")
        self.controlsLayout = QtWidgets.QHBoxLayout(self.controlsGroupBox)
        
        main_ui.pushButton_3 = QtWidgets.QPushButton("Record")
        main_ui.pushButton_3.setCheckable(True)
        main_ui.pushButton_3.toggled.connect(main_ui.on_toggled)
        main_ui.pushButton_3.setStyleSheet("background-color: #28a745; color: white;")
        
        main_ui.pushButton_31 = QtWidgets.QPushButton("Clear Data")
        main_ui.pushButton_31.setCheckable(True)
        main_ui.pushButton_31.toggled.connect(main_ui.clear_data)
        main_ui.pushButton_31.setStyleSheet("background-color: #dc3545; color: white;")

        self.controlsLayout.addWidget(main_ui.pushButton_3)
        self.controlsLayout.addWidget(main_ui.pushButton_31)
        
        main_ui.horizontalLayout_s2 = QtWidgets.QHBoxLayout()
        self.controlsLayout.addLayout(main_ui.horizontalLayout_s2)

        self.rightLayout.addWidget(self.controlsGroupBox)

        # Notes and Measurements
        self.infoLayout = QtWidgets.QHBoxLayout()
        
        # Notes
        self.notesGroupBox = QtWidgets.QGroupBox("Notes")
        self.notesLayout = QtWidgets.QVBoxLayout(self.notesGroupBox)
        main_ui.label_10 = QtWidgets.QLabel("Notes:")
        main_ui.label_10.setVisible(False)
        main_ui.textEdit_2 = QtWidgets.QTextEdit()
        main_ui.textEdit_2.setPlaceholderText("Enter specific observations here...")
        self.notesLayout.addWidget(main_ui.textEdit_2)
        self.infoLayout.addWidget(self.notesGroupBox, 2)

        # Measurements
        self.measureGroupBox = QtWidgets.QGroupBox("Measurements")
        self.measureLayout = QtWidgets.QFormLayout(self.measureGroupBox)
        
        main_ui.label_11 = QtWidgets.QLabel("Measurements:")
        main_ui.label_11.setVisible(False)

        main_ui.label_17 = QtWidgets.QLabel("Affected or weak leg extension")
        main_ui.label_17.setStyleSheet("font-style: italic; color: gray;")
        self.measureLayout.addRow(main_ui.label_17)

        main_ui.strongLegAverageStrengthLabel_2 = QtWidgets.QLabel("Force average:")
        main_ui.strongLegAverageStrengthLineEdit_2 = QtWidgets.QLineEdit()
        main_ui.strongLegAverageStrengthLineEdit_2.setReadOnly(True)
        self.measureLayout.addRow(main_ui.strongLegAverageStrengthLabel_2, main_ui.strongLegAverageStrengthLineEdit_2)
        
        main_ui.strongLegPeakStrengthLabel_2 = QtWidgets.QLabel("Force peak:\n(Affected leg\nvoluntary extension)")
        main_ui.strongLegPeakStrengthLineEdit_2 = QtWidgets.QLineEdit()
        main_ui.strongLegPeakStrengthLineEdit_2.setReadOnly(True)
        self.measureLayout.addRow(main_ui.strongLegPeakStrengthLabel_2, main_ui.strongLegPeakStrengthLineEdit_2)
        
        self.infoLayout.addWidget(self.measureGroupBox, 1)
        
        self.rightLayout.addLayout(self.infoLayout, 2)
        self.mainLayout.addLayout(self.rightLayout, 3)

    def setup_step_3(self, main_ui, parent_widget):
        self.mainLayout = QtWidgets.QHBoxLayout(parent_widget)
        self.mainLayout.setContentsMargins(20, 20, 20, 20)
        self.mainLayout.setSpacing(20)

        # Left Side
        self.leftLayout = QtWidgets.QVBoxLayout()
        self.leftLayout.setSpacing(10)
        
        main_ui.label_3 = QtWidgets.QLabel()
        main_ui.label_3.setPixmap(QtGui.QPixmap(get_resource_path("images/infographic3.drawio.png")))
        main_ui.label_3.setScaledContents(True)

        # FIX 1: Change SizePolicy to 'Ignored' for Horizontal. 
        # This tells the layout "Don't look at the image size, just force it to the layout size."
        main_ui.label_3.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Expanding)
        
        self.leftLayout.addWidget(main_ui.label_3)
        
        self.mainLayout.addLayout(self.leftLayout, 2)

        # Right Side
        self.rightLayout = QtWidgets.QVBoxLayout()
        self.rightLayout.setSpacing(20)

        # Graph
        main_ui.graphWidget_hs3 = pg.PlotWidget()
        main_ui.graphWidget_hs3.setBackground('w')
        main_ui.graphWidget_hs3.addLegend()
        main_ui.graphWidget_hs3.setLabel('left', "Force (N)", **{'font-size': '12pt', 'color': '#333'})
        main_ui.graphWidget_hs3.setLabel('bottom', "Time (seconds)", **{'font-size': '12pt', 'color': '#333'})
        pen = pg.mkPen(color=(255, 0, 0), width=2)
        main_ui.hsS3RForceLine = main_ui.graphWidget_hs3.plot(main_ui.timeData, main_ui.hsS3RForce, name="Extension Sensor", pen=pen)
        pen_avg = pg.mkPen(color=(0,0,0), width=2, style=QtCore.Qt.DashLine)
        main_ui.hsS3RForceAverageLine = main_ui.graphWidget_hs3.plot(main_ui.timeData, main_ui.hsS3RAverage, name = "Extension Force Average", pen=pen_avg)
        self.rightLayout.addWidget(main_ui.graphWidget_hs3, 3)

        # Controls
        self.controlsGroupBox = QtWidgets.QGroupBox("Controls")
        self.controlsLayout = QtWidgets.QHBoxLayout(self.controlsGroupBox)
        
        main_ui.pushButton_4 = QtWidgets.QPushButton("Record")
        main_ui.pushButton_4.setCheckable(True)
        main_ui.pushButton_4.toggled.connect(main_ui.on_toggled)
        main_ui.pushButton_4.setStyleSheet("background-color: #28a745; color: white;")
        
        main_ui.pushButton_41 = QtWidgets.QPushButton("Clear Data")
        main_ui.pushButton_41.setCheckable(True)
        main_ui.pushButton_41.toggled.connect(main_ui.clear_data)
        main_ui.pushButton_41.setStyleSheet("background-color: #dc3545; color: white;")

        self.controlsLayout.addWidget(main_ui.pushButton_4)
        self.controlsLayout.addWidget(main_ui.pushButton_41)
        
        main_ui.horizontalLayout_s3 = QtWidgets.QHBoxLayout()
        self.controlsLayout.addLayout(main_ui.horizontalLayout_s3)

        self.rightLayout.addWidget(self.controlsGroupBox)

        # Notes and Measurements
        self.infoLayout = QtWidgets.QHBoxLayout()
        
        # Notes
        self.notesGroupBox = QtWidgets.QGroupBox("Notes")
        self.notesLayout = QtWidgets.QVBoxLayout(self.notesGroupBox)
        main_ui.label_14 = QtWidgets.QLabel("Notes:")
        main_ui.label_14.setVisible(False)
        main_ui.textEdit_6 = QtWidgets.QTextEdit()
        main_ui.textEdit_6.setPlaceholderText("Enter specific observations here...")
        self.notesLayout.addWidget(main_ui.textEdit_6)
        self.infoLayout.addWidget(self.notesGroupBox, 2)

        # Measurements
        self.measureGroupBox = QtWidgets.QGroupBox("Measurements")
        self.measureLayout = QtWidgets.QFormLayout(self.measureGroupBox)
        
        main_ui.label_15 = QtWidgets.QLabel("Measurements:")
        main_ui.label_15.setVisible(False)

        main_ui.label_18 = QtWidgets.QLabel("Affected leg involuntary extension")
        main_ui.label_18.setStyleSheet("font-style: italic; color: gray;")
        self.measureLayout.addRow(main_ui.label_18)

        main_ui.weakLegPeakStrengthLabel_3 = QtWidgets.QLabel("Affected leg involuntary extension:")
        main_ui.weakLegPeakStrengthLineEdit_3 = QtWidgets.QLineEdit()
        main_ui.weakLegPeakStrengthLineEdit_3.setReadOnly(True)
        self.measureLayout.addRow(main_ui.weakLegPeakStrengthLabel_3, main_ui.weakLegPeakStrengthLineEdit_3)
        
        self.infoLayout.addWidget(self.measureGroupBox, 1)
        
        self.rightLayout.addLayout(self.infoLayout, 2)
        self.mainLayout.addLayout(self.rightLayout, 3)

    def retranslate_step_1(self, main_ui):
        _translate = QtCore.QCoreApplication.translate
        main_ui.pushButton_2.setText(_translate("MainWindow", "Record"))
        main_ui.pushButton_21.setText(_translate("MainWindow", "Clear Data"))
        main_ui.extensionForceLabel.setText(_translate("MainWindow", "Extension force:"))

    def retranslate_step_2(self, main_ui):
        _translate = QtCore.QCoreApplication.translate
        main_ui.pushButton_3.setText(_translate("MainWindow", "Record"))
        main_ui.pushButton_31.setText(_translate("MainWindow", "Clear Data"))
        main_ui.strongLegAverageStrengthLabel_2.setText(_translate("MainWindow", "Force average:"))
        main_ui.strongLegPeakStrengthLabel_2.setText(_translate("MainWindow", "Force peak:\n(Affected leg\nvoluntary extension)"))

    def retranslate_step_3(self, main_ui):
        _translate = QtCore.QCoreApplication.translate
        main_ui.pushButton_4.setText(_translate("MainWindow", "Record"))
        main_ui.pushButton_41.setText(_translate("MainWindow", "Clear Data"))
        main_ui.weakLegPeakStrengthLabel_3.setText(_translate("MainWindow", "Affected leg involuntary extension:"))