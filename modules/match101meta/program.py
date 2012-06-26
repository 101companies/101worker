import os
import sys
import simplejson as json
import commands
import re

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
   if not checkFileConstraint(rule, "filename", eFilename):
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
      content = open(iFilename, 'r').read()
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
      cmd = os.path.join(repo, predicate)
      for arg in args:
         cmd += " \"" + arg + "\""
      cmd += " \"" + iFilename + "\""
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
   if len(units) > 0:
      global noFiles
      noFiles += 1
      entry = dict()
      entry["filename"] = eFilename
      entry["units"] = units
      matches.append(entry)

# Get directories from argument list
if (len(sys.argv) != 3): sys.exit(-1)
repo = sys.argv[1]
result = sys.argv[2]

# Load 101meta rules as prepared by module gather101meta
rules = json.load(open(os.path.join(result, "rules.json"), 'r'))

# Find and process (almost) all files
matches = list()
noFiles = 0
noUnits = 0
noPattFiles = 0
noPattFilesOk = 0 
noPredFiles = 0
noPredFilesOk = 0 
noContFiles = 0
noContFilesOk = 0 
for root, dirs, files in os.walk(os.path.join(repo, "contributions")):
   if not root.startswith(os.path.join(repo, ".git")+os.sep):
      for basename in files:
         sys.stdout.write('.')
         sys.stdout.flush()
         if not basename in [".gitignore"]:
            # INTERNAL file name, as used by this program
            iFilename = os.path.join(root, basename)
            # EXTERNAL file name, as assumed by the rules
            eFilename = iFilename[len(repo)+1:]
            handleFile()
sys.stdout.write('\n')

# Store matches
matchesFile = open(os.path.join(result, "matches.json"), 'w')
matchesFile.write(json.dumps(matches))
matchesFile.write("\n")
print str(noFiles) + " files affected."
print str(noPattFiles) + " files checked with filename pattern constraint."
print str(noPattFilesOk) + " files selected with filename pattern constraint."
print str(noPredFiles) + " files checked with predicate constraint."
print str(noPredFilesOk) + " files selected with predicate constraint."
print str(noContFiles) + " files checked with content constraint."
print str(noContFilesOk) + " files selected with content constraint."
print str(noUnits) + " metadata units attached."
sys.exit(0)
