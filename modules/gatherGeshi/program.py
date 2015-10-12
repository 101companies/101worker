import os
import os.path
import sys
import commands

if (len(sys.argv) == 3):
   repo = sys.argv[1] 
   result = sys.argv[2]
   for lang in os.listdir(repo+'/languages'):
      dir = repo+'/languages/'+lang+'/geshi'
      if (os.path.isdir(dir)):
         for f in os.listdir(dir):
            file = dir+'/'+f
            if (f.endswith('.php')):
               print 'Gathering '+file
               command = 'cp '+file+' '+result
               status, output = commands.getstatusoutput(command)
               if (status):
                  sys.exit(status)
   sys.exit(0)
else:
   sys.exit(-1)
