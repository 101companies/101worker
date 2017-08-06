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
        'creates': [['dump', 'sentimentsPerContribution'],
                    ['dump', 'sentimentsPerLanguage']],
        'uses': [['resource', 'lang'],
                 ['resource', 'sentiment']]
    },
    'visualization': True
}


def run(env, res):
    data = env.read_dump('sentimentsPerLanguage')
    helpData = env.read_dump('sentimentsPerContribution')

    if data is None:
        data = {}
    if helpData is None:
        helpData = {}
    f = res['file']
    if f.startswith('contributions' + os.sep):
        folders = f.split(os.sep)
        contribution = folders[1]
        fileSentiment = env.get_derived_resource(f, 'sentiment')
		
        lang = env.get_derived_resource(f, 'lang')
        fileName = folders[-1]

        if helpData.get(lang, None) is None:
            helpData[lang] = {}
        if helpData[lang].get(contribution, None) is None:
            helpData[lang][contribution] = {}
        if res['type'] == "NEW_FILE" or res['type'] == "FILE_CHANGED":
            helpData[lang][contribution][fileName] = env.get_derived_resource(f, 'sentiment')
        else:
            del helpData[lang][contribution][fileName]

        if data.get(lang, None) is None:
            data[lang] = {}
        
        for c_lang in helpData:
            polarity = []
            subjectivity = []
            for c_name in helpData[c_lang]:
                for c_file in helpData[c_lang][c_name]:
                    if helpData[c_lang][c_name][c_file] != 'N/A':
                        f_sentiment = helpData[c_lang][c_name][c_file]
                        polarity.append(f_sentiment[0])
                        subjectivity.append(f_sentiment[1])
            if len(polarity) != 0:
                p_min = min(polarity)
                p_max = max(polarity)

                s_min = min(subjectivity)
                s_max = max(subjectivity)

                data[c_lang]['Min'] = (p_min, s_min)
                data[c_lang]['Max'] = (p_max, s_max)



    env.write_dump('sentimentsPerContribution', helpData)
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
