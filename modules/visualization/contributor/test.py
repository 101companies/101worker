from ..program import check_path
from ..program import write_csv

def run(env, res):
	
	# test
	data = env.read_dump('locPerContribution')
	out = []
	header = ['loc']
	sum_value = ['101_loc']
	for key, value in data.items():
		header.append(key)
		sum_value.append(value)
	out.append(header)
	out.append(sum_value)	
	write_csv('test', 'contributor', out)
