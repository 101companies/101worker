import os
import os.path
import sys
import commands

def megals(dir):
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


if (len(sys.argv) == 2):
   repo = sys.argv[1]
   for capa in os.listdir(repo+'/capabilities'):
      dir = repo+'/capabilities/'+capa+'/MegaL'
      megals(dir)
   for tech in os.listdir(repo+'/technologies'):
      dir = repo+'/technologies/'+tech+'/MegaL'
      megals(dir)
   sys.exit(0)
else:
   sys.exit(-1)
