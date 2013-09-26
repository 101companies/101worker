from django.http import HttpResponse
import subprocess
import json
import urllib2
import os

def saveDetection(reponame, contribname, sha):
  base = 'http://worker.101companies.org/services/featureNameDetection'
  parameters = "?reponame={0}&contribname={1}&sha={2}".format(reponame, contribname, sha)
  detectionUrl = base + parameters
  detection = json.load(urllib2.urlopen(detectionUrl))
  title = detection.keys()[0]
  features = {}
  for feature, locations in (detection[title]['features']).items():
    features[feature] = map(lambda l: l['resource'].replace("http://101companies.org/resources/contributions/" + contribname, ''), locations)
  return features

def diffFeatures(originalFeatures, clonedFeatures):
  features = {}
  for feature, locations in originalFeatures.items():
    if not feature in clonedFeatures:
      features[feature] = []
    else:
      diff = set(locations).intersection(set(clonedFeatures[feature]))
      diff = sorted(map(lambda x: locations.index(x) + 1, diff))
      features[feature] = diff
  return features


def diff(request):
  clonename = request.GET.get('clonename', '')
  if len(clonename) > 0:
    clones = json.load(urllib2.urlopen('http://101companies.org/api/clones'))
    clone = filter(lambda x: x['title'] == clonename, clones)
    if len(clone) > 0:
      clone = clone[0]
      if clone['clone_commit_sha']:
        originalFeatures = saveDetection('101haskell', clone['original'], clone['original_commit_sha'])
        clonedFeatures = saveDetection('101haskellclones', clone['title'], clone['clone_commit_sha'])
        result = diffFeatures(originalFeatures, clonedFeatures)
      else:
        result = {'error': 'no clone commit found'}
    else:
     result = {'error': 'clone not found'}
  else:
    result = {'error': 'no clone name given'}
  return HttpResponse(json.dumps(result), content_type='text/json')
