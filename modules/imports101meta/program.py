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
            package = facts["package"]
            defined.add(package)
            if not package in filesByDef:
               filesByDef[package] = []
            filesByDef[package].append(filename)
            for imp in facts["imports"]:
               used.add(imp)
               if not imp in filesByUse:
                  filesByUse[imp] = []
               filesByUse[imp].append(filename)
         except IOError:
            problems.append(filename)

print "Analyzing imports for 101repo."
defined = set()
used = set()
matched = set()
predicates = json.load(open(const101.rulesDump, 'r'))["results"]["predicates"]
for p in predicates:
   if p in ['technologies/Java_platform/javaImport.sh']:
      for x in predicates[p]:
         matched.add(x)
filesByDef = dict()
filesByUse = dict()
problems = []

tools101.loopOverFiles(fun, True)

both = defined.union(used)
unmatched = used.difference(defined).difference(matched)

numbers = dict()
dump = dict()
dump["results"] = dict()
dump["problems"] = problems
dump["numbers"] = numbers

dump["results"]["packages"] = dict()
dump["results"]["packages"]["allPackages"] = sorted(list(both))
dump["results"]["packages"]["definedPackages"] = sorted(list(defined))
dump["results"]["packages"]["usedPackages"] = sorted(list(used))
dump["results"]["packages"]["matchedPackages"] = sorted(list(matched))
dump["results"]["packages"]["unmatchedPackages"] = sorted(list(unmatched))

filesByDef = filesByDef.items()
filesByDef = sorted(filesByDef, reverse=True, key=lambda (pkg, list): len(list))
dump["results"]["filesByDef"] = dict()
dump["results"]["filesByDef"]["allFiles"] = [ tools101.pair2json(x) for x in filesByDef ]
dump["results"]["filesByDef"]["matchedFiles"] = [ tools101.pair2json(x) for x in filesByDef if x[0] in matched ]
dump["results"]["filesByDef"]["unmatchedFiles"] = [ tools101.pair2json(x) for x in filesByDef if x[0] in unmatched ]

filesByUse = filesByUse.items()
filesByUse = sorted(filesByUse, reverse=True, key=lambda (pkg, list): len(list))
dump["results"]["filesByUse"] = dict()
dump["results"]["filesByUse"]["allFiles"] = [ tools101.pair2json(x) for x in filesByUse ]
dump["results"]["filesByUse"]["matchedFiles"] = [ tools101.pair2json(x) for x in filesByUse if x[0] in matched ]
dump["results"]["filesByUse"]["unmatchedFiles"] = [ tools101.pair2json(x) for x in filesByUse if x[0] in unmatched ]

dump["numbers"]["numberOfPackages"] = len(both)
dump["numbers"]["numberOfDefinedPackages"] = len(defined)
dump["numbers"]["numberOfUsedPackages"] = len(used)
dump["numbers"]["numberOfMatchedPackages"] = len(matched)
dump["numbers"]["numberOfUnmatchedPackages"] = len(unmatched)

importsFile = open(const101.importsDump, 'w')
importsFile.write(json.dumps(dump))
exit(0)
