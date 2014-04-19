#-*- coding: utf-8 -*-
#file: connMySQLDB.py
import os, sys, string
import MySQLdb #导入MySQLdb模块

conn = MySQLdb.connect(
	host = 'localhost',       #连接到数据库， 服务器为本机 
	user = 'root',            #用户名为root
	passwd = 'admin',         #密码为admin
	db = 'user')              #数据库名为user

cursor = conn.cursor()        #获取数据库游标
#sql插入语句
sql = "insert into telephone(name, telephone) values ('%s', %d)" % ("Cryhelyx", 10086)

cursor.execute(sql)           #执行sql插入语句
#sql查询语句
sql = "select * from telephone"
cursor.execute(sql)           #执行sql查询语句
alldata = cursor.fetchall()   #接收全部的返回结果行
#打印每条记录行
if alldata:
    for rec in alldata:
        print rec[0], rec[1]
#关闭数据库连接, 需要分别的关闭指针对象和连接对象
cursor.close()                #关闭游标
conn.close()                  #关闭数据库
