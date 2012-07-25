import sys
import shutil
import commands
import os

if os.path.isfile('../configs/%s' % sys.argv[1]) == False:
	print "Config file not found"
	sys.exit(-1)

try:
    os.makedirs('../101web/logs')
except OSError:
	print "error"
	pass

config_file = open('../configs/%s' % sys.argv[1], "r")
modules = config_file.readlines()

for module in modules:
	module = module.strip()	
	if module.__len__() < 2:
		continue

	if os.path.isfile(module+'/module.log'):
		shutil.copy2(module+'/module.log', '../101web/logs/'+module+".log")

sys.exit(0)