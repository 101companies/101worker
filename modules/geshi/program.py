import os
import sys
import commands

if (len(sys.argv) == 3):
   repo = sys.argv[1]
   result = sys.argv[2]
   for dirname, subdirnames, _ in os.walk(repo+"/languages"):
      for subdirname in subdirnames:
         if (subdirname=="geshi"):
            geshidirname = os.path.join(dirname, subdirname)
            for _, _, filenames in os.walk(geshidirname):             
               for filename in filenames:
                  geshifilename = os.path.join(geshidirname, filename)
                  command = 'cp '+geshifilename+' '+result
                  status, output = commands.getstatusoutput(command)
   sys.exit(0)
else:
   sys.exit(-1)
