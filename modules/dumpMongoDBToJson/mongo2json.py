#!/usr/bin/env python
# coding=utf-8

from pymongo import MongoClient
import json
import os
from bson.json_util import dumps

config = {
    'wantdiff': False,
    'wantsfiles': False,
    'threadsafe': True
}

def get_db():
    client = MongoClient('localhost', 27017)
    db = client['wiki_development']

    MONGODB_USER = os.environ['MONGODB_USER']
    MONGODB_PWD = os.environ['MONGODB_PWD']

    if MONGODB_USER and MONGODB_PWD:
        db.authenticate(MONGODB_USER, MONGODB_PWD)

    return db

def get_pages(db):
    return list(db.pages.find())

def get_output(context):
    return os.path.join(context.get_env('dumps101dir'), 'pages.json')

def run(context):
    db = get_db()
    output = get_output(context)
    allPages = get_pages(db)
    with open(output, 'w') as f:
        f.write(dumps({'pageCount': len(allPages), 'pages': allPages}))

if __name__ == '__main__':
    main()
