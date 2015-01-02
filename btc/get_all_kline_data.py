#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# FileName: get_trade_data.py

import urllib2
import json
import time
import csv
import sys

sys.setrecursionlimit(1000000) #例如这里设置为一百万, 解决RuntimeError: maximum recursion depth exceeded在网上查了，发现python默认的递归深度是很有限的，大概是900多的样子，当递归深度超过这个值的时候，就会引发这样的一个异常。
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
    with open('all_kline_data.csv', 'wb') as csvfile:
        # spamwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter = csv.writer(csvfile, dialect='excel')
        firsttime = alldata[0]['date_ms']
        lasttime = firsttime + 60 * 1000
        # record_container = []      # record_container用来装载每1min内的所有记录
        price_container = []      # price_container用来装载每1min内的所有记录的price
        record = []         # record 表示一根K线(在1min内)
        alldata_len = len(alldata)
        print alldata_len
        counter = 0
        for data in alldata:
            counter += 1
            if (data['date_ms'] >= firsttime and data['date_ms'] < lasttime):
                # print(type(data['price']))
                price_container.append(data['price'])
                # record_container.extend(data)
                if counter == alldata_len:       # 最后1min内的K线记录(未达到1min按1min计)
                    timestamp = time.localtime(firsttime/1000)
                    record_date = time.strftime("%Y-%m-%d", timestamp)
                    record_time = time.strftime("%H:%M:%S", timestamp)
                    record_openprice = price_container[0]
                    record_closeprice = price_container[-1]
                    record_hightprice = get_max_value(price_container)
                    record_lowprice = get_min_value(price_container)
                    record_volume = get_volume(price_container)
                    record_number = len(price_container)

                    record.append(record_date)
                    record.append(record_time)
                    record.append(record_openprice)
                    record.append(record_hightprice)
                    record.append(record_lowprice)
                    record.append(record_closeprice)
                    record.append(record_volume)
                    record.append(record_number)

                    spamwriter.writerow([record[0]] + [record[1]] + [record[2]] + [record[3]] + [record[4]] + [record[5]] + [record[6]] + [record[7]])
                    result = "%s, %s, %s, %s, %s, %s, %s, %s" % (record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7])
                    print result
                    # price_container = []    # 清空list
                    del price_container[:]      # 清空list
                    del record[:]
            elif price_container:
                timestamp = time.localtime(firsttime/1000)
                record_date = time.strftime("%Y-%m-%d", timestamp)
                record_time = time.strftime("%H:%M:%S", timestamp)
                # print price_container
                # print(len(price_container))
                record_openprice = price_container[0]
                record_closeprice = price_container[-1]
                record_hightprice = get_max_value(price_container)
                record_lowprice = get_min_value(price_container)
                record_volume = get_volume(price_container)
                record_number = len(price_container)

                record.append(record_date)
                record.append(record_time)
                record.append(record_openprice)
                record.append(record_hightprice)
                record.append(record_lowprice)
                record.append(record_closeprice)
                record.append(record_volume)
                record.append(record_number)

                spamwriter.writerow([record[0]] + [record[1]] + [record[2]] + [record[3]] + [record[4]] + [record[5]] + [record[6]] + [record[7]])
                result = "%s, %s, %s, %s, %s, %s, %s, %s" % (record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7])
                print result

                firsttime = lasttime
                lasttime = firsttime + 60 * 1000
                # price_container = []    # 清空list
                del price_container[:]      # 清空list
                del record[:]
            else:
                firsttime = lasttime
                lasttime = firsttime + 60 * 1000
                continue



                # spamwriter.writerow([data['amount']] + [data['date']] + [data['date_ms']] + [data['price']] + [data['tid']] + [data['type']])


def get_max_value(my_list):
    max_value = my_list[0]
    for i in my_list:
        if i > max_value:
            max_value = i
    return max_value


def get_min_value(my_list):
    min_value = my_list[0]
    for i in my_list:
        if i < min_value:
            min_value = i
    return min_value


def get_volume(my_list):
    counter = 0.0
    for i in my_list:
        # print(type(i))
        counter += float(i)
    return counter


if __name__ == '__main__':
    get_last_data(0)        # 通过递归获取所有成交记录
    output_data_to_csv()    # 获取每1min的K线数据并导出为csv文件
    del alldata[:]          # 清空list