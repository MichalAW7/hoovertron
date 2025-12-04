# hoover_backend/file_mixin.py
import os
import csv
from datetime import datetime
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMessageBox, QFileDialog

class FileMixin:
    def show_message(self, title, message, icon=QMessageBox.Information):
        msg = QMessageBox()
        msg.setIcon(icon)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec_()

    def file_open(self):
        name, _ = QFileDialog.getOpenFileName(self, caption='Open File', directory=os.getcwd() + r"\ ",
                                                        filter="CSV Files (*.csv)")
        if name:
            try:
                with open(name, 'r') as read_obj:
                    csv_reader = csv.reader(read_obj)
                    counter = 0
                    for row in csv_reader:
                        if counter == 0:
                            self.nameLineEdit.setText(row[1])
                            self.preferredNameLineEdit.setText(row[2])
                            bday = QtCore.QDate.fromString(row[3])
                            self.dateOfBirthDateEdit.setDate(bday)
                            vday = QtCore.QDate.fromString(row[4])
                            self.dateOfVisitDateEdit.setDate(vday)
                            self.ageLineEdit.setText(row[5])
                            self.sexLineEdit.setText(row[6])

                            self.reasonForVisitLineEdit.setText(row[7])
                            self.notesLineEdit.setText(row[8])
                            self.examinerLineEdit.setText(row[9])
                            self.dominantLegLineEdit.setText(row[10])
                            self.selectLegLineEdit.setText(row[11])
                        elif counter == 2:
                            del row[0]
                            self.hsS1RForce = [float(x) for x in row]
                            self.hsS1RForceLine.setData(self.hsS1RForce)
                        elif counter == 6:
                            del row[0]
                            self.hsS2RForce = [float(x) for x in row]
                            self.hsS2RForceLine.setData(self.hsS2RForce)
                        elif counter == 8:
                            del row[0]
                            self.hsS2RAverage = [float(x) for x in row]
                            self.hsS2RAverageLine.setData(self.hsS2RAverage)
                        elif counter == 10:
                            del row[0]
                            self.hsS3RForce = [float(x) for x in row]
                            self.hsS3RForceLine.setData(self.hsS3RForce)
                        elif counter == 12:
                            del row[0]
                            self.hsS3RAverage = [float(x) for x in row]
                            self.hsS3RForceAverageLine.setData(self.hsS3RAverage)
                        elif counter == 16:
                            self.textEdit.setText(row[1])
                            self.textEdit_2.setText(row[2])
                            self.textEdit_6.setText(row[3])
                            self.textEdit_7.setText(row[4])
                        counter += 1

                self.extensionForceLineEdit.setText(str(max(self.hsS1RForce)))
                self.strongLegAverageStrengthLineEdit_2.setText(str(max(self.hsS2RAverage)))
                self.strongLegPeakStrengthLineEdit_2.setText(str(max(self.hsS2RForce)))
                self.weakLegPeakStrengthLineEdit_3.setText(str(max(self.hsS3RForce)))
                self.fill_values()

            except FileNotFoundError:
                QMessageBox.critical(self, "File Error", "The selected file does not exist.")
            except PermissionError:
                QMessageBox.critical(self, "Permission Error",
                                               "You don't have permission to access this file.")
            except Exception as e: None

    def file_save(self):
        if self.patientDataFile != '' :
            with open(self.patientDataFile, 'w', encoding='UTF8') as f:
                writer = csv.writer(f)
                writer.writerow(["Patient Information:", self.nameLineEdit.text(), self.preferredNameLineEdit.text(),
                                 self.dateOfBirthDateEdit.date().toString(), self.dateOfVisitDateEdit.date().toString(), self.ageLineEdit.text(),
                                 self.sexComboBox.currentText(),
                                 self.reasonForVisitLineEdit.text(),
                                 self.notesLineEdit.text(),
                                 self.examinerLineEdit.text(), self.dominantLegComboBox.currentText(), self.selectedLegComboBox.currentText()
                                 ])
                self.hsS1RForce.insert(0, "HS step 1 extension force: ")
                writer.writerow(self.hsS1RForce)
                self.hsS2RForce.insert(0, "HS step 2 extension force: ")
                writer.writerow(self.hsS2RForce)
                self.hsS2RAverage.insert(0, "HS step 2 extension force average: ")
                writer.writerow(self.hsS2RAverage)
                self.hsS3RForce.insert(0, "HS step 3 extension force: ")
                writer.writerow(self.hsS3RForce)
                self.hsS3RAverage.insert(0, "HS step 3 extension force average: ")
                writer.writerow(self.hsS3RAverage)
                writer.writerow(["Text edit contents: ", self.textEdit.toPlainText(), self.textEdit_2.toPlainText(),
                                 self.textEdit_6.toPlainText(), self.textEdit_7.toPlainText()])
                writer.writerow([
                                 "Unaffected leg extension:", 
                                 "Affected leg voluntary extension (V):", "Affected leg involuntary extension (IV):",
                                 "Affected leg involuntary/voluntary ratio (IVVR = IV/V):",
                                ])
                writer.writerow([
                                 self.extensionForceLineEdit.text(),
                                 self.strongLegPeakStrengthLineEdit_2.text(),
                                 self.strongLegAverageStrengthLineEdit_2.text(),
                                 self.weakLegPeakStrengthLineEdit_3.text(),
                                 self.involuntaryVoluntaryRatioAffectedLegLineEdit.text()
                                ])
            print("File saved successfully as: " + self.patientDataFile)
        else:
            print("Error! You must create a New File before saving!")

    def file_new(self):
        name = QFileDialog.getSaveFileName(self, caption="New File", directory=os.getcwd() + r"\patient data", filter="CSV Files (*.csv)")
        self.patientDataFile = name[0]
        with open(self.patientDataFile, 'w', encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerow(["Patient Information:", self.nameLineEdit.text(), self.preferredNameLineEdit.text(),
                             self.dateOfBirthDateEdit.date().toString(), self.dateOfVisitDateEdit.date().toString(),
                             self.ageLineEdit.text(),
                             self.sexComboBox.currentText(),
                             self.reasonForVisitLineEdit.text(),
                             self.notesLineEdit.text(),
                             self.examinerLineEdit.text(), self.dominantLegComboBox.currentText(), self.selectedLegComboBox.currentText()
                             ])
            self.hsS1RForce.insert(0, "HS step 1 extension force: ")
            writer.writerow(self.hsS1RForce)
            self.hsS2RForce.insert(0, "HS step 2 extension force: ")
            writer.writerow(self.hsS2RForce)
            self.hsS2RAverage.insert(0, "HS step 2 extension force average: ")
            writer.writerow(self.hsS2RAverage)
            self.hsS3RForce.insert(0, "HS step 3 extension force: ")
            writer.writerow(self.hsS3RForce)
            self.hsS3RAverage.insert(0, "HS step 3 extension force average: ")
            writer.writerow(self.hsS3RAverage)
            writer.writerow(["Text edit contents: ", self.textEdit.toPlainText(), self.textEdit_2.toPlainText(),
                             self.textEdit_6.toPlainText(), self.textEdit_7.toPlainText()])
            writer.writerow(
                [ "Unaffected leg extension:", 
                 "Affected leg voluntary extension (V):", "Affected leg involuntary extension (IV):",
                 "Affected leg involuntary/voluntary ratio (IVVR = IV/V):"
                  ])
            writer.writerow([
                             self.extensionForceLineEdit.text(),
                             self.strongLegPeakStrengthLineEdit_2.text(),
                             self.strongLegAverageStrengthLineEdit_2.text(),
                             self.weakLegPeakStrengthLineEdit_3.text(),
                             self.involuntaryVoluntaryRatioAffectedLegLineEdit.text()
                               ])
        print("File saved successfully.")

    def file_new_database(self):
        name, _ = QFileDialog.getSaveFileName(self, caption="New File", directory=os.getcwd() + "\\FND patient database", filter="CSV Files (*.csv)")
        self.dataBaseFile = name
        if self.dataBaseFile:
            self.testNumber = 1
            with open(self.dataBaseFile, 'w', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Test Number", "System Date and Time",
                                 "Patient Name",
                                 "Preferred Name",
                                 "Date of Birth",
                                 "Date of Visit",
                                 "Age", "Sex",
                                 "Reason For Visit",
                                 "Notes", "Examiner Name",
                                 "Dominant Leg", "Selected Leg",
                                 "Unaffected leg extension",
                                 "Affected leg voluntary extension (V)",
                                 "Affected leg involuntary extension (IV)",
                                 "Affected leg involuntary/voluntary ratio (IVVR = IV/V)",])


                writer.writerow([self.testNumber, datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                                 self.nameLineEdit.text(),
                                 self.preferredNameLineEdit.text(),
                                 self.dateOfBirthDateEdit.date().toString(),
                                 self.dateOfVisitDateEdit.date().toString(),
                                 self.ageLineEdit.text(), self.sexComboBox.currentText(),
                                 self.reasonForVisitLineEdit.text(),
                                 self.notesLineEdit.text(), self.examinerLineEdit.text(),
                                 self.dominantLegComboBox.currentText(), self.selectedLegComboBox.currentText(),
                                 self.extensionForceLineEdit.text(),
                                 self.strongLegPeakStrengthLineEdit_2.text(),
                                 self.weakLegPeakStrengthLineEdit_3.text(),
                                 self.involuntaryVoluntaryRatioAffectedLegLineEdit.text()])

            self.isNewDatabase = False
            self.save_config()
            self.show_message("Database Created", "Database created successfully!!!")
            print("File created successfully.")

    def file_open_database(self):
        name, _ = QFileDialog.getOpenFileName(self, caption="Open File", directory=os.getcwd(),
                                              filter="CSV Files (*.csv)")
        self.dataBaseFile = name
        if self.dataBaseFile:
            self.load_last_test_number()
            self.save_config()
            self.show_message("Database Opened", "Database opened successfully!!!")
            print("Database opened successfully!!!")

    def file_update_database(self):
        if self.dataBaseFile:
            try:
                with open(self.dataBaseFile, 'a', encoding='UTF8', newline='') as f:
                    writer = csv.writer(f)
                    self.testNumber += 1
                    writer.writerow(
                        [self.testNumber, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.nameLineEdit.text(),
                         self.preferredNameLineEdit.text(), self.dateOfBirthDateEdit.date().toString(),
                         self.dateOfVisitDateEdit.date().toString(), self.ageLineEdit.text(),
                         self.sexComboBox.currentText(), self.reasonForVisitLineEdit.text(), self.notesLineEdit.text(),
                         self.examinerLineEdit.text(), self.dominantLegComboBox.currentText(),
                         self.selectedLegComboBox.currentText(), self.extensionForceLineEdit.text(),
                         self.strongLegPeakStrengthLineEdit_2.text(), self.weakLegPeakStrengthLineEdit_3.text(),
                         self.involuntaryVoluntaryRatioAffectedLegLineEdit.text()])

                    self.show_message("Data Saved", "Data saved successfully in the database!!!")
                    print("File saved successfully as: " + self.dataBaseFile)
            except PermissionError:
                self.show_message("Permission Denied", "Permission denied: file is running in another application",
                                  icon=QMessageBox.Critical)
                print("Error: Permission denied: file is running in another application")
        else:
            print("Error! You must create a New File before saving!")