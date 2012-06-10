import os
import subprocess
import sys
import commands

from time import gmtime, strftime

log = open('../../101logs/runner.log', 'a')

def write2log(msg):
   global log
   print msg


if (len(sys.argv) == 2):
   module = sys.argv[1]
   write2log('\nPerforming module %s.' % module)
   write2log('Started at % s' % strftime("%Y-%m-%d %H:%M:%S", gmtime()))

   p = subprocess.Popen('cd '+module+'; make', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
   write2log('Module PID: %s' % p.pid)

   #creating a PID file is the module subdir indicating the the module is running.
   pidFileName = module + "/pid"; 

   print os.getcwd()
   #if file exists -- the process is already running, report to the log and skip it
   if os.path.isfile(os.getcwd() + '/' + pidFileName):
      write2log('Module %s is already running; processId: %s' %(module,str(p.pid)))
      sys.exit(-1)

   pid_file = open(os.getcwd() + '/' + pidFileName, "w")
   print "Creating PID file: %s" % str(os.getcwd() + '/' + pidFileName)
   pid_file.write(str(p.pid))
   pid_file.close()

   for line in p.stdout.readlines():
      write2log(line)
   retval = p.wait()

   write2log('Finished at % s' % strftime("%Y-%m-%d %H:%M:%S", gmtime()))
   write2log("Retval %s" % retval)

   #remove PID file when the process finished
   os.remove(pidFileName)

   if (retval == 0):
      msg = 'OK'
   else:
      msg = 'FAIL ('+str(retval)+')'
   
   write2log(msg)
   #status, output = commands.getstatusoutput('cd '+module+'; make')
   #log.write('BEGIN '+module+'\n')
   #if (status == 0):
   #   msg = 'OK'
   #else:
   #   msg = 'FAIL ('+str(status)+')'
   #   print msg
   #log.write(output+'\n')
   #log.write('END -- '+msg+'\n')
   sys.exit(0)
else:
   sys.exit(-1)
