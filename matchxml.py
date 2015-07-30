#!/usr/bin/env python
# coding: UTF-8

from lxml import etree
import re
import sys
import codecs

with codecs.open(sys.argv[1],mode='r',encoding='shiftjis') as file:
	lines = file.read()
with codecs.open("dummy.xml",mode='w',encoding='utf-8') as file:
	for line in lines:
		line.encode('utf-8')
		#print line
		#print type(line)
		file.write(line)

#ifile = unicode(sys.argv[1], encoding='shift-jis')
mxml = etree.parse(sys.argv[2]).getroot()
mtree = etree.ElementTree(mxml)
sxml = etree.parse('dummy.xml').getroot()
stree = etree.ElementTree(sxml)

#mtag = [(mtree.getpath(m)).split("/") for m in mxml.iter()]
#stag = [(stree.getpath(s)).split("/") for s in sxml.iter()]
mtag = [('%s/%s' % (mtree.getpath(m),m.text)).split("/") for m in mxml.iter()]
stag = [('%s/%s' % (stree.getpath(s),s.text)).split("/") for s in sxml.iter()]
pattern = re.compile("\[\d\]")

#initialize
mmtag = []
sstag = []
tab_list = []

for a in mtag:
	m_off_list = []
	if "TOKEN" in a:
		m_off_list = []
		a = [pattern.sub('',tempstr) for tempstr in a]
		if "column_name" in a:
			a.pop()
		if "table_name" in a:
			if "result_column" not in a:
				try:
					tab_list.index(a[-1])
					a[-1] = "tabs"


				except ValueError:
					tab_list.append(a[-1])
					a[-1] = "tab1"
		if "table_alias" in a:
			a.pop()	#Table_alias値を削除


		if "literal_value" in a:
			del a[a.index("TOKEN")+1:]	#配列からliteral値を削除

		for x in a:
			if x not in ['expr', 'select_stmt', 'select_or_values', 'table_or_subquery', 'join_clause']:
				m_off_list.append(x)
		mmtag.append(m_off_list)

tab_list = []
for a in stag:
	if "TOKEN" in a:
		s_off_list = []
		a = [pattern.sub('',tempstr) for tempstr in a]
		if "column_name" in a:
			a.pop()
		if "table_name" in a:
			if "result_column" not in a:
				try:
					tab_list.index(a[-1])
					a[-1] = "tabs"


				except ValueError:
					tab_list.append(a[-1])
					a[-1] = "tab1"
		if "table_alias" in a:
			a.pop()	#Table_alias値を削除


		if "literal_value" in a:
			del a[a.index("TOKEN")+1:]	#配列からliteral値を削除

		for x in a:
			if x not in ['expr', 'select_stmt', 'select_or_values', 'table_or_subquery', 'join_clause']:
				s_off_list.append(x)
		sstag.append(s_off_list)

matched_list=[tag for tag in mmtag if tag in sstag]
for a in sstag:
	print a
print mmtag == matched_list

