import unittest

from . import mongo2Onto
import os
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

def test():
    pass
    # mongo2json.MongoClient = TestMongoClient
    #
    # import TAP
    # import TAP.Simple
    # import StringIO
    #
    # t = TAP.Simple
    # t.builder._plan = None
    #
    # t.plan(6)
    #
    # env = {}
    #
    # dumps101dir = '/some/test/dir'
    # env['dumps101dir'] = dumps101dir
    #
    # result = mongo2json.get_db()
    # t.eq_ok(result.name, 'wiki_production', 'chooses correct database')
    #
    # user = 'user'
    # password = 'password'
    # os.environ['MONGODB_USER'] = user
    # os.environ['MONGODB_PWD'] = password
    #
    # result = mongo2json.get_db()
    #
    # t.eq_ok(result.name, 'wiki_production', 'chooses correct collection')
    # t.eq_ok(result.user, user, 'uses given username')
    # t.eq_ok(result.password, password, 'uses given password')
    #
    #
    # db = mongo2json.get_db()
    # result = mongo2json.get_pages(db)
    # t.eq_ok(result, pages, 'lists all pages')
    #
    #
    # db = mongo2json.get_db()
    # result = mongo2json.get_output(env)
    # t.eq_ok(result, os.path.join(dumps101dir, 'pages.json'), 'uses correct output folder')
