#! /usr/bin/env python


import urllib2
import json
import sys
import os

sys.path.append('../../libraries/101meta')
import const101


opener = urllib2.build_opener()
problems = []


def loadPage(url):
    req = urllib2.Request(url)
    f = opener.open(req)
    return json.load(f)


def getFileData(file):
    data = loadPage(file['resource'])

    return {
        'name'    : data.get('name', None),
        'language': data.get('language', None),
        'geshi'   : data.get('geshi', None),
        'content' : data.get('content', None)
    }


def extractFiles(entity, languages=[]):
    files = []
    try:
        data = loadPage(entity['resource'])

        for f in data.get('files', []):
            fileData = getFileData(f)
            if not languages or fileData['language'] in languages:
                files.append({
                    'uri' : f['resource'],
                    'data': fileData
                })

        for d in data.get('folders', []):
            files += extractFiles(d)

    except Exception as e:
        problems.append({
            'member' : entity,
            'problem': str(e)
        })

    return files

print 'gathering all files...\n'
filesList = []

contributions = loadPage('http://101companies.org/resources/contributions')
#contributions = loadPage('http://localhost/services/discovery/contributions')
for member in contributions['members']:
    filesList += extractFiles(member)
    sys.stdout.write('.')
    sys.stdout.flush()

print '\n\nanalyzing contents...'
contents = {}
for file in filesList:
    content = file['data']['content']
    if content:
        if not content in contents:
            contents[content] = []
        contents[content].append(file['uri'])

# writing those where multiple file have the same content into the list, ignore others
clonesList = []
for c, v in contents.items():
    if len(v) > 1:
        clonesList.append(v)

json.dump(problems, open('problems.json', 'w'), indent=4)
json.dump(clonesList, open(os.path.join(const101.views, 'clones.json'), 'w'), indent=4)

print '\nFinished - saved clones.json in views\n'
print 'Problems:\n'
print json.dumps(problems, indent=4)