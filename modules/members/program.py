#! /usr/bin/env python

import os
import sys
import json

sys.path.append('../../libraries/101meta')
import const101

wikiDump = json.load(open(const101.wikiDump, 'r'))

def findNamespaceMembers(namespace, instanceof):
    members = []
    for page in wikiDump['wiki']['pages']:
        pageData = page['page']
        if pageData['page']['p'] == namespace and not pageData['page']['n'] == namespace:
            if (instanceof and any(instanceof in s for s in pageData.get('internal_links', []))) or not instanceof:
                members.append(pageData['page']['n'])
    members.sort()
    return [s.encode('ascii') for s in members]
    #return members

def findAndWrite(dirname, namespace, instanceof=None):
    members = findNamespaceMembers(namespace, instanceof)
    path = os.path.join(const101.tRoot, dirname)
    if not os.path.exists(path):
        os.mkdir(path)
    json.dump(members, open(os.path.join(path, 'members.json'), 'w'))

print "Trying to find namespaces..."

findAndWrite('contributions', 'Contribution')
findAndWrite('contributors',  'Contributor')
findAndWrite('languages',     'Language')
findAndWrite('technologies',  'Technology')
findAndWrite('themes',        'Theme')
findAndWrite('vocabularies',  'Vocabulary')
findAndWrite('concepts',      None)
findAndWrite('',              'Namespace', 'instanceof::Namespace:Namespace')