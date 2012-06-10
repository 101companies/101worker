import sys
import commands
import os

if (len(sys.argv) == 2):
   module = sys.argv[1]
   commands.getstatusoutput('cd '+module+'; make clean')
   if os.path.isfile(module+'/pid'): 
   	os.remove(module+'/pid')
   sys.exit(0)
else:
   sys.exit(-1)
