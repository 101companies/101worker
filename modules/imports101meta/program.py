#! /usr/bin/env python

import os
import os.path
import sys
import json
sys.path.append('../../libraries/101meta')
import const101
import tools101

def fun(dirname, dirs, files):
   for basename in files:
      filename = os.path.join(dirname, basename)
      matchesFilename = os.path.join(const101.tRoot, filename + '.matches.json')
      try:
         matches = json.load(open(matchesFilename, 'r'))
      except IOError:
         matches = []
      if tools101.valuesByKey(matches, "extractor"):
         factFilename = os.path.join(const101.tRoot, filename + '.extractor.json')
         try:
            facts = json.load(open(factFilename, 'r'))
            for imp in facts["imports"]:
               if not imp in filesByImport:
                  filesByImport[imp] = []
               filesByImport[imp].append(filename)
         except IOError:
            problems.append(filename)

print "Analyzing imports for 101repo."
predicates = json.load(open(const101.rulesDump, 'r'))["results"]["predicates"]
dump = dict()
filesByPackage = dict()
filesByImport = dict()
problems = []
numbers = dict()
dump["filesByPackage"] = filesByPackage
dump["filesByImport"] = dict()
dump["problems"] = problems
#dump["numbers"] = numbers
tools101.loopOverFiles(fun, True)
filesByImport = filesByImport.items()
filesByImport = sorted(filesByImport, reverse=True, key=lambda (pkg, list): len(list))
filesByImport = [ tools101.pair2json(x) for x in filesByImport ]
dump["filesByImport"]["all"] = filesByImport
dump["filesByImport"]["matched"] = []
dump["filesByImport"]["unmatched"] = []

#dump["filesBySuffix"] = dict()
#dump["filesBySuffix"]["all"] = filesBySuffix
#dump["filesBySuffix"]["matched"] = [ x for x in filesBySuffix if x[0] in suffixes ]
#dump["filesBySuffix"]["unmatched"] = [ x for x in filesBySuffix if not x[0] in suffixes ]

#dump["numbersBySuffix"] = dict()
#dump["numbersBySuffix"]["all"] = [ (x, len(y)) for (x, y) in filesBySuffix ]
#dump["numbersBySuffix"]["matched"] = [ (x, len(y)) for (x, y) in filesBySuffix if x in suffixes ]
#dump["numbersBySuffix"]["unmatched"] = [ (x, len(y)) for (x, y) in filesBySuffix if not x in suffixes ]

#dump["numbersOfSuffixes"] = dict()
#dump["numbersOfSuffixes"]["all"] = len(dump["filesBySuffix"]["all"])
#dump["numbersOfSuffixes"]["matched"] = len(dump["filesBySuffix"]["matched"])
#dump["numbersOfSuffixes"]["unmatched"] = len(dump["filesBySuffix"]["unmatched"])
#tools101.dump(dump,"numbersOfSuffixes")
importsFile = open(const101.importsDump, 'w')
importsFile.write(json.dumps(dump))
exit(0)
