#!/usr/bin/python
#-*- coding: utf-8 -*-
#filename: func_default.py
"""
    对于一些函数，你可能希望它的一些参数是可选的，
    如果用户不想要为这些参数提供值的话，这些参数就使用默认值。
    这个功能借助于默认参数值完成。
    你可以在函数定义的形参名后加上赋值运算符（=）和默认值，
    从而给形参指定默认参数值
"""
def say(message, times = 1):
    print message * times

say('Hello')
say('World', 5)
