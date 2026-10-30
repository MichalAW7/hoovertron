import copy
import csv
import hashlib
import json
import os
import uuid
from datetime import datetime, timezone

from PyQt5 import QtCore
from PyQt5.QtWidgets import QMessageBox

from config import get_drafts_dir, get_settings_file_path


class SettingsMixin:
    SNAPSHOT_VERSION = 2
    # Snapshots older than this hold the patient's name, date of birth, age and sex
    PATIENT_ID_SNAPSHOT_VERSION = 2
    AUTOSAVE_DELAY_MS = 2000
    SNAPSHOT_JSON_LABEL = "HooverTron Snapshot JSON:"

    def initialize_persistence(self):
        self.settings_file_path = get_settings_file_path()
        self.drafts_dir = get_drafts_dir()
        self.settings_data = {}
        self.current_draft_id = None
        self.current_draft_path = ""
        self.current_draft_created_at = self._utcnow_iso()
        self.last_autosave_signature = None
        self.is_dirty = False
        self.pending_autosave_reason = ""
        self._startup_draft_to_offer = ""
        self._is_applying_snapshot = False

        self.autosave_timer = QtCore.QTimer(self)
        self.autosave_timer.setSingleShot(True)
        self.autosave_timer.timeout.connect(self._run_debounced_autosave)

    def _utcnow_iso(self):
        return datetime.now(timezone.utc).replace(microsecond=0).isoformat()

    def _load_settings_file(self):
        if not os.path.exists(self.settings_file_path):
            return {}

        try:
            with open(self.settings_file_path, "r", encoding="utf-8") as settings_file:
                data = json.load(settings_file)
                return data if isinstance(data, dict) else {}
        except (OSError, json.JSONDecodeError):
            return {}

    def save_config(self):
        settings_payload = dict(self.settings_data)
        settings_payload["last_database_file"] = self.dataBaseFile or ""
        settings_payload["active_draft_path"] = settings_payload.get("active_draft_path", "")

        os.makedirs(os.path.dirname(self.settings_file_path), exist_ok=True)
        with open(self.settings_file_path, "w", encoding="utf-8") as config_file:
            json.dump(settings_payload, config_file, indent=2)

        self.settings_data = settings_payload

    def load_config(self):
        self.settings_data = self._load_settings_file()
        self.dataBaseFile = self.settings_data.get("last_database_file", "")
        if self.dataBaseFile:
            self.load_last_test_number()

        # Restore preferred theme
        theme_mode = self.settings_data.get("theme_mode", "light")
        if theme_mode == "dark" and hasattr(self, "apply_theme_mode"):
            self.apply_theme_mode("dark")
            if hasattr(self, "actionToggleDarkMode"):
                self.actionToggleDarkMode.blockSignals(True)
                self.actionToggleDarkMode.setChecked(True)
                self.actionToggleDarkMode.blockSignals(False)

        active_draft_path = self.settings_data.get("active_draft_path", "")
        if active_draft_path and os.path.exists(active_draft_path):
            self._startup_draft_to_offer = active_draft_path

        self.start_new_draft(reset_state=False, save_settings=False)

    def offer_draft_recovery(self):
        if not self._startup_draft_to_offer:
            return

        draft_path = self._startup_draft_to_offer
        self._startup_draft_to_offer = ""

        reply = QMessageBox.question(
            self,
            "Restore Draft",
            "An autosaved patient draft was found. Would you like to restore it?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes,
        )

        if reply != QMessageBox.Yes:
            self.mark_draft_inactive(draft_path)
            return

        snapshot = self.load_snapshot_from_draft(draft_path)
        if not snapshot:
            QMessageBox.warning(self, "Restore Draft", "The draft could not be restored.")
            self.mark_draft_inactive(draft_path)
            return

        self.activate_snapshot(snapshot, draft_path=draft_path)
        if hasattr(self, "statusbar"):
            self.statusbar.showMessage("Restored autosaved draft", 4000)

    def start_new_draft(self, reset_state=False, save_settings=True):
        if reset_state:
            self.reset_patient_state()

        self.current_draft_id = uuid.uuid4().hex
        self.current_draft_created_at = self._utcnow_iso()
        self.current_draft_path = os.path.join(self.drafts_dir, f"{self.current_draft_id}.json")
        self.last_autosave_signature = None
        self.is_dirty = False
        self.pending_autosave_reason = ""
        if save_settings:
            self.settings_data["active_draft_path"] = ""
            self.save_config()

    def mark_draft_inactive(self, draft_path=None):
        draft_path = draft_path or self.current_draft_path
        if not draft_path:
            return

        if os.path.exists(draft_path):
            try:
                with open(draft_path, "r", encoding="utf-8") as draft_file:
                    snapshot = json.load(draft_file)
                draft_meta = snapshot.setdefault("draft", {})
                draft_meta["is_active"] = False
                draft_meta["updated_at"] = self._utcnow_iso()
                with open(draft_path, "w", encoding="utf-8") as draft_file:
                    json.dump(snapshot, draft_file, indent=2)
            except (OSError, json.JSONDecodeError):
                pass

        if self.settings_data.get("active_draft_path") == draft_path:
            self.settings_data["active_draft_path"] = ""
            self.save_config()

    def _snapshot_signature(self, snapshot):
        signature_snapshot = copy.deepcopy(snapshot)
        draft_meta = signature_snapshot.get("draft", {})
        for key in ("id", "created_at", "updated_at", "is_active"):
            draft_meta.pop(key, None)

        encoded_snapshot = json.dumps(signature_snapshot, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(encoded_snapshot.encode("utf-8")).hexdigest()

    def schedule_autosave(self, reason="change", restart=True):
        if getattr(self, "_is_applying_snapshot", False):
            return

        self.is_dirty = True
        self.pending_autosave_reason = reason
        if restart or not self.autosave_timer.isActive():
            self.autosave_timer.start(self.AUTOSAVE_DELAY_MS)

    def _run_debounced_autosave(self):
        self.force_autosave(self.pending_autosave_reason or "debounced")

    def force_autosave(self, reason="manual"):
        if getattr(self, "_is_applying_snapshot", False):
            return True

        snapshot = self.collect_snapshot()
        if not self.is_autosave_eligible(snapshot):
            return True

        if not self.current_draft_id or not self.current_draft_path:
            self.start_new_draft(reset_state=False)
            snapshot = self.collect_snapshot()

        try:
            export_path = self.get_auto_export_path(snapshot)
        except OSError as error:
            QMessageBox.critical(
                self,
                "Autosave Failed",
                f"HooverTron could not prepare the patient CSV autosave file.\n\n{error}",
            )
            return False

        self.patientDataFile = export_path
        snapshot.setdefault("draft", {})["export_path"] = export_path

        signature = self._snapshot_signature(snapshot)
        if signature == self.last_autosave_signature and reason not in {"close", "recording-stop", "new-patient"}:
            return True

        draft_meta = snapshot.setdefault("draft", {})
        draft_meta["id"] = self.current_draft_id
        draft_meta["created_at"] = self.current_draft_created_at
        draft_meta["updated_at"] = self._utcnow_iso()
        draft_meta["is_active"] = True

        os.makedirs(self.drafts_dir, exist_ok=True)
        temp_path = f"{self.current_draft_path}.tmp"

        try:
            with open(temp_path, "w", encoding="utf-8") as draft_file:
                json.dump(snapshot, draft_file, indent=2)
            os.replace(temp_path, self.current_draft_path)
            self._write_snapshot_csv(export_path, snapshot)
        except OSError as error:
            if os.path.exists(temp_path):
                os.remove(temp_path)
            QMessageBox.critical(
                self,
                "Autosave Failed",
                f"HooverTron could not autosave the current patient draft.\n\n{error}",
            )
            return False

        self.last_autosave_signature = signature
        self.is_dirty = False
        self.settings_data["active_draft_path"] = self.current_draft_path
        self.save_config()

        if hasattr(self, "statusbar"):
            self.statusbar.showMessage("Draft autosaved", 2000)
        return True

    def load_snapshot_from_draft(self, draft_path):
        try:
            with open(draft_path, "r", encoding="utf-8") as draft_file:
                snapshot = json.load(draft_file)
        except (OSError, json.JSONDecodeError):
            return None

        return snapshot if isinstance(snapshot, dict) else None

    def activate_snapshot(self, snapshot, draft_path=None):
        draft_meta = snapshot.get("draft", {})
        self.current_draft_id = draft_meta.get("id") or uuid.uuid4().hex
        self.current_draft_created_at = draft_meta.get("created_at") or self._utcnow_iso()
        self.current_draft_path = draft_path or os.path.join(self.drafts_dir, f"{self.current_draft_id}.json")
        self.apply_snapshot(snapshot)
        self.last_autosave_signature = self._snapshot_signature(self.collect_snapshot())
        self.is_dirty = False
        self.settings_data["active_draft_path"] = self.current_draft_path
        self.save_config()

    def _restore_date(self, date_string, fallback_date):
        if not date_string:
            return fallback_date

        parsed_date = QtCore.QDate.fromString(date_string, QtCore.Qt.ISODate)
        if parsed_date.isValid():
            return parsed_date

        fallback_parsed_date = QtCore.QDate.fromString(date_string)
        if fallback_parsed_date.isValid():
            return fallback_parsed_date

        for fmt in ("ddd MMM d yyyy", "ddd MMM dd yyyy", "yyyy-MM-dd"):
            parsed_date = QtCore.QDate.fromString(date_string, fmt)
            if parsed_date.isValid():
                return parsed_date

        return fallback_date

    def _set_combo_text(self, combo_box, value):
        target_index = combo_box.findText(value or "")
        combo_box.setCurrentIndex(target_index if target_index >= 0 else 0)

    def _set_record_buttons_checked(self, checked):
        for button in (self.pushButton_2, self.pushButton_3, self.pushButton_4):
            button.blockSignals(True)
            button.setChecked(checked)
            button.blockSignals(False)
            button.setText("Stop" if checked else "Record")

    def _step_snapshot_key(self, step_index):
        return f"step_{step_index + 1}"

    def _get_completion_status(self):
        completed_required_steps = sum(1 for index in (1, 2) if self.has_meaningful_step_data(index))
        optional_status = "optional Step 1 complete" if self.has_meaningful_step_data(0) else "optional Step 1 blank"
        return f"{completed_required_steps}/2 required steps complete; {optional_status}"

    def collect_snapshot(self):
        steps = {}
        for step_index, config in self.STEP_CONFIG.items():
            step_key = self._step_snapshot_key(step_index)
            average_widget_attr = config["average_widget_attr"]
            steps[step_key] = {
                "time": list(self.get_step_time_data(step_index)),
                "force": list(self.get_step_force_data(step_index)),
                "average": list(self.get_step_average_data(step_index)),
                "selection": list(self.get_step_selection_range(step_index)),
                "selection_active": self.step_selection_active.get(step_index, False),
                "note": getattr(self, config["note_widget_attr"]).toPlainText(),
                "peak_text": getattr(self, config["peak_widget_attr"]).text(),
                "average_text": getattr(self, average_widget_attr).text() if average_widget_attr else "",
            }

        return {
            "version": self.SNAPSHOT_VERSION,
            "draft": {
                "id": self.current_draft_id,
                "created_at": self.current_draft_created_at,
                "updated_at": self._utcnow_iso(),
                "patient_id": self.patientIdLineEdit.text().strip(),
                "export_path": self.patientDataFile or "",
                "completion_status": self._get_completion_status(),
                "is_active": True,
            },
            "ui": {
                "workflow_tab_id": self.get_current_workflow_tab_id(),
                "main_tab_index": self.tabWidget.currentIndex(),
                "test_tab_index": self.tabWidget_2.currentIndex(),
            },
            "patient": {
                "patient_id": self.patientIdLineEdit.text().strip(),
                "examiner": self.examinerLineEdit.text(),
                "date_of_visit": self.dateOfVisitDateEdit.date().toString(QtCore.Qt.ISODate),
                "reason_for_visit": self.reasonForVisitLineEdit.text(),
                "notes": self.notesLineEdit.text(),
                "dominant_leg": self.dominantLegComboBox.currentText(),
                "selected_leg": self.selectedLegComboBox.currentText(),
            },
            "steps": steps,
            "results": {
                "unaffected_leg_extension": self.unaffectedLegExtensionLLineEdit.text(),
                "affected_leg_voluntary_extension": self.affectedLegVoluntaryExtensionLineEdit.text(),
                "affected_leg_involuntary_extension": self.affectedLegInvoluntaryExtensionLineEdit.text(),
                "ivvr": self.involuntaryVoluntaryRatioAffectedLegLineEdit.text(),
                "analysis": self.label_21.text(),
                "observations": self.textEdit_7.toPlainText(),
            },
        }

    def is_autosave_eligible(self, snapshot):
        patient = snapshot.get("patient", {})
        if not patient.get("patient_id", "").strip():
            return False

        meaningful_patient_fields = (
            patient.get("reason_for_visit"),
            patient.get("notes"),
            patient.get("examiner"),
        )
        if any(value for value in meaningful_patient_fields):
            return True

        if patient.get("dominant_leg", "----") != "----":
            return True
        if patient.get("selected_leg", "----") != "----":
            return True

        for step_key, step_payload in snapshot.get("steps", {}).items():
            force_values = step_payload.get("force", [])
            if len(force_values) > 1 or any(abs(value) > 1e-9 for value in force_values):
                return True
            if step_payload.get("note", "").strip():
                return True

        results = snapshot.get("results", {})
        return bool(results.get("observations", "").strip())

    def _is_legacy_snapshot(self, snapshot):
        return snapshot.get("version", 1) < self.PATIENT_ID_SNAPSHOT_VERSION

    def _warn_legacy_patient_details(self):
        QMessageBox.information(
            self,
            "Older Patient File",
            "This file was saved by an older version of HooverTron. Its personal details "
            "(name, date of birth, age and sex) were not loaded.\n\n"
            "Enter a patient ID on the Patient Info tab so this session can be saved. "
            "Saving writes a new file named by the patient ID.",
        )
        self.set_workflow_tab_by_id("patient")

    def apply_snapshot(self, snapshot):
        self._is_applying_snapshot = True
        if self.autosave_timer.isActive():
            self.autosave_timer.stop()

        is_legacy_snapshot = self._is_legacy_snapshot(snapshot)
        try:
            patient = snapshot.get("patient", {})
            results = snapshot.get("results", {})
            ui_state = snapshot.get("ui", {})
            steps = snapshot.get("steps", {})

            # An older file's name holds the patient's name and date of birth, so save to a new one
            export_path = snapshot.get("draft", {}).get("export_path", "") or ""
            self.patientDataFile = "" if is_legacy_snapshot else export_path

            today = QtCore.QDate.currentDate()
            self.patientIdLineEdit.setText(patient.get("patient_id", ""))
            self.examinerLineEdit.setText(patient.get("examiner", ""))
            self.dateOfVisitDateEdit.setDate(self._restore_date(patient.get("date_of_visit", ""), today))
            self.reasonForVisitLineEdit.setText(patient.get("reason_for_visit", ""))
            self.notesLineEdit.setText(patient.get("notes", ""))
            self._set_combo_text(self.dominantLegComboBox, patient.get("dominant_leg", "----"))
            self._set_combo_text(self.selectedLegComboBox, patient.get("selected_leg", "----"))

            for step_index, config in self.STEP_CONFIG.items():
                step_payload = steps.get(self._step_snapshot_key(step_index), {})
                self.set_step_data(
                    step_index,
                    time_data=step_payload.get("time", [0.0]),
                    force_data=step_payload.get("force", [0.0]),
                    average_data=step_payload.get("average", [0.0]),
                )
                self.step_selection_active[step_index] = bool(step_payload.get("selection_active", False))
                getattr(self, config["note_widget_attr"]).setPlainText(step_payload.get("note", ""))
                self.update_step_plot(step_index)
                self.set_step_selection_range(
                    step_index,
                    step_payload.get("selection", (0.0, 1.0)),
                    active=self.step_selection_active[step_index],
                )

            self.refresh_all_step_measurements()
            if results.get("unaffected_leg_extension"):
                self._set_line_edit_text(
                    self.unaffectedLegExtensionLLineEdit, results.get("unaffected_leg_extension", "")
                )
            if results.get("affected_leg_voluntary_extension"):
                self._set_line_edit_text(
                    self.affectedLegVoluntaryExtensionLineEdit,
                    results.get("affected_leg_voluntary_extension", ""),
                )
            if results.get("affected_leg_involuntary_extension"):
                self._set_line_edit_text(
                    self.affectedLegInvoluntaryExtensionLineEdit,
                    results.get("affected_leg_involuntary_extension", ""),
                )
            if results.get("ivvr"):
                self._set_line_edit_text(
                    self.involuntaryVoluntaryRatioAffectedLegLineEdit, results.get("ivvr", "")
                )
            self.label_21.setText(results.get("analysis") or self.label_21.text() or self.DEFAULT_ANALYSIS_TEXT)
            self.textEdit_7.setPlainText(results.get("observations", ""))

            workflow_tab_id = ui_state.get("workflow_tab_id")
            if not workflow_tab_id:
                workflow_tab_id = self.get_workflow_tab_id_from_legacy_state(
                    ui_state.get("main_tab_index", 0),
                    ui_state.get("test_tab_index", 0),
                )
            self.set_workflow_tab_by_id(workflow_tab_id)
            self._set_record_buttons_checked(False)
            self.is_recording = False
        finally:
            self._is_applying_snapshot = False

        if is_legacy_snapshot:
            self._warn_legacy_patient_details()

    def reset_patient_state(self):
        self._is_applying_snapshot = True
        if self.autosave_timer.isActive():
            self.autosave_timer.stop()

        try:
            today = QtCore.QDate.currentDate()
            self.patientDataFile = ""
            self.patientIdLineEdit.clear()
            self.dateOfVisitDateEdit.setDate(today)
            self.reasonForVisitLineEdit.clear()
            self.notesLineEdit.clear()
            # The examiner is kept: the same clinician usually tests the next patient
            self.dominantLegComboBox.setCurrentIndex(0)
            self.selectedLegComboBox.setCurrentIndex(0)

            self.textEdit.clear()
            self.textEdit_2.clear()
            self.textEdit_6.clear()
            self.textEdit_7.clear()

            self.reset_all_step_states()

            self.unaffectedLegExtensionLLineEdit.clear()
            self.affectedLegVoluntaryExtensionLineEdit.clear()
            self.affectedLegInvoluntaryExtensionLineEdit.clear()
            self.involuntaryVoluntaryRatioAffectedLegLineEdit.clear()
            self.label_21.setText(self.DEFAULT_ANALYSIS_TEXT)

            self._set_record_buttons_checked(False)
            self.is_recording = False
            self.set_workflow_tab_by_id("patient")
        finally:
            self._is_applying_snapshot = False

        self.is_dirty = False
        self.last_autosave_signature = None

    def load_last_test_number(self):
        if not os.path.exists(self.dataBaseFile):
            self.testNumber = 1
            self.isNewDatabase = True
            return

        with open(self.dataBaseFile, "r", encoding="utf-8", newline="") as database_file:
            reader = csv.reader(database_file)
            next(reader, None)
            last_test_number = 0
            for row in reader:
                if not row:
                    continue
                try:
                    last_test_number = int(row[0])
                except (TypeError, ValueError):
                    continue

        self.testNumber = last_test_number or 1
        self.isNewDatabase = False
