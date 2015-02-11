#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2
import os
from bs4 import *
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
baseDir = os.getcwd()

tbName = raw_input("输入贴吧名: ")
namedir = os.path.join(baseDir, tbName)
search_url = "http://tieba.baidu.com/f?ie=utf-8&kw=" + tbName + "&fr=search"
if not os.path.exists(namedir):
	os.mkdir(namedir)
html = urllib2.urlopen(search_url).read()
soup = BeautifulSoup(html)
tiebapage = soup.find(id="frs_list_pager")
if tiebapage == None:
	tiebapage = 1
else:
	tiebapage = tiebapage.contents[-2]
	tiebapage = int((tiebapage['href'].split('='))[-1])
print tiebapage
	# print soup.prettify()
for i in range(tiebapage):
	search_url = "http://tieba.baidu.com/f?ie=utf-8&kw=" + tbName + "&pn=" + str(i*50) + "&fr=search"
	if not os.path.exists(namedir):
		os.mkdir(namedir)
	html = urllib2.urlopen(search_url).read()
	soup = BeautifulSoup(html)
	raw_list = soup.find_all("a", class_="j_th_tit")
	title_list = []
	titlename = []
	for l in raw_list:
		title_list.append(l['href'])
		titlename.append(l.contents)
	
	title = zip(title_list,titlename)
	for t in title:
		di = os.path.join(namedir, t[1][0])
		if not os.path.exists(di):
			os.mkdir(di)
	
		tie = urllib2.urlopen("http://tieba.baidu.com"+t[0]).read()
		ties = BeautifulSoup(tie)
		pageli = ties.find_all("li", class_="l_pager pager_theme_4 pb_list_pager")
		page_num = 0
		for p in pageli:
			if p.contents == []:
				continue
			pa = p.find_all('a')
			page_num = int(pa[-1]['href'].split('=')[1])
		f = open(os.path.join(di, '1.html'), "w")
		f.write(str(ties))
		f.close()
		if page_num != 0:
			for i in range(2, page_num+1):
				backpage = urllib2.urlopen("http://tieba.baidu.com"+t[0]+'?pn='+str(i)).read()
				backpage = BeautifulSoup(backpage)
				f = open(os.path.join(di, str(i)+'.html'), "w")
				f.write(str(backpage))
				f.close()
	

	