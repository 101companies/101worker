#! /usr/bin/env python


import os
import commands
import json
import sys
sys.path.append('../../libraries/101meta')
import const101
import tools101
import re

#TODO make incremental
#TODO add to production.config

debug = False

commits = []
cmd = 'git log --name-status --format="%H|%an|%ct|%ce"'
cwd = os.getcwd()
results101 = os.path.dirname(const101.sRoot)
regex = re.compile('.*/(?P<folder>[^\.]+)\.git')

def parseOutput(output, prefix):
    commits = []
    lines = output.splitlines(True)

    commitInfo = None
    for line in lines:
        if '|' in line:
            if commitInfo:
                commits.append(commitInfo)
            commitInfo = {}
            parts = line.split('|')
            commitInfo['sha']       = parts[0]
            commitInfo['author']    = parts[1]
            commitInfo['timestamp'] = parts[2]
            commitInfo['email']     = parts[3].replace('\n', '')
            commitInfo['changes']   = []
        elif not line == '\n':
            parts = line.split('\t')
            file = parts[1].replace('\n', '')
            if prefix in file:
                commitInfo['changes'].append({
                    'action': parts[0],
                    'file': file
                })

    return commits


#gather repositories, which have to analyzed
print 'Gathering commit infos from all repositories'
toAnalyze = [{'path': const101.sRoot, 'sourcedir': '', 'targetdir':'', 'mode': None}]

gitdeps = json.load(open(os.path.join(const101.sRoot, '.gitdeps'), 'r'))
for dep in gitdeps:
    match = regex.match(dep['sourcerepo'])
    toAnalyze.append({
        'path': os.path.join(results101,'gitdeps',match.group('folder')),
        'sourcedir': dep['sourcedir'][1:],
        'targetdir': dep['targetdir'],
        'mode'     : dep.get('mode', None)
    })

#analyze main repo
for target in toAnalyze:
    os.chdir(target['path'])
    status, output = commands.getstatusoutput(cmd)
    os.chdir(cwd)



    if status:
        raise Exception('problem with "git log" command', output)

    cs = parseOutput(output, target['sourcedir'])
    for c in cs:
        for ch in c['changes']:
            if target['sourcedir'] == '':
                ch['file'] = os.path.join(target['targetdir'],ch['file'])
            else:
                ch['file'] = ch['file'].replace(target['sourcedir'], target['targetdir'], 1)

    commits += cs


if debug:
    json.dump(commits, open('temporary.debug.json', 'w'), indent=4)

print 'Finished gathering, will now associate commits with files'

#map created list to real files
for root, dirs, files in os.walk(const101.sRoot):
    for file in files:
        fileInfo = []
        relPath = os.path.join(root,file).replace(const101.sRoot, '')[1:]
        for commit in commits:
            for change in commit['changes']:
                if change['file'] == relPath:
                    fileInfo.append({
                        'author': commit['author'],
                        'email': commit['email'],
                        'timestamp': commit['timestamp'],
                        'action' : change['action']
                    })

        fileInfo = sorted(fileInfo, key=lambda k: k['timestamp'])
        if not os.path.exists(os.path.dirname(os.path.join(const101.tRoot,relPath))):
            os.makedirs(os.path.join(const101.tRoot,relPath))

        json.dump(fileInfo, open(os.path.join(const101.tRoot,relPath+'.commitInfo.json'), 'w'))
        tools101.tick()

print '\nFinished'
