from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QComboBox, QLineEdit, QLabel, QDateEdit

from ui_components import theme


_FUSION_STYLE = None


def _fusion_style():
    """Return a single shared Fusion style instance.

    Calling QStyleFactory.create on every popup, or applying it per-child,
    can cause access violations on PyQt5/Windows when the popup is later
    repolished. One persistent style instance avoids that.
    """
    global _FUSION_STYLE
    if _FUSION_STYLE is None:
        _FUSION_STYLE = QtWidgets.QStyleFactory.create("Fusion")
    return _FUSION_STYLE


def _modernize_calendar(date_edit):
    """Apply themed styling to the calendar popup of a QDateEdit."""
    cal = date_edit.calendarWidget()
    if cal is None:
        return
    fusion = _fusion_style()
    if fusion is not None:
        cal.setStyle(fusion)
    cal.setStyleSheet(theme.calendar_stylesheet())
    cal.setHorizontalHeaderFormat(QtWidgets.QCalendarWidget.ShortDayNames)
    cal.setVerticalHeaderFormat(QtWidgets.QCalendarWidget.NoVerticalHeader)
    cal.setGridVisible(False)
    cal.setFirstDayOfWeek(QtCore.Qt.Monday)
    # Normalise weekday colours so weekends aren't red
    p = theme.palette()
    fmt = QtGui.QTextCharFormat()
    fmt.setForeground(QtGui.QColor(p["text"]))
    for day in (
        QtCore.Qt.Monday, QtCore.Qt.Tuesday, QtCore.Qt.Wednesday,
        QtCore.Qt.Thursday, QtCore.Qt.Friday, QtCore.Qt.Saturday, QtCore.Qt.Sunday,
    ):
        cal.setWeekdayTextFormat(day, fmt)


