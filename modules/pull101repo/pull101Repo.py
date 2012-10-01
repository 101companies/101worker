#! /usr/bin/env python

import os
import sys
import commands
sys.path.append('../../libraries/101meta')
import const101

status = os.system("./pullRepo.py " + const101.sRoot + " https://github.com/101companies/101repo")
#status, output = commands.getstatusoutput(cmd)
if (status):
	print "pull101Repo failed"
	sys.exit(status)
	
