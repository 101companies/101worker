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

def handlePage(p):
    if p.has_key('headline'):
        res = {'headline': p['headline']}
    else:
        res = {'headline': 'n/a'}
    handle_page_name(p['page_title_namespace'], res)

    res['_id'] = p['_id']['$oid']

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

    return res

import storm

class Wiki2JSONBolt(storm.BasicBolt):

    def __init__(self):
        storm.BasicBolt.__init__(self)
        self.client = MongoClient()
        self.db = self.client['wiki2json']
        self.pages = self.db['pages']
        self.pages.drop()

    def add_page(self, page):
        return self.pages.insert_one(page)

    def update_page(self, page):
        return self.pages.update({ '_id': page['_id'] }, { '$set': page }, upsert=False)

    def remove_page(self, page):
        return self.pages.remove(page['_id'])

    def emit_output(self, action, page, result):
        storm.emit([action, page['raw_content'], result['n'],
            result['p'], result])

    def process(self, tup):
        event = json.loads(tup.values[0])
        page = event['page']
        result = handlePage(page)

        if event['action'] == 'created':
            self.add_page(result)

        elif event['action'] == 'updated':
            self.update_page(result)

        else:
            self.remove_page(result)

        self.emit_output(event['action'], page, result)

        # with open('dump.json', 'w') as f:
            # f.write(json.dumps({'wiki': {'pageCount': pages.count(), 'pages': list(pages.find())}}, sort_keys=False))

        # storm.ack(tup)

Wiki2JSONBolt().run()
