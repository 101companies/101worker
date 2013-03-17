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

    github = DataProvider.getGithub(namespace,member)
    github = os.path.join(github, path, file)
    response['github'] = github
    wiki, headline = DataProvider.getWikiData(namespace,member)
    response['headline'] = headline
    response['wiki'] = wiki

    initiator, contributors = DataProvider.getCommitInfo(filePath)
    response['commits'] = {'initiator' : initiator['author'], 'contributors' : []}
    for contributor in contributors:
        response['commits']['contributors'].append(contributor['author'])

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

    github = DataProvider.getGithub(namespace,member)
    github = os.path.join(github, path, file)

    response['github'] = github
    wiki, headline = DataProvider.getWikiData(namespace,member)
    response['headline'] = headline
    response['wiki'] = wiki

    response['commits'] = {'initiator' : None, 'contributors' : None}
    initiator, contributors = DataProvider.getCommitInfo(filePath)
    if initiator:
        response['commits']['initiator'] = initiator['author']
    if contributors:
        response['commits']['contributors'] = []
        for contributor in contributors:
            if contributor['author'] not in response['commits']['contributors']:
                response['commits']['contributors'].append(contributor['author'])

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
    response = { 'folders' : [], 'files': [], 'classifier': 'Folder', 'name': os.path.basename(path) }

    github = DataProvider.getGithub(namespace,member)
    if github:
        github = os.path.join(github, path)
    response['github'] = github
    wiki, headline = DataProvider.getWikiData(namespace,member)
    response['headline'] = headline
    response['wiki'] = wiki

    dirPath = os.path.join(namespace, member, path)
    files, dirs = DataProvider.getDirContent(dirPath)

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

    return response

def discoverNamespaceMember(namespace, member):
    response = {
        'folders': [], 'files': [],
        'classifier': 'Member', 'name': member,
        'github': DataProvider.getGithub(namespace, member)
    }

    wiki, headline = DataProvider.getWikiData(namespace,member)
    response['headline'] = headline
    response['wiki'] = wiki

    dirPath = os.path.join(namespace, member)
    files, dirs = DataProvider.getDirContent(dirPath)

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

    return response

def discoverNamespace(namespace):
    response = {'classifier': 'Namespace', 'name': namespace, 'github': DataProvider.getGithub(namespace, '')}

    wiki, headline = DataProvider.getWikiData('Namespace', namespace)
    response['headline'] = headline
    response['wiki'] = wiki

    members = DataProvider.getMembers(namespace)
    response['members'] = []
    for member in members:
        response['members'].append({
            'resource': os.path.join(base_uri, namespace, member),
            'name'    : member
        })

    return response

def discoverAllNamespaces():
    files, dirs = DataProvider.getDirContent('')
    response = {'members': [], 'classifier': 'Namespace', 'name': 'Namespace', 'github': DataProvider.getGithub('', '')}

    wiki, headline = DataProvider.getWikiData('Namespace','Namespace')
    response['headline'] = headline
    response['wiki'] = wiki

    for d in dirs:
        if not d.startswith('.'):
            response['members'].append({
                'resource': os.path.join(base_uri, d),
                'name'    : d
            })

    return response

