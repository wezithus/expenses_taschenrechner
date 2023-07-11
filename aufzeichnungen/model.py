# -*- coding: utf-8 -*-
# aufzeichnungen/database.py

""" this module provides models related to records """
from xml.dom import ValidationErr
from .datasets import ( DIGIT_TYPES, CURFEWS )
from datetime import datetime 

from PyQt5.QtCore import Qt
from PyQt5.QtSql import *

class Record():
    def __init__(self):
        self.model = self._getModels()

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
    
    def addRecord(self, data):
        date, digit, curfew, limit  = data[0].isoformat(), DIGIT_TYPES[data[1]], CURFEWS[data[2]], data[3]
        data = [date, digit, curfew, limit, datetime.today().strftime("%Y-%m-%d")]
        """validation"""
        self._validateRecordBeforeInsert(tuple(data))
        """insert record to the database."""
        rows = self.model.rowCount()
        self.model.insertRows(rows, 1)
        for column, field in enumerate(data):
            self.model.setData(self.model.index(rows, column + 1), field)
        self.model.submitAll()
        """refetch"""
        self.model.select()

    def _validateRecordBeforeInsert(self, data : tuple):
        for i in range(self.model.rowCount()):
            if self.model.record(i).value("date") == data[0] and self.model.record(i).value("digits") == data[1] and self.model.record(i).value("curfew") == data[2]:
                raise ValidationErr(f"{data[0]} နေ့အတွက် {data[1]}D စာရင်းဖွင့်ပြီးသားဖြစ်ပါသည်")
        match data[1]:
            case 2:
                if data[0] == datetime.now().strftime("%Y-%m-%d") and datetime.now().strftime("%H%M%S") > "120000" and data[2] == "နေ့လည်":
                    raise ValidationErr(f"{data[0]} နေ့အတွက် {data[1]}D စာရင်းပိတ်သွားပါပြီ")
            case 3:
                if data[0][-2:] > "16" and datetime.now().strftime("%H%M%S") > "160000" and data[2] == "၁ - ၁၆":
                    raise ValidationErr(f"{data[0][:-6]}နှစ် {data[0][-4:][-2:]}လ အတွက် {data[1]}D စာရင်းပိတ်သွားပါပြီ")
            case _:
                raise ValidationErr("အချက်အလက် မှားယွင်းနေပါသည်")
            
