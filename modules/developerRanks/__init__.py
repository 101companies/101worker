from collections import Counter

import matplotlib.pylot as plt
import seaborn as sns

config = {
    'wantdiff': False,
    'wantsfiles': False,
    'threadsafe': False,
    'behavior': {
        'uses': [['dump', 'wiki-links']],
        'creates': [['dump', 'developerRanks']]
    }
}

def run(env):
    wiki_dump = env.read_dump('wiki-links')

    pages = wiki_dump['wiki']['pages']
    
    data = {}

    contributions = filter(lambda p: 'Contribution' == p.get('p', ''), pages)
    for c in contributions:

        languages = [c.get('Uses', [])]
        languages = [p for language in languages for p in language]

        languages = list(filter(lambda u: u['p'] == 'Language', languages))
        languages = [language['n'].replace('_', ' ') for language in languages]
    
        contributors = [c.get('DevelopedBy', [])]
        contributors = [p['n'] for contributor in contributors for p in contributor]

        
    
         	
        for language in languages:
            if language in data.keys():
                data2 = data[language]
            else:  
                data2 = {}
            for contributor in contributors:    
                if contributor in data2.keys():                
                    data2[contributor] = data2[contributor] + 1
                else: 
                    data2[contributor] = 1
               
            data[language] = data2
   
    env.write_dump('developerRanks', data)

    x = []
    y = []
    for (k,v) in data['Javascript']:
        x.append(k)
        y.append(v)
    sns.barplot(x, y)
    sns.plt.show()










