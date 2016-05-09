import os
import json

config = {
    'wantdiff': False,
    'wantsfiles': True,
    'threadsafe': False
}

def run(env, change):
    data = env.read_dump('locPerContribution')

    if data is None:
        data = {}

    f = change['file']
    if f.startswith('contributions/'):
        contribution = f.split('/')[1]

        if data.get(contribution, None) is None:
            data[contribution] = 0

        data[contribution] += env.get_derived_resource(f, '.loc')

    env.write_dump('locPerContribution', data)

import unittest
from unittest.mock import Mock, patch

class LocPerContributionTest(unittest.TestCase):

    def test_run(self):
        change = {
            'file': 'contributions/python/some-file.py'
        }
        env = Mock()
        env.read_dump.return_value = { 'python': 45 }
        env.get_derived_resource.return_value = 10

        run(env, change)

        env.write_dump.assert_called_with('locPerContribution', { 'python': 55 })

    def test_run_no_contribution(self):
        change = {
            'file': 'something/python/some-file.py'
        }
        env = Mock()
        env.read_dump.return_value = { 'python': 45 }
        env.get_derived_resource.return_value = 10

        run(env, change)

        env.write_dump.assert_called_with('locPerContribution', { 'python': 45 })

def test():
    suite = unittest.TestLoader().loadTestsFromTestCase(LocPerContributionTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
