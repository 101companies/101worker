#! /usr/bin/env python

import os
import sys
import json
import warnings
sys.path.append('../../libraries/101meta')
import const101
import tools101

def noMetrics():
   default = const101.noMetrics()
   default["relevance"] = "system"
   return default

def readOrDefault(filename, default):
   try:
      return json.load(open(filename, 'r'))
   except (IOError, ValueError):
      return default

def fun(dirname, dirs, files):
   for basename in files:
      filename = os.path.join(dirname, basename)
      f1 = os.path.join(const101.tRoot, filename + ".matches.json")
      matches = readOrDefault(f1, [])
      f2 = os.path.join(const101.tRoot, filename + ".predicates.json")
      matches += readOrDefault(f2, [])
      f3 = os.path.join(const101.tRoot, filename + ".fragments.json")
      matches += readOrDefault(f3, [])
      f4 = os.path.join(const101.tRoot, filename + ".metrics.json")
      metrics = readOrDefault(f4, noMetrics())
      f5 = os.path.join(const101.tRoot, filename + ".refinedTokens.json")
      tokens = readOrDefault(f5, [])

      try:
         tDirname  = os.path.join(const101.tRoot, dirname)
         if not os.path.exists(tDirname):
            os.makedirs(tDirname)

         tFilename = os.path.join(const101.tRoot, filename + ".summary.json")
         with open(tFilename, 'w') as tFile:
             json.dump({
                "units"         : matches,
                "metrics"       : metrics,
                "refinedTokens" : tokens,
             }, tFile)

      except Exception as e:
         warnings.warn(e)


tools101.loopOverFiles(fun, True)
