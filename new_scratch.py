import sqlite3

con = sqlite3.connect("test.sqlite")
cur = con.cursor()

auditorium = """CREATE TABLE IF NOT EXISTS rooms("name" TEXT, 
"address" TEXT)"""
groups = """CREATE TABLE IF NOT EXISTS "groups"("name" TEXT NOT NULL UNIQUE PRIMARY KEY, 
"direction"	TEXT NOT NULL, 
"course" INTEGER NOT NULL)"""
schedule = """CREATE TABLE IF NOT EXISTS "schedule"("group"	TEXT NOT NULL, 
"subject" TEXT NOT NULL, 
"auditorium" TEXT NOT NULL, 
"date_start" TEXT NOT NULL, 
"date_end" TEXT, 
"time_start" TEXT NOT NULL, 
"time_end" TEXT NOT NULL)"""
subject = """CREATE TABLE IF NOT EXISTS "subject"("name" TEXT NOT NULL, 
"teacher" TEXT NOT NULL)"""

cur.execute(auditorium)
cur.execute(groups)
cur.execute(schedule)
cur.execute(subject)
con.commit()

con.close()
