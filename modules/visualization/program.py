import os
import json
import csv


'''
write functions
'''

def check_path(path):
	if not os.path.exists(path):
       		os.mkdir(path)

def write_csv(name, source, dest, data, env):
	destination = os.path.join(env.get_env('views101dir'), source)
	check_path(destination)
	destination = os.path.join(destination, dest)
	check_path(destination)
	d = os.path.join(destination, name + '.csv')
	with open(d, 'w') as f:
		wr = csv.writer(f)
		for item in data:
			wr.writerow(item)
	
def write_tsv(name, source, dest, data, env):
	destination = env.get_env('views101dir')
	destination = os.path.join(destination, source, dest)
	check_path(destination)
	d = os.path.join(destination, name + '.tsv')
	with open(d, 'w') as f:
		wr = csv.writer(f, delimiter='\t')
		for item in data:
			wr.writerow(item)


'''
write functions
'''
		
def assemble_barchart(xName,yName,xValues,yValues, source, dest, env):
	out = []
	labels = ['letter','frequency']
	out.append(labels)
	for x,y in zip(xValues,yValues): 
		out.append([x,y])
	write_tsv('bar', source, dest, out, env)

def assemble_piechart(xName,yName,xValues,yValues, source, dest, env):
	out = []
	labels = [xName,yName]
	out.append(labels)
	for x,y in zip(xValues,yValues): 
		out.append([x,y])
	write_csv('pie', source, dest, out, env)


'''
program
'''

def run(env, res):

	# modules
	from .module.locPerContribution import run as runLocPerContribution
	runLocPerContribution(env, res)
