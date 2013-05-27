import copy
import json

sys.path.append('../../libraries')
from service_api import *


def main(data):
    
    if data['type'] != 'folders':
        raise
        
    old_data = copy.copy(data)
    data = expand_data(data)
    
    languages = []
    
    for f in data['data']:
        
        if os.path.exists(f + '.metadata.json'):
            metadata = json.load(open(f + '.metadata.json'))
            
            if metadata.get('relevance', 'system') == 'system':
                for unit in metadata:
                    
                    if unit.has_key('language'):
                        languages.append(unit['language'])
                        
                    if unit.has_key(''                    
            
        
        
