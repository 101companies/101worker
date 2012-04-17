import sys
import commands

if (len(sys.argv) == 2):
   log = open('../../101logs/runner.log', 'a')
   module = sys.argv[1]
   print 'Performing module %s.' % module
   status, output = commands.getstatusoutput('cd '+module+'; make')
   log.write('BEGIN '+module+'\n')
   if (status == 0):
      msg = 'OK'
   else:
      msg = 'FAIL ('+str(status)+')'
      print msg
   log.write(output+'\n')
   log.write('END -- '+msg+'\n')
   sys.exit(0)
else:
   sys.exit(-1)
