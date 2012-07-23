#! /usr/bin/env python

import os
import sys
import simplejson as json
sys.path.append('../../libraries/101meta')
import const101
import tools101

# Per-file functinonality
def fun(extractor, rFilename, sFilename, tFilename, new):

   # Global counters
   global numberOfSuccesses
   global numberOfFailures

   # Housekeeping for extractor
   extractors.add(extractor)
   
   print "Extract facts from " + rFilename + " with " + extractor + "."
   cmd = os.path.join(const101.sRoot, extractor) + " \"" + sFilename + "\" \"" + tFilename + "\" "
   (status, output) = tools101.run(cmd)

   #
   # Create an empty file if extraction failed to create a file.
   # This improves the incremental experience.
   #
   if not os.path.exists(tFilename):
      empty = dict()
      tFile = open(tFilename, 'w')
      tFile.write(json.dumps(empty))
      if status != 0:
         status = 1
         output = "Empty target file written by 101worker/modules/extract101meta."

   # Create problem record if needed
   if status != 0:
      result = dict()
      result["filename"] = rFilename
      result["extractor"] = extractor
      result["status"] = status
      result["output"] = output

   # Record failure entries
   if status != 0:
      problems.append(rFilename)
   else:
      successes.append(rFilename)

   return status

print "Extracting facts from 101repo."

try:
   oldDump = json.load(open(const101.extractorDump, 'r'))
except:
   oldDump = dict()
   oldDump["extractors"] = list() 
   oldDump["problems"] = list()

extractors = set()
successes = list()
problems = list()

dump = tools101.mapMatchesWithKey("extractor", ".extractor.json", fun)

dump["extractors"] = list(extractors.union(oldDump["extractors"]))
dump["problems"] = list(set(problems).union(set(oldDump["problems"])).difference(successes))
dump["numbers"]["numberOfExtractors"] = len(dump["extractors"])
dump["numbers"]["numberOfProblems"] = len(dump["problems"])
extractorFile = open(const101.extractorDump, 'w')
extractorFile.write(json.dumps(dump))
tools101.dump(dump)
sys.exit(0)
