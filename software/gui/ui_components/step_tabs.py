from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg

from config import get_resource_path
from ui_components import theme


# ============================================================================
# Graph theming
# ============================================================================

LINE_WIDTHS = {"primary": 2.4, "average": 2.0}
CONTROL_HEIGHT = 38


def format_sig_fig_axis_value(value, significant_figures=3):
    return f"{value:.{significant_figures}g}" if value else "0.00"


class SignificantFigureAxisItem(pg.AxisItem):
    def tickStrings(self, values, scale, spacing):
        return [format_sig_fig_axis_value(value) for value in values]


def apply_graph_theme(graph_widget):
    """Apply current theme palette to a pyqtgraph PlotWidget."""
    p = theme.palette()
    pg.setConfigOptions(antialias=True)

    graph_widget.setBackground(p["graph_bg"])
    plot_item = graph_widget.getPlotItem()
    view_box = plot_item.getViewBox()
    view_box.setBackgroundColor(p["graph_bg"])
    view_box.setDefaultPadding(0.05)

    plot_item.showGrid(x=True, y=True, alpha=0.25)
    for axis_name in ("left", "bottom"):
        axis = plot_item.getAxis(axis_name)
        axis.setPen(pg.mkPen(color=p["graph_axis"], width=1))
        axis.setTextPen(pg.mkPen(color=p["graph_label"]))
        font = QtGui.QFont("Segoe UI", 9)
        axis.setTickFont(font)
        axis.setStyle(tickLength=-6, tickTextOffset=6)

    plot_item.hideAxis("top")
    plot_item.hideAxis("right")

    # Hide pyqtgraph's tiny "A" – we have our own Fit-view button in the controls row.
    try:
        plot_item.hideButtons()
    except Exception:
        pass

    legend = plot_item.legend
    if legend:
        legend.setLabelTextColor(p["graph_label"])
        legend.setBrush(pg.mkBrush(color=_with_alpha(p["graph_bg"], 230)))
        legend.setPen(pg.mkPen(color=p["graph_grid"], width=1))

    # Repaint existing line items to match theme
    for item in plot_item.listDataItems():
        opts = item.opts
        name = (opts.get("name") or "").lower()
        if "average" in name:
            item.setPen(pg.mkPen(color=p["graph_average"], width=LINE_WIDTHS["average"], style=QtCore.Qt.DashLine))
        else:
            item.setPen(pg.mkPen(color=p["graph_primary"], width=LINE_WIDTHS["primary"]))


def _with_alpha(hex_or_color, alpha):
    c = QtGui.QColor(hex_or_color)
    c.setAlpha(alpha)
    return c


def create_legend(graph_widget):
    p = theme.palette()
    legend = graph_widget.addLegend(
        offset=(12, 10),
        labelTextSize="10pt",
        brush=pg.mkBrush(_with_alpha(p["graph_bg"], 230)),
        pen=pg.mkPen(color=p["graph_grid"], width=1),
    )
    legend.setLabelTextColor(p["graph_label"])
    return legend


def set_axis_labels(graph_widget, left, bottom):
    p = theme.palette()
    style = {"color": p["graph_label"], "font-size": "11pt"}
    graph_widget.setLabel("left", left, **style)
    graph_widget.setLabel("bottom", bottom, **style)


# ============================================================================
# Aspect-ratio image helper
# ============================================================================

class AspectRatioLabel(QtWidgets.QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._original_pixmap = None
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setMinimumSize(1, 1)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )

    def setPixmap(self, pixmap):
        self._original_pixmap = pixmap
        self._update_scaled()

    def resizeEvent(self, event):
        self._update_scaled()
        super().resizeEvent(event)

    def _update_scaled(self):
        if self._original_pixmap and not self._original_pixmap.isNull():
            scaled = self._original_pixmap.scaled(
                self.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation
            )
            super().setPixmap(scaled)


# ============================================================================
# Step tabs
# ============================================================================

