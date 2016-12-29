#!/usr/bin/env python3
# coding=utf-8

import sys
import json
import os

from datetime import datetime

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    raise TypeError ("Type not serializable")

try:
    import psycopg2
    import psycopg2.extras
except ImportError:
    print('psycopg2 is missing: "pip3 install psycopg2"')
    sys.exit(1)


def get_db():
    conn = psycopg2.connect("dbname=wiki_development user=postgres password=root110120 host=localhost")
    return conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

def get_pages(db):
    db.execute('select * from pages')
    return db.fetchall()

def get_output(context):
    return os.path.join(context.get_env('dumps101dir'), 'raw-wiki.json')

def run(context):
    db = get_db()
    output = get_output(context)
    allPages = get_pages(db)
    with open(output, 'w') as f:
        f.write(json.dumps({'pageCount': len(allPages), 'pages': allPages}, indent=4, default=json_serial))

if __name__ == '__main__':
    main()
