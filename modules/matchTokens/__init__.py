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

    logging.basicConfig(filename='matchSimpleRules.log',level=logging.DEBUG)

    data = expand_data(data)

    rules = json.load(open(const101.rulesDump))
    fpredicate_rules = interpretRules.group_fast_predicates(rules)
    print fpredicate_rules

    interpretRules.apply_rules(data['data'], fpredicate_rules, lambda rule: lambda rule: rule['rule']['fpredicate'] == "technologies/fpredicate_generic_platform/tokens.py", append=True)
