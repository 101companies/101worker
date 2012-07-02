#! /usr/bin/env python

import os
import sys
import json
sys.path.append('../../libraries/101meta')
import const101
import tools101

def readOrEmptyList(filename):
   return json.load(open(filename, 'r'))


def fun(dirname, dirs, files):
   for basename in files:
      tools101.tick()
      filename = os.path.join(dirname, basename)
      m1 = os.path.join(const101.tRoot, filename + ".matches.json")
      matches = readOrEmptyList(m1)
      m2 = os.path.join(const101.tRoot, filename + ".predicates.json")
      matches += readOrEmptyList(m2)
      m3 = os.path.join(const101.tRoot, filename + ".fragments.json")
      matches += readOrEmptyList(m3)
      tFilename = os.path.join(const101.tRoot, filename + ".summary.json")
      tFile = open(tFilename, 'w')
      dump = dict()
      dump["units"] = matches
      tFile.write(json.dumps(dump))

print "Summarizing 101repo."
tools101.loopOverFiles(fun, True)
print ""
exit(0)
