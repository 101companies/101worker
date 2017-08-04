import os
import json

config = {
    'wantdiff': False,
    'wantsfiles': False,
    'threadsafe': True,
    'behavior': {
        'creates': [['dump', 'moduleDependencies']]
    }
}

dir = os.path.dirname(__file__)

with open(os.path.join(dir, 'config.json')) as f:
    config = json.load(f)


def run(env):
    json = env.read_dump('moduleDescriptions')
    endingToModule = []
    #modules, who directly depend on wiki dump:
    wiki_modules = ['dumpMongoDBToJson','mongodump','extractFacts','zip','pull']
    
    #create endingToModule
    for data in json:
        module_name = data['name']
        behavior = data['behavior'] 
        create = behavior.get('creates')
        if create != None:
            endingToModule.append({'name': module_name, 'creates': create})

    for data in json:
        if data.get('behavior').get('creates') != None:
            data['behavior'].pop('creates')
        if data.get('behavior').get('uses') != None:
            for entry in endingToModule:
                for uses in data['behavior']['uses']:
                    for creates in entry['creates']:
                        if creates == uses:
                            data ['behavior']['uses'].remove(uses)
                            data ['behavior']['uses'].append(entry)

    #built output
    result = []
    for data in json:
        if data.get('behavior').get('uses') != None:
            result.append({data['name']:data['behavior']['uses']})
        else:
            result.append({data['name']:[]})
    
    #remove modules who depend on wiki
    for wiki_module in wiki_modules:
        for entry in result:
            if wiki_module in entry.keys():
                result.remove(entry)
    
    #remove all modules who transitively depend on the wiki
    while(wiki_modules):
        for entry in result:
            for key in entry.keys():
                for value in entry.values():
                    for wiki_module in wiki_modules:
                        if wiki_module in value:
                            wiki_modules.append(key)
                            result.remove(entry)
                            break
        wiki_modules.pop(0)

    final = {}
    for entry in result:
        for key in entry.keys():
            for value in entry.values():
                final[key] = value

    env.write_dump('moduleDependencies',final)


                
