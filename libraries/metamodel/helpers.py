__author__ = 'martin'

import sys
import json
import re

sys.path.append('../101meta')
sys.path.append('..')
import const101
from mediawiki import remove_headline_markup
import urllib2


def loadDerivativeNames(scope):
    m = {}
    d = json.load(open(const101.tModuleSummaryDump, 'r'))
    d = d[scope]
    for suffix in d.keys():
        target = d[suffix]
        if 'propertyName' in target:
            m[target['propertyName']] = target['className']

    return m


def loadJSONFromUrl(url):
    req = urllib2.Request(url)
    opened = urllib2.build_opener().open(req)
    return json.load(opened)


def extractHeadline(namespace, pagetitle):
    wikidata = json.load(open(const101.wikiDump, 'r'))
    target = {'p': namespace, 'n': pagetitle}
    for page in wikidata['wiki']['pages']:
        if target == page['page'].get('page', None):
            return remove_headline_markup(page['page']['headline'])


def isFileIdentifier(identifier):
    return re.match('.*\.[^/]*$', identifier)