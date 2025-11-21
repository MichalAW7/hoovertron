# hoover_logic.py
import sys, os, math, bisect
import statistics as st
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QFileDialog
from PyQt5.QtCore import Qt, pyqtSignal, QDate
import csv
from csv import reader
import configparser
from datetime import datetime
import matplotlib.pyplot as plt
import random
import numpy as np
import re
import errno
import asyncio
from bleak import BleakClient, BleakScanner

from ui_layout import Ui_Layout
from config import CONFIG_FILE_PATH

# BLE UUIDs (must match Arduino firmware)
SERVICE_UUID = "180D"
CHARACTERISTIC_UUID = "2A37"

class HooverTronWindow(QMainWindow, Ui_Layout):
    def __init__(self):
        super().__init__()
        self.timeData = [0]
        self.hsS1RForce = [0]
        self.hsS1LForce = [0]
        self.hsS2RForce = [0]
        self.hsS2LForce = [0]
        self.hsS3RForce = [0]
        self.hsS3RAverage = [0]
        self.hsS3LForce = [0]
        self.hsS2RAverage = [0]
        self.dataBaseFile = ''
        self.testNumber = 1
        self.isNewDatabase = False
        self.currentFrequency = 10
        self.start_time_input = [[], [], []]
        self.end_time_input = [[], [], []]
        self.select_button = [[], [], []]
        self.data_x = [[], [], []]
        self.data_y = [[], [], []]
        self.patientDataFile = ''
        self.databaseFile = ''
        
        # BLE related attributes
        self.ble_client = None
        self.ble_device = None
        self.is_connected = False
        self.data_buffer = ""

        self.load_config()
        self.setupUi(self)

    def update_data(self):
        if self.select_button:
            if self.tabWidget_2.currentIndex() == 0:
                new_data_point = (self.hsS1RForce)
            elif self.tabWidget_2.currentIndex() == 1:
                new_data_point = (self.hsS2RForce)
            elif self.tabWidget_2.currentIndex() == 2:
                new_data_point = (self.hsS3RForce)
        else:
            new_data_point = 0.0

        x_a, x_b = self.selection_region.getRegion()
        start_a = float(str(x_a))
        start_b = "{:.2f}".format(start_a)
        x_a = float(start_b)

        end_a = float(str(x_b))
        end_b = "{:.2f}".format(end_a)
        x_b = float(end_b)

    def update_selection(self, checked):
        current_index = self.tabWidget_2.currentIndex()
        xmin, xmax = self.selection_region[current_index].getRegion()

        start_a = float(str(xmin))
        start_b = "{:.2f}".format(start_a)
        xmin = float(start_b)

        end_a = float(str(xmax))
        end_b = "{:.2f}".format(end_a)
        xmax = float(end_b)

        self.start_time_input[current_index][0].setText(str(xmin))
        self.end_time_input[current_index][0].setText(str(xmax))

    def select_time_period(self):
        button = self.sender()
        button.setStyleSheet("background-color: green; color: white; font-weight: bold; font-size: 16px;")

        current_index = self.tabWidget_2.currentIndex()
        xmin, xmax = self.selection_region[current_index].getRegion()

        start_time = float("{:.2f}".format(xmin))
        end_time = float("{:.2f}".format(xmax))

        selected_data = None
        if current_index == 0:
            selected_data = self.hsS1RForce
            average_data = None
            average_widget = None
            peak_widget = self.extensionForceLineEdit
        elif current_index == 1:
            selected_data = self.hsS2RForce
            average_data = self.hsS2RAverage
            average_widget = self.strongLegAverageStrengthLineEdit_2
            peak_widget = self.strongLegPeakStrengthLineEdit_2
        elif current_index == 2:
            selected_data = self.hsS3RForce
            average_data = None
            average_widget = None
            peak_widget = self.weakLegPeakStrengthLineEdit_3

        if selected_data is not None:
            selected_data_filtered = [value for idx, value in enumerate(selected_data) if
                                      self.timeData[idx] >= start_time and self.timeData[idx] <= end_time]

            peak_value = max(selected_data_filtered, default=None)
            peak_widget.setText(str(peak_value) if peak_value is not None else 'N/A')

        if average_data is not None:
            average_data_filtered = [value for idx, value in enumerate(average_data) if
                                      self.timeData[idx] >= start_time and self.timeData[idx] <= end_time]

            average_value =max(average_data_filtered, default=None)
            average_widget.setText(str(average_value) if average_value is not None else 'N/A')

    def notification_handler(self, sender, data):
        """Handle BLE notifications from the Arduino"""
        try:
            text = data.decode('utf-8', errors='ignore').strip()
            
            # Add to buffer
            self.data_buffer += text
            
            # Process complete lines (ending with newline or complete data packet)
            if ',' in self.data_buffer:
                # Extract complete message
                text_to_process = self.data_buffer
                self.data_buffer = ""
                
                if not text_to_process:
                    return

                if text_to_process.startswith("Frequency updated to:"):
                    print(f"ARDUINO CONFIRMATION >> {text_to_process}")
                    return

                words = text_to_process.split(",")
                current_index = self.tabWidget_2.currentIndex()

                time_value = float(words[0])/300000
                force_value = float(words[1])
                force_average_value = float(words[3]) if len(words) > 3 else None

                if current_index == 0:
                    previous_time = self.timeData[-1]
                elif current_index == 1:
                    previous_time = self.timeData[-1]
                elif current_index == 2:
                    previous_time = self.timeData[-1]

                if current_index == 0:
                    self.timeData.append(previous_time + time_value)
                    self.hsS1RForce.append(force_value)
                    self.hsS1RForceLine.setData(self.timeData[:len(self.hsS1RForce)], self.hsS1RForce)
                elif current_index == 1:
                    self.timeData.append(previous_time + time_value)
                    self.hsS2RForce.append(force_value)
                    self.hsS2RAverage.append(force_average_value)
                    self.hsS2RForceLine.setData(self.timeData[:len(self.hsS2RForce)], self.hsS2RForce)
                    self.hsS2RAverageLine.setData(self.timeData[:len(self.hsS2RAverage)], self.hsS2RAverage)
                elif current_index == 2:
                    self.timeData.append(previous_time + time_value)
                    self.hsS3RForce.append(force_value)
                    self.hsS3RAverage.append(force_average_value)
                    self.hsS3RForceLine.setData(self.timeData[:len(self.hsS3RForce)], self.hsS3RForce)
                    self.hsS3RForceAverageLine.setData(self.timeData[:len(self.hsS3RAverage)], self.hsS3RAverage)

        except (ValueError, IndexError) as e:
            print(f"Error processing BLE data: {e}")
            pass

    @QtCore.pyqtSlot(bool)
    def on_toggled(self, checked):
        self.pushButton_4.setText("Stop" if checked else "Record")
        self.pushButton_3.setText("Stop" if checked else "Record")
        self.pushButton_2.setText("Stop" if checked else "Record")

        if checked:
            print("Connecting to BLE device...")
            asyncio.ensure_future(self.connect_ble())
        else:
            print("Disconnecting from BLE device...")
            asyncio.ensure_future(self.disconnect_ble())

            self.extensionForceLineEdit.setText(str(max(self.hsS1RForce)))
            self.strongLegAverageStrengthLineEdit_2.setText(str(max(self.hsS2RAverage)))
            self.strongLegPeakStrengthLineEdit_2.setText(str(max(self.hsS2RForce)))
            self.weakLegPeakStrengthLineEdit_3.setText(str(max(self.hsS3RForce)))

    async def connect_ble(self):
        """Connect to the BLE device"""
        try:
            print("Scanning for HooverTron device...")
            devices = await BleakScanner.discover(timeout=5.0)
            
            # Find the HooverTron device
            for device in devices:
                if device.name == "HooverTron":
                    self.ble_device = device
                    break
            
            if not self.ble_device:
                QMessageBox.critical(self, "Error", "HooverTron device not found. Please ensure the Arduino is powered on and in range.")
                self.pushButton_4.setChecked(False)
                self.pushButton_3.setChecked(False)
                self.pushButton_2.setChecked(False)
                return

            # Connect to the device
            self.ble_client = BleakClient(self.ble_device)
            await self.ble_client.connect()
            
            if self.ble_client.is_connected:
                print(f"Connected to {self.ble_device.name}")
                self.is_connected = True
                
                # Start notifications
                await self.ble_client.start_notify(CHARACTERISTIC_UUID, self.notification_handler)
                print("Notifications started")
            else:
                QMessageBox.critical(self, "Error", "Failed to connect to HooverTron")
                self.pushButton_4.setChecked(False)
                self.pushButton_3.setChecked(False)
                self.pushButton_2.setChecked(False)
                
        except Exception as e:
            print(f"BLE connection error: {e}")
            QMessageBox.critical(self, "Error", f"Failed to connect to BLE device: {str(e)}")
            self.pushButton_4.setChecked(False)
            self.pushButton_3.setChecked(False)
            self.pushButton_2.setChecked(False)

    async def disconnect_ble(self):
        """Disconnect from the BLE device"""
        try:
            if self.ble_client and self.ble_client.is_connected:
                # Stop notifications
                await self.ble_client.stop_notify(CHARACTERISTIC_UUID)
                await self.ble_client.disconnect()
                print("Disconnected from BLE device")
                self.is_connected = False
        except Exception as e:
            print(f"BLE disconnection error: {e}")

    @QtCore.pyqtSlot(bool)
    def clear_data(self, checked):
        current_index = self.tabWidget_2.currentIndex()

        if current_index== 0:
            self.timeData = [0]
            self.hsS1RForce = [0]
            self.hsS1RForceLine.setData(self.timeData, self.hsS1RForce)
            self.extensionForceLineEdit.setText(str(0.0))
            self.selection_region[self.tabWidget_2.currentIndex()].setRegion((0, 1))
            for button in self.select_button[current_index]:
                button.setStyleSheet("background-color: red; color: white; font-weight: bold; font-size: 16px;")

        elif current_index == 1:
            self.timeData = [0]
            self.hsS2RForce = [0]
            self.hsS2RAverage = [0]
            self.hsS2RForceLine.setData(self.timeData, self.hsS2RForce)
            self.hsS2RAverageLine.setData(self.timeData, self.hsS2RAverage)
            self.strongLegAverageStrengthLineEdit_2.setText(str(0.0))
            self.strongLegPeakStrengthLineEdit_2.setText(str(0.0))
            self.selection_region[self.tabWidget_2.currentIndex()].setRegion((0, 1))
            for button in self.select_button[current_index]:
                button.setStyleSheet("background-color: red; color: white; font-weight: bold; font-size: 16px;")

        elif current_index == 2:
            self.timeData = [0]
            self.hsS3RForce = [0]
            self.hsS3RAverage = [0]
            self.hsS3RForceLine.setData(self.timeData, self.hsS3RForce)
            self.hsS3RForceAverageLine.setData(self.timeData, self.hsS3RAverage)
            self.weakLegPeakStrengthLineEdit_3.setText(str(0.0))
            self.selection_region[self.tabWidget_2.currentIndex()].setRegion((0, 1))
            for button in self.select_button[current_index]:
                button.setStyleSheet("background-color: red; color: white; font-weight: bold; font-size: 16px;")
        else:
            print("Tab index finder not working")

    def fill_values(self):
        try:
            self.unaffectedLegExtensionLLineEdit.setText(self.extensionForceLineEdit.text())
            self.affectedLegVoluntaryExtensionLineEdit.setText(self.strongLegPeakStrengthLineEdit_2.text())
            self.affectedLegInvoluntaryExtensionLineEdit.setText(self.weakLegPeakStrengthLineEdit_3.text())
            print(max(self.hsS2RForce))
            print(max(self.hsS3RForce))
            ivvr = (float(max(self.hsS3RForce)) /
                    float(max(self.hsS2RForce)))
            ivvr = str(f'{ivvr:.2f}')
            self.involuntaryVoluntaryRatioAffectedLegLineEdit.setText(ivvr)

            self.label_21.setText("The ratio between the affected leg\'s voluntary and involuntary flexion was "
                           + ivvr
                           + ". An IVVR of 2.48 with a standard error of 0.61 was determined to be a high confidence "
                           + "measurement for a positive Hoover's Sign.")

        except Exception:
            print("Error: all measured values must be filled in to see results")

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

    def load_config(self):
        config = configparser.ConfigParser()
        if os.path.exists(CONFIG_FILE_PATH):
            config.read(CONFIG_FILE_PATH)
            self.dataBaseFile = config.get('Settings', 'last_file', fallback='')
            if self.dataBaseFile:
                self.load_last_test_number()

    def save_config(self):
        config = configparser.ConfigParser()
        config['Settings'] = {'last_file': self.dataBaseFile}
        with open(CONFIG_FILE_PATH, 'w') as configfile:
            config.write(configfile)

    def load_last_test_number(self):
        if os.path.exists(self.dataBaseFile):
            with open(self.dataBaseFile, 'r', encoding='UTF8') as f:
                reader = csv.reader(f)
                next(reader) 
                rows = list(reader)
                if rows:
                    last_row = rows[-1]
                    try:
                        self.testNumber = int(last_row[0])
                    except ValueError:
                        self.testNumber = 1
                else:
                    self.testNumber = 1
                    self.isNewDatabase = False
        else:
            self.testNumber = 1
            self.isNewDatabase = True

    def show_message(self, title, message, icon=QMessageBox.Information):
        msg = QMessageBox()
        msg.setIcon(icon)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec_()

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

    def valgAfComport(self, nyport):
        """Legacy COM port selection - now used for BLE device selection"""
        print(f"BLE device selection: {nyport}")
        # This function is kept for compatibility but doesn't do anything with BLE

    async def set_filter_frequency_async(self, frequency):
        """Send filter frequency update via BLE"""
        if self.ble_client and self.ble_client.is_connected:
            try:
                command = f"F{frequency}\n"
                await self.ble_client.write_gatt_char(CHARACTERISTIC_UUID, command.encode())
                self.currentFrequency = frequency
                self.statusbar.showMessage(f"Filter frequency set to {frequency} Hz", 3000)
                print(f"Filter frequency changed to {frequency} Hz")
            except Exception as e:
                print(f"Error setting frequency: {e}")
        else:
            QMessageBox.warning(self, "Connection Error", 
                            "Please connect to BLE device before changing filter frequency")

    def set_filter_frequency(self, frequency):
        """Wrapper for async frequency setting"""
        asyncio.ensure_future(self.set_filter_frequency_async(frequency))
        
    def closeEvent(self, event):
        # Disconnect BLE before closing
        if self.ble_client and self.ble_client.is_connected:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.disconnect_ble())
        print("All connections closed")