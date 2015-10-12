#! /usr/bin/env python

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

wordList = load('../../libraries/cores/wordnet/index.adj')
wordList = load('../../libraries/cores/wordnet/index.adv', wordList)
wordList = load('../../libraries/cores/wordnet/index.noun', wordList)
wordList = load('../../libraries/cores/wordnet/index.verb', wordList)
wordList = load('../../libraries/cores/wordnet/specific.txt', wordList)

def isWord(term):
    return wordList.has_key(term.lower())
