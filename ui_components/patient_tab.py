from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QComboBox, QLineEdit, QLabel, QDateEdit

class PatientTab:
    def setup_ui(self, main_ui, parent_widget):
        """
        main_ui: The instance of the Ui_Layout class (to attach attributes to)
        parent_widget: The widget to add this layout to (self.tab_3)
        """
        # Create a main layout for the tab
        self.mainLayout = QtWidgets.QVBoxLayout(parent_widget)
        self.mainLayout.setContentsMargins(20, 20, 20, 20)
        self.mainLayout.setSpacing(20)

        # Create a GroupBox for Patient Details
        self.detailsGroupBox = QtWidgets.QGroupBox("Patient Details", parent_widget)
        self.detailsLayout = QtWidgets.QFormLayout(self.detailsGroupBox)
        self.detailsLayout.setContentsMargins(20, 20, 20, 20)
        self.detailsLayout.setVerticalSpacing(15)
        self.detailsLayout.setLabelAlignment(QtCore.Qt.AlignRight)

        # Create Widgets and attach to main_ui
        main_ui.nameLabel = QtWidgets.QLabel("Name:")
        main_ui.nameLineEdit = QtWidgets.QLineEdit()
        self.detailsLayout.addRow(main_ui.nameLabel, main_ui.nameLineEdit)
        
        main_ui.preferredNameLabel = QtWidgets.QLabel("Preferred name:")
        main_ui.preferredNameLineEdit = QtWidgets.QLineEdit()
        self.detailsLayout.addRow(main_ui.preferredNameLabel, main_ui.preferredNameLineEdit)
        
        main_ui.dateOfBirthLabel = QtWidgets.QLabel("Date of birth:")
        main_ui.dateOfBirthDateEdit = QtWidgets.QDateEdit()
        main_ui.dateOfBirthDateEdit.setCalendarPopup(True)
        self.detailsLayout.addRow(main_ui.dateOfBirthLabel, main_ui.dateOfBirthDateEdit)

        main_ui.dateOfVisitLabel_2 = QtWidgets.QLabel("Date of visit:")
        main_ui.dateOfVisitDateEdit = QtWidgets.QDateEdit()
        main_ui.dateOfVisitDateEdit.setCalendarPopup(True)
        main_ui.dateOfVisitDateEdit.setDate(QtCore.QDate.currentDate())
        self.detailsLayout.addRow(main_ui.dateOfVisitLabel_2, main_ui.dateOfVisitDateEdit)

        main_ui.ageLabel = QtWidgets.QLabel("Age:")
        main_ui.ageLineEdit = QtWidgets.QLineEdit()
        main_ui.ageLineEdit.setReadOnly(True)
        self.detailsLayout.addRow(main_ui.ageLabel, main_ui.ageLineEdit)

        main_ui.sexLabel = QtWidgets.QLabel("Sex:")
        main_ui.sexComboBox = QtWidgets.QComboBox()
        main_ui.sexComboBox.addItems(["----", "Male", "Female", "Other", "Prefer not to say"])
        self.detailsLayout.addRow(main_ui.sexLabel, main_ui.sexComboBox)

        main_ui.reasonForVisitLabel = QtWidgets.QLabel("Reason for visit:")
        main_ui.reasonForVisitLineEdit = QtWidgets.QLineEdit()
        self.detailsLayout.addRow(main_ui.reasonForVisitLabel, main_ui.reasonForVisitLineEdit)
        
        main_ui.notesLabel = QtWidgets.QLabel("Notes:")
        main_ui.notesLineEdit = QtWidgets.QLineEdit()
        self.detailsLayout.addRow(main_ui.notesLabel, main_ui.notesLineEdit)
        
        main_ui.examinerLabel = QtWidgets.QLabel("Examiner name:")
        main_ui.examinerLineEdit = QtWidgets.QLineEdit()
        self.detailsLayout.addRow(main_ui.examinerLabel, main_ui.examinerLineEdit)
        
        main_ui.dominantLegLabel = QtWidgets.QLabel("Dominant leg:")
        main_ui.dominantLegComboBox = QComboBox()
        main_ui.dominantLegComboBox.addItems(["----", "Right Leg", "Left Leg"])
        self.detailsLayout.addRow(main_ui.dominantLegLabel, main_ui.dominantLegComboBox)

        main_ui.SelectLegLabel = QtWidgets.QLabel("Selected leg:")
        main_ui.selectedLegComboBox = QComboBox()
        main_ui.selectedLegComboBox.addItems(["----", "Right Leg", "Left Leg"])
        self.detailsLayout.addRow(main_ui.SelectLegLabel, main_ui.selectedLegComboBox)

        # Add GroupBox to main layout
        self.mainLayout.addWidget(self.detailsGroupBox)
        
        # Add spacer to push content up
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.mainLayout.addItem(spacerItem)

        # Logic for age calculation
        def update_age():
            main_ui.ageLineEdit.clear()
            dob = main_ui.dateOfBirthDateEdit.date()
            if dob.isValid():
                visit = main_ui.dateOfVisitDateEdit.date()
                age = calculate_age(dob, visit)
                main_ui.ageLineEdit.setText(str(age))
            else:
                main_ui.ageLineEdit.clear()

        def calculate_age(date_of_birth, date_of_visit):
            dob = date_of_birth.toPyDate()
            visit = date_of_visit.toPyDate()
            age = visit.year - dob.year - ((visit.month, visit.day) < (dob.month, dob.day))
            return age

        main_ui.dateOfBirthDateEdit.dateChanged.connect(update_age)
        main_ui.dateOfVisitDateEdit.dateChanged.connect(update_age)
        main_ui.dateOfBirthDateEdit.editingFinished.connect(update_age)
        main_ui.ageLineEdit.clear()

    def retranslate_ui(self, main_ui):
        _translate = QtCore.QCoreApplication.translate
        main_ui.nameLabel.setText(_translate("MainWindow", "Name:"))
        main_ui.preferredNameLabel.setText(_translate("MainWindow", "Preferred name:"))
        main_ui.dateOfBirthLabel.setText(_translate("MainWindow", "Date of birth:"))
        main_ui.ageLabel.setText(_translate("MainWindow", "Age:"))
        main_ui.sexLabel.setText(_translate("MainWindow", "Sex:"))
        main_ui.dateOfVisitLabel_2.setText(_translate("MainWindow", "Date of visit:"))
        main_ui.reasonForVisitLabel.setText(_translate("MainWindow", "Reason for visit:"))
        main_ui.notesLabel.setText(_translate("MainWindow", "Notes:"))
        main_ui.examinerLabel.setText(_translate("MainWindow", "Examiner name:"))
        main_ui.dominantLegLabel.setText(_translate("MainWindow", "Dominant leg:"))
        main_ui.SelectLegLabel.setText(_translate("MainWindow", "Selected leg:"))