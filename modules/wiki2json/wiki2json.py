#!/usr/bin/env python
# coding=utf-8

from pymongo import MongoClient
import json
import os

camelize = lambda words: ''.join(words[0].lower() + words[1:])


def extract_properties(internal_links):
    links = {}
    for link in internal_links:
        if not '::' in link:
            if link.startswith('~'):
               p = 'mentionsNot'
               n = link[1:]
            else:
                p = 'mentions'
                n = link
        else:
            l = link.split('::')
            p = camelize(l[0])  # property
            n = l[1]
        if p in links:
            links[p].append(handle_page_name(n, {}))
        else:
            links[p] = [handle_page_name(n, {})]

    return links


def handle_page_name(name, props):
    if name.startswith('http'):
        return name
    # print name
    n = name.split(':')
    if len(n) == 1:
        props['p'] = None
        props['n'] = n[0]
    else:
        props['p'] = n[0]
        props['n'] = n[1]
    return props


client = MongoClient('localhost', 27017)
db = client['wiki_production']

MONGODB_USER = os.environ['MONGODB_USER']
MONGODB_PWD = os.environ['MONGODB_PWD']

db.authenticate(MONGODB_USER, MONGODB_PWD)

allPages = []
for p in db.pages.find():
    if not p.has_key('page_title_namespace'):
        continue
    if p.has_key('headline'):
        res = {'headline': p['headline']}
    else:
        res = {'headline': 'n/a'}
    handle_page_name(p['page_title_namespace'], res)

    if 'used_links' in p:
        res['internal_links'] = p['used_links']

        properties = extract_properties(res['internal_links'])
        for k, v in properties.items():
            res[k] = v
    else:
        res['internal_links'] = {}

    if 'subresources' in p:
        res['subresources'] = {}
        for sr in p['subresources']:
            for key, value in sr.iteritems():
                res['subresources'][key] = extract_properties(value)
                res['subresources'][key]['internal_links'] = value

    allPages.append(res)

with open('dump.json', 'w') as f:
    f.write(json.dumps({'wiki': {'pageCount': len(allPages), 'pages': allPages}}, sort_keys=True, indent=4))
