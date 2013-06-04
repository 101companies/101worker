from tools import loadPage
from tools import dot
import json


def _getMetrics(file):
    data = loadPage(file)
    derived = data.get('derived', [])

    if derived:
        for d in derived:
            if d['name'].endswith('metrics.json'):
                return loadPage(d['resource'])

    return {}


def _extractFilesFromFolder(uri):
    folder = loadPage(uri)
    files = []

    for file in folder.get('files', []):
        files.append({
            'resource': file['resource'],
            'metrics': _getMetrics(file['resource'])
        })

    for subFolder in folder.get('folders', []):
        files += _extractFilesFromFolder(subFolder['resource'])

    return files


def _isSystemRelevant(data):
    return data.get('relevance', 'system') == 'system'


def calculateMetricsForContributions(blacklist=[]):
    problems = []
    contributionMetrics = {}
    debug = {}

    contributions = loadPage('http://101companies.org/resources/contributions')['members']
    for contribution in contributions:
        if contribution['name'] in blacklist:
            continue

        dot()
        #print 'extracting files from {}'.format(contribution['name'])
        try:
            files = _extractFilesFromFolder(contribution['resource'])
        except Exception as e:
            problems.append({
                'resource': contribution['resource'],
                'exception': str(e)
            })

        size = 0
        loc = 0
        ncloc = 0

        for file in files:
            if not file.get('metrics', {}) == {}:
                metrics = file['metrics']
                if _isSystemRelevant(metrics):
                    size += int(metrics['size'])
                    loc += int(metrics['loc'])
                    ncloc += int(metrics['ncloc'])

        finalMetrics = {
            'size': size,
            'loc': loc,
            'ncloc': ncloc
        }

        debug[contribution['name']] = {
            'files': files,
            'metrics': finalMetrics
        }

        contributionMetrics[contribution['name']] = finalMetrics

    #serialize debug output
    json.dump(contributionMetrics, open('debugOutput/contributionMetrics.json', 'w'), indent=4)
    json.dump(debug, open('debugOutput/debug.json', 'w'), indent=4)
    json.dump(problems, open('debugOutput/metrics_problems.json', 'w'), indent=4)

    return contributionMetrics