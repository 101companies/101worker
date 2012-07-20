#! /usr/bin/env python

import os
import sys
import simplejson as json
sys.path.append('../../libraries/101meta')
import const101
import tools101

def resolveEntity(unit, key, map, resolve):
   if key in unit:
      val = unit[key]
      if not val in map:
         map[val] = resolve(val)

print "Resolving entities of 101meta rules."
rules = json.load(open(const101.rulesDump, 'r'))["results"]["rules"]
languages = dict()
technologies = dict()

for entry in rules:
   for unit in entry["rule"]["metadata"]:
      resolveEntity(unit, "language", languages, lambda x : const101.url101 + "Language:" + x)
      resolveEntity(unit, "dependsOn", technologies, lambda x : const101.url101 + "Technology:" + x)
      resolveEntity(unit, "inputOf", technologies, lambda x : const101.url101 + "Technology:" + x)
      resolveEntity(unit, "outputOf", technologies, lambda x : const101.url101 + "Technology:" + x)
      resolveEntity(unit, "partOf", technologies, lambda x : const101.url101 + "Technology:" + x)

dump = dict()
dump["results"] = dict()
dump["results"]["languages"] = languages
dump["results"]["technologies"] = technologies
dump["numbers"] = dict()
dump["numbers"]["numbersOfLanguages"] = len(languages)
dump["numbers"]["numbersOfTechnologies"] = len(technologies)
resolutionFile = open(const101.resolutionDump, 'w')
resolutionFile.write(json.dumps(dump))
sys.exit(0)
