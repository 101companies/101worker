#! /usr/bin/env python

import os
import sys
import json
sys.path.append('../../libraries/101meta')
import const101
import tools101

def readOrDefault(filename, default):
   try:
      return json.load(open(filename, 'r'))
   except IOError:
      return default

def fun(dirname, dirs, files):
   for basename in files:
      tools101.tick()
      filename = os.path.join(dirname, basename)
      f1 = os.path.join(const101.tRoot, filename + ".matches.json")
      matches = readOrDefault(f1, [])
      f2 = os.path.join(const101.tRoot, filename + ".predicates.json")
      matches += readOrDefault(f2, [])
      f3 = os.path.join(const101.tRoot, filename + ".fragments.json")
      matches += readOrDefault(f3, [])
      f4 = os.path.join(const101.tRoot, filename + ".metrics.json")
      metrics = readOrDefault(f4, const101.noMetrics())
      tFilename = os.path.join(const101.tRoot, filename + ".summary.json")
      tFile = open(tFilename, 'w')
      dump = dict()
      dump["units"] = matches
      dump["metrics"] = metrics
      tFile.write(json.dumps(dump))

print "Summarizing 101repo."
tools101.loopOverFiles(fun, True)
print ""
exit(0)
