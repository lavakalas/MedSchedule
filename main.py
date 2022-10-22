import sqlite3


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
