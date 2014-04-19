#-*- coding: utf-8 -*-
#filename: getcontent.py

"""
    抓取文章正文标题及正文内容
"""

import re
import urllib2
import bs4
from bs4 import BeautifulSoup

import sys
reload(sys)
sys.setdefaultencoding('utf8')



#1. 抓取网页数据
def getContent(filename1):
	#数据源
	url = 'http://www.cnblogs.com/shendiao/p/3254552.html'
	#伪装浏览器抓取网页数据
	headers = {
	'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/33.0.1750.152 Chrome/33.0.1750.152 Safari/537.36'}
	req = urllib2.Request(url, headers=headers)
	fp = urllib2.urlopen(req)
	op = open(filename1, "wb")
	while 1:
	    s = fp.read(8192)
	    if not s:
	        break
	    op.write(s)
	fp.close()

#2. 往终端打印正文标题及内容   
def printContent(filename1):
	#将抓取到的文件传入BeautifulSoup的构造方法
	soup = BeautifulSoup(open(filename1))
	print_title = soup.find(id='cb_post_title_url').string
	print "正文标题：", print_title         #往终端打印正文标题
	print_content = soup.find(id="cnblogs_post_body").get_text()
	print "正文内容：", print_content   #往终端打印正文内容

	return soup

#3. 从文档中找到所有<a>标签的链接
def print_links(soup):
	print '-------------------------------------------------------------------------'
	list_links = []
	for link in soup.find_all('a'):

		if link.get('href') == None:
			continue
		#筛选"http://"开头的链接
		match = re.search(r'^(http://)', link.get('href'), re.I)
		if match == None:
			continue
		if match.group().find("http://") != -1:
			#进一步去掉重复的链接
			if link.get('href') not in list_links:
			#if list_links.count(link.get('href')) == 0:     #与上一句等效
				list_links.append(link.get('href'))
				print(link.get('href'))
	print len(list_links)       
 			

#4. 往mainData.html文件写入正文标题及内容, 保留原来的排版
def outputData(soup, filename2):
	op = open(filename2, "wb+")
	title = soup.find(id='cb_post_title_url').string
	content = soup.find(id="cnblogs_post_body").children
	#往mainData.html文件写入正文标题
	op.write(str(title))
	#往mainData.html文件写入正文内容
	for child in content:
		op.write(str(child))

	op.close()

#python中的main函数    
if __name__ == "__main__":
	filename1 = 'outData.html'
	filename2 = 'mainData.html'
	getContent(filename1)
	soup = printContent(filename1)
	print_links(soup)
	outputData(soup, filename2)
