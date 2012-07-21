#! /usr/bin/env python

import os
import sys
import simplejson as json
import re
sys.path.append('../../libraries/101meta')
import const101
import tools101

def eliminate(pat, str):
   while True:
      c = re.compile(pat)
      m = c.match(str)
      if m is None:
         break
      str = ""
      for x in m.groups():
         str += x
   return str

def noMarkup(str):
   str = eliminate('(.*)\[\[.*\|(.*)\]\](.*)', str)
   str = eliminate('(.*)\[\[(.*)\]\](.*)', str)
   str = eliminate('(.*):Category:(.*)', str)
   return str

def resolveEntity(unit, key, map, resolve):
   if key in unit:
      val = unit[key]
      if not val in map:
         url = const101.url101 + resolve(val)
         entity = dict()
         entity["url"] = url
         if url in headline:
            entity["headline"] = headline[url]
         else:
            entity["headline"] = "<unresolved>"
            problems.append(url)
         map[val] = entity

def space2underscore(str):
   return str.replace(" ", "_")

print "Resolving entities of 101meta rules."
rules = json.load(open(const101.rulesDump, 'r'))["results"]["rules"]
wiki = json.load(open(const101.wikiDump, 'r'))

# Map URLs to headlines
headline = dict()
for k1 in wiki:
   section = wiki[k1]
   for k2 in section:
      url = space2underscore(section[k2]["url"])
      headline[url] = noMarkup(section[k2]["headline"])

terms = dict()
concepts = dict()
features = dict()
languages = dict()
technologies = dict()
results = dict()
results["terms"] = terms
results["concepts"] = concepts
results["features"] = features
results["languages"] = languages
results["technologies"] = technologies
problems = list()

for entry in rules:
   for unit in entry["rule"]["metadata"]:
      resolveEntity(unit, "concept", concepts, lambda x : space2underscore(x))
      resolveEntity(unit, "language", languages, lambda x : "Language:" + space2underscore(x))
      resolveEntity(unit, "dependsOn", technologies, lambda x : "Technology:" + space2underscore(x))
      resolveEntity(unit, "inputOf", technologies, lambda x : "Technology:" + space2underscore(x))
      resolveEntity(unit, "outputOf", technologies, lambda x : "Technology:" + space2underscore(x))
      resolveEntity(unit, "partOf", technologies, lambda x : "Technology:" + space2underscore(x))
      resolveEntity(unit, "term", terms, lambda x : "101term:" + space2underscore(x))
      resolveEntity(unit, "feature", features, lambda x : "101feature:" + space2underscore(x))

dump = dict()
dump["results"] = results
dump["numbers"] = dict()
dump["numbers"]["numbersOfTerms"] = len(terms)
dump["numbers"]["numbersOfConcepts"] = len(concepts)
dump["numbers"]["numbersOfFeatures"] = len(features)
dump["numbers"]["numbersOfLanguages"] = len(languages)
dump["numbers"]["numbersOfTechnologies"] = len(technologies)
dump["problems"] = problems
resolutionFile = open(const101.resolutionDump, 'w')
resolutionFile.write(json.dumps(dump))
tools101.dump(dump)
sys.exit(0)
