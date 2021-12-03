import sys
import sqlite3
from add_book import Add_book
from PyQt5 import uic, QtWidgets  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox


class Main_form(QMainWindow):
    def __init__(self):
        super().__init__()
        self.connection = sqlite3.connect("library_db2.sqlite")
        uic.loadUi('main_wid.ui', self)  # Загружаем дизайн
        self.id_books = []
        self.books_view()
        self.btn_books.clicked.connect(self.books_view)
        self.btn_journal.clicked.connect(self.journal)
        self.btn_author.clicked.connect(self.author_view)
        self.btn_add.clicked.connect(self.add)
        self.btn_edit.clicked.connect(self.edit)
        self.btn_del.clicked.connect(self.delete)
        # self.main_table.itemChanged.connect(self.edit)

    def books_view(self):
        # Удаление содержимого таблицы
        self.main_table.clear()
        # Удаление сетки таблицы
        self.main_table.setRowCount(0)
        self.main_table.setColumnCount(0)
        cursor = self.connection.cursor()
        books = cursor.execute(
            """SELECT id_book, name_book, id_book, id_book, year_publication, count_books, comm_book FROM books""").fetchall()
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
        self.main_table.verticalHeader().setDefaultSectionSize(70)
        # self.main_table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        # установка размера ячеек по горизонтали
        self.main_table.horizontalHeader().setDefaultSectionSize(150)
        # фиксированный размер 3 столбца
        self.main_table.horizontalHeader().setSectionResizeMode(5, QtWidgets.QHeaderView.Fixed)

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

    def journal(self):
        # Удаление содержимого таблицы
        self.main_table.clear()
        # Удаление сетки таблицы
        self.main_table.setRowCount(0)
        self.main_table.setColumnCount(0)

    def author_view(self):
        # Удаление содержимого таблицы
        self.main_table.clear()
        # Удаление сетки таблицы
        self.main_table.setRowCount(0)
        self.main_table.setColumnCount(0)
        self.books_view()

    def add(self):
        self.add_book = Add_book(0, self, 0)
        self.add_book.show()
        self.books_view()

    def edit(self):
        id_book = self.check()
        if id_book:
            self.edit_book = Add_book(1, self, str(id_book))
            self.edit_book.show()

    def delete(self):
        id_book = self.check()
        if id_book:
            choice = QMessageBox.question(self, '', 'Вы действительно хотите удалить книгу?',
                                          QMessageBox.Yes | QMessageBox.No)
            if choice == QMessageBox.Yes:
                cursor = self.connection.cursor()
                m = f'DELETE FROM books WHERE id_book = {str(id_book)}'
                cursor.execute(m)
                self.connection.commit()
                self.books_view()
            elif choice == QMessageBox.No:
                pass

    def check(self):
        # Получение номера строки
        rows = list(set([i.row() for i in self.main_table.selectedItems()]))
        if rows:
            # Получение ID книги
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
