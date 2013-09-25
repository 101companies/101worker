from repo import Repo
from contribution import Contribution
import getpass
import json
import sys
import os
from termcolor import colored

# detect contributions of lectures, their features and relevant commits
def detect_all(contribname, sha):
  print "Detecting for commit " + colored(sha, 'magenta')
  cachedir = '.'
  contributionso = {}
  features = set([])
  c = Contribution(contribname, loadfeatures=True, commitsha=sha)
  features.update(set(c.features.keys()))
  contributionso[c.rtitle] = {'features' : c.features}
  return json.dump(contributionso)

