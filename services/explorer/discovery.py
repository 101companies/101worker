# -*- coding: utf-8 -*-


import os
import sys
import json

os.chdir(os.path.dirname(__file__))

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../libraries')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../libraries/101meta')))
from mediawiki import wikifyNamespace
from mediawiki import dewikifyNamespace
from data101 import DumpdataProvider
from data101 import WikidataProvider
from data101 import TripledataProvider


class DiscoveryException(Exception):
    def __init__(self, status, msg):
        self._status = status
        self._msg = msg

    @property
    def ErrorMessage(self):
        return self._msg

    @property
    def Status(self):
        return self._status

    def __str__(self):
        return str(self.Status) + '\n\n' + self.ErrorMessage


class ResourceNotFoundException(DiscoveryException):
    def __init__(self):
        DiscoveryException.__init__(self, '404 Not found', 'Requested resource not found')

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
    initiator, contributors = DumpdataProvider.getCommitInfo(filePath)
    if initiator:
        response['people'] = []
        response['people'].append({'name' : initiator['author'], 'role' : 'Initiator?'})
    if contributors:
        contribList = []
        for contributor in contributors:
            if contributor['author'] not in contribList and not contributor['author'] == initiator['author']:
                contribList.append(contributor['author'])

        for c in contribList:
            response['people'].append({'name' : c, 'role' : None})


def discoverFileFragment(namespace, member, path, file, fragment):
    filePath = os.path.join(namespace, member, path, file)
    if not DumpdataProvider.exists(filePath):
        raise ResourceNotFoundException()

    #remove tailing slash, if there is one
    if fragment.endswith('/'):
        fragment = fragment[:-1]

    #if no geshi code is defined, then we'll return basically "geshi : null"
    locator, extractor, geshi, language = DumpdataProvider.getMetadata(filePath)

    #name and classifier are set later (in the extractor phase
    response = {
        'geshi'    : geshi,
        'fragments': [],
        'github'   : DumpdataProvider.getGithub(namespace,member)
    }

    if language:
        response['language'] = language

    #update github data
    if response['github']:
        response['github'] = os.path.join(response['github'], path, file)

    #gather wiki data
    wikiNS = wikifyNamespace(namespace)
    setWikidata(response, wikiNS, member)

    response['namespace'] = wikiNS

    #gather member data
    lineNumbers = None
    if extractor:
        #try:
        extractedFacts = DumpdataProvider.getFacts(filePath, extractor)
        #TODO There has to be a better way to do this
        for f1 in extractedFacts['fragments']:
            selected, fragmentPath = find(f1, fragment)
            if selected:
                response['classifier'] = selected['classifier']
                response['name'] = selected['name']
                if 'startLine' in selected:
                    raise Exception(json.dumps(selected, indent=4))
                    lineNumbers = {'from':selected['startLine'], 'to':selected['endLine']}
                for f2 in selected.get('fragments',[]):
                    response['fragments'].append(mapFragment(filePath, fragmentPath, f2))
                break
        #except:
        #    pass

    #gather content
    if lineNumbers or locator:
        if not lineNumbers:
            lineNumbers = DumpdataProvider.getFragment(filePath, fragment, locator)

        fragmentText = DumpdataProvider.read(filePath, range(lineNumbers['from'] - 1, lineNumbers['to']))
        response['content'] = fragmentText
        response['github'] += '#L{0}-{1}'.format(lineNumbers['from'], lineNumbers['to'])
    #except Exception as e:
        #    raise DiscoveryException('500 Internal Server Error', 'Fragment location failed:\n' + str(e))

    setCommitInfos(response, filePath)

    response['endpoint'] = TripledataProvider.getEndpointLink(wikiNS, member)
    response['sesame']   = TripledataProvider.getSesameLink(namespace, member)

    return response


