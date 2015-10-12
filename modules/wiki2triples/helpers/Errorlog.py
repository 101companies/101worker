#! /usr/bin/env python

import json

__author__ = 'Martin Leinberger'

__log = {}


def reportError(page, errorMsg):
    if not page['p']: page['p'] = 'Concept'
    key = page['p'] + ':' + page['n']
    __log.setdefault(key, []).append(errorMsg)


def serializeLog(path):
    json.dump(__log, open(path, 'w'), indent=4)