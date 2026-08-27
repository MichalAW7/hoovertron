from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QComboBox, QLineEdit, QLabel, QDateEdit

class PatientTab:
    def setup_ui(self, main_ui, parent_widget):
        """
        main_ui: The instance of the Ui_Layout class (to attach attributes to)
        parent_widget: The widget to add this layout to (self.tab_3)
        """
        self.horizontalLayoutWidget_7 = QtWidgets.QWidget(parent_widget)
        self.horizontalLayoutWidget_7.setGeometry(QtCore.QRect(-1, -1, 1201, 831))
        self.horizontalLayoutWidget_7.setObjectName("horizontalLayoutWidget_7")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_7)
        self.horizontalLayout_12.setContentsMargins(20, 20, 20, 20)
        self.horizontalLayout_12.setSpacing(20)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.formLayout_7 = QtWidgets.QFormLayout()
        self.formLayout_7.setContentsMargins(0, -1, -1, -1)
        self.formLayout_7.setVerticalSpacing(20)
        self.formLayout_7.setObjectName("formLayout_7")

        # Create Widgets and attach to main_ui
        main_ui.nameLabel = QtWidgets.QLabel(self.horizontalLayoutWidget_7)
        main_ui.nameLabel.setObjectName("nameLabel")
        self.formLayout_7.setWidget(0, QtWidgets.QFormLayout.LabelRole, main_ui.nameLabel)
        
        main_ui.nameLineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget_7)
        main_ui.nameLineEdit.setObjectName("nameLineEdit")
        self.formLayout_7.setWidget(0, QtWidgets.QFormLayout.FieldRole, main_ui.nameLineEdit)
        
        main_ui.preferredNameLabel = QtWidgets.QLabel(self.horizontalLayoutWidget_7)
        main_ui.preferredNameLabel.setObjectName("preferredNameLabel")
        self.formLayout_7.setWidget(1, QtWidgets.QFormLayout.LabelRole, main_ui.preferredNameLabel)
        
        main_ui.preferredNameLineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget_7)
        main_ui.preferredNameLineEdit.setObjectName("preferredNameLineEdit")
        self.formLayout_7.setWidget(1, QtWidgets.QFormLayout.FieldRole, main_ui.preferredNameLineEdit)
        
        main_ui.dateOfBirthLabel = QtWidgets.QLabel(self.horizontalLayoutWidget_7)
        main_ui.dateOfBirthLabel.setObjectName("dateOfBirthLabel")
        self.formLayout_7.setWidget(2, QtWidgets.QFormLayout.LabelRole, main_ui.dateOfBirthLabel)
        
        main_ui.dateOfBirthDateEdit = QtWidgets.QDateEdit(self.horizontalLayoutWidget_7)
        main_ui.dateOfBirthDateEdit.setObjectName("dateOfBirthDateEdit")
        main_ui.dateOfBirthDateEdit.setCalendarPopup(True)
        self.formLayout_7.setWidget(2, QtWidgets.QFormLayout.FieldRole, main_ui.dateOfBirthDateEdit)

        main_ui.dateOfVisitLabel_2 = QtWidgets.QLabel(self.horizontalLayoutWidget_7)
        main_ui.dateOfVisitLabel_2.setObjectName("dateOfVisitLabel_2")
        self.formLayout_7.setWidget(3, QtWidgets.QFormLayout.LabelRole, main_ui.dateOfVisitLabel_2)
        
        main_ui.dateOfVisitDateEdit = QtWidgets.QDateEdit(self.horizontalLayoutWidget_7)
        main_ui.dateOfVisitDateEdit.setObjectName("dateOfVisitDateEdit")
        main_ui.dateOfVisitDateEdit.setCalendarPopup(True)
        main_ui.dateOfVisitDateEdit.setDate(QtCore.QDate.currentDate())
        self.formLayout_7.setWidget(3, QtWidgets.QFormLayout.FieldRole, main_ui.dateOfVisitDateEdit)

        main_ui.ageLabel = QtWidgets.QLabel(self.horizontalLayoutWidget_7)
        main_ui.ageLabel.setObjectName("ageLabel")
        self.formLayout_7.setWidget(4, QtWidgets.QFormLayout.LabelRole, main_ui.ageLabel)
        
        main_ui.ageLineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget_7)
        main_ui.ageLineEdit.setObjectName("ageLineEdit")
        self.formLayout_7.setWidget(4, QtWidgets.QFormLayout.FieldRole, main_ui.ageLineEdit)

        main_ui.sexLabel = QtWidgets.QLabel(self.horizontalLayoutWidget_7)
        main_ui.sexLabel.setObjectName("sexLabel")
        self.formLayout_7.setWidget(5, QtWidgets.QFormLayout.LabelRole, main_ui.sexLabel)
        
        main_ui.sexComboBox = QtWidgets.QComboBox(self.horizontalLayoutWidget_7)
        main_ui.sexComboBox.setObjectName("sexComboBox")
        main_ui.sexComboBox.addItem("----")
        main_ui.sexComboBox.addItem("Male")
        main_ui.sexComboBox.addItem("Female")
        main_ui.sexComboBox.addItem("Other")
        main_ui.sexComboBox.addItem("Prefer not to say")
        self.formLayout_7.setWidget(5, QtWidgets.QFormLayout.FieldRole, main_ui.sexComboBox)

        main_ui.reasonForVisitLabel = QtWidgets.QLabel(self.horizontalLayoutWidget_7)
        main_ui.reasonForVisitLabel.setObjectName("reasonForVisitLabel")
        self.formLayout_7.setWidget(6, QtWidgets.QFormLayout.LabelRole, main_ui.reasonForVisitLabel)
        
        main_ui.reasonForVisitLineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget_7)
        main_ui.reasonForVisitLineEdit.setObjectName("reasonForVisitLineEdit")
        self.formLayout_7.setWidget(6, QtWidgets.QFormLayout.FieldRole, main_ui.reasonForVisitLineEdit)
        
        main_ui.notesLabel = QtWidgets.QLabel(self.horizontalLayoutWidget_7)
        main_ui.notesLabel.setObjectName("notesLabel")
        self.formLayout_7.setWidget(7, QtWidgets.QFormLayout.LabelRole, main_ui.notesLabel)
        
        main_ui.notesLineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget_7)
        main_ui.notesLineEdit.setObjectName("notesLineEdit")
        self.formLayout_7.setWidget(7, QtWidgets.QFormLayout.FieldRole, main_ui.notesLineEdit)
        
        main_ui.examinerLabel = QtWidgets.QLabel(self.horizontalLayoutWidget_7)
        main_ui.examinerLabel.setObjectName("examinerLabel")
        self.formLayout_7.setWidget(8, QtWidgets.QFormLayout.LabelRole, main_ui.examinerLabel)
        
        main_ui.examinerLineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget_7)
        main_ui.examinerLineEdit.setObjectName("examinerLineEdit")
        self.formLayout_7.setWidget(8, QtWidgets.QFormLayout.FieldRole, main_ui.examinerLineEdit)
        
        main_ui.dominantLegLabel = QtWidgets.QLabel(self.horizontalLayoutWidget_7)
        main_ui.dominantLegLabel.setObjectName("dominantLegLabel")
        self.formLayout_7.setWidget(9, QtWidgets.QFormLayout.LabelRole, main_ui.dominantLegLabel)
        
        main_ui.dominantLegComboBox = QComboBox(self.horizontalLayoutWidget_7)
        main_ui.dominantLegComboBox.setObjectName("dominantLegComboBox")
        main_ui.dominantLegComboBox.addItem("----")
        main_ui.dominantLegComboBox.addItem("Right Leg")
        main_ui.dominantLegComboBox.addItem("Left Leg")
        self.formLayout_7.setWidget(9, QtWidgets.QFormLayout.FieldRole, main_ui.dominantLegComboBox)

        main_ui.SelectLegLabel = QtWidgets.QLabel(self.horizontalLayoutWidget_7)
        main_ui.SelectLegLabel.setObjectName("SelectLegLabel")
        self.formLayout_7.setWidget(10, QtWidgets.QFormLayout.LabelRole, main_ui.SelectLegLabel)
        
        main_ui.selectedLegComboBox = QComboBox(self.horizontalLayoutWidget_7)
        main_ui.selectedLegComboBox.setObjectName("selectedLegComboBox")
        main_ui.selectedLegComboBox.addItem("----")
        main_ui.selectedLegComboBox.addItem("Right Leg")
        main_ui.selectedLegComboBox.addItem("Left Leg")
        self.formLayout_7.setWidget(10, QtWidgets.QFormLayout.FieldRole, main_ui.selectedLegComboBox)

        self.horizontalLayout_12.addLayout(self.formLayout_7)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem)
        self.horizontalLayout_12.setStretch(0, 2)
        self.horizontalLayout_12.setStretch(1, 3)

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