#! /usr/bin/env python

import Helper
import Tokenization
import json
import sys
import os

def run():
	print 'Refining .tokens.json files'
	files = Helper.derivedFiles(Helper.relevantFiles(), '.tokens.json')
	for file in files:
		tokenized = Tokenization.tokenizeFile(file)
		json.dump(tokenized, open(file.replace('.tokens.json', Helper.fileExt()), 'w'))
		Helper.incProgress()
	print ''
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

