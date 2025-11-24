# ui_layout.py
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QLineEdit, QPushButton
import pyqtgraph as pg

# Import the new modular components
from ui_components.patient_tab import PatientTab
from ui_components.step_tabs import StepTabs
from ui_components.results_tab import ResultsTab
from ui_components.menu_bar import MenuBar

class Ui_Layout(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 900)
        MainWindow.setMinimumSize(QtCore.QSize(1200, 900))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setMinimumSize(QtCore.QSize(1200, 900))
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")

        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 1200, 850))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setMinimumSize(QtCore.QSize(1200, 850))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.tabWidget.setFont(font)
        self.tabWidget.setStyleSheet("")
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.tabWidget.setUsesScrollButtons(False)
        self.tabWidget.setObjectName("tabWidget")

        # --- Tab 1: Patient Information ---
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.patient_tab_manager = PatientTab()
        self.patient_tab_manager.setup_ui(self, self.tab_3)
        self.tabWidget.addTab(self.tab_3, "")

        # --- Tab 2: Hoover's Sign Test Container ---
        self.tab = QtWidgets.QWidget()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.tab.setFont(font)
        self.tab.setStyleSheet("")
        self.tab.setObjectName("tab")
        
        self.tabWidget_2 = QtWidgets.QTabWidget(self.tab)
        self.tabWidget_2.setGeometry(QtCore.QRect(0, 0, 1200, 900))
        self.tabWidget_2.setMinimumSize(QtCore.QSize(1200, 900))
        self.tabWidget_2.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget_2.setUsesScrollButtons(False)
        self.tabWidget_2.setObjectName("tabWidget_2")

        # Create manager for Step tabs
        self.step_tabs_manager = StepTabs()

        # Step 1
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setMinimumSize(QtCore.QSize(1200, 800))
        self.tab_4.setObjectName("tab_4")
        self.step_tabs_manager.setup_step_1(self, self.tab_4)
        self.tabWidget_2.addTab(self.tab_4, "")

        # Step 2
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.step_tabs_manager.setup_step_2(self, self.tab_5)
        self.tabWidget_2.addTab(self.tab_5, "")

        # Step 3
        self.tab_6 = QtWidgets.QWidget()
        self.tab_6.setObjectName("tab_6")
        self.step_tabs_manager.setup_step_3(self, self.tab_6)
        self.tabWidget_2.addTab(self.tab_6, "")

        # --- Tab 3 (Nested): Results ---
        self.tab_7 = QtWidgets.QWidget()
        self.tab_7.setObjectName("tab_7")
        self.results_tab_manager = ResultsTab()
        self.results_tab_manager.setup_ui(self, self.tab_7)
        self.tabWidget_2.addTab(self.tab_7, "")

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        MainWindow.setCentralWidget(self.centralwidget)

        # --- Menu Bar ---
        self.menu_manager = MenuBar()
        self.menu_manager.setup_ui(self, MainWindow)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # --- Post-Setup Logic (Plots and Region Selectors) ---
        self.plot_region = [self.graphWidget_hs1.plotItem,
                         self.graphWidget_hs2.plotItem,
                         self.graphWidget_hs3.plotItem]

        self.selection_region = [pg.LinearRegionItem() for _ in range(3)]
        for region, plot_region in zip(self.selection_region, self.plot_region):
            plot_region.addItem(region)
            region.sigRegionChanged.connect(self.update_selection)
        
        # Initialize lists for input handling
        if not hasattr(self, 'start_time_input'): self.start_time_input = [[] for _ in range(3)]
        if not hasattr(self, 'end_time_input'): self.end_time_input = [[] for _ in range(3)]
        if not hasattr(self, 'select_button'): self.select_button = [[] for _ in range(3)]
        if not hasattr(self, 'data_x'): self.data_x = [[] for _ in range(3)]
        if not hasattr(self, 'data_y'): self.data_y = [[] for _ in range(3)]

        for i in range(3):
            start_time_input = QLineEdit(MainWindow)
            start_time_input.setPlaceholderText('Start Time')
            self.start_time_input[i].append(start_time_input)

            end_time_input = QLineEdit(MainWindow)
            end_time_input.setPlaceholderText('End Time')
            self.end_time_input[i].append(end_time_input)

            select_button = QPushButton('Select Time Period', MainWindow)
            select_button.setStyleSheet("background-color: red;color: white; font-weight: bold; font-size: 16px;")
            select_button.clicked.connect(self.select_time_period)
            self.select_button[i].append(select_button)

        for i, layout in enumerate([self.horizontalLayout_s1, self.horizontalLayout_s2, self.horizontalLayout_s3]):
            for start_input, end_input, select_button in zip(self.start_time_input[i], self.end_time_input[i], self.select_button[i]):
                layout.addWidget(start_input)
                layout.addWidget(end_input)
                layout.addWidget(select_button)
                self.data_x[i].append([])
                self.data_y[i].append([])

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        
        # Call retranslate on components
        self.patient_tab_manager.retranslate_ui(self)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Patient Information"))
        
        self.step_tabs_manager.retranslate_step_1(self)
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_4), _translate("MainWindow", "Step 1"))
        
        self.step_tabs_manager.retranslate_step_2(self)
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_5), _translate("MainWindow", "Step 2"))
        
        self.step_tabs_manager.retranslate_step_3(self)
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_6), _translate("MainWindow", "Step 3"))
        
        self.results_tab_manager.retranslate_ui(self)
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_7), _translate("MainWindow", "Results"))
        
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Hoover\'s Sign Test"))
        
        self.menu_manager.retranslate_ui(self)