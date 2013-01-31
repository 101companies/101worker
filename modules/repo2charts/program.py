#! /usr/bin/env python

__author__ = 'martin'

import metrics
import charts
import json
import os
import sys
sys.path.append('../../libraries/101meta')
import const101

results = metrics.collect()
settings = json.load(open('settings.json', 'r'))
path = os.path.join(os.path.dirname(const101.dumps), 'views')

print 'Generating charts in 101web/views...'

for chart in settings:
	list = []
	for entry in results:
		val = 0
		for rel in chart['relevanceValues']:
			val += entry[rel][chart['metricsValue']]
		list.append(val)
	list.sort()
	charts.makeLineChart(list, os.path.join(path, chart['filename']), **chart)
