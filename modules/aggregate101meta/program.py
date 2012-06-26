import os
import sys
import simplejson as json
import commands
import time
sys.path.append('../../libraries/101meta')
import matches101

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
   langs = matches101.valuesByKey(entry, "language")
   mapFileToKey(entry, bylang, langs)

   # Summarize technologies
   techs = matches101.valuesByKey(entry, "partOf") \
           + matches101.valuesByKey(entry, "inputOf") \
           + matches101.valuesByKey(entry, "outputOf") \
           + matches101.valuesByKey(entry, "dependsOn")
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
