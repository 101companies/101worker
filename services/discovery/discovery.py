import os
from data101 import DumpdataProvider
from data101 import WikidataProvider
from data101 import TripledataProvider
from xml.sax.saxutils import escape
import sys
sys.path.append('../../libraries')
from mediawiki import wikifyNamespace
from mediawiki import dewikifyNamespace


base_uri = ''

def find(fragment, query, basePath=None):
    #recreate fragment path
    fragmentPath = os.path.join(fragment['classifier'], fragment['name'])
    if 'index' in fragment: fragmentPath = os.path.join(fragmentPath, str(fragment['index']))
    if basePath: fragmentPath = os.path.join(basePath, fragmentPath)

    #if we have found our fragment, return it
    if fragmentPath == query:
        return fragment, fragmentPath

    #otherwise, we need to search in the subfragments
    for f in fragment.get('fragments', []):
        x, y = find(f, query, fragmentPath)
        if x: return x, y

    return None, None

def mapFragment(filePath, fragmentPath, fragment):
    resource = os.path.join(base_uri, filePath, fragmentPath)
    #TODO I guess this is more of a hack instead of a true bugfix, so I guess it should be changed at some point
    if not fragmentPath.endswith(os.path.join(fragment['classifier'], fragment['name'])):
        resource = os.path.join(resource, fragment['classifier'], fragment['name'])

    mapped = {
        'resource'  : resource,
        'name'      : fragment['name'],
        'classifier': fragment['classifier']
    }

    if 'index' in fragment:
        mapped['index'] = fragment['index']
        mapped['resource'] = os.path.join(resource, str(fragment['index']))

    return mapped

def setWikidata(response, namespace, member):
    wikiUrl, headline = WikidataProvider.getWikiData(namespace,member)
    response['headline'] = headline
    response['wiki'] = wikiUrl

def setCommitInfos(response, filePath):
    #TODO update, just a rudimentary implementation
    response['commits'] = {'initiator' : None, 'contributors' : None}
    initiator, contributors = DumpdataProvider.getCommitInfo(filePath)
    if initiator:
        response['commits']['initiator'] = initiator['author']
    if contributors:
        response['commits']['contributors'] = []
        for contributor in contributors:
            if contributor['author'] not in response['commits']['contributors']:
                response['commits']['contributors'].append(contributor['author'])

def discoverFileFragment(namespace, member, path, file, fragment):
    filePath = os.path.join(namespace, member, path, file)
    #if no geshi code is defined, then we'll return basically "geshi : null"
    locator, extractor, geshi = DumpdataProvider.getMetadata(filePath)

    #name and classifier are set later (in the extractor phase
    response = {
        'geshi'    : geshi,
        'fragments': [],
        'github'   : DumpdataProvider.getGithub(namespace,member)
    }

    #update github data
    if response['github']:
        response['github'] = os.path.join(response['github'], path, file)

    #gather wiki data
    wikiNs = wikifyNamespace(namespace)
    setWikidata(response, wikiNs, member)

    #gather member data
    if extractor:
        extractedFacts = DumpdataProvider.getFacts(filePath, extractor)
        #TODO There has to be a better way to do this
        for f1 in extractedFacts['fragments']:
            selected, fragmentPath = find(f1, fragment)
            if selected:
                response['classifier'] = selected['classifier']
                response['name'] = selected['name']
                for f2 in selected.get('fragments',[]):
                    response['fragments'].append(mapFragment(filePath, fragmentPath, f2))
                break

    #gather content
    if locator:
        try:
            lines = DumpdataProvider.getFragment(filePath, fragment, locator)
            fragmentText = DumpdataProvider.read(filePath, range(lines['from'] - 1, lines['to']))
            response['content'] = escape(fragmentText)
            response['github'] += '#L{0}-{1}'.format(lines['from'], lines['to'])
        except:
            pass

    setCommitInfos(response, filePath)

    response['triples'] = TripledataProvider.getTriplesContaining(wikiNs, member)

    return response



