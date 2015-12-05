import unittest
from mock import Mock, MagicMock, patch
import os

import wiki2json

class Wiki2JSONTestCase(unittest.TestCase):
    def setUp(self):
        self.dumps101dir = '/some/test/dir'
        os.environ['dumps101dir'] = self.dumps101dir

    def tearDown(self):
        os.environ['dumps101dir'] = ''

    def test_extract_properties(self):
        properties = [
            "101project",
            "101contribution",
            "Implementation",
            "Model",
            "101system",
            "101contributor",
            "101project",
            "http://google.de",
            "~SomethingNotMentioned",
            "RelatesTo::@contributor",
            "InstanceOf::Namespace:101"
        ]

        result = wiki2json.extract_properties(properties)

        self.assertEqual(len(result['InstanceOf']), 1)
        self.assertEqual(result['InstanceOf'][0]['n'], '101')
        self.assertEqual(result['InstanceOf'][0]['p'], 'Namespace')

        self.assertEqual(len(result['mentions']), 8)
        self.assertTrue('http://google.de' in result['mentions'])

        self.assertEqual(len(result['mentionsNot']), 1)
        self.assertEqual(result['mentionsNot'][0]['n'], 'SomethingNotMentioned')
