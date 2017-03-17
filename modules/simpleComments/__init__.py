import os
import json
import unittest
from unittest.mock import Mock


config = {
    'wantdiff': True,
    'wantsfiles': True,
    'threadsafe': True,
    'behavior': {
        'creates': [['resource', 'comments']],
        'uses': [['resource', 'lang']]
    }
}

generic = ['//', '///']
generic_block_start = ['/*', '/**']
generic_block_end = ['*/']
generic_ignore = ['*']

haskell = ['--']
haskell_block_start = ['{-']
haskell_block_end = ['-}']

perl_ruby = ['#']
perl_ruby_block_start = ['=begin']
perl_ruby_block_end = ['=end', '=cut']

python = ['#']
python_block = ['\'\'\'', '\"\"\"']


def collect_comments(context, f):
    source = context.get_primary_resource(f)
    lang = context.get_derived_resource(f, 'lang')
    inline = []
    block_start = []
    block_end = []
    ignore = []
    if (lang == 'Python'):
        inline = python
        block_start = python_block
        block_end = python_block
    elif (lang == 'Perl' or lang == 'Ruby'):
        inline = perl_ruby
        block_start = perl_ruby_block_start
        block_end = perl_ruby_block_end
    elif (lang == 'Haskell'):
        inline = haskell
        block_start = haskell_block_start
        block_end = haskell_block_end
    else:
        inline = generic
        block_start = generic_block_start
        block_end = generic_block_end
        ignore = generic_ignore

    line_comment = False
    block_comment = False

    comments = ''
    for line in source.split('\n'):
        for word in line.split(' '):
            if (word in inline):
                line_comment = True
            elif (word in block_start):
                if (lang == 'Python' and block_comment is True):
                    block_comment = False
                else:
                    block_comment = True
            elif (word in block_end):
                block_comment = False

            if (line_comment or block_comment):
                if not (word in inline or word in block_start or
                        word in block_end or word in ignore):
                    comments += word + ' '

        line_comment = False

    return comments


def update_file(context, f):
    # reads the content of the file (primary resource)
    try:
        comments = collect_comments(context, f)
        context.write_derived_resource(f, comments, 'comments')
    except UnicodeDecodeError:
        context.write_derived_resource(f, '', 'comments')


def remove_file(context, f):
    context.remove_derived_resource(f, 'comments')


def run(context, change):
    # dispatch the modified file
    if change['type'] == 'NEW_FILE':
        update_file(context, change['file'])

    elif change['type'] == 'FILE_CHANGED':
        update_file(context, change['file'])

    else:
        remove_file(context, change['file'])


class extractCommentsTest(unittest.TestCase):

    def setUp(self):
        self.env = Mock()
        self.env.get_primary_resource.return_value = 'x = 5 // set x to 5\n/* set\ny to\n6 */\ny=6\nprint(x)\n'
        self.env.get_derived_resource.return_value = 'Java'

    def test_run_new(self):
        change = {
            'type': 'NEW_FILE',
            'file': 'some-file.java'
        }
        run(self.env, change)

        self.env.write_derived_resource.assert_called_with('some-file.java',
                                                           'set x to 5 set y to 6 ',
                                                           'comments')

    def test_run_changed(self):
        change = {
            'type': 'FILE_CHANGED',
            'file': 'some-file.java'
        }
        run(self.env, change)

        self.env.write_derived_resource.assert_called_with('some-file.java',
                                                           'set x to 5 set y to 6 ',
                                                           'comments')

    def test_run_removed(self):
        change = {
            'type': '',
            'file': 'some-file.java'
        }
        run(self.env, change)

        self.env.remove_derived_resource.assert_called_with('some-file.java', 'comments')


def test():
    suite = unittest.TestLoader().loadTestsFromTestCase(extractCommentsTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

