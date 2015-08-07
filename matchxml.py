#!/usr/bin/env python
# coding: UTF-8
from lxml import etree
import re
import sys
import codecs

def chksql(arg1,arg2):

	with codecs.open(arg1,mode='r',encoding='shiftjis') as file:
		lines = file.read()
	with codecs.open("dummy.xml",mode='w',encoding='utf-8') as file:
		for line in lines:
			line.encode('utf-8')
			#print line
			#print type(line)
			file.write(line)

	mxml = etree.parse(arg2).getroot()
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
				if x not in ['expr', 'select_stmt', 'select_or_values', 'table_or_subquery', 'join_clause', 'common_table_expression', 'select_core']:
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
				if x not in ['expr', 'select_stmt', 'select_or_values', 'table_or_subquery', 'join_clause', 'common_table_expression', 'select_core']:
					s_off_list.append(x)
			sstag.append(s_off_list)

	matched_list=[tag for tag in mmtag if tag in sstag]

	flg = mmtag == matched_list
	#print str(arg1) +":"+ str(arg2) +" "+ str(flg)
	return flg
if __name__ == '__main__':
	import glob
	files = glob.glob("F:/nii/test/*.xml")
	for file in files:
		tf = []
		tf_flg = chksql(file,"F:/nii/report/model2.xml") #select .. from tab,(select max(col1) from tab)
		tf.append(tf_flg)
		tf_flg = chksql(file,"F:/nii/report/model3.xml") #select .. from tab where col1 = (select max(col1)..
		tf.append(tf_flg)
		tf_flg = chksql(file,"F:/nii/report/model4.xml") #select .. from tab where col1 = (select col1 from tab)
		tf.append(tf_flg)
		tf_flg = chksql(file,"F:/nii/report/model7.xml") #select .. from tab where col1 = (select min(col1)..
		tf.append(tf_flg)
		tf_flg = chksql(file,"F:/nii/report/model8.xml") #select .. union select ..
		tf.append(tf_flg)
		print file+":"+str(max(tf))

