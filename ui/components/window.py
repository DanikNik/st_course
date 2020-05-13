# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'window.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(906, 714)
        MainWindow.setIconSize(QtCore.QSize(32, 32))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textList = QtWidgets.QListWidget(self.centralwidget)
        self.textList.setObjectName("textList")
        self.verticalLayout.addWidget(self.textList)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.message = QtWidgets.QTextEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.message.sizePolicy().hasHeightForWidth())
        self.message.setSizePolicy(sizePolicy)
        self.message.setMaximumSize(QtCore.QSize(16777215, 100))
        self.message.setObjectName("message")
        self.horizontalLayout.addWidget(self.message)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.dst = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dst.sizePolicy().hasHeightForWidth())
        self.dst.setSizePolicy(sizePolicy)
        self.dst.setText("")
        self.dst.setCursorMoveStyle(QtCore.Qt.LogicalMoveStyle)
        self.dst.setObjectName("dst")
        self.verticalLayout_2.addWidget(self.dst)
        self.send_button = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.send_button.sizePolicy().hasHeightForWidth())
        self.send_button.setSizePolicy(sizePolicy)
        self.send_button.setMinimumSize(QtCore.QSize(150, 40))
        self.send_button.setCheckable(False)
        self.send_button.setChecked(False)
        self.send_button.setDefault(False)
        self.send_button.setFlat(False)
        self.send_button.setObjectName("send_button")
        self.verticalLayout_2.addWidget(self.send_button)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.LeftToolBarArea, self.toolBar)
        self.mSetting = QtWidgets.QAction(MainWindow)
        self.mSetting.setObjectName("mSetting")
        self.mConnect = QtWidgets.QAction(MainWindow)
        self.mConnect.setObjectName("mConnect")
        self.mExit = QtWidgets.QAction(MainWindow)
        self.mExit.setObjectName("mExit")
        self.mInfo = QtWidgets.QAction(MainWindow)
        self.mInfo.setObjectName("mInfo")
        self.toolBar.addAction(self.mSetting)
        self.toolBar.addAction(self.mConnect)
        self.toolBar.addAction(self.mExit)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.mInfo)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Главное окно"))
        self.dst.setPlaceholderText(_translate("MainWindow", "Адрес назначения (адрес 255 - отправить всем)"))
        self.send_button.setText(_translate("MainWindow", "Отправить"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.mSetting.setText(_translate("MainWindow", "Настроить"))
        self.mConnect.setText(_translate("MainWindow", "Подключиться"))
        self.mExit.setText(_translate("MainWindow", "Выход"))
        self.mInfo.setText(_translate("MainWindow", "Информация"))
