from django.http import HttpResponse
import subprocess
import json
import urllib2
import os

def saveDetection(reponame, contribname, sha):
  base = 'http://worker.101companies.org/services/featureNameDetection'
  parameters = "?reponame={0}&contribname={1}&sha={2}".format(reponame, contribname, sha)
  detectionUrl = base + parameters
  try:
    detection = json.load(urllib2.urlopen(detectionUrl))
  except HTTPError:
    return None
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
    clones = json.load(urllib2.urlopen('http://101companies.org/api/clones?no_update=Yes'))
    clone = filter(lambda x: x['title'] == clonename, clones)
    return HttpResponse(json.dumps(clones), content_type='text/json')

