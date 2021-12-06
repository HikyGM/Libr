import sys
import sqlite3
from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow


class Check(QMainWindow):
    def __init__(self, id_book):
        super().__init__()
        self.connection = sqlite3.connect("db/library_db.sqlite")
        uic.loadUi('forms/check_dialog.ui', self)  # Загружаем дизайн
        self.id_book = id_book
        self.btn_no.clicked.connect(self.close)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Check()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
