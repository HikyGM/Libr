import sys
import sqlite3
import datetime
from PyQt5 import uic, QtWidgets  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class Give_book(QMainWindow):
    def __init__(self, type, ex, id_journal=0):
        super().__init__()
        uic.loadUi('forms/give_book.ui', self)
        self.connection = sqlite3.connect("db/library_db.sqlite")
        self.ex = ex
        self.type = type
        self.id_journal = id_journal
        self.btn_add.clicked.connect(self.add_give)
        self.btn_cancel.clicked.connect(self.close)

        self.date_give.setDate(datetime.date.today())
        self.date_give.setCalendarPopup(True)

        # if self.type == 0:
        # заполнение комбобокса клиентов
        cursor = self.connection.cursor()
        clients = cursor.execute("""SELECT * FROM clients""").fetchall()
        self.client = [[i[0], i[1]] for i in clients]
        for row in self.client:
            self.search_clients.addItem(row[1])

        # заполнение комбобокса книг
        cursor = self.connection.cursor()
        books = cursor.execute("""SELECT * FROM books""").fetchall()
        self.book = [[i[0], i[1]] for i in books]
        d = str(datetime.date.today()).split('-')
        self.date_give.setDate(datetime.date(int(d[0]), int(d[1]), int(d[2])))
        for row in self.book:
            self.search_books.addItem(row[1])
        if self.type == 1:
            cursor = self.connection.cursor()
            res = cursor.execute(
                """SELECT id_book, id_client, date, count_book FROM clients_books WHERE id_clients_books = ?""",
                (self.id_journal,)).fetchall()
            all_info = res[0]
            id_book, id_client, date, count_book = all_info
            for i in range(len(clients)):
                if clients[i][0] == id_client:
                    self.search_clients.setCurrentIndex(i)
                    break

            for i in range(len(books)):
                if books[i][0] == id_book:
                    self.search_books.setCurrentIndex(i)
                    break
            d = date.split('-')
            self.date_give.setDate(datetime.date(int(d[0]), int(d[1]), int(d[2])))
            self.count_line.setText(str(count_book))
            cursor = self.connection.cursor()
            give = f'UPDATE books ' + \
                   f'SET count_books = count_books + {int(count_book)} ' + \
                   f'WHERE id_book = {id_book}'
            cursor.execute(give)
            self.connection.commit()

    def add_give(self):

        index_client = self.search_clients.currentIndex()
        index_book = self.search_books.currentIndex()
        date = self.date_give.date().toPyDate()
        cursor = self.connection.cursor()
        res = list(cursor.execute(f'SELECT count_books FROM books WHERE id_book = {self.book[index_book][0]}'))[0][0]
        if self.count_line.text():
            if int(self.count_line.text()) < 1:
                self.label_info.setText('Укажите корректное кол-во книг')
            elif int(res) - int(self.count_line.text()) >= 0:

                if self.type == 0:
                    cursor = self.connection.cursor()
                    give = f'INSERT INTO clients_books(id_book, id_client, date, count_book) ' \
                           f'VALUES ({self.book[index_book][0]}, {self.client[index_client][0]}, ' \
                           f'"{date}", {self.count_line.text()})'
                    cursor.execute(give)
                    self.connection.commit()
                    cursor = self.connection.cursor()
                    give = f'UPDATE books ' + \
                           f'SET count_books = "{int(res) - int(self.count_line.text())}" ' + \
                           f'WHERE id_book = {self.book[index_book][0]}'
                    cursor.execute(give)
                    self.connection.commit()

                elif self.type == 1:



                    cursor = self.connection.cursor()
                    give = f'UPDATE clients_books ' + \
                           f'SET id_book = "{self.book[index_book][0]}", id_client = "{self.client[index_client][0]}", ' + \
                           f'date= "{date}", count_book = "{self.count_line.text()}" ' + \
                           f'WHERE id_clients_books = {self.id_journal}'
                    cursor.execute(give)
                    self.connection.commit()

                    cursor = self.connection.cursor()
                    give = f'UPDATE books ' + \
                           f'SET count_books = "{int(res) - int(self.count_line.text())}" ' + \
                           f'WHERE id_book = {self.book[index_book][0]}'
                    cursor.execute(give)
                    self.connection.commit()

                self.ex.journal()
                self.close()
            else:
                self.label_info.setText('Нет в наличии такого кол-ва')
        else:
            self.label_info.setText('Укажите кол-во книг')


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Give_book()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
