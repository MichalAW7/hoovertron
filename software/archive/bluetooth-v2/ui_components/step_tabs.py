from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg

class StepTabs:
    def setup_step_1(self, main_ui, parent_widget):
        self.horizontalLayoutWidget = QtWidgets.QWidget(parent_widget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(-1, -1, 1201, 801))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(20, 20, 20, 20)
        self.horizontalLayout.setSpacing(20)
        self.horizontalLayout.setObjectName("horizontalLayout")
        
        main_ui.label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(main_ui.label.sizePolicy().hasHeightForWidth())
        main_ui.label.setSizePolicy(sizePolicy)
        main_ui.label.setMinimumSize(QtCore.QSize(200, 450))
        main_ui.label.setText("")
        main_ui.label.setPixmap(QtGui.QPixmap("images/infographic1.drawio.png"))
        main_ui.label.setScaledContents(True)
        main_ui.label.setObjectName("label")
        self.horizontalLayout.addWidget(main_ui.label)
        
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(7)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(20)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setContentsMargins(-1, -1, -1, 20)
        self.verticalLayout_4.setSpacing(20)
        self.verticalLayout_4.setObjectName("verticalLayout_4")

        # Graph HS1
        main_ui.graphWidget_hs1 = pg.PlotWidget()
        main_ui.graphWidget_hs1.setObjectName("graphWidget_hs1")
        main_ui.graphWidget_hs1.setBackground('w')
        main_ui.graphWidget_hs1.addLegend()
        main_ui.graphWidget_hs1.setLabel('left', "<span style=\"color:gray;font-size:20px\">Force (N)</span>")
        main_ui.graphWidget_hs1.setLabel('bottom', "<span style=\"color:gray;font-size:20px\">Time (seconds) </span>")
        pen = pg.mkPen(color=(255,0,0))
        main_ui.hsS1RForceLine = main_ui.graphWidget_hs1.plot(main_ui.timeData, main_ui.hsS1RForce, name = "Extension Sensor", pen=pen)
        self.verticalLayout_4.addWidget(main_ui.graphWidget_hs1)

        # Buttons Step 1
        main_ui.horizontalLayout_s1 = QtWidgets.QHBoxLayout()
        main_ui.pushButton_2 = QtWidgets.QPushButton(
            self.horizontalLayoutWidget,
            checkable=True,
            toggled=main_ui.on_toggled
        )
        main_ui.pushButton_2.setObjectName("pushButton_2")
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        main_ui.pushButton_2.setFont(font)
        main_ui.horizontalLayout_s1.addWidget(main_ui.pushButton_2)

        main_ui.pushButton_21 = QtWidgets.QPushButton(
            self.horizontalLayoutWidget,
            checkable=True,
            toggled=main_ui.clear_data
        )
        main_ui.pushButton_21.setObjectName("pushButton_21")
        font.setPointSize(14)
        font.setBold(True)
        main_ui.pushButton_21.setFont(font)
        main_ui.horizontalLayout_s1.addWidget(main_ui.pushButton_21)
        self.verticalLayout_4.addLayout(main_ui.horizontalLayout_s1)
        self.horizontalLayout_3.addLayout(self.verticalLayout_4)
        self.horizontalLayout_3.setStretch(0, 3)
        self.horizontalLayout_3.setStretch(1, 2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        
        self.line = QtWidgets.QFrame(self.horizontalLayoutWidget)
        self.line.setStyleSheet("")
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_2.addWidget(self.line)
        
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setSpacing(20)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        
        main_ui.label_4 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        main_ui.label_4.setFont(font)
        main_ui.label_4.setObjectName("label_4")
        self.verticalLayout_6.addWidget(main_ui.label_4)

        main_ui.label_41 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        main_ui.label_41.setFont(font)
        main_ui.label_41.setObjectName("label_41")
        self.verticalLayout_6.addWidget(main_ui.label_41)

        main_ui.label_42 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        main_ui.label_42.setFont(font)
        main_ui.label_42.setObjectName("label_42")
        self.verticalLayout_6.addWidget(main_ui.label_42)

        main_ui.textEdit = QtWidgets.QTextEdit(self.horizontalLayoutWidget)
        main_ui.textEdit.setObjectName("textEdit")
        self.verticalLayout_6.addWidget(main_ui.textEdit)
        self.verticalLayout_6.setStretch(0, 1)
        self.verticalLayout_6.setStretch(1, 6)
        self.horizontalLayout_4.addLayout(self.verticalLayout_6)
        
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        main_ui.label_5 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        main_ui.label_5.setFont(font)
        main_ui.label_5.setObjectName("label_5")
        self.verticalLayout_7.addWidget(main_ui.label_5)
        
        main_ui.label_16 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font_italic = QtGui.QFont()
        font_italic.setItalic(True)
        main_ui.label_16.setFont(font_italic)
        main_ui.label_16.setWordWrap(True)
        main_ui.label_16.setObjectName("label_16")
        self.verticalLayout_7.addWidget(main_ui.label_16)
        
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setFormAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout.setVerticalSpacing(25)
        self.formLayout.setObjectName("formLayout")
        
        main_ui.extensionForceLabel = QtWidgets.QLabel(self.horizontalLayoutWidget)
        main_ui.extensionForceLabel.setObjectName("extensionForceLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, main_ui.extensionForceLabel)
        main_ui.extensionForceLineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        main_ui.extensionForceLineEdit.setObjectName("extensionForceLineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, main_ui.extensionForceLineEdit)
        
        self.verticalLayout_7.addLayout(self.formLayout)
        self.verticalLayout_7.setStretch(0, 1)
        self.verticalLayout_7.setStretch(1, 1)
        self.verticalLayout_7.setStretch(2, 5)
        self.horizontalLayout_4.addLayout(self.verticalLayout_7)
        self.horizontalLayout_4.setStretch(0, 3)
        self.horizontalLayout_4.setStretch(1, 2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.verticalLayout_2.setStretch(0, 4)
        self.verticalLayout_2.setStretch(2, 3)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.horizontalLayout.setStretch(0, 2)
        self.horizontalLayout.setStretch(1, 3)

    def setup_step_2(self, main_ui, parent_widget):
        self.horizontalLayoutWidget_4 = QtWidgets.QWidget(parent_widget)
        self.horizontalLayoutWidget_4.setGeometry(QtCore.QRect(0, 0, 1201, 801))
        self.horizontalLayoutWidget_4.setObjectName("horizontalLayoutWidget_4")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_4)
        self.horizontalLayout_5.setContentsMargins(19, 19, 21, 21)
        self.horizontalLayout_5.setSpacing(20)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        
        main_ui.label_2 = QtWidgets.QLabel(self.horizontalLayoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(main_ui.label_2.sizePolicy().hasHeightForWidth())
        main_ui.label_2.setSizePolicy(sizePolicy)
        main_ui.label_2.setMinimumSize(QtCore.QSize(200, 450))
        main_ui.label_2.setText("")
        main_ui.label_2.setPixmap(QtGui.QPixmap("images/infographic2.drawio.png"))
        main_ui.label_2.setScaledContents(True)
        main_ui.label_2.setObjectName("label_2")
        self.horizontalLayout_5.addWidget(main_ui.label_2)
        
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setSpacing(7)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setSpacing(20)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setContentsMargins(-1, -1, -1, 20)
        self.verticalLayout_8.setSpacing(20)
        self.verticalLayout_8.setObjectName("verticalLayout_8")

        # Graph HS2
        main_ui.graphWidget_hs2 = pg.PlotWidget()
        main_ui.graphWidget_hs2.setObjectName("graphWidget_hs2")
        main_ui.graphWidget_hs2.setBackground('w')
        main_ui.graphWidget_hs2.addLegend()
        main_ui.graphWidget_hs2.setLabel('left', "<span style=\"color:gray;font-size:20px\">Force (N)</span>")
        main_ui.graphWidget_hs2.setLabel('bottom', "<span style=\"color:gray;font-size:20px\">Time (seconds)</span>")
        pen = pg.mkPen(color=(255, 0, 0))
        main_ui.hsS2RForceLine = main_ui.graphWidget_hs2.plot(main_ui.timeData, main_ui.hsS2RForce, name="Extension Sensor", pen=pen)
        pen = pg.mkPen(color=(0,0,0))
        main_ui.hsS2RAverageLine = main_ui.graphWidget_hs2.plot(main_ui.timeData, main_ui.hsS2RAverage, name="Extension Force Average", pen=pen)
        self.verticalLayout_8.addWidget(main_ui.graphWidget_hs2)

        # Buttons Step 2
        main_ui.horizontalLayout_s2 = QtWidgets.QHBoxLayout()
        main_ui.pushButton_3 = QtWidgets.QPushButton(
            self.horizontalLayoutWidget_4,
            checkable=True,
            toggled=main_ui.on_toggled
        )
        main_ui.pushButton_3.setObjectName("pushButton_3")
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        main_ui.pushButton_3.setFont(font)
        main_ui.horizontalLayout_s2.addWidget(main_ui.pushButton_3)

        main_ui.pushButton_31 = QtWidgets.QPushButton(
            self.horizontalLayoutWidget_4,
            checkable=True,
            toggled=main_ui.clear_data
        )
        main_ui.pushButton_31.setObjectName("pushButton_31")
        font.setPointSize(14)
        font.setBold(True)
        main_ui.pushButton_31.setFont(font)
        main_ui.horizontalLayout_s2.addWidget(main_ui.pushButton_31)
        self.verticalLayout_8.addLayout(main_ui.horizontalLayout_s2)
        
        self.horizontalLayout_6.addLayout(self.verticalLayout_8)
        self.horizontalLayout_6.setStretch(0, 3)
        self.horizontalLayout_6.setStretch(1, 2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_6)
        
        self.line_2 = QtWidgets.QFrame(self.horizontalLayoutWidget_4)
        self.line_2.setStyleSheet("")
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout_3.addWidget(self.line_2)
        
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setSpacing(20)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        
        main_ui.label_10 = QtWidgets.QLabel(self.horizontalLayoutWidget_4)
        font.setPointSize(12)
        main_ui.label_10.setFont(font)
        main_ui.label_10.setObjectName("label_10")
        self.verticalLayout_10.addWidget(main_ui.label_10)
        
        main_ui.textEdit_2 = QtWidgets.QTextEdit(self.horizontalLayoutWidget_4)
        main_ui.textEdit_2.setObjectName("textEdit_2")
        self.verticalLayout_10.addWidget(main_ui.textEdit_2)
        self.verticalLayout_10.setStretch(0, 1)
        self.verticalLayout_10.setStretch(1, 6)
        self.horizontalLayout_7.addLayout(self.verticalLayout_10)
        
        self.verticalLayout_11 = QtWidgets.QVBoxLayout()
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        
        main_ui.label_11 = QtWidgets.QLabel(self.horizontalLayoutWidget_4)
        main_ui.label_11.setFont(font)
        main_ui.label_11.setObjectName("label_11")
        self.verticalLayout_11.addWidget(main_ui.label_11)
        
        main_ui.label_17 = QtWidgets.QLabel(self.horizontalLayoutWidget_4)
        font_small = QtGui.QFont()
        font_small.setPointSize(10)
        font_small.setItalic(True)
        main_ui.label_17.setFont(font_small)
        main_ui.label_17.setObjectName("label_17")
        self.verticalLayout_11.addWidget(main_ui.label_17)
        
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setFormAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout_2.setVerticalSpacing(25)
        self.formLayout_2.setObjectName("formLayout_2")
        
        main_ui.strongLegAverageStrengthLabel_2 = QtWidgets.QLabel(self.horizontalLayoutWidget_4)
        font_p10 = QtGui.QFont()
        font_p10.setPointSize(10)
        main_ui.strongLegAverageStrengthLabel_2.setFont(font_p10)
        main_ui.strongLegAverageStrengthLabel_2.setObjectName("strongLegAverageStrengthLabel_2")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, main_ui.strongLegAverageStrengthLabel_2)
        
        main_ui.strongLegAverageStrengthLineEdit_2 = QtWidgets.QLineEdit(self.horizontalLayoutWidget_4)
        main_ui.strongLegAverageStrengthLineEdit_2.setObjectName("strongLegAverageStrengthLineEdit_2")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, main_ui.strongLegAverageStrengthLineEdit_2)
        
        main_ui.strongLegPeakStrengthLabel_2 = QtWidgets.QLabel(self.horizontalLayoutWidget_4)
        main_ui.strongLegPeakStrengthLabel_2.setFont(font_p10)
        main_ui.strongLegPeakStrengthLabel_2.setObjectName("strongLegPeakStrengthLabel_2")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, main_ui.strongLegPeakStrengthLabel_2)
        
        main_ui.strongLegPeakStrengthLineEdit_2 = QtWidgets.QLineEdit(self.horizontalLayoutWidget_4)
        main_ui.strongLegPeakStrengthLineEdit_2.setObjectName("strongLegPeakStrengthLineEdit_2")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, main_ui.strongLegPeakStrengthLineEdit_2)
        
        self.verticalLayout_11.addLayout(self.formLayout_2)
        self.verticalLayout_11.setStretch(0, 1)
        self.verticalLayout_11.setStretch(1, 1)
        self.verticalLayout_11.setStretch(2, 5)
        self.horizontalLayout_7.addLayout(self.verticalLayout_11)
        self.horizontalLayout_7.setStretch(0, 3)
        self.horizontalLayout_7.setStretch(1, 2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_7)
        self.verticalLayout_3.setStretch(0, 4)
        self.verticalLayout_3.setStretch(2, 3)
        self.horizontalLayout_5.addLayout(self.verticalLayout_3)
        self.horizontalLayout_5.setStretch(0, 2)
        self.horizontalLayout_5.setStretch(1, 3)

    def setup_step_3(self, main_ui, parent_widget):
        self.horizontalLayoutWidget_5 = QtWidgets.QWidget(parent_widget)
        self.horizontalLayoutWidget_5.setGeometry(QtCore.QRect(0, 0, 1201, 801))
        self.horizontalLayoutWidget_5.setObjectName("horizontalLayoutWidget_5")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_5)
        self.horizontalLayout_8.setContentsMargins(19, 19, 21, 21)
        self.horizontalLayout_8.setSpacing(20)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        
        main_ui.label_3 = QtWidgets.QLabel(self.horizontalLayoutWidget_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(main_ui.label_3.sizePolicy().hasHeightForWidth())
        main_ui.label_3.setSizePolicy(sizePolicy)
        main_ui.label_3.setMinimumSize(QtCore.QSize(200, 450))
        main_ui.label_3.setText("")
        main_ui.label_3.setPixmap(QtGui.QPixmap("images\infographic3.drawio.png"))
        main_ui.label_3.setScaledContents(True)
        main_ui.label_3.setObjectName("label_3")
        self.horizontalLayout_8.addWidget(main_ui.label_3)
        
        self.verticalLayout_12 = QtWidgets.QVBoxLayout()
        self.verticalLayout_12.setSpacing(7)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setSpacing(20)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout()
        self.verticalLayout_13.setContentsMargins(-1, -1, -1, 20)
        self.verticalLayout_13.setSpacing(20)
        self.verticalLayout_13.setObjectName("verticalLayout_13")

        # Graph HS3
        main_ui.graphWidget_hs3 = pg.PlotWidget()
        main_ui.graphWidget_hs3.setObjectName("graphWidget_hs3")
        main_ui.graphWidget_hs3.setBackground('w')
        main_ui.graphWidget_hs3.addLegend()
        main_ui.graphWidget_hs3.setLabel('left', "<span style=\"color:gray;font-size:20px\">Force (N)</span>")
        main_ui.graphWidget_hs3.setLabel('bottom', "<span style=\"color:gray;font-size:20px\">Time (seconds)</span>")
        pen = pg.mkPen(color=(255, 0, 0))
        main_ui.hsS3RForceLine = main_ui.graphWidget_hs3.plot(main_ui.timeData, main_ui.hsS3RForce, name="Extension Sensor", pen=pen)
        pen = pg.mkPen(color=(0,0,0))
        main_ui.hsS3RForceAverageLine = main_ui.graphWidget_hs3.plot(main_ui.timeData, main_ui.hsS3RAverage, name = "Extension Force Average", pen=pen)
        self.verticalLayout_13.addWidget(main_ui.graphWidget_hs3)

        # Buttons Step 3
        main_ui.horizontalLayout_s3 = QtWidgets.QHBoxLayout()
        main_ui.pushButton_4 = QtWidgets.QPushButton(
            self.horizontalLayoutWidget_5,
            checkable=True,
            toggled=main_ui.on_toggled
        )
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        main_ui.pushButton_4.setFont(font)
        main_ui.pushButton_4.setObjectName("pushButton_4")
        main_ui.horizontalLayout_s3.addWidget(main_ui.pushButton_4)

        main_ui.pushButton_41 = QtWidgets.QPushButton(
            self.horizontalLayoutWidget_5,
            checkable=True,
            toggled=main_ui.clear_data
        )
        main_ui.pushButton_41.setFont(font)
        main_ui.pushButton_41.setObjectName("pushButton_41")
        main_ui.horizontalLayout_s3.addWidget(main_ui.pushButton_41)

        self.verticalLayout_13.addLayout(main_ui.horizontalLayout_s3)
        self.horizontalLayout_9.addLayout(self.verticalLayout_13)
        self.horizontalLayout_9.setStretch(0, 3)
        self.horizontalLayout_9.setStretch(1, 2)
        self.verticalLayout_12.addLayout(self.horizontalLayout_9)
        
        self.line_3 = QtWidgets.QFrame(self.horizontalLayoutWidget_5)
        self.line_3.setStyleSheet("")
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout_12.addWidget(self.line_3)
        
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setSpacing(20)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.verticalLayout_15 = QtWidgets.QVBoxLayout()
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        
        main_ui.label_14 = QtWidgets.QLabel(self.horizontalLayoutWidget_5)
        font.setPointSize(12)
        main_ui.label_14.setFont(font)
        main_ui.label_14.setObjectName("label_14")
        self.verticalLayout_15.addWidget(main_ui.label_14)
        
        main_ui.textEdit_6 = QtWidgets.QTextEdit(self.horizontalLayoutWidget_5)
        main_ui.textEdit_6.setObjectName("textEdit_6")
        self.verticalLayout_15.addWidget(main_ui.textEdit_6)
        self.verticalLayout_15.setStretch(0, 1)
        self.verticalLayout_15.setStretch(1, 6)
        self.horizontalLayout_10.addLayout(self.verticalLayout_15)
        
        self.verticalLayout_16 = QtWidgets.QVBoxLayout()
        self.verticalLayout_16.setObjectName("verticalLayout_16")
        
        main_ui.label_15 = QtWidgets.QLabel(self.horizontalLayoutWidget_5)
        main_ui.label_15.setFont(font)
        main_ui.label_15.setObjectName("label_15")
        self.verticalLayout_16.addWidget(main_ui.label_15)
        
        main_ui.label_18 = QtWidgets.QLabel(self.horizontalLayoutWidget_5)
        font_it = QtGui.QFont()
        font_it.setItalic(True)
        main_ui.label_18.setFont(font_it)
        main_ui.label_18.setWordWrap(True)
        main_ui.label_18.setObjectName("label_18")
        self.verticalLayout_16.addWidget(main_ui.label_18)
        
        self.formLayout_3 = QtWidgets.QFormLayout()
        self.formLayout_3.setFormAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout_3.setVerticalSpacing(25)
        self.formLayout_3.setObjectName("formLayout_3")

        main_ui.weakLegPeakStrengthLabel_3 = QtWidgets.QLabel(self.horizontalLayoutWidget_5)
        font_p10 = QtGui.QFont()
        font_p10.setPointSize(10)
        main_ui.weakLegPeakStrengthLabel_3.setFont(font_p10)
        main_ui.weakLegPeakStrengthLabel_3.setWordWrap(True)
        main_ui.weakLegPeakStrengthLabel_3.setObjectName("weakLegPeakStrengthLabel_3")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, main_ui.weakLegPeakStrengthLabel_3)
        
        main_ui.weakLegPeakStrengthLineEdit_3 = QtWidgets.QLineEdit(self.horizontalLayoutWidget_5)
        main_ui.weakLegPeakStrengthLineEdit_3.setObjectName("weakLegPeakStrengthLineEdit_3")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, main_ui.weakLegPeakStrengthLineEdit_3)
        
        self.verticalLayout_16.addLayout(self.formLayout_3)
        self.verticalLayout_16.setStretch(0, 1)
        self.verticalLayout_16.setStretch(1, 1)
        self.verticalLayout_16.setStretch(2, 5)
        self.horizontalLayout_10.addLayout(self.verticalLayout_16)
        self.horizontalLayout_10.setStretch(0, 3)
        self.horizontalLayout_10.setStretch(1, 2)
        self.verticalLayout_12.addLayout(self.horizontalLayout_10)
        self.verticalLayout_12.setStretch(0, 4)
        self.verticalLayout_12.setStretch(2, 3)
        self.horizontalLayout_8.addLayout(self.verticalLayout_12)
        self.horizontalLayout_8.setStretch(0, 2)
        self.horizontalLayout_8.setStretch(1, 3)

    def retranslate_step_1(self, main_ui):
        _translate = QtCore.QCoreApplication.translate
        main_ui.pushButton_2.setText(_translate("MainWindow", "Record"))
        main_ui.pushButton_21.setText(_translate("MainWindow", "Clear Data"))
        main_ui.label_4.setText(_translate("MainWindow", "Notes:"))
        main_ui.textEdit.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
 "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
 "p, li { white-space: pre-wrap; }\n"
 "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
 "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">A place for a clinician to note down any specific observations when performing the test</p>\n"
 "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        main_ui.label_5.setText(_translate("MainWindow", "Measurements:"))
        main_ui.label_16.setText(_translate("MainWindow", "Unaffected or strong leg extension"))
        main_ui.extensionForceLabel.setText(_translate("MainWindow", "Extension force:"))

    def retranslate_step_2(self, main_ui):
        _translate = QtCore.QCoreApplication.translate
        main_ui.pushButton_3.setText(_translate("MainWindow", "Record"))
        main_ui.pushButton_31.setText(_translate("MainWindow", "Clear Data"))
        main_ui.label_10.setText(_translate("MainWindow", "Notes:"))
        main_ui.textEdit_2.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
 "p, li { white-space: pre-wrap; }\n"
 "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
 "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">A place for a clinician to note down any specific observations when performing the test</p>\n"
 "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        main_ui.label_11.setText(_translate("MainWindow", "Measurements:"))
        main_ui.label_17.setText(_translate("MainWindow", "Affected or weak leg extension"))
        main_ui.strongLegAverageStrengthLabel_2.setText(_translate("MainWindow", "Force average:"))
        main_ui.strongLegPeakStrengthLabel_2.setText(_translate("MainWindow", "Force peak:\n(Affected leg\nvoluntary extension)"))

    def retranslate_step_3(self, main_ui):
        _translate = QtCore.QCoreApplication.translate
        main_ui.pushButton_4.setText(_translate("MainWindow", "Record"))
        main_ui.pushButton_41.setText(_translate("MainWindow", "Clear Data"))
        main_ui.label_14.setText(_translate("MainWindow", "Notes:"))
        main_ui.textEdit_6.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
 "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
 "p, li { white-space: pre-wrap; }\n"
 "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
 "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">A place for a clinician to note down any specific observations when performing the test</p>\n"
 "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        main_ui.label_15.setText(_translate("MainWindow", "Measurements:"))
        main_ui.weakLegPeakStrengthLabel_3.setText(_translate("MainWindow", "Affected leg involuntary extension:"))