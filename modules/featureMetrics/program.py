#! /usr/bin/env python

import sys
import json
import features
import os
import metrics
import visualization

sys.path.append('../../libraries/101meta')

import tools101
import const101

blacklist = json.load(open('blacklist.json', 'r'))

#features = json.load(open('debugOutput/features.json', 'r'))
features = features.deriveFeaturesForContributions(blacklist)
#metrics = json.load(open('debugOutput/contributionMetrics.json', 'r'))
metrics = metrics.calculateMetricsForContributions(blacklist)


idx = 0

for featureMapping in features:
    if len(featureMapping['contributions']) > 1:
        contributions = featureMapping['contributions']

        path= os.path.join(const101.views, 'features', str(idx))
        tools101.makedirs(path)

        json.dump(featureMapping['features'], open(os.path.join(path, 'features.json'), 'w'), indent=4)
        visualization.visualize(contributions, metrics, os.path.join(path, str(idx)+'.png'))

        idx += 1

print '\n\nFinished'