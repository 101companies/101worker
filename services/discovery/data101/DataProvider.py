__author__ = 'martin'

import json
import commands
import os
import re
import sys
sys.path.append('../../libraries/101meta')
import const101

extractContribRegex = re.compile('contributions/(?P<contribName>[^/]+)(/(?P<githubPath>.*))?')

def getMetadata(filePath):
    locator, extractor, geshi = None, None, None
    matchesFile = os.path.join(const101.tRoot, filePath + '.matches.json')
    if os.path.exists(matchesFile):
        matches = json.load(open(matchesFile))

        for unit in matches:
            if 'locator' in unit['metadata']  : locator = unit['metadata']['locator']
            if 'extractor' in unit['metadata']: extractor = unit['metadata']['extractor']
            if 'geshi' in unit['metadata']    : geshi = unit['metadata']['geshi']

    #locator = DataCache.getMatchesMetadata(filePath,'locator')
    #extractor = DataCache.getMatchesMetadata(filePath,'extractor')
    #geshi = DataCache.getMatchesMetadata(filePath, 'geshi')
    return locator, extractor, geshi

def getFragment(file, fragment, locator):
    fullFile = os.path.join(const101.sRoot, file)
    fullLocator = os.path.join(const101.sRoot, locator)
    command = '{0} {1} < {2}'.format(fullLocator, fragment, fullFile)
    status, output = commands.getstatusoutput(command)
    if not status == 0: raise Exception('Fragment location failed: {0}'.format(output))

    return json.loads(output)

def getFacts(file, extractor):
    #since the extractor module isn't ready to deal with the new form of communicating, I commented the file lookup out
    #for now
    #extractorFile = os.path.join(const101.tRoot, file + '.extractor.json')
    #if os.path.exists(extractorFile):
    #    return json.load(open(extractorFile, 'r'))

    fullFile = os.path.join(const101.sRoot, file)
    fullExtractor = os.path.join(const101.sRoot, extractor)
    command = '{0} < {1}'.format(fullExtractor, fullFile)
    status, output = commands.getstatusoutput(command)
    if not status == 0: raise Exception('Fact extraction failed: {0}'.format(output))

    return json.loads(output)

def getDirContent(dir):
    files, dirs = [], []
    path = os.path.join(const101.sRoot, dir)
    for f in os.listdir(path):
        if os.path.isdir(os.path.join(path, f)):
            dirs.append(f)
        else:
            files.append(f)

    files.sort()
    dirs.sort()

    return files, dirs
    #indexPath = os.path.join(const101.tRoot, dir, 'index.json')
    #index = json.load(open(indexPath, 'r'))
    #return index['files'], index['dirs']

def getResolutionData(path):
    match = extractContribRegex.match(path)
    if match:
        contrib = match.group('contribName')
        #metadata = DataCache.getResolutionData('contributions',contrib)

        #return metadata['101repo'], metadata['headline']

        resolutionDump = json.load(open(const101.resolutionDump, 'r'))
        meta = resolutionDump['results']['contributions'].get(contrib, None)
        if meta:
            github = meta['101repo']
            headline = meta['headline']
            if match.group('githubPath') and not github == '<unresolved>':
                github = os.path.join(github, match.group('githubPath'))

            return github, headline

    return None, None

def read(filePath, lines=None):
    fullPath = os.path.join(const101.sRoot, filePath)
    fp = open(fullPath, 'r')
    if lines:
        txt = [x for i, x in enumerate(fp) if i in lines]
    else:
        txt = fp.readlines()
    return ''.join(txt)