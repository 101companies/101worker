#! /usr/bin/env python

import os
import sys
import simplejson as json
import commands
import re
sys.path.append('../../libraries/101meta')
import const101
import tools101

#
# Build metadata unit
#
def buildUnit(units, id, metadata):
   global noUnits
   noUnits += 1
   unit = dict()
   unit["id"] = id
   unit["metadata"] = metadata
   units.append(unit)

#
# Handle filename and basename constraints alike
#
def checkFileConstraint(rule, key, value):
   if not key in rule:
      return True
   else:
      either = False
      values = rule[key]
      if not isinstance(values, list): values = [ values ]
      for pattern in values:
         if pattern[0] != "#" or pattern[len(pattern)-1] != "#":
            if value == pattern:
               either = True
               break
         else:
            global noPattFiles
            noPattFiles += 1
            pattern = pattern[1:len(pattern)-2]
            result = re.search(pattern, value)
            if not result is None:
               either = True
               global noPattFilesOk
               noPattFilesOk += 1
               break
      return either

#
# Try one rule for the given file
#
def matchFile(rule):

   #
   # Check filename constraint
   #
   if not checkFileConstraint(rule, "filename", filename):
      return False
   
   #
   # Check basename constraint
   #
   if not checkFileConstraint(rule, "basename", basename):
      return False

   #
   # Check suffix constraint
   #      
   if "suffix" in rule:
      suffixes = rule["suffix"]
      if not isinstance(suffixes, list): suffixes = [ suffixes ]
      either = False
      for suffix in suffixes:
         if basename.endswith(suffix):
            either = True
            break
      if not either: return False

   #
   # Check content, if required.
   #
   if "content" in rule:
      global noContFiles
      noContFiles += 1
      pattern = rule["content"]
      if pattern[0]=="#" and pattern[len(pattern)-1]=="#":
         pattern = pattern[1:len(pattern)-2]
      content = open(sFilename, 'r').read()
      result = re.search(pattern, content)
      if result is None:
         return False
      else:
         global noContFilesOk
         noContFilesOk += 1
         
   #
   # Apply predicate, if present.
   #
   if "predicate" in rule:
      global noPredFiles
      noPredFiles += 1
      predicate = rule["predicate"]
      if "args" in rule:
         args = rule["args"]
         if not isinstance(args, list): args = [ args ]
      else:
         args = []
      cmd = os.path.join(const101.sRoot, predicate)
      for arg in args:
         cmd += " \"" + arg + "\""
      cmd += " \"" + sFilename + "\""
      (status, output) = commands.getstatusoutput(cmd)
      if status == 0:
         global noPredFilesOk
         noPredFilesOk += 1
      else:
         return False

   #
   # No constraint left to check
   #
   return True


#
# Try all rules for the given file and build metadata units
#
def handleFile():
   units = list() # metadata units for the file at hand
   id = 0 # current rule number
   for r in rules:
      rule = r["rule"]
      if matchFile(rule):      
         if "metadata" in rule:
            metadata = rule["metadata"]
            if isinstance(metadata, list):
               for m in metadata:
                  buildUnit(units, id, m)                    
            else:
               buildUnit(units, id, metadata)
      id += 1
      
   # Add entry to matches if any matches for file at hand
   tools101.makedirs(tDirname)
   matchesFile = open(tFilename, 'w')
   matchesFile.write(json.dumps(units))
   if len(units) > 0:
      global noFiles
      noFiles += 1
      entry = dict()
      entry["filename"] = filename
      entry["units"] = units
      matches.append(entry)


rules = json.load(open(const101.rulesDump, 'r')) # Load rules as prepared by module gather101meta
matches = list()
noFiles = 0
noUnits = 0
noPattFiles = 0
noPattFilesOk = 0 
noPredFiles = 0
noPredFilesOk = 0 
noContFiles = 0
noContFilesOk = 0
print "Matching 101meta metadata on 101repo."
for root, dirs, files in os.walk(os.path.join(const101.sRoot, "contributions")):
   if not root.startswith(os.path.join(const101.sRoot, ".git")+os.sep):
      for basename in files:
         tools101.tick()
         if not basename in [".gitignore"]:
            # Source file name
            sFilename = os.path.join(root, basename)
            # More relative file name
            filename = sFilename[len(const101.sRoot)+1:]
            dirname = os.path.dirname(filename)
            basename = os.path.basename(filename) 
            # Target file name, as used by this program
            tDirname = os.path.join(const101.tRoot, dirname)
            tFilename = os.path.join(tDirname, basename + ".matches.json")
            handleFile()
sys.stdout.write('\n')

# Store matches
matchesFile = open(const101.matchesDump, 'w')
matchesFile.write(json.dumps(matches))
matchesFile.write("\n")
print str(noFiles) + " files affected."
print str(noPattFiles) + " filename-pattern constraints checked."
print str(noPattFilesOk) + " files selected with filename-pattern constraints."
print str(noPredFiles) + " predicate constraints checked."
print str(noPredFilesOk) + " files selected with predicate constraints."
print str(noContFiles) + " content constraints checked."
print str(noContFilesOk) + " files selected with content constraints."
print str(noUnits) + " metadata units attached."
sys.exit(0)
