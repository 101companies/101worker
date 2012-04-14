import sys
import commands

if (len(sys.argv) == 2):
   log = open('logs/runner.log', 'a')
   module = sys.argv[1]
   print 'Performing module %s.' % module
   status, output = commands.getstatusoutput('cd modules/'+module+'; make')
   if (status == 0):
      msg = 'OK'
   else:
      msg = 'FAIL ('+str(status)+')'
   log.write(module+': '+msg+'\n')
   sys.exit(0)
else:
   sys.exit(-1)
