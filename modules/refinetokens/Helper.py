#! /usr/bin/env python

import sys
import os
import json
sys.path.append('../../libraries/101meta')
import const101
import tools101

matches = json.load(open(os.path.join(const101.dumps, 'matches.json'), 'r'))['matches']

def relevantFiles(relevanceValues = [ 'system' ]):
	files = []
	for match in matches:
		relevance = 'system'
		for unit in match['units']:
			if 'relevance' in unit['metadata']:
				relevance = unit['metadata']['relevance']
		if relevance in relevanceValues:
			files.append(match['filename'])
	return files

def derivedFiles(baseFiles, derivedFileName):
	files = []
	for f in baseFiles:
		if os.path.exists(os.path.join(tRoot(), f + derivedFileName)):
			files.append(os.path.join(tRoot(), f + derivedFileName))
	return files

def tRoot():
	return const101.tRoot

def fileExt():
	return '.refinedTokens.json'

def incProgress():
	tools101.tick();