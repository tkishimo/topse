from lxml import etree
import re

mxml = etree.parse('model2.xml').getroot()
mtree = etree.ElementTree(mxml)
sxml = etree.parse('samp.xml').getroot()
stree = etree.ElementTree(sxml)


#mtag = [(mtree.getpath(m)).split("/") for m in mxml.iter()]
#stag = [(stree.getpath(s)).split("/") for s in sxml.iter()]
mtag = [('%s/%s' % (mtree.getpath(m),m.text)).split("/") for m in mxml.iter()]
stag = [('%s/%s' % (stree.getpath(s),s.text)).split("/") for s in sxml.iter()]
#print stag
pattern = re.compile("\[\d\]")
mmtag = []
sstag = []
i = 0
for a in mtag:
	m_off_list = []
	dict = {}
	if "TOKEN" in a:
		if "column_name" in a:
			a.pop()
			#print a
		if "table_name" in a:
			i += 1
			print i
			print a[-1]
			dict[i] = a[-1]
			print dict
		a = [pattern.sub('',str) for str in a]
		for x in a:
			if x not in ['expr']:
				m_off_list.append(x)
		#print m_off_list
		mmtag.append(m_off_list)

for a in stag:
	s_off_list = []
	if "TOKEN" in a:
		if "column_name" in a:
			a.pop()
			#print a
		a = [pattern.sub('',str) for str in a]
		#print a
		for x in a:
			if x not in ['expr']:
				s_off_list.append(x)
		sstag.append(s_off_list)

for a in mmtag:
	print a

print mmtag == matched_list

