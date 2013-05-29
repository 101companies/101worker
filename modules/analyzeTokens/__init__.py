#! /usr/bin/env python

<<<<<<< HEAD
import Tokenization
import json
import sys
import Helper
import os

sys.path.append('../../libraries')
from service_api import *

=======
#import Helper
import Tokenization
import json
import sys
import os

>>>>>>> 789459768f776d4d06b3c35544858ffc922ad749
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

<<<<<<< HEAD
def refineTokens(data, debug = False, force = True):
	#find all .tokens.json files
	files = Helper.derivedFiles(Helper.relevantFiles(data['data']), inputFileExt)
=======
def refineTokens(debug = False, force = True):
	#find all .tokens.json files
	files = Helper.derivedFiles(Helper.relevantFiles(), inputFileExt)
>>>>>>> 789459768f776d4d06b3c35544858ffc922ad749
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
<<<<<<< HEAD
    #if data['type'] == 'folders':
    #    folders = data['data']
    #    folders = map(lambda folder: os.path.join('../../../101repo/', folder), folders)
    #    data['data'] = []
    #    for folder in folders:
    #        for root, subFolders, files in os.walk(folder):
    #            for file in files:
    ##                f = os.path.join(root,file)
     #               data['data'].append(f)

    #refineTokens(data, debug, force)
    pass
=======
    if data['type'] == 'folders':
        folders = data['data']
        folders = map(lambda folder: os.path.join('../../../101repo/', folder), folders)
        data['data'] = []
        for folder in folders:
            for root, subFolders, files in os.walk(folder):
                for file in files:
                    f = os.path.join(root,file)
                    data['data'].append(f)

    refineTokens(data, debug, force)
>>>>>>> 789459768f776d4d06b3c35544858ffc922ad749

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

