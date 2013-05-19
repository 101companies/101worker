#! /usr/bin/env python

import os
import sys
import json

sys.path.append('../../libraries/101meta')
import const101
import tools101

wikiDump = json.load(open(const101.wikiDump, 'r'))
mappings = json.load(open('../../libraries/mediawiki/Mappings.json'))['wikify']





# def findNamespaceMembers(instanceOf):
#     members = []
#     for page in wikiDump['wiki']['pages']:
#         pageData = page['page']
#         if instanceOf in pageData.get('instanceOf', []):
#             members.append(pageData['page']['n'])
#
#     members.sort()
#     return [s.encode('latin_1') for s in members]
#
# def findAndWrite(dirname, instanceOf):
#     members = findNamespaceMembers(instanceOf)
#     path = os.path.join(const101.tRoot, dirname, 'members.json')
#     tools101.makedirs(os.path.dirname(path))
#     json.dump(members, open(path, 'w'))
#
#
# print "Trying to find namespaces..."
# for folderName in mappings.keys():
#     namespace = mappings[folderName]
#     instanceOf = {'p' : 'Namespace', 'n' : namespace}
#     if namespace == '':
#         instanceOf = None
#     findAndWrite(folderName, instanceOf)
#
# findAndWrite('', {'p': 'Namespace', 'n': 'Namespace'})


# This is a bad interface... But I have no clue how to make it better
def findNamespaceMembers(namespace, instanceof, nameRestriction):
    members = []
    for page in wikiDump['wiki']['pages']:
        pageData = page['page']
        if pageData['page']['p'] == namespace and not pageData['page']['n'] == namespace:
            if (instanceof and instanceof in pageData.get('instanceOf',[])) or not instanceof:
                if not nameRestriction or not pageData['page']['n'].startswith(nameRestriction):
                    members.append(pageData['page']['n'])
    members.sort()
    return [s.encode('latin_1') for s in members]


def findAndWrite(dirname, namespace, instanceof=None, nameRestriction=None):
    members = findNamespaceMembers(namespace, instanceof, nameRestriction)
    path = os.path.join(const101.tRoot, dirname, 'members.json')
    tools101.makedirs(os.path.dirname(path))
    json.dump(members, open(path, 'w'))

for folderName in mappings.keys():
    namespace = mappings[folderName]
    if namespace == '':
        findAndWrite(folderName, None, None,'@')
    elif namespace == '101':
        findAndWrite(folderName, None, {'p' : 'Namespace', 'n' : '101'})
    else:
        findAndWrite(folderName, namespace)

findAndWrite('', 'Namespace', {'p': 'Namespace', 'n': 'Namespace'})