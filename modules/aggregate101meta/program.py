#! /usr/bin/env python

import os
import sys
import simplejson as json
import commands
import time
sys.path.append('../../libraries/101meta')
import const101
import tools101

# Map some keys of a dictionary to the filename of an entry
def mapFileToKey(entry, dict, keys):
   for key in keys:
      if not key in dict: dict[key] = list()
      dict[key].append(entry["filename"])

# Go over matches and gather files by language
matches = json.load(open(const101.matchesDump, 'r'))["matches"]
bylang = dict()
bytech = dict()
for entry in matches:

   # Summarize languages
   langs = tools101.valuesByKey(entry, "language")
   mapFileToKey(entry, bylang, langs)

   # Summarize technologies
   techs = tools101.valuesByKey(entry, "partOf") \
           + tools101.valuesByKey(entry, "inputOf") \
           + tools101.valuesByKey(entry, "outputOf") \
           + tools101.valuesByKey(entry, "dependsOn")
   mapFileToKey(entry, bytech, techs)

# Store summary
summary = dict()
summary["languages"] = bylang 
summary["technologies"] = bytech 
summaryFile = open(const101.summaryDump, 'w')
summaryFile.write(json.dumps(summary))
print str(len(bylang.keys())) + " languages in use."
print str(len(bytech.keys())) + " technologies in use."
sys.exit(0)
