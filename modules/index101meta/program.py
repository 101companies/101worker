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
    tools101.tick()
    languages = dict()
    indexFile = open(os.path.join(const101.tRoot, dirname, "index.json"), 'w')

    for basename in files:
        summaryFile = open(os.path.join(const101.tRoot, dirname, basename + ".summary.json"), 'r')
        summary = json.load(summaryFile)
        summaryFile.close()
        values = tools101.valuesByKey(summary, "language")
        for key in values:
            if not key in languages: languages[key] = set()
            languages[key].add(basename)

    for subdirname in dirs:
        subdirFile = open(os.path.join(const101.tRoot, dirname, subdirname, "index.json"), 'r')
        index = json.load(subdirFile)
        subdirFile.close()
        for key in index["languages"]:
            for filename in index["languages"][key]:
                if not key in languages: languages[key] = set()
                languages[key].add(os.path.join(subdirname, filename))                

    for key in languages:
        languages[key] = list(languages[key])
    index = dict()
    index["dirs"] = dirs
    index["files"] = files
    index["languages"] = languages
    indexFile.write(json.dumps(index))
    indexFile.close()

tools101.loopOverFiles(fun, False)
print ""
exit(0)
