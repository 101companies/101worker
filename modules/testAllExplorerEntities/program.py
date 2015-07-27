#!/usr/bin/env python
# -*- coding: utf-8 -*-

import jinja2
import json
import os

# set environment variable that our test is to be ran
# (is skipped for normal testing as it takes a long time)
os.environ['TEST_ALL_EXPLORER_ENTITIES'] = '1'

manage_py = os.path.join(os.environ["worker101dir"], 'services', 'manage.py')
os.system('python ' + manage_py + ' test explorer.testAllExplorerEntities')

with open('results.json') as infile:
    data = json.loads(infile.read())

# For debugging, limit high error listings to 100
# data['fragment_errors']['error_list']['ResourceNotFoundException'] = \
#     data['fragment_errors']['error_list']['ResourceNotFoundException'][:100]
# data['fragment_errors']['error_list']['ResourceAlreadyAssignedError'] = \
#     data['fragment_errors']['error_list']['ResourceAlreadyAssignedError'][:100]

environment = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
template = environment.get_template('main.html')

outpath = os.path.join(os.environ['views101dir'], 'testAllExplorerEntities.html')
with open(outpath, 'w') as outfile:
    outfile.write(template.render(data))
