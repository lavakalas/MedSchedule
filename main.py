import sqlite3
import sys
from pprint import pprint

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlRecord
from PyQt5.QtWidgets import QWidget, QApplication


class DictChange(QWidget):
    def __init__(self, db):
        super(DictChange, self).__init__()
        self.db = db
        self.setupUi(self)
        self.tb_AddRoom.clicked.connect(self.addRow)

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(773, 611)
        self.QTdb = QSqlDatabase.addDatabase('QSQLITE')
        self.QTdb.setDatabaseName(self.db)
        self.QTdb.open()

        self.model = QSqlTableModel(self, self.QTdb)
        self.model.setTable('rooms')
        self.model.select()

        self.tabWidget = QtWidgets.QTabWidget(Form)
        self.tabWidget.setGeometry(QtCore.QRect(-7, 1, 781, 611))
        self.tabWidget.setObjectName("tabWidget")
        self.Groups = QtWidgets.QWidget()
        self.Groups.setObjectName("Groups")
        self.pb_ImportGroups = QtWidgets.QPushButton(self.Groups)
        self.pb_ImportGroups.setGeometry(QtCore.QRect(650, 550, 111, 21))
        self.pb_ImportGroups.setObjectName("pb_ImportGroups")
        self.tb_AddGroup = QtWidgets.QToolButton(self.Groups)
        self.tb_AddGroup.setGeometry(QtCore.QRect(10, 550, 31, 31))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(".\\ui\\AddIcon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tb_AddGroup.setIcon(icon)
        self.tb_AddGroup.setObjectName("tb_AddGroup")
        self.tv_Groups = QtWidgets.QTableView(self.Groups)
        self.tv_Groups.setGeometry(QtCore.QRect(10, 10, 751, 531))
        self.tv_Groups.setObjectName("tv_Groups")

        self.QTdb.exec('INSERT INTO rooms(number) VALUES (210), (245)')
        self.QTdb.commit()

        self.tabWidget.addTab(self.Groups, "")
        self.Subjects = QtWidgets.QWidget()
        self.Subjects.setObjectName("Subjects")
        self.tv_Subjects = QtWidgets.QTableView(self.Subjects)
        self.tv_Subjects.setGeometry(QtCore.QRect(10, 10, 751, 531))
        self.tv_Subjects.setObjectName("tv_Subjects")
        self.pb_ImportSubjects = QtWidgets.QPushButton(self.Subjects)
        self.pb_ImportSubjects.setGeometry(QtCore.QRect(650, 550, 111, 21))
        self.pb_ImportSubjects.setObjectName("pb_ImportSubjects")
        self.tb_AddSubject = QtWidgets.QToolButton(self.Subjects)
        self.tb_AddSubject.setGeometry(QtCore.QRect(10, 550, 31, 31))
        self.tb_AddSubject.setIcon(icon)
        self.tb_AddSubject.setObjectName("tb_AddSubject")
        self.tabWidget.addTab(self.Subjects, "")
        self.Rooms = QtWidgets.QWidget()
        self.Rooms.setObjectName("Rooms")

        self.tv_Rooms = QtWidgets.QTableView(self.Rooms)
        self.tv_Rooms.setGeometry(QtCore.QRect(10, 10, 751, 531))
        self.tv_Rooms.setObjectName("tv_Rooms")
        self.tv_Rooms.setModel(self.model)

        self.pb_ImportRooms = QtWidgets.QPushButton(self.Rooms)
        self.pb_ImportRooms.setGeometry(QtCore.QRect(650, 550, 111, 21))
        self.pb_ImportRooms.setObjectName("pb_ImportRooms")
        self.tb_AddRoom = QtWidgets.QToolButton(self.Rooms)
        self.tb_AddRoom.setGeometry(QtCore.QRect(10, 550, 31, 31))
        self.tb_AddRoom.setIcon(icon)
        self.tb_AddRoom.setObjectName("tb_AddRoom")
        self.tabWidget.addTab(self.Rooms, "")

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pb_ImportGroups.setText(_translate("Form", "Import from Excel"))
        self.tb_AddGroup.setText(_translate("Form", "..."))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Groups), _translate("Form", "Учебные группы"))
        self.pb_ImportSubjects.setText(_translate("Form", "Import from Excel"))
        self.tb_AddSubject.setText(_translate("Form", "..."))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Subjects), _translate("Form", "Дисциплины"))
        self.pb_ImportRooms.setText(_translate("Form", "Import from Excel"))
        self.tb_AddRoom.setText(_translate("Form", "..."))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Rooms), _translate("Form", "Аудитории"))

    def addRow(self):
        record = self.model.record()
        record.remove(record.indexOf('id'))
        # record.setValue('number')
        self.model.insertRecord(-1, record)
        self.model.submitAll()


class AdapterDB:
    def __init__(self, db):
        self.db = db
        self.con = sqlite3.connect(self.db)
        self.cur = self.con.cursor()

    def select(self, content, table, *args):
        sqlReq = f"""SELECT * FROM {table}"""
        if len(args) > 0:
            conds = " and ".join(args)
            sqlReq = sqlReq + f" WHERE {conds}"
        print(sqlReq)
        return self.cur.execute(sqlReq).fetchall()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    wid = DictChange('Master.sqlite')
    wid.show()
    sys.exit(app.exec_())
# Don't mind me. I'm just an easter egg.
