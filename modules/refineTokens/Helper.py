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