#! /usr/bin/env python

import sys
import simplejson as json
sys.path.append('../../libraries/101meta')
import const101
import matches101
mr = matches101.matchAll(2, ".predicates.json")
mrFile = open(const101.predicatesDump, 'w')
mrFile.write(json.dumps(mr))
print str(matches101.noPredFiles) + " predicate constraints checked."
print str(matches101.noPredFilesOk) + " files selected with predicate constraints."
sys.exit(0)
