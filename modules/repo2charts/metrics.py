import json
import sys
import os
sys.path.append('../../libraries/101meta')
import const101

relevanceValues = ['system', 'ignore', 'derive', 'reuse']
metricValues = ['ncloc', 'loc', 'numberOfFiles', 'size']

def metricsDefault():
	data = {}
	for rel in relevanceValues:
		metricsData = {}
		for m in metricValues:
			metricsData[m] = 0
		data[rel] = metricsData
	return data


def medianAndPos(list):
	list.sort()
	if len(list) % 2 == 1:
		pos = (len(list) + 1) / 2
		return list[pos], pos
	pos = len(list) / 2
	return (list[pos] + list[pos+1]) / 2.0 , pos + 1

def collect():
	result = []
	path = os.path.join(const101.tRoot, 'contributions')
	for contrib in os.listdir(path):
		if os.path.isdir(os.path.join(path, contrib)):
			print 'Looking at ' + os.path.join(path, contrib)
			index = json.load(open(os.path.join(path, contrib, 'index.json'), 'r'))
			data = metricsDefault()
			for lang in index['languages']:
				langData = index['languages'][lang]
				for rel in relevanceValues:
					for m in metricValues:
						data[rel][m] += langData['metrics'][rel][m]

			result.append(data)
	return result