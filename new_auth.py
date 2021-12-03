import sys
import sqlite3
from PyQt5 import uic, QtWidgets  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class New_auth(QMainWindow):
    def __init__(self, ab):
        super().__init__()
        self.ab = ab
        uic.loadUi('new_auth.ui', self)
        self.connection = sqlite3.connect("library_db2.sqlite")
        self.btn_ok_auth.clicked.connect(self.add_auth)

    def add_auth(self):
        cursor = self.connection.cursor()
        cursor.execute(f'INSERT INTO authors(name_author) VALUES ("{self.name_auth.text()}")')
        self.connection.commit()
        self.ab.tab_add()
        self.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = New_auth()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
