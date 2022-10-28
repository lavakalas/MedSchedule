import sqlite3
import sys
from pprint import pprint

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtWidgets import QWidget, QApplication


class DictChange(QWidget,):
    def __init__(self, db):
        super(DictChange, self).__init__()
        self.db = db
        self.setupUi(self)

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
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.Groups)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(9, 9, 761, 561))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.tv_Groups = QtWidgets.QTableView(self.horizontalLayoutWidget)

        self.tv_Groups.setObjectName("tv_Groups")
        self.horizontalLayout.addWidget(self.tv_Groups)
        self.tv_Groups.setModel(self.model)

        self.tabWidget.addTab(self.Groups, "")
        self.Subjects = QtWidgets.QWidget()
        self.Subjects.setObjectName("Subjects")
        self.tabWidget.addTab(self.Subjects, "")
        self.Rooms = QtWidgets.QWidget()
        self.Rooms.setObjectName("Rooms")
        self.tabWidget.addTab(self.Rooms, "")

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Groups), _translate("Form", "Учебные группы"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Subjects), _translate("Form", "Дисциплины"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Rooms), _translate("Form", "Аудитории"))


class AdapterDB:
    def __init__(self, db):
        self.db = db
        self.con = sqlite3.connect(self.db)
        self.cur = self.con.cursor()

    def get_all_from(self, table):
        sqlReq = f"""SELECT * FROM {table}"""
        return self.cur.execute(sqlReq).fetchall()

    def get_selective(self, table, condition):
        sqlReq = f"""SELECT * FROM {table} WHERE {condition}"""
        return self.cur.execute(sqlReq).fetchall()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    wid = DictChange('Master.db')
    wid.show()
    sys.exit(app.exec_())
# Don't mind me. I'm just an easter egg.
