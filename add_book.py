import sys
import sqlite3
from PyQt5 import uic, QtWidgets  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class Add_book(QMainWindow):
    def __init__(self, type, ex, id_book=0):
        super().__init__()
        self.type = type
        self.id_book = id_book
        self.ex = ex
        self.count_author = 0
        self.connection = sqlite3.connect("library_db2.sqlite")
        uic.loadUi('add_book.ui', self)  # Загружаем дизайн
        self.btn_cancel.clicked.connect(self.close)
        self.btn_add_tab_auth.clicked.connect(self.add_tab_auth)
        self.btn_del_auth_tab.clicked.connect(self.del_tab_auth)
        self.table_authors.setColumnCount(2)
        self.table_authors.setColumnHidden(0, True)
        self.table_authors.setHorizontalHeaderLabels(['id', 'Авторы'])
        self.table_authors.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        cursor = self.connection.cursor()
        authors = cursor.execute("""SELECT * FROM authors""").fetchall()
        # имена авторов

        self.auth = [[i[0], i[1]] for i in authors]
        # заполнение комбобокс именами авторов
        for row in self.auth:
            self.search_author.addItem(row[1])

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


            idab = list(cursor.execute(f'SELECT id_author FROM authors_books WHERE id_book = {self.id_book}').fetchall())
            a = [idab[i] for i in range(len(idab))]
            for i in a:
                rowPosition = self.table_authors.rowCount()
                self.table_authors.insertRow(rowPosition)
                cursor = self.connection.cursor()
                nb = cursor.execute(f'SELECT name_author FROM authors WHERE id_author = {i[0]}').fetchone()
                for j in nb:
                    self.table_authors.setItem(self.count_author, 0, QTableWidgetItem(str(i[0])))
                    self.table_authors.setItem(self.count_author, 1, QTableWidgetItem(j))
                    self.count_author += 1
            self.cr = [self.table_authors.item(i, 0).text() for i in range(self.table_authors.rowCount())]
            self.text_comm.setPlainText(comm)
            self.btn_add.setText('Изменить')
            self.btn_add.clicked.connect(self.check)

    def add_tab_auth(self):
        rowPosition = self.table_authors.rowCount()
        self.table_authors.insertRow(rowPosition)
        index = self.search_author.currentIndex()
        print('in', index)
        self.table_authors.setItem(self.count_author, 0, QTableWidgetItem(str(self.auth[index][0])))
        self.table_authors.setItem(self.count_author, 1, QTableWidgetItem(self.auth[index][1]))
        self.count_author += 1

    def del_tab_auth(self):
        index_rows = list([i.row() for i in self.table_authors.selectedItems()])
        if index_rows:
            index_rows.reverse()
            for elem in index_rows:
                self.table_authors.removeRow(elem)
                self.count_author -= 1

    def check(self):
        if not self.line_name.text():
            self.lab_info.setText('Заполните название книги')
        elif not self.table_authors.rowCount():
            self.lab_info.setText('Добавьте автора книги')
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

        cursor = self.connection.cursor()
        ids = cursor.execute(f'SELECT id_book FROM books ORDER BY id_book DESC LIMIT 1').fetchone()
        ida = list(set([self.table_authors.item(i, 0).text() for i in range(self.table_authors.rowCount())]))
        for num in range(len(ida)):
            cursor.execute(f'INSERT INTO authors_books(id_book, id_author) VALUES ({ids[0]}, {ida[num]})')
            self.connection.commit()

        self.ex.books_view()
        self.close()

    def edit(self):
        cursor = self.connection.cursor()
        res = f'UPDATE books SET name_book = "{self.line_name.text()}", year_publication = "{self.line_year.text()}", count_books= "{self.line_count.text()}", comm_book = "{self.text_comm.toPlainText()}" WHERE id_book = {self.id_book}'
        cursor.execute(res)
        self.connection.commit()

        for i in range(len(self.cr)):
            cursor = self.connection.cursor()
            tabres = f'DELETE FROM authors_books WHERE id_book = {self.id_book} AND id_author = {self.cr[i]}'
            print(tabres)
            cursor.execute(tabres)
            self.connection.commit()

        cursor = self.connection.cursor()
        ids = cursor.execute(f'SELECT id_book FROM books ORDER BY id_book DESC LIMIT 1').fetchone()
        ida = list(set([self.table_authors.item(i, 0).text() for i in range(self.table_authors.rowCount())]))
        for num in range(len(ida)):
            cursor.execute(f'INSERT INTO authors_books(id_book, id_author) VALUES ({self.id_book}, {ida[num]})')
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
