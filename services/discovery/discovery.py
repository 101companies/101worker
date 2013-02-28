import os
import json
import re
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
    return {
        'resource' : os.path.join(base_uri, filePath, fragmentPath, fragment['classifier'], fragment['name']),
        'name'     : fragment['name'],
    }

def mapFacts(filePath, facts, query=None):
    result = []
    if query:
        for fragment in facts['fragments']:
            frag, fragmentPath = find(fragment, query)
            if frag:
                for fr in frag.get('fragments',[]):
                    result.append( mapFragment(filePath, fragmentPath, fr) )
                return result

    for fragment in facts.get('fragments', []):
        fragmentPath = os.path.join(fragment['classifier'], fragment['name'])
        result.append( mapFragment(filePath, fragmentPath, fragment) )

    return result

def discoverFragment(path, fileName, fragment):
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
        response['fragments'] = mapFacts(filePath, extractedFacts, fragment)

    return json.dumps( response )

def discoverFile(path, fileName):
    filePath = os.path.join(path, fileName)

    #if no geshi code is defined, then we'll return basically "geshi : null" and nothing else
    locator, extractor, geshi = helper101.getMetadata(filePath)
    response = { 'geshi' : geshi }

    #if there is a geshi code, we should be able to get content
    if geshi:
        response['content'] = helper101.read(filePath)

    #if there is a fact extractor, then we also want give back selectable fragments
    if extractor:
        extractedFacts = helper101.getFacts(filePath, extractor)
        response['fragments'] = mapFacts(filePath, extractedFacts)

    #get repo link
    response['github'] = '<not resolved>'
    regex = re.compile('contributions/(?P<contribName>[^/]+)/(?P<githubPath>.+)')
    match = regex.match(filePath)
    github =  helper101.getRepoLink(match.group('contribName'))
    if github:
        response['github'] = os.path.join(github, match.group('githubPath'))

    return json.dumps( response )

def discoverDir(path):
    files, dirs = helper101.getDirContent(path)
    response = { 'folders' : [], 'files': [] }

    for d in dirs:
        response['folders'].append({
            'resource': os.path.join(base_uri, path, d),
            'name'    : d
        })

    for f in files:
        response['files'].append({
            'resource': os.path.join(base_uri, path, f),
            'name'    : f,
        })

    return json.dumps( response )