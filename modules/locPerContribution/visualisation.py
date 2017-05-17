def createImage(env):
    data = env.read_dump('locPerContribution')
    out = []
    xName = 'Contribution'
    yName = 'Lines of Code'
    xValue = []
    yValue = []
    for key, value in data.items():
        xValue.append(key)
        yValue.append(value)

    env.create_piechart('Piechart1',xName,yName,xValue,yValue)

