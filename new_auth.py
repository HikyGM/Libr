import sys
import sqlite3
from PyQt5 import uic, QtWidgets  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem

class New_auth(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('new_auth.ui', self)
        self.btn_ok_auth.clicked.connect(self.add_auth)

    def add_auth(self):
        return self.name_auth.text()