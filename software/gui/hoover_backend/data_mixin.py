# hoover_backend/data_mixin.py
from PyQt5 import QtCore

class DataMixin:
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
        average_data = None
        
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

            average_value = max(average_data_filtered, default=None)
            average_widget.setText(str(average_value) if average_value is not None else 'N/A')

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

    def process_incoming_data(self, text_line):
        """Process a line of comma-separated data from the device"""
        try:
            words = text_line.split(",")
            if len(words) < 2:
                return

            current_index = self.tabWidget_2.currentIndex()

            # Parse values
            time_value = float(words[0])/300000
            force_value = float(words[1])
            force_average_value = float(words[3]) if len(words) > 3 else None

            # Get previous time
            previous_time = self.timeData[-1] if self.timeData else 0

            # Update arrays based on active tab
            if current_index == 0:
                self.timeData.append(previous_time + time_value)
                self.hsS1RForce.append(force_value)
                self.hsS1RForceLine.setData(self.timeData[:len(self.hsS1RForce)], self.hsS1RForce)
            elif current_index == 1:
                self.timeData.append(previous_time + time_value)
                self.hsS2RForce.append(force_value)
                if force_average_value is not None:
                    self.hsS2RAverage.append(force_average_value)
                self.hsS2RForceLine.setData(self.timeData[:len(self.hsS2RForce)], self.hsS2RForce)
                if force_average_value is not None:
                    self.hsS2RAverageLine.setData(self.timeData[:len(self.hsS2RAverage)], self.hsS2RAverage)
            elif current_index == 2:
                self.timeData.append(previous_time + time_value)
                self.hsS3RForce.append(force_value)
                if force_average_value is not None:
                    self.hsS3RAverage.append(force_average_value)
                self.hsS3RForceLine.setData(self.timeData[:len(self.hsS3RForce)], self.hsS3RForce)
                if force_average_value is not None:
                    self.hsS3RForceAverageLine.setData(self.timeData[:len(self.hsS3RAverage)], self.hsS3RAverage)

        except (ValueError, IndexError) as e:
            print(f"Error processing data: {e}")
            pass