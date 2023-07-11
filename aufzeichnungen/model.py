# -*- coding: utf-8 -*-
# aufzeichnungen/database.py

""" this module provides models related to records """
from xml.dom import ValidationErr
from .datasets import ( DIGIT_TYPES, CURFEWS, CURFEWS_LABEL )
from datetime import datetime 

from PyQt5.QtCore import Qt
from PyQt5.QtSql import *

class Record():
    def __init__(self):
        self.model = self._getModels()

    @staticmethod
    def _getModels():
        """ query records """
        model = QSqlTableModel()
        model.setTable("records")
        model.setEditStrategy(QSqlTableModel.OnFieldChange)
        model.select()
        headers = (" ", "ရက်စွဲ", "အမျိုးအစား    ", "ပိတ်ချိန်        ", "တန်ဖိုး     ", "ပြုလုပ်ချိန်     ")
        for colIndex, header in enumerate(headers):
            model.setHeaderData(colIndex, Qt.Orientation.Horizontal, header)
        return model
    
    # def _insertRecords(self, data):

        # insertRecordQuery = QSqlQuery()
        # insertRecordQuery.prepare(
        #     """
        #         INSERT INTO records (
        #             date, digits, curfew, cover, created_at
        #         )
        #         VALUES (?, ?, ?, ?, ?);
        #     """
        # )

        # for val in data:
        #     insertRecordQuery.addBindValue(val)
        
        # insertRecordQuery.addBindValue(datetime.today().isoformat())
        # insertRecordQuery.exec_()
        # self.model.select()
    
    def addRecord(self, data):
        date, digit, curfew, limit  = data[0].isoformat(), DIGIT_TYPES[data[1]], CURFEWS_LABEL[DIGIT_TYPES[data[1]]][CURFEWS[data[2]]], data[3]

        data = [date, digit, curfew, limit, datetime.today().strftime("%Y-%m-%d")]

        self._validateRecordBeforeInsert(tuple(data))
        # self._insertRecords(data)   

        """Add a record to the database."""
        rows = self.model.rowCount()
        self.model.insertRows(rows, 1)
        for column, field in enumerate(data):
            self.model.setData(self.model.index(rows, column + 1), field)
        self.model.submitAll()
        self.model.select()

    def _validateRecordBeforeInsert(self, data : tuple):
        for i in range(self.model.rowCount()):
            if self.model.record(i).value("date") == data[0] and self.model.record(i).value("digits") == data[1] and self.model.record(i).value("curfew") == data[2]:
                raise ValidationErr(f"{data[0]} နေ့အတွက် {data[1]}D စာရင်းဖွင့်ပြီးသားဖြစ်ပါသည်")
            
        print(data[1])
        match data[1]:
            case 2:
                if data[0] == datetime.now().strftime("%Y-%m-%d") and datetime.now().strftime("%H%M%S") > "120000" and data[2] == "နေ့လည်":
                    raise ValidationErr(f"{data[0]} နေ့အတွက် {data[1]}D စာရင်းပိတ်သွားပါပြီ")
            case 3:
                if data[0][-2:] > "16" and datetime.now().strftime("%H%M%S") > "160000" and data[2] == "၁ - ၁၆":
                    raise ValidationErr(f"{data[0][:-6]}နှစ် {data[0][-4:][-2:]}လ အတွက် {data[1]}D စာရင်းပိတ်သွားပါပြီ")
            case _:
                raise ValidationErr("အချက်အလက် မှားယွင်းနေပါသည်")
            
