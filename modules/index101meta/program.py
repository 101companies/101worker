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
        d[key]["files"] = dict()
        d[key]["metrics"] = const101.noMetrics()

def addFile(r, d, val2key, values, basename, summary):           
    for value in values:
        key = val2key(value)
        initializeKey(r[d],key)
        r[d][key]["files"][basename] = []
        addMetrics(r[d][key],summary) 

def addDir(r, d, subdirname, index):
    for key in index[d]:
        initializeKey(r[d],key)
        for filename in index[d][key]["files"]:
           r[d][key]["files"][os.path.join(subdirname, filename)] = []              
        addMetrics(r[d][key],index[d][key])

def phrase2str(phrase):
    key = phrase[0]
    for x in phrase[1:]: key += "/" + x
    return key

def fun(dirname, dirs, files):
    tools101.tick()
    result = dict()
    result["languages"] = dict()
    result["technologies"] = dict()
    result["features"] = dict()
    result["concepts"] = dict()
    result["terms"] = dict()
    result["phrases"] = dict()
    
    #
    # Aggregation of file summaries
    #
    for basename in files:
        summaryFile = open(os.path.join(const101.tRoot, dirname, basename + ".summary.json"), 'r')
        summary = json.load(summaryFile)
        summaryFile.close()

        # Deal with languages for file
        values = tools101.valuesByKey(summary, "language")
        addFile(result, "languages", lambda x: x, values, basename, summary)
        
        # Deal with technologies for file
        values = tools101.valuesByKey(summary, "partOf")
        values += tools101.valuesByKey(summary, "inputOf")
        values += tools101.valuesByKey(summary, "outputOf")
        values += tools101.valuesByKey(summary, "dependsOn")
        addFile(result, "technologies", lambda x: x, values, basename, summary)

        # Deal with features for file
        values = tools101.valuesByKey(summary, "feature")
        addFile(result, "features", lambda x: x, values, basename, summary)

        # Deal with concepts for file
        values = tools101.valuesByKey(summary, "concept")
        addFile(result, "concepts", lambda x: x, values, basename, summary)

        # Deal with terms for file
        values = tools101.valuesByKey(summary, "term")
        addFile(result, "terms", lambda x: x, values, basename, summary)

        # Deal with phases for file
        values = tools101.valuesByKey(summary, "phrase")
        addFile(result, "phrases", phrase2str, values, basename, summary)


    #
    # Aggregation of subdirectory indexes
    #
    for subdirname in dirs:
        subdirFile = open(os.path.join(const101.tRoot, dirname, subdirname, "index.json"), 'r')
        index = json.load(subdirFile)
        subdirFile.close()
        for key in result:
            addDir(result, key, subdirname, index)


    # Dumping the index
    result["dirs"] = dirs
    result["files"] = files
    resultFile = open(os.path.join(const101.tRoot, dirname, "index.json"), 'w')
    resultFile.write(json.dumps(result))
    resultFile.close()

tools101.loopOverFiles(fun, False)
print ""
exit(0)
