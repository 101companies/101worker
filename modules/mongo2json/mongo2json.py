#!/usr/bin/env python
# coding=utf-8

from pymongo import MongoClient
import json
import os

def get_db():
    client = MongoClient('localhost', 27017)
    db = client['wiki_production']

    MONGODB_USER = os.environ['MONGODB_USER']
    MONGODB_PWD = os.environ['MONGODB_PWD']

    if MONGODB_USER and MONGODB_PWD:
        db.authenticate(MONGODB_USER, MONGODB_PWD)

    return db

def get_pages(db):
    return list(db.pages.find())

def get_output():
    return os.environ['dumps101dir'] + '/pages.json'

def main():
    db = get_db()
    output = get_output()
    allPages = get_pages(db)
    with open(output, 'w') as f:
        f.write(json.dumps({'pageCount': len(allPages), 'pages': allPages}, sort_keys=True, indent=4))

if __name__ == '__main__':
    main()
