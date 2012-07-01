#! /usr/bin/env python

import os
import fnmatch
import sys
import simplejson as json
sys.path.append('../../libraries/101meta')
import const101
import tools101

#
# Qualify rule with origin information.
# Enforce priorities for rules.
#
def handleRule(rule):
   if not "filename" in rule \
      and not "basename" in rule \
      and not "dirname" in rule \
      and not "suffix" in rule:
      invalids.append(rFilename)
   else:
      entry = dict()
      entry['filename'] = rFilename
      entry['rule'] = rule
      rules.append(entry)

rules = list()
noFiles = 0
unreadables = list()
invalids = list()
for root, dirs, files in os.walk(const101.sRoot):
   for basename in fnmatch.filter(files, "*.101meta"):
      filename = os.path.join(root, basename)
      rFilename = filename[len(const101.sRoot)+1:] # relative file name
      noFiles += 1

      # Shield against JSON encoding errors
      try:        
         jsonfile = open(filename, "r")
         data = json.load(jsonfile)
 
         # Handle lists of rules
         if isinstance(data, list):
            for rule in data:
               handleRule(rule)
         else:
            handleRule(data)
         break
         
      except json.decoder.JSONDecodeError:
         print "Unreadable file: " + rFilename + " (JSONDecodeError)"
         unreadables.append(rFilename)

# Store sorted list of rules
dump = dict()
dump["rules"] = rules
dump["noFiles"] = noFiles
dump["unreadables"] = unreadables
dump["invalids"] = invalids
rulesFile = open(const101.rulesDump, 'w')
rulesFile.write(json.dumps(dump))
print str(noFiles) + " 101meta files read."
print str(len(unreadables)) + " unreadable 101meta files encountered."
print str(len(invalids)) + " invalid 101meta files encountered."
print str(len(rules)) + " 101meta rules gathered."
#sys.exit(len(unreadables)+len(invalids))
sys.exit(len(unreadables))
