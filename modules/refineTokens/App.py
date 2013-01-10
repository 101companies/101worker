#! /usr/bin/env python

import Helper
import Tokenization
import json
import sys
import os

inputFileExt = '.tokens.json'
outputFileExt = '.refinedTokens.json'
outputDebugFileExt = '.refinedTokens.debug.json'

def createMap(tokenized):
	result = dict()
	terms = sum(tokenized, [])
	terms = [x.lower() for x in terms]
	for term in terms:
		if not result.has_key(term):
			result[term] = 0
		result[term] += 1
	return result

def refineTokens(debug = False, force = True):
	#find all .tokens.json files
	files = Helper.derivedFiles(Helper.relevantFiles(), inputFileExt)
	if (not force):
		files = Helper.disregardFiles(files, inputFileExt, outputFileExt)

	for file in files:
		tokenized = Tokenization.tokenizeFile(file)
		if (debug):
			json.dump(tokenized, open(file.replace(inputFileExt, outputDebugFileExt), 'w'))
		map = createMap(tokenized)
		json.dump(map, open(file.replace('.tokens.json', outputFileExt), 'w'))
		Helper.incProgress()
	print ''


def run(debug = False, force = False):
	refineTokens(debug, force)

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
else:
	print 'unrecognized parameters'
	usage()

