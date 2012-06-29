#! /usr/bin/env python

import os
import sys
import simplejson as json
import commands
import re
sys.path.append('../../libraries/101meta')
import const101
import tools101
import matches101


mr = matches101.matchAll(1)
mrFile = open(const101.matchesDump, 'w')
mrFile.write(json.dumps(mr))
print str(matches101.noPredFiles) + " predicate constraints checked."
print str(matches101.noPredFilesOk) + " files selected with predicate constraints."
sys.exit(0)
