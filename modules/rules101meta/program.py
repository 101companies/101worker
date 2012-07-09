#! /usr/bin/env python

import os
import fnmatch
import sys
import simplejson as json
sys.path.append('../../libraries/101meta')
import const101
import tools101

# Check rule for validity
def validRule(rule):
   return \
      ("filename" in rule \
      or "basename" in rule \
      or "dirname" in rule \
      or "suffix" in rule) \
      and \
      (not "predicate" in rule \
       or not "fragment" in rule)

# Gather metrics
def countRule(rule):
   
   global suffixes
   if "suffix" in rule:
      suffix = rule["suffix"]
      if not suffix in suffixes:
         suffixes += [suffix]
         
   global predicates
   if "predicate" in rule:
      predicate = rule["predicate"]
      if not predicate in predicates:
         predicates += [predicate]

#
# Gather metrics.
# Check validity upfront.
# Qualify rule with origin information.
#
def handleRule(rule):
   countRule(rule)
   if validRule(rule):
      entry = dict()
      entry['filename'] = rFilename
      entry['rule'] = rule
      rules.append(entry)
   else:
      invalidFiles.append(rFilename)

# Prepare dump
results = dict()
rules = list()
results["rules"] = rules
errors = dict()
unreadableFiles = list()
invalidFiles = list()
errors["unreadableFiles"] = unreadableFiles
errors["invalidFiles"] = invalidFiles
numbers = dict()
numberOfFiles = 0
details = dict()
suffixes = list()
details["suffixes"] = suffixes
predicates = list()
details["predicates"] = predicates
dump = dict()
dump["results"] = rules
dump["errors"] = errors
dump["numbers"] = numbers
dump["details"] = details

# Main loop
for root, dirs, files in os.walk(const101.sRoot):
   for basename in fnmatch.filter(files, "*.101meta"):
      filename = os.path.join(root, basename)
      rFilename = filename[len(const101.sRoot)+1:] # relative file name
      numberOfFiles += 1

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
         unreadableFiles.append(rFilename)

# Completion of dump
numbers["numberOfRules"] = len(rules)
numbers["numberOfSuffixes"] = len(suffixes)
numbers["numberOfPredicates"] = len(predicates)

# Write to files and stdout
rulesFile = open(const101.rulesDump, 'w')
rulesFile.write(json.dumps(dump))
tools101.dump(dump)
sys.exit(0)
