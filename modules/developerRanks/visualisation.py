def createImage(env):
    data = env.read_dump('developerRanks')
    xName = 'Language'
    yName = 'Contributor'
    for keys in data.keys():
        xValue = []
        yValue = []
        for key, value in data[keys].items():
            xValue.append(key)
            yValue.append(value)
        env.create_piechart(keys,xName,yName,xValue,yValue)

