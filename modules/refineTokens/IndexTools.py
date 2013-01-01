__author__ = 'martin'

import os
import glob
import json
import Helper

def findIndexFiles():
	indexFiles = []
	for (path, dirs, files) in os.walk(os.path.join(Helper.tRoot(), 'contributions', 'javaStatic'), False):
		for f in files:
			if f == 'index.json':
				indexFiles.append(os.path.join(path, f))
	return indexFiles

def createTermMap(dir):
	files = glob.glob(os.path.join(dir, '*' + Helper.fileExt()))
	map = dict()
	for refined in files:
		terms = sum(json.load(open(refined, 'r')), [])
		terms = [x.lower() for x in terms]
		termMap = dict()
		for term in terms:
			if termMap.has_key(term):
				termMap[term] += 1
			else:
				termMap[term] = 1
		map[refined.replace(Helper.tRoot() + '/', '')] = termMap
	return map

def considerOtherIndexFiles(dir, map = None):
	if map == None: map = dict()
	for (path, dirs, files) in os.walk(dir):
		for file in files:
			if file == 'index.json' and not path == dir:
				index = json.load(open(os.path.join(path, file)))
				for f in index['terms'].keys():
					map[f] = index['terms'][f]
	return map

def appendToIndex():
	indexFiles = findIndexFiles()
	for indexFile in indexFiles:
		termMap = createTermMap(os.path.dirname(indexFile))
		termMap = considerOtherIndexFiles(os.path.dirname(indexFile), termMap)
		index = json.load(open(indexFile, 'r'))
		index['terms'] = termMap
		json.dump(index, open(indexFile, 'w'))