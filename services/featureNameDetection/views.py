from repo import Repo
from wikiResource import WikiResource
import detection
import getpass
import json
import sys
import subprocess
from django.http import HttpResponse
from termcolor import colored
import pysftp

def set_worker(reponame, contribname, sha):
  print "Preparing worker for commit " + colored(sha, 'magenta')
  subprocess.Popen(["git", "checkout " + sha], cwd="/home/worker/101results/gitdeps/" + reponame, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  print "> " + colored(contribname, 'cyan')
  subprocess.Popen(["rm", "-rf", contribname], cwd="/home/worker/101results/101repo/contributions/", stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  subprocess.Popen(["cp", "-r", "/home/worker/101results/gitdeps/" + reponame + "/contributions/" + contribname, "/home/worker/101results/101repo/contributions/"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

def normalize_rules(rules):
  normalized_rules = {}
  for feature_name in rules:
    normalized_rules[feature_name.lower().replace('_', ' ')] = rules[feature_name]
  return normalized_rules

def explode_feature_rules():
  feature_ns = WikiResource("Namespace", "Feature", load=True)
  feature_ns_triples = feature_ns.triples
  feature_names = map(lambda y: y.subject.rtitle.lower().replace('_', ' '), filter(lambda x: x.predicate == "instanceOf" and x.subject.ns == "Feature" , feature_ns_triples))
  rules_raw =open('./rules.json')
  rules = normalize_rules(json.load(rules_raw))
  for feature_name in feature_names:
    if not feature_name in rules:
      rules[feature_name] = {'*': {'*': {'any': [feature_name]}}}
  return rules

def detectRequest(request):
  reponame = request.GET.get('reponame', '').split('/')[0]
  contribname = request.GET.get('contribname', '').split('/')[0]
  sha = request.GET.get('sha', '').split('/')[0]
  return detect(reponame, contribname, sha, True)


def detect(reponame, contribname, sha, set_worker):
  if len(contribname) > 0 and len(reponame) > 0 and len(sha) > 0:
    repo = Repo("101companies", reponame)
    if set_worker:
      set_worker(reponame, contribname, sha)
    rules = explode_feature_rules()
    features = detection.detect_all(contribname, sha, rules)
    if set_worker:
      set_worker(reponame, contribname, 'master')
    return json.dumps(features, indent=2)#HttpResponse(json.dumps(features), content_type='text/json')

#explode_feature_rules()
#print detect("101haskell", "haskellProfessional", "HEAD", False)
