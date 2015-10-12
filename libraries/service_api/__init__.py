import os
import copy
import sys

def expand_data(data, tmp=True):
    print data
    data = copy.copy(data)
    if data['type'] == 'folders':
            folders = data['data']
            folders = map(lambda folder: os.path.join(folder), folders)
            data['data'] = []
            for folder in folders:
                for root, subFolders, files in os.walk(folder, followlinks=True):
                    for file in files:
                        f = os.path.join(root,file)
                        data['data'].append(f)
                        
    data['data'] = filter(lambda f: not any(map(lambda e: f.endswith(e), ('.metadata.json', '.metrics.json', '.extractor.json', '.tokens.json', '.refinedTokens.json'))), data['data'])
    return data
    
