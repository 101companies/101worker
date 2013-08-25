#!/usr/bin/env python

from __init__ import Namespace
from __init__ import NotReadableException
import sys


#function for indicating progress (just prints a . on the console)
def progress():
    sys.stdout.write('.')
    sys.stdout.flush()


#extracts all files from a folder including subfolders
#remember: members are just special folders
def extractFiles(folder):
    files = folder.files
    for subFolder in folder.folders:
        files +=( extractFiles(subFolder) )
    return files


if __name__ == '__main__':
    #start at the contribution namespace and initialize a list that will later contain all files
    contributionsNamespace = Namespace('namespace/contributions')
    files = []

    #extract the files
    for contribution in contributionsNamespace.members:
        files += extractFiles(contribution)
        progress()

    #create a index, mapping file content to filename so that files that have the same content will be
    #in the same list
    contentIndex = {}
    for file in files:
        try:
            content = file.content
            if content in contentIndex:
                contentIndex[content].append(file.identifier)
            else:
                contentIndex[content] = [ file.identifier ]

        except NotReadableException:
            pass

        progress()

    #create a new line and start printing lists that are longer than 1 (meaning that at least two files
    #have the same content)
    print ''
    for i in contentIndex.itervalues():
        if len(i) > 1:
            print str(i) + ' are perfect clones'