def createImage(env):
    data = env.read_dump('locPerContribution')
    out = []
    xName = 'Contribution'
    yName = 'Lines of Code'
    xValue = []
    yValue = []
    
    data_in = []
    options_in = '{title: \'locPerContribution\'}'    

    data_in.append(['contribution', 'loc'])

    for key, value in data.items():
        xValue.append(key)
        yValue.append(value)
        data_in.append([key, value])

<<<<<<< HEAD
    #env.create_piechart('Piechart1','locPerContribution',xName,yName,xValue,yValue)

    env.create_googleChart_pie('locPerContribution', 'googlePieFTW', options_in, data_in)
=======
    env.create_piechart('Piechart1',xName,yName,xValue,yValue)
<<<<<<< HEAD
    env.create_piechart('Piechart6',xName,yName,xValue,yValue)
    env.create_piechart('Piechart999',xName,yName,xValue,yValue)
=======
>>>>>>> f28d9b9e9e25722e593d0e03569310596222d192

>>>>>>> bda499c19c38fedee986d5c2c3b4cd9b120029ac
