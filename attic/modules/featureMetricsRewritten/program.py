#! /usr/bin/env python

import sys
import matplotlib

matplotlib.use('Agg')

import numpy as np
import matplotlib.pyplot as plt

sys.path.append('../../libraries')
sys.path.append('../../libraries/101meta')

from metamodel import *

import config
from config import validateAutomaticTagging


#build "Feature" -> ["File 1", "File 2", ...] association
featureIndex = {}
contributions = Namespace('contributions')

for folders, files in walk(contributions):
    for file in files:
        for feature in file.features:
            featureIndex.setdefault(feature, []).append(file)


#validation of results
validateAutomaticTagging(featureIndex)
#validate through wiki page
for contribution in config.contributionWhitelist:
    for f in (set(contribution.implements) & config.featuresToInspect):
        if not any(file.member == contribution for file in
                   featureIndex.get(f, [])) and not f in config.implicitlyImplemented.get(contribution.name, []):
            print 'Warning: missing feature {} for contribution {}'.format(f, contribution.name)


#build "contributionName" -> "ncloc" association
contributionIndex = {}
examinedFiles = []
for feature in config.featuresToInspect:
    for file in featureIndex.get(feature, []):
        member = file.member
        if member in config.contributionWhitelist and file.metrics.exists and file.relevance == 'system' and not file in examinedFiles:
            print member.name
	    contributionIndex[member.name] = contributionIndex.get(member.name, 0) + file.metrics.ncloc
            examinedFiles.append(file)




#----------------------------------------------------------
#visualize results
bars = contributionIndex.values()
labels = contributionIndex.keys()

figure = plt.figure()
width = 0.35

ind = np.arange(len(bars))
plt.bar(ind, bars)
plt.xticks(ind + width / 2.0, labels, rotation=15)
plt.ylabel('lines of code (ncloc)')

plt.savefig('linesOfCode.png')
