__author__ = 'martin'

import commands

def load(fileName, buffer=None):
	if not buffer:
		buffer = {}

	file = open(fileName)
	line = file.readline().replace('\n', '')

	while line:
		if not line[0].isspace():
			splitted = line.split(' ')[0].split('_')
			for s in splitted:
				buffer[s] = True
		line = file.readline().replace('\n', '')
		while len(line) == 1:
			line = file.readline().replace('\n', '')

	file.close()
	return buffer

wordList = load('wordnet/index.adj')
wordList = load('wordnet/index.adv', wordList)
wordList = load('wordnet/index.noun', wordList)
wordList = load('wordnet/index.verb', wordList)
wordList = load('wordnet/specific.txt', wordList)


def isWord(term):
	return wordList.has_key(term.lower())


#def blah(term):
#	cmd = 'wordnet ' + 'gfhd' + " -over"
#	(status, output) = commands.getstatusoutput(cmd)
#	print status
#	if output == '':
#		print 'yes'



#legacy stuff, just because it might be useful again in case wordnet isn't as good as I think
#def load(fileName, buffer=None):
#	if not buffer:
#		buffer = {}
#
#	file = open(fileName)
#	line = file.readline().replace('\n', '')
#
#	while line:
#		buffer[line] = True
#		line = file.readline().replace('\n', '')
#		while len(line) == 1:
#			line = file.readline().replace('\n', '')
#
#	file.close()
#	return buffer
#
#wordList = load('input/wordlists/english-words.10.txt')
#wordList = load('input/wordlists/english-words.20.txt', wordList)
#wordList = load('input/wordlists/english-words.35.txt', wordList)
#wordList = load('input/wordlists/english-words.40.txt', wordList)
#wordList = load('input/wordlists/english-words.50.txt', wordList)
#wordList = load('input/wordlists/specific-words.txt', wordList)
#
#wordList = load('input/wordlists/english-abbreviations.10.txt', wordList)
#wordList = load('input/wordlists/english-abbreviations.20.txt', wordList)
#wordList = load('input/wordlists/english-abbreviations.35.txt', wordList)
#wordList = load('input/wordlists/english-abbreviations.40.txt', wordList)
#wordList = load('input/wordlists/english-abbreviations.50.txt', wordList)
#
#def getList():
#	return wordList