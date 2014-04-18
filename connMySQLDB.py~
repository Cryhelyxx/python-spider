
import os, sys, string
import MySQLdb

con=MySQLdb.connect(host='localhost',user='root',passwd='admin',db='user')

cursor = con.cursor()
sql = "insert into telephone(name, telephone) values ('%s', %d)" % ("fei", 13826442877)

cursor.execute(sql)

sql = "select * from telephone"
cursor.execute(sql)
alldata = cursor.fetchall()

if alldata:
    for rec in alldata:
        print rec[0], rec[1]

cursor.close()

con.close()