import sys
import sqlite3
from PyQt5 import uic, QtWidgets  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class Clients(QMainWindow):
    def __init__(self, ab, id_client='', e_type='', type=''):
        super().__init__()
        self.ab = ab
        self.e_type = e_type
        self.type = type
        self.id_client = id_client
        print(self.type)
        uic.loadUi('client_add.ui', self)
        self.connection = sqlite3.connect("library_db2.sqlite")
        self.btn_ok.clicked.connect(self.add_client)
        self.btn_cancel.clicked.connect(self.close)


        if self.e_type == 1:
            cursor = self.connection.cursor()
            authors = cursor.execute(f'SELECT name_client FROM clients WHERE id_client = "{self.id_client}"').fetchall()
            self.client_name.setText(str(authors[0][0]))

    def add_client(self):
        if self.e_type == 0:
            cursor = self.connection.cursor()
            cursor.execute(f'INSERT INTO clients(name_client) VALUES ("{self.client_name.text()}")')
            self.connection.commit()
            if not self.type:
                self.ab.tab_add()
            elif self.type == 1:
                self.ab.client_view()
        elif self.e_type == 1:
            if self.id_client:
                cursor = self.connection.cursor()
                res = f'UPDATE clients SET name_client = "{self.client_name.text()}" WHERE id_client = {self.id_client}'
                cursor.execute(res)
                self.connection.commit()
                self.ab.client_view()
            else:
                pass

        self.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Clients()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
