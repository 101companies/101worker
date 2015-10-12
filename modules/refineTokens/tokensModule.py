#! /usr/bin/env python

# new version

import os
import json
import sys
sys.path.append('../../libraries/101meta')
import const101
import tools101
sys.path.append('../../libraries')
from cores import *
from cores import tokensCore


matches = json.load(open(const101.matchesDump, 'r'))['matches']

def getRelevanceForFile(f):
    for m in matches:
        if m['filename'] == f:
            units = m['units']
            units = filter(lambda u: u['metadata'].has_key('relevance'), units)
            if units:
                return units[0]['metadata']['relevance']
            else:
                return 'system'
    return 'system'

def hasGeshi(f):
    for m in matches:
        if m['filename'] == f:
            units = m['units']
            units = filter(lambda u: u['metadata'].has_key('geshi'), units)
            if units:
                return True
            else:
                return False
    #return True

def tokensFunc(sFile, tFile):
    if getRelevanceForFile(sFile[len(const101.sRoot) + 1:]) in ['system'] and hasGeshi(sFile[len(const101.sRoot) + 1:]):
        tokens = tokensCore.extractTokens(sFile)

        refinedTokens = [ tokensCore.refineToken(x) for x in tokens]
        refinedTokens = sum(refinedTokens, [])
        tick()


print 'Starting to tokenize files'

loopOverDir(const101.sRoot, const101.tRoot, '.tokens.json', tokensFunc)

print '\n\n'