#! /usr/bin/env python

import sys
import os
import json

def update(repo, path):
    cwd = os.getcwd()

    if os.path.exists(path):
        os.chdir(path)
        cmd = "git pull"
    else:
        os.chdir(os.path.dirname(path))
        cmd = "git clone " + repo

    status = os.system(cmd)
    if status:
        print "Failed to update {0}".format(repo)
        sys.exit(status)

    os.chdir(cwd)

repos = json.load(open('repositories.json', 'r'))

for target in repos:
    update(target['repo'], target['targetdir'])

print '\n\nFinished updating repos'