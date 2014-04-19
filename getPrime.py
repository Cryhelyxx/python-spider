#! /usr/bin/python
#-*- coding: utf-8 -*-
#filename: getPrime.py
"""
    用python求第1000个质数的值
"""
def getprim(n):
 #我们从3开始，提升效率，呵呵，微乎其微啦
    p = 3
    x = 0       #x表示质数计数器
    #中止循环的条件是：质数计数器达到1000
    while(x < n):
        result = True
        #如果不是质数， 标记为False
        for i in range(2, p-1):
            if(p % i == 0):
                result = False
        #如果是质数， 标记为Ture， 并且质数计数器加1， 结果值记作p
        if result == True:
            x +=  1
            rst = p
        #注意:这里加2是为了提升效率，因为能被双数肯定不是质数。
        p += 2
    print(rst)

#python主函数
if __name__ == '__main__':
    #调用函数
    getprim(1000)
