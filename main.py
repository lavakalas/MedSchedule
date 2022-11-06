import string
import sys

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox, QFileDialog, QMainWindow
from openpyxl import load_workbook

from PyQt5.QtWidgets import QComboBox, QCompleter
from PyQt5.QtCore import QSortFilterProxyModel, Qt, QDate
from PyQt5.QtGui import QStandardItemModel, QStandardItem


class ExtendedCombo(QComboBox):
    def __init__(self, parent=None):
        super(ExtendedCombo, self).__init__(parent)

        self.setFocusPolicy(Qt.StrongFocus)
        self.setEditable(True)
        self.completer = QCompleter(self)

        # always show all completions
        self.completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.pFilterModel = QSortFilterProxyModel(self)
        self.pFilterModel.setFilterCaseSensitivity(Qt.CaseInsensitive)

        self.completer.setPopup(self.view())

        self.setCompleter(self.completer)

        self.lineEdit().textEdited.connect(self.pFilterModel.setFilterFixedString)
        self.completer.activated.connect(self.setTextIfCompleterIsClicked)

    def setModel(self, model):
        super(ExtendedCombo, self).setModel(model)
        self.pFilterModel.setSourceModel(model)
        self.completer.setModel(self.pFilterModel)

    def setModelColumn(self, column):
        self.completer.setCompletionColumn(column)
        self.pFilterModel.setFilterKeyColumn(column)
        super(ExtendedCombo, self).setModelColumn(column)

    def view(self):
        return self.completer.popup()

    def index(self):
        return self.currentIndex()

    def setTextIfCompleterIsClicked(self, text):
        if text:
            index = self.findText(text)
            self.setCurrentIndex(index)


