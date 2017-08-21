import os
import statistics
import unittest
from unittest.mock import Mock, patch
from .visualization import visualize

config = {
    'wantdiff': True,
    'wantsfiles': True,
    'threadsafe': False,
    'behavior': {
        'creates': [['dump', 'sentimentsPerContribution']],
        'uses': [['resource', 'lang'],
                 ['resource', 'sentiment']]
    },
    'visualization': True
}


def run(env, res):
    data = env.read_dump('sentimentsPerLanguage')
    testRange = {'Python', 'Haskell', 'Java', 'XML', 'SQL'}
    if data is None:
        data = {}
    f = res['file']
    if f.startswith('contributions' + os.sep):
        folders = f.split(os.sep)
        fileSentiment = env.get_derived_resource(f, 'sentiment')
		
        lang = env.get_derived_resource(f, 'lang')

        if (lang in testRange) & (fileSentiment[0] != 0.0):
            if data.get(lang, None) is None:
                data[lang] = {}
            if (data[lang].get('Min', None) is None):
                data[lang]['Min'] = 0.0
            if (data[lang]['Min'] > fileSentiment[0]):
                data[lang]['Min'] = fileSentiment[0]
            if (data[lang].get('Max', None) is None):
                data[lang]['Max'] = 0.0
            if (data[lang]['Max'] < fileSentiment[0]):
                data[lang]['Max'] = fileSentiment[0]
            if data[lang].get('Average', None) is None:
                data[lang]['Average'] = (fileSentiment[0],1)
            else:
                data[lang]['Average'] = (((data[lang]['Average'][0] + fileSentiment[0])/2.0),(data[lang]['Average'][1] + 1))

    env.write_dump('sentimentsPerLanguage', data)
        
class CommentSentimentPerLanguageTest(unittest.TestCase):

    def setUp(self):
        self.env = Mock()
        
        def side_effect(name):
            if name == 'LangPerContribution':
                return {'haskell':{'Main Language': 'Haskell'}, 'java':{'Main Language': 'Java'}}
            elif name == 'sentimentsPerContribution':
                return {'Java':{'stupidJava':{'Main.java':[-0.9, 0.5]}}}
            elif name == 'sentimentsPerLanguage':
                return {'Java': {'Min':(-0.9, 0.5),
                                                 'Max':(-0.9, 0.5),
                                                 'Median':(-0.9, 0.5),
                                                 'Mean':(-0.9, 0.5),}}
            
        self.env.read_dump.side_effect = side_effect
        self.env.get_derived_resource.return_value=[0.7, 0.5]
    
    def test_run(self):
        res = {
            'file': 'contributions' + os.sep + 'java' + os.sep + 'EvenWorseJava.java',
            'type': 'NEW_FILE'
        }
        run(self.env, res)
        self.env.write_dump.assert_called_with('sentimentsPerLanguage', {'Java': {'Min': (-0.9, 0.5),
                                                                                          'Max': (0.7, 0.5),
                                                                                          'Median': (statistics.median([-0.9, 0.7]), 0.5),
                                                                                          'Mean': (statistics.median([-0.9, 0.7]), 0.5)}})
        
    def test_new_Contribution(self):
        res = {
            'file': 'contributions' + os.sep + 'haskell' + os.sep + 'haskell.hs',
            'type': 'NEW_FILE'
        }
        run(self.env, res)
        self.env.write_dump.assert_called_with('sentimentsPerLanguage', {'Java': {'Min': (-0.9, 0.5),
                                                                                          'Max': (-0.9, 0.5),
                                                                                          'Median': (-0.9, 0.5),
                                                                                          'Mean': (-0.9, 0.5)},
                                                                                 'Haskell': {'Min': (0.7, 0.5),
                                                                                             'Max': (0.7, 0.5),
                                                                                             'Median': (0.7, 0.5),
                                                                                             'Mean': (0.7, 0.5)}})  
        
    def test_no_Contribution(self):
        res = {
                'file': 'something' + os.sep + 'haskellIsGreat' + os.sep + 'really.hs',
                'type': 'NEW_FILE'
            }
        run(self.env, res)
        self.env.write_dump.assert_called_with('sentimentsPerLanguage', {'Java': {'Min': (-0.9, 0.5),
                                                                                          'Max': (-0.9, 0.5),
                                                                                          'Median': (-0.9, 0.5),
                                                                                          'Mean': (-0.9, 0.5)}})
        
def test():
    suite = unittest.TestLoader().loadTestsFromTestCase(CommentSentimentPerLanguageTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
