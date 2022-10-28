import sqlite3

con = sqlite3.connect("Master.sqlite")
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
