from PyQt5 import QtCore, QtGui, QtWidgets

class ResultsTab:
    def setup_ui(self, main_ui, parent_widget):
        self.horizontalLayoutWidget_6 = QtWidgets.QWidget(parent_widget)
        self.horizontalLayoutWidget_6.setGeometry(QtCore.QRect(-1, -1, 1191, 801))
        self.horizontalLayoutWidget_6.setObjectName("horizontalLayoutWidget_6")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_6)
        self.horizontalLayout_11.setContentsMargins(20, 20, 20, 20)
        self.horizontalLayout_11.setSpacing(20)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        main_ui.label_19 = QtWidgets.QLabel(self.horizontalLayoutWidget_6)
        font = QtGui.QFont()
        font.setPointSize(32)
        font.setBold(True)
        font.setWeight(75)
        main_ui.label_19.setFont(font)
        main_ui.label_19.setObjectName("label_19")
        self.verticalLayout.addWidget(main_ui.label_19)
        
        self.formLayout_4 = QtWidgets.QFormLayout()
        self.formLayout_4.setVerticalSpacing(20)
        self.formLayout_4.setObjectName("formLayout_4")
        
        main_ui.unaffectedLegExtensionLLabel = QtWidgets.QLabel(self.horizontalLayoutWidget_6)
        main_ui.unaffectedLegExtensionLLabel.setObjectName("unaffectedLegExtensionLLabel")
        self.formLayout_4.setWidget(1, QtWidgets.QFormLayout.LabelRole, main_ui.unaffectedLegExtensionLLabel)
        
        main_ui.unaffectedLegExtensionLLineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget_6)
        main_ui.unaffectedLegExtensionLLineEdit.setReadOnly(True)
        main_ui.unaffectedLegExtensionLLineEdit.setObjectName("unaffectedLegExtensionLLineEdit")
        self.formLayout_4.setWidget(1, QtWidgets.QFormLayout.FieldRole, main_ui.unaffectedLegExtensionLLineEdit)
        
        main_ui.affectedLegVoluntaryExtensionLabel = QtWidgets.QLabel(self.horizontalLayoutWidget_6)
        main_ui.affectedLegVoluntaryExtensionLabel.setObjectName("affectedLegVoluntaryExtensionLabel")
        self.formLayout_4.setWidget(3, QtWidgets.QFormLayout.LabelRole, main_ui.affectedLegVoluntaryExtensionLabel)
        
        main_ui.affectedLegVoluntaryExtensionLineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget_6)
        main_ui.affectedLegVoluntaryExtensionLineEdit.setReadOnly(True)
        main_ui.affectedLegVoluntaryExtensionLineEdit.setObjectName("affectedLegVoluntaryExtensionLineEdit")
        self.formLayout_4.setWidget(3, QtWidgets.QFormLayout.FieldRole, main_ui.affectedLegVoluntaryExtensionLineEdit)
        
        main_ui.affectedLegInvoluntaryExtensionLabel = QtWidgets.QLabel(self.horizontalLayoutWidget_6)
        main_ui.affectedLegInvoluntaryExtensionLabel.setObjectName("affectedLegInvoluntaryExtensionLabel")
        self.formLayout_4.setWidget(4, QtWidgets.QFormLayout.LabelRole, main_ui.affectedLegInvoluntaryExtensionLabel)
        
        main_ui.affectedLegInvoluntaryExtensionLineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget_6)
        main_ui.affectedLegInvoluntaryExtensionLineEdit.setReadOnly(True)
        main_ui.affectedLegInvoluntaryExtensionLineEdit.setObjectName("affectedLegInvoluntaryExtensionLineEdit")
        self.formLayout_4.setWidget(4, QtWidgets.QFormLayout.FieldRole, main_ui.affectedLegInvoluntaryExtensionLineEdit)
        
        self.verticalLayout.addLayout(self.formLayout_4)
        main_ui.label_22 = QtWidgets.QLabel(self.horizontalLayoutWidget_6)
        main_ui.label_22.setFont(font)
        main_ui.label_22.setObjectName("label_22")
        self.verticalLayout.addWidget(main_ui.label_22)
        
        self.formLayout_5 = QtWidgets.QFormLayout()
        self.formLayout_5.setVerticalSpacing(20)
        self.formLayout_5.setObjectName("formLayout_5")
        self.formLayout_6 = QtWidgets.QFormLayout()
        self.formLayout_6.setObjectName("formLayout_6")
        self.formLayout_5.setLayout(0, QtWidgets.QFormLayout.LabelRole, self.formLayout_6)
        
        main_ui.involuntaryVoluntaryRatioAffectedLegLabel = QtWidgets.QLabel(self.horizontalLayoutWidget_6)
        main_ui.involuntaryVoluntaryRatioAffectedLegLabel.setObjectName("involuntaryVoluntaryRatioAffectedLegLabel")
        self.formLayout_5.setWidget(1, QtWidgets.QFormLayout.LabelRole, main_ui.involuntaryVoluntaryRatioAffectedLegLabel)
        
        main_ui.involuntaryVoluntaryRatioAffectedLegLineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget_6)
        main_ui.involuntaryVoluntaryRatioAffectedLegLineEdit.setReadOnly(True)
        main_ui.involuntaryVoluntaryRatioAffectedLegLineEdit.setObjectName("involuntaryVoluntaryRatioAffectedLegLineEdit")
        self.formLayout_5.setWidget(1, QtWidgets.QFormLayout.FieldRole, main_ui.involuntaryVoluntaryRatioAffectedLegLineEdit)
        
        main_ui.label_23 = QtWidgets.QLabel(self.horizontalLayoutWidget_6)
        font_it = QtGui.QFont()
        font_it.setItalic(True)
        main_ui.label_23.setFont(font_it)
        main_ui.label_23.setObjectName("label_23")
        self.formLayout_5.setWidget(2, QtWidgets.QFormLayout.LabelRole, main_ui.label_23)
        
        main_ui.label_24 = QtWidgets.QLabel(self.horizontalLayoutWidget_6)
        main_ui.label_24.setFont(font_it)
        main_ui.label_24.setObjectName("label_24")
        self.formLayout_5.setWidget(5, QtWidgets.QFormLayout.LabelRole, main_ui.label_24)

        self.verticalLayout.addLayout(self.formLayout_5)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 3)
        self.verticalLayout.setStretch(2, 1)
        self.verticalLayout.setStretch(3, 3)
        self.horizontalLayout_11.addLayout(self.verticalLayout)
        
        self.line_4 = QtWidgets.QFrame(self.horizontalLayoutWidget_6)
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.horizontalLayout_11.addWidget(self.line_4)
        
        self.verticalLayout_17 = QtWidgets.QVBoxLayout()
        self.verticalLayout_17.setObjectName("verticalLayout_17")
        
        main_ui.label_20 = QtWidgets.QLabel(self.horizontalLayoutWidget_6)
        main_ui.label_20.setFont(font)
        main_ui.label_20.setObjectName("label_20")
        self.verticalLayout_17.addWidget(main_ui.label_20)

        main_ui.pushButton_5 = QtWidgets.QPushButton(
            self.horizontalLayoutWidget_6,
            checkable=True,
            toggled=main_ui.fill_values
        )
        main_ui.pushButton_5.setObjectName("pushButton_5")
        font_16 = QtGui.QFont()
        font_16.setPointSize(16)
        main_ui.pushButton_5.setFont(font_16)
        self.verticalLayout_17.addWidget(main_ui.pushButton_5)

        main_ui.label_21 = QtWidgets.QLabel(self.horizontalLayoutWidget_6)
        main_ui.label_21.setScaledContents(True)
        main_ui.label_21.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        main_ui.label_21.setWordWrap(True)
        main_ui.label_21.setObjectName("label_21")
        self.verticalLayout_17.addWidget(main_ui.label_21)

        main_ui.label_25 = QtWidgets.QLabel(self.horizontalLayoutWidget_6)
        font_bold = QtGui.QFont()
        font_bold.setBold(True)
        main_ui.label_25.setFont(font_bold)
        main_ui.label_25.setObjectName("label_25")
        self.verticalLayout_17.addWidget(main_ui.label_25)

        main_ui.textEdit_7 = QtWidgets.QTextEdit(self.horizontalLayoutWidget_6)
        main_ui.textEdit_7.setObjectName("textEdit_7")
        self.verticalLayout_17.addWidget(main_ui.textEdit_7)
        self.verticalLayout_17.setStretch(0, 1)
        self.verticalLayout_17.setStretch(1, 4)
        self.verticalLayout_17.setStretch(2, 3)
        self.horizontalLayout_11.addLayout(self.verticalLayout_17)
        self.horizontalLayout_11.setStretch(0, 3)
        self.horizontalLayout_11.setStretch(2, 4)

    def retranslate_ui(self, main_ui):
        _translate = QtCore.QCoreApplication.translate
        main_ui.label_19.setText(_translate("MainWindow", "All Measurements:"))
        main_ui.unaffectedLegExtensionLLabel.setText(_translate("MainWindow", "Unaffected leg extension:"))
        main_ui.affectedLegVoluntaryExtensionLabel.setText(_translate("MainWindow", "Affected leg voluntary extension (V):"))
        main_ui.affectedLegInvoluntaryExtensionLabel.setText(_translate("MainWindow", "Affected leg involuntary extension (IV):"))
        main_ui.label_22.setText(_translate("MainWindow", "Calculations:"))
        main_ui.involuntaryVoluntaryRatioAffectedLegLabel.setText(_translate("MainWindow", "Involuntary/voluntary ratio (IVVR), affected leg:"))
        main_ui.label_23.setText(_translate("MainWindow", "IVVR = IV/V"))
        main_ui.label_20.setText(_translate("MainWindow", "Results and Analysis:"))
        main_ui.label_21.setText(_translate("MainWindow", "Press \"Calculate Results\" for an analysis of your tests."))
        main_ui.label_25.setText(_translate("MainWindow", "Observations:"))
        main_ui.textEdit_7.setHtml(_translate("MainWindow",
                                           "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                           "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                           "p, li { white-space: pre-wrap; }\n"
                                           "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
                                           "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">A place for a clinician to note down any specific observations and comments</p>\n"
                                           "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))

        main_ui.pushButton_5.setText(_translate("MainWindow", "Calculate Results"))