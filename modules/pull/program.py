#! /usr/bin/env python

import sys
import os
import json

def update(repo, path):
    cwd = os.getcwd()

    if os.path.exists(path):
        os.chdir(path)
        cmd = 'git pull'
    else:
        os.makedirs(path)
        os.chdir(path)
        cmd = 'git clone {0} .'.format(repo)

    status = os.system(cmd)
    if status:
        print('Failed to update {0}'.format(repo))
        return status

    os.chdir(cwd)
    return 0


repos = json.load(open('repositories.json', 'r'))
ret   = 0

for target in repos:
    try:
        ret |= update(target['repo'], target['targetdir'])
    except os.error as e:
        print(e.strerror)
        ret |= e.errno

print('\n\nFinished updating repos with {0}errors'.format('' if ret else 'no '))
sys.exit(ret)
