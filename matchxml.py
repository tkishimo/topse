from lxml import etree
import re
import sys

mxml = etree.parse('model2.xml').getroot()
mtree = etree.ElementTree(mxml)
sxml = etree.parse(sys.argv[1]).getroot()
stree = etree.ElementTree(sxml)

#mtag = [(mtree.getpath(m)).split("/") for m in mxml.iter()]
#stag = [(stree.getpath(s)).split("/") for s in sxml.iter()]
mtag = [('%s/%s' % (mtree.getpath(m),m.text)).split("/") for m in mxml.iter()]
stag = [('%s/%s' % (stree.getpath(s),s.text)).split("/") for s in sxml.iter()]
#print stag
pattern = re.compile("\[\d\]")
mmtag = []
sstag = []

tab_list = []
blist = []
for a in mtag:
	m_off_list = []
	if "TOKEN" in a:
		blist = [a[-3].upper(),a[-2].upper(),a[-1].upper()]
		if "column_name" in a:
			blist.pop()
		if "table_alias" in a:
			blist.pop()
		if "table_name" in a:
			if "result_column" not in a:
				try:
					tab_list.index(a[-1])
					#print repr(1)
					tabname = "tab"+repr(tab_list.index(a[-1]))
				except ValueError:
					tab_list.append(a[-1])
					tabname = "tab"+repr(len(tab_list)-1)
				blist[-1] = tabname
				#print a
		blist = [pattern.sub('',str) for str in blist]
		mmtag.append(blist)

tab_list = []
blist = []
for a in stag:
	if "TOKEN" in a:
		blist = [a[-3].upper(),a[-2].upper(),a[-1].upper()]
		if "column_name" in a:
			blist.pop()
		if "table_alias" in a:
			blist.pop()
		if "table_name" in a:
			if "result_column" not in a:
				try:
					tab_list.index(a[-1])
					#print repr(1)
					tabname = "tab"+repr(tab_list.index(a[-1]))
				except ValueError:
					tab_list.append(a[-1])
					tabname = "tab"+repr(len(tab_list)-1)
				blist[-1] = tabname
				#print a
		blist = [pattern.sub('',str) for str in blist]
		sstag.append(blist)

matched_list=[tag for tag in mmtag if tag in sstag]
#for a in mmtag:
#	print a
print mmtag == matched_list

