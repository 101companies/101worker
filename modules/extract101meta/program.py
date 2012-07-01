#! /usr/bin/env python

import os
import sys
import simplejson as json
sys.path.append('../../libraries/101meta')
import const101
import tools101

# Per-file functinonality
def fun(extractor, rFilename, sFilename, tFilename):
   print "Extract facts from " + rFilename + " with " + extractor + "."
   cmd = os.path.join(const101.sRoot, extractor) + " \"" + sFilename + "\" \"" + tFilename + "\" "
   (status, output) = tools101.run(cmd)
   return status

print "Extracting facts from 101repo."
dump = tools101.mapMatchesWithKey("extractor", ".extractor.json", fun)
extractorFile = open(const101.extractorDump, 'w')
extractorFile.write(json.dumps(dump))
sys.exit(dump["noProblems"])
