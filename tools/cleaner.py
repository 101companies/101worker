import sys
import commands

if (len(sys.argv) == 2):
   module = sys.argv[1]
   commands.getstatusoutput('cd modules/'+module+'; make clean')
   sys.exit(0)
else:
   sys.exit(-1)
