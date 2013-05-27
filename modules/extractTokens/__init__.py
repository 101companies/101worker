#! /usr/bin/env python

import sys
import simplejson as json
sys.path.append('../../libraries/101meta')
import const101
import tools101
<<<<<<< HEAD
import logging

sys.path.append('../../libraries')
from service_api import *
=======
>>>>>>> 789459768f776d4d06b3c35544858ffc922ad749

#used for the incrementally stuff
def testFile(sFilename, tFilename):
    return tools101.build(sFilename, tFilename)

#accept files that have  a geshi code - but also add the relevance of a file with respect to the default relevance
def testEntry(entry):
<<<<<<< HEAD
    print entry
    meta = {"relevance" : "system"}
    if any(["relevance" in item for item in entry["metadata"]]) :
        meta["relevance"] = [item for item in entry["metadata"] if "relevance" in item][0]['relevance']
    if any(["geshi" in item for item in entry["metadata"]]):
        meta["geshi"] = [item for item in entry["metadata"] if "geshi" in item][0]['geshi']
=======
    meta = {"relevance" : "system"}
    for m in entry["units"]:
        if "relevance" in m["metadata"]:
            meta["relevance"] = m["metadata"]["relevance"]
        if "geshi" in m["metadata"]:
            meta["geshi"] = m["metadata"]["geshi"]
>>>>>>> 789459768f776d4d06b3c35544858ffc922ad749
    return meta

# Per-file functionality
def derive(info, rFilename, sFilename, tFilename1):
<<<<<<< HEAD
    print 'derive'
    if "geshi" in info:
        tFilename2 = tFilename1[:-len(".metrics.json")]+".tokens.json"
        print "Process " + rFilename + " for GeSHi code " + info["geshi"] + "."
        command = "php " + os.path.join(os.path.dirname(__file__), 'helper.php') + " \"" + sFilename + "\" \"" + tFilename1 + "\" \"" + tFilename2 + "\" \"" + info["geshi"] + "\" " + info["relevance"]
=======
    if "geshi" in info:
        tFilename2 = tFilename1[:-len(".metrics.json")]+".tokens.json"
        print "Process " + rFilename + " for GeSHi code " + info["geshi"] + "."
        command = "php helper.php" + " \"" + sFilename + "\" \"" + tFilename1 + "\" \"" + tFilename2 + "\" \"" + info["geshi"] + "\" " + info["relevance"]
>>>>>>> 789459768f776d4d06b3c35544858ffc922ad749
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
<<<<<<< HEAD
    files,
=======
    dump,
>>>>>>> 789459768f776d4d06b3c35544858ffc922ad749
    testEntry # a predicate to select the file
    , testFiles # a predicate to test source and target file
    , suffix    # the extra suffix for target files
    , fun       # the function to apply to each match
    ):

<<<<<<< HEAD
    for f in files:
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
    data = expand_data(data)
=======

    matches = json.load(open(dump, 'r'))["matches"]

    for entry in matches:

        value = testEntry(entry)
        if value is None: continue

        # RELATIVE dirname and filename
        rFilename = entry["filename"]
        rDirname = os.path.dirname(rFilename)
        basename = os.path.basename(rFilename)

        # SOURCE dirname and filename
        sDirname = os.path.join(const101.sRoot, rDirname)
        sFilename = os.path.join(sDirname, basename)

        # TARGET dirname and filename
        tDirname = os.path.join(const101.tRoot, rDirname)
        tFilename = os.path.join(tDirname, basename + suffix)

        # Skip file, if possible
        makedirs(tDirname)
        if not testFiles(sFilename, tFilename): continue

        # Find and remove related problem
        failure = False
        idx = 0
        for p in problems:
            if p["filename"] == rFilename:
                del problems[idx]
                failure = True
                break
            else:
                idx += 1
        exists = os.path.exists(tFilename)
        if not failure and exists:

        # Generate target
        tick()
        result = fun(value, rFilename, sFilename, tFilename)

    # Terminate ticking
    sys.stdout.write('\n')

def main(data):

    if data['type'] != 'folders':
        raise

    assert len(data['data']) == 1
>>>>>>> 789459768f776d4d06b3c35544858ffc922ad749

    print "Generating GeSHi-based metrics for 101repo."

    # Initialize housekeeping
    geshicodes = set()
<<<<<<< HEAD
    #dump = tools101.beforeMapMatches(const101.metricsDump)
   # if "geshicodes" in dump:
   #     geshicodes = set(dump["geshicodes"])
=======
    dump = tools101.beforeMapMatches(const101.metricsDump)
    if "geshicodes" in dump:
        geshicodes = set(dump["geshicodes"])
>>>>>>> 789459768f776d4d06b3c35544858ffc922ad749

    # Loop over matches
    dump = mapMatches(data['data'], testEntry, testFile, ".metrics.json", derive)

    # Convert set to list before dumping JSON
    geshicodes = list(geshicodes)

    # Assemble dump, save it, and exit
<<<<<<< HEAD
    #dump = dict()
    #dump["geshicodes"] = geshicodes
    #dump["numbers"] = dict()
    #dump["numbers"]["numberOfGeshicodes"] = len(geshicodes)
    #tools101.afterMapMatches(dump, const101.metricsDump)
=======
    dump = dict()
    dump["geshicodes"] = geshicodes
    dump["numbers"] = dict()
    dump["numbers"]["numberOfGeshicodes"] = len(geshicodes)
    tools101.afterMapMatches(dump, const101.metricsDump)
>>>>>>> 789459768f776d4d06b3c35544858ffc922ad749
