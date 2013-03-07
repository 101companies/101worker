import os
import json
from string import Template
import helper101


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

#user has given us the path to a fragment - so we'll return infos, content of that fragment plus all sub-fragments
def discoverFragment(path, fileName, fragment):
    filePath = os.path.join(path, fileName)

    #if no geshi code is defined, then we'll return basically "geshi : null" and nothing else
    locator, extractor, geshi = helper101.getMetadata(filePath)
    response = { 'geshi' : geshi }

    github, headline = helper101.getResolutionData(filePath)
    response['github'] = github
    response['headline'] = headline

    if locator:
        lines = helper101.getFragment(filePath, fragment, locator)
        fragmentText = helper101.read(filePath, range(lines['from'] - 1, lines['to']))
        response['content'] = fragmentText

        response['github'] += '#L{0}-{1}'.format(lines['from'], lines['to'])

    if extractor:
        extractedFacts = helper101.getFacts(filePath, extractor)
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

#user has given us path to a file - so we'll return infos about that files plus all fragments in that file and the content
def discoverFile(path, fileName):
    filePath = os.path.join(path, fileName)

    #if no geshi code is defined, then we'll return basically "geshi : null" and nothing else
    locator, extractor, geshi = helper101.getMetadata(filePath)
    response = { 'geshi' : geshi, 'classifier': 'File' }

    #if there is a geshi code, we should be able to get content
    if geshi:
        response['content'] = helper101.read(filePath)

    github, headline = helper101.getResolutionData(filePath)
    response['github'] = github
    response['headline'] = headline

    #if there is a fact extractor, then we also want give back selectable fragments
    if extractor:
        extractedFacts = helper101.getFacts(filePath, extractor)
        fragments = []
        for fragment in extractedFacts.get('fragments', []):
            fragmentPath = os.path.join(fragment['classifier'], fragment['name'])
            fragments.append( mapFragment(filePath, fragmentPath, fragment) )

        response['fragments'] = fragments

    #response['github'] = helper101.getRepoLink(filePath)

    return response

#user has given us the path to a dir, so we'll return a list of all files and folders in that particular folder
def discoverDir(path):
    files, dirs = helper101.getDirContent(path)
    response = { 'folders' : [], 'files': [], 'classifier': 'Folder' }

    github, headline = helper101.getResolutionData(path)
    response['github'] = github
    response['headline'] = headline

    #add all folders to the folders list and then sort the result
    for d in dirs:
        response['folders'].append({
            'resource': os.path.join(base_uri, path, d),
            'name'    : d
        })

    #add all files to the files list and then sort the result
    for f in files:
        response['files'].append({
            'resource': os.path.join(base_uri, path, f),
            'name'    : f,
        })

    return response