import os
import json
import csv

'''
output definitions
'''

def check_path(path):
	if not os.path.exists(path):
        	os.mkdir(path)

def write_csv(name, dest, data):
	path = {'meta': '../101web/data/views/meta',
		'contribution': '../101web/data/views/contribution',
		'contributor': '../101web/data/views/contributor',
		'module': '../101web/data/views/module'}	

	destination = path[dest]
	check_path(destination)
	d = os.path.join(destination, name + '.csv')
	with open(d, 'w') as f:
		wr = csv.writer(f)
		for item in data:
			wr.writerow(item)


'''
program
+ graphs need to be put into seperate folders: meta, contribution, contributor
+ 1 file per graph
'''

def run(env, res):
	
	# meta
	from .meta.test import run as test_meta
	test_meta(env, res)
	
	# contribution	
	from .contribution.test import run as test_contribution
	test_contribution(env, res)

	# contributor
	from .contributor.test import run as test_contributor
	test_contributor(env, res)

	# modules
	from .module.test import run as test_module
	test_module(env, res)