class StatCard(QtWidgets.QFrame):
    """A small card with an uppercase label and a large numeric value."""

    def __init__(self, label, parent=None, unit="N"):
        super().__init__(parent)
        self.setProperty("card", "muted")
        lay = QtWidgets.QVBoxLayout(self)
        lay.setContentsMargins(14, 12, 14, 12)
        lay.setSpacing(4)

        self.label = QtWidgets.QLabel(label)
        self.label.setProperty("role", "metric-label")
        lay.addWidget(self.label)

        row = QtWidgets.QHBoxLayout()
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(6)
        self.value = QtWidgets.QLabel("–")
        self.value.setProperty("role", "metric")
        row.addWidget(self.value)
        if unit:
            unit_label = QtWidgets.QLabel(unit)
            unit_label.setProperty("role", "metric-unit")
            row.addWidget(unit_label, 0, QtCore.Qt.AlignBottom)
        row.addStretch(1)
        lay.addLayout(row)

    def setText(self, text):
        self.value.setText(text if text else "–")


class _ValueProxyLineEdit(QtWidgets.QLineEdit):
    """Hidden QLineEdit that mirrors its value into a StatCard.

    Preserves the existing backend API (setText / clear / .text()).
    """

    def __init__(self, card):
        super().__init__()
        self._card = card
        self.setVisible(False)
        self.textChanged.connect(self._sync)

    def _sync(self, text):
        self._card.setText(text)


