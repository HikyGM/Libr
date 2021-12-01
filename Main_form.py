import sys
import sqlite3
from check_dialog import Check
from add_book import Add_book
from edit_book import Edit_book
from error_edit import Error_edit
from PyQt5 import uic, QtWidgets  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class Main_form(QMainWindow):
    def __init__(self):
        super().__init__()
        self.connection = sqlite3.connect("library_db2.sqlite")
        uic.loadUi('main_wid.ui', self)  # Загружаем дизайн
        self.id_books = []
        self.books_view()
        self.btn_books.clicked.connect(self.books_view)
        self.btn_journal.clicked.connect(self.journal)
        self.btn_add.clicked.connect(self.add)
        self.btn_edit.clicked.connect(self.edit)
        self.btn_del.clicked.connect(self.delete)
        # self.main_table.itemChanged.connect(self.edit)

    def add(self):
        self.add_book = Add_book(0)
        self.add_book.show()

    def edit(self, item):
        # Получение номера строки
        rows = list(set([i.row() for i in self.main_table.selectedItems()]))
        # Получение 0-го элемента в строке (Название книги)
        ids = [self.main_table.item(i, 0).text() for i in rows]
        if ids:
            self.edit_book = Add_book(1, self.id_books[rows[0]])
            self.edit_book.show()
        else:
            self.error_edit = Error_edit()
            self.error_edit.show()

    def delete(self):
        self.check = Check()
        self.check.show()

    def books_view(self):
        # Удаление содержимого таблицы
        self.main_table.clear()
        # Удаление сетки таблицы
        self.main_table.setRowCount(0)
        self.main_table.setColumnCount(0)

        cursor = self.connection.cursor()

        books = cursor.execute("""SELECT name_book, id_book, id_book, year_publication FROM books""").fetchall()
        self.main_table.setColumnCount(4)
        self.main_table.setHorizontalHeaderLabels(['Название книги', 'Авторы', 'Жанр', 'Год издания'])
        self.main_table.setRowCount(len(books))

        # запрет на редактирование содержимого таблицы
        self.main_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        self.main_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

        row_num = self.main_table.currentRow()
        self.main_table.selectRow(row_num)
        # убираем не нужные номера строк
        self.main_table.verticalHeader().setVisible(False)

        # установка адаптивно заполняющего размера ячеек
        self.main_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        # установка размера ячеек по вертикали
        self.main_table.verticalHeader().setDefaultSectionSize(70)

        # self.main_table.horizontalHeader().setMinimumSectionSize(90)

        # установка размера ячеек по горизонтали
        self.main_table.horizontalHeader().setDefaultSectionSize(200)
        # установка фиксированного размера определённых столбцов
        # Interactive(или 0) - размер может быть изменен пользователем или программно;

        # Stretch(или 1) - секции автоматически равномерно распределяют свободное пространство между собой.Размер не
        # может быть изменен ни пользователем, ни программно;

        # Fixed(или 2) - размер может быть изменен только программно;

        # ResizeToContents(или 3) - размер определяется автоматически по содержимому секции.Размер не может быть изменен
        # ни пользователем, ни программно;
        # self.main_table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.main_table.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Fixed)

        # запрос на авторов
        # select a.name_author
        # from authors_books ab, authors a
        # where ab.id_author = a.id_author and ab.id_book = 1

        for i, elem in enumerate(books):
            for j, val in enumerate(elem):

                if j == 1:
                    self.id_books.append(val)
                    authors = cursor.execute("""
                            SELECT a.name_author 
                            FROM authors_books ab, authors a
                            WHERE ab.id_author = a.id_author and ab.id_book = ?""", (val,)).fetchall()
                    self.main_table.setItem(i, j, QTableWidgetItem(", ".join([i[0] for i in authors])))
                elif j == 2:
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


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main_form()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
