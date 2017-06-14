def visualize(env):
    data = env.read_dump('locPerContribution')
    
    # google input variables
    google_data = []
    google_options = '{title: \'locPerContribution\'}'    

    # value labels
    google_data.append(['contribution', 'loc'])

    # filling data
    for key, value in data.items():
        google_data.append([key, value])

    # create  charts
    env.create_googleChart('pieChart', 'googlePie', google_data, google_options)
    env.create_googleChart('barChart', 'googleBar', google_data, google_options)
    env.create_googleChart('lineChart', 'googleLine', google_data, google_options)
    env.create_googleChart('bubbleChart', 'googleBubble', google_data, google_options)
