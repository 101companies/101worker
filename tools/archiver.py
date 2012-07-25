import datetime
import sys
import shutil
import commands
import os

if os.path.isfile('../configs/%s' % sys.argv[1]) == False:
	print "Config file not found"
	sys.exit(-1)

today = str(datetime.date.today())
now = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")

lastArchive = open('../../101web/logs/lastArchive', "w")
lastArchive.write(now)
lastArchive.close()

try:
	print now
	os.makedirs('../../101web/logs/'+now)
except OSError:
	pass

config_file = open('../configs/%s' % sys.argv[1], "r")
modules = config_file.readlines()

for module in modules:
	module = module.strip()	
	if module.__len__() < 2:
		continue

	if os.path.isfile(module+'/module.log'):
		shutil.copy2(module+'/module.log', '../../101web/logs/'+now+"/"+module+".log")

sys.exit(0)