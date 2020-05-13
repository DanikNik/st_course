# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'connect.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 201)
        self.submit = QtWidgets.QPushButton(Dialog)
        self.submit.setGeometry(QtCore.QRect(270, 170, 111, 23))
        self.submit.setObjectName("submit")
        self.com1 = QtWidgets.QLineEdit(Dialog)
        self.com1.setGeometry(QtCore.QRect(110, 40, 113, 23))
        self.com1.setObjectName("com1")
        self.com2 = QtWidgets.QLineEdit(Dialog)
        self.com2.setGeometry(QtCore.QRect(110, 80, 113, 23))
        self.com2.setObjectName("com2")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 40, 81, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(10, 80, 81, 16))
        self.label_2.setObjectName("label_2")
        self.addr = QtWidgets.QLineEdit(Dialog)
        self.addr.setGeometry(QtCore.QRect(110, 170, 113, 23))
        self.addr.setText("")
        self.addr.setObjectName("addr")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(20, 170, 81, 16))
        self.label_3.setObjectName("label_3")
        self.speed = QtWidgets.QLineEdit(Dialog)
        self.speed.setGeometry(QtCore.QRect(110, 120, 113, 23))
        self.speed.setText("")
        self.speed.setObjectName("speed")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(20, 120, 81, 16))
        self.label_4.setObjectName("label_4")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Подключиться"))
        self.submit.setText(_translate("Dialog", "Подключиться"))
        self.label.setText(_translate("Dialog", " COM-port 1"))
        self.label_2.setText(_translate("Dialog", " COM-port 2"))
        self.label_3.setText(_translate("Dialog", "Адрес"))
        self.label_4.setText(_translate("Dialog", "Скорость"))
