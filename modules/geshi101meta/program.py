#! /usr/bin/env python

import sys
import simplejson as json
sys.path.append('../../libraries/101meta')
import const101
import tools101

# Per-file functinonality
def fun(geshicode, rFilename, sFilename, tFilename):
   print "Process " + rFilename + " for GeSHi code " + geshicode + "."
   cmd = "php " + geshi + " \"" + sFilename + "\" \"" + tFilename + "\" " + geshicode
   (status, output) = tools101.run(cmd)
   return status

if (len(sys.argv) != 2): sys.exit(-1)
geshi = sys.argv[1] # GeSHi in the workspace
dump = tools101.mapMatchesWithKey("geshi", ".html", fun)
geshiFile = open(const101.geshiDump, 'w')
geshiFile.write(json.dumps(dump))
sys.exit(dump["noProblems"])
