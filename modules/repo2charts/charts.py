__author__ = 'martin'

import sys
import metrics
try:
	import matplotlib
	matplotlib.use('Agg')
	from matplotlib import pyplot
except ImportError:
	print 'This module needs matplotlib - please install it'
	print 'You can find more infos @ http://matplotlib.org/'
	sys.exit(1)

def makeLineChart(values, fileName, **kwargs):
	pyplot.clf()
	pyplot.plot(values, marker=kwargs.get('marker', None))
	if 'annotations' in kwargs:
		for annotation in kwargs['annotations']:
			value = 0
			pos = 0
			if annotation["type"] == "median":
				value, pos = metrics.medianAndPos(values)
			annotation.pop("type")
			pyplot.annotate(annotation.pop('text') + str(value), (pos,values[pos]),**annotation)
	if 'xlabel' in kwargs: pyplot.xlabel(kwargs['xlabel'])
	if 'ylabel' in kwargs: pyplot.ylabel(kwargs['ylabel'])
	if 'title' in kwargs: pyplot.title(kwargs['title'])
	pyplot.savefig(fileName)
