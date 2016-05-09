#! /usr/bin/env python

import os
import sys
import json
import subprocess

config = {
    'wantdiff': True,
    'wantsfiles': True,
    'threadsafe': True
}

def run(context, change):
    if change['type'] == 'NEW_FILE' or change['type'] == 'FILE_CHANGED':
        language = context.get_derived_resource(change['file'], '.lang')

        path = os.path.join('extractors', language, 'extractor')
        if os.path.exists(path):
            extractor = path
        else:
            extractor = None

        if extractor:
            source_file = os.path.join(context.get_env('repo101dir'), change['file'])
            command = "{0} < \"{1}\"".format(extractor, source_file)

            output = subprocess.check_output(command, stderr=subprocess.STDOUT)

            context.write_derived_resource(change['file'], json.loads(output), '.extractor')

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
        lang = env.get_derived_resource('some-file.py', '.lang')
        os.path.join('extractors', lang, 'extractor')

        run(env, change)

        check_output.assert_called_with('extractors/Python/extractor < "/some/path/some-file.py"', stderr=-2)

def test():
    suite = unittest.TestLoader().loadTestsFromTestCase(RunTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
