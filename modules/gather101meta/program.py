import os
import fnmatch
import sys
import simplejson as json

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

# Get directories from argument list
if (len(sys.argv) != 3): sys.exit(-1)
repo = sys.argv[1]
result = sys.argv[2]

# Prepare lists of rules
firstlist = list() # rules without "predicate" and "fragment"
secondlist = list() # other rules

# Find and process all ".101meta" files
for root, dirs, files in os.walk(repo):
   for basename in fnmatch.filter(files, "*.101meta"):
      filename = os.path.join(root, basename)
      rFilename = filename[len(repo)+1:] # relative file name

      # Shield against JSON encoding errors
      try:        
         jsonfile = open(filename, "r")
         data = json.load(jsonfile)
         print rFilename + ": OK"

         # Handle lists of rules
         if isinstance(data, list):
            for rule in data:
               handleRule(rule)
         else:
            handleRule(data)
         break
         
      except json.decoder.JSONDecodeError:
         print rFilename + ": FAIL (JSONDecodeError)"

# Store sorted list of rules
rulesFile = open(os.path.join(result, "rules.json"), 'w')
rulesFile.write(json.dumps(firstlist + secondlist))
rulesFile.write("\n")
sys.exit(0)