class ScheduleEditor(QMainWindow):
    # noinspection PyUnresolvedReferences
    def __init__(self):
        super(ScheduleEditor, self).__init__()
        self.init_DB('Master.sqlite')
        self.setupUi(self)
        self.sw = DictChange('Master.sqlite')
        self.action.triggered.connect(self.show_editor)

        self.non_repeating = [self.lbl_Date, self.dE_Single]
        self.chB_DotW = [self.chB_Mo, self.chB_Tu, self.chB_We, self.chB_Th, self.chB_Fr, self.chB_Sa]
        self.repeating = [self.lbl_DotW, self.lbl_Mo, self.lbl_Tu, self.lbl_We, self.lbl_Th, self.lbl_Fr, self.lbl_Sa,
                          self.lbl_Dates, self.lbl_DashBD, self.dE_RepeatStart, self.dE_RepeatEnd] + self.chB_DotW
        self.rB_Single.clicked.connect(self.repeat_choice)
        self.rB_Repeat.clicked.connect(self.repeat_choice)

        for el in self.get_info('groups'):
            self.cB_Group.addItem(str(el[0]))
        for el in self.get_info('rooms'):
            self.cB_Venue.addItem(str(el[0]))
        for el in self.get_info('subjects'):
            self.cB_Subject.addItem(str(el[0]))

    @staticmethod
    def init_DB(db):
        import sqlite3
        con = sqlite3.connect(db)
        cur = con.cursor()

        auditorium = """CREATE TABLE IF NOT EXISTS rooms("id" INTEGER  PRIMARY KEY AUTOINCREMENT UNIQUE, "name" TEXT, 
        "address" TEXT)"""
        groups = """CREATE TABLE IF NOT EXISTS "groups"("id" INTEGER  PRIMARY KEY AUTOINCREMENT UNIQUE,"name" TEXT, 
        "direction"	TEXT, 
        "course" INTEGER )"""
        schedule = """CREATE TABLE IF NOT EXISTS "schedule"("id" INTEGER  PRIMARY KEY AUTOINCREMENT UNIQUE,"group"	TEXT , 
        "subject" TEXT , 
        "auditorium" TEXT , 
        "date_start" TEXT , 
        "date_end" TEXT, 
        "time_start" TEXT , 
        "time_end" TEXT )"""
        subject = """CREATE TABLE IF NOT EXISTS "subjects"("id" INTEGER  PRIMARY KEY AUTOINCREMENT UNIQUE,"name" TEXT , 
        "teacher" TEXT )"""

        cur.execute(auditorium)
        cur.execute(groups)
        cur.execute(schedule)
        cur.execute(subject)
        con.commit()

        con.close()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(480, 190)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lbl_Dates = QtWidgets.QLabel(self.centralwidget)
        self.lbl_Dates.setEnabled(False)
        self.lbl_Dates.setGeometry(QtCore.QRect(240, 120, 47, 21))
        self.lbl_Dates.setObjectName("lbl_Dates")
        self.cB_Subject = ExtendedCombo(self.centralwidget)
        self.cB_Subject.setGeometry(QtCore.QRect(140, 35, 60, 19))
        self.cB_Subject.setObjectName("cB_Subject")
        self.dE_RepeatEnd = QtWidgets.QDateEdit(self.centralwidget)
        self.dE_RepeatEnd.setEnabled(False)
        self.dE_RepeatEnd.setGeometry(QtCore.QRect(390, 120, 81, 22))
        self.dE_RepeatEnd.setObjectName("dE_RepeatEnd")
        self.chB_Th = QtWidgets.QCheckBox(self.centralwidget)
        self.chB_Th.setEnabled(False)
        self.chB_Th.setGeometry(QtCore.QRect(380, 80, 16, 21))
        self.chB_Th.setText("")
        self.chB_Th.setObjectName("chB_Th")
        self.lbl_Sa = QtWidgets.QLabel(self.centralwidget)
        self.lbl_Sa.setEnabled(False)
        self.lbl_Sa.setGeometry(QtCore.QRect(420, 100, 47, 16))
        self.lbl_Sa.setObjectName("lbl_Sa")
        self.cB_Venue = ExtendedCombo(self.centralwidget)
        self.cB_Venue.setGeometry(QtCore.QRect(140, 60, 60, 19))
        self.cB_Venue.setObjectName("cB_Venue")
        self.lbl_Tu = QtWidgets.QLabel(self.centralwidget)
        self.lbl_Tu.setEnabled(False)
        self.lbl_Tu.setGeometry(QtCore.QRect(340, 100, 47, 16))
        self.lbl_Tu.setObjectName("lbl_Tu")
        self.lbl_Subject = QtWidgets.QLabel(self.centralwidget)
        self.lbl_Subject.setGeometry(QtCore.QRect(10, 36, 98, 20))
        self.lbl_Subject.setObjectName("lbl_Subject")
        self.lbl_Time = QtWidgets.QLabel(self.centralwidget)
        self.lbl_Time.setGeometry(QtCore.QRect(10, 90, 47, 21))
        self.lbl_Time.setObjectName("lbl_Time")
        self.lbl_Date = QtWidgets.QLabel(self.centralwidget)
        self.lbl_Date.setGeometry(QtCore.QRect(240, 30, 47, 21))
        self.lbl_Date.setObjectName("lbl_Date")
        self.lbl_We = QtWidgets.QLabel(self.centralwidget)
        self.lbl_We.setEnabled(False)
        self.lbl_We.setGeometry(QtCore.QRect(360, 100, 47, 16))
        self.lbl_We.setObjectName("lbl_We")
        self.cB_Group = QtWidgets.QComboBox(self.centralwidget)
        self.cB_Group.setGeometry(QtCore.QRect(140, 10, 60, 19))
        self.cB_Group.setObjectName("cB_Group")
        self.rB_Single = QtWidgets.QRadioButton(self.centralwidget)
        self.rB_Single.setEnabled(True)
        self.rB_Single.setGeometry(QtCore.QRect(220, 0, 101, 31))
        self.rB_Single.setAutoFillBackground(False)
        self.rB_Single.setChecked(True)
        self.rB_Single.setObjectName("rB_Single")
        self.lbl_Fr = QtWidgets.QLabel(self.centralwidget)
        self.lbl_Fr.setEnabled(False)
        self.lbl_Fr.setGeometry(QtCore.QRect(400, 100, 47, 16))
        self.lbl_Fr.setObjectName("lbl_Fr")
        self.lbl_DashBT = QtWidgets.QLabel(self.centralwidget)
        self.lbl_DashBT.setGeometry(QtCore.QRect(130, 90, 47, 20))
        self.lbl_DashBT.setObjectName("lbl_DashBT")
        self.chB_Tu = QtWidgets.QCheckBox(self.centralwidget)
        self.chB_Tu.setEnabled(False)
        self.chB_Tu.setGeometry(QtCore.QRect(340, 80, 16, 21))
        self.chB_Tu.setText("")
        self.chB_Tu.setObjectName("chB_Tu")
        self.lbl_Group = QtWidgets.QLabel(self.centralwidget)
        self.lbl_Group.setGeometry(QtCore.QRect(10, 10, 98, 21))
        self.lbl_Group.setObjectName("lbl_Group")
        self.dE_RepeatStart = QtWidgets.QDateEdit(self.centralwidget)
        self.dE_RepeatStart.setEnabled(False)
        self.dE_RepeatStart.setGeometry(QtCore.QRect(280, 120, 81, 22))
        self.dE_RepeatStart.setObjectName("dE_RepeatStart")
        self.chB_Fr = QtWidgets.QCheckBox(self.centralwidget)
        self.chB_Fr.setEnabled(False)
        self.chB_Fr.setGeometry(QtCore.QRect(400, 80, 16, 21))
        self.chB_Fr.setText("")
        self.chB_Fr.setObjectName("chB_Fr")
        self.lbl_Venue = QtWidgets.QLabel(self.centralwidget)
        self.lbl_Venue.setGeometry(QtCore.QRect(10, 60, 98, 21))
        self.lbl_Venue.setObjectName("lbl_Venue")
        self.dE_Single = QtWidgets.QDateEdit(self.centralwidget)
        self.dE_Single.setGeometry(QtCore.QRect(280, 30, 81, 22))
        self.dE_Single.setObjectName("dE_Single")
        self.rB_Repeat = QtWidgets.QRadioButton(self.centralwidget)
        self.rB_Repeat.setGeometry(QtCore.QRect(220, 50, 91, 31))
        self.rB_Repeat.setObjectName("rB_Repeat")
        self.lbl_DotW = QtWidgets.QLabel(self.centralwidget)
        self.lbl_DotW.setEnabled(False)
        self.lbl_DotW.setGeometry(QtCore.QRect(240, 82, 81, 31))
        self.lbl_DotW.setObjectName("lbl_DotW")
        self.chB_We = QtWidgets.QCheckBox(self.centralwidget)
        self.chB_We.setEnabled(False)
        self.chB_We.setGeometry(QtCore.QRect(360, 80, 16, 21))
        self.chB_We.setText("")
        self.chB_We.setObjectName("chB_We")
        self.tE_End = QtWidgets.QTimeEdit(self.centralwidget)
        self.tE_End.setGeometry(QtCore.QRect(150, 90, 61, 22))
        self.tE_End.setObjectName("tE_End")
        self.tE_Start = QtWidgets.QTimeEdit(self.centralwidget)
        self.tE_Start.setGeometry(QtCore.QRect(60, 90, 61, 22))
        self.tE_Start.setObjectName("tE_Start")
        self.lbl_DashBD = QtWidgets.QLabel(self.centralwidget)
        self.lbl_DashBD.setEnabled(False)
        self.lbl_DashBD.setGeometry(QtCore.QRect(370, 120, 16, 20))
        self.lbl_DashBD.setObjectName("lbl_DashBD")
        self.lbl_Th = QtWidgets.QLabel(self.centralwidget)
        self.lbl_Th.setEnabled(False)
        self.lbl_Th.setGeometry(QtCore.QRect(380, 100, 47, 16))
        self.lbl_Th.setObjectName("lbl_Th")
        self.chB_Mo = QtWidgets.QCheckBox(self.centralwidget)
        self.chB_Mo.setEnabled(False)
        self.chB_Mo.setGeometry(QtCore.QRect(320, 80, 31, 21))
        self.chB_Mo.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.chB_Mo.setText("")
        self.chB_Mo.setObjectName("chB_Mo")
        self.chB_Sa = QtWidgets.QCheckBox(self.centralwidget)
        self.chB_Sa.setEnabled(False)
        self.chB_Sa.setGeometry(QtCore.QRect(420, 80, 16, 21))
        self.chB_Sa.setText("")
        self.chB_Sa.setObjectName("chB_Sa")
        self.lbl_Mo = QtWidgets.QLabel(self.centralwidget)
        self.lbl_Mo.setEnabled(False)
        self.lbl_Mo.setGeometry(QtCore.QRect(320, 100, 16, 16))
        self.lbl_Mo.setObjectName("lbl_Mo")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 480, 21))
        self.menubar.setObjectName("menubar")
        self.EditGuides = QtWidgets.QMenu(self.menubar)
        self.EditGuides.setObjectName("EditGuides")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action = QtWidgets.QAction(MainWindow)
        self.action.setObjectName("action")
        self.EditGuides.addAction(self.action)
        self.menubar.addAction(self.EditGuides.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.lbl_Dates.setText(_translate("MainWindow", "Даты:"))
        self.lbl_Sa.setText(_translate("MainWindow", "Сб"))
        self.lbl_Tu.setText(_translate("MainWindow", "Вт"))
        self.lbl_Subject.setText(_translate("MainWindow", "Дисциплина:"))
        self.lbl_Time.setText(_translate("MainWindow", "Время:"))
        self.lbl_Date.setText(_translate("MainWindow", "Дата:"))
        self.lbl_We.setText(_translate("MainWindow", "Ср"))
        self.rB_Single.setText(_translate("MainWindow", "Не повторяется"))
        self.lbl_Fr.setText(_translate("MainWindow", "Пт"))
        self.lbl_DashBT.setText(_translate("MainWindow", "—"))
        self.lbl_Group.setText(_translate("MainWindow", "Учебная группа:"))
        self.lbl_Venue.setText(_translate("MainWindow", "Место проведения:"))
        self.rB_Repeat.setText(_translate("MainWindow", "Повторяется"))
        self.lbl_DotW.setText(_translate("MainWindow", "День недели:"))
        self.lbl_DashBD.setText(_translate("MainWindow", "—"))
        self.lbl_Th.setText(_translate("MainWindow", "Чт"))
        self.lbl_Mo.setText(_translate("MainWindow", "Пн"))
        self.EditGuides.setTitle(_translate("MainWindow", "File"))
        self.action.setText(_translate("MainWindow", "Редактировать справочники"))

    def show_editor(self):
        self.sw.show()

    def get_info(self, table):
        return self.sw.get_info(table)

    def repeat_choice(self):
        flag = self.rB_Repeat.isChecked()
        self.dE_Single.setDate(QDate(2000, 1, 1))
        self.dE_RepeatStart.setDate(QDate(2000, 1, 1))
        self.dE_RepeatEnd.setDate(QDate(2000, 1, 1)) # просто дефолтные даты
        for el in self.chB_DotW:
            el.setChecked(False)
        for el in self.repeating:
            el.setEnabled(flag)
        for el in self.non_repeating:
            el.setEnabled(not flag)


class DictChange(QWidget):
    smodel: QSqlTableModel
    subjectsName: str
    gmodel: QSqlTableModel
    groupsName: str
    rmodel: QSqlTableModel
    roomsName: str

    # noinspection PyUnresolvedReferences
    def __init__(self, db):
        super(DictChange, self).__init__()
        self.columns = {'rooms': ['name', 'address'],
                       'groups': ['name', 'direction', 'course'],
                       'subjects': ['name', 'teacher']}
        self.db = db
        self.setupUI(self)

        obj_list = [[self.rmodel, self.tv_Rooms, self.roomsName], [self.gmodel, self.tv_Groups, self.groupsName],
                    [self.smodel, self.tv_Subjects, self.subjectsName]]
        self.tb_AddRoom.clicked.connect(lambda: self.addRow(obj_list[0]))
        self.tb_AddGroup.clicked.connect(lambda: self.addRow(obj_list[1]))
        self.tb_AddSubject.clicked.connect(lambda: self.addRow(obj_list[2]))

        self.tb_DelRoom.clicked.connect(lambda: self.delRow(obj_list[0]))
        self.tb_DelGroup.clicked.connect(lambda: self.delRow(obj_list[1]))
        self.tb_DelSubject.clicked.connect(lambda: self.delRow(obj_list[2]))

        self.pb_ImportRooms.clicked.connect(lambda: self.load(obj_list[0]))
        self.pb_ImportGroups.clicked.connect(lambda: self.load(obj_list[1]))
        self.pb_ImportSubjects.clicked.connect(lambda: self.load(obj_list[2]))

    def load_models(self):
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
        self.load_models()
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

    def closeEvent(self, event):  # TODO: размножить для остальных таблиц
        reply = QMessageBox.No
        query = QSqlQuery()
        query.exec("SELECT RowNum from "
                   "(SELECT ROW_NUMBER () OVER (ORDER BY id) RowNum, name, address FROM rooms)"
                   " WHERE name IS NULL or address IS NULL or name = '' or address = ''")
        query.first()
        roomsNULL = query.value(0)
        if roomsNULL is not None:
            alert = QMessageBox.information(self, 'Ошибка сохранения', 'Остались незаполненные данные')
            self.tv_Rooms.selectRow(roomsNULL - 1)
            self.tabWidget.setCurrentIndex(2)
        else:
            reply = QMessageBox.question(self, 'Закрыть', 'Закрыть редактор справочников и сохранить изменения?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()

        else:
            event.ignore()

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

    @staticmethod
    def addRow(toAdd):
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
            wb = load_workbook(file)
            ws1 = wb['Лист1']
            rc = ws1.max_row
            cc = ws1.max_column
            print(rc, cc)
            column_names = list(string.ascii_uppercase)
            record.remove(record.indexOf("id"))
            for i in range(1, rc + 1):
                for j in range(len(self.columns[toLoadInto[2]])):
                    target = column_names[j] + str(i)
                    record.setValue(self.columns[toLoadInto[2]][j], ws1[target].value)
                toLoadInto[0].insertRecord(-1, record)
                toLoadInto[0].submitAll()

    @staticmethod
    def get_info(table):
        lengths = {'rooms': 2,
                   'groups': 3,
                   'subjects': 2}
        out = list()
        query = QSqlQuery()
        query.exec(f"SELECT COUNT(*) FROM {table}")
        query.first()
        count = query.value(0)
        # print(count)
        query.exec(f'SELECT * FROM {table}')
        query.first()
        out.append([query.value(i) for i in range(1, lengths[table] + 1)])
        for _ in range(1, count):
            query.next()
            out.append([query.value(i) for i in range(1, lengths[table] + 1)])
        return out


if __name__ == '__main__':
    app = QApplication(sys.argv)

    Schedule = ScheduleEditor()
    Schedule.show()
    sys.exit(app.exec_())
# Don't mind me. I'm just an easter egg.
