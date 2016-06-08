import os
import sys
import json

rootdir = sys.argv[1]

print rootdir
for contribdir in filter(lambda x: os.path.exists(os.path.join(rootdir, x, "index.summary.json")),os.listdir(rootdir)):
	print "Current contributution:", contribdir
	fragments = dict(tags={}, files={})
	for root, subFolders, files in os.walk(os.path.join(rootdir, contribdir)):
		for file in filter(lambda x: x.endswith(".fragments.json") and x != "index.fragments.json", files):
			fullpath = os.path.join(root,file)
			tags = json.loads(open(fullpath).read())['tags'].keys()
			for tag in tags:
				if fragments['tags'].has_key(tag):
					fragments['tags'][tag].append(os.sep.join(fullpath.split(os.sep)[5:]))
				else:
					fragments['tags'][tag] = [os.sep.join(fullpath.split(os.sep)[5:])]
			fragments['files'][os.sep.join(fullpath.split(os.sep)[5:])] = json.loads(open(fullpath).read())
	print len(fragments), "fragments found."
	#os.remove(os.path.join(rootdir,contribdir, "index.fragments.json"))
	f = open(os.path.join(rootdir,contribdir, "index.fragments.json"), "w+")
	f.write(json.dumps(fragments))