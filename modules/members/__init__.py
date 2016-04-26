#! /usr/bin/env python
__author__ = 'Martin Leinberger'


import sys
import os
import json

sys.path.append('../../libraries')
sys.path.append('../../libraries/101meta')

config = {
    'wantdiff': False
}


def run(context):
    mappings = json.load(open('modules/members/Mappings.json'))['dewikify']
    problems = []
    namespaceMembers = dict([(ns, []) for ns in mappings.values()])

    for page in json.load(open(context.get_env('wiki101dump'), 'r'))['wiki']['pages']:
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
        path = os.path.join(context.get_env('targets101dir'), ns)
        if not os.path.exists(path):
            os.mkdir(path)
        json.dump(namespaceMembers[ns], open(os.path.join(path, 'members.json'), 'w'), indent=4)

    if problems:
        print 'The following problems occured:'
        print json.dumps(problems, indent=4)
