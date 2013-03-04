import os
import json
import re
from string import Template
import urlparse
import helper101

base_uri = ''

def find(fragment, query, basePath=None):
    #create recreate fragment path
    fragmentPath = os.path.join(fragment['classifier'], fragment['name'])
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

    return {
        'resource'  : resource,
        'name'      : fragment['name'],
        'classifier': fragment['classifier']
    }

def discoverFragment(path, fileName, fragment, url_params):
    filePath = os.path.join(path, fileName)

    #if no geshi code is defined, then we'll return basically "geshi : null" and nothing else
    locator, extractor, geshi = helper101.getMetadata(filePath)
    response = { 'geshi' : geshi }

    if locator:
        lines = helper101.getFragment(filePath, fragment, locator)
        fragmentText = helper101.read(filePath, range(lines['from'] - 1, lines['to']))
        response['content'] = fragmentText

    if extractor:
        extractedFacts = helper101.getFacts(filePath, extractor)
        for f1 in extractedFacts['fragments']:
            selected, fragmentPath = find(f1, fragment)
            if selected:
                response['classifier'] = selected['classifier']
                response['fragments'] = []
                for f2 in selected.get('fragments',[]):
                    response['fragments'].append(mapFragment(filePath, fragmentPath, f2))
                break

    if url_params.get('format', 'json') == 'json':
        return json.dumps( response )

    return wrapInHTML('fragment', response)

def discoverFile(path, fileName, url_params):
    filePath = os.path.join(path, fileName)

    #if no geshi code is defined, then we'll return basically "geshi : null" and nothing else
    locator, extractor, geshi = helper101.getMetadata(filePath)
    response = { 'geshi' : geshi, 'classifier': 'File' }

    #if there is a geshi code, we should be able to get content
    if geshi:
        response['content'] = helper101.read(filePath)

    #if there is a fact extractor, then we also want give back selectable fragments
    if extractor:
        extractedFacts = helper101.getFacts(filePath, extractor)
        fragments = []
        for fragment in extractedFacts.get('fragments', []):
            fragmentPath = os.path.join(fragment['classifier'], fragment['name'])
            fragments.append( mapFragment(filePath, fragmentPath, fragment) )

        response['fragments'] = fragments

    #get repo link
    response['github'] = '<not resolved>'
    regex = re.compile('contributions/(?P<contribName>[^/]+)/(?P<githubPath>.+)')
    match = regex.match(filePath)
    github = helper101.getRepoLink(match.group('contribName'))
    if github:
        response['github'] = os.path.join(github, match.group('githubPath'))

    if url_params.get('format', 'json') == 'json':
        return json.dumps( response )

    return wrapInHTML('file', response)

def discoverDir(path, url_params):
    files, dirs = helper101.getDirContent(path)
    response = { 'folders' : [], 'files': [], 'classifier': 'Folder' }


    for d in dirs:
        response['folders'].append({
            'resource': os.path.join(base_uri, path, d),
            'name'    : d
        })
    response['folders'].sort()

    for f in files:
        response['files'].append({
            'resource': os.path.join(base_uri, path, f),
            'name'    : f,
        })
    response['files'].sort()

    if url_params.get('format', 'json') == 'json':
        return json.dumps( response )

    return wrapInHTML('folders', response)

def wrapInHTML(discoverType, response):
    def read(path):
        return ''.join(open(path, 'r').readlines())

    if discoverType == 'folders':
        dirTemplate = Template(read('templates/discoverDir.html'))

        dirs = ''
        for d in response['folders']:
            dirs += Template(read('templates/singledir.html')).substitute({'name':str(d['name']), 'link':str(d['resource'])})
        if dirs == '': dirs = 'None'

        files = ''
        for f in response['files']:
            files += Template(read('templates/singlefile.html')).substitute({'name':str(f['name']), 'link':str(f['resource'])})
        if files == '': files = 'None'

        return dirTemplate.substitute({'folderList' : dirs, 'filesList' : files})

    #if it isn't a folder, then we can expect some values
    if 'fragments' in response:
        fragments = ''
        for f in response['fragments']:
            fragments += Template(read('templates/singlefragment.html')).substitute({'name':str(f['name']), 'link':str(f['resource'])})
        if fragments == '': fragments = 'None'
    else:
        fragments = 'not extractable'

    if 'content' in response:
        content = response['content']
    else:
        content = 'not extractable'


    if discoverType == 'file':
        fileTemplate = Template(read('templates/discoverFile.html'))
        return fileTemplate.substitute({'content': content, 'fragmentList':fragments, 'github':str(response['github'])})

    if discoverType == 'fragment':
        fragmentTemplate = Template(read('templates/discoverFragment.html'))
        return fragmentTemplate.substitute({'content': content, 'fragmentList': fragments, 'fragmentType': str(response['classifier'])})
