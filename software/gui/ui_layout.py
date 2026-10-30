# ui_layout.py
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QLineEdit, QPushButton
import pyqtgraph as pg

from ui_components.patient_tab import PatientTab
from ui_components.step_tabs import StepTabs, apply_graph_theme
from ui_components.results_tab import ResultsTab
from ui_components.menu_bar import MenuBar
from ui_components import theme




WORKFLOW_TABS = [
    # (attr_name, tab_id, label, subtitle, step_index)
    ("tab_3", "patient",          "Patient Info",  "Demographics & visit", None),
    ("tab_5", "step_2",           "Step 1",        "Affected leg push",    1),
    ("tab_6", "step_3",           "Step 2",        "Hoover's sign test",   2),
    ("tab_7", "results",          "Results",       "Analysis & IVVR",      None),
    ("tab_4", "optional_step_1",  "Optional Step", "Optional: unaffected leg", 0),
]


class Ui_Layout(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 880)
        MainWindow.setMinimumSize(QtCore.QSize(1180, 780))

        self._apply_theme(MainWindow)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.centralLayout.setContentsMargins(14, 14, 14, 14)
        self.centralLayout.setSpacing(0)

        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.tabBar().setExpanding(False)
        self.tabWidget.tabBar().setDrawBase(False)
        self.tabWidget.setDocumentMode(False)
        self.centralLayout.addWidget(self.tabWidget, 1)

        self.tabWidget_2 = self.tabWidget  # back-compat alias
        self.workflow_tab_indices_by_id = {}
        self.workflow_tab_ids_by_index = {}
        self.workflow_step_by_tab_index = {}

        # Create per-tab widgets and managers
        self.patient_tab_manager = PatientTab()
        self.step_tabs_manager = StepTabs()
        self.results_tab_manager = ResultsTab()

        setup_fns = {
            "patient":          lambda w: self.patient_tab_manager.setup_ui(self, w),
            "step_2":           lambda w: self.step_tabs_manager.setup_step_2(self, w),
            "step_3":           lambda w: self.step_tabs_manager.setup_step_3(self, w),
            "results":          lambda w: self.results_tab_manager.setup_ui(self, w),
            "optional_step_1":  lambda w: self.step_tabs_manager.setup_step_1(self, w),
        }

        for attr, tab_id, label, subtitle, step_index in WORKFLOW_TABS:
            widget = QtWidgets.QWidget()
            widget.setObjectName(attr)
            setattr(self, attr, widget)
            setup_fns[tab_id](widget)
            self._add_workflow_tab(widget, tab_id, step_index=step_index)

        MainWindow.setCentralWidget(self.centralwidget)

        # ---- Tab corner widget (Save / Clear) ------------------------------
        self._setup_tab_corner_actions()

        # ---- Menu Bar ------------------------------------------------------
        self.menu_manager = MenuBar()
        self.menu_manager.setup_ui(self, MainWindow)
        self._setup_connection_indicator()

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.update_step_tab_action_state(self.tabWidget.currentIndex())
        self.tabWidget.currentChanged.connect(self.update_step_tab_action_state)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # ---- Post-setup: plot regions and time-period inputs ---------------
        self.plot_region = [
            self.graphWidget_hs1.plotItem,
            self.graphWidget_hs2.plotItem,
            self.graphWidget_hs3.plotItem,
        ]

        region_color = theme.palette()["graph_region"]
        self.selection_region = []
        for step_index, plot_region in enumerate(self.plot_region):
            region = pg.LinearRegionItem(brush=pg.mkBrush(*region_color))
            plot_region.addItem(region)
            region.sigRegionChanged.connect(
                lambda *_, step_index=step_index: self.update_selection(step_index)
            )
            self.selection_region.append(region)

        if not hasattr(self, 'start_time_input'): self.start_time_input = [[] for _ in range(3)]
        if not hasattr(self, 'end_time_input'): self.end_time_input = [[] for _ in range(3)]
        if not hasattr(self, 'select_button'): self.select_button = [[] for _ in range(3)]
        if not hasattr(self, 'data_x'): self.data_x = [[] for _ in range(3)]
        if not hasattr(self, 'data_y'): self.data_y = [[] for _ in range(3)]

        for i in range(3):
            start_time_input = QLineEdit()
            start_time_input.setPlaceholderText('Start Time')
            start_time_input.setMaximumWidth(110)
            self.start_time_input[i].append(start_time_input)

            end_time_input = QLineEdit()
            end_time_input.setPlaceholderText('End Time')
            end_time_input.setMaximumWidth(110)
            self.end_time_input[i].append(end_time_input)

            select_button = QPushButton('Apply')
            select_button.setProperty("variant", "ghost")
            select_button.setCursor(QtCore.Qt.PointingHandCursor)
            select_button.setToolTip("Apply selected time range")
            select_button.setFixedSize(174, 38)
            select_button.clicked.connect(self.select_time_period)
            self.select_button[i].append(select_button)

        for i, layout in enumerate([self.horizontalLayout_s1, self.horizontalLayout_s2, self.horizontalLayout_s3]):
            for start_input, end_input, btn in zip(
                self.start_time_input[i], self.end_time_input[i], self.select_button[i]
            ):
                layout.addWidget(start_input)
                layout.addWidget(end_input)
                layout.addWidget(btn)
                self.data_x[i].append([])
                self.data_y[i].append([])

    # ------------------------------------------------------------------
    # Theme
    # ------------------------------------------------------------------
    def _apply_theme(self, MainWindow):
        self._theme_mode = getattr(self, "_theme_mode", "light")
        theme.set_mode(self._theme_mode)
        sheet = theme.build_stylesheet()
        MainWindow.setStyleSheet(sheet)
        app = QtWidgets.QApplication.instance()
        if app is not None:
            app.setStyleSheet(sheet)

    def apply_theme_mode(self, mode):
        """Public: switch between 'light' and 'dark' and repaint everything."""
        self._theme_mode = mode
        theme.set_mode(mode)
        sheet = theme.build_stylesheet()
        win = self.centralwidget.window()
        win.setStyleSheet(sheet)
        app = QtWidgets.QApplication.instance()
        if app is not None:
            app.setStyleSheet(sheet)

        # Repaint graphs and region brushes
        region_color = theme.palette()["graph_region"]
        for plot in (
            getattr(self, "graphWidget_hs1", None),
            getattr(self, "graphWidget_hs2", None),
            getattr(self, "graphWidget_hs3", None),
        ):
            if plot is not None:
                apply_graph_theme(plot)
        for region in getattr(self, "selection_region", []):
            region.setBrush(pg.mkBrush(*region_color))

        # Re-style the connection indicator
        self.update_connection_indicator()
        # Refresh dashboard if present
        if hasattr(self, "results_tab_manager"):
            self.results_tab_manager.refresh_theme(self)

    # ------------------------------------------------------------------
    # Tab-bar corner widget (Save / Clear)
    # ------------------------------------------------------------------
    def _setup_tab_corner_actions(self):
        # Match the rendered tab height so buttons read as inline siblings
        # of the tab buttons rather than floating chips.
        TAB_BAND_HEIGHT = 36
        BUTTON_WIDTH = 88
        BUTTON_HEIGHT = 32

        corner = QtWidgets.QWidget()
        corner.setObjectName("tabCornerActions")
        corner.setFixedHeight(TAB_BAND_HEIGHT)
        corner.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        layout = QtWidgets.QHBoxLayout(corner)
        layout.setContentsMargins(0, 2, 0, 2)
        layout.setSpacing(6)
        layout.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)

        self.stepTabSaveButton = QtWidgets.QPushButton("Save")
        self.stepTabSaveButton.setCursor(QtCore.Qt.PointingHandCursor)
        self.stepTabSaveButton.setAutoDefault(False)
        self.stepTabSaveButton.setFixedSize(BUTTON_WIDTH, BUTTON_HEIGHT)
        self.stepTabSaveButton.clicked.connect(lambda checked=False: self.file_save())
        layout.addWidget(self.stepTabSaveButton, 0, QtCore.Qt.AlignVCenter)

        self.stepTabClearButton = QtWidgets.QPushButton("Clear")
        self.stepTabClearButton.setProperty("variant", "ghost")
        self.stepTabClearButton.setCursor(QtCore.Qt.PointingHandCursor)
        self.stepTabClearButton.setAutoDefault(False)
        self.stepTabClearButton.setFixedSize(BUTTON_WIDTH, BUTTON_HEIGHT)
        self.stepTabClearButton.clicked.connect(
            lambda checked=False: self._confirm_clear_current_step()
        )
        layout.addWidget(self.stepTabClearButton, 0, QtCore.Qt.AlignVCenter)

        self.tabWidget.setCornerWidget(corner, QtCore.Qt.TopRightCorner)

    def _confirm_clear_current_step(self):
        if not self.stepTabClearButton.isEnabled():
            return
        if not getattr(self, "_clear_confirmations_enabled", True):
            self.clear_current_step()
            return
        reply = QtWidgets.QMessageBox.question(
            self.centralwidget.window(),
            "Clear step data?",
            "This will remove the recorded data and notes for the current step. Continue?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel,
            QtWidgets.QMessageBox.Cancel,
        )
        if reply == QtWidgets.QMessageBox.Yes:
            self.clear_current_step()

    # ------------------------------------------------------------------
    # Workflow tab utilities (preserved API)
    # ------------------------------------------------------------------
    def _add_workflow_tab(self, widget, tab_id, step_index=None):
        index = self.tabWidget.addTab(widget, "")
        self.workflow_tab_indices_by_id[tab_id] = index
        self.workflow_tab_ids_by_index[index] = tab_id
        if step_index is not None:
            self.workflow_step_by_tab_index[index] = step_index
        return index

    def get_current_workflow_tab_id(self):
        return self.workflow_tab_ids_by_index.get(self.tabWidget.currentIndex(), "patient")

    def set_workflow_tab_by_id(self, tab_id):
        tab_aliases = {
            "step_1": "optional_step_1",
            "step_1_optional": "optional_step_1",
            "hoovers_sign_test": "step_2",
        }
        resolved_tab_id = tab_aliases.get(tab_id, tab_id)
        target_index = self.workflow_tab_indices_by_id.get(resolved_tab_id)
        if target_index is not None:
            self.tabWidget.setCurrentIndex(target_index)

    def get_workflow_tab_id_from_legacy_state(self, main_tab_index=0, test_tab_index=0):
        if main_tab_index == 0:
            return "patient"
        return {
            0: "optional_step_1",
            1: "step_2",
            2: "step_3",
            3: "results",
        }.get(test_tab_index, "step_2")

    def get_active_step_index(self):
        return self.workflow_step_by_tab_index.get(self.tabWidget.currentIndex())

    # ------------------------------------------------------------------
    # Connection indicator
    # ------------------------------------------------------------------
    def _setup_connection_indicator(self):
        self.connectionIndicatorWidget = QtWidgets.QWidget(self.statusbar)
        self.connectionIndicatorWidget.setObjectName("connectionIndicatorWidget")

        layout = QtWidgets.QHBoxLayout(self.connectionIndicatorWidget)
        layout.setContentsMargins(8, 0, 8, 0)
        layout.setSpacing(6)

        self.connectionIndicatorDot = QtWidgets.QLabel(self.connectionIndicatorWidget)
        self.connectionIndicatorDot.setObjectName("connectionIndicatorDot")
        self.connectionIndicatorDot.setFixedSize(8, 8)
        layout.addWidget(self.connectionIndicatorDot, 0, QtCore.Qt.AlignVCenter)

        self.connectionIndicatorLabel = QtWidgets.QLabel(
            "Disconnected", self.connectionIndicatorWidget
        )
        self.connectionIndicatorLabel.setObjectName("connectionIndicatorLabel")
        layout.addWidget(self.connectionIndicatorLabel, 0, QtCore.Qt.AlignVCenter)

        self.statusbar.addPermanentWidget(self.connectionIndicatorWidget)
        self.statusbar.setSizeGripEnabled(False)
        self.update_connection_indicator(False)

    def update_connection_indicator(self, connected=None, connection_type=None, detail=""):
        if not hasattr(self, "connectionIndicatorWidget"):
            return

        if connected is None:
            connected = getattr(self, "is_connected", False)
        connection_type = connection_type or getattr(self, "connection_type", None) or "Device"

        p = theme.palette()
        if connected:
            text = f"{connection_type} connected"
            tooltip = f"Connected to {detail}" if detail else text
            dot_color = p["success"]
            label_color = p["text"]
        else:
            text = "Disconnected"
            tooltip = "No HooverTron device is connected."
            dot_color = p["text_subtle"]
            label_color = p["text_muted"]

        self.connectionIndicatorLabel.setText(text)
        self.connectionIndicatorWidget.setToolTip(tooltip)
        # Transparent container, no pill background
        self.connectionIndicatorWidget.setStyleSheet("background: transparent;")
        self.connectionIndicatorDot.setStyleSheet(
            f"background-color: {dot_color}; border-radius: 4px;"
        )
        self.connectionIndicatorLabel.setStyleSheet(
            f"color: {label_color}; font-size: 12px; font-style: italic;"
        )

    def update_step_tab_action_state(self, current_index):
        is_step_tab = self.workflow_step_by_tab_index.get(current_index) is not None
        self.stepTabClearButton.setEnabled(is_step_tab)
        self.stepTabClearButton.setToolTip(
            "" if is_step_tab else "Select a measurement step to clear its data."
        )
        if self.workflow_tab_ids_by_index.get(current_index) == "results":
            self.fill_values()

    # ------------------------------------------------------------------
    # Translations / labels
    # ------------------------------------------------------------------
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "HooverTron"))

        self.patient_tab_manager.retranslate_ui(self)
        self.step_tabs_manager.retranslate_step_1(self)
        self.step_tabs_manager.retranslate_step_2(self)
        self.step_tabs_manager.retranslate_step_3(self)
        self.results_tab_manager.retranslate_ui(self)

        for _attr, tab_id, label, _sub, _step in WORKFLOW_TABS:
            idx = self.workflow_tab_indices_by_id.get(tab_id)
            if idx is None:
                continue
            self.tabWidget.setTabText(idx, _translate("MainWindow", label))

        self.menu_manager.retranslate_ui(self)
