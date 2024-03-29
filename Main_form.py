import sys
import sqlite3
import csv
from add_book import Add_book
from new_auth import New_auth
from client_add import Clients
from give_book import Give_book
from PyQt5 import uic, QtWidgets  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox, QFileDialog


class Main_form(QMainWindow):
    def __init__(self):
        super().__init__()
        self.connection = sqlite3.connect("db/library_db.sqlite")
        uic.loadUi('forms/main_wid.ui', self)  # Загружаем дизайн
        self.id_books = []
        self.type_table = 0
        self.books_view()
        self.btn_books.clicked.connect(self.books_view)
        self.btn_journal.clicked.connect(self.journal)
        self.btn_author.clicked.connect(self.author_view)
        self.btn_clients.clicked.connect(self.client_view)
        self.btn_add.clicked.connect(self.add)
        self.btn_edit.clicked.connect(self.edit)
        self.btn_del.clicked.connect(self.delete)
        # self.main_table.itemChanged.connect(self.edit)
        self.btn_search.clicked.connect(self.search)
        self.export_base.clicked.connect(self.export)

    def export(self):
        cursor = self.connection.cursor()
        name_dir = QFileDialog.getExistingDirectory()
        name_tables = ['authors', 'authors_books', 'books', 'clients',
                       'clients_books', 'genre', 'genre_books', 'users']
        if name_dir:
            for table in name_tables:
                cursor.execute(f'SELECT * FROM {table}')
                with open(name_dir + '/' + table + '.csv', 'w', encoding="utf8") as csv_file:
                    csv_out = csv.writer(csv_file)
                    csv_out.writerow([d[0] for d in cursor.description])
                    for result in cursor:
                        csv_out.writerow(result)
            cursor.close()

    def search(self):
        if self.type_table == 0:
            self.books_view(self.input_search.text())
        elif self.type_table == 1:
            self.journal(self.input_search.text())
        elif self.type_table == 2:
            self.author_view(self.input_search.text())
        elif self.type_table == 3:
            self.client_view(self.input_search.text())

    def books_view(self, search=''):
        self.type_table = 0
        self.tab_clear()
        if not search:
            search = ''
        cursor = self.connection.cursor()
        books = cursor.execute(f"SELECT id_book, name_book, id_book, id_book, year_publication, count_books, comm_book "
                               f"FROM books "
                               f"WHERE name_book "
                               f"LIKE '%{search}%'").fetchall()
        self.main_table.setColumnCount(7)
        # скрытие столбца с ID книг
        self.main_table.setColumnHidden(0, True)
        self.main_table.setHorizontalHeaderLabels(
            ['ID', 'Название книги', 'Авторы', 'Жанр', 'Год', 'Кол-во', 'Комментарий'])
        self.main_table.setRowCount(len(books))
        # запрет на редактирование содержимого таблицы
        self.main_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # выделение всей строки при нажатии на айтем
        self.main_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        row_num = self.main_table.currentRow()
        self.main_table.selectRow(row_num)
        # убираем не нужные номера строк
        self.main_table.verticalHeader().setVisible(False)
        # установка адаптивно заполняющего размера ячеек
        self.main_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        # установка размера ячеек по вертикали
        self.main_table.verticalHeader().setDefaultSectionSize(100)
        # self.main_table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        # установка размера ячеек по горизонтали
        # self.main_table.horizontalHeader().setDefaultSectionSize(150)
        # фиксированный размер 3 столбца
        # self.main_table.horizontalHeader().setSectionResizeMode(5, QtWidgets.QHeaderView.Fixed)

        self.main_table.horizontalHeader().setDefaultSectionSize(100)
        # фиксированный размер 3 столбца
        self.main_table.horizontalHeader().setSectionResizeMode(4, QtWidgets.QHeaderView.Fixed)
        self.main_table.horizontalHeader().setSectionResizeMode(5, QtWidgets.QHeaderView.Fixed)

        for i, elem in enumerate(books):
            for j, val in enumerate(elem):
                if j == 2:
                    self.id_books.append(val)
                    authors = cursor.execute("""
                            SELECT a.name_author 
                            FROM authors_books ab, authors a
                            WHERE ab.id_author = a.id_author and ab.id_book = ?""", (val,)).fetchall()
                    self.main_table.setItem(i, j, QTableWidgetItem(", ".join([i[0] for i in authors])))
                elif j == 3:
                    genre = cursor.execute("""
                            SELECT a.name_genre
                            FROM genre_books ab, genre a
                            WHERE ab.id_genre = a.id_genre and ab.id_book = ?""", (val,)).fetchall()
                    self.main_table.setItem(i, j, QTableWidgetItem(", ".join([i[0] for i in genre])))
                else:
                    self.main_table.setItem(i, j, QTableWidgetItem(str(val)))

    def tab_clear(self):
        # Удаление содержимого таблицы
        self.main_table.clear()
        # Удаление сетки таблицы
        self.main_table.setRowCount(0)
        self.main_table.setColumnCount(0)

    def journal(self, search=''):
        self.type_table = 1
        self.tab_clear()
        if not search:
            search = ''
        cursor = self.connection.cursor()
        ar = f"SELECT cb.id_clients_books, cb.id_client, cb.id_book, cb.date, cb.count_book, cb.id_book " + \
             f"FROM clients_books cb, clients c " + \
             f"WHERE cb.id_client = c.id_client AND c.name_client " + \
             f"LIKE '%{search}%'"
        journal = cursor.execute(ar).fetchall()
        self.main_table.setColumnCount(6)
        self.main_table.setColumnHidden(0, True)
        self.main_table.setColumnHidden(5, True)
        self.main_table.setHorizontalHeaderLabels(
            ['ID', 'Клиент', 'Книга', 'Дата выдачи', 'Кол-во', 'ID_book'])
        self.main_table.setRowCount(len(journal))
        self.main_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.main_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        row_num = self.main_table.currentRow()
        self.main_table.selectRow(row_num)
        self.main_table.verticalHeader().setVisible(False)
        self.main_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.main_table.verticalHeader().setDefaultSectionSize(70)
        for i, elem in enumerate(journal):
            for j, val in enumerate(elem):
                if j == 1:
                    self.id_books.append(val)
                    client = cursor.execute("""
                            SELECT name_client 
                            FROM clients
                            WHERE id_client = ?""", (val,)).fetchall()
                    self.main_table.setItem(i, j, QTableWidgetItem(", ".join([i[0] for i in client])))
                elif j == 2:
                    book = cursor.execute("""
                            SELECT name_book
                            FROM books
                            WHERE id_book = ?""", (val,)).fetchall()
                    self.main_table.setItem(i, j, QTableWidgetItem(", ".join([i[0] for i in book])))
                else:
                    self.main_table.setItem(i, j, QTableWidgetItem(str(val)))

    def author_view(self, search=''):
        self.type_table = 2
        self.tab_clear()
        if not search:
            search = ''
        cursor = self.connection.cursor()
        auth = cursor.execute(f"SELECT id_author, name_author "
                              f"FROM authors "
                              f"WHERE name_author "
                              f"LIKE '%{search}%'").fetchall()
        self.main_table.setColumnCount(2)
        self.main_table.setColumnHidden(0, True)
        self.main_table.setHorizontalHeaderLabels(
            ['ID', 'Авторы'])
        self.main_table.setRowCount(len(auth))
        self.main_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.main_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        row_num = self.main_table.currentRow()
        self.main_table.selectRow(row_num)
        self.main_table.verticalHeader().setVisible(False)
        self.main_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.main_table.verticalHeader().setDefaultSectionSize(70)
        for i, elem in enumerate(auth):
            for j, val in enumerate(elem):
                self.main_table.setItem(i, j, QTableWidgetItem(str(val)))

    def client_view(self, search=''):
        self.type_table = 3
        self.tab_clear()
        if not search:
            search = ''
        cursor = self.connection.cursor()
        auth = cursor.execute(f"SELECT id_client, name_client "
                              f"FROM clients "
                              f"WHERE name_client "
                              f"LIKE '%{search}%'"
                              ).fetchall()
        self.main_table.setColumnCount(2)
        self.main_table.setColumnHidden(0, True)
        self.main_table.setHorizontalHeaderLabels(
            ['ID', 'Клиенты'])
        self.main_table.setRowCount(len(auth))
        self.main_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.main_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        row_num = self.main_table.currentRow()
        self.main_table.selectRow(row_num)
        self.main_table.verticalHeader().setVisible(False)
        self.main_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.main_table.verticalHeader().setDefaultSectionSize(70)
        for i, elem in enumerate(auth):
            for j, val in enumerate(elem):
                self.main_table.setItem(i, j, QTableWidgetItem(str(val)))

    def add(self):
        if self.type_table == 0:
            self.add_book = Add_book(0, self, 0)
            self.add_book.show()
            self.books_view()
        elif self.type_table == 1:
            self.add_give = Give_book(0, self)
            self.add_give.show()
        elif self.type_table == 2:
            self.add_auth = New_auth(self, 0, 0, 1)
            self.add_auth.show()
        elif self.type_table == 3:
            self.add_client = Clients(self, 0, 0, 1)
            self.add_client.show()

    def edit(self):
        if self.type_table == 0:
            id_book = self.check()
            if id_book:
                self.edit_book = Add_book(1, self, str(id_book))
                self.edit_book.show()
        elif self.type_table == 1:
            id_journal = self.check()
            if id_journal:
                self.add_give = Give_book(1, self, id_journal)
                self.add_give.show()
        elif self.type_table == 2:
            id_auth = self.check()
            if id_auth:
                self.add_auth = New_auth(self, self.check(), 1)
                self.add_auth.show()
        elif self.type_table == 3:
            id_client = self.check()
            if id_client:
                self.edit_client = Clients(self, self.check(), 1)
                self.edit_client.show()

    def delete(self):
        if self.type_table == 0:
            index_rows = list(set(i.row() for i in self.main_table.selectedItems()))
            if index_rows:
                choice = QMessageBox.question(self, '', 'Вы действительно хотите удалить книгу?',
                                              QMessageBox.Yes | QMessageBox.No)
                if choice == QMessageBox.Yes:
                    for elem in index_rows:
                        ids = self.main_table.item(elem, 0).text()
                        cursor = self.connection.cursor()
                        m = f'DELETE FROM books WHERE id_book = {str(ids)}'
                        cursor.execute(m)
                        self.connection.commit()
                        self.connection.commit()
                        cursor = self.connection.cursor()
                        n = f'DELETE FROM clients_books WHERE id_book = {str(ids)}'
                        cursor.execute(n)
                        self.connection.commit()
                        self.books_view()
                elif choice == QMessageBox.No:
                    pass
        elif self.type_table == 1:
            index_rows = list(set(i.row() for i in self.main_table.selectedItems()))
            if index_rows:
                choice = QMessageBox.question(self, '', 'Вы действительно хотите удалить запись?',
                                              QMessageBox.Yes | QMessageBox.No)
                if choice == QMessageBox.Yes:
                    for elem in index_rows:
                        idk = self.main_table.item(elem, 4).text()
                        idb = self.main_table.item(elem, 5).text()
                        cursor = self.connection.cursor()
                        give = f'UPDATE books ' + \
                               f'SET count_books = count_books + {int(idk)} ' + \
                               f'WHERE id_book = {idb}'
                        cursor.execute(give)
                        self.connection.commit()

                        ids = self.main_table.item(elem, 0).text()
                        cursor = self.connection.cursor()
                        m = f'DELETE FROM clients_books WHERE id_clients_books = {str(ids)}'
                        cursor.execute(m)
                        self.connection.commit()
                    self.journal()
                elif choice == QMessageBox.No:
                    pass
        elif self.type_table == 2:
            index_rows = list([i.row() for i in self.main_table.selectedItems()])
            if index_rows:
                choice = QMessageBox.question(self, '', 'Вы действительно хотите удалить автора?',
                                              QMessageBox.Yes | QMessageBox.No)
                if choice == QMessageBox.Yes:
                    for elem in index_rows:
                        ids = self.main_table.item(elem, 0).text()
                        cursor = self.connection.cursor()
                        m = f'DELETE FROM authors WHERE id_author = {str(ids)}'
                        cursor.execute(m)
                        self.connection.commit()
                        cursor = self.connection.cursor()
                        n = f'DELETE FROM authors_books WHERE id_author = {str(ids)}'
                        cursor.execute(n)
                        self.connection.commit()
                    self.author_view()
                elif choice == QMessageBox.No:
                    pass
        elif self.type_table == 3:
            index_rows = list([i.row() for i in self.main_table.selectedItems()])
            if index_rows:
                choice = QMessageBox.question(self, '', 'Вы действительно хотите удалить клиента?',
                                              QMessageBox.Yes | QMessageBox.No)
                if choice == QMessageBox.Yes:
                    for elem in index_rows:
                        ids = self.main_table.item(elem, 0).text()
                        cursor = self.connection.cursor()
                        m = f'DELETE FROM clients WHERE id_client = {str(ids)}'
                        cursor.execute(m)
                        self.connection.commit()
                        cursor = self.connection.cursor()
                        n = f'DELETE FROM clients_books WHERE id_client = {str(ids)}'
                        cursor.execute(n)
                        self.connection.commit()
                    self.client_view()
                elif choice == QMessageBox.No:
                    pass

    def check(self):
        # Получение номера строки
        rows = list(set([i.row() for i in self.main_table.selectedItems()]))
        if rows:
            # Получение ID в строке (0-ой столбец)
            ids = self.main_table.item(rows[0], 0).text()
            return ids
        else:
            return False


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main_form()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
