# -*- coding: utf-8 -*-
# aufzeichnungen/views.py

""" This module provides view to manage aufzeichnungen table """

from datetime import date
from xml.dom import ValidationErr
from .model import Record

from PyQt5.QtCore import QDate
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *



class Window(QMainWindow):
    """Main Window"""
    def __init__(self, parent: QWidget | None = None) -> None:
        """ Initializer """
        super().__init__(parent)

        """ Data initialize """
        self.records = Record()

        """ UI setup"""
        self.setupUI() 
        
    def setupUI(self):
        """set base styles"""
        self.setWindowTitle("Taschenrechner")
        self.setFont(QFont("Myanmar Text"))
        self.setGeometry(0, 0, 600, 500)

        self._setRecordsTable()

        """buttons"""

        """create button"""
        self.createButton = QPushButton("အသစ်လုပ်မည်")
        self.createButton.clicked.connect(self.openAddRecordDialog)
        """update button"""
        self.updateButton = QPushButton("စာရင်းထည့်မည်")
        """calculate button"""
        self.calcuateButton = QPushButton("တွက်မည်")
        """delete button"""
        self.deleteButton = QPushButton("ဖျက်မည်") 

        """Lay out the GUI"""
        buttonLayout = QVBoxLayout()
        buttonLayout.addWidget(self.createButton)
        buttonLayout.addWidget(self.updateButton)
        buttonLayout.addWidget(self.calcuateButton)
        buttonLayout.addStretch()
        buttonLayout.addWidget(self.deleteButton)

        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.recordTable)
        mainLayout.addLayout(buttonLayout)

        widget = QWidget()
        widget.setLayout(mainLayout)
        self.setCentralWidget(widget)
    
    def openAddRecordDialog(self):
        """open dialog for adding records"""
        dialog = AddRecordDialog(self)
        if dialog.exec() == QDialog.Accepted:
            try:
                self.records.addRecord(dialog.data)
            except ValidationErr as e:
                QMessageBox.critical(
                    self, "Error", f"{e}"
                )
            self.recordTable.resizeColumnsToContents()

    def _setRecordsTable(self):
        self.recordTable = QTableView()
        self.recordTable.setModel(self.records.model)
        self.recordTable.hideColumn(0)
        self.recordTable.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.recordTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.recordTable.resizeColumnsToContents()

class AddRecordDialog(QDialog):
    """ Dialog for adding records """
    def __init__(self, parent: QWidget | None) -> None:

        super().__init__(parent=parent)

        self.setWindowTitle("စာအုပ်အသစ်လုပ်ရန်")
        """base layout"""
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        """input data"""
        self.data = None
        """setup form"""
        self._setUpForm()
        """creating a dialog button for ok and cancel"""
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        """adding action when form is accepted"""
        self.buttonBox.accepted.connect(self.accept)
        """adding action when form is rejected"""
        self.buttonBox.rejected.connect(self.reject)
        """append form and btns to main layout"""
        self.layout.addWidget(self.recordFormGroup)
        self.layout.addWidget(self.buttonBox)

    def _setUpForm(self):
        """formGroup"""
        self.recordFormGroup = QGroupBox("လိုအပ်သော အချက်အလက်များ")

        """date"""
        self.dateField = QDateEdit()
        self.dateField.setDate(QDate(date.today()))
        self.dateField.setObjectName("ရက်စွဲ")

        """value_limit"""
        self.limitField = QSpinBox()
        self.limitField.setMaximum(100000)
        self.limitField.setObjectName("ကာမည့် ပမာဏ")

        """record_type"""
        self.digitsComboBox = QComboBox()
        self.digitsComboBox.addItems([" ","2D", "3D"])
        self.digitsComboBox.setObjectName("အမျိုးအစား")

        """limit specifications"""
        self.curfewComboBox = QComboBox()
        self.curfewComboBox.addItems([])
        self.curfewComboBox.setObjectName("စာရင်းပိတ်ချိန်")
        """limit depends on record_type"""
        self.digitsComboBox.currentTextChanged.connect(self.updateLimitBox)

        """creating table layout"""
        createTableLayout = QFormLayout()
        createTableLayout.addRow(QLabel("ရက်စွဲ"), self.dateField)
        createTableLayout.addRow(QLabel("အမျိုးအစား"), self.digitsComboBox)
        createTableLayout.addRow(QLabel("စာရင်းပိတ်ချိန်"), self.curfewComboBox)
        createTableLayout.addRow(QLabel("ကာမည့် ပမာဏ"), self.limitField)

        """registering table layout group"""
        self.recordFormGroup.setLayout(createTableLayout)
        
    def updateLimitBox(self):
        """Reset"""
        self.curfewComboBox.clear()
        if self.digitsComboBox.currentText() == "2D":
            self.curfewComboBox.addItems(["မနက်ပိုင်း", "ညနေပိုင်း"])
        elif self.digitsComboBox.currentText() == "3D":
            self.curfewComboBox.addItems(["လဝက်", "လကုန်"])
        else:
             self.curfewComboBox.clear()

    def accept(self):
        """Accept the data provided through the dialog."""
        self.data = []
    
        if not self.dateField.date():
            QMessageBox.critical(
                    self,
                    "Error",
                    f"{self.dateField.objectName()} ကိုဖြည့်ပေးပါ"
                )
            self.data = None
            return
        self.data.append(self.dateField.date().toPyDate())
        
        for comboBox in (self.digitsComboBox, self.curfewComboBox):
            if not comboBox.currentText():
                QMessageBox.critical(
                    self,
                    "Error",
                    f"{comboBox.objectName()} ကိုဖြည့်ပေးပါ"
                )
                self.data = None
                return
            self.data.append(comboBox.currentIndex())

        if not self.limitField.text():
            QMessageBox.critical(
                    self,
                    "Error",
                    f"{self.limitField.objectName()} ကိုဖြည့်ပေးပါ"
                )
            self.data = None
            return
        self.data.append(self.limitField.text())

        super().accept()
    