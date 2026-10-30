from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMessageBox

from hoover_backend.ble_mixin import BleMixin
from hoover_backend.data_mixin import DataMixin
from hoover_backend.file_mixin import FileMixin
from hoover_backend.serial_mixin import SerialMixin
from hoover_backend.settings_mixin import SettingsMixin
from ui_layout import Ui_Layout


class HooverTronWindow(
    QtWidgets.QMainWindow, Ui_Layout, BleMixin, SerialMixin, FileMixin, DataMixin, SettingsMixin
):
    def __init__(self):
        super().__init__()

        self.ble_device = None
        self.ble_client = None
        self.is_connected = False
        self.is_recording = False
        self.data_buffer = ""
        self.currentFrequency = 10

        self.patientDataFile = ""
        self.dataBaseFile = ""
        self.testNumber = 1
        self.isNewDatabase = True

        self.initialize_step_data()
        self.setupUi(self)
        self.setup_serial()
        self.initialize_persistence()
        self._connect_change_tracking()
        self.load_config()
        QtCore.QTimer.singleShot(0, self.offer_draft_recovery)

    def _connect_change_tracking(self):
        line_edits = [
            self.patientIdLineEdit,
            self.reasonForVisitLineEdit,
            self.notesLineEdit,
            self.examinerLineEdit,
        ]
        for line_edit in line_edits:
            line_edit.textChanged.connect(lambda *_: self.schedule_autosave("patient-field"))

        for combo_box in (self.dominantLegComboBox, self.selectedLegComboBox):
            combo_box.currentIndexChanged.connect(lambda *_: self.schedule_autosave("patient-field"))

        self.dateOfVisitDateEdit.dateChanged.connect(lambda *_: self.schedule_autosave("patient-field"))

        for text_edit in (self.textEdit, self.textEdit_2, self.textEdit_6, self.textEdit_7):
            text_edit.textChanged.connect(lambda: self.schedule_autosave("notes-updated"))

    def _set_recording_buttons_checked(self, checked):
        for button in (self.pushButton_2, self.pushButton_3, self.pushButton_4):
            button.blockSignals(True)
            button.setChecked(checked)
            button.blockSignals(False)
            button.setText("Stop" if checked else "Record")

    def valgAfComport(self, port_name):
        """Handle Serial Port selection."""
        if self.is_connected and self.connection_type == "BLE":
            reply = QMessageBox.question(
                self,
                "Switch Connection",
                "BLE is currently connected. Disconnect BLE and switch to Serial?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if reply == QMessageBox.Yes:
                self.disconnect_ble_persistent()
            else:
                return

        self.connect_serial(port_name)

    def set_filter_frequency(self, frequency):
        if self.connection_type == "BLE":
            BleMixin.set_filter_frequency(self, frequency)
        elif self.connection_type == "Serial":
            self.set_filter_frequency_serial(frequency)
        else:
            QMessageBox.warning(self, "Connection Error", "Please connect to a device first.")

    @QtCore.pyqtSlot(bool)
    def on_toggled(self, checked):
        self.pushButton_4.setText("Stop" if checked else "Record")
        self.pushButton_3.setText("Stop" if checked else "Record")
        self.pushButton_2.setText("Stop" if checked else "Record")

        if checked:
            if not self.is_connected:
                QMessageBox.warning(self, "Connection Error", "Please connect to a device first (BLE or Serial).")
                self._set_recording_buttons_checked(False)
                return

            self.is_recording = True
            if hasattr(self, "statusbar"):
                self.statusbar.showMessage("Recording started", 2000)
            return

        self.is_recording = False
        self.refresh_all_step_measurements()
        self.force_autosave("recording-stop")
        if hasattr(self, "statusbar"):
            self.statusbar.showMessage("Recording stopped", 2000)

    def closeEvent(self, event):
        if self.autosave_timer.isActive():
            self.autosave_timer.stop()

        snapshot = self.collect_snapshot()
        if self.is_autosave_eligible(snapshot):
            if not self.force_autosave("close"):
                event.ignore()
                return

        if self.connection_type == "Serial":
            self.disconnect_serial()

        event.accept()
