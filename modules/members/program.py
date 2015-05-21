#! /usr/bin/env python
__author__ = 'Martin Leinberger'


import sys
import os
import json

sys.path.append('../../libraries')
sys.path.append('../../libraries/101meta')

import const101

mappings = json.load(open('../../libraries/mediawiki/Mappings.json'))['dewikify']
problems = []
namespaceMembers = dict([(ns, []) for ns in mappings.values()])

for page in json.load(open(const101.wikiDump, 'r'))['wiki']['pages']:
    p, n = page.get('p', None), page.get('n', 'None')
    if n.startswith('@'): p = '101'
    elif not p: p = 'Concept'
    if p and n:
        dewikified = mappings.get(p, None)
        if dewikified in namespaceMembers:
            namespaceMembers[dewikified].append(n)
        else:
            problems.append('Unkown namespace: {} ({})'.format(p, n))

for ns in namespaceMembers:
    path = os.path.join(const101.tRoot, ns)
    if not os.path.exists(path):
        os.mkdir(path)
    json.dump(namespaceMembers[ns], open(os.path.join(path, 'members.json'), 'w'), indent=4)

if problems:
    print 'The following problems occured:'
    print json.dumps(problems, indent=4)