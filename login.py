import sys
import sqlite3
from Main_form import Main_form
from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow


class Login(QMainWindow):
    def __init__(self):
        super().__init__()
        self.connection = sqlite3.connect("db/library_db.sqlite")
        uic.loadUi('forms/login_form.ui', self)  # Загружаем дизайн
        self.btn_chek_auth.clicked.connect(self.chek_user)

    def chek_user(self):
        cursor = self.connection.cursor()
        if self.login_input.text():
            check = cursor.execute("""SELECT password FROM Users WHERE login = ?""",
                                        (self.login_input.text(),)).fetchone()
            if check[0] == self.password_input.text():
                ex.hide()
                self.main_form = Main_form()
                self.main_form.show()
            else:
                self.error_label.setText('Неверный логин или пароль')
        else:
            self.error_label.setText('Введите логин')


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Login()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
