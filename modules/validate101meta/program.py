#! /usr/bin/env python

import os
import sys
import json
sys.path.append('../../libraries/101meta')
import const101
import tools101

# Per-file functinonality
def fun(validator, rFilename, sFilename, tFilename):

   # Housekeeping
   global validators
   validators.add(validator) # account for validator

   # Command execution
   print "Validate " + rFilename + " with " + validator + "."
   cmd = os.path.join(const101.sRoot, validator) + " \"" + sFilename + "\""
   (status, output) = tools101.run(cmd)

   # Save validation result
   result = dict()
   result["filename"] = rFilename
   result["validator"] = validator
   result["status"] = status
   result["output"] = output
   tFile = open(tFilename, 'w')
   tFile.write(json.dumps(result))

   # Record failure entries
   if status != 0:
      failures.append(result)

   return status


validators = set()
failures = list()
print "Validating 101repo."
dump = tools101.mapMatchesWithKey("validator", ".json", fun)
print "Applied " + str(len(validators)) + " validator(s)."
print str(len(failures)) + " files failed to validate."
dump["validators"] = list(validators)
dump["failures"] = failures
validatorFile = open(const101.validatorDump, 'w')
validatorFile.write(json.dumps(dump))
sys.exit(dump["noProblems"])
