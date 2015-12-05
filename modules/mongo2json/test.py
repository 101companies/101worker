import unittest

import mongo2json
import os
from mock import Mock, MagicMock, patch
import io
import json

pages = [
{
    "headline": "A contribution to the 101project",
    "instanceOf": [
        {
            "n": "101",
            "p": "Namespace"
        }
    ],
    "internal_links": [
        "101project",
        "101contribution",
        "Implementation",
        "Model",
        "101system",
        "101contributor",
        "101project",
        "RelatesTo::@contributor",
        "InstanceOf::Namespace:101"
    ],
    "mentions": [
        {
            "n": "101project",
            "p": None
        },
        {
            "n": "101contribution",
            "p": None
        },
        {
            "n": "Implementation",
            "p": None
        },
        {
            "n": "Model",
            "p": None
        },
        {
            "n": "101system",
            "p": None
        },
        {
            "n": "101contributor",
            "p": None
        },
        {
            "n": "101project",
            "p": None
        }
    ],
    "n": "@contribution",
    "p": "101",
    "relatesTo": [
        {
            "n": "@contributor",
            "p": None
        }
    ],
    "subresources": {}
    }
]

class TestCollection(object):

    def __init__(self, data=[]):
        self.data = data

    def find(self):
        for item in self.data:
            yield item

class TestDatabase(object):

    def __init__(self, name):
        self.name = name
        self.user = None
        self.password = None

    def authenticate(self, user, password):
        self.user = user
        self.password = password

    @property
    def pages(self):
        return TestCollection(data=pages)

class TestMongoClient(object):

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def __getitem__(self, index):
        return TestDatabase(index)

mongo2json.MongoClient = TestMongoClient

class Mongo2JSONTestCase(unittest.TestCase):
    def setUp(self):
        self.dumps101dir = '/some/test/dir'
        os.environ['dumps101dir'] = self.dumps101dir

    def tearDown(self):
        os.environ['MONGODB_USER'] = ''
        os.environ['MONGODB_PWD'] = ''
        os.environ['dumps101dir'] = ''

    def test_get_db(self):
        result = mongo2json.get_db()
        self.assertEqual(result.name, 'wiki_production')

    def test_get_db_auth(self):
        user = 'user'
        password = 'password'
        os.environ['MONGODB_USER'] = user
        os.environ['MONGODB_PWD'] = password

        result = mongo2json.get_db()

        self.assertEqual(result.name, 'wiki_production')
        self.assertEqual(result.user, user)
        self.assertEqual(result.password, password)

    def test_get_pages(self):
        db = mongo2json.get_db()

        result = mongo2json.get_pages(db)

        self.assertEqual(result, pages)

    def test_get_output(self):
        db = mongo2json.get_db()

        result = mongo2json.get_output()

        self.assertEqual(result, self.dumps101dir + '/pages.json')

    def test_main(self):
        with patch('mongo2json.open', create=True) as mock_open:
            mock_open.return_value = MagicMock(spec=file)

            mongo2json.main()

            file_handle = mock_open.return_value.__enter__.return_value

            result = file_handle.write.call_args[0][0]
            result = json.loads(result)
            self.assertEqual(result['pageCount'], len(pages))
