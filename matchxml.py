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
	pattern = re.compile("¥[¥d+¥]")

	#initialize
	mmtag = []
	sstag = []
	tab_dict = {}
	alias_list = []
	cnt = 0

	for a in mtag:
		m_off_list = []
		if "TOKEN" in a:
			m_off_list = []
			a = [pattern.sub('',tempstr) for tempstr in a]
			if "column_name" in a:
				a.pop()
			if "table_alias" in a:
				alias_list.append(a[-1])
				a.pop()	#Table_alias値を削除
			if "column_alias" in a:
				a.pop()	#Column_alias値を削除
			if "table_name" in a:
				if "result_column" not in a:
					try:
						v = tab_dict[a[-1]]
						#print stag[tab_dict[a[-1]]]
						mmtag[v][-1] = "tabs"
						a[-1] = "tabs"
					except KeyError:
						if a[-1] in alias_list: #aliasにあればtabsに変換
							a[-1] = "tabs"
						else:
							tab_dict[a[-1]] = cnt
							a[-1] = "tab"

			if "literal_value" in a:
				del a[a.index("TOKEN")+1:]	#配列からliteral値を削除
			for x in a:
				if x not in ['expr', 'select_stmt', 'select_or_values', 'table_or_subquery', 'join_clause', 'common_table_expression', 'select_core', 'join_constraint', 'factored_select_stmt', 'insert_stmt']:
					m_off_list.append(x)
			mmtag.append(m_off_list)
			cnt += 1

	tab_dict = {}
	alias_list = []
	cnt = 0
	for a in stag:
		if "TOKEN" in a:
			s_off_list = []
			a = [pattern.sub('',tempstr) for tempstr in a]
			if "column_name" in a:
				a.pop()
			if "table_alias" in a:
				alias_list.append(a[-1])
				a.pop()	#Table_alias値を削除

			if "column_alias" in a:
				a.pop()	#Column_alias値を削除
			if "table_name" in a:
				if "result_column" not in a:
					try:
						v = tab_dict[a[-1]]
						#print stag[tab_dict[a[-1]]]
						sstag[v][-1] = "tabs"
						a[-1] = "tabs"
					except KeyError:
						if a[-1] in alias_list: #aliasにあればtabsに変換
							a[-1] = "tabs"
						else:
							tab_dict[a[-1]] = cnt
							a[-1] = "tab"

			if "literal_value" in a:
				del a[a.index("TOKEN")+1:]	#配列からliteral値を削除

			for x in a:
				if x not in ['expr', 'select_stmt', 'select_or_values', 'table_or_subquery', 'join_clause', 'common_table_expression', 'select_core', 'join_constraint', 'factored_select_stmt', 'insert_stmt']:
					s_off_list.append(x)
			sstag.append(s_off_list)
			cnt += 1


	i = -1
	matched_list = []
	for tag in mmtag:
		while i<=len(sstag)-2:
			i += 1
			#print tag
			if tag==sstag[i]:
				matched_list.append(tag)
				break

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
		tf_flg = chksql(file,"F:/nii/report/model8.xml") #select .. from tab1 union select ..from tab1
		tf.append(tf_flg)
		tf_flg = chksql(file,"F:/nii/report/model9.xml") #SELECT COL2 FROM TAB1 A,TAB1 B WHERE A.COL1=B.COL1
		tf.append(tf_flg)
		tf_flg = chksql(file,"F:/nii/report/model11.xml") #SELECT .. FROM TAB1 INNER JOIN (SELECT ..,MAX(COL1) FROM TAB1) ON ..
		tf.append(tf_flg)
		tf_flg = chksql(file,"F:/nii/report/model12.xml") #SELECT .. FROM TAB1 A JOIN TAB1 B ON A.COL1=B.COL1
		tf.append(tf_flg)
		tf_flg = chksql(file,"F:/nii/report/model13.xml") #SELECT COL2 FROM TAB2 B INNER JOIN TAB1 A ON A.COL1 = (SELECT MIN(COL1) FROM TAB1)
		tf.append(tf_flg)
		print file+":"+str(max(tf))
