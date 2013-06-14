#! /usr/bin/env python

import sys
import simplejson as json
sys.path.append('../../libraries/101meta')
import const101
import tools101

#used for the incrementally stuff
def testFile(sFilename, tFilename):
	return tools101.build(sFilename, tFilename)

#accept files that have  a geshi code - but also add the relevance of a file with respect to the default relevance
def testEntry(entry):
	meta = {"relevance" : "system"}
	for m in entry["units"]:
		if "relevance" in m["metadata"]:
			meta["relevance"] = m["metadata"]["relevance"]
		if "geshi" in m["metadata"]:
			meta["geshi"] = m["metadata"]["geshi"]
	return meta

# Per-file functionality
def derive(info, rFilename, sFilename, tFilename1):
   if "geshi" in info:
      tFilename2 = tFilename1[:-len(".metrics.json")]+".tokens.json"
      print "Process " + rFilename + " for GeSHi code " + info["geshi"] + "."
      command = "php helper.php" + " \"" + sFilename + "\" \"" + tFilename1 + "\" \"" + tFilename2 + "\" \"" + info["geshi"] + "\" " + info["relevance"]
      print command
      (status, output) = tools101.run(command) 

      # Result aggregation
      result = dict()
      result["geshicode"] = info["geshi"]
      result["command"] = command
      result["status"] = status
      result["output"] = output
   else:
	   default = const101.noMetrics()
	   default["relevance"] = info["relevance"]
	   json.dump(default, open(tFilename1, 'w'))

	   result = dict()
	   result["status"] = 0

   return result

print "Generating GeSHi-based metrics for 101repo."

# Initialize housekeeping
geshicodes = set()
dump = tools101.beforeMapMatches(const101.metricsDump)
if "geshicodes" in dump:
   geshicodes = set(dump["geshicodes"])

# Loop over matches
dump = tools101.mapMatches(testEntry, testFile, ".metrics.json", derive)

# Convert set to list before dumping JSON
geshicodes = list(geshicodes)

# Assemble dump, save it, and exit
dump = dict()
dump["geshicodes"] = geshicodes
dump["numbers"] = dict()
dump["numbers"]["numberOfGeshicodes"] = len(geshicodes)
tools101.afterMapMatches(dump, const101.metricsDump)
