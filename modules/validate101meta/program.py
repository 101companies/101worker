#! /usr/bin/env python

import os
import sys
import json
sys.path.append('../../libraries/101meta')
import const101
import tools101


# Per-file functinonality
def check(validator, rFilename, sFilename):

   # Housekeeping for validator
   validators.add(validator)

   # Command execution
   print "Validate " + rFilename + " with " + validator + "."
   command = os.path.join(const101.sRoot, validator) + " \"" + sFilename + "\""
   (status, output) = tools101.run(command)

   # Result aggregation
   result = dict()
   result["validator"] = validator
   result["command"] = command
   result["status"] = status
   result["output"] = output

   return result


print "Validating 101repo."

# Initialize housekeeping
validators = set()
dump = tools101.beforeMapMatches(const101.validatorDump)
if "validators" in dump:
   validators = set(dump["validators"])

# Loop over matches
tools101.checkByKey("validator", ".validator.json", check)

# Convert set to list before dumping JSON
validators = list(validators)

# Assemble dump, save it, and exit
dump = dict()
dump["validators"] = validators
dump["numbers"] = dict()
dump["numbers"]["numberOfValidators"] = len(validators)
tools101.afterMapMatches(dump, const101.validatorDump)
