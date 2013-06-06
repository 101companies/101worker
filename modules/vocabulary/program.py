#!/usr/bin/env python
#coding=utf-8

import json
import urllib2
import asq
from asq.initiators import query
import sys
import os
from jinja2 import FileSystemLoader, Environment

sys.path.append('../../libraries/101meta')
sys.path.append('../../libraries')
import const101
import tools101
from mediawiki import remove_headline_markup

output = os.path.join(const101.tRoot, 'vocabularies')
output = os.path.abspath(output)

if not os.path.exists(output):
    os.mkdir(output)

wikidump = json.load(open(sys.argv[1], 'r'))
pages = wikidump['wiki']['pages']

vocs = (query(pages).where(lambda page: page['page']['page']['p'] == 'Vocabulary')
    .select(lambda p: p['page']['page']['n']).to_list())

def toTex(list, file):
    with open (file, 'w') as f:
        f.write(',\n'.join(map(lambda x: "\wikipage{" + x['name'] + "}",  list)))

for voc in vocs:
    voc_name = unicode('instanceOf::Vocabulary:' + voc).strip()
    
    instances = (query(pages).where(lambda page: voc_name in page['page'].get('internal_links', [])).to_list())

    if not os.path.exists(os.path.join(output, voc)):
        os.mkdir(os.path.join(output, voc))

    f = open(os.path.join(output, voc, 'members.json'), 'w')
    data = []

    for instance in instances:
        data.append({
            'name': instance['page']['page']['n'],
            #'namespace': instance['page']['page']['p'] or '',
            'headline': remove_headline_markup(instance['page'].get('headline', ''))
        })

    data = sorted(data, key=lambda s: s['name'])
    for d in data:
        if data.count(d) > 1:
            data.remove(d)

    json.dump(data, f, indent=4, sort_keys=True)
    f.close()

    loader = FileSystemLoader('.')
    env = Environment(loader=loader)
    template = env.get_template('html.tpl')

    f = open(os.path.join(output, voc, 'members.html'), 'w')
    f.write(template.render({'data': data}))
    f.close()

    template = env.get_template('tex.tpl')

    f = open(os.path.join(output, voc, 'members.tex'), 'w')
    f.write(template.render({'data': data}))
    f.close()

    toTex(data, os.path.join(output, voc, 'members_list.tex'))
