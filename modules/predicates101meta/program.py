#! /usr/bin/env python

import sys
import simplejson as json
sys.path.append('../../libraries/101meta')
import const101
import matches101
mr = matches101.matchAll("predicates", ".predicates.json")
mrFile = open(const101.predicatesDump, 'w')
mrFile.write(json.dumps(mr))
print str(matches101.noPredicateConstraints) + " predicate constraints checked."
print str(matches101.noPredicateConstraintsOk) + " predicate constraints succeeded."
sys.exit(0)
