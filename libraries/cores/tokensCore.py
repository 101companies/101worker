#! /usr/bin/env python

import re
import oracle


# try to split up even further to words that are known to the oracle
# the process starts at the beginning of the word and the end and tries to find it in the oracle,
# if it doesn't the end pointer is put left one character and so on
def greedy(start, t):
    end = len(t)
    if start == end:
        return []

    while not oracle.isWord(t[start:end].lower()):
        end -= 1
        if start == end:
            return [t[start:]]

    return [ t[start:end] ] + greedy(end, t)


def refineUnknown(token):
    if not oracle.isWord(token):
        return greedy(0, token)
    return [ token ]


#difference on splitOnChange and splitPenultimate becomes clear with "isOSGiCompatible"
#try to split on case change - StyledEditorKit => [Styled, Editor, Kit]
def splitOnChange(token):
    pattern = r'([A-Z]{2,}(?=A-Z|$)|[A-Z][a-z]*)'
    found = re.findall(pattern, token)
    if found == []:
        return [token]
    return found


#try to split one before case changes - HTMLEditor => [HTML, Editor]
def splitPenultimate(token):
    boundaries = []
    lastStart = 0
    for idx, char in enumerate(token):
        if char.isupper():
            if idx+1 < len(token) and token[idx+1].islower():
                if idx-1 > 0:
                    boundaries.append(token[lastStart:idx])
                    lastStart = idx

    boundaries.append(token[lastStart:len(token)])
    return boundaries


#both methods applied, then it's checked which one provides better results
def splitOnUCLC(token):
    refined1 = splitOnChange(token)
    hits1 = 0
    for t in refined1:
        if oracle.isWord(t.lower()):
            hits1 += 1

    refined2 = splitPenultimate(token)
    hits2 = 0
    for t in refined2:
        if oracle.isWord(t.lower()):
            hits2 += 1

    if hits2 > hits1:
        return refined2
    return refined1


def splitOnSeparators(token):
    list = []

    #split on separator icons
    tokens = re.split('_|\.', token)

    #split extract numbers (101companies => [101, companies])
    for t in tokens:
        list += re.findall(r'\d+|[^\d\s]+', t)
    return list


def preProcess(token):
    def isValidToken(token):
        if not token: return False

        #currently, the only criteria is that it's length is bigger than 1
        if len(token) > 1:
            return True

        return False

    result = []
    parts = re.split('\s|-|/|=|\"|:|;|<|>|,|\(|\)|\[|\]|\'', token)
    for t in parts:
        if isValidToken(t):
            result.append(t)

    return result

#tokenize a single word
def refineToken(word):
    result = []

    #do some preprocessing (tries to filter out variable names and stuff like that)
    preProcessing = preProcess(word)

    #for every term that survived preprocessing, first try to split on possible seperators
    #then split on UCLC boundaries (camel case) and if that doesn't produce known words,
    #then split them um further with the greedy algorithm
    for t1 in preProcessing:
        firstStep = splitOnSeparators(t1)
        for t2 in firstStep:
            secondStep = splitOnUCLC(t2)
            for t3 in secondStep:
                result += refineUnknown(t3)
    return result

def extractTokens(filePath):
    text = open(filePath, 'r').read()
    return re.findall('\w+', text)