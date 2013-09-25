import json
import urllib2
import os
import shutil
from subprocess import call

def aggregateCommentLines(source, features):
  detectionsurl = 'http://data.101companies.org/dumps/detection_HEAD.json'
  detections = json.load(urllib2.urlopen(detectionsurl))[source]['features']
  commentLines = []
  for feature in features:
    print feature
    if feature in detections:
      for location in detections[feature]:
        locationurl = location['resource']
        complete = location['classifier'] == 'File'
        res =  {'complete': complete}
        path = locationurl.replace('http://101companies.org/resources/','')
        if not complete:
          done = False
          while not done:
            try:
              fragment = json.load(urllib2.urlopen(locationurl))
              done = True
            except urllib2.HTTPError as e:
              pass
          [start, end] = fragment['github'].split('#L')[1].split('-')
          res['start'] = int(start)
          res['end'] = int(end)
          path = '/'.join(path.split('/')[0:-2])
        res['path'] = path
        commentLines.append(res)
  return commentLines

def create(repofrombase, repotobase, title, original, features):
  originalpath = repofrombase + 'contributions/' + original
  clonepath = repotobase + 'contributions/' + title
  if not os.path.exists(clonepath):
    shutil.copytree(originalpath, clonepath)
    liness = aggregateCommentLines(original, features)
    for lines in liness:
      path = lines['path']
      print path
      print lines
      pathto = '/'.join(path.split('/')[0:1] + [title] + path.split('/')[2:])
      f1 = open(repofrombase + path, 'r+')
      f2 = open(repotobase + pathto, 'w+')
      filelines = f1.read().splitlines()
      f1.close()
      if lines['complete']:
        lines['start'] = 0
        lines['end'] = len(filelines)
      newlines = filelines[:lines['start']] + map(lambda l: '-- ' + l, filelines[lines['start']:lines['end']]) + filelines[lines['end']:]
      f2.seek(0)
      for line in newlines:
        f2.write(line + '\n')
      f2.truncate()
      f2.close()

repofrombase = '../../../101results/gitdeps/101haskell/'
repotobase = '../../../101results/gitdeps/101haskellclones/'
cloneapiurl = "http://localhost:3000/api/clones"
clones = json.load(urllib2.urlopen(cloneapiurl))
for clone in clones:
  if clone['status'] == 'in_preparation':
    os.system('cd ' + repotobase + '; git pull')
    print 'Preparing ' + clone['title']
    create(repofrombase, repotobase, clone['title'], clone['original'], clone['minusfeatures'])
    os.system('cd ' + repotobase + '; git add .; git commit -m "preparing clone \'' + clone['title'] + ' \' "; git push')

