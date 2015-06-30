# -*- coding: utf-8 -*-


import json
import sys
sys.path.append('../../libraries/101meta')
sys.path.append('../../libraries')
from mediawiki101 import remove_headline_markup
import const101



def getWikiData(namespace, member):
    wiki = json.load(open(const101.wikiDump, 'r'))
    if namespace == '':
        namespace = None
    if member == '':
        member = 'Concept'

    for page in wiki['wiki']['pages']:
        if page.get('p', None) == namespace and page.get('n', None) == member:
            #return page
            url = 'http://101companies.org/wiki/'
            if namespace:
                url += namespace + ':' + member
            else:
                url += member

            headline = page.get('headline', '')

    #for page in wiki['pages']:
    #    if page['page'] == {}:
    #        continue
    #    if page['page']['page']['p'] == namespace and page['page']['page']['n'] == member:
    #        url = 'http://101companies.org/wiki/'
    #        if namespace: url += namespace + ':' + member
    #        else: url += member

    #        headline = page['page'].get('headline','')
            headline = remove_headline_markup(headline)
            return url, headline

    return None, None
