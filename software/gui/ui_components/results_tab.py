from PyQt5 import QtCore, QtGui, QtWidgets

from ui_components import theme


GAUGE_MIN = 0.0
GAUGE_MAX = 4.0


class IvvrGauge(QtWidgets.QWidget):
    """Neutral IVVR position indicator without diagnostic cutoffs."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._value = None
        self.setMinimumHeight(46)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

    def setValue(self, value):
        self._value = value
        self.update()

    def paintEvent(self, event):
        p = theme.palette()
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        rect = self.rect().adjusted(4, 18, -4, -18)
        bar_h = rect.height()
        radius = bar_h / 2

        total = GAUGE_MAX - GAUGE_MIN
        x = rect.left()
        y = rect.top()
        w = rect.width()

        # Background pill
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtGui.QColor(p["surface_sunken"]))
        painter.drawRoundedRect(rect, radius, radius)

        # Indicator
        if self._value is not None:
            v = max(GAUGE_MIN, min(GAUGE_MAX, self._value))
            vx = x + (v - GAUGE_MIN) / total * w
            fill = QtGui.QColor(p["border_emphasis"])
            fill.setAlpha(120)
            painter.setBrush(fill)
            painter.setPen(QtCore.Qt.NoPen)
            painter.drawRoundedRect(
                QtCore.QRectF(x, y, max(0, vx - x), bar_h), radius, radius
            )
            # Drop shadow
            shadow = QtGui.QColor(0, 0, 0, 60)
            painter.setBrush(shadow)
            painter.setPen(QtCore.Qt.NoPen)
            painter.drawEllipse(QtCore.QPointF(vx, y + bar_h / 2 + 1), 10, 10)
            painter.setBrush(QtGui.QColor(p["surface"]))
            painter.setPen(QtGui.QPen(QtGui.QColor(p["text"]), 2))
            painter.drawEllipse(QtCore.QPointF(vx, y + bar_h / 2), 9, 9)
            # Top label
            painter.setPen(QtGui.QPen(QtGui.QColor(p["text"])))
            font = QtGui.QFont("Segoe UI", 9, QtGui.QFont.Bold)
            painter.setFont(font)
            painter.drawText(
                QtCore.QRectF(vx - 40, y - 18, 80, 14),
                QtCore.Qt.AlignCenter,
                f"{self._value:.2f}",
            )

        painter.end()


def _ivvr_classification(ivvr):
    """Return (label, color_key, helper_text) for the current IVVR value."""
    if ivvr is None:
        return ("Awaiting data", "text_subtle",
                "Record Step 1 and Step 2 to see the analysis.")
    return ("IVVR recorded", "text_muted",
            "Review this value alongside the full clinical picture.")


class ResultsTab:
    def setup_ui(self, main_ui, parent_widget):
        self._main_ui = main_ui

        outer = QtWidgets.QHBoxLayout(parent_widget)
        outer.setContentsMargins(24, 24, 24, 24)
        outer.setSpacing(20)

        # ------------------------------------------------------------------
        # Left column: raw data + formula
        # ------------------------------------------------------------------
        leftColumn = QtWidgets.QVBoxLayout()
        leftColumn.setSpacing(16)

        rawCard = QtWidgets.QFrame(parent_widget)
        rawCard.setProperty("card", True)
        rawCardLayout = QtWidgets.QVBoxLayout(rawCard)
        rawCardLayout.setContentsMargins(20, 20, 20, 20)
        rawCardLayout.setSpacing(8)

        eyebrow = QtWidgets.QLabel("Captured forces")
        eyebrow.setProperty("role", "eyebrow")
        rawCardLayout.addWidget(eyebrow)
        main_ui.label_19 = eyebrow  # back-compat ref

        # Mini grid of values
        gridForm = QtWidgets.QFormLayout()
        gridForm.setContentsMargins(0, 4, 0, 0)
        gridForm.setVerticalSpacing(10)
        gridForm.setHorizontalSpacing(16)

        def _row(label_text):
            lbl = QtWidgets.QLabel(label_text)
            lbl.setProperty("role", "row-label")
            edit = QtWidgets.QLineEdit()
            edit.setReadOnly(True)
            edit.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            edit.setMaximumWidth(160)
            edit.setProperty("role", "row-value")
            gridForm.addRow(lbl, edit)
            return lbl, edit

        main_ui.unaffectedLegExtensionLLabel, main_ui.unaffectedLegExtensionLLineEdit = _row("Unaffected leg (baseline)")
        main_ui.affectedLegVoluntaryExtensionLabel, main_ui.affectedLegVoluntaryExtensionLineEdit = _row("Voluntary push (V)")
        main_ui.affectedLegInvoluntaryExtensionLabel, main_ui.affectedLegInvoluntaryExtensionLineEdit = _row("Involuntary push (IV)")

        rawCardLayout.addLayout(gridForm)
        leftColumn.addWidget(rawCard)

        # Formula card
        formulaCard = QtWidgets.QFrame(parent_widget)
        formulaCard.setProperty("card", "muted")
        formulaLayout = QtWidgets.QVBoxLayout(formulaCard)
        formulaLayout.setContentsMargins(20, 18, 20, 18)
        formulaLayout.setSpacing(6)

        formulaEyebrow = QtWidgets.QLabel("How it's calculated")
        formulaEyebrow.setProperty("role", "eyebrow")
        formulaLayout.addWidget(formulaEyebrow)

        formula_label = QtWidgets.QLabel()
        formula_label.setAlignment(QtCore.Qt.AlignCenter)
        formula_label.setText(self._formula_html())
        formulaLayout.addWidget(formula_label)
        self._formula_label = formula_label
        main_ui.label_23 = formula_label  # back-compat

        helper = QtWidgets.QLabel(
            "IVVR = Involuntary peak ÷ Voluntary peak. Use this value as one part "
            "of the wider clinical assessment."
        )
        helper.setWordWrap(True)
        helper.setProperty("role", "subtitle")
        formulaLayout.addWidget(helper)
        leftColumn.addWidget(formulaCard)

        leftColumn.addStretch(1)
        outer.addLayout(leftColumn, 4)

        # Vertical divider
        vline = QtWidgets.QFrame()
        vline.setProperty("role", "vdivider")
        vline.setFrameShape(QtWidgets.QFrame.NoFrame)
        vline.setFixedWidth(1)
        outer.addWidget(vline)
        main_ui.line_4 = vline  # back-compat

        # ------------------------------------------------------------------
        # Right column: hero dashboard
        # ------------------------------------------------------------------
        rightColumn = QtWidgets.QVBoxLayout()
        rightColumn.setSpacing(14)

        heroCard = QtWidgets.QFrame(parent_widget)
        heroCard.setObjectName("ivvrHero")
        heroCard.setProperty("card", True)
        heroLayout = QtWidgets.QVBoxLayout(heroCard)
        heroLayout.setContentsMargins(24, 22, 24, 22)
        heroLayout.setSpacing(10)

        heroEyebrow = QtWidgets.QLabel("Hoover's Sign · Analysis")
        heroEyebrow.setProperty("role", "eyebrow")
        heroLayout.addWidget(heroEyebrow)

        valueRow = QtWidgets.QHBoxLayout()
        valueRow.setSpacing(14)
        valueRow.setAlignment(QtCore.Qt.AlignVCenter)

        # Large value
        self.ivvrValue = QtWidgets.QLabel("–")
        self.ivvrValue.setObjectName("ivvrValue")
        self.ivvrValue.setStyleSheet(
            "font-size: 44px; font-weight: 500; letter-spacing: -0.5px;"
        )
        self.ivvrValue.setMinimumWidth(140)
        self.ivvrValue.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        valueRow.addWidget(self.ivvrValue)

        valueColumn = QtWidgets.QVBoxLayout()
        valueColumn.setContentsMargins(0, 6, 0, 0)
        valueColumn.setSpacing(4)
        self.ivvrLabel = QtWidgets.QLabel("IVVR")
        self.ivvrLabel.setProperty("role", "metric-label")
        self.ivvrBadge = QtWidgets.QLabel("Awaiting data")
        self.ivvrBadge.setStyleSheet(theme.chip_style("primary"))
        self.ivvrBadge.setAlignment(QtCore.Qt.AlignCenter)
        self.ivvrBadge.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        valueColumn.addWidget(self.ivvrLabel)
        valueColumn.addWidget(self.ivvrBadge, 0, QtCore.Qt.AlignLeft)
        valueColumn.addStretch(1)
        valueRow.addLayout(valueColumn)
        valueRow.addStretch(1)
        heroLayout.addLayout(valueRow)

        # Gauge band
        self.gauge = IvvrGauge()
        heroLayout.addWidget(self.gauge)

        # Interpretation paragraph
        DEFAULT_ANALYSIS_TEXT = "Record Step 1 and Step 2 to see the analysis."
        self.interpretation = QtWidgets.QLabel(DEFAULT_ANALYSIS_TEXT)
        self.interpretation.setWordWrap(True)
        self.interpretation.setProperty("role", "subtitle")
        heroLayout.addWidget(self.interpretation)
        main_ui.label_21 = self.interpretation  # back-compat – backend writes to .setText

        # Patch fill_values so it also drives gauge/badge when new values land
        self._patch_main_ui_for_dashboard(main_ui)

        # Hidden compat field (backend uses .setText / .clear / .text())
        main_ui.involuntaryVoluntaryRatioAffectedLegLineEdit = _ProxyIvvrLineEdit(self)

        rightColumn.addWidget(heroCard, 0)

        # Action buttons row
        actionsRow = QtWidgets.QHBoxLayout()
        actionsRow.setSpacing(10)
        main_ui.pushButton_5 = QtWidgets.QPushButton()
        main_ui.pushButton_5.setVisible(False)

        main_ui.clearAllTestDataButton = QtWidgets.QPushButton("Clear All")
        main_ui.clearAllTestDataButton.setProperty("variant", "danger")
        main_ui.clearAllTestDataButton.setCursor(QtCore.Qt.PointingHandCursor)
        main_ui.clearAllTestDataButton.clicked.connect(
            lambda: self._confirm_clear_all(main_ui)
        )
        actionsRow.addWidget(main_ui.clearAllTestDataButton, 1)

        main_ui.newPatientResultsButton = QtWidgets.QPushButton("New Patient")
        main_ui.newPatientResultsButton.setProperty("variant", "ghost")
        main_ui.newPatientResultsButton.setCursor(QtCore.Qt.PointingHandCursor)
        main_ui.newPatientResultsButton.clicked.connect(
            lambda: self._confirm_new_patient(main_ui)
        )
        actionsRow.addWidget(main_ui.newPatientResultsButton, 1)
        rightColumn.addLayout(actionsRow)

        self.powerReminderCard = QtWidgets.QFrame(parent_widget)
        self.powerReminderCard.setObjectName("powerReminderCard")
        self.powerReminderCard.setMinimumHeight(128)
        powerLayout = QtWidgets.QVBoxLayout(self.powerReminderCard)
        powerLayout.setContentsMargins(20, 18, 20, 18)
        powerLayout.setSpacing(8)

        self.powerReminderTitle = QtWidgets.QLabel("DEVICE POWER REMINDER")
        powerLayout.addWidget(self.powerReminderTitle)

        self.powerReminderMessage = QtWidgets.QLabel(
            "Before leaving, switch off HooverTron by double-pressing the power button on the battery pack."
        )
        self.powerReminderMessage.setWordWrap(True)
        powerLayout.addWidget(self.powerReminderMessage)

        self.powerReminderSubtext = QtWidgets.QLabel(
            "Confirm the battery pack is off at the end of the session."
        )
        self.powerReminderSubtext.setWordWrap(True)
        powerLayout.addWidget(self.powerReminderSubtext)
        self._apply_power_reminder_style()
        rightColumn.addWidget(self.powerReminderCard, 0)

        # Observations card
        obsCard = QtWidgets.QFrame(parent_widget)
        obsCard.setProperty("card", True)
        obsLayout = QtWidgets.QVBoxLayout(obsCard)
        obsLayout.setContentsMargins(18, 16, 18, 16)
        obsLayout.setSpacing(8)
        obsEyebrow = QtWidgets.QLabel("Observations")
        obsEyebrow.setProperty("role", "eyebrow")
        obsLayout.addWidget(obsEyebrow)
        main_ui.textEdit_7 = QtWidgets.QTextEdit()
        main_ui.textEdit_7.setPlaceholderText("Clinical observations, follow-up notes…")
        obsLayout.addWidget(main_ui.textEdit_7, 1)
        rightColumn.addWidget(obsCard, 1)

        outer.addLayout(rightColumn, 5)

        # Hidden / back-compat labels
        main_ui.label_22 = QtWidgets.QLabel(); main_ui.label_22.setVisible(False)
        main_ui.label_24 = QtWidgets.QLabel(); main_ui.label_24.setVisible(False)
        main_ui.label_25 = QtWidgets.QLabel(); main_ui.label_25.setVisible(False)
        main_ui.label_20 = QtWidgets.QLabel(); main_ui.label_20.setVisible(False)
        main_ui.involuntaryVoluntaryRatioAffectedLegLabel = QtWidgets.QLabel()
        main_ui.involuntaryVoluntaryRatioAffectedLegLabel.setVisible(False)

        # Initialize dashboard state
        self.set_ivvr(None)

    # ------------------------------------------------------------------
    # Dashboard plumbing
    # ------------------------------------------------------------------
    def set_ivvr(self, ivvr):
        """Update the gauge, badge and large value."""
        label, color_key, helper = _ivvr_classification(ivvr)
        self.ivvrBadge.setText(label.upper())
        self.ivvrBadge.setStyleSheet(theme.chip_style(color_key))
        base_style = "font-size: 44px; font-weight: 500; letter-spacing: -0.5px;"
        if ivvr is None:
            self.ivvrValue.setText("–")
            self.ivvrValue.setStyleSheet(
                base_style + f"color: {theme.palette()['text_subtle']};"
            )
        else:
            self.ivvrValue.setText(f"{ivvr:.2f}")
            self.ivvrValue.setStyleSheet(base_style + f"color: {theme.palette()['text']};")
        self.gauge.setValue(ivvr)

    def _apply_power_reminder_style(self):
        p = theme.palette()
        self.powerReminderCard.setStyleSheet(
            f"""
            QFrame#powerReminderCard {{
                background-color: {p['warning_soft']};
                border: 1px solid {p['warning']};
                border-radius: 10px;
            }}
            """
        )
        self.powerReminderTitle.setStyleSheet(
            f"color: {p['warning']}; font-size: 12px; font-weight: 700; letter-spacing: 0.8px;"
        )
        self.powerReminderMessage.setStyleSheet(
            f"color: {p['text']}; font-size: 20px; font-weight: 650; line-height: 1.25;"
        )
        self.powerReminderSubtext.setStyleSheet(
            f"color: {p['text_muted']}; font-size: 13px;"
        )

    def _patch_main_ui_for_dashboard(self, main_ui):
        """Re-route fill_values / clear_all_test_data so the dashboard stays in sync."""

        original_fill = getattr(main_ui, "fill_values", None)
        if callable(original_fill) and not getattr(original_fill, "_patched", False):
            tab = self

            def patched_fill(*args, **kwargs):
                result = original_fill(*args, **kwargs)
                tab._sync_from_main_ui(main_ui)
                return result

            patched_fill._patched = True
            main_ui.fill_values = patched_fill

        original_clear = getattr(main_ui, "clear_all_test_data", None)
        if callable(original_clear) and not getattr(original_clear, "_patched", False):
            tab = self

            def patched_clear(*args, **kwargs):
                result = original_clear(*args, **kwargs)
                tab.set_ivvr(None)
                return result

            patched_clear._patched = True
            main_ui.clear_all_test_data = patched_clear

    def _sync_from_main_ui(self, main_ui):
        proxy = main_ui.involuntaryVoluntaryRatioAffectedLegLineEdit
        try:
            value = float(proxy.text())
        except (TypeError, ValueError):
            value = None
        self.set_ivvr(value)

    # ------------------------------------------------------------------
    # Confirm dialogs
    # ------------------------------------------------------------------
    def _confirm_clear_all(self, main_ui):
        parent = main_ui.clearAllTestDataButton.window()
        if not getattr(main_ui, "_clear_confirmations_enabled", True):
            return main_ui.clear_all_test_data()
        reply = QtWidgets.QMessageBox.question(
            parent,
            "Clear all test data?",
            "This removes the recordings, notes and analysis for every step. "
            "Patient demographics are kept.",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel,
            QtWidgets.QMessageBox.Cancel,
        )
        if reply == QtWidgets.QMessageBox.Yes:
            main_ui.clear_all_test_data()

    def _confirm_new_patient(self, main_ui):
        parent = main_ui.newPatientResultsButton.window()
        if not getattr(main_ui, "_clear_confirmations_enabled", True):
            return main_ui.new_patient()

        dialog = QtWidgets.QDialog(parent)
        dialog.setWindowTitle("Start a new patient?")
        dialog.setModal(True)
        dialog.setMinimumWidth(520)

        outer = QtWidgets.QVBoxLayout(dialog)
        outer.setContentsMargins(22, 18, 22, 18)
        outer.setSpacing(18)

        prompt_row = QtWidgets.QHBoxLayout()
        prompt_row.setSpacing(14)
        icon = QtWidgets.QLabel()
        icon.setPixmap(
            dialog.style()
            .standardIcon(QtWidgets.QStyle.SP_MessageBoxQuestion)
            .pixmap(40, 40)
        )
        icon.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
        prompt_row.addWidget(icon, 0, QtCore.Qt.AlignTop)

        text_column = QtWidgets.QVBoxLayout()
        text_column.setSpacing(8)
        question = QtWidgets.QLabel(
            "Would you like to save the current patient's CSV before starting a new patient?"
        )
        question.setWordWrap(True)
        note = QtWidgets.QLabel(
            "Choosing New Patient will still use the app's autosave draft safety net."
        )
        note.setWordWrap(True)
        note.setProperty("role", "subtitle")
        text_column.addWidget(question)
        text_column.addWidget(note)
        prompt_row.addLayout(text_column, 1)
        outer.addLayout(prompt_row)

        button_row = QtWidgets.QHBoxLayout()
        button_row.setSpacing(8)
        button_row.addStretch(1)

        selected_action = {"value": None}

        def choose(action):
            selected_action["value"] = action
            dialog.accept()

        save_button = QtWidgets.QPushButton("Save && New Patient")
        save_button.setMinimumSize(160, 38)
        save_button.clicked.connect(lambda: choose("save"))
        save_button.setDefault(True)

        new_button = QtWidgets.QPushButton("New Patient")
        new_button.setProperty("variant", "ghost")
        new_button.setMinimumSize(118, 38)
        new_button.clicked.connect(lambda: choose("new"))

        cancel_button = QtWidgets.QPushButton("Cancel")
        cancel_button.setProperty("variant", "ghost")
        cancel_button.setMinimumSize(92, 38)
        cancel_button.clicked.connect(dialog.reject)

        button_row.addWidget(save_button)
        button_row.addWidget(new_button)
        button_row.addWidget(cancel_button)
        button_row.addStretch(1)
        outer.addLayout(button_row)

        if dialog.exec_() != QtWidgets.QDialog.Accepted:
            return

        if selected_action["value"] == "save":
            main_ui.file_save()

        if selected_action["value"] in ("save", "new"):
            main_ui.new_patient()

    # ------------------------------------------------------------------
    # Theme
    # ------------------------------------------------------------------
    def refresh_theme(self, main_ui):
        self._formula_label.setText(self._formula_html())
        self._apply_power_reminder_style()
        # Re-apply badge styling so soft-colour backgrounds repaint
        self._sync_from_main_ui(main_ui)
        self.gauge.update()

    def _formula_html(self):
        p = theme.palette()
        return (
            "<html><body>"
            f"<table border='0' cellspacing='0' cellpadding='0' style='color:{p['text_muted']};"
            "font-size:14pt; font-family:Segoe UI, sans-serif;'>"
            "<tr>"
            f"<td rowspan='2' valign='middle' align='right' style='padding-right:12px; "
            f"font-weight:500; font-style:italic; color:{p['text']};'>IVVR &nbsp;=</td>"
            f"<td align='center' style='border-bottom:1px solid {p['border_emphasis']}; "
            f"padding-bottom:2px;'>IV</td></tr>"
            "<tr>"
            f"<td align='center' style='padding-top:2px;'>V</td>"
            "</tr></table></body></html>"
        )

    def retranslate_ui(self, main_ui):
        _translate = QtCore.QCoreApplication.translate
        main_ui.clearAllTestDataButton.setText(_translate("MainWindow", "Clear All"))
        main_ui.newPatientResultsButton.setText(_translate("MainWindow", "New Patient"))


class _ProxyIvvrLineEdit(QtWidgets.QLineEdit):
    """Hidden QLineEdit kept for backend compatibility – drives the gauge on update."""

    def __init__(self, tab):
        super().__init__()
        self._tab = tab
        self.setVisible(False)
        self.textChanged.connect(self._on_changed)

    def _on_changed(self, text):
        try:
            value = float(text) if text else None
        except ValueError:
            value = None
        self._tab.set_ivvr(value)
