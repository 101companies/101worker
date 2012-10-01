#! /usr/bin/env python

import os
import sys
import commands

path = sys.argv[1]
repoUrl = sys.argv[2]

if (os.path.exists(path)):
	os.chdir(path)
	cmd = "git pull -q"
else:
	os.chdir(os.path.dirname(path))
	cmd = "git clone " + repoUrl

status = os.system(cmd)
#status, output = commands.getstatusoutput(cmd)
if (status):
	print "pullRepo failed"
	sys.exit(status)
