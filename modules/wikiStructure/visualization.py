def visualize(env):
    data = env.read_dump('wiki-structure')
    
    # google input variables
    google_data = []
    google_options = '{title: \'relations\'}'    

    # filling data
    google_data = data["structure"]

    # create  charts
    env.create_googleChart('orgChart', 'orgChart', google_data, google_options)
