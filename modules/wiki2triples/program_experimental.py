# -*- coding: utf-8 -*-
__author__ = 'Martin Leinberger'

import sys
sys.path.append('../../libraries')
sys.path.append('../../libraries/101meta')
import urllib
import json
import os



allowed_relations = {}
erroneous_pages = []

models = os.listdir('./../validate/models')
print models
for model in models:
    model_name = model.replace('.json', '')
    allowed_relations[model_name] = []
    x = json.load(open('../validate/models/' + model, 'r'))
    for property in x.get('properties', []):
        allowed_relations[model_name].append(property['property'])
print allowed_relations
for y in filter(lambda x: x not in ['entity'], allowed_relations.keys()):
    allowed_relations[y] += allowed_relations['entity']


print json.dumps(allowed_relations, indent=4)