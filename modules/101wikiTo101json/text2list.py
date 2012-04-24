import sys
import re
import json


def text2Links(text):
	prefix2type = {'Language' : 'Language', '' : 'Concept', '101feature' : 'Feature', '101implementation' : "Implementation", 'Technology' : 'Technology', ':Category' : 'Category'}
	textstart = 0
	links = []
	for textm in re.finditer("\[\[([^\[\|]+)(\|([^\[]+))?\]\]",text):
		linkm = re.match("(([^\:]+):)?(.+)", textm.group(1))
		if linkm.group(2) in prefix2type:
			ltype = prefix2type[linkm.group(2)]
		else:
			ltype = "Page"
		links.append(dict(type=ltype, name=linkm.group(3)))	
		textstart = textm.end()
	return links

def listify(json, textsections):
	for t in json:
		for e in json[t]:
			linkified = {}
			for attr in json[t][e]:
				if attr in textsections:
					linkified[attr + "_links"] = text2Links(json[t][e][attr])
			for l in linkified:
				json[t][e][l] = linkified[l]


if len(sys.argv) <= 2:
	print "Need input path of basic json and output for linkified json"
else:
	json101 = json.load(open(sys.argv[1]))		
	listify(json101,['discussion', 'dicussion', 'architecture', 'intent', 'motivation', 'issues', 'usage', 'description', 'summary', 'illustration', 'headline'])
	outf = open(sys.argv[2], "write")
	outf.write(json.dumps(json101))