import sys
import json
<<<<<<< HEAD
import os
=======
>>>>>>> 789459768f776d4d06b3c35544858ffc922ad749

sys.path.append('..')
import interpretRules

sys.path.append('../../libraries/101meta')
import const101
import tools101

<<<<<<< HEAD
import logging

sys.path.append('../../libraries')
from service_api import *

def main(data):

    logging.basicConfig(filename='matchSimpleRules.log',level=logging.DEBUG)

    data = expand_data(data)

    rules = json.load(open(const101.rulesDump))

    interpretRules.apply_rules(data['data'], rules, lambda rule: not any(filter(lambda key: key in ('predicate', 'fpredicate', 'content', 'locator'), rule['rule'].keys())), False)
=======
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

    apply_rules(data['data'], rules, lambda rule: not any(lambda key: key in ('predicate', 'fpredicate', 'content', 'locator'), rule['rule'].keys())
>>>>>>> 789459768f776d4d06b3c35544858ffc922ad749



