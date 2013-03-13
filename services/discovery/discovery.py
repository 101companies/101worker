import os
from data101 import DataProvider

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

def discoverFileFragment(namespace, member, path, file, fragment):
    filePath = os.path.join(namespace, member, path, file)

    #if no geshi code is defined, then we'll return basically "geshi : null"
    locator, extractor, geshi = DataProvider.getMetadata(filePath)
    response = { 'geshi' : geshi }

    github, headline, wiki = DataProvider.getResolutionData(namespace, member)
    github = os.path.join(github, path, file)
    response['github'] = github
    response['headline'] = headline
    response['wiki'] = wiki

    if locator:
        lines = DataProvider.getFragment(filePath, fragment, locator)
        fragmentText = DataProvider.read(filePath, range(lines['from'] - 1, lines['to']))
        response['content'] = fragmentText
        response['github'] += '#L{0}-{1}'.format(lines['from'], lines['to'])

    if extractor:
        extractedFacts = DataProvider.getFacts(filePath, extractor)
        #TODO There has to be a better way to do this
        for f1 in extractedFacts['fragments']:
            selected, fragmentPath = find(f1, fragment)
            if selected:
                response['classifier'] = selected['classifier']
                response['name'] = selected['name']
                response['fragments'] = []
                for f2 in selected.get('fragments',[]):
                    response['fragments'].append(mapFragment(filePath, fragmentPath, f2))
                break

    return response



def discoverMemberFile(namespace, member, path, file):
    filePath = os.path.join(namespace, member, path, file)

    #if no geshi code is defined, then we'll return basically "geshi : null" and nothing else
    locator, extractor, geshi = DataProvider.getMetadata(filePath)
    response = { 'geshi' : geshi, 'classifier': 'File', 'name':file}

    #if there is a geshi code, we should be able to get content
    if geshi:
        response['content'] = DataProvider.read(filePath)

    github, headline, wiki = DataProvider.getResolutionData(namespace, member)
    github = os.path.join(github, path, file)

    response['github'] = github
    response['headline'] = headline
    response['wiki'] = wiki

    #if there is a fact extractor, then we also want give back selectable fragments
    if extractor:
        extractedFacts = DataProvider.getFacts(filePath, extractor)
        fragments = []
        for fragment in extractedFacts.get('fragments', []):
            fragmentPath = os.path.join(fragment['classifier'], fragment['name'])
            fragments.append( mapFragment(filePath, fragmentPath, fragment) )

        response['fragments'] = fragments


    return response

def discoverMemberPath(namespace, member, path):
    dirPath = os.path.join(namespace, member, path)

    files, dirs = DataProvider.getDirContent(dirPath)
    response = { 'folders' : [], 'files': [], 'classifier': 'Folder', 'name': os.path.basename(path) }

    github, headline, wiki = DataProvider.getResolutionData(namespace, member)
    github = os.path.join(github, path)
    response['github'] = github
    response['headline'] = headline
    response['wiki'] = wiki

    #add all folders to the folders list and then sort the result
    for d in dirs:
        response['folders'].append({
            'resource': os.path.join(base_uri, dirPath, d),
            'name'    : d
        })

    #add all files to the files list and then sort the result
    for f in files:
        response['files'].append({
            'resource': os.path.join(base_uri, dirPath, f),
            'name'    : f,
            })

    return response

def discoverNamespaceMember(namespace, member):
    return discoverMemberPath(namespace, member,'')

def discoverNamespace(namespace):
    files, dirs = DataProvider.getDirContent(namespace)
    response = { 'members' : [], 'classifier': 'Namespace', 'name':namespace }

    github, headline, wiki = DataProvider.getResolutionData('namespaces',namespace)
    response['github'] = github
    response['headline'] = headline
    response['wiki'] = wiki

    for d in dirs:
        if not d.startswith('.'):
            response['members'].append({
                'resource': os.path.join(base_uri, namespace, d),
                'name'    : d
            })

    return response

def discoverAllNamespaces():
    files, dirs = DataProvider.getDirContent('')
    response = { 'members' : [], 'classifier':'Namespace', 'name':'Namespace'}

    github, headline, wiki = DataProvider.getResolutionData('namespaces','namespaces')
    response['github'] = github
    response['headline'] = headline
    response['wiki'] = wiki

    for d in dirs:
        if not d.startswith('.'):
            response['members'].append({
                'resource': os.path.join(base_uri, d),
                'name'    : d
            })

    return response

