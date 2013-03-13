#! /usr/bin/env python

import os
import sys
import json

sys.path.append('../../libraries/101meta')
import const101

wikiDump = json.load(open(const101.wikiDump, 'r'))

def findNamespaceMembers(namespace):
    members = []
    for page in wikiDump['wiki']['pages']:
        pageData = page['page']
        if pageData['page']['p'] == namespace:
            members.append(pageData['page']['n'])
    return members

def findAndWrite(dirname, namespace):
    members = findNamespaceMembers(namespace)
    path = os.path.join(const101.tRoot, dirname)
    if not os.path.exists(path):
        os.mkdir(path)
    json.dump(members, open(os.path.join(path, 'members.json'), 'w'), indent=4)

findAndWrite('contributions', 'Contribution')
findAndWrite('contributors', 'Contributor')
findAndWrite('languages', 'Language')
findAndWrite('technologies', 'Technology')
findAndWrite('themes', 'Theme')
findAndWrite('vocabularies', 'Vocabulary')
findAndWrite('concepts', None)

print 'Finished analyzing the wiki'