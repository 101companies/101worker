#! /usr/bin/env python

import sys

sys.path.append('../../libraries')
sys.path.append('../../libraries/101meta')

from metamodel import *


featuresToInspect = ['total', 'cut']
contributionWhitelist = ['antlrLexer']


featureIndex = {}
contributions = Namespace('contributions')

for folders, files in walk(contributions):
    for file in files:
        for feature in file.features:
            featureIndex.setdefault(feature, []).append(file)


contributionIndex = {}
for feature in featuresToInspect:
    for file in featureIndex.get(feature, []):
        member = file.member
        if member.name in contributionWhitelist and file.metrics.exists:
            contributionIndex[member.name] = contributionIndex.get(member.name, 0) + file.metrics.ncloc

print contributionIndex