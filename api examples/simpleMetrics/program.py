#! /usr/bin/env python

import sys

sys.path.append('../../libraries')
sys.path.append('../../libraries/101meta')

from metamodel import *

contributionsNamespace = Namespace('contributions')
noOfContributions = len(contributionsNamespace.members)

languageSet = set()
technologySet = set()
for folders, files in walk(contributionsNamespace):
    for file in files:
        if file.language:
            languageSet.add(file.language)
        if file.dependsOn:
            for tech in file.dependsOn:
                technologySet.add(tech)
noOfLanguages = len(languageSet)
noOfTechnologies = len(technologySet)


print 'Number of contributions: {}'.format(noOfContributions)
print 'Number of languages according to files on worker: {}'.format(noOfLanguages)
print 'Number of technologies according to files on worker: {}'.format(noOfTechnologies)

#try it for wiki data
languageSet = set()
technologySet = set()
for contribution in contributionsNamespace.members:
    for s, p, o in filter(lambda x: 'uses' in x[1] and 'languages' in x[2], contribution.endpointData):
        languageSet.add(o)
    #technologySet |= set(filter(lambda x: 'uses' in x[1] and 'technologies' in x[2], contribution.endpointData))

print 'Number of languages according to wiki {}'.format(len(languageSet))