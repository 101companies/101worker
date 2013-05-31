import sys
import json

sys.path.append('..')
import interpretRules

sys.path.append('../../libraries')
from service_api import *

sys.path.append('../../libraries/101meta')
import const101
import tools101

def main(data):
    print data
    data = expand_data(data)

    rules = json.load(open(const101.rulesDump))

    interpretRules.apply_rules(data['data'], rules, lambda rule: any(filter(lambda key: key  == 'predicate', rule['rule'].keys())), append=True)

