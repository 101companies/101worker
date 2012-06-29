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
def matchFile(phase, dirname, basename, rule):

   #
   # Check whether there is a predicate constraint
   #      
   if "predicate" in rule:
       if phase==1:
           return False
       else:
           predicate = rule["predicate"]


   #
   # Check filename constraint
   #
   if not checkFileConstraint(rule, "filename", os.path.join(dirname, basename)):
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
      content = open(os.path.join(const101.sRoot, dirname, basename), 'r').read()
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
      if "args" in rule:
         args = rule["args"]
         if not isinstance(args, list): args = [ args ]
      else:
         args = []
      cmd = os.path.join(const101.sRoot, predicate)
      for arg in args:
         cmd += " \"" + arg + "\""
      cmd += " \"" + os.path.join(const101.sRoot, dirname, basename) + "\""
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
def handleFile(phase, dirname, basename):
   units = list() # metadata units for the file at hand
   id = 0 # current rule number
   for r in rules:
      rule = r["rule"]
      if matchFile(phase, dirname, basename, rule):      
         if "metadata" in rule:
            metadata = rule["metadata"]
            if isinstance(metadata, list):
               for m in metadata:
                  buildUnit(units, id, m)                    
            else:
               buildUnit(units, id, metadata)
      id += 1
      
   # Add entry to matches if any matches for file at hand
#   tools101.makedirs(os.path.join(tRoot, dirname))
#   matchesFile = open(os.path.join(tRoot, dirname, basename), 'w')
#   matchesFile.write(json.dumps(units))
   if len(units) > 0:
      global noUnits
      global noFiles
      noUnits += len(units)
      noFiles += 1
      entry = dict()
      entry["filename"] = os.path.join(dirname, basename)
      entry["units"] = units
      matches.append(entry)


#
# Process all rules and files
#
def matchAll(phase):
    global rules
    global matches
    global noFiles
    global noUnits
    global noPattFiles
    global noPattFilesOk
    global noPredFiles
    global noPredFilesOk
    global noContFiles
    global noContFilesOk
    rules = json.load(open(const101.rulesDump, 'r'))
    matches = list()
    noFiles = 0
    noUnits = 0
    noPattFiles = 0
    noPattFilesOk = 0 
    noPredFiles = 0
    noPredFilesOk = 0 
    noContFiles = 0
    noContFilesOk = 0
    print "Matching 101meta metadata on 101repo (phase " + str(phase)+ ")."
    for root, dirs, files in os.walk(os.path.join(const101.sRoot, "contributions")):
        if not root.startswith(os.path.join(const101.sRoot, ".git")+os.sep):
            for basename in files:
                tools101.tick()
                if not basename in [".gitignore"]:
                    dirname = root[len(const101.sRoot)+1:]
                    handleFile(phase, dirname, basename)
    sys.stdout.write('\n')
    mr = dict()
    mr["matches"] = matches
    mr["rules"] = rules
    print str(noFiles) + " files affected."
    print str(noUnits) + " metadata units attached."
    print str(noPattFiles) + " filename-pattern constraints checked."
    print str(noPattFilesOk) + " files selected with filename-pattern constraints."
    print str(noContFiles) + " content constraints checked."
    print str(noContFilesOk) + " files selected with content constraints."
    return mr
