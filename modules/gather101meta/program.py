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
   entry = dict()
   entry['filename'] = rFilename
   entry['rule'] = rule
   if ("predicate" in rule or "fragment" in rule):
      secondlist.append(entry)
   else:
      firstlist.append(entry)

# Prepare lists of rules
firstlist = list() # rules without "predicate" and "fragment"
secondlist = list() # other rules

# Find and process all ".101meta" files
oks = 0
fails = 0
for root, dirs, files in os.walk(const101.sRoot):
   for basename in fnmatch.filter(files, "*.101meta"):
      filename = os.path.join(root, basename)
      rFilename = filename[len(const101.sRoot)+1:] # relative file name

      # Shield against JSON encoding errors
      try:        
         jsonfile = open(filename, "r")
         data = json.load(jsonfile)
         print rFilename + ": OK"
         oks += 1

         # Handle lists of rules
         if isinstance(data, list):
            for rule in data:
               handleRule(rule)
         else:
            handleRule(data)
         break
         
      except json.decoder.JSONDecodeError:
         print rFilename + ": FAIL (JSONDecodeError)"
         raise
         fails += 1

# Store sorted list of rules
rulesFile = open(const101.rulesDump, 'w')
rules = firstlist + secondlist
rulesFile.write(json.dumps(rules))
rulesFile.write("\n")
print str(oks) + " 101meta files read with success."
print str(fails) + " 101meta files read with failure."
print str(len(rules)) + " 101meta rules gathered."
sys.exit(fails)
