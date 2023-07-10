# -*- coding: utf-8 -*-
# aufzeichnungen/main.py

"""This module provides aufzeichnungen."""

import sys
from PyQt5.QtWidgets import QApplication

from .views import Window
from .database import createConnection

def main():
    """ Create aufzeichnungen application"""
    app = QApplication(sys.argv)

    if not createConnection("aufzeichnungen.sqlite"):
        sys.exit(1)

    win = Window()
    win.show()

    sys.exit(app.exec_())