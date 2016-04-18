#! /usr/bin/env python

import sys
import simplejson as json
sys.path.append('../../libraries/101meta')
import const101
import tools101
import logging

sys.path.append('../../libraries')
from service_api import *


#used for the incrementally stuff
def testFile(sFilename, tFilename):
    return tools101.build(sFilename, tFilename)

#accept files that have  a geshi code - but also add the relevance of a file with respect to the default relevance
def testEntry(entry):
    print entry
    meta = {"relevance" : "system"}
    if any(["relevance" in item for item in entry["metadata"]]) :
        meta["relevance"] = [item for item in entry["metadata"] if "relevance" in item][0]['relevance']
    if any(["geshi" in item for item in entry["metadata"]]):
        meta["geshi"] = [item for item in entry["metadata"] if "geshi" in item][0]['geshi']

    return meta

# Per-file functionality
def derive(info, rFilename, sFilename, tFilename1):
    print 'derive'
    if "geshi" in info:
        tFilename2 = tFilename1[:-len(".metrics.json")]+".tokens.json"
        print "Process " + rFilename + " for GeSHi code " + info["geshi"] + "."
        command = "php " + os.path.join(os.path.dirname(__file__), 'helper.php') + " \"" + sFilename + "\" \"" + tFilename1 + "\" \"" + tFilename2 + "\" \"" + info["geshi"] + "\" " + info["relevance"]

        (status, output) = tools101.run(command)

        # Result aggregation
        result = dict()
        result["geshicode"] = info["geshi"]
        result["command"] = command
        result["status"] = status
        result["output"] = output
    else:
        default = const101.noMetrics()
        default["relevance"] = info["relevance"]
        json.dump(default, open(tFilename1, 'w'))

        result = dict()
        result["status"] = 0

    return result


def mapMatches(
    files,
    testEntry # a predicate to select the file
    , testFiles # a predicate to test source and target file
    , suffix    # the extra suffix for target files
    , fun       # the function to apply to each match
    ):

    for f in files:
        print f
        if os.path.exists(f + '.metadata.json'):
            entries = json.load(open(f + '.metadata.json'))

        else:
            continue

        for entry in entries:
            value = testEntry(entry)
            if value is None: continue

            # RELATIVE dirname and filename
            rFilename = f
            #rDirname = os.path.dirname(rFilename)
            #basename = os.path.basename(rFilename)

            # SOURCE dirname and filename
            #sDirname = os.path.join(const101.sRoot, rDirname)
            sFilename = f

            # TARGET dirname and filename
            #tDirname = os.path.join(const101.tRoot, rDirname)
            tFilename = f + suffix

            # Find and remove related problem
            #failure = False
            idx = 0
            #for p in problems:
            #    if p["filename"] == rFilename:
            #        del problems[idx]
            #        failure = True
            #        break
            #    else:
            #        idx += 1

            result = fun(value, rFilename, sFilename, tFilename)
            logging.info(str(result))

def main(data):
    print data
    data = expand_data(data)

    print data

    print "Generating GeSHi-based metrics for 101repo."

    # Initialize housekeeping
    #geshicodes = set()
    #dump = tools101.beforeMapMatches(const101.metricsDump)
   # if "geshicodes" in dump:
   #     geshicodes = set(dump["geshicodes"])


    # Loop over matches
    dump = mapMatches(data['data'], testEntry, testFile, ".metrics.json", derive)

    # Convert set to list before dumping JSON
    #geshicodes = list(geshicodes)

    # Assemble dump, save it, and exit
    #dump = dict()
    #dump["geshicodes"] = geshicodes
    #dump["numbers"] = dict()
    #dump["numbers"]["numberOfGeshicodes"] = len(geshicodes)
    #tools101.afterMapMatches(dump, const101.metricsDump)
