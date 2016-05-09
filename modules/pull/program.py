#! /usr/bin/env python

import sys
import os
import json
import re

def update(repo, path, context):
    cwd  = os.getcwd()
    path = re.sub('\$(\w+)', lambda match: context.get_env(match.group(1)), path)

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

def load_repos():
    repo_json = os.path.join(os.path.dirname(__file__), 'repositories.json')
    with open(repo_json, 'r') as f:
        return json.load(f)

def run(context):
    repos = load_repos()
    ret   = 0

    for target in repos:
        try:
            ret |= update(target['repo'], target['targetdir'], context)
        except os.error as e:
            print(e.strerror)
            ret |= e.errno

    print('\n\nFinished updating repos with {0}errors'.format('' if ret else 'no '))

import unittest

class TestPull(unittest.TestCase):

  def test_load(self):
      self.assertTrue(len(load_repos()) > 0)

def test():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPull)
    unittest.TextTestRunner(verbosity=2).run(suite)
