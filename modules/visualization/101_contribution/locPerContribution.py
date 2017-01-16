def contribution_locPerContribution(env, res):

	# locPerContribution - contribution - BarChart
	data = env.read_dump('locPerContribution')
	out = []
	header = ['contribution','loc']
	out.append(header)	
	for key, value in data.items():
		out.append([key, value])
	write_csv_contribution('locPerContribution', out)
