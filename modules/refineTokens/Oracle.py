__author__ = 'martin'

def load(fileName, buffer=None):
	if not buffer:
		buffer = {}

	file = open(fileName)
	line = file.readline().replace('\n', '')

	while line:
		buffer[line] = True
		line = file.readline().replace('\n', '')
		while len(line) == 1:
			line = file.readline().replace('\n', '')

	file.close()
	return buffer

def oracle(term):
	return wordList.has_key(term.lower()) or abbrevList.has_key(term)


wordList = load('input/wordlists/english-words.10.txt')
wordList = load('input/wordlists/english-words.20.txt', wordList)
wordList = load('input/wordlists/english-words.35.txt', wordList)
wordList = load('input/wordlists/english-words.40.txt', wordList)
wordList = load('input/wordlists/english-words.50.txt', wordList)
wordList = load('input/wordlists/specific-words.txt', wordList)

abbrevList = load('input/wordlists/english-abbreviations.10.txt')
abbrevList = load('input/wordlists/english-abbreviations.20.txt', abbrevList)
abbrevList = load('input/wordlists/english-abbreviations.35.txt', abbrevList)
abbrevList = load('input/wordlists/english-abbreviations.40.txt', abbrevList)
abbrevList = load('input/wordlists/english-abbreviations.50.txt', abbrevList)