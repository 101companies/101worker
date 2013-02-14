import sys
import os
import json
import commands
sys.path.append('../../libraries/101meta')
import const101

def readLines(filePath, lines):
	fp = open(filePath, 'r')
	l = [x for i, x in enumerate(fp) if i in lines]
	return ''.join(l)

def readFile(filePath):
	return open(filePath, 'r').read()

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

	raise Exception('specified file not found')

def getFileText(path, file):
	fullPath = os.path.join(const101.sRoot, path, file)
	return readFile(fullPath)

def getFragmentText(path, file, fragment, locator):
	fullPath = os.path.join(const101.sRoot, path, file)
	fullLocator = os.path.join(const101.sRoot, locator)

	command = fullLocator + ' ' + os.path.abspath(fullPath) + ' ' + fragment.replace("'", "\\'")
	status, output = commands.getstatusoutput(command)
	if not status == 0:
		raise Exception(locator + ' failed: ' + output)

	try:
		lines = json.loads(output)
	except:
		raise Exception('Output was no json: ' + output)
	return readLines(fullPath, range(lines['from']-1, lines['to']))


def findFragment(path, file, fragment):
	geshi, locator = getLanguageAndLocator(os.path.join(path, file))
	if not geshi:
		raise Exception('No geshi code associated - file is probably no text file')

	data = {'geshi' : geshi}
	if not fragment:
		data['text'] = getFileText(path, file)
	else:
		if not locator:
			raise Exception('No fragment locator associated with this type of file')

		data['text'] = getFragmentText(path, file, fragment, str(locator))

	return json.dumps(data)