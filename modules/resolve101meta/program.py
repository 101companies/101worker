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
   str = eliminate('(.*)Language:(.*)', str)
   str = eliminate('(.*)Technology:(.*)', str)
   return str


def resolveEntity(val, map, uriResolve, fileResolve):
   if not val in map:
      url101wiki = const101.url101wiki + space2underscore(uriResolve(val))
      entity = dict()
      entity["101wiki"] = url101wiki
      if not fileResolve is None:
         rDirname = space2underscore(fileResolve(val))
         aDirname = os.path.join(const101.sRoot,rDirname)
         if os.path.exists(aDirname):
            url101repo = const101.url101repo + rDirname
            entity["101repo"] = url101repo
      if url101wiki in headline:
         entity["headline"] = headline[url101wiki]
         if entity["headline"] == "":
            entity["headline"] == "empty"
            problem = dict()
            problem["missingWikiHeadline"] = url101wiki 
            problems.append(problem)
      else:
         entity["headline"] = "<unresolved>"
         problem = dict()
         problem["missingWikiPage"] = url101wiki 
         problems.append(problem)
      map[val] = entity


def handleMention(unit, key, map, uriResolve, fileResolve):
   if key in unit:
      val = unit[key]
      resolveEntity(val, map, uriResolve, fileResolve)

         
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
contributions = dict()
results = dict()
results["terms"] = terms
results["concepts"] = concepts
results["features"] = features
results["languages"] = languages
results["technologies"] = technologies
results["contributions"] = contributions
problems = list()

for entry in rules:
   rule = entry["rule"]
   if "filename" in rule:
      filename = rule["filename"]
      if not filename.startswith("#") or not filename.endswith("#"):
         pat = re.compile('contributions/([^/]*)/.*')
         res = re.match(pat, filename)
         if not res is None:
            val = res.group(1)
            resolveEntity(val, contributions, lambda x : "101implementation:" + x, lambda x : "contributions/" + x)
   for unit in rule["metadata"]:
      tRes1 = lambda x : "Technology:" + x
      tRes2 = lambda x : "technologies/" + x
      handleMention(unit, "concept", concepts, lambda x : x, None)
      handleMention(unit, "language", languages, lambda x : "Language:" + x, lambda x : "languages/" + x)
      handleMention(unit, "dependsOn", technologies, tRes1, tRes2)
      handleMention(unit, "inputOf", technologies, tRes1, tRes2)
      handleMention(unit, "outputOf", technologies, tRes1, tRes2)
      handleMention(unit, "partOf", technologies, tRes1, tRes2)
      handleMention(unit, "term", terms, lambda x : "101term:" + x, None)
      handleMention(unit, "feature", features, lambda x : "101feature:" + x, None)

dump = dict()
dump["results"] = results
dump["numbers"] = dict()
dump["numbers"]["numbersOfTerms"] = len(terms)
dump["numbers"]["numbersOfConcepts"] = len(concepts)
dump["numbers"]["numbersOfFeatures"] = len(features)
dump["numbers"]["numbersOfLanguages"] = len(languages)
dump["numbers"]["numbersOfTechnologies"] = len(technologies)
dump["numbers"]["numbersOfContributions"] = len(contributions)
dump["problems"] = problems
resolutionFile = open(const101.resolutionDump, 'w')
resolutionFile.write(json.dumps(dump))
tools101.dump(dump)
sys.exit(0)
