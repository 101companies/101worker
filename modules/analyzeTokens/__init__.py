#! /usr/bin/env python

import Tokenization
import json
import sys
import Helper
import os

sys.path.append('../../libraries')
from service_api import *


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


def refineTokens(data, debug = False, force = True):
	#find all .tokens.json files
	files = Helper.derivedFiles(Helper.relevantFiles(data['data']), inputFileExt)

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


def main(data, debug = False, force = False):

    data = expand_data(data)

    refineTokens(data, debug, force)

def reset():
	print 'removing all ' + outputFileExt + ' files'
	for (path, dirs, files) in os.walk(Helper.tRoot()):
		for file in files:
			if file.endswith(outputFileExt) or file.endswith(outputDebugFileExt):
				os.remove(os.path.join(path, file))


if __name__ == '__main__':
    main({
  'type': "folders",
  'data': ["contributions/pyJson"]
})

