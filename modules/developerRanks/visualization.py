def visualize(env):
    data = env.read_dump('developerRanks')
    
    google_data_bubble = []
    google_data_bubble.append(['Language', '#Contributors', '#Contributions'])
    google_options_bubble = '{title: \'bubble\'}'   

    for keys in data.keys():
        
        # google input variables
        google_data = []
        google_options = '{title: \'' + keys + '\'}'    

        # value labels
        google_data.append(['Contributor', 'Contributioncount'])

        # filling data
        bubble_y = 0
        bubble_x = 0
        for key, value in data[keys].items():
            google_data.append([key, value])
            bubble_x = bubble_x + 1
            bubble_y = bubble_y + value
        
        google_data_bubble.append([keys, bubble_x, bubble_y])
        # create  charts
        env.create_googleChart('pieChart', keys, google_data, google_options)

    env.create_googleChart('bubbleChart', 'bubble', google_data_bubble, google_options_bubble)
        
        
        
    
