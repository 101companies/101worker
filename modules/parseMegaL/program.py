import os
import sys
import commands

if (len(sys.argv) == 2):
   repo = sys.argv[1]
   for dir, subdirs, _ in os.walk(repo+"/technologies"):
      for s in subdirs:
         if (s=="MegaL"):
            subdir = os.path.join(dir, s)
            for _, _, files in os.walk(subdir):             
               for f in files:
                  file = os.path.join(subdir, f)
                  if (f.endswith('.megal')):
                     print file
                  # status, output = commands.getstatusoutput(command)
   sys.exit(0)
else:
   sys.exit(-1)