class StepTabs:
    def _create_plot_widget(self):
        axis_items = {
            "left":   SignificantFigureAxisItem(orientation="left"),
            "bottom": SignificantFigureAxisItem(orientation="bottom"),
        }
        return pg.PlotWidget(axisItems=axis_items)

    # ------------------------------------------------------------------
    # Shared builder
    # ------------------------------------------------------------------
    def _build_step(
        self,
        main_ui,
        parent_widget,
        *,
        step_index,
        step_label,
        title,
        instruction,
        image_filename,
        graph_attr,
        plot_data_attrs,
        average_attrs,
        average_line_attr,
        force_line_attr,
        record_btn_attr,
        clear_btn_attr,
        horiz_layout_attr,
        notes_attr,
        stat_definitions,        # list of (card_attr, lineedit_attr, label, unit)
    ):
        rootLayout = QtWidgets.QHBoxLayout(parent_widget)
        rootLayout.setContentsMargins(24, 22, 24, 22)
        rootLayout.setSpacing(28)

        # ---- Left: instruction with illustration -----------------------
        leftLayout = QtWidgets.QVBoxLayout()
        leftLayout.setContentsMargins(0, 0, 0, 0)
        leftLayout.setSpacing(10)

        eyebrow = QtWidgets.QLabel(step_label)
        eyebrow.setProperty("role", "eyebrow")
        leftLayout.addWidget(eyebrow)

        title_label = QtWidgets.QLabel(title)
        title_label.setProperty("role", "title")
        title_label.setWordWrap(True)
        leftLayout.addWidget(title_label)

        instr = QtWidgets.QLabel(instruction)
        instr.setProperty("role", "subtitle")
        instr.setWordWrap(True)
        leftLayout.addWidget(instr)

        image = AspectRatioLabel()
        image.setPixmap(QtGui.QPixmap(get_resource_path(image_filename)))
        image.setMinimumHeight(220)
        leftLayout.addWidget(image, 1)

        leftHolder = QtWidgets.QWidget()
        leftHolder.setLayout(leftLayout)
        leftHolder.setMinimumWidth(240)
        leftHolder.setMaximumWidth(340)
        rootLayout.addWidget(leftHolder, 0)

        # ---- Right: graph + controls + measurements --------------------
        rightLayout = QtWidgets.QVBoxLayout()
        rightLayout.setSpacing(16)

        graph_widget = self._create_plot_widget()
        setattr(main_ui, graph_attr, graph_widget)
        create_legend(graph_widget)
        apply_graph_theme(graph_widget)
        set_axis_labels(graph_widget, "Force (N)", "Time (seconds)")
        graph_widget.setMinimumHeight(260)

        pen = pg.mkPen(color=theme.palette()["graph_primary"], width=LINE_WIDTHS["primary"])
        time_data = getattr(main_ui, plot_data_attrs[0])
        force_data = getattr(main_ui, plot_data_attrs[1])
        force_line = graph_widget.plot(time_data, force_data, name="Extension Sensor", pen=pen)
        setattr(main_ui, force_line_attr, force_line)

        if average_attrs:
            avg_pen = pg.mkPen(color=theme.palette()["graph_average"], width=LINE_WIDTHS["average"], style=QtCore.Qt.DashLine)
            avg_data = getattr(main_ui, average_attrs[0])
            avg_line = graph_widget.plot(time_data, avg_data, name="Force Average", pen=avg_pen)
            setattr(main_ui, average_line_attr, avg_line)

        rightLayout.addWidget(graph_widget, 1)

        # Controls row
        controlsLayout = QtWidgets.QHBoxLayout()
        controlsLayout.setContentsMargins(0, 0, 0, 0)
        controlsLayout.setSpacing(10)

        record_btn = QtWidgets.QPushButton("Record")
        record_btn.setCheckable(True)
        record_btn.setProperty("variant", "record")
        record_btn.setCursor(QtCore.Qt.PointingHandCursor)
        record_btn.setFixedSize(120, CONTROL_HEIGHT)
        record_btn.toggled.connect(main_ui.on_toggled)
        setattr(main_ui, record_btn_attr, record_btn)

        clear_btn = QtWidgets.QPushButton("Clear data")
        clear_btn.setCheckable(True)
        clear_btn.setProperty("variant", "ghost")
        clear_btn.setCursor(QtCore.Qt.PointingHandCursor)
        clear_btn.setFixedSize(120, CONTROL_HEIGHT)
        clear_btn.toggled.connect(self._wrap_confirm_clear(main_ui, clear_btn))
        setattr(main_ui, clear_btn_attr, clear_btn)

        # Fit-view button (replaces pyqtgraph's tiny A icon)
        fit_btn = QtWidgets.QPushButton("  Resize Graph")
        fit_btn.setProperty("variant", "ghost")
        fit_btn.setCursor(QtCore.Qt.PointingHandCursor)
        fit_btn.setToolTip("Fit graph view to the recorded data")
        fit_btn.setFixedSize(154, CONTROL_HEIGHT)
        icon = QtGui.QIcon(theme.fit_view_url(theme.palette()["text_muted"]))
        fit_btn.setIcon(icon)
        fit_btn.setIconSize(QtCore.QSize(16, 16))
        fit_btn.clicked.connect(lambda: main_ui.fit_step_graph_to_data(step_index))

        controlsLayout.addWidget(record_btn)
        controlsLayout.addWidget(clear_btn)
        controlsLayout.addWidget(fit_btn)

        horiz_layout = QtWidgets.QHBoxLayout()
        horiz_layout.setContentsMargins(0, 0, 0, 0)
        horiz_layout.setSpacing(8)
        setattr(main_ui, horiz_layout_attr, horiz_layout)
        controlsLayout.addLayout(horiz_layout, 1)
        rightLayout.addLayout(controlsLayout, 0)

        # Notes + measurements row
        bottomRow = QtWidgets.QHBoxLayout()
        bottomRow.setSpacing(28)

        notesLayout = QtWidgets.QVBoxLayout()
        notesLayout.setContentsMargins(0, 0, 0, 0)
        notesLayout.setSpacing(6)
        notesHeader = QtWidgets.QLabel("Notes")
        notesHeader.setProperty("role", "eyebrow")
        notesLayout.addWidget(notesHeader)
        textEdit = QtWidgets.QTextEdit()
        textEdit.setPlaceholderText("Observations for this step…")
        textEdit.setMinimumHeight(96)
        setattr(main_ui, notes_attr, textEdit)
        notesLayout.addWidget(textEdit)
        bottomRow.addLayout(notesLayout, 2)

        statsLayout = QtWidgets.QVBoxLayout()
        statsLayout.setContentsMargins(0, 0, 0, 0)
        statsLayout.setSpacing(6)
        statsHeader = QtWidgets.QLabel("Measurements")
        statsHeader.setProperty("role", "eyebrow")
        statsLayout.addWidget(statsHeader)
        for card_attr, lineedit_attr, lbl, unit in stat_definitions:
            card = StatCard(lbl, unit=unit)
            setattr(main_ui, card_attr, card)
            statsLayout.addWidget(card)
            proxy = _ValueProxyLineEdit(card)
            proxy.setReadOnly(True)
            setattr(main_ui, lineedit_attr, proxy)
            statsLayout.addWidget(proxy)
        statsLayout.addStretch(1)
        bottomRow.addLayout(statsLayout, 1)

        rightLayout.addLayout(bottomRow, 0)
        rootLayout.addLayout(rightLayout, 1)

    def _wrap_confirm_clear(self, main_ui, button):
        def handler(checked):
            if not checked:
                return main_ui.clear_data(checked)
            # Ask before clearing
            parent = button.window()
            if not getattr(main_ui, "_clear_confirmations_enabled", True):
                return main_ui.clear_data(checked)
            reply = QtWidgets.QMessageBox.question(
                parent,
                "Clear recorded data?",
                "This removes the captured trace for this step. Continue?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel,
                QtWidgets.QMessageBox.Cancel,
            )
            if reply == QtWidgets.QMessageBox.Yes:
                main_ui.clear_data(checked)
            else:
                # Revert the toggle without firing the handler again
                button.blockSignals(True)
                button.setChecked(False)
                button.blockSignals(False)
        return handler

    # ------------------------------------------------------------------
    # Step 1 (Optional baseline) – unaffected leg
    # ------------------------------------------------------------------
    def setup_step_1(self, main_ui, parent_widget):
        self._build_step(
            main_ui,
            parent_widget,
            step_index=0,
            step_label="Optional Step",
            title="Baseline – unaffected leg",
            instruction=(
                "Have the patient press their unaffected leg down onto the device. "
                "Records a reference for comparison."
            ),
            image_filename="images/infographic1.drawio.png",
            graph_attr="graphWidget_hs1",
            plot_data_attrs=("hsS1TimeData", "hsS1RForce"),
            average_attrs=None,
            average_line_attr=None,
            force_line_attr="hsS1RForceLine",
            record_btn_attr="pushButton_2",
            clear_btn_attr="pushButton_21",
            horiz_layout_attr="horizontalLayout_s1",
            notes_attr="textEdit",
            stat_definitions=[
                ("statCard_s1_extension", "extensionForceLineEdit", "Extension force", "N"),
            ],
        )
        # Hidden legacy labels for translation parity
        main_ui.label = AspectRatioLabel()  # legacy alias kept for save/load if referenced
        main_ui.label.setVisible(False)
        main_ui.label_4 = QtWidgets.QLabel(); main_ui.label_4.setVisible(False)
        main_ui.label_5 = QtWidgets.QLabel(); main_ui.label_5.setVisible(False)
        main_ui.label_16 = QtWidgets.QLabel(); main_ui.label_16.setVisible(False)
        main_ui.extensionForceLabel = QtWidgets.QLabel("Extension force")
        main_ui.extensionForceLabel.setVisible(False)

    # ------------------------------------------------------------------
    # Step 2 – Voluntary (affected leg push) → "Step 1" tab in legacy UI
    # ------------------------------------------------------------------
    def setup_step_2(self, main_ui, parent_widget):
        self._build_step(
            main_ui,
            parent_widget,
            step_index=1,
            step_label="Step 1",
            title="Voluntary push – affected leg",
            instruction=(
                "Ask the patient to press their affected leg firmly down onto the device."
            ),
            image_filename="images/infographic2.drawio.png",
            graph_attr="graphWidget_hs2",
            plot_data_attrs=("hsS2TimeData", "hsS2RForce"),
            average_attrs=("hsS2RAverage",),
            average_line_attr="hsS2RAverageLine",
            force_line_attr="hsS2RForceLine",
            record_btn_attr="pushButton_3",
            clear_btn_attr="pushButton_31",
            horiz_layout_attr="horizontalLayout_s2",
            notes_attr="textEdit_2",
            stat_definitions=[
                ("statCard_s2_avg",  "unaffectedLegAverageStrengthLineEdit_2", "Force average",      "N"),
                ("statCard_s2_peak", "unaffectedLegPeakStrengthLineEdit_2",    "Voluntary peak (V)", "N"),
            ],
        )
        main_ui.label_2 = AspectRatioLabel(); main_ui.label_2.setVisible(False)
        main_ui.label_10 = QtWidgets.QLabel(); main_ui.label_10.setVisible(False)
        main_ui.label_11 = QtWidgets.QLabel(); main_ui.label_11.setVisible(False)
        main_ui.label_17 = QtWidgets.QLabel(); main_ui.label_17.setVisible(False)
        main_ui.unaffectedLegAverageStrengthLabel_2 = QtWidgets.QLabel("Force average"); main_ui.unaffectedLegAverageStrengthLabel_2.setVisible(False)
        main_ui.unaffectedLegPeakStrengthLabel_2 = QtWidgets.QLabel("Voluntary peak (V)"); main_ui.unaffectedLegPeakStrengthLabel_2.setVisible(False)

    # ------------------------------------------------------------------
    # Step 3 – Involuntary (Hoover test) → "Step 2" tab in legacy UI
    # ------------------------------------------------------------------
    def setup_step_3(self, main_ui, parent_widget):
        self._build_step(
            main_ui,
            parent_widget,
            step_index=2,
            step_label="Step 2",
            title="Involuntary extension – Hoover's sign",
            instruction=(
                "While applying resistance to the unaffected leg as the patient lifts it, "
                "watch for involuntary downward pressure from the affected leg."
            ),
            image_filename="images/infographic3.drawio.png",
            graph_attr="graphWidget_hs3",
            plot_data_attrs=("hsS3TimeData", "hsS3RForce"),
            average_attrs=("hsS3RAverage",),
            average_line_attr="hsS3RForceAverageLine",
            force_line_attr="hsS3RForceLine",
            record_btn_attr="pushButton_4",
            clear_btn_attr="pushButton_41",
            horiz_layout_attr="horizontalLayout_s3",
            notes_attr="textEdit_6",
            stat_definitions=[
                ("statCard_s3_peak", "affectedLegPeakStrengthLineEdit_3", "Involuntary peak (IV)", "N"),
            ],
        )
        main_ui.label_3 = AspectRatioLabel(); main_ui.label_3.setVisible(False)
        main_ui.label_14 = QtWidgets.QLabel(); main_ui.label_14.setVisible(False)
        main_ui.label_15 = QtWidgets.QLabel(); main_ui.label_15.setVisible(False)
        main_ui.label_18 = QtWidgets.QLabel(); main_ui.label_18.setVisible(False)
        main_ui.affectedLegPeakStrengthLabel_3 = QtWidgets.QLabel("Involuntary peak (IV)"); main_ui.affectedLegPeakStrengthLabel_3.setVisible(False)

    # ------------------------------------------------------------------
    def retranslate_step_1(self, main_ui):
        _translate = QtCore.QCoreApplication.translate
        main_ui.pushButton_2.setText(_translate("MainWindow", "Record"))
        main_ui.pushButton_21.setText(_translate("MainWindow", "Clear data"))

    def retranslate_step_2(self, main_ui):
        _translate = QtCore.QCoreApplication.translate
        main_ui.pushButton_3.setText(_translate("MainWindow", "Record"))
        main_ui.pushButton_31.setText(_translate("MainWindow", "Clear data"))

    def retranslate_step_3(self, main_ui):
        _translate = QtCore.QCoreApplication.translate
        main_ui.pushButton_4.setText(_translate("MainWindow", "Record"))
        main_ui.pushButton_41.setText(_translate("MainWindow", "Clear data"))
