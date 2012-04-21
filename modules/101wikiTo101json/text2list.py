import sys
import re
import json

def text2List(text):
	textstart = 0
	for textm in re.finditer("\[\[([^\[\|]+)(\|([^\[]+))?\]\]",text):
		linkm = re.match("(([^\:]+):)?(.+)", textm.group(1))
		yield ('text', text[textstart:textm.start()])
		yield ('link', linkm.group(2), linkm.group(3), textm.group(3))
		textstart = textm.end()

def listify(json, textsections):
	for t in json:
		for e in json[t]:
			for attr in json[t][e]:
				if attr in textsections:
					json[t][e][attr] = list(text2List(json[t][e][attr]))				

if len(sys.argv) <= 2:
	print "Need input path of basic json and output for linkified json"
else:
	json101 = json.load(open(sys.argv[1]))		
	listify(json101,['discussion', 'dicussion', 'architecture', 'intent', 'motivation', 'issues', 'usage', 'description', 'summary', 'illustration'])
	outf = open(sys.argv[2], "write")
	outf.write(json.dumps(json101))