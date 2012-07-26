#! /usr/bin/env python

import sys
import simplejson as json
sys.path.append('../../libraries/101meta')
import const101
import tools101

# Per-file functinonality
def derive(geshicode, rFilename, sFilename, tFilename):

   # Housekeeping for geshicode
   geshicodes.add(geshicode)

   print "Process " + rFilename + " for GeSHi code " + geshicode + "."
   command = "php " + geshi + " \"" + sFilename + "\" \"" + tFilename + "\" " + geshicode
   (status, output) = tools101.run(command)

   # Result aggregation
   result = dict()
   result["geshicode"] = geshicode
   result["command"] = command
   result["status"] = status
   result["output"] = output

   return result


print "Generating GeSHi-based HTML for 101repo."

if (len(sys.argv) != 2): sys.exit(-1)
geshi = sys.argv[1] # GeSHi in the workspace

# Initialize housekeeping
geshicodes = set()
dump = tools101.loadDumpIncrementally(const101.geshiDump)
if "geshicodes" in dump:
   geshicodes = set(dump["geshicodes"])

# Loop over matches
dump = tools101.deriveByKey("geshi", ".geshi.html", derive)

# Convert set to list before dumping JSON
geshicodes = list(geshicodes)

# Assemble dump, save it, and exit
dump = dict()
dump["geshicodes"] = geshicodes
dump["numbers"] = dict()
dump["numbers"]["numberOfGeshicodes"] = len(geshicodes)
tools101.saveDumpAndExit(const101.geshiDump, dump)
