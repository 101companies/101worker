#!/usr/bin/env python
# -*- coding: utf-8 -*-

import jinja2
import json
import os

# set environment variable that our test is to be ran
# (is skipped for normal testing as it takes a long time)
os.environ['TEST_ALL_EXPLORER_ENTITIES'] = '1'

manage_py = os.path.join(os.environ["worker101dir"], 'services', 'manage.py')
#os.system('python ' + manage_py + ' test explorer.testAllExplorerEntities')

with open('results.json') as infile:
    data = json.loads(infile.read())

environment = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
template = environment.get_template('main.html')

with open('results.html', 'w') as outfile:
    outfile.write(template.render(data))
