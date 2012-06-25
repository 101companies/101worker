import os
import fnmatch
import sys
import simplejson as json

def buildUnit(units, id, metadata):
   unit = dict()
   unit["id"] = id
   unit["metadata"] = metadata
   units.append(unit)

#
# Perform matching per file
#
def handleFile(rules, matches, basename, ifilename, efilename):

   units = list() # metadata units for the file at hand

   # Try all rules for file at hand
   id = 0
   for r in rules:
      rule = r["rule"]
      if "suffix" in rule:
         if basename.endswith(rule["suffix"]):
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
      entry = dict()
      entry["filename"] = efilename
      entry["units"] = units
      matches.append(entry)

# Get directories from argument list
if (len(sys.argv) != 3): sys.exit(-1)
repo = sys.argv[1]
result = sys.argv[2]
rules = json.load(open(os.path.join(result, "rules.json"), 'r'))

# Find and process (almost) all files
matches = list()
for root, dirs, files in os.walk(repo):
   if not root.startswith(os.path.join(repo, ".git")+os.sep):
      for basename in files:
         if not basename in [".gitignore"]:
            ifilename = os.path.join(root, basename)
            efilename = ifilename[len(repo)+1:]
            handleFile(rules, matches, basename, ifilename, efilename)

# Store matches
matchesFile = open(os.path.join(result, "matches.json"), 'w')
matchesFile.write(json.dumps(matches))
matchesFile.write("\n")
sys.exit(0)
