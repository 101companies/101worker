#! /usr/bin/env python

import sys
import simplejson as json
sys.path.append('../../libraries/101meta')
import const101
import tools101

# Per-file functinonality
def derive(geshicode, rFilename, sFilename, tFilename1):
   tFilename2 = tFilename1[:-len(".metrics.json")]+".tokens.json"
   print "Process " + rFilename + " for GeSHi code " + geshicode + "."
   command = "php helper.php" + " \"" + sFilename + "\" \"" + tFilename1 + "\" \"" + tFilename2 + "\" "+ geshicode
   (status, output) = tools101.run(command)

   # Result aggregation
   result = dict()
   result["geshicode"] = geshicode
   result["command"] = command
   result["status"] = status
   result["output"] = output

   return result


print "Generating GeSHi-based metrics for 101repo."

# Initialize housekeeping
geshicodes = set()
dump = tools101.loadDumpIncrementally(const101.metricsDump)
if "geshicodes" in dump:
   geshicodes = set(dump["geshicodes"])

# Loop over matches
dump = tools101.deriveByKey("geshi", ".metrics.json.html", derive)

# Convert set to list before dumping JSON
geshicodes = list(geshicodes)

# Assemble dump, save it, and exit
dump = dict()
dump["geshicodes"] = geshicodes
dump["numbers"] = dict()
dump["numbers"]["numberOfGeshicodes"] = len(geshicodes)
tools101.saveDumpAndExit(const101.metricsDump, dump)
