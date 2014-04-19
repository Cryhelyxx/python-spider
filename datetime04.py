#! /usr/bin/python
#-*- coding: utf-8 -*-
#filename: datetime03.py
"""
    python获取网络时间和本地时间
"""
import httplib
import datetime, calendar
import logging
import time
import os

#获取网络时间
def getBeijinTime():
 """
　　 获取北京时间
 """
 try:
     conn = httplib.HTTPConnection("www.beijing-time.org")
     conn.request("GET", "/time.asp")
     response = conn.getresponse()
     print response.status, response.reason
     if response.status == 200:
         #解析响应的消息
         result = response.read()
         logging.debug(result)
         data = result.split("\r\n")
         year = data[1][len("nyear")+1 : len(data[1])-1]
         month = data[2][len("nmonth")+1 : len(data[2])-1]
         day = data[3][len("nday")+1 : len(data[3])-1]
         #wday = data[4][len("nwday")+1 : len(data[4])-1]
         hrs = data[5][len("nhrs")+1 : len(data[5])-1]
         minute = data[6][len("nmin")+1 : len(data[6])-1]
         sec = data[7][len("nsec")+1 : len(data[7])-1]
           
         beijinTimeStr = "%s/%s/%s %s:%s:%s" % (year, month, day, hrs, minute, sec)
         beijinTime = time.strptime(beijinTimeStr, "%Y/%m/%d %X")
         return beijinTime
 except:
     logging.exception("getBeijinTime except")
     return None

#同步本地系统时间
def syncLocalTime():
 """
 	同步本地时间
 """
 logging.info("current local time is: %d-%d-%d %d:%d:%d" % time.localtime()[:6])
   
 beijinTime = getBeijinTime()
 if beijinTime is None:
     logging.info("get beijinTime is None, will try again in 30 seconds...")
     timer = threading.Timer(30.0, syncLocalTime)
     timer.start();
 else:
     logging.info("get beijinTime is: %d-%d-%d %d:%d:%d" % beijinTime[:6])
           
     tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec = beijinTime[:6]
     os.system("date %d-%d-%d" % (tm_year, tm_mon, tm_mday))     #设置日期
     os.system("time %d:%d:%d.0" % (tm_hour, tm_min, tm_sec))    #设置时间
     logging.info("syncLocalTime complete, current local time: %d-%d-%d %d:%d:%d \n" % time.localtime()[:6])

#python主函数
if __name__ == '__main__':
	getBeijinTime()
	syncLocalTime()
