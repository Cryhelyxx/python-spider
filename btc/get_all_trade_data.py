#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# FileName: get_trade_data.py

import urllib2
import json
import time
import csv
import sys

sys.setrecursionlimit(1000000) #例如这里设置为一百万  
alldata = []


def http_get(tid):          # 获取OKCoin期货交易记录信息的json数据
    #数据源
    url = 'https://www.okcoin.com/api/v1/trades.do?symbol=btc_usd&since=%d' % tid
    #伪装浏览器抓取网页数据
    headers = {
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/33.0.1750.152 Chrome/33.0.1750.152 Safari/537.36'}
    req = urllib2.Request(url, headers=headers)
    # response = urllib2.urlopen(url)
    # response = urllib2.urlopen(req)
    # response = urllib2.urlopen(req, timeout=15)
    # result = response.read()
    # return result
    
    try:
        response = urllib2.urlopen(req, data=None, timeout=60)
        result = response.read()
        return result
    except urllib2.URLError, e:
        print '网络异常， 连接超时.'
        print e.reason
        # return None


def get_final_tid(since_tid):       # 取得最早的成交数据， 然后将返回结果中最后的tid数据传递给since参数
    retdata = http_get(since_tid)
    ddata = json.loads(retdata)     # 由json字符串转为列表
    if ddata:
        return ddata[-1]['tid']
    else:
        return -1


def get_last_data(since_tid):           # 获取新一批成交数据
    if since_tid == -1:
        return
    retdata = http_get(since_tid)
    ddata = json.loads(retdata)
    alldata.extend(ddata)
    for onedata in ddata:
        timestamp = time.localtime(onedata['date'])
        timestr = time.strftime("%Y-%m-%d %H:%M:%S", timestamp)
        content = "%s, %s, %s, %s, %s" % (onedata['amount'], timestr, onedata['price'], onedata['tid'], onedata['type'])
        print content
    
    final_tid = get_final_tid(since_tid)
    get_last_data(final_tid)


def output_data_to_csv():
    with open('all_trave_data.csv', 'wb') as csvfile:
        # spamwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter = csv.writer(csvfile, dialect='excel')
        for data in alldata:
            spamwriter.writerow([data['amount']] + [data['date']] + [data['date_ms']] + [data['price']] + [data['tid']] + [data['type']])


if __name__ == '__main__':
    get_last_data(0)
    output_data_to_csv()