# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'client_add.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(466, 142)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.client_name = QtWidgets.QLineEdit(self.centralwidget)
        self.client_name.setGeometry(QtCore.QRect(10, 20, 441, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.client_name.setFont(font)
        self.client_name.setObjectName("client_name")
        self.btn_ok = QtWidgets.QPushButton(self.centralwidget)
        self.btn_ok.setGeometry(QtCore.QRect(70, 80, 141, 31))
        self.btn_ok.setObjectName("btn_ok")
        self.btn_cancel = QtWidgets.QPushButton(self.centralwidget)
        self.btn_cancel.setGeometry(QtCore.QRect(260, 80, 141, 31))
        self.btn_cancel.setObjectName("btn_cancel")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Клиент"))
        self.btn_ok.setText(_translate("MainWindow", "Добавить"))
        self.btn_cancel.setText(_translate("MainWindow", "Отмена"))
