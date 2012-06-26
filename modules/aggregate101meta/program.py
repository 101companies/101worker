import os
import sys
import simplejson as json
import commands
import time

# Look up all metadata values, if any, for a certain metadata key
def valuesByKey(entry, key):
   return [ x[key]
                 for x in map(lambda u: u["metadata"], entry["units"])
                 if key in x ]

# Map some keys of a dictionary to the filename of an entry
def mapFileToKey(entry, dict, keys):
   for key in keys:
      if not key in dict: dict[key] = list()
      dict[key].append(entry["filename"])

# Get directories from argument list
if (len(sys.argv) != 4): sys.exit(-1)
repo = sys.argv[1]
matches = json.load(open(sys.argv[2], 'r')) # load 101meta matches
result = sys.argv[3]

# Go over matches and gather files by language
bylang = dict()
bytech = dict()
for entry in matches:

   # Summarize languages
   langs = valuesByKey(entry, "language")
   mapFileToKey(entry, bylang, langs)

   # Summarize technologies
   techs = valuesByKey(entry, "partOf") \
           + valuesByKey(entry, "inputOf") \
           + valuesByKey(entry, "outputOf") \
           + valuesByKey(entry, "dependsOn")
   mapFileToKey(entry, bytech, techs)

# Store summary
summary = dict()
summary["languages"] = bylang 
summary["technologies"] = bytech 
summaryFile = open(os.path.join(result, "summary.json"), 'w')
summaryFile.write(json.dumps(summary))
print str(len(bylang.keys())) + " languages in use."
print str(len(bytech.keys())) + " technologies in use."
sys.exit(0)
