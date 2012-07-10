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
   result["validator"] = validator
   result["status"] = status
   result["output"] = output
   tFile = open(tFilename, 'w')
   tFile.write(json.dumps(result))

   # Record failure entries
   if status != 0:
      problems.append(rFilename)
   else:
      successes.append(rFilename)

   return status

try:
   oldDump = json.load(open(const101.validatorDump, 'r'))
except:
   oldDump = dict()
   oldDump["validators"] = list() 
   oldDump["problems"] = list()

validators = set()
successes = list()
problems = list()
print "Validating 101repo."
dump = tools101.mapMatchesWithKey("validator", ".validator.json", fun)
dump["validators"] = list(validators.union(oldDump["validators"]))
dump["problems"] = list(set(problems).union(set(oldDump["problems"])).difference(successes))
dump["numbers"]["numberOfValidators"] = len(dump["validators"])
dump["numbers"]["numberOfProblems"] = len(dump["problems"])
validatorFile = open(const101.validatorDump, 'w')
validatorFile.write(json.dumps(dump))
tools101.dump(dump)
sys.exit(0)
