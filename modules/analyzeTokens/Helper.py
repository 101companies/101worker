#! /usr/bin/env python

import sys
import os
import json
sys.path.append('../../libraries/101meta')
import const101
import tools101


def relevantFiles(matches, relevanceValues = [ 'system' ]):
    files = []
    for f in matches:
        print f
        relevance = 'system'
        if os.path.exists(f + '.metrics.json'):
            match = json.load(open(f + '.metrics.json'))
            if 'relevance' in match:
                relevance = match['relevance']
            if relevance in relevanceValues:
                files.append(f)

    return files

def derivedFiles(baseFiles, fileExt):
    files = []
    for f in baseFiles:
        if os.path.exists(os.path.join(tRoot(), f + fileExt)):
            files.append(os.path.join(tRoot(), f + fileExt))
    return files

def build(sFilename, tFilename):
    try:
        sSize = os.stat(sFilename).st_size
        if sSize == 0:
            return False
        else:
            sCtime = os.path.getmtime(sFilename)
            tCtime = os.path.getmtime(tFilename)
            return sCtime > tCtime
    except:
        return True

def disregardFiles(baseFiles, inputFileExt, outputFileExt):
    files = []
    for f in baseFiles:
        if (build(f, f.replace(inputFileExt, outputFileExt))):
            files.append(f)
    return files


def tRoot():
    return const101.tRoot

def incProgress():
    tools101.tick();

