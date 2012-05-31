import os
import sys
import json

rootdir = sys.argv[1]

print rootdir
for contribdir in filter(lambda x: os.path.exists(os.path.join(rootdir, x, "index.summary.json")),os.listdir(rootdir)):
	print "Current contributution:", contribdir
	fragments = {}
	for root, subFolders, files in os.walk(os.path.join(rootdir, contribdir)):
		for file in filter(lambda x: x.endswith(".fragments.json"), files):
			fullpath = os.path.join(root,file)
			print fullpath
			print open(fullpath).read()
			fragments[os.sep.join(fullpath.split(os.sep)[5:])] = json.loads(open(fullpath).read())
	print len(fragments), "fragments found."
	open(os.path.join(rootdir,contribdir, "index.fragments.json"), "r+").write(json.dumps(fragments))