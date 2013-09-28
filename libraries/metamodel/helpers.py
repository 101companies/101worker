__author__ = 'martin'

import sys
import json
import re
import os

sys.path.append('../101meta')
sys.path.append('..')
import const101
from mediawiki import remove_headline_markup
import urllib2


__opener = urllib2.build_opener()


def loadJSONFromUrl(url):
    def load(url):
        req = urllib2.Request(url)
        return json.load(__opener.open(req))

    # sometimes, the web request doesn't work, so use 2 tries for that
    try:
        return load(url)
    except urllib2.HTTPError:
        #second try
        try:
            return load(url)
        except urllib2.HTTPError:
            #third try - if this still fails, then something is really wrong
            return load(url)



def loadDerivativeNames(scope):
    m = {}
    if USE_EXPLORER_SERVICE:
        d = loadJSONFromUrl(os.path.join(const101.url101data, 'dumps', 'tempModuleSummaryDump.json'))
    else:
        d = json.load(open(const101.tModuleSummaryDump, 'r'))
    d = d[scope]
    for suffix in d.keys():
        target = d[suffix]
        if 'propertyName' in target:
            m[target['propertyName']] = target['className']

    return m


def extractHeadline(namespace, pagetitle):
    wikidata = json.load(open(const101.wikiDump, 'r'))
    target = {'p': namespace, 'n': pagetitle}
    for page in wikidata['wiki']['pages']:
        if target == page['page'].get('page', None):
            return remove_headline_markup(page['page']['headline'])


def isFileIdentifier(identifier):
    return re.match('.*\.[^/]*$', identifier)