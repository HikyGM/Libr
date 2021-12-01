import sys
from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow


class Edit_book(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('add_book.ui', self)  # Загружаем дизайн


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Edit_book()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
