# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(460, 390)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(238, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setText("")
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 0, 1, 3)
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.sAWC = QtWidgets.QWidget()
        self.sAWC.setGeometry(QtCore.QRect(0, 0, 440, 266))
        self.sAWC.setObjectName("sAWC")
        self.gridLayout = QtWidgets.QGridLayout(self.sAWC)
        self.gridLayout.setObjectName("gridLayout")
        self.tV = QtWidgets.QTableView(self.sAWC)
        self.tV.setMouseTracking(False)
        self.tV.setAutoScrollMargin(18)
        self.tV.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tV.setObjectName("tV")
        self.gridLayout.addWidget(self.tV, 0, 0, 1, 1)
        self.scrollArea.setWidget(self.sAWC)
        self.gridLayout_2.addWidget(self.scrollArea, 1, 0, 1, 3)
        self.pB_Plus = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pB_Plus.sizePolicy().hasHeightForWidth())
        self.pB_Plus.setSizePolicy(sizePolicy)
        self.pB_Plus.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("AddIcon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pB_Plus.setIcon(icon)
        self.pB_Plus.setObjectName("pB_Plus")
        self.gridLayout_2.addWidget(self.pB_Plus, 2, 0, 1, 1)
        self.pB_Minus = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pB_Minus.sizePolicy().hasHeightForWidth())
        self.pB_Minus.setSizePolicy(sizePolicy)
        self.pB_Minus.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("DelIcon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pB_Minus.setIcon(icon1)
        self.pB_Minus.setObjectName("pB_Minus")
        self.gridLayout_2.addWidget(self.pB_Minus, 2, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(371, 21, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 2, 2, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 460, 22))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action = QtWidgets.QAction(MainWindow)
        self.action.setObjectName("action")
        self.menu.addAction(self.action)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menu.setTitle(_translate("MainWindow", "Справочники"))
        self.action.setText(_translate("MainWindow", "Редактировать"))
