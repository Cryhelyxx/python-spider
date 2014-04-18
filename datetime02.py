#! /usr/bin/env python
#coding=utf-8
"""
	借助模运算，可以一次算出需要减去的天数，计算上一个星期五
"""
#同样引入datetime,calendar两个模块
import datetime 
import calendar 
    
today = datetime.date.today() 
target_day = calendar.FRIDAY 
this_day = today.weekday() 
delta_to_target = (this_day - target_day) % 7
last_friday = today - datetime.timedelta(days = delta_to_target) 
    
print(last_friday.strftime("%d-%b-%Y"))