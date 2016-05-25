from collections import Counter

config = {
    'wantdiff': False,
    'wantsfiles': False,
    'threadsafe': False,
    'behavior': {
        'uses': [['dump', 'wiki']],
        'creates': [['dump', 'languageFrequency']]
    }
}

def run(env):
    wiki_dump = env.read_dump('wiki')

    pages = wiki_dump['wiki']['pages']

    contributions = filter(lambda p: 'Contribution' == p.get('p', ''), pages)

    uses = [p.get('Uses', []) for p in contributions]
    uses = [p for use in uses for p in use]

    uses = list(filter(lambda u: u['p'] == 'Language', uses))

    uses = [use['n'].replace('_', ' ') for use in uses]

    lcounts = dict(Counter(uses))

    env.write_dump('languageFrequency', lcounts)


import unittest
from unittest.mock import Mock, patch

class LanguageFrequencyTest(unittest.TestCase):

    def setUp(self):
        self.env = Mock()
        self.env.read_dump.return_value = {
            'wiki': {
                'pages': [
                    {
                        'p': 'Contribution',
                        'Uses': [
                            { 'p': 'Language', 'n': 'Python' }
                        ]
                    }
                ]
            }
        }

    def test_run(self):
        run(self.env)

        self.env.write_dump.assert_called_with('languageFrequency', { 'Python': 1 })

def test():
    suite = unittest.TestLoader().loadTestsFromTestCase(LanguageFrequencyTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
