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

def addFile(d, values, basename, summary):           
    for key in values:
        initializeKey(d,key)
        d[key]["files"][basename] = []
        addMetrics(d[key],summary) 

def addDir(p, d, subdirname, index):
    for key in index[p]:
        initializeKey(d,key)
        for filename in index[p][key]["files"]:
           d[key]["files"][os.path.join(subdirname, filename)] = []              
        addMetrics(d[key],index[p][key])

def fun(dirname, dirs, files):
    tools101.tick()
    languages = dict()
    technologies = dict()
    features = dict()
    concepts = dict()
    terms = dict()
    indexFile = open(os.path.join(const101.tRoot, dirname, "index.json"), 'w')

    #
    # Aggregation of file summaries
    #
    for basename in files:
        summaryFile = open(os.path.join(const101.tRoot, dirname, basename + ".summary.json"), 'r')
        summary = json.load(summaryFile)
        summaryFile.close()

        # Deal with languages for file
        values = tools101.valuesByKey(summary, "language")
        addFile(languages, values, basename, summary)
        
        # Deal with technologies for file
        values = tools101.valuesByKey(summary, "partOf")
        values += tools101.valuesByKey(summary, "inputOf")
        values += tools101.valuesByKey(summary, "outputOf")
        values += tools101.valuesByKey(summary, "dependsOn")
        addFile(technologies, values, basename, summary)

        # Deal with features for file
        values = tools101.valuesByKey(summary, "feature")
        addFile(features, values, basename, summary)

        # Deal with concepts for file
        values = tools101.valuesByKey(summary, "feature")
        addFile(concepts, values, basename, summary)

        # Deal with terms for file
        values = tools101.valuesByKey(summary, "term")
        addFile(terms, values, basename, summary)


    #
    # Aggregation of subdirectory indexes
    #
    for subdirname in dirs:
        subdirFile = open(os.path.join(const101.tRoot, dirname, subdirname, "index.json"), 'r')
        index = json.load(subdirFile)
        subdirFile.close()

        # Deal with languages for directory
        addDir("technologies", languages, subdirname, index)

        # Deal with technologies for directory
        addDir("technologies", technologies, subdirname, index)

        # Deal with features for directory
        addDir("features", features, subdirname, index)

        # Deal with concepts for directory
        addDir("concepts", concepts, subdirname, index)

        # Deal with terms for directory
        addDir("terms", terms, subdirname, index)


    # Dumping the index
    index = dict()
    index["dirs"] = dirs
    index["files"] = files
    index["languages"] = languages
    index["technologies"] = technologies
    index["features"] = features
    index["concepts"] = concepts
    index["terms"] = terms
    indexFile.write(json.dumps(index))
    indexFile.close()

tools101.loopOverFiles(fun, False)
print ""
exit(0)
