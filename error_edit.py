import sys
from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow


class Error_edit(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('error_edit.ui', self)  # Загружаем дизайн
        self.btn_error.clicked.connect(self.close)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Error_edit()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
