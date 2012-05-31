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
			fragments[os.sep.join(fullpath.split(os.sep)[5:])] = json.loads(open(fullpath).read())
	print len(fragments), "fragments found."
	#os.remove(os.path.join(rootdir,contribdir, "index.fragments.json"))
	f = open(os.path.join(rootdir,contribdir, "index.fragments.json"), "r+")
	f.write(json.dumps(fragments))