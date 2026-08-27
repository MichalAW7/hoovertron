from PyQt5 import QtCore, QtGui, QtWidgets

class ResultsTab:
    def setup_ui(self, main_ui, parent_widget):
        self.mainLayout = QtWidgets.QHBoxLayout(parent_widget)
        self.mainLayout.setContentsMargins(20, 20, 20, 20)
        self.mainLayout.setSpacing(20)
        
        # Left Column: Measurements and Calculations
        self.leftLayout = QtWidgets.QVBoxLayout()
        self.leftLayout.setSpacing(20)
        
        main_ui.label_19 = QtWidgets.QLabel("All Measurements")
        font = QtGui.QFont()
        font.setPointSize(28) # Increased font size for headings
        font.setBold(True)
        main_ui.label_19.setFont(font)
        self.leftLayout.addWidget(main_ui.label_19)
        
        # Measurements Group
        self.measureGroupBox = QtWidgets.QGroupBox("Raw Data")
        self.measureLayout = QtWidgets.QFormLayout(self.measureGroupBox)
        self.measureLayout.setVerticalSpacing(15)
        
        main_ui.unaffectedLegExtensionLLabel = QtWidgets.QLabel("Unaffected leg extension:")
        main_ui.unaffectedLegExtensionLLineEdit = QtWidgets.QLineEdit()
        main_ui.unaffectedLegExtensionLLineEdit.setReadOnly(True)
        self.measureLayout.addRow(main_ui.unaffectedLegExtensionLLabel, main_ui.unaffectedLegExtensionLLineEdit)
        
        main_ui.affectedLegVoluntaryExtensionLabel = QtWidgets.QLabel("Affected leg voluntary extension (V):")
        main_ui.affectedLegVoluntaryExtensionLineEdit = QtWidgets.QLineEdit()
        main_ui.affectedLegVoluntaryExtensionLineEdit.setReadOnly(True)
        self.measureLayout.addRow(main_ui.affectedLegVoluntaryExtensionLabel, main_ui.affectedLegVoluntaryExtensionLineEdit)
        
        main_ui.affectedLegInvoluntaryExtensionLabel = QtWidgets.QLabel("Affected leg involuntary extension (IV):")
        main_ui.affectedLegInvoluntaryExtensionLineEdit = QtWidgets.QLineEdit()
        main_ui.affectedLegInvoluntaryExtensionLineEdit.setReadOnly(True)
        self.measureLayout.addRow(main_ui.affectedLegInvoluntaryExtensionLabel, main_ui.affectedLegInvoluntaryExtensionLineEdit)
        
        self.leftLayout.addWidget(self.measureGroupBox)
        
        # Calculations Group
        self.calcGroupBox = QtWidgets.QGroupBox("Calculations")
        self.calcLayout = QtWidgets.QVBoxLayout(self.calcGroupBox)
        
        main_ui.label_22 = QtWidgets.QLabel("Calculations")
        main_ui.label_22.setVisible(False) # Hidden but kept
        
        self.calcFormLayout = QtWidgets.QFormLayout()
        
        main_ui.involuntaryVoluntaryRatioAffectedLegLabel = QtWidgets.QLabel("Involuntary/voluntary ratio (IVVR), affected leg:")
        main_ui.involuntaryVoluntaryRatioAffectedLegLineEdit = QtWidgets.QLineEdit()
        main_ui.involuntaryVoluntaryRatioAffectedLegLineEdit.setReadOnly(True)
        main_ui.involuntaryVoluntaryRatioAffectedLegLineEdit.setStyleSheet("font-weight: bold; font-size: 14pt; color: #0078d7;")
        self.calcFormLayout.addRow(main_ui.involuntaryVoluntaryRatioAffectedLegLabel, main_ui.involuntaryVoluntaryRatioAffectedLegLineEdit)
        
        self.calcLayout.addLayout(self.calcFormLayout)
        
        # --- BEAUTIFUL FORMULA SECTION START ---
        main_ui.label_23 = QtWidgets.QLabel()
        
        # We use an HTML table to create a vertical fraction structure.
        # This mimics LaTeX formatting: \frac{IV}{V}
        formula_html = (
            "<html><head/><body>"
            "<table border='0' cellspacing='0' cellpadding='0' style='color:#666666; font-size:16pt; font-family:Segoe UI, sans-serif;'>"
            "<tr>"
            # Rowspan=2 centers the 'IVVR =' vertically against the fraction
            "<td rowspan='2' valign='middle' align='right' style='padding-right:12px; font-weight:600; font-style:italic;'>IVVR &nbsp;=</td>"
            # Bottom border creates the fraction bar
            "<td align='center' style='border-bottom:2px solid #666666; padding-bottom:1px;'>IV</td>"
            "</tr>"
            "<tr>"
            # Denominator
            "<td align='center' style='padding-top:1px;'>V</td>"
            "</tr>"
            "</table>"
            "</body></html>"
        )
        main_ui.label_23.setText(formula_html)
        
        # Add widget with Center Alignment to make it look prominent
        self.calcLayout.addWidget(main_ui.label_23, 0, QtCore.Qt.AlignCenter)
        # --- BEAUTIFUL FORMULA SECTION END ---

        main_ui.label_24 = QtWidgets.QLabel("") # Placeholder
        main_ui.label_24.setVisible(False)
        
        self.leftLayout.addWidget(self.calcGroupBox)
        self.leftLayout.addStretch()
        
        self.mainLayout.addLayout(self.leftLayout, 1)
        
        # Vertical Line Separator
        self.line_4 = QtWidgets.QFrame()
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.mainLayout.addWidget(self.line_4)
        
        # Right Column: Analysis and Actions
        self.rightLayout = QtWidgets.QVBoxLayout()
        self.rightLayout.setSpacing(20)
        
        main_ui.label_20 = QtWidgets.QLabel("Results and Analysis")
        main_ui.label_20.setFont(font)
        self.rightLayout.addWidget(main_ui.label_20)
        
        # Actions
        main_ui.pushButton_5 = QtWidgets.QPushButton("Calculate Results")
        main_ui.pushButton_5.setCheckable(True)
        # Assuming main_ui.fill_values exists in the main class
        if hasattr(main_ui, 'fill_values'):
            main_ui.pushButton_5.toggled.connect(main_ui.fill_values)
        main_ui.pushButton_5.setStyleSheet("background-color: #0078d7; color: white; font-size: 16pt; padding: 15px;")
        self.rightLayout.addWidget(main_ui.pushButton_5)
        
        main_ui.label_21 = QtWidgets.QLabel("Press \"Calculate Results\" for an analysis of your tests.")
        main_ui.label_21.setWordWrap(True)
        self.rightLayout.addWidget(main_ui.label_21)
        
        # Observations
        self.obsGroupBox = QtWidgets.QGroupBox("Observations")
        self.obsLayout = QtWidgets.QVBoxLayout(self.obsGroupBox)
        
        main_ui.label_25 = QtWidgets.QLabel("Observations:")
        main_ui.label_25.setVisible(False)
        
        main_ui.textEdit_7 = QtWidgets.QTextEdit()
        main_ui.textEdit_7.setPlaceholderText("Enter specific observations and comments here...")
        self.obsLayout.addWidget(main_ui.textEdit_7)
        
        self.rightLayout.addWidget(self.obsGroupBox)
        self.rightLayout.addStretch()
        
        self.mainLayout.addLayout(self.rightLayout, 1)

    def retranslate_ui(self, main_ui):
        _translate = QtCore.QCoreApplication.translate
        main_ui.label_19.setText(_translate("MainWindow", "All Measurements"))
        main_ui.unaffectedLegExtensionLLabel.setText(_translate("MainWindow", "Unaffected leg extension:"))
        main_ui.affectedLegVoluntaryExtensionLabel.setText(_translate("MainWindow", "Affected leg voluntary extension (V):"))
        main_ui.affectedLegInvoluntaryExtensionLabel.setText(_translate("MainWindow", "Affected leg involuntary extension (IV):"))
        main_ui.involuntaryVoluntaryRatioAffectedLegLabel.setText(_translate("MainWindow", "Involuntary/voluntary ratio (IVVR), affected leg:"))
        
        # NOTE: We do NOT retranslate label_23 here because it uses HTML set in setup_ui. 
        # If you need to translate it, you must reconstruct the HTML string here.
        
        main_ui.label_20.setText(_translate("MainWindow", "Results and Analysis"))
        main_ui.label_21.setText(_translate("MainWindow", "Press \"Calculate Results\" for an analysis of your tests."))
        main_ui.pushButton_5.setText(_translate("MainWindow", "Calculate Results"))