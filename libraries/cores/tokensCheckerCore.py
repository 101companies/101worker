#! /usr/bin/env python

import sys
import os
import json
sys.path.append('../../libraries/101meta')
import const101



def gatherRules():
    l = []
    rules = json.load(open(const101.rulesDump, 'r'))['results']['rules']
    for r in rules:
        if 'tokensChecker.py' in r['rule'].get('predicate', ''):
            l.append(r)

    return l

def check(tokens, rules):
    units = []
    for r in rules:
        if set(r['rule']['args']).issubset(tokens):
            units.append({'id': 0, 'metadata': r['rule']['metadata'][0]})

    return units