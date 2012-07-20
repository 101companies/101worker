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

def space2underscore(str):
   return str.replace(" ", "_")

print "Resolving entities of 101meta rules."
rules = json.load(open(const101.rulesDump, 'r'))["results"]["rules"]
terms = dict()
concepts = dict()
features = dict()
languages = dict()
technologies = dict()

for entry in rules:
   for unit in entry["rule"]["metadata"]:
      resolveEntity(unit, "concept", concepts, lambda x : const101.url101 + space2underscore(x))
      resolveEntity(unit, "language", languages, lambda x : const101.url101 + "Language:" + space2underscore(x))
      resolveEntity(unit, "dependsOn", technologies, lambda x : const101.url101 + "Technology:" + space2underscore(x))
      resolveEntity(unit, "inputOf", technologies, lambda x : const101.url101 + "Technology:" + space2underscore(x))
      resolveEntity(unit, "outputOf", technologies, lambda x : const101.url101 + "Technology:" + space2underscore(x))
      resolveEntity(unit, "partOf", technologies, lambda x : const101.url101 + "Technology:" + space2underscore(x))
      resolveEntity(unit, "term", terms, lambda x : const101.url101 + "101term:" + space2underscore(x))
      resolveEntity(unit, "feature", features, lambda x : const101.url101 + "101feature:" + space2underscore(x))

dump = dict()
dump["results"] = dict()
dump["results"]["terms"] = terms
dump["results"]["concepts"] = concepts
dump["results"]["features"] = features
dump["results"]["languages"] = languages
dump["results"]["technologies"] = technologies
dump["numbers"] = dict()
dump["numbers"]["numbersOfTerms"] = len(terms)
dump["numbers"]["numbersOfConcepts"] = len(concepts)
dump["numbers"]["numbersOfFeatures"] = len(features)
dump["numbers"]["numbersOfLanguages"] = len(languages)
dump["numbers"]["numbersOfTechnologies"] = len(technologies)
resolutionFile = open(const101.resolutionDump, 'w')
resolutionFile.write(json.dumps(dump))
sys.exit(0)
