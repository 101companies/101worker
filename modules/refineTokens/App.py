#! /usr/bin/env python

import Helper
import Tokenization
import json
import sys
import os

inputFileExt = '.tokens.json'
outputFileExt = '.refinedTokens.json'
inputFragFileExt = '.fragments.tokens.json'
outputFragFileExt = '.fragments.refinedTokens.json'
outputDebugFileExt = '.refinedTokens.debug.json'

def createMap(tokenized, fragments=False):
    result = dict()
    if fragments:
        for fragment, tokens in tokenized.iteritems():
            terms = sum(tokens, [])
            terms = [x.lower() for x in terms]
            fragResult = dict()
            for term in terms:
                if not fragResult.has_key(term):
                    fragResult[term] = 0
                fragResult[term] += 1
            result[fragment] = fragResult

    else:
        terms = sum(tokenized, [])
        terms = [x.lower() for x in terms]
        for term in terms:
            if not result.has_key(term):
                result[term] = 0
            result[term] += 1

    return result

def refineTokens(debug = False, force = True, fragments=False):
	#find all .tokens.json or fragments.tokens.json files
    if fragments:
        ending = inputFragFileExt
        outEnding = outputFragFileExt
        files = Helper.derivedFiles(Helper.relevantFiles(), inputFragFileExt)
        if (not force):
            files = Helper.disregardFiles(files, inputFragFileExt, outputFragFileExt)
    else:
        ending = inputFileExt
        outEnding = outputFileExt
        files = Helper.derivedFiles(Helper.relevantFiles(), inputFileExt)
        if (not force):
		    files = Helper.disregardFiles(files, inputFileExt, outputFileExt)

    for file in files:
        tokenized = Tokenization.tokenizeFile(file, fragments=fragments)
        if (debug):
            json.dump(tokenized, open(file.replace(ending, outputDebugFileExt), 'w'))
        map = createMap(tokenized, fragments=fragments)
        json.dump(map, open(file.replace(ending, outEnding), 'w'))
        Helper.incProgress()
    print ''


def run(debug = False, force = False, fragments=False):
	refineTokens(debug, force, fragments=fragments)

def reset():
	print 'removing all ' + outputFileExt + ' files'
	for (path, dirs, files) in os.walk(Helper.tRoot()):
		for file in files:
			if file.endswith(outputFileExt) or file.endswith(outputDebugFileExt):
				os.remove(os.path.join(path, file))

def usage():
	print './App.py [-debug|-reset]'


#command line parsing
if len(sys.argv) == 1:
	run()
elif sys.argv[1] == '-debug':
	run(True)
elif sys.argv[1] == '-reset':
	reset()
elif sys.argv[1] == '-fragments':
	run(fragments=True)
else:
	print 'unrecognized parameters'
	usage()

