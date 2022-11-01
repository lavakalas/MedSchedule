import sqlite3
import string
import sys

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox, QFileDialog
from openpyxl import load_workbook


class DictChange(QWidget):
    def __init__(self, db):
        super(DictChange, self).__init__()
        self.db = db
        self.setupUI(self)

        objList = [[self.rmodel, self.tv_Rooms, self.roomsName], [self.gmodel, self.tv_Groups, self.groupsName],
                   [self.smodel, self.tv_Subjects, self.subjectsName]]
        self.tb_AddRoom.clicked.connect(lambda: self.addRow(objList[0]))
        self.tb_AddGroup.clicked.connect(lambda: self.addRow(objList[1]))
        self.tb_AddSubject.clicked.connect(lambda: self.addRow(objList[2]))

        self.tb_DelRoom.clicked.connect(lambda: self.delRow(objList[0]))
        self.tb_DelGroup.clicked.connect(lambda: self.delRow(objList[1]))
        self.tb_DelSubject.clicked.connect(lambda: self.delRow(objList[2]))

        self.pb_ImportRooms.clicked.connect(lambda: self.load(objList[0]))
        self.pb_ImportGroups.clicked.connect(lambda: self.load(objList[1]))
        self.pb_ImportSubjects.clicked.connect(lambda: self.load(objList[2]))

    def loadModels(self):
        self.roomsName = 'rooms'  # loading rooms
        self.rmodel = QSqlTableModel(self, self.QTdb)
        self.rmodel.setTable(self.roomsName)
        self.rmodel.select()

        self.groupsName = 'groups'  # loading groups
        self.gmodel = QSqlTableModel(self, self.QTdb)
        self.gmodel.setTable(self.groupsName)
        self.gmodel.select()

        self.subjectsName = 'subjects'  # loading subjects
        self.smodel = QSqlTableModel(self, self.QTdb)
        self.smodel.setTable(self.subjectsName)
        self.smodel.select()

    def setupUI(self, Form):
        Form.setObjectName("Form")
        Form.resize(773, 611)
        self.QTdb = QSqlDatabase.addDatabase('QSQLITE')
        self.QTdb.setDatabaseName(self.db)
        self.QTdb.open()
        self.loadModels()
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
        icon.addPixmap(QtGui.QPixmap("./ui/AddIcon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tb_AddGroup.setIcon(icon)
        self.tb_AddGroup.setObjectName("tb_AddGroup")

        self.tv_Groups = QtWidgets.QTableView(self.Groups)
        self.tv_Groups.setGeometry(QtCore.QRect(10, 10, 751, 531))
        self.tv_Groups.setObjectName("tv_Groups")
        self.tv_Groups.setModel(self.gmodel)
        self.tv_Groups.hideColumn(0)

        self.tb_DelGroup = QtWidgets.QToolButton(self.Groups)
        self.tb_DelGroup.setGeometry(QtCore.QRect(50, 550, 31, 31))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("./ui/DelIcon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tb_DelGroup.setIcon(icon1)
        self.tb_DelGroup.setObjectName("tb_DelGroup")
        self.tabWidget.addTab(self.Groups, "")
        self.Subjects = QtWidgets.QWidget()
        self.Subjects.setObjectName("Subjects")

        self.tv_Subjects = QtWidgets.QTableView(self.Subjects)
        self.tv_Subjects.setGeometry(QtCore.QRect(10, 10, 751, 531))
        self.tv_Subjects.setObjectName("tv_Subjects")
        self.tv_Subjects.setModel(self.smodel)
        self.tv_Subjects.hideColumn(0)

        self.pb_ImportSubjects = QtWidgets.QPushButton(self.Subjects)
        self.pb_ImportSubjects.setGeometry(QtCore.QRect(650, 550, 111, 21))
        self.pb_ImportSubjects.setObjectName("pb_ImportSubjects")
        self.tb_AddSubject = QtWidgets.QToolButton(self.Subjects)
        self.tb_AddSubject.setGeometry(QtCore.QRect(10, 550, 31, 31))
        self.tb_AddSubject.setIcon(icon)
        self.tb_AddSubject.setObjectName("tb_AddSubject")
        self.tb_DelSubject = QtWidgets.QToolButton(self.Subjects)
        self.tb_DelSubject.setGeometry(QtCore.QRect(50, 550, 31, 31))
        self.tb_DelSubject.setIcon(icon1)
        self.tb_DelSubject.setObjectName("tb_DelSubject")
        self.tabWidget.addTab(self.Subjects, "")
        self.Rooms = QtWidgets.QWidget()
        self.Rooms.setObjectName("Rooms")

        self.tv_Rooms = QtWidgets.QTableView(self.Rooms)
        self.tv_Rooms.setGeometry(QtCore.QRect(10, 10, 751, 531))
        self.tv_Rooms.setObjectName("tv_Rooms")
        self.tv_Rooms.setModel(self.rmodel)
        self.tv_Rooms.hideColumn(0)

        self.pb_ImportRooms = QtWidgets.QPushButton(self.Rooms)
        self.pb_ImportRooms.setGeometry(QtCore.QRect(650, 550, 111, 21))
        self.pb_ImportRooms.setObjectName("pb_ImportRooms")
        self.tb_AddRoom = QtWidgets.QToolButton(self.Rooms)
        self.tb_AddRoom.setGeometry(QtCore.QRect(10, 550, 31, 31))
        self.tb_AddRoom.setIcon(icon)
        self.tb_AddRoom.setObjectName("tb_AddRoom")
        self.tb_DelRoom = QtWidgets.QToolButton(self.Rooms)
        self.tb_DelRoom.setGeometry(QtCore.QRect(50, 550, 31, 31))
        self.tb_DelRoom.setIcon(icon1)
        self.tb_DelRoom.setObjectName("tb_DelRoom")
        self.tabWidget.addTab(self.Rooms, "")

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pb_ImportGroups.setText(_translate("Form", "Import from Excel"))
        self.tb_AddGroup.setText(_translate("Form", "..."))
        self.tb_DelGroup.setText(_translate("Form", "..."))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Groups), _translate("Form", "Учебные группы"))
        self.pb_ImportSubjects.setText(_translate("Form", "Import from Excel"))
        self.tb_AddSubject.setText(_translate("Form", "..."))
        self.tb_DelSubject.setText(_translate("Form", "..."))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Subjects), _translate("Form", "Дисциплины"))
        self.pb_ImportRooms.setText(_translate("Form", "Import from Excel"))
        self.tb_AddRoom.setText(_translate("Form", "..."))
        self.tb_DelRoom.setText(_translate("Form", "..."))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Rooms), _translate("Form", "Аудитории"))

    def addRow(self, toAdd):
        print(toAdd)
        record = toAdd[0].record()
        print(toAdd[0].insertRecord(-1, record))
        toAdd[0].submitAll()
        toAdd[0].clear()
        toAdd[0].setTable(toAdd[2])
        toAdd[0].select()
        toAdd[1].selectRow(toAdd[1].model().rowCount() - 1)
        toAdd[1].hideColumn(0)

    def delRow(self, toDel):
        rows = list(set([el.row() for el in toDel[1].selectionModel().selectedIndexes()]))
        if rows:
            ask = QMessageBox
            status = ask.question(self, '', 'Вы уверены?', ask.Yes | ask.No)

            if status == ask.Yes:
                for i in rows:
                    toDel[0].deleteRowFromTable(i)
                toDel[0].submitAll()
                toDel[0].clear()
                toDel[0].setTable(toDel[2])
                toDel[0].select()
                toDel[1].selectRow(rows[0] - 1)
        toDel[1].hideColumn(0)

    def load(self, toLoadInto):
        file, status = QFileDialog.getOpenFileName()
        if status:
            print(file, status)
            record = toLoadInto[0].record()
            columns = {'rooms': ['name', 'address'],
                       'groups': ['name', 'direction', 'course'],
                       'subjects': ['name', 'teacher']}
            wb = load_workbook(file)
            ws1 = wb['Лист1']
            rc = ws1.max_row
            cc = ws1.max_column
            print(rc, cc)
            column_names = list(string.ascii_uppercase)
            record.remove(record.indexOf("id"))
            for i in range(1, rc + 1):
                for j in range(len(columns[toLoadInto[2]])):
                    target = column_names[j] + str(i)
                    record.setValue(columns[toLoadInto[2]][j], ws1[target].value)
                toLoadInto[0].insertRecord(-1, record)
                toLoadInto[0].submitAll()


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

    Dic = DictChange('test.sqlite')
    Dic.show()
    sys.exit(app.exec_())
# Don't mind me. I'm just an easter egg.
