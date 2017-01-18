#! /usr/bin/env python

import os
import sys
import json
import subprocess

import json
import os

dir = os.path.dirname(__file__)

with open(os.path.join(dir, 'config.json')) as f:
    config = json.load(f)

def run(context, change):
    '''
    New/Changed files:
        - get the language
        - find the matching extractor (https://github.com/101companies/101docs/blob/master/worker/extractors.md)
        - run the extractor
        - save the extractor output as a derived resource
    Deleted Files:
        - remove a possible extractor resource
    '''
    if change['type'] == 'NEW_FILE' or change['type'] == 'FILE_CHANGED':
        language = context.get_derived_resource(change['file'], 'lang')

        path = os.path.abspath(os.path.join('extractors', language, 'extractor'))
        # we ignore non-existant extractors
        if os.path.exists(path):
            extractor = path

            # run the extractor
            source_file = os.path.join(context.get_env('repo101dir'), change['file'])
            command = "{0} < \"{1}\"".format(extractor, source_file)
            output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True).decode('utf-8')

            context.write_derived_resource(change['file'], json.loads(output), 'extractor')
    else:
        context.remove_derived_resource(change['file'], 'extractor')

import unittest
from unittest.mock import Mock, patch

class RunTest(unittest.TestCase):

    @patch('subprocess.check_output')
    def test_run(self, check_output):
        check_output.return_value = '{ "imports": [] }'

        change = {
            'type': 'NEW_FILE',
            'file': 'some-file.py'
        }

        env = Mock(**{'get_derived_resource.return_value': 'Python', 'get_env.return_value': '/some/path'})
        lang = env.get_derived_resource('some-file.py', 'lang')
        os.path.join('extractors', lang, 'extractor')

        run(env, change)

        check_output.assert_called_with('extractors/Python/extractor < "/some/path/some-file.py"', stderr=-2)

def test():
    suite = unittest.TestLoader().loadTestsFromTestCase(RunTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
