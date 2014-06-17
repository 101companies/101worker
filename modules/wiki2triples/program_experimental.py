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

for model in models:
    allowed_relations[model] = []
    x = json.load(urllib.urlopen("http://worker.101companies.org/data/onto/models/"+model+".json"))
    for property in x.get('properties',[]):
        allowed_relations[model].append(property['property'])

print allowed_relations