# -*- coding: utf-8 -*-
# aufzeichnungen/database.py

""" this module provides database connection """

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtSql import (
    QSqlDatabase,
    QSqlQuery
)

def _createRecordsTable():
    "Create records table in the database"
    createRecordsTableQuery = QSqlQuery()
    createRecordsTableQuery.exec(
        """
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            date VARCHAR(40) NOT NULL,
            record_type VARCHAR(50) NOT NULL,
            time_limit VARCHAR(50) NOT NULL,
            created_at DATE NOT NULL
        )
        """
    )

def _createRecordDetailsTable():
    createRecordDetailsTableQuery = QSqlQuery()
    createRecordDetailsTableQuery.exec(
        """
        CREATE TABLE IF NOT EXISTS record_details (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            key VARCHAR(20) NOT NULL,
            value VARCHAR(20) NOT NULL,
            record_id VARCHAR(20) NOT NULL,
            FOREIGN KEY (record_id) REFERENCES records ON DELETE CASCADE
        )
        """
    )

def createConnection(databaseName):
    "Create and open database connection"
    connection = QSqlDatabase.addDatabase("QSQLITE")
    connection.setDatabaseName(databaseName)

    if not connection.open():
        QMessageBox.warning(
            None,
            "စာရင်းဒေတာ",
            f"Database Error : {connection.lastError().text()}"
        )
        return False
    _createRecordsTable()
    _createRecordDetailsTable()
    return True