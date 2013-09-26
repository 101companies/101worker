from django.http import HttpResponse
import subprocess
import json
import urllib2
import os

def saveDetection(reponame, contribname, sha, filename):
  base = 'http://worker.101companies.org/services/featureNameDetection'
  parameters = "?reponame={0}&contribname={1}&sha={2}".format(reponame, contribname, sha)
  detectionUrl = base + parameters
  detection = json.load(urllib2.urlopen(detectionUrl))
  title = detection.keys()[0]
  features = {}
  for feature, locations in (detection[title]['features']).items():
    features[feature] = map(lambda l: l['resource'].replace("http://101companies.org/resources/contributions/" + contribname, ''), locations)
  with open(filename, 'w') as outfile:
    json.dump(features, outfile, indent=2)


def diff(request):
  clonename = request.GET.get('clonename', '')
  if len(clonename) > 0:
    clones = json.load(urllib2.urlopen('http://101companies.org/api/clones'))
    clone = filter(lambda x: x['title'] == clonename, clones)
    if len(clone) > 0:
      clone = clone[0]
      if clone['clone_commit_sha']:
        originalFileName = 'original.json'
        cloneFileName = 'clone.json'
        diffFileName = 'diff.json'
        saveDetection('101haskell', clone['original'], clone['original_commit_sha'], originalFileName)
        saveDetection('101haskellclones', clone['title'], clone['clone_commit_sha'], cloneFileName)
        p = subprocess.Popen(["java", "-jar", "FeatureDiff.jar", originalFileName, cloneFileName, diffFileName], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        p.wait()
        result = json.load(open(diffFileName))
        os.remove(originalFileName)
        os.remove(cloneFileName)
        os.remove(diffFileName)
      else:
        result = {'error': 'no clone commit found'}
    else:
     result = {'error': 'clone not found'}
  else:
    result = {'error': 'no clone name given'}
  return HttpResponse(json.dumps(result), content_type='text/json')
