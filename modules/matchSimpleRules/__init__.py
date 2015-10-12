import sys
import json
import os

sys.path.append('..')
import interpretRules

sys.path.append('../../libraries/101meta')
import const101
import tools101

import logging

sys.path.append('../../libraries')
from service_api import *

def main(data):

    data = expand_data(data)

    rules = json.load(open(const101.rulesDump))

    interpretRules.apply_rules(data['data'], rules, lambda rule: not any(filter(lambda key: key in ('predicate', 'fpredicate', 'content', 'locator'), rule['rule'].keys())), False)



