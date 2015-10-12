import urllib2
import json
import sys

opener = urllib2.build_opener()

def loadPage(url):
    req = urllib2.Request(url)
    f = opener.open(req)
    return json.load(f)

def dot():
    sys.stdout.write('.')
    sys.stdout.flush()