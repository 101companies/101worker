#! /usr/bin/env python

import os
import sys
import simplejson as json
import commands
import re
sys.path.append('../../libraries/101meta')
import const101
import tools101

def addRefinedTokens(result, dirname, basename, summary):
    if not summary['refinedTokens'] == []:
        result['refinedTokens'][os.path.join(dirname, basename)] = summary['refinedTokens']

def addRefinedTokensDir(result, index):
    result['refinedTokens'].update(index['refinedTokens'])

def addMetrics(lvalue, rvalue):
    if "relevance" in rvalue["metrics"]:
        relevance = rvalue["metrics"]["relevance"]
        lvalue["metrics"][relevance]["size"] += rvalue["metrics"]["size"]
        lvalue["metrics"][relevance]["loc"] += rvalue["metrics"]["loc"]
        lvalue["metrics"][relevance]["ncloc"] += rvalue["metrics"]["ncloc"]
    else:
        for x in ["system", "reuse", "derive", "ignore"]:
            lvalue["metrics"][x]["size"] += rvalue["metrics"][x]["size"]
            lvalue["metrics"][x]["loc"] += rvalue["metrics"][x]["loc"]
            lvalue["metrics"][x]["ncloc"] += rvalue["metrics"][x]["ncloc"]

def initializeKey(r, map, key):
    d = r[map]
    if not key in d:
        d[key] = dict()
        d[key]["files"] = dict()
        d[key]["metrics"] = { "system":const101.noMetrics(),
							  "reuse" : const101.noMetrics(),
							  "derive": const101.noMetrics(),
							  "ignore" : const101.noMetrics() }
        d[key]["resources"] = []
        if map in resolution:
            if key in resolution[map]:
                e = resolution[map][key]
                d[key]["headline"] = e["headline"]
                resources = dict()
                d[key]["resources"] = resources
                if "101wiki" in e:
                    resources["101wiki"] = e["101wiki"]
                if "101repo" in e:
                    resources["101repo"] = e["101repo"]

def addFile(result, rkey, mkey, val2key, basename, summary):
    for unit in summary["units"]:
        if mkey in unit["metadata"]:
            val = unit["metadata"][mkey]
            key = val2key(val)
            initializeKey(result, rkey, key)
            if not basename in result[rkey][key]["files"]:
                result[rkey][key]["files"][basename] = list()
            result[rkey][key]["files"][basename].append(unit)
            addMetrics(result[rkey][key],summary)


def addDir(r, d, subdirname, index):
        for key in index[d]:
            initializeKey(r, d, key)
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
    result["refinedTokens"] = dict()

    #
    # Aggregation of file summaries
    #
    for basename in files:
        try:

            summaryFile = open(os.path.join(const101.tRoot, dirname, basename + ".summary.json"), 'r')
            summary = json.load(summaryFile)
            summaryFile.close()

            # Deal with languages for file
            addFile(result, "languages", "language", lambda x: x, basename, summary)

            # Deal with refinedTokens for file
            addRefinedTokens(result, dirname, basename, summary)

            # Deal with technologies for file
            addFile(result, "technologies", "partOf", lambda x: x, basename, summary)
            addFile(result, "technologies", "inputOf", lambda x: x, basename, summary)
            addFile(result, "technologies", "outputOf", lambda x: x, basename, summary)
            addFile(result, "technologies", "dependsOn", lambda x: x, basename, summary)

            # Deal with features for file
            addFile(result, "features", "feature", lambda x: x, basename, summary)

            # Deal with concepts for file
            addFile(result, "concepts", "concept", lambda x: x, basename, summary)

            # Deal with terms for file
            addFile(result, "terms", "term", lambda x: x, basename, summary)

            # Deal with phases for file
            addFile(result, "phrases", "phrase", phrase2str, basename, summary)

        except IOError:
            pass

    #
    # Aggregation of subdirectory indexes
    #
    for subdirname in dirs:
        subdirFile = open(os.path.join(const101.tRoot, dirname, subdirname, "index.json"), 'r')
        try:
            index = json.load(subdirFile)
            subdirFile.close()
            for key in result:
		if key == 'refinedTokens':
                    addRefinedTokensDir(result, index)
                else:
                    addDir(result, key, subdirname, index)
        except IOError:
            pass

    # Dumping the index
    result["dirs"] = dirs
    result["files"] = files
    resultFile = open(os.path.join(const101.tRoot, dirname, "index.json"), 'w')
    resultFile.write(json.dumps(result))
    resultFile.close()

    # Dumping the file index
    fileresult = dict()
    fileresult["dirs"] = dirs
    fileresult["files"] = files
    fileresultFile = open(os.path.join(const101.tRoot, dirname, "fileindex.json"), 'w')
    fileresultFile.write(json.dumps(fileresult))
    fileresultFile.close()

resolution = json.load(open(const101.resolutionDump, 'r'))["results"]
tools101.loopOverFiles(fun, False)
print ""
exit(0)
