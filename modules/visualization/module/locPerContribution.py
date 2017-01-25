from ..program import check_path
from ..program import create_barchart

def run(env, res):

    data = env.read_dump('locPerContribution')
    out = []
    xName = ['Contribution']
    yName = ['Lines of Code']
    xValues = []
    yValues = []
    for key, value in data.items():
        xValues.append(key)
        yValues.append(value)
    create_barchart(xName, yName, xValues, yValues,'locPerContribution', env)
