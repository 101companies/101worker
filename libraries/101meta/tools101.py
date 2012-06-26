import os
import sys
import commands

# Dot-wise progress information
def tick():
    sys.stdout.write('.')
    sys.stdout.flush()

# Create target directory, if necessary
def makedirs(d):
   try:
      os.stat(d)
   except:
      try:
         os.makedirs(d)
      except OSError:
         pass

# Test whether a target is needed relative to a source
def build(sFilename, tFilename):
   try:
      sSize = os.stat(sFilename).st_size
      if sSize == 0:
         return False
      else:
         sCtime = os.path.getmtime(sFilename)
         tCtime = os.path.getmtime(tFilename)
         return sCtime > tCtime
   except:
      return True

# Run a command
def run(cmd):
   (status, output) = commands.getstatusoutput(cmd)
   if status != 0:
      print "Command failed: " + cmd
      print "Status: " + str(status)
      print "Output: " + output
   return status
