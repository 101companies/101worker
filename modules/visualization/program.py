import os
import json
import csv

'''
output definitions
'''

def check_path(path):
	if not os.path.exists(path):
        	os.mkdir(path)

def write_csv_meta(visualization_name, data):
	path = '../101web/data/views/101_meta'
	check_path(path)
	d = os.path.join(path, visualization_name + '.csv')
	with open(d, 'w') as f:
		wr = csv.writer(f)
		for item in data:
			wr.writerow(item)

def write_csv_contribution(visualization_name, data):
	path = '../101web/data/views/101_contribution'
	check_path(path)
	d = os.path.join(path, visualization_name + '.csv')
	with open(d, 'w') as f:
		wr = csv.writer(f)
		for item in data:
			wr.writerow(item)

def write_csv_contributor(visualization_name, data):
	path = '../101web/data/views/101_contributor'
	check_path(path)
	d = os.path.join(path, visualization_name + '.csv')
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
	
	# locPerContribution - meta - Stacked BarChart
	data = env.read_dump('locPerContribution')
	out = []
	header = ['loc']
	sum_value = ['101_loc']
	for key, value in data.items():
		header.append(key)
		sum_value.append(value)
	out.append(header)
	out.append(sum_value)	
	write_csv_meta('locPerContribution', out)

	# locPerContribution - contribution - BarChart
	data = env.read_dump('locPerContribution')
	out = []
	header = ['contribution','loc']
	out.append(header)	
	for key, value in data.items():
		out.append([key, value])
	write_csv_contribution('locPerContribution', out)