def discoverMemberFile(namespace, member, path, file):
    filePath = os.path.join(namespace, member, path, file)
    if not DumpdataProvider.exists(filePath):
        raise ResourceNotFoundException()

    #if no geshi code is defined, then we'll return basically "geshi : null" and nothing else
    locator, extractor, geshi, language = DumpdataProvider.getMetadata(filePath)

    response = {
        'geshi'     : geshi,
        'fragments' : [],
        'classifier': 'File',
        'name'      : file,
        'github'    : DumpdataProvider.getGithub(namespace,member)
    }

    if language:
        response['language'] = language

    #update github data
    if response['github']:
        response['github'] = os.path.join(response['github'], path, file)

    #gather wiki data
    wikiNS = wikifyNamespace(namespace)
    setWikidata(response, wikiNS, member)

    response['namespace'] = wikiNS

    #gather member data - if there is a fact extractor, then we also want give back selectable fragments
    if extractor:
        try:
            extractedFacts = DumpdataProvider.getFacts(filePath, extractor)
            for fragment in extractedFacts.get('fragments', []):
                fragmentPath = os.path.join(fragment['classifier'], fragment['name'])
                response['fragments'].append( mapFragment(filePath, fragmentPath, fragment) )
        except:
            pass


    #gather content - if there is a geshi code, we should be able to get content
    if geshi:
        response['content'] = DumpdataProvider.read(filePath)

    #commit infos
    setCommitInfos(response,filePath)

    response['endpoint'] = TripledataProvider.getEndpointLink(wikiNS, member)
    response['sesame']   = TripledataProvider.getSesameLink(namespace, member)

    response['derived'] = DumpdataProvider.getDerivedFiles(filePath)

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

    response['namespace'] = wikiNS

    #gather member data
    dirPath = os.path.join(namespace, member, path)
    files, dirs = DumpdataProvider.getDirContent(dirPath)

    for d in dirs:
        response['folders'].append({
            'resource': os.path.join(base_uri, dirPath, d),
            'classifier': 'Folder',
            'name'    : d
        })

    for f in files:
        response['files'].append({
            'resource': os.path.join(base_uri, dirPath, f),
            'classifier': 'File',
            'name'    : f,
        })

    response['endpoint'] = TripledataProvider.getEndpointLink(wikiNS, member)
    response['sesame']   = TripledataProvider.getSesameLink(namespace, member)

    return response


def discoverNamespaceMember(namespace, member):
    if not member.decode('utf_8') in DumpdataProvider.getMembers(namespace):
        raise ResourceNotFoundException()

    response = {
        'folders'   : [],
        'files'     : [],
        'classifier': 'Namespace member',
        'name'      : member,
        'github'    : DumpdataProvider.getGithub(namespace, member)
    }

    #gather wiki data
    wikiNS = wikifyNamespace(namespace)
    setWikidata(response, wikiNS, member)

    response['namespace'] = wikiNS

    #gather member data
    dirPath = os.path.join(namespace, member.replace(' ','_'))
    files, dirs = DumpdataProvider.getDirContent(dirPath)

    for d in dirs:
        response['folders'].append({
            'resource'  : os.path.join(base_uri, dirPath, d),
            'classifier': 'Folder',
            'name'      : d
        })

    for f in files:
        response['files'].append({
            'resource'  : os.path.join(base_uri, dirPath, f),
            'classifier': 'File',
            'name'      : f
            })

    response['endpoint'] = TripledataProvider.getEndpointLink(wikiNS, member)
    response['sesame']   = TripledataProvider.getSesameLink(namespace, member)

    if namespace == 'modules':
        response['module'] = DumpdataProvider.getModuleDescription(member)

    return response


def discoverNamespace(namespace):
    if not wikifyNamespace(namespace) in DumpdataProvider.getMembers('') and not wikifyNamespace(namespace) == '':
        raise ResourceNotFoundException()

    response = {'classifier': 'Namespace', 'name': namespace, 'members': []}#, 'github': DumpdataProvider.getGithub(namespace, '')}

    #gather wiki data
    wikiNS = wikifyNamespace(namespace)
    setWikidata(response,'Namespace', wikiNS)

    response['namespace'] = 'Namespace'

    #gather member data
    members = DumpdataProvider.getMembers(namespace)
    for member in members:
        response['members'].append({
            'resource': os.path.join(base_uri, namespace, member).replace(' ', '_'),
            'classifier': 'Namespace member',
            'name'    : member
        })

    response['endpoint'] = TripledataProvider.getEndpointLink('Namespace', wikiNS)
    response['sesame']   = TripledataProvider.getSesameLink('namespaces', wikiNS)

    return response


def discoverAllNamespaces():
    response = {'classifier': 'Namespace', 'name': 'Namespace', 'members': []}#, 'github': DumpdataProvider.getGithub('', '')}

    #gather wiki data
    setWikidata(response,'Namespace','Namespace')

    response['namespace'] = 'Namespace'

    #gather member data
    members = DumpdataProvider.getMembers('')
    for member in members:
        response['members'].append({
            'resource'  : os.path.join(base_uri, dewikifyNamespace(member)).replace(' ', '_'),
            'classifier': 'Namespace',
            'name'      : member
        })

    response['endpoint'] = TripledataProvider.getEndpointLink('Namespace', 'Namespace')
    response['sesame']   = TripledataProvider.getSesameLink('namespaces', 'Namespace')

    return response


def createRedirectUrl(wikititle):
    if not ':' in wikititle:
        if '@' in wikititle:
            ns = '101'
        else:
            ns = 'concepts'
        member = wikititle
    else:
        parts = wikititle.split(':')
        if not parts[0] == 'Namespace':
            ns = dewikifyNamespace(parts[0])
            member = parts[1]
        else:
            ns = ''
            member = dewikifyNamespace(parts[1])

    return os.path.join(base_uri, ns, member)

