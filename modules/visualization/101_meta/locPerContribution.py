def meta_locPerContribution(env, res):
	
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
