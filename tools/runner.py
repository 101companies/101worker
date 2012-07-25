import os
import subprocess
import sys
import commands

from threading import Timer
from time import gmtime, strftime

log = open('../../101logs/runner.log', 'a')
print log

VERBOSE = False

def write2log(msg):
   global log
   global VERBOSE
   if VERBOSE == True:
      print msg
   else:
      log.write(msg)

def write2moduleLog(msg, module):
   global VERBOSE
   if VERBOSE == True:
      print msg
   else:
      log = open(module+'/module.log', 'a')
      log.write(msg)

def kill_proc(proc, timeout):
   timeout["value"] = True
   write2log("FAIL : TIMEOUT " + str(proc.pid))
   print "KILLING PROCESS TREE"
   currentDir = os.path.dirname(os.path.abspath(__file__))
   killCmd = currentDir + '/killtree.sh ' + str(proc.pid) +' TERM'
   write2log(killCmd)
   p = subprocess.Popen(killCmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
   stdout, stderr = p.communicate()
   print "writing to log"
   print stdout
   print stderr
   write2log(stdout)
   write2log(stderr)

def run(proc, timeout_sec):
   timeout = {"value": False}
   timer = Timer(timeout_sec, kill_proc, [proc, timeout])
   timer.start()
   stdout, stderr = proc.communicate()
   timer.cancel()
   return proc.returncode, stdout, timeout["value"]   

def main(config, is_verbose):
   global VERBOSE
   VERBOSE = is_verbose

   config_file = open(config, "r")
   modules = config_file.readlines()
   for module in modules:
      module = module.strip()
      if module.__len__() < 2:
         continue

      write2log('\nPerforming module %s.' % module)
      write2log('\nStarted at % s' % strftime("%Y-%m-%d %H:%M:%S", gmtime()))

      p = subprocess.Popen('cd '+module+'; make', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
      write2log('\nModule PID: %s' % p.pid)

      #creating a PID file is the module subdir indicating the the module is running.
      pidFileName = module + "/pid"; 

      #if file exists -- the process is already running, report to the log and skip it
      if os.path.isfile(os.getcwd() + '/' + pidFileName):
         write2log('\nModule %s is already running; processId: %s' %(module,str(p.pid)))

      pid_file = open(os.getcwd() + '/' + pidFileName, "w")
      #write2log("\nCreating PID file: %s" % str(os.getcwd() + '/' + pidFileName))
      pid_file.write(str(p.pid))
      pid_file.close()

      print "\nWaiting for completion..." + module
      retval, stdout, timeout = run(p, 30*60)
      #for line in stdout.readlines():
      write2moduleLog(stdout, module) 

      write2log('\nFinished at % s' % strftime("%Y-%m-%d %H:%M:%S", gmtime()))
      if (retval == 0):
         msg = '\nOK'
      else:
         msg = '\nFAIL ('+str(retval)+')'
      
      write2log(msg)
      #remove PID file when the process finished
      if os.path.isfile(os.getcwd() + '/' + pidFileName):
         os.remove(os.getcwd() + '/' + pidFileName)
   
   sys.exit(0)

if __name__ == "__main__":
   try:
      if (len(sys.argv) > 1):
         #check if the config file exists
         if os.path.isfile('../configs/%s' % sys.argv[1]) == False:
            print 'Config file does not exist: %s' % sys.argv[1]
            sys.exit(-1)
         else:
          if(len(sys.argv) == 3):
               if(sys.argv[2] == 'verbose'): main('../configs/%s' % sys.argv[1], True) 
          else: main('../configs/%s' % sys.argv[1], False) 
         main()
   except KeyboardInterrupt:
      print "Received CTRL+C...Killing process tree NOW"
      currentDir = os.path.dirname(os.path.abspath(__file__))
      killCmd = currentDir + '/killtree.sh ' + str(os.getpid()) +' TERM'
      p = subprocess.Popen(killCmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
      stdout, stderr = p.communicate()
      pass          
