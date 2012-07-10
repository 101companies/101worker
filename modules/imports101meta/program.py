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
            if not package in filesByPackage:
               filesByPackage[package] = []
            filesByPackage[package].append(filename)
            for imp in facts["imports"]:
               imported.add(package)
               if not imp in filesByImport:
                  filesByImport[imp] = []
               filesByImport[imp].append(filename)
         except IOError:
            problems.append(filename)

print "Analyzing imports for 101repo."
defined = set()
imported = set()
matched = set()
unmatched = set()
predicates = json.load(open(const101.rulesDump, 'r'))["results"]["predicates"]
matched = set()
for p in predicates:
   if p in ['technologies/Java_platform/javaImport.sh']:
      for x in predicates[p]:
         matched.add(x)
dump = dict()
filesByPackage = dict()
filesByImport = dict()
problems = []
numbers = dict()
dump["results"] = dict()
dump["problems"] = problems
dump["results"]["filesByPackage"] = filesByPackage
dump["results"]["filesByImport"] = dict()
#dump["numbers"] = numbers

tools101.loopOverFiles(fun, True)

filesByPackage = filesByPackage.items()
filesByPackage = sorted(filesByPackage, reverse=True, key=lambda (pkg, list): len(list))
filesByPackage = [ tools101.pair2json(x) for x in filesByPackage ]
dump["results"]["filesByPackage"]["all"] = filesByPackage
dump["results"]["filesByPackage"]["matched"] = []
dump["results"]["filesByPackage"]["unmatched"] = []

filesByImport = filesByImport.items()
filesByImport = sorted(filesByImport, reverse=True, key=lambda (pkg, list): len(list))
dump["results"]["filesByImport"]["all"] = [ tools101.pair2json(x) for x in filesByImport ]
dump["results"]["filesByImport"]["matched"] = []
dump["results"]["filesByImport"]["unmatched"] = []

dump["results"]["packages"] = dict()
dump["results"]["packages"]["all"] = sorted(list(defined.union(imported)))
dump["results"]["packages"]["defined"] = sorted(list(defined))
dump["results"]["packages"]["imported"] = sorted(list(imported))
dump["results"]["packages"]["matched"] = sorted(list(matched))
dump["results"]["packages"]["unmatched"] = sorted(list(imported.difference(defined).difference(matched)))

importsFile = open(const101.importsDump, 'w')
importsFile.write(json.dumps(dump))
exit(0)
