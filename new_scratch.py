import sqlite3

con = sqlite3.connect("test.sqlite")
cur = con.cursor()

auditorium = """CREATE TABLE IF NOT EXISTS rooms("id" INTEGER  PRIMARY KEY AUTOINCREMENT UNIQUE, "name" TEXT, 
"address" TEXT)"""
groups = """CREATE TABLE IF NOT EXISTS "groups"("id" INTEGER  PRIMARY KEY AUTOINCREMENT UNIQUE,"name" TEXT UNIQUE, 
"direction"	TEXT, 
"course" INTEGER )"""
schedule = """CREATE TABLE IF NOT EXISTS "schedule"("id" INTEGER  PRIMARY KEY AUTOINCREMENT UNIQUE,"group"	TEXT , 
"subject" TEXT , 
"auditorium" TEXT , 
"date_start" TEXT , 
"date_end" TEXT, 
"time_start" TEXT , 
"time_end" TEXT )"""
subject = """CREATE TABLE IF NOT EXISTS "subject"("id" INTEGER  PRIMARY KEY AUTOINCREMENT UNIQUE,"name" TEXT , 
"teacher" TEXT )"""

cur.execute(auditorium)
cur.execute(groups)
cur.execute(schedule)
cur.execute(subject)
con.commit()

con.close()