def discoverMemberFile(namespace, member, path, file):
    filePath = os.path.join(namespace, member, path, file)
    #if no geshi code is defined, then we'll return basically "geshi : null" and nothing else
    locator, extractor, geshi = DumpdataProvider.getMetadata(filePath)

    response = {
        'geshi'     : geshi,
        'fragments' : [],
        'classifier': 'File',
        'name'      : file,
        'github'    : DumpdataProvider.getGithub(namespace,member)
    }

    #update github data
    if response['github']:
        response['github'] = os.path.join(response['github'], path, file)

    #gather wiki data
    wikiNs = wikifyNamespace(namespace)
    setWikidata(response, wikiNs, member)

    #gather member data - if there is a fact extractor, then we also want give back selectable fragments
    if extractor:
        extractedFacts = DumpdataProvider.getFacts(filePath, extractor)
        for fragment in extractedFacts.get('fragments', []):
            fragmentPath = os.path.join(fragment['classifier'], fragment['name'])
            response['fragments'].append( mapFragment(filePath, fragmentPath, fragment) )


    #gather content - if there is a geshi code, we should be able to get content
    if geshi:
        response['content'] = escape(DumpdataProvider.read(filePath))

    #commit infos
    setCommitInfos(response,filePath)

    #terms
    response['terms'] = DumpdataProvider.getTerms(filePath)

    response['triples'] = TripledataProvider.getTriplesContaining(wikiNs, member)

    return response

def discoverMemberPath(namespace, member, path):
    response = {
        'folders'   : [],
        'files'     : [],
        'classifier': 'Folder',
        'name'      : os.path.basename(path),
        'github'    : DumpdataProvider.getGithub(namespace, member)
    }

    #update github data
    if response['github']:
        response['github'] = os.path.join(response['github'], path)

    #gather wiki data
    wikiNS = wikifyNamespace(namespace)
    setWikidata(response, wikiNS, member)

    #gather member data
    dirPath = os.path.join(namespace, member, path)
    files, dirs = DumpdataProvider.getDirContent(dirPath)

    for d in dirs:
        response['folders'].append({
            'resource': os.path.join(base_uri, dirPath, d),
            'name'    : d
        })

    for f in files:
        response['files'].append({
            'resource': os.path.join(base_uri, dirPath, f),
            'name'    : f,
        })

    response['triples'] = TripledataProvider.getTriplesContaining(wikiNS, member)

    return response

def discoverNamespaceMember(namespace, member):
    response = {
        'folders'   : [],
        'files'     : [],
        'classifier': 'Member',
        'name'      : member,
        'github'    : DumpdataProvider.getGithub(namespace, member)
    }

    #gather wiki data
    wikiNS = wikifyNamespace(namespace)
    setWikidata(response, wikiNS, member)

    #gather member data
    dirPath = os.path.join(namespace, member.replace(' ','_'))
    files, dirs = DumpdataProvider.getDirContent(dirPath)

    for d in dirs:
        response['folders'].append({
            'resource': os.path.join(base_uri, dirPath, d),
            'name'    : d
        })

    for f in files:
        response['files'].append({
            'resource': os.path.join(base_uri, dirPath, f),
            'name'    : f,
            })

    response['triples'] = TripledataProvider.getTriplesContaining(wikiNS, member)

    return response

def discoverNamespace(namespace):
    response = {'classifier': 'Namespace', 'name': namespace, 'members': [], 'github': DumpdataProvider.getGithub(namespace, '')}

    #gather wiki data
    wikiNS = wikifyNamespace(namespace)
    setWikidata(response,'Namespace', wikiNS)

    #gather member data
    members = DumpdataProvider.getMembers(namespace)
    for member in members:
        response['members'].append({
            'resource': os.path.join(base_uri, namespace, member),
            'name'    : member
        })

    response['triples'] = TripledataProvider.getTriplesContaining('Namespace', wikiNS)

    return response

def discoverAllNamespaces():
    response = {'classifier': 'Namespace', 'name': 'Namespace', 'members': [], 'github': DumpdataProvider.getGithub('', '')}

    #gather wiki data
    setWikidata(response,'Namespace','Namespace')

    #gather member data
    members = DumpdataProvider.getMembers('')
    for member in members:
        response['members'].append({
            'resource': os.path.join(base_uri, dewikifyNamespace(member)),
            'name'    : member
        })

    response['triples'] = TripledataProvider.getTriplesContaining('Namespace','Namespace')

    return response

