#!/usr/bin/python
# Generate cionfig file from top level DDI XML instance
# Usage: config_gen.py 

import sys
import re
import glob
from lxml import etree

files={"alspac_ss.xml":"alspac","bcs70_ss.xml":"bsc70","hcs_ss.xml":"hcs","mcs_ss.xml":"mcs","ncds_ss.xml":"ncds","nshd_ss.xml":"nshd","sws_ss.xml":"sws","usoc_ss.xml":"usoc"}

nsmap={'ddi': 'instance:3_2', 'r': 'ddi:reusable:3_2', 'g': 'ddi:group:3_2','ddi': 'ddi:logicalproduct:3_2', 'p': 'ddi:physicaldataproduct:3_2', 'ddi1':'physicaldataproduct_proprietary:3_2', 'pi':'ddi:physicalinstance:3_2'}

for file in files:
	study = files[file]

	try:
		tree = etree.parse(file)
	except IOError:
		continue
		
	root = tree.getroot()

	for selem in tree.findall('{ddi:group:3_2}Group/{ddi:studyunit:3_2}StudyUnit'):
		surn=""
		for s in selem.iter():
			sagency=""
			sid=""
			if s.tag == '{ddi:reusable:3_2}agency':
				sagency = s.text
			if s.tag == '{ddi:reusable:3_2}ID':
				sid = s.text
				surn="urn:ddi:"+sagency+":"+sid
			if s.tag == '{ddi:datacollection:3_2}DataCollectionModuleName':
				name=""
				for y in s.iter():
					if y.tag== '{ddi:reusable:3_2}String':
						name  = y.text								
						print "dataset"+"\t"+study+"\t"+name+"\t"+surn+"\t"+"dataset\\"+name+".ddi32.rp.xml"
			
	for elem in tree.findall('{ddi:group:3_2}Group/{ddi:studyunit:3_2}StudyUnit/{ddi:datacollection:3_2}DataCollection'):
		urn=""
		agency=""
		id=""
		for x in elem.iter():
			if x.tag == '{ddi:reusable:3_2}Agency':
				agency = x.text
			if x.tag == '{ddi:reusable:3_2}ID':
				id = x.text
				urn="urn:ddi:"+agency+":"+id
			if x.tag == '{ddi:datacollection:3_2}DataCollectionModuleName':
				name=""
				for y in x.iter():
					if y.tag== '{ddi:reusable:3_2}String':
						name  = y.text								
						print "instrument"+"\t"+study+"\t"+name+"\t"+urn+"\t"+"instruments\\"+name+".xml"
				
		


