import os
import sys
import simplejson as json
import commands
sys.path.append('../../libraries/101meta')
import matches101
import tools101

# Get directories from argument list
if (len(sys.argv) != 4): sys.exit(-1)
repo = sys.argv[1]
matches = json.load(open(sys.argv[2], 'r')) # load 101meta matches
result = sys.argv[3]

# Accumulate non-successful exit codes
exitcode = 0

# Go over matches to find validation opportunities
validations = 0
validators = set()
failures = list()
for entry in matches:

   # Look up validator
   validator = matches101.valuesByKey(entry, "validator")

   # Continue if validator is missing or ambiguous
   if len(validator) != 1: continue   
   validator = validator[0]
   validators.add(validator)

   # RELATIVE dirname and filename
   rFilename = entry["filename"]
   rDirname = os.path.dirname(rFilename)
   basename = os.path.basename(rFilename)

   # SOURCE dirname and filename
   sDirname = os.path.join(repo, rDirname)
   sFilename = os.path.join(sDirname, basename)

   # Run validator and report problems, if any
   validations += 1
   tools101.tick()
   cmd = os.path.join(repo, validator) + " \"" + sFilename + "\""
   status = tools101.run(cmd)
   if status != 0:
      if exitcode == 0: exitcode = status
      entry = dict()
      entry["filename"] = rFilename
      entry["validator"] = validator
      failures.append(entry)
sys.stdout.write('\n')

failuresFile = open(os.path.join(result, "validation.json"), 'w')
failuresFile.write(json.dumps(failures))
print "Validated " + str(validations) + " files."
print "Applied " + str(len(validators)) + " validator(s)."
print str(len(failures)) + " files failed to validate."
sys.exit(exitcode)
