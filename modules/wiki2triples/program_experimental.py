# -*- coding: utf-8 -*-
__author__ = 'Martin Leinberger'

import sys
sys.path.append('../../libraries')
sys.path.append('../../libraries/101meta')
import urllib
import json

models = ["concept", "contribution", "contributor", "feature", "language",
          "technology", "vocabulary"]
allowed_relations = {}
erroneous_pages = []

for model in models:
    allowed_relations[model] = []
    x = json.load(urllib.urlopen("http://worker.101companies.org/data/onto/models/"+model+".json"))
    for property in x.get('properties', []):
        allowed_relations[model].append(property['property'])

    for y in filter(lambda x: x not in ['concept'], allowed_relations.keys()):
        allowed_relations[y] += (allowed_relations['concept'])


print json.dumps(allowed_relations, indent=4)