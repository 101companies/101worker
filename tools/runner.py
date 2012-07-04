import os
import subprocess
import sys
import commands

from threading import Timer
from time import gmtime, strftime

log = open('../../101logs/runner.log', 'a')

def write2log(msg):
   global log
   #print msg
   log.write(msg)

def write2moduleLog(msg, module):
   log = open(module+'/module.log', 'a')
   log.write(msg)
   #print msg

def kill_proc(proc, timeout):
   timeout["value"] = True
   write2log("FAIL : TIMEOUT " + str(proc.pid))
   write2log("KILLING PROCESS TREE")
   currentDir = os.path.dirname(os.path.abspath(__file__))
   killCmd = currentDir + '/killtree.sh ' + str(proc.pid) +' TERM'
   write2log(killCmd)
   p = subprocess.Popen(killCmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
   stdout, stderr = p.communicate()
   write2log(stdout)
   write2log(stderr)

def run(proc, timeout_sec):
   timeout = {"value": False}
   timer = Timer(timeout_sec, kill_proc, [proc, timeout])
   timer.start()
   stdout, stderr = proc.communicate()
   timer.cancel()
   return proc.returncode, stdout, timeout["value"]   

if (len(sys.argv) == 2):
   module = sys.argv[1]
   write2log('\nPerforming module %s.' % module)
   write2log('\nStarted at % s' % strftime("%Y-%m-%d %H:%M:%S", gmtime()))

   p = subprocess.Popen('cd '+module+'; make', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
   write2log('\nModule PID: %s' % p.pid)

   #creating a PID file is the module subdir indicating the the module is running.
   pidFileName = module + "/pid"; 

   #if file exists -- the process is already running, report to the log and skip it
   if os.path.isfile(os.getcwd() + '/' + pidFileName):
      write2log('\nModule %s is already running; processId: %s' %(module,str(p.pid)))
      sys.exit(0)

   pid_file = open(os.getcwd() + '/' + pidFileName, "w")
   write2log("\nCreating PID file: %s" % str(os.getcwd() + '/' + pidFileName))
   pid_file.write(str(p.pid))
   pid_file.close()

   write2log("\nWaiting for completion...")
   retval, stdout, timeout = run(p, 30*60)
   #for line in stdout.readlines():
   write2moduleLog(stdout, module) 

   write2log('\nFinished at % s' % strftime("%Y-%m-%d %H:%M:%S", gmtime()))
   #write2log("Retval %s" % retval)

   if (retval == 0):
      msg = '\nOK'
   else:
      msg = '\nFAIL ('+str(retval)+')'
   
   write2log(msg)
   #remove PID file when the process finished
   write2log("\nRemoving PID file: %s" % str(os.getcwd() + '/' + pidFileName))
   os.remove(pidFileName)
   sys.exit(0)
else:
   sys.exit(-1)
