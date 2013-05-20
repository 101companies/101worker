# -*- coding: utf-8 -*-


import json
import sys
sys.path.append('../../libraries/101meta')
sys.path.append('../../libraries')
from mediawiki import remove_headline_markup
import const101



def getWikiData(namespace, member):
    wiki = json.load(open(const101.wikiDump, 'r'))['wiki']
    if namespace == '' or namespace == '101':
        namespace = None
    if member == '':
        member = 'Concept'

    for page in wiki['pages']:
        if page['page']['page']['p'] == namespace and page['page']['page']['n'] == member:
            url = 'http://101companies.org/wiki/'
            if namespace: url += namespace + ':' + member
            else: url += member

            headline = page['page'].get('headline','')
            headline = remove_headline_markup(headline)
            return url, headline

    return None, None