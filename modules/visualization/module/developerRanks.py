from ..program import assemble_piechart

def run(env, res):

	data = env.read_dump('locPerContribution')
	out = []
	xName = 'Contribution'
	yName = 'Lines of Code'
	xValues = []
	yValues = []
	for key, value in data.items():
		xValues.append(key)
		yValues.append(value)

	assemble_piechart("normal",xName, yName, xValues, yValues, 'locPerContribution', env)
	assemble_piechart("inverted",yName, xName, xValues, yValues, 'locPerContribution', env)
