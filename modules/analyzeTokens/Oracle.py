import os

def load(fileName, buffer=None):

    fileName = os.path.join(os.path.dirname(__file__), fileName)

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

