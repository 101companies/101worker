import os
import sys
import simplejson as json
import commands
import time

# Get directories from argument list
if (len(sys.argv) != 5): sys.exit(-1)
repo = sys.argv[1]
geshi = sys.argv[2]
matches = json.load(open(sys.argv[3], 'r')) # load 101meta matches
result = sys.argv[4]

# Accumulate non-successful exit codes
exitcode = 0

# Go over matches to find opportunities for geshi
skipped = 0
for entry in matches:

   # Look up geshi code
   geshicode = [ x["geshi"]
                 for x in map(lambda u: u["metadata"], entry["units"])
                 if "geshi" in x ]

   # Continue if geshi code is missing or ambiguous
   if len(geshicode) != 1: continue   
   geshicode = geshicode[0]

   # RELATIVE dirname and filename
   rFilename = entry["filename"]
   rDirname = os.path.dirname(rFilename)
   basename = os.path.basename(rFilename)

   # SOURCE dirname and filename
   sDirname = os.path.join(repo, rDirname)
   sFilename = os.path.join(sDirname, basename)

   # TARGET dirname and filename
   tDirname = os.path.join(result, "geshi", rDirname)
   tFilename = os.path.join(tDirname, basename + ".html")

   # Create target directory, if necessary
   try:
      os.stat(tDirname)
   except:
      try:
         os.makedirs(tDirname)
      except OSError:
         pass

   try:
      sSize = os.stat(sFilename).st_size
      if sSize == 0:
         run = False
      else:
         sCtime = os.path.getmtime(sFilename)
         tCtime = os.path.getmtime(tFilename)
         run = sCtime > tCtime
   except:
      run = True

   # Run geshi, if needed, and report problems, if any
   if not run:
      skipped += 1
      continue
   print "Process " + rFilename + " for GeSHi code " + geshicode + "."
   cmd = "php " + geshi + " \"" + sFilename + "\" \"" + tFilename + "\" " + geshicode
   (status, output) = commands.getstatusoutput(cmd)
   if status != 0:
      print "Command failed: " + cmd
      print "Status: " + str(status)
      print "Output: " + output
      if exitcode == 0: exitcode = status

print "Skipped " + str(skipped) + " up-to-date files."
sys.exit(exitcode)
