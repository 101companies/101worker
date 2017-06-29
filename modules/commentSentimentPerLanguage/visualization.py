def visualize(env):
    data = env.read_dump('sentimentsPerLanguage')
    
    # google input variables
    google_data = []
    google_options = '{title: \'commentSentimentPerLanguage\'}'    

    # filling data
    for key, value in data.items():
        google_data.append([key, value['Min'][0], value['Min'][0], value['Max'][0], value['Max'][0]])

    # create  charts
    env.create_googleChart('candlestickChart', 'googleCandle', google_data, google_options)
    

