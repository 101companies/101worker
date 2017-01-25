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

def create_barchart(xName,yName,xValues,yValues,moduleName,env):
    path = env.get_env("views101dir")+os.sep+'Module'
    check_path(path)
    path = path +os.sep+moduleName
    check_path(path)
    d = os.path.join(path, 'data.tsv')
    data = []
    #labels = [xName,yName] actually not in use because of special read in format
    labels = ['letter','frequency']
    data.append(labels)
    for x,y in zip(xValues,yValues): 
        data.append([x,y])
    with open(d, 'w') as f:
        wr = csv.writer(f, delimiter = "\t")        
        for item in data:
            wr.writerow(item)
    #TODO: shutil copy js data (like the one at http://bl.ocks.org/mbostock/3885304) to path



'''
program
+ graphs need to be put into seperate folders: meta, contribution, contributor
+ 1 file per graph
'''

def run(env, res):

	# modules
	from .module.locPerContribution import run as runLocPerContribution
	runLocPerContribution(env, res)
