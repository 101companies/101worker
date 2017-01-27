from ..program import assemble_barchart
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

	assemble_barchart(xName, yName, xValues, yValues,'module', 'locPerContribution', env)
	assemble_piechart(xName, yName, xValues, yValues,'module', 'locPerContribution', env)
