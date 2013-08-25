__author__ = 'martin'

import sys
import os
import json

sys.path.append('../101meta')
sys.path.append('..')
import const101
from mediawiki import remove_headline_markup

def extractHeadline(namespace, pagetitle):
    wikidata = json.load(open(const101.wikiDump, 'r'))
    target = {'p': namespace, 'n': pagetitle}
    for page in wikidata['wiki']['pages']:
        if target == page['page'].get('page', None):
            return remove_headline_markup(page['page']['headline'])


def constructWikiUrl():
    pass