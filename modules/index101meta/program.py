#! /usr/bin/env python

import os
import sys
import simplejson as json
import commands
import re
sys.path.append('../../libraries/101meta')
import const101
import tools101

def addMetrics(lvalue, rvalue):
    lvalue["metrics"]["size"] += rvalue["metrics"]["size"]
    lvalue["metrics"]["loc"] += rvalue["metrics"]["loc"]
    lvalue["metrics"]["ncloc"] += rvalue["metrics"]["ncloc"]

def initializeKey(d,key):
    if not key in d:
        d[key] = dict()
        d[key]["files"] = set()
        d[key]["metrics"] = const101.noMetrics()

def fun(dirname, dirs, files):
    tools101.tick()
    languages = dict()
    technologies = dict()
    indexFile = open(os.path.join(const101.tRoot, dirname, "index.json"), 'w')

    for basename in files:
        summaryFile = open(os.path.join(const101.tRoot, dirname, basename + ".summary.json"), 'r')
        summary = json.load(summaryFile)
        summaryFile.close()

        # Deal with languages for file
        values = tools101.valuesByKey(summary, "language")
        for key in values:
            initializeKey(languages,key)
            languages[key]["files"].add(basename)
            addMetrics(languages[key],summary)

        # Deal with technologies for file
        values = tools101.valuesByKey(summary, "partOf")
        values += tools101.valuesByKey(summary, "inputOf")
        values += tools101.valuesByKey(summary, "outputOf")
        values += tools101.valuesByKey(summary, "dependsOn")
        for key in values:
            initializeKey(technologies,key)
            technologies[key]["files"].add(basename)
            addMetrics(technologies[key],summary)

    for subdirname in dirs:
        subdirFile = open(os.path.join(const101.tRoot, dirname, subdirname, "index.json"), 'r')
        index = json.load(subdirFile)
        subdirFile.close()

        # Deal with languages for directory
        for key in index["languages"]:
            initializeKey(languages,key)
            for filename in index["languages"][key]:
                languages[key]["files"].add(os.path.join(subdirname, filename))                
            addMetrics(languages[key],index["languages"][key])

        # Deal with technologies for directory
        for key in index["technologies"]:
            initializeKey(technologies,key)
            for filename in index["technologies"][key]:
                technologies[key]["files"].add(os.path.join(subdirname, filename))                
            addMetrics(technologies[key],index["technologies"][key])

    for key in languages:
        languages[key]["files"] = list(languages[key]["files"])
    for key in technologies:
        technologies[key]["files"] = list(technologies[key]["files"])
    index = dict()
    index["dirs"] = dirs
    index["files"] = files
    index["languages"] = languages
    index["technologies"] = technologies
    indexFile.write(json.dumps(index))
    indexFile.close()

tools101.loopOverFiles(fun, False)
print ""
exit(0)
