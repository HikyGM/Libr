import sys
import sqlite3
from PyQt5 import uic, QtWidgets  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class Add_book(QMainWindow):
    def __init__(self, type, ex, id_book=0):
        super().__init__()
        self.type = type
        self.id_book = id_book
        print(self.id_book)

        self.ex = ex
        self.count_author = 0
        self.connection = sqlite3.connect("library_db2.sqlite")
        uic.loadUi('add_book.ui', self)  # Загружаем дизайн
        self.btn_cancel.clicked.connect(self.close)
        self.table_authors.setColumnCount(1)
        self.table_authors.setHorizontalHeaderLabels(['Авторы'])
        self.table_authors.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        cursor = self.connection.cursor()
        authors = cursor.execute("""SELECT * FROM authors""").fetchall()

        # id авторов
        self.id_authors = [i[0] for i in authors]
        # имена авторов
        self.auth = [i[1] for i in authors]
        # заполнение комбобокс именами авторов
        for i in self.auth:
            self.search_author.addItem(i)
        self.btn_add_tab_auth.clicked.connect(self.add_tab_auth)
        if self.type == 0:

            self.btn_add.setText('Добавить')
            self.btn_add.clicked.connect(self.check)
        elif self.type == 1:

            cursor = self.connection.cursor()
            res = cursor.execute(
                """SELECT name_book, year_publication, count_books, comm_book FROM books WHERE id_book = ?""",
                (self.id_book,)).fetchall()
            all_info = res[0]
            name, year, count, comm = all_info
            self.line_name.setText(name)
            self.line_year.setText(str(year))
            self.line_count.setText(str(count))
            self.text_comm.setPlainText(comm)
            self.btn_add.setText('Изменить')
            self.btn_add.clicked.connect(self.check)

    def add_tab_auth(self):
        rowPosition = self.table_authors.rowCount()
        self.table_authors.insertRow(rowPosition)
        curr_text = self.search_author.currentText()
        self.table_authors.setItem(self.count_author, 0, QTableWidgetItem(curr_text))
        self.count_author += 1

    def check(self):
        if not self.line_name.text():
            self.lab_info.setText('Заполните название книги')
        # elif not self.table_authors.rowCount():
        #     self.lab_info.setText('Добавьте автора книги')
        elif not self.line_year.text():
            self.lab_info.setText('Заполните год издания')
        elif not self.line_count.text():
            self.lab_info.setText('Заполните количество')
        else:
            if self.type == 0:
                self.add()
            elif self.type == 1:
                self.edit()

    def add(self):
        cursor = self.connection.cursor()
        res = f'INSERT INTO books(name_book, year_publication, count_books, comm_book) VALUES ("{self.line_name.text()}", "{self.line_year.text()}", "{self.line_count.text()}", "{self.text_comm.toPlainText()}")'
        cursor.execute(res)
        self.connection.commit()
        self.ex.books_view()
        self.close()

    def edit(self):
        cursor = self.connection.cursor()
        res = f'UPDATE books SET name_book = "{self.line_name.text()}", year_publication = "{self.line_year.text()}", count_books= "{self.line_count.text()}", comm_book = "{self.text_comm.toPlainText()}" WHERE id_book = {self.id_book}'
        cursor.execute(res)
        self.connection.commit()
        self.ex.books_view()
        self.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Add_book()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
