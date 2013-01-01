#! /usr/bin/env python

import Helper
import Tokenization
import IndexTools
import json
import sys
import os


def createMap(tokenized):
	result = dict()
	terms = sum(tokenized, [])
	terms = [x.lower() for x in terms]
	for term in terms:
		if not result.has_key(term):
			result[term] = 0
		result[term] += 1
	return result

def refineTokens():
	print 'Refining...'
	files = Helper.derivedFiles(Helper.relevantFiles(), '.tokens.json')
	for file in files:
		tokenized = Tokenization.tokenizeFile(file)
		map = createMap(tokenized)
		json.dump(map, open(file.replace('.tokens.json', Helper.fileExt()), 'w'))
		Helper.incProgress()
	print ''

#def appendToIndex():
#	print 'Appending to index...'
#	IndexTools.appendToIndex()

def run():
	refineTokens()
#	appendToIndex()
	print 'Finished'


def reset():
	print 'removing all ' + Helper.fileExt() + ' files'
	for (path, dirs, files) in os.walk(Helper.tRoot()):
		for file in files:
			if file.endswith(Helper.fileExt()):
				os.remove(os.path.join(path, file))

def usage():
	print './App.py [-reset]'


#command line parsing
if len(sys.argv) == 1:
	run()
elif sys.argv[1] == '-reset':
	reset()
else:
	print 'unrecognized parameter'
	usage()