class PatientTab:
    def setup_ui(self, main_ui, parent_widget):
        outer = QtWidgets.QVBoxLayout(parent_widget)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        formCardLayout = QtWidgets.QVBoxLayout()
        formCardLayout.setContentsMargins(36, 28, 36, 28)
        formCardLayout.setSpacing(10)
        outer.addLayout(formCardLayout, 1)

        # Title block
        title = QtWidgets.QLabel("Patient Information")
        title.setProperty("role", "title")
        formCardLayout.addWidget(title)

        subtitle = QtWidgets.QLabel(
            "Capture demographics and choose the affected leg before recording."
        )
        subtitle.setProperty("role", "subtitle")
        subtitle.setWordWrap(True)
        formCardLayout.addWidget(subtitle)
        formCardLayout.addSpacing(6)

        # ---- Single unified form so columns align across sections ----
        unifiedForm = self._new_form()
        formCardLayout.addLayout(unifiedForm)

        def add_section(text, top_spacing=12):
            spacer = QtWidgets.QLabel()
            spacer.setFixedHeight(top_spacing)
            unifiedForm.addRow(spacer)
            header = self._section_header(text)
            unifiedForm.addRow(header)

        def add_row(label, field):
            field.setSizePolicy(
                QtWidgets.QSizePolicy.Expanding, field.sizePolicy().verticalPolicy()
            )
            unifiedForm.addRow(label, field)

        # Identity
        unifiedForm.addRow(self._section_header("Identity"))

        main_ui.nameLabel = QLabel("Full name")
        main_ui.nameLineEdit = QLineEdit()
        main_ui.nameLineEdit.setPlaceholderText("e.g. Jane Smith")
        add_row(main_ui.nameLabel, main_ui.nameLineEdit)

        main_ui.preferredNameLabel = QLabel("Preferred name")
        main_ui.preferredNameLineEdit = QLineEdit()
        main_ui.preferredNameLineEdit.setPlaceholderText("Optional")
        add_row(main_ui.preferredNameLabel, main_ui.preferredNameLineEdit)

        main_ui.sexLabel = QLabel("Sex")
        main_ui.sexComboBox = QComboBox()
        main_ui.sexComboBox.addItems(["----", "Male", "Female", "Other", "Prefer not to say"])
        add_row(main_ui.sexLabel, main_ui.sexComboBox)

        # Visit
        add_section("Visit")

        main_ui.dateOfBirthLabel = QLabel("Date of birth")
        main_ui.dateOfBirthDateEdit = QDateEdit()
        main_ui.dateOfBirthDateEdit.setCalendarPopup(True)
        main_ui.dateOfBirthDateEdit.setDate(QtCore.QDate.currentDate().addYears(-40))
        main_ui.dateOfBirthDateEdit.setDisplayFormat("d MMM yyyy")
        _modernize_calendar(main_ui.dateOfBirthDateEdit)
        add_row(main_ui.dateOfBirthLabel, main_ui.dateOfBirthDateEdit)

        main_ui.dateOfVisitLabel_2 = QLabel("Date of visit")
        main_ui.dateOfVisitDateEdit = QDateEdit()
        main_ui.dateOfVisitDateEdit.setCalendarPopup(True)
        main_ui.dateOfVisitDateEdit.setDate(QtCore.QDate.currentDate())
        main_ui.dateOfVisitDateEdit.setDisplayFormat("d MMM yyyy")
        _modernize_calendar(main_ui.dateOfVisitDateEdit)
        add_row(main_ui.dateOfVisitLabel_2, main_ui.dateOfVisitDateEdit)

        main_ui.ageLabel = QLabel("Age")
        main_ui.ageLineEdit = QLineEdit()
        main_ui.ageLineEdit.setReadOnly(True)
        main_ui.ageLineEdit.setPlaceholderText("Computed from DOB")
        add_row(main_ui.ageLabel, main_ui.ageLineEdit)

        main_ui.reasonForVisitLabel = QLabel("Reason for visit")
        main_ui.reasonForVisitLineEdit = QLineEdit()
        add_row(main_ui.reasonForVisitLabel, main_ui.reasonForVisitLineEdit)

        main_ui.examinerLabel = QLabel("Examiner")
        main_ui.examinerLineEdit = QLineEdit()
        main_ui.examinerLineEdit.setPlaceholderText("Clinician name")
        add_row(main_ui.examinerLabel, main_ui.examinerLineEdit)

        main_ui.notesLabel = QLabel("Notes")
        main_ui.notesLineEdit = QLineEdit()
        main_ui.notesLineEdit.setPlaceholderText("Optional observations for this visit")
        add_row(main_ui.notesLabel, main_ui.notesLineEdit)

        # Examination
        add_section("Examination")

        main_ui.dominantLegLabel = QLabel("Dominant leg")
        main_ui.dominantLegComboBox = QComboBox()
        main_ui.dominantLegComboBox.addItems(["----", "Right Leg", "Left Leg"])
        add_row(main_ui.dominantLegLabel, main_ui.dominantLegComboBox)

        main_ui.SelectLegLabel = QLabel("Affected leg")
        main_ui.selectedLegComboBox = QComboBox()
        main_ui.selectedLegComboBox.addItems(["----", "Right Leg", "Left Leg"])
        add_row(main_ui.SelectLegLabel, main_ui.selectedLegComboBox)

        formCardLayout.addStretch(1)

        # ---- Behaviour: auto-compute age from DOB --------------------
        def update_age():
            dob = main_ui.dateOfBirthDateEdit.date()
            visit = main_ui.dateOfVisitDateEdit.date()
            if dob.isValid() and visit.isValid():
                age = visit.year() - dob.year() - (
                    (visit.month(), visit.day()) < (dob.month(), dob.day())
                )
                if age < 0 or age > 130:
                    main_ui.ageLineEdit.clear()
                else:
                    main_ui.ageLineEdit.setText(str(age))
            else:
                main_ui.ageLineEdit.clear()

        main_ui.dateOfBirthDateEdit.dateChanged.connect(update_age)
        main_ui.dateOfVisitDateEdit.dateChanged.connect(update_age)
        update_age()

    # ------------------------------------------------------------------
    def _new_form(self):
        form = QtWidgets.QFormLayout()
        form.setContentsMargins(0, 0, 0, 0)
        form.setHorizontalSpacing(18)
        form.setVerticalSpacing(10)
        form.setLabelAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        form.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        form.setRowWrapPolicy(QtWidgets.QFormLayout.DontWrapRows)
        form.setFormAlignment(QtCore.Qt.AlignTop)
        return form

    def _section_header(self, text):
        label = QtWidgets.QLabel(text)
        label.setProperty("role", "eyebrow")
        return label

    def retranslate_ui(self, main_ui):
        _translate = QtCore.QCoreApplication.translate
        main_ui.nameLabel.setText(_translate("MainWindow", "Full name"))
        main_ui.preferredNameLabel.setText(_translate("MainWindow", "Preferred name"))
        main_ui.dateOfBirthLabel.setText(_translate("MainWindow", "Date of birth"))
        main_ui.ageLabel.setText(_translate("MainWindow", "Age"))
        main_ui.sexLabel.setText(_translate("MainWindow", "Sex"))
        main_ui.dateOfVisitLabel_2.setText(_translate("MainWindow", "Date of visit"))
        main_ui.reasonForVisitLabel.setText(_translate("MainWindow", "Reason for visit"))
        main_ui.notesLabel.setText(_translate("MainWindow", "Notes"))
        main_ui.examinerLabel.setText(_translate("MainWindow", "Examiner"))
        main_ui.dominantLegLabel.setText(_translate("MainWindow", "Dominant leg"))
        main_ui.SelectLegLabel.setText(_translate("MainWindow", "Affected leg"))
