import copy
import json
import sys

sys.path.append('../../libraries')
from service_api import *


def main(data):
    
    if data['type'] != 'folders':
        raise
        
    old_data = copy.copy(data)
    data = expand_data(data)
    
    languages = []
    technologies = []
    concepts = []
    features = []
    
    for f in data['data']:
        
        if os.path.exists(f + '.metadata.json'):
            metadata = json.load(open(f + '.metadata.json'))
            for m in metadata:
                if m.get('relevance', 'system') == 'system':
                    for unit in m['metadata']:
                        
                        if unit.has_key('language'):
                            languages.append(unit['language'])
                        
                        elif unit.has_key('dependsOn'):
                            technologies.append(unit['dependsOn'])
   
                        elif unit.has_key('concept'):
                            concepts.append(unit['concept'])
                            
                        elif unit.has_key('feature'):
                            features.append(unit['feature'])
   
    print {
        'languages' : list(set(languages)),
        'technologies': list(set(technologies)),
        'concepts': list(set(concepts)),
        'features': list(set(features))
    }
    
    f = open(os.path.join(old_data['data'][0], 'summary.json'), 'w')
    json.dump({
        'languages' : list(set(languages)),
        'technologies': list(set(technologies)),
        'concepts': list(set(concepts)),
        'features': []
    }, f)
    f.close()
        

if __name__ == '__main__':
    main({'data': ['/tmp/jaxbExtension/contributions/jaxbExtension'], 'type': 'folders'})
        
        
