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
               imported.add(imp)
               if not imp in filesByUse:
                  filesByUse[imp] = []
               filesByUse[imp].append(filename)
         except IOError:
            problems.append(filename)

print "Analyzing imports for 101repo."
defined = set()
imported = set()
matched = set()
predicates = json.load(open(const101.rulesDump, 'r'))["results"]["predicates"]
matched = set()
for p in predicates:
   if p in ['technologies/Java_platform/javaImport.sh']:
      for x in predicates[p]:
         matched.add(x)
dump = dict()
filesByDef = dict()
filesByUse = dict()
problems = []
numbers = dict()
dump["results"] = dict()
dump["problems"] = problems
dump["results"]["filesByDef"] = filesByDef
dump["results"]["filesByUse"] = dict()
#dump["numbers"] = numbers

tools101.loopOverFiles(fun, True)

unmatched = imported.difference(defined).difference(matched)

dump["results"]["packages"] = dict()
dump["results"]["packages"]["all"] = sorted(list(defined.union(imported)))
dump["results"]["packages"]["defined"] = sorted(list(defined))
dump["results"]["packages"]["used"] = sorted(list(imported))
dump["results"]["packages"]["matched"] = sorted(list(matched))
dump["results"]["packages"]["unmatched"] = sorted(list(unmatched))

filesByDef = filesByDef.items()
filesByDef = sorted(filesByDef, reverse=True, key=lambda (pkg, list): len(list))
dump["results"]["filesByDef"]["all"] = [ tools101.pair2json(x) for x in filesByDef ]
dump["results"]["filesByDef"]["matched"] = [ tools101.pair2json(x) for x in filesByDef if x[0] in matched ]
dump["results"]["filesByDef"]["unmatched"] = [ tools101.pair2json(x) for x in filesByDef if x[0] in unmatched ]

filesByUse = filesByUse.items()
filesByUse = sorted(filesByUse, reverse=True, key=lambda (pkg, list): len(list))
dump["results"]["filesByUse"]["all"] = [ tools101.pair2json(x) for x in filesByUse ]
dump["results"]["filesByUse"]["matched"] = [ tools101.pair2json(x) for x in filesByUse if x[0] in matched ]
dump["results"]["filesByUse"]["unmatched"] = [ tools101.pair2json(x) for x in filesByUse if x[0] in unmatched ]

importsFile = open(const101.importsDump, 'w')
importsFile.write(json.dumps(dump))
exit(0)
