import os
import json

config = {
    'wantdiff': True,
    'wantsfiles': True,
    'threadsafe': True
}

# this is the actual logic of the module
def count_lines(source):
    return sum(1 for line in source)

def update_file(context, f):
    # reads the content of the file (primary resource)
    source = context.get_primary_resource(f)

    loc = count_lines(source)

    context.write_derived_resource(f, loc, '.loc')

def remove_file(context, f):
    context.remove_derived_resource(f, '.loc')

def run(context, change):
    # dispatch the modified file
    if change['type'] == 'NEW_FILE':
        update_file(context, change['file'])

    elif change['type'] == 'FILE_CHANGED':
        update_file(context, change['file'])

    else:
        remove_file(context, change['file'])

import unittest
from unittest.mock import Mock
import io

class SimpleLocTest(unittest.TestCase):

    def test_count_lines_three(self):
        three_lines = io.StringIO('''
        Test
        ''')

        self.assertEqual(count_lines(three_lines), 3)

    def test_count_zero_lines(self):
        zero_lines = io.StringIO('')

        self.assertEqual(count_lines(zero_lines), 0)

def test():
    suite = unittest.TestLoader().loadTestsFromTestCase(SimpleLocTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
