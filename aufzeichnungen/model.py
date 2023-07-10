# -*- coding: utf-8 -*-
# aufzeichnungen/database.py

""" this module provides models related to records """
from PyQt5.QtSql import QSqlQuery

class Record():
    def __init__(self):
        self.model = self._getModels()

    @staticmethod
    def _getModels():
        """ query records """
        query = QSqlQuery("SELECT id, date, record_type, time_limit FROM records ORDER BY date DESC")
        return []
    
    def addRecord(self, data):
        print(data)