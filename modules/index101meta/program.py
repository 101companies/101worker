#! /usr/bin/env python

import os
import sys
import simplejson as json
import commands
import re
sys.path.append('../../libraries/101meta')
import const101
import tools101

def fun(dirname, dirs, files):
    indexFile = open(os.path.join(const101.tRoot, dirname, "index.json"), 'w')
    index = dict()
    index["dirs"] = dirs
    index["files"] = files
    indexFile.write(json.dumps(index))
    indexFile.close()

tools101.loopOverFiles(fun)
exit(0)
