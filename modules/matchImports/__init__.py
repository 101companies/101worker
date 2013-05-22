import sys
import json

sys.path.append('..')
import interpretRules

sys.path.append('../../libraries/101meta')
import const101
import tools101

def main(data):
    if data['type'] == 'folders':
        folders = data['data']
        folders = map(lambda folder: os.path.join('/tmp/', folder), folders)
        data['data'] = []
        for folder in folders:
            for root, subFolders, files in os.walk(folder):
                for file in files:
                    f = os.path.join(root,file)
                    data['data'].append(f)

    rules = json.load(open(rulesDump))

    apply_rules(data['data'], rules, lambda rule: any(lambda key: key == 'predicate'), rule['rule'].keys())



