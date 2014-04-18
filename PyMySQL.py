#-*- coding: utf-8 -*-
#file: PyMySQL.py

import MySQLdb      #导入MySQLdb模块
conn = MySQLdb.connect(
        host = 'localhost',     #连接到数据库， 服务器为本机 
        user = 'root',          #用户名为root
        passwd = 'admin',       #密码为admin
        db = 'python',          #数据库名为python
        unix_socket = '/tmp/mysql.sock')   #指定Unix socket的位置
cur = conn.cursor()               #获取数据库游标
cur.execute('insert into people(name, age, sex) values(\'Jee\', 21, \'F\')')    #执行SQL语句， 添加记录
conn.commit()                   #提交事务
r = cur.execute('SELECT * FROM people')     #执行SQL语句， 获取记录
r = cur.fetchall()              #获取数据
print r                         #输入数据
cur.close()                     #关闭游标
conn.close()                    #关闭数据库
