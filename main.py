import sqlite3
import excel
from pprint import pprint

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtWidgets import QWidget, QApplication


class DictChange(QWidget):
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

    def select(self, content, table, *args):
        sqlReq = f"""SELECT * FROM {table}"""
        if len(args) > 0:
            conds = " and ".join(args)
            sqlReq = sqlReq + f" WHERE {conds}"
        print(sqlReq)
        return self.cur.execute(sqlReq).fetchall()



if __name__ == '__main__':
    ADB = AdapterDB('Master.sqlite')
    pprint(ADB.select('*', 'rooms', 'id <= 10 or id >= 40'))
    # app = QApplication(sys.argv)
    #
    # wid = DictChange('Master.sqlite')
    # wid.show()
    # sys.exit(app.exec_())
# Don't mind me. I'm just an easter egg.
