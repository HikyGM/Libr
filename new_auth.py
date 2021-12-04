import sys
import sqlite3
from PyQt5 import uic, QtWidgets  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class New_auth(QMainWindow):
    def __init__(self, ab, id_auth='', e_type='', type=''):
        super().__init__()
        self.ab = ab
        self.e_type = e_type
        self.type = type
        self.id_auth = id_auth
        print(self.type)
        uic.loadUi('new_auth.ui', self)
        self.connection = sqlite3.connect("library_db2.sqlite")
        self.btn_ok_auth.clicked.connect(self.add_auth)
        self.btn_canc.clicked.connect(self.close)


        if self.e_type == 1:
            cursor = self.connection.cursor()
            authors = cursor.execute(f'SELECT name_author FROM authors WHERE id_author = "{self.id_auth}"').fetchall()
            self.name_auth.setText(str(authors[0][0]))

    def add_auth(self):
        if self.e_type == 0:
            cursor = self.connection.cursor()
            cursor.execute(f'INSERT INTO authors(name_author) VALUES ("{self.name_auth.text()}")')
            self.connection.commit()
            if not self.type:
                self.ab.tab_add()
            elif self.type == 1:
                self.ab.author_view()
        elif self.e_type == 1:
            if self.id_auth:
                cursor = self.connection.cursor()
                res = f'UPDATE authors SET name_author = "{self.name_auth.text()}" WHERE id_author = {self.id_auth}'
                print(res)
                cursor.execute(res)
                self.connection.commit()
                self.ab.author_view()
            else:
                pass

        self.close()

    # def check(self):
    #     # Получение номера строки
    #     rows = list(set([i.row() for i in self.main_table.selectedItems()]))
    #     if rows:
    #         # Получение ID книги
    #         ids = self.main_table.item(rows[0], 0).text()
    #         return ids
    #     else:
    #         return False


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = New_auth()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
