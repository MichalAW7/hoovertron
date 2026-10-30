import math

from PyQt5 import QtCore


class DataMixin:
    STEP_CONFIG = {
        0: {
            "graph_widget_attr": "graphWidget_hs1",
            "time_attr": "hsS1TimeData",
            "force_attr": "hsS1RForce",
            "average_attr": None,
            "force_line_attr": "hsS1RForceLine",
            "average_line_attr": None,
            "peak_widget_attr": "extensionForceLineEdit",
            "average_widget_attr": None,
            "note_widget_attr": "textEdit",
        },
        1: {
            "graph_widget_attr": "graphWidget_hs2",
            "time_attr": "hsS2TimeData",
            "force_attr": "hsS2RForce",
            "average_attr": "hsS2RAverage",
            "force_line_attr": "hsS2RForceLine",
            "average_line_attr": "hsS2RAverageLine",
            "peak_widget_attr": "unaffectedLegPeakStrengthLineEdit_2",
            "average_widget_attr": "unaffectedLegAverageStrengthLineEdit_2",
            "note_widget_attr": "textEdit_2",
        },
        2: {
            "graph_widget_attr": "graphWidget_hs3",
            "time_attr": "hsS3TimeData",
            "force_attr": "hsS3RForce",
            "average_attr": "hsS3RAverage",
            "force_line_attr": "hsS3RForceLine",
            "average_line_attr": "hsS3RForceAverageLine",
            "peak_widget_attr": "affectedLegPeakStrengthLineEdit_3",
            "average_widget_attr": None,
            "note_widget_attr": "textEdit_6",
        },
    }

    DEFAULT_ANALYSIS_TEXT = "Record Step 1 and Step 2 to see the analysis."

    def initialize_step_data(self):
        self.hsS1TimeData = [0.0]
        self.hsS1RForce = [0.0]
        self.hsS2TimeData = [0.0]
        self.hsS2RForce = [0.0]
        self.hsS2RAverage = [0.0]
        self.hsS3TimeData = [0.0]
        self.hsS3RForce = [0.0]
        self.hsS3RAverage = [0.0]
        self.step_selection_active = {0: False, 1: False, 2: False}

    def get_step_config(self, step_index):
        return self.STEP_CONFIG[step_index]

    def get_step_time_data(self, step_index):
        return getattr(self, self.get_step_config(step_index)["time_attr"])

    def get_step_force_data(self, step_index):
        return getattr(self, self.get_step_config(step_index)["force_attr"])

    def get_step_average_data(self, step_index):
        average_attr = self.get_step_config(step_index)["average_attr"]
        if not average_attr:
            return []
        return getattr(self, average_attr)

    def set_step_data(self, step_index, time_data=None, force_data=None, average_data=None):
        config = self.get_step_config(step_index)
        if time_data is not None:
            setattr(self, config["time_attr"], self._normalize_series(time_data))
        if force_data is not None:
            setattr(self, config["force_attr"], self._normalize_series(force_data))
        if config["average_attr"] and average_data is not None:
            setattr(self, config["average_attr"], self._normalize_series(average_data))

    def _normalize_series(self, values):
        cleaned_values = []
        for value in values or []:
            try:
                cleaned_values.append(float(value))
            except (TypeError, ValueError):
                continue
        return cleaned_values or [0.0]

    def _normalize_selection_range(self, selection_range):
        if not selection_range or len(selection_range) != 2:
            return (0.0, 1.0)

        try:
            start = float(selection_range[0])
            end = float(selection_range[1])
        except (TypeError, ValueError):
            return (0.0, 1.0)

        if end < start:
            start, end = end, start
        return (start, end)

    def _set_line_edit_text(self, widget, value):
        widget.setText(self.format_display_value(value))

    def format_display_value(self, value):
        return self.format_display_value_3sf(value)

    def format_display_value_3sf(self, value):
        if value in (None, ""):
            return ""

        if isinstance(value, str):
            stripped_value = value.strip()
            if not stripped_value:
                return ""
            try:
                return self._format_sig_fig_number(float(stripped_value))
            except ValueError:
                return value

        try:
            return self._format_sig_fig_number(float(value))
        except (TypeError, ValueError):
            return str(value)

    def _format_sig_fig_number(self, value, significant_figures=3):
        if value == 0:
            return "0.00"

        abs_value = abs(value)
        if abs_value < 1e-4 or abs_value >= 1e6:
            return f"{value:.{significant_figures}g}"

        decimal_places = significant_figures - int(math.floor(math.log10(abs_value))) - 1
        if decimal_places > 0:
            return f"{value:.{decimal_places}f}"

        rounded_value = round(value, decimal_places)
        return f"{rounded_value:.0f}"

    def _parse_float_text(self, text):
        try:
            if text in (None, ""):
                return None
            return float(text)
        except (TypeError, ValueError):
            return None

    def has_meaningful_step_data(self, step_index):
        force_data = self.get_step_force_data(step_index)
        if len(force_data) > 1:
            return True
        return any(abs(value) > 1e-9 for value in force_data)

    def get_step_selection_range(self, step_index):
        if not hasattr(self, "selection_region"):
            return (0.0, 1.0)
        return self._normalize_selection_range(self.selection_region[step_index].getRegion())

    def set_step_selection_range(self, step_index, selection_range, active=None):
        start, end = self._normalize_selection_range(selection_range)
        if hasattr(self, "selection_region"):
            self.selection_region[step_index].setRegion((start, end))
        if hasattr(self, "start_time_input"):
            self.start_time_input[step_index][0].setText(self.format_display_value(start))
            self.end_time_input[step_index][0].setText(self.format_display_value(end))
        if active is not None:
            self.step_selection_active[step_index] = bool(active)
            self._update_selection_button_state(step_index)

    def _update_selection_button_state(self, step_index):
        color = "green" if self.step_selection_active.get(step_index, False) else "red"
        for button in self.select_button[step_index]:
            button.setStyleSheet(
                f"background-color: {color}; color: white; font-weight: bold; font-size: 16px;"
            )

    def update_step_plot(self, step_index):
        config = self.get_step_config(step_index)
        time_data = self.get_step_time_data(step_index)
        force_data = self.get_step_force_data(step_index)
        getattr(self, config["force_line_attr"]).setData(time_data[: len(force_data)], force_data)

        average_attr = config["average_attr"]
        if average_attr and config["average_line_attr"]:
            average_data = getattr(self, average_attr)
            getattr(self, config["average_line_attr"]).setData(time_data[: len(average_data)], average_data)

    def update_all_step_plots(self):
        for step_index in self.STEP_CONFIG:
            self.update_step_plot(step_index)

    def fit_step_graph_to_data(self, step_index=None):
        if step_index is None:
            step_index = self.get_active_step_index()
        if step_index not in self.STEP_CONFIG:
            return

        graph_widget = getattr(self, self.get_step_config(step_index)["graph_widget_attr"], None)
        if not graph_widget:
            return

        view_box = graph_widget.getPlotItem().getViewBox()
        view_box.autoRange()
        # autoRange() is one-shot and disables live auto-ranging; turn it back on
        # so incoming samples remain visible after the user presses Fit view.
        view_box.enableAutoRange(x=True, y=True)

    def calculate_step_measurements(self, step_index, use_selection=None):
        config = self.get_step_config(step_index)
        time_data = self.get_step_time_data(step_index)
        force_data = self.get_step_force_data(step_index)
        average_data = self.get_step_average_data(step_index)

        if use_selection is None:
            use_selection = self.step_selection_active.get(step_index, False)

        selected_force = force_data
        selected_average = average_data
        if use_selection and time_data:
            start_time, end_time = self.get_step_selection_range(step_index)
            selected_force = [
                value
                for idx, value in enumerate(force_data)
                if idx < len(time_data) and start_time <= time_data[idx] <= end_time
            ]
            if average_data:
                selected_average = [
                    value
                    for idx, value in enumerate(average_data)
                    if idx < len(time_data) and start_time <= time_data[idx] <= end_time
                ]

        peak_value = max(selected_force, default=None) if self.has_meaningful_step_data(step_index) else None
        average_value = None
        if average_data and any(abs(value) > 1e-9 for value in average_data):
            average_value = max(selected_average or average_data, default=None)

        return {
            "peak": peak_value,
            "average": average_value,
            "selection": self.get_step_selection_range(step_index),
            "selection_active": self.step_selection_active.get(step_index, False),
        }

    def refresh_step_measurements(self, step_index):
        config = self.get_step_config(step_index)
        measurements = self.calculate_step_measurements(step_index)

        peak_widget = getattr(self, config["peak_widget_attr"])
        peak_value = measurements["peak"]
        self._set_line_edit_text(peak_widget, peak_value)

        average_widget_attr = config["average_widget_attr"]
        if average_widget_attr:
            average_widget = getattr(self, average_widget_attr)
            average_value = measurements["average"]
            self._set_line_edit_text(average_widget, average_value)

    def refresh_all_step_measurements(self):
        for step_index in self.STEP_CONFIG:
            self.refresh_step_measurements(step_index)
        self.fill_values()

    def update_selection(self, step_index=None):
        if getattr(self, "_is_applying_snapshot", False):
            return

        if step_index is None:
            step_index = self.get_active_step_index()
        if step_index not in self.STEP_CONFIG:
            return

        xmin, xmax = self.get_step_selection_range(step_index)
        self.start_time_input[step_index][0].setText(self.format_display_value(xmin))
        self.end_time_input[step_index][0].setText(self.format_display_value(xmax))

    def select_time_period(self):
        step_index = self.get_active_step_index()
        if step_index not in self.STEP_CONFIG:
            return

        start_text = self.start_time_input[step_index][0].text()
        end_text = self.end_time_input[step_index][0].text()

        try:
            start_time = float(start_text) if start_text else 0.0
            end_time = float(end_text) if end_text else 0.0
        except ValueError:
            start_time, end_time = self.get_step_selection_range(step_index)

        self.step_selection_active[step_index] = True
        self.set_step_selection_range(step_index, (start_time, end_time), active=True)
        self.refresh_step_measurements(step_index)
        self.fill_values()
        self.schedule_autosave("selection-updated")

    def clear_current_step(self):
        step_index = self.get_active_step_index()
        if step_index not in self.STEP_CONFIG:
            return
        self.reset_step_state(step_index)

    @QtCore.pyqtSlot(bool)
    def clear_data(self, checked):
        if not checked:
            return

        self.clear_current_step()

        button = self.sender()
        if button and hasattr(button, "blockSignals"):
            button.blockSignals(True)
            button.setChecked(False)
            button.blockSignals(False)

    def reset_step_state(self, step_index):
        config = self.get_step_config(step_index)
        setattr(self, config["time_attr"], [0.0])
        setattr(self, config["force_attr"], [0.0])
        if config["average_attr"]:
            setattr(self, config["average_attr"], [0.0])

        self.step_selection_active[step_index] = False
        self.update_step_plot(step_index)
        self.set_step_selection_range(step_index, (0.0, 1.0), active=False)
        self._set_line_edit_text(getattr(self, config["peak_widget_attr"]), "")

        average_widget_attr = config["average_widget_attr"]
        if average_widget_attr:
            self._set_line_edit_text(getattr(self, average_widget_attr), "")

        if hasattr(self, self.get_step_config(step_index)["note_widget_attr"]):
            getattr(self, self.get_step_config(step_index)["note_widget_attr"]).clear()

        self.fill_values()
        if not getattr(self, "_is_applying_snapshot", False):
            self.schedule_autosave("step-cleared")

    def reset_all_step_states(self):
        for step_index in self.STEP_CONFIG:
            config = self.get_step_config(step_index)
            setattr(self, config["time_attr"], [0.0])
            setattr(self, config["force_attr"], [0.0])
            if config["average_attr"]:
                setattr(self, config["average_attr"], [0.0])
            self.step_selection_active[step_index] = False

        self.update_all_step_plots()
        for step_index in self.STEP_CONFIG:
            self.set_step_selection_range(step_index, (0.0, 1.0), active=False)

        self._set_line_edit_text(self.extensionForceLineEdit, "")
        self._set_line_edit_text(self.unaffectedLegAverageStrengthLineEdit_2, "")
        self._set_line_edit_text(self.unaffectedLegPeakStrengthLineEdit_2, "")
        self._set_line_edit_text(self.affectedLegPeakStrengthLineEdit_3, "")

    def clear_all_test_data(self):
        self.reset_all_step_states()
        self.textEdit.clear()
        self.textEdit_2.clear()
        self.textEdit_6.clear()
        self.textEdit_7.clear()
        self.unaffectedLegExtensionLLineEdit.clear()
        self.affectedLegVoluntaryExtensionLineEdit.clear()
        self.affectedLegInvoluntaryExtensionLineEdit.clear()
        self.involuntaryVoluntaryRatioAffectedLegLineEdit.clear()
        self.label_21.setText(self.DEFAULT_ANALYSIS_TEXT)
        self.schedule_autosave("test-data-cleared")

    def fill_values(self, *_):
        unaffected_measurements = self.calculate_step_measurements(0)
        voluntary_measurements = self.calculate_step_measurements(1)
        involuntary_measurements = self.calculate_step_measurements(2)

        unaffected = unaffected_measurements["peak"]
        voluntary = voluntary_measurements["peak"]
        involuntary = involuntary_measurements["peak"]

        self._set_line_edit_text(self.unaffectedLegExtensionLLineEdit, unaffected)
        self._set_line_edit_text(self.affectedLegVoluntaryExtensionLineEdit, voluntary)
        self._set_line_edit_text(self.affectedLegInvoluntaryExtensionLineEdit, involuntary)

        if voluntary and involuntary is not None and voluntary != 0:
            ivvr = involuntary / voluntary
            ivvr_text = self.format_display_value(ivvr)
            self.involuntaryVoluntaryRatioAffectedLegLineEdit.setText(ivvr_text)
            self.label_21.setText(
                "The ratio between the affected leg's voluntary and involuntary force was "
                f"{ivvr_text}. Review this value alongside the full clinical picture."
            )
        else:
            self.involuntaryVoluntaryRatioAffectedLegLineEdit.clear()
            self.label_21.setText(self.DEFAULT_ANALYSIS_TEXT)

    def process_incoming_data(self, text_line):
        """Process a line of comma-separated data from the device."""
        try:
            words = text_line.split(",")
            if len(words) < 2:
                return

            step_index = self.get_active_step_index()
            if step_index not in self.STEP_CONFIG:
                return

            config = self.get_step_config(step_index)

            time_value = float(words[0]) / 300000
            force_value = float(words[1])
            force_average_value = float(words[3]) if len(words) > 3 else None

            time_data = self.get_step_time_data(step_index)
            previous_time = time_data[-1] if time_data else 0.0
            time_data.append(previous_time + time_value)

            force_data = self.get_step_force_data(step_index)
            force_data.append(force_value)

            average_attr = config["average_attr"]
            if average_attr and force_average_value is not None:
                average_data = getattr(self, average_attr)
                average_data.append(force_average_value)

            self.update_step_plot(step_index)
            self.schedule_autosave("data-captured", restart=False)

        except (ValueError, IndexError) as error:
            print(f"Error processing data: {error}")
