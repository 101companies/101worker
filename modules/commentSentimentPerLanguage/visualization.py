def visualize(env):
    data = env.read_dump('sentimentsPerLanguage')
    
    # google input variables
    google_data = []
    google_options = '{title: \'commentSentimentPerLanguage\'}'    

    # filling data
    for key, value in data.items():
        google_data.append([(key+" ("+str(value['Average'][1])+")"), value['Min'], value['Average'][0], value['Average'][0], value['Max']])

    # create  charts
    env.create_googleChart('candlestickChart', 'googleCandle', google_data, google_options)
    

