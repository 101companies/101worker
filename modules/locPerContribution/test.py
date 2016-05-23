from .program import run

import unittest
from unittest.mock import Mock, patch

class LocPerContributionTest(unittest.TestCase):

    def setUp(self):
        self.env = Mock()
        self.env.read_dump.return_value = { 'python': 45 }
        self.env.get_derived_resource.return_value = 10

    def test_run(self):
        res = {
            'file': 'contributions/python/some-file.py'
        }
        run(self.env, res)

        self.env.write_dump.assert_called_with('locPerContribution', { 'python': 55 })

    def test_new_contribution(self):
        res = {
            'file': 'contributions/ruby/some-file.rb'
        }
        run(self.env, res)
        self.env.write_dump.assert_called_with('locPerContribution', { 'python': 45, 'ruby': 10 })

    def test_run_no_contribution(self):
        res = {
            'file': 'something/python/some-file.py'
        }
        run(self.env, res)

        self.env.write_dump.assert_called_with('locPerContribution', { 'python': 45 })

def test():
    suite = unittest.TestLoader().loadTestsFromTestCase(LocPerContributionTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
