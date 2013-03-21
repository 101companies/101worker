import json
import sys
sys.path.append('../../libraries/101meta')
import const101

def dewikifyNamespace(namespace):
    values = {
        'Contribution': 'contributions',
        'Contributor' : 'contributors',
        'Concept'     : 'concepts',
        'Technology'  : 'technologies',
        'Language'    : 'languages',
        'Theme'       : 'themes',
        'Vocabulary'  : 'vocabularies'
    }
    return values.get(namespace,'')

def wikifyNamespace(namespace):
    values = {
        'contributions': 'Contribution',
        'contributors' : 'Contributor',
        'concepts'     : None,
        'technologies' : 'Technology',
        'languages'    : 'Language',
        'themes'       : 'Theme',
        'vocabularies' : 'Vocabulary',
        'Namespace'    : 'Namespace'
    }
    return values[namespace]

def getWikiData(namespace, member):
    wiki = json.load(open(const101.wikiDump, 'r'))['wiki']

    for page in wiki['pages']:
        if page['page']['page']['p'] == namespace and page['page']['page']['n'] == member:
            url = 'http://101companies.org/wiki/'
            if namespace: url += namespace + ':' + member
            else: url += member

            headline = page['page'].get('headline','')
            headline = headline.replace('== Headline ==','').replace('\n','').replace('[[','').replace(']]','')
            return url, headline
    return None, None