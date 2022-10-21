import sqlite3

con = sqlite3.connect("Rooms.db")
cur = con.cursor()
sql = """CREATE TABLE IF NOT EXISTS rooms("id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, "number" int)"""
cur.execute(sql)
cur.execute("""DELETE FROM rooms""")
cur.execute("""DELETE FROM sqlite_sequence WHERE name = "rooms" """)
sql1 = "INSERT INTO rooms(number) VALUES"
for i in range(101, 201):
    sql1 += f"({i}), "
else:
    sql1 = sql1[:-2]
cur.execute(sql1)
con.commit()

con.close()
