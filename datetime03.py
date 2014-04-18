#! /usr/bin/python
#-*- coding: utf-8 -*-
#file: datetime03.py
"""
	计算上一个的时间
"""
#引入datetime,calendar两个模块
import datetime,calendar
  
last_friday = datetime.date.today() 
oneday = datetime.timedelta(days = 1) 
    
while last_friday.weekday() != calendar.FRIDAY: 
    last_friday -= oneday 
    
print(last_friday.strftime('%A, %d-%b-%Y'))
