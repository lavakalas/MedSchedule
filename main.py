import sqlite3
from pprint import pprint


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
    RoomsDB = AdapterDB("Rooms.db")
    pprint(RoomsDB.get_all_from('rooms'))

    con = sqlite3.connect("Rooms.db")
    cur = con.cursor()

    sql = """CREATE TABLE IF NOT EXISTS rooms("id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, "number" int)"""
    cur.execute(sql)

    cur.execute("""DELETE FROM rooms""")  # Очищает существующую таблицу

    cur.execute("""DELETE FROM sqlite_sequence WHERE name = "rooms" """)  # обнуляет счётчик для id (автоинкременция)

    sql1 = "INSERT INTO rooms(number) VALUES"  # заготовка для вставления новых значений
    for i in range(101, 201):
        sql1 += f"({i}), "
    else:
        sql1 = sql1[:-2]  # создание полного запроса
    cur.execute(sql1)

    con.commit()
    con.close()

# Don't mind me. I'm just an easter egg.
