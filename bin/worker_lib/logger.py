from pymongo import MongoClient
import os
import datetime

client = MongoClient('localhost', 27017)
db = client['worker']

MONGODB_USER = os.environ.get('MONGODB_USER', '')
MONGODB_PWD = os.environ.get('MONGODB_PWD', '')

if MONGODB_USER and MONGODB_PWD:
    db.authenticate(MONGODB_USER, MONGODB_PWD)

def report_error(error_type, error_data):
    '''
    Logs an error to an internal dump.
    :param error_type: error name
    :param error_data: data for the error, e.g. stack trace
    '''

    print error_type
    print error_data

    db.errors.insert_one({
        'error': error_type,
        'data': error_data,
        'created_at': datetime.datetime.now()
    })
