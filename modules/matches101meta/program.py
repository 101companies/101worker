#! /usr/bin/env python

import sys
import simplejson as json
sys.path.append('../../libraries/101meta')
import const101
import matches101
mr = matches101.matchAll(1, ".matches.json")
mrFile = open(const101.matchesDump, 'w')
mrFile.write(json.dumps(mr))
sys.exit(0)
