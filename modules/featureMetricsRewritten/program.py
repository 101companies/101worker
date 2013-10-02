#! /usr/bin/env python

import sys
import matplotlib
matplotlib.use('Agg')

import numpy as np
import matplotlib.pyplot as plt

sys.path.append('../../libraries')
sys.path.append('../../libraries/101meta')

from metamodel import *


featuresToInspect = ['total', 'cut']
contributionWhitelist = ['antlrLexer']


#build "Feature" -> ["File 1", "File 2", ...] association
featureIndex = {}
contributions = Namespace('contributions')

for folders, files in walk(contributions):
    for file in files:
        for feature in file.features:
            featureIndex.setdefault(feature, []).append(file)

#build "contributionName" -> "ncloc" association
contributionIndex = {}
for feature in featuresToInspect:
    for file in featureIndex.get(feature, []):
        member = file.member
        if member.name in contributionWhitelist and file.metrics.exists:
            contributionIndex[member.name] = contributionIndex.get(member.name, 0) + file.metrics.ncloc


#visualize results
bars = contributionIndex.values()
labels = contributionIndex.keys()

figure = plt.figure()
width = 0.35

ind = np.arange(len(bars))
plt.bar(ind, bars)
plt.xticks(ind+width/2.0, labels, rotation=0)
plt.ylabel('lines of code')

plt.savefig('linesOfCode.png')