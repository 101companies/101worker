import os
import json

dir = os.path.dirname(__file__)

with open(os.path.join(dir, 'config.json')) as f:
    config = json.load(f)

def run(context, change):
    f = change['file']

    lang = context.get_derived_resource(f, 'lang')
    if lang == 'Java':
        dump = context.read_dump('packageFrequency')
        if dump is None:
            dump = {}

        facts = context.get_derived_resource(f, 'extractor')

        for i in facts['imports']:
            if not i in dump:
                dump[i] = 1
            else:
                dump[i] += 1

        context.write_dump('packageFrequency', dump)

import unittest
from unittest.mock import Mock, patch

class PackageFrequencyTest(unittest.TestCase):

    def setUp(self):
        self.env = Mock()

        def get_derived_resource(f, ns):
            if ns == 'extractor':
                return { 'imports': ['java.util.List'] }
            else:
                return 'Java'

        self.env.get_derived_resource = get_derived_resource
        self.env.read_dump.return_value = None

    def test_run(self):
        run(self.env, { 'file': 'aa' })

        self.env.write_dump.assert_called_with('packageFrequency', { 'java.util.List': 1 })

def test():
    suite = unittest.TestLoader().loadTestsFromTestCase(PackageFrequencyTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
