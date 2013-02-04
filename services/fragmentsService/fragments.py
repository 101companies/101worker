__author__ = 'martin'

import sys
import os
import json
import commands
sys.path.append('../../libraries/101meta')
import const101

def readLines(filePath, lines):
	return [x for i, x in enumerate(filePath) if i in lines]

def readFile(filePath):
	fp = open(filePath, 'r')
	str = fp.read()
	fp.close()
	return str

def extract(entry):
	geshi, locator = None, None
	for unit in entry['units']:
		if 'geshi' in unit['metadata']: geshi = unit['metadata']['geshi']
		if 'locator' in unit['metadata']: locator = unit['metadata']['locator']
	return geshi, locator

def getLanguageAndLocator(filename):
	matches = json.load(open(os.path.join(const101.dumps, 'matches.json'), 'r'))['matches']
	for entry in matches:
		if entry['filename'] == filename: return extract(entry)

	return None, None

def getFileText(path, file):
	fullPath = os.path.join(const101.sRoot, path, file)
	return readFile(fullPath)

def getFragmentText(path, file, fragment, locator):
	fullPath = os.path.join(const101.sRoot, path, file)
	fullLocator = os.path.join(const101.sRoot, locator)

	f = fragment.split('/')
	json.dump({'class':f[0], 'method':f[1]}, open('fragment.json', 'w'))

	command = fullLocator + ' ' + fullPath + ' ' + os.path.abspath('./fragment.json') + ' ' + os.path.abspath('./lines.json')
	status, output = commands.getstatusoutput(command)

	if not status == 0:
		raise Exception(locator + ' failed: ' + output)

	lines = json.load(open('./lines.json', 'r'))
	fp = open(fullPath, 'r')
	str = readLines(fp, range(lines['from']-1, lines['to']))
	fp.close()
	return ''.join(str)

def findFragment(path, file, fragment):
	geshi, locator = getLanguageAndLocator(os.path.join(path, file))
	if not geshi:
		raise Exception('No geshi code associated - file is probably no textfile')

	data = {'geshi' : geshi}
	if not fragment:
		data['text'] = getFileText(path, file)
	else:
		if not locator:
			raise Exception('No fragment locator associated with this type of file')

		data['text'] = getFragmentText(path, file, fragment, str(locator))

	return json.dumps(data)