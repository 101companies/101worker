import os
import json
import sys
sys.path.append('../../libraries/101meta')
import const101

#TODO usefullness of cache is limited - basically, there are multiple processes and every process uses his own "cache". also, this is a hack, i guess

_matchesCache = None
_resolutionCache = None

def _loadMatchesDump():
    global _matchesCache

    rawDump = json.load(open(const101.matchesDump, 'r'))['matches']
    _matchesCache = {
        'source' : const101.matchesDump,
        'mTime' : os.path.getmtime(const101.matchesDump),
        'data'  : {}
    }

    for entry in rawDump:
        filename = entry['filename']
        metadata = {}
        for unit in entry['units']:
            for key in unit['metadata'].keys():
                metadata[key] = unit['metadata'][key]
        _matchesCache['data'][filename] = metadata

def _loadResolution():
    global _resolutionCache

    rawDump = json.load(open(const101.resolutionDump, 'r'))['results']
    _resolutionCache = {'source': const101.resolutionDump, 'mTime': os.path.getmtime(const101.resolutionDump), 'data': rawDump}

def _cacheValid(cache):
    if not cache:
        return False
    #if os.path.getmtime(cache['source']) > cache['mTime']:
    #    return False

    return True

def getMatchesMetadata(filename, key, stdValue = None):
    global _matchesCache

    if not _cacheValid(_matchesCache):
        _loadMatchesDump()

    if not filename in _matchesCache['data']: return None

    return _matchesCache['data'][filename].get(key, stdValue)

def getResolutionData(category, key, stdValue = None):
    global _resolutionCache

    if not _cacheValid(_resolutionCache):
        _loadResolution()

    if not category in _resolutionCache['data']: return None

    return _resolutionCache['data'][category].get(key, stdValue)