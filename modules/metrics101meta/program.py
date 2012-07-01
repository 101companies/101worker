#! /usr/bin/env python

import sys
import simplejson as json
sys.path.append('../../libraries/101meta')
import const101
import tools101

# Per-file functinonality
def fun(geshicode, rFilename, sFilename, tFilename1):
   tFilename2 = tFilename1[:-len(".metrics.json")]+".tokens.json"
   print "Process " + rFilename + " for GeSHi code " + geshicode + "."
   cmd = "php helper.php" + " \"" + sFilename + "\" \"" + tFilename1 + "\" \"" + tFilename2 + "\" "+ geshicode
   (status, output) = tools101.run(cmd)
   return status

print "Generating GeSHi-based metrics for 101repo."
dump = tools101.mapMatchesWithKey("geshi", ".metrics.json", fun)
geshiFile = open(const101.metricsDump, 'w')
geshiFile.write(json.dumps(dump))
sys.exit(dump["noProblems"])
