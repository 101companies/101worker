import os
import os.path
import sys
import commands

if (len(sys.argv) == 2):
   repo = sys.argv[1]
   for tech in os.listdir(repo+'/technologies'):
      dir = repo+'/technologies/'+tech+'/MegaL'
      if (os.path.isdir(dir)):
         for f in os.listdir(dir):
            file = dir+'/'+f
            if (f.endswith('.megal')):
               print 'Parsing '+file
               command = 'make '+file+'.parse'
               status, output = commands.getstatusoutput(command)
               if (status):
                  print output
                  sys.exit(status)
   sys.exit(0)
else:
   sys.exit(-1)
