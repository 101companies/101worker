import os
import json
import unittest
from unittest.mock import Mock
from textblob import TextBlob


config = {
    'wantdiff': True,
    'wantsfiles': True,
    'threadsafe': True,
    'behavior': {
        'creates': [['resource', 'sentiment']],
        'uses': [['resource', 'comments']]
    }
}


def calc_sentiment(context, f):
    comments = context.get_derived_resource(f, 'comments')
    comments_blob = TextBlob(comments)
    comment_sentiment = comments_blob.sentiment
    if (comments == ''):
        return 'N/A'
    else:
        return comment_sentiment


def update_file(context, f):
    # reads the content of the file (primary resource)
    try:
        sentiment = calc_sentiment(context, f)
        context.write_derived_resource(f, sentiment, 'sentiment')
    except UnicodeDecodeError:
        context.write_derived_resource(f, 0, 'sentiment')


def remove_file(context, f):
    context.remove_derived_resource(f, 'sentiment')


def run(context, change):
    # dispatch the modified file
    if change['type'] == 'NEW_FILE':
        update_file(context, change['file'])

    elif change['type'] == 'FILE_CHANGED':
        update_file(context, change['file'])

    else:
        remove_file(context, change['file'])


class simpleSentimentsTest(unittest.TestCase):

    def setUp(self):
        self.env = Mock()
        self.env.get_derived_resource.return_value = 'set x to 5 set y to 6 '

    def test_run_new(self):
        change = {
            'type': 'NEW_FILE',
            'file': 'some-file.java'
        }
        run(self.env, change)

        self.env.write_derived_resource.assert_called_with('some-file.java',
                                                           (0.0, 0.0),
                                                           'sentiment')

    def test_run_changed(self):
        change = {
            'type': 'FILE_CHANGED',
            'file': 'some-file.java'
        }
        run(self.env, change)

        self.env.write_derived_resource.assert_called_with('some-file.java',
                                                           (0.0, 0.0),
                                                           'sentiment')

    def test_run_removed(self):
        change = {
            'type': '',
            'file': 'some-file.java'
        }
        run(self.env, change)

        self.env.remove_derived_resource.assert_called_with('some-file.java', 'sentiment')


def test():
    suite = unittest.TestLoader().loadTestsFromTestCase(simpleSentimentsTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
