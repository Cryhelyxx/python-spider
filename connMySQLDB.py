#-*- coding:utf-8 -*-
import os, sys, string
import MySQLdb

conn = MySQLdb.connect(host = 'localhost', user = 'root', passwd = 'admin',db = 'user')

cursor = conn.cursor()
sql = "insert into telephone(name, telephone) values ('%s', %d)" % ("Cryhelyx", 10086)

cursor.execute(sql)

sql = "select * from telephone"
cursor.execute(sql)
alldata = cursor.fetchall()

if alldata:
    for rec in alldata:
        print rec[0], rec[1]

cursor.close()

conn.close()
