#! /usr/bin/env python

import os
import sys
import simplejson as json
sys.path.append('../../libraries/101meta')
import const101
import tools101


# Per-file functinonality
def derive(extractor, rFilename, sFilename, tFilename):

   # Housekeeping for extractor
   extractors.add(extractor)
   
   print "Extract facts from " + rFilename + " with " + extractor + "."
   command = os.path.join(const101.sRoot, extractor) + " \"" + sFilename + "\" \"" + tFilename + "\" "
   (status, output) = tools101.run(command)

   # Result aggregation
   result = dict()
   result["extractor"] = extractor
   result["command"] = command
   result["status"] = status
   result["output"] = output

   return result


print "Extracting facts from 101repo."

# Initialize housekeeping
extractors = set()
dump = tools101.beforeMapMatches(const101.extractorDump)
if "extractors" in dump:
   extractors = set(dump["extractors"])

# Loop over matches
dump = tools101.deriveByKey("extractor", ".extractor.json", derive)

# Convert set to list before dumping JSON
extractors = list(extractors)

# Assemble dump, save it, and exit
dump = dict()
dump["extractors"] = extractors
dump["numbers"] = dict()
dump["numbers"]["numberOfExtractors"] = len(extractors)
tools101.afterMapMatches(dump, const101.extractorDump)
