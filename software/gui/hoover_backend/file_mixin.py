import csv
import json
import os
import re
from datetime import datetime

from PyQt5 import QtCore
from PyQt5.QtWidgets import QFileDialog, QMessageBox

from config import get_patient_exports_dir


class FileMixin:
    def show_message(self, title, message, icon=QMessageBox.Information):
        msg = QMessageBox()
        msg.setIcon(icon)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec_()

    def _default_export_directory(self):
        if self.patientDataFile:
            return os.path.dirname(self.patientDataFile)
        return get_patient_exports_dir()

    def _sanitize_filename_part(self, value, fallback):
        cleaned_value = re.sub(r'[<>:"/\\|?*]+', "_", (value or "").strip())
        cleaned_value = re.sub(r"[\s_]+", "_", cleaned_value).strip("._-")
        return cleaned_value or fallback

    def _auto_export_base_path(self, snapshot):
        patient = snapshot.get("patient", {})
        patient_name = self._sanitize_filename_part(patient.get("name", ""), "Unnamed_Patient")
        date_of_birth = self._sanitize_filename_part(patient.get("date_of_birth", ""), "Unknown-DOB")
        date_of_visit = self._sanitize_filename_part(patient.get("date_of_visit", ""), "Unknown-Visit")
        filename = f"{patient_name}_{date_of_birth}-DOB_{date_of_visit}-Visit.csv"
        return os.path.join(get_patient_exports_dir(), filename)

    def _csv_path_matches_current_draft(self, path):
        if not path or not os.path.exists(path) or not self.current_draft_id:
            return False

        try:
            snapshot = self.load_snapshot_from_csv(path)
        except OSError:
            return False

        return snapshot.get("draft", {}).get("id") == self.current_draft_id

    def get_auto_export_path(self, snapshot):
        if self.patientDataFile:
            return self.patientDataFile

        base_path = self._auto_export_base_path(snapshot)
        if not os.path.exists(base_path) or self._csv_path_matches_current_draft(base_path):
            return base_path

        root, extension = os.path.splitext(base_path)
        suffix = 2
        while True:
            candidate_path = f"{root}-{suffix}{extension}"
            if not os.path.exists(candidate_path) or self._csv_path_matches_current_draft(candidate_path):
                return candidate_path
            suffix += 1

    def _prompt_to_replace_current_patient(self, action_title):
        if self.is_recording:
            QMessageBox.warning(self, action_title, "Please stop recording before continuing.")
            return False

        current_snapshot = self.collect_snapshot()
        if not self.is_autosave_eligible(current_snapshot):
            return True

        if not self.force_autosave(f"before-{action_title.lower().replace(' ', '-')}"):
            return False

        reply = QMessageBox.question(
            self,
            action_title,
            "The current patient has been autosaved. Continue and replace the active patient?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        return reply == QMessageBox.Yes

    def _serialize_export_rows(self, snapshot):
        patient = snapshot.get("patient", {})
        results = snapshot.get("results", {})
        steps = snapshot.get("steps", {})

        return [
            [
                "Patient Information:",
                patient.get("name", ""),
                patient.get("preferred_name", ""),
                patient.get("date_of_birth", ""),
                patient.get("date_of_visit", ""),
                patient.get("age", ""),
                patient.get("sex", ""),
                patient.get("reason_for_visit", ""),
                patient.get("notes", ""),
                patient.get("examiner", ""),
                patient.get("dominant_leg", ""),
                patient.get("selected_leg", ""),
            ],
            ["HS step 1 extension force:"] + steps.get("step_1", {}).get("force", []),
            ["HS step 2 extension force:"] + steps.get("step_2", {}).get("force", []),
            ["HS step 2 extension force average:"] + steps.get("step_2", {}).get("average", []),
            ["HS step 3 extension force:"] + steps.get("step_3", {}).get("force", []),
            ["HS step 3 extension force average:"] + steps.get("step_3", {}).get("average", []),
            [
                "Text edit contents:",
                steps.get("step_1", {}).get("note", ""),
                steps.get("step_2", {}).get("note", ""),
                steps.get("step_3", {}).get("note", ""),
                results.get("observations", ""),
            ],
            [
                "Unaffected leg extension:",
                "Affected leg voluntary extension (V):",
                "Affected leg involuntary extension (IV):",
                "Affected leg involuntary/voluntary ratio (IVVR = IV/V):",
            ],
            [
                results.get("unaffected_leg_extension", ""),
                results.get("affected_leg_voluntary_extension", ""),
                steps.get("step_2", {}).get("average_text", ""),
                results.get("affected_leg_involuntary_extension", ""),
                results.get("ivvr", ""),
            ],
            [self.SNAPSHOT_JSON_LABEL, json.dumps(snapshot, separators=(",", ":"))],
        ]

    def _read_csv_rows(self, path):
        with open(path, "r", encoding="utf-8", newline="") as csv_file:
            return list(csv.reader(csv_file))

    def _float_list_from_row(self, row):
        values = []
        for raw_value in row[1:]:
            try:
                values.append(float(raw_value))
            except (TypeError, ValueError):
                continue
        return values or [0.0]

    def _build_legacy_snapshot(self, rows, source_path):
        today = QtCore.QDate.currentDate().toString(QtCore.Qt.ISODate)
        snapshot = {
            "version": self.SNAPSHOT_VERSION,
            "draft": {
                "id": "",
                "created_at": self._utcnow_iso(),
                "updated_at": self._utcnow_iso(),
                "patient_name": "",
                "export_path": source_path,
                "completion_status": "legacy import",
                "is_active": True,
            },
            "ui": {"main_tab_index": 0, "test_tab_index": 0},
            "patient": {
                "name": "",
                "preferred_name": "",
                "date_of_birth": today,
                "date_of_visit": today,
                "age": "",
                "sex": "----",
                "reason_for_visit": "",
                "notes": "",
                "examiner": "",
                "dominant_leg": "----",
                "selected_leg": "----",
            },
            "steps": {
                "step_1": {
                    "time": [0.0],
                    "force": [0.0],
                    "average": [0.0],
                    "selection": [0.0, 1.0],
                    "selection_active": False,
                    "note": "",
                    "peak_text": "",
                    "average_text": "",
                },
                "step_2": {
                    "time": [0.0],
                    "force": [0.0],
                    "average": [0.0],
                    "selection": [0.0, 1.0],
                    "selection_active": False,
                    "note": "",
                    "peak_text": "",
                    "average_text": "",
                },
                "step_3": {
                    "time": [0.0],
                    "force": [0.0],
                    "average": [0.0],
                    "selection": [0.0, 1.0],
                    "selection_active": False,
                    "note": "",
                    "peak_text": "",
                    "average_text": "",
                },
            },
            "results": {
                "unaffected_leg_extension": "",
                "affected_leg_voluntary_extension": "",
                "affected_leg_involuntary_extension": "",
                "ivvr": "",
                "analysis": self.DEFAULT_ANALYSIS_TEXT,
                "observations": "",
            },
        }

        expect_results_row = False
        for row in rows:
            if not row:
                continue

            label = row[0].strip()
            if label == "Patient Information:":
                snapshot["patient"] = {
                    "name": row[1] if len(row) > 1 else "",
                    "preferred_name": row[2] if len(row) > 2 else "",
                    "date_of_birth": row[3] if len(row) > 3 else today,
                    "date_of_visit": row[4] if len(row) > 4 else today,
                    "age": row[5] if len(row) > 5 else "",
                    "sex": row[6] if len(row) > 6 else "----",
                    "reason_for_visit": row[7] if len(row) > 7 else "",
                    "notes": row[8] if len(row) > 8 else "",
                    "examiner": row[9] if len(row) > 9 else "",
                    "dominant_leg": row[10] if len(row) > 10 else "----",
                    "selected_leg": row[11] if len(row) > 11 else "----",
                }
                snapshot["draft"]["patient_name"] = snapshot["patient"]["name"]
            elif label == "HS step 1 extension force:":
                force_values = self._float_list_from_row(row)
                snapshot["steps"]["step_1"]["force"] = force_values
                snapshot["steps"]["step_1"]["time"] = [float(index) for index in range(len(force_values))]
            elif label == "HS step 2 extension force:":
                force_values = self._float_list_from_row(row)
                snapshot["steps"]["step_2"]["force"] = force_values
                snapshot["steps"]["step_2"]["time"] = [float(index) for index in range(len(force_values))]
            elif label == "HS step 2 extension force average:":
                snapshot["steps"]["step_2"]["average"] = self._float_list_from_row(row)
            elif label == "HS step 3 extension force:":
                force_values = self._float_list_from_row(row)
                snapshot["steps"]["step_3"]["force"] = force_values
                snapshot["steps"]["step_3"]["time"] = [float(index) for index in range(len(force_values))]
            elif label == "HS step 3 extension force average:":
                snapshot["steps"]["step_3"]["average"] = self._float_list_from_row(row)
            elif label == "Text edit contents:":
                snapshot["steps"]["step_1"]["note"] = row[1] if len(row) > 1 else ""
                snapshot["steps"]["step_2"]["note"] = row[2] if len(row) > 2 else ""
                snapshot["steps"]["step_3"]["note"] = row[3] if len(row) > 3 else ""
                snapshot["results"]["observations"] = row[4] if len(row) > 4 else ""
            elif label == "Unaffected leg extension:":
                expect_results_row = True
            elif expect_results_row:
                snapshot["results"]["unaffected_leg_extension"] = row[0] if len(row) > 0 else ""
                snapshot["results"]["affected_leg_voluntary_extension"] = row[1] if len(row) > 1 else ""
                snapshot["steps"]["step_2"]["average_text"] = row[2] if len(row) > 2 else ""
                snapshot["results"]["affected_leg_involuntary_extension"] = row[3] if len(row) > 3 else ""
                snapshot["results"]["ivvr"] = row[4] if len(row) > 4 else ""
                expect_results_row = False

        return snapshot

    def load_snapshot_from_csv(self, path):
        rows = self._read_csv_rows(path)
        for row in rows:
            if row and row[0].strip() == self.SNAPSHOT_JSON_LABEL and len(row) > 1:
                try:
                    snapshot = json.loads(row[1])
                except json.JSONDecodeError:
                    break
                snapshot.setdefault("draft", {})["export_path"] = path
                return snapshot

        return self._build_legacy_snapshot(rows, path)

    def _write_snapshot_csv(self, path, snapshot):
        directory = os.path.dirname(path)
        if directory:
            os.makedirs(directory, exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="") as export_file:
            writer = csv.writer(export_file)
            writer.writerows(self._serialize_export_rows(snapshot))

    def export_snapshot_to_csv(self, path, set_active_path=True):
        snapshot = self.collect_snapshot()
        snapshot.setdefault("draft", {})["export_path"] = path
        self._write_snapshot_csv(path, snapshot)

        if set_active_path:
            self.patientDataFile = path
        if hasattr(self, "statusbar"):
            self.statusbar.showMessage(f"Saved patient export to {path}", 4000)

    def file_save(self):
        snapshot = self.collect_snapshot()
        path = self.get_auto_export_path(snapshot)
        self.export_snapshot_to_csv(path, set_active_path=True)
        self.force_autosave("manual-export")

    def file_save_as(self):
        path, _ = QFileDialog.getSaveFileName(
            self,
            caption="Save Patient As",
            directory=self._default_export_directory(),
            filter="CSV Files (*.csv)",
        )
        if path:
            self.export_snapshot_to_csv(path, set_active_path=False)

    def file_open(self):
        if not self._prompt_to_replace_current_patient("Open Patient"):
            return

        path, _ = QFileDialog.getOpenFileName(
            self,
            caption="Open Patient",
            directory=self._default_export_directory(),
            filter="CSV Files (*.csv)",
        )
        if not path:
            return

        try:
            snapshot = self.load_snapshot_from_csv(path)
        except OSError as error:
            QMessageBox.critical(self, "Open Patient", f"Unable to open the patient file.\n\n{error}")
            return

        self.mark_draft_inactive()
        self.start_new_draft(reset_state=False)
        self.apply_snapshot(snapshot)
        self.patientDataFile = path
        self.force_autosave("open-patient")

    def file_open_draft(self):
        if not self._prompt_to_replace_current_patient("Open Draft"):
            return

        path, _ = QFileDialog.getOpenFileName(
            self,
            caption="Open Draft",
            directory=self.drafts_dir,
            filter="Draft Files (*.json)",
        )
        if not path:
            return

        snapshot = self.load_snapshot_from_draft(path)
        if not snapshot:
            QMessageBox.warning(self, "Open Draft", "The selected draft could not be loaded.")
            return

        self.mark_draft_inactive()
        self.activate_snapshot(snapshot, draft_path=path)

    def new_patient(self):
        if self.is_recording:
            QMessageBox.warning(self, "New Patient", "Please stop recording before starting a new patient.")
            return

        current_snapshot = self.collect_snapshot()
        if self.is_autosave_eligible(current_snapshot):
            if not self.force_autosave("new-patient"):
                return

        self.mark_draft_inactive()
        self.start_new_draft(reset_state=True)
        if hasattr(self, "statusbar"):
            self.statusbar.showMessage("Ready for a new patient", 3000)

    def file_new_database(self):
        name, _ = QFileDialog.getSaveFileName(
            self,
            caption="Create Database",
            directory=self._default_export_directory(),
            filter="CSV Files (*.csv)",
        )
        self.dataBaseFile = name
        if self.dataBaseFile:
            self.testNumber = 1
            with open(self.dataBaseFile, "w", encoding="utf-8", newline="") as database_file:
                writer = csv.writer(database_file)
                writer.writerow(
                    [
                        "Test Number",
                        "System Date and Time",
                        "Patient Name",
                        "Preferred Name",
                        "Date of Birth",
                        "Date of Visit",
                        "Age",
                        "Sex",
                        "Reason For Visit",
                        "Notes",
                        "Examiner Name",
                        "Dominant Leg",
                        "Selected Leg",
                        "Unaffected leg extension",
                        "Affected leg voluntary extension (V)",
                        "Affected leg involuntary extension (IV)",
                        "Affected leg involuntary/voluntary ratio (IVVR = IV/V)",
                    ]
                )
                writer.writerow(
                    [
                        self.testNumber,
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        self.nameLineEdit.text(),
                        self.preferredNameLineEdit.text(),
                        self.dateOfBirthDateEdit.date().toString(),
                        self.dateOfVisitDateEdit.date().toString(),
                        self.ageLineEdit.text(),
                        self.sexComboBox.currentText(),
                        self.reasonForVisitLineEdit.text(),
                        self.notesLineEdit.text(),
                        self.examinerLineEdit.text(),
                        self.dominantLegComboBox.currentText(),
                        self.selectedLegComboBox.currentText(),
                        self.extensionForceLineEdit.text(),
                        self.unaffectedLegPeakStrengthLineEdit_2.text(),
                        self.affectedLegPeakStrengthLineEdit_3.text(),
                        self.involuntaryVoluntaryRatioAffectedLegLineEdit.text(),
                    ]
                )

            self.isNewDatabase = False
            self.save_config()
            self.show_message("Database Created", "Database created successfully.")

    def file_open_database(self):
        name, _ = QFileDialog.getOpenFileName(
            self,
            caption="Open Database",
            directory=self._default_export_directory(),
            filter="CSV Files (*.csv)",
        )
        self.dataBaseFile = name
        if self.dataBaseFile:
            self.load_last_test_number()
            self.save_config()
            self.show_message("Database Opened", "Database opened successfully.")

    def file_update_database(self):
        if not self.dataBaseFile:
            QMessageBox.warning(self, "Update Database", "Open or create a database before saving.")
            return

        self.fill_values()
        try:
            with open(self.dataBaseFile, "a", encoding="utf-8", newline="") as database_file:
                writer = csv.writer(database_file)
                self.testNumber += 1
                writer.writerow(
                    [
                        self.testNumber,
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        self.nameLineEdit.text(),
                        self.preferredNameLineEdit.text(),
                        self.dateOfBirthDateEdit.date().toString(),
                        self.dateOfVisitDateEdit.date().toString(),
                        self.ageLineEdit.text(),
                        self.sexComboBox.currentText(),
                        self.reasonForVisitLineEdit.text(),
                        self.notesLineEdit.text(),
                        self.examinerLineEdit.text(),
                        self.dominantLegComboBox.currentText(),
                        self.selectedLegComboBox.currentText(),
                        self.extensionForceLineEdit.text(),
                        self.unaffectedLegPeakStrengthLineEdit_2.text(),
                        self.affectedLegPeakStrengthLineEdit_3.text(),
                        self.involuntaryVoluntaryRatioAffectedLegLineEdit.text(),
                    ]
                )

            self.show_message("Data Saved", "Data saved successfully in the database.")
        except PermissionError:
            self.show_message(
                "Permission Denied",
                "Permission denied: file is open in another application.",
                icon=QMessageBox.Critical,
            )
