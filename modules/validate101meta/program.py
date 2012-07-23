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
   result["filename"] = rFilename
   result["validator"] = validator
   result["command"] = command
   result["status"] = status
   result["output"] = output
   return result


print "Validating 101repo."

# Set up old dump as starting point for incremental operation
try:
   dump = json.load(open(const101.validatorDump, 'r'))
   validators = set(dump["validators"])
   problems = dump["problems"]
   numberOfSuccesses = dump["numbers"]["numberOfSuccesses"]
   numberOfFailures = dump["numbers"]["numberOfFailures"]

# Start from initial state if old dump is missing 
except IOError:
   validators = set()
   problems = list()
   numberOfSuccesses = 0
   numberOfFailures = 0

tools101.checkByKey("validator", ".validator.json", check)

# Convert set to list before dumping JSON
validators = list(validators)

# Assemble dump
dump = dict()
dump["validators"] = validators
dump["problems"] = problems
dump["numbers"] = dict()
dump["numbers"]["numberOfValidators"] = len(validators)
dump["numbers"]["numberOfSuccesses"] = numberOfSuccesses
dump["numbers"]["numberOfFailures"] = numberOfFailures

# Write dump with preview to stdout and exit
validatorFile = open(const101.validatorDump, 'w')
validatorFile.write(json.dumps(dump))
tools101.dump(dump)
sys.exit(0)
