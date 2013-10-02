from repo import Repo
import json
import urllib2
import os

orignalsrepo = Repo('101clonebot', '101haskelloriginals)
clonerepo = Repo('tschmorleiz', '101haskellclones')
clones = json.load(urllib2.urlopen('http://101companies.org/api/clones'))


def prepareWorker(reponame, contribname, sha):
  #print 'cd ~/101results/gitdeps/' + reponame + '/; git checkout %s; cd ~'%sha
  os.popen('cd ~/101results/gitdeps/' + reponame + '/; git checkout %s; cd ~'%sha).read()
  os.popen('cp -r ~/101results/gitdeps/' + reponame + '/contributions/' + contribname + '/ ~/101results/101repo/contributions/').read()

def getFragmentsContents(relevantFiles, reponame, contribname, sha):
  urlbase = 'http://worker.101companies.org/services/featureNameDetection'
  params = '?reponame=%s&contribname=%s&sha=%s'%(reponame, contribname, sha)
  detection = json.load(urllib2.urlopen(urlbase + params))
  contents = {}
  prepareWorker(reponame, contribname, sha)
  for f, resources in detection[contribname]['features'].items():
    contents[f] = {}
    for i, r in enumerate(resources):
      resource = r['resource']
      if any(map(lambda f: f in resource, relevantFiles)):
        content = json.load(urllib2.urlopen(resource))['content']
      else:
        content = ''
      contents[f][resource] = {'index': i, 'content': content}
  return contents

def getLines(reponame, contribname, sha, fragmentpath):
  prepareWorker(reponame, contribname, sha)
  lines = json.load(urllib2.urlopen(fragmentpath))['github'].split('#L')[1].split('-')
  return {'from': int(lines[0]), 'to': int(lines[1])}

def isNewest(repo, path, since):
  x = repo.commits_by_path_since(path, since)
  return len(x) == 1

def replaceLines(contribname, path, lines, newcontent):
  path = path.split('.hs')[0] + '.hs'
  path = '/home/worker/101results/gitdeps/101haskellclones/contributions/' + contribname + path
  with open(path) as f:
    oldlines = f.read().splitlines()
    newlines = oldlines[:lines['from']-1] + newcontent.split('\n') + oldlines[lines['to']:]
    newcontent = '\n'.join(newlines)
  with open(path, 'w') as f:
    f.write(newcontent)

def check(clone, history):
  if 'checked_sha' in clone:
    lastChecked = clone['checked_sha']
  else:
    lastChecked = clone['original_commit_sha']
  if clone['title'] in history and type(history[clone['title']]) is dict:
    history = history[clone['title']]
  else:
    history = {'done': []}
  if 'inspection' in history:
    print 'Skipping %s, due to current inspection'%clone['title']
    return history
  print 'Checking "%s" at %s'%(clone['title'], lastChecked)
  lastCheckedDate = clonerepo.commit(lastChecked)['commit']['committer']['date']
  newcommits = orignalsrepo.commits_by_path_since('contributions/' + clone['original'], lastCheckedDate)
  print '> %d new commits found for original'%len(newcommits)
  if len(newcommits) > 0:
    try:
      os.popen('cd ~/101results/gitdeps/101haskellclones/contributions/%s; git checkout master; git checkout .; cd ~'%clone['title']).read()
      isNewest = len(clonerepo.commits_by_path_since('contributions/' + clone['title'], lastCheckedDate)) == 1
      if isNewest:
        print '> Can be automatically propagated to clone!'
      else:
        pass
      commit = newcommits[0]
      clonediffUrl = 'http://worker.101companies.org/services/diffClone?clonename=%s'
      clonediff = json.load(urllib2.urlopen(clonediffUrl%clone['title']))
      print ' > Checking commit %s'%commit['sha']
      commit = orignalsrepo.commit(commit['sha'])
      files = map(lambda f: f['filename'], commit['files'])
      print '  > %d files changed in commit'%len(files)
      lastCheckedFragments = getFragmentsContents(files, '101haskelloriginals', clone['original'], lastChecked)
      print '  > Checking %d fragments for changes '%len(lastCheckedFragments)
      commitFragments = getFragmentsContents(files, '101haskelloriginals', clone['original'], commit['sha'])
      changed = {}
      changedcount = 0
      for f, locations in lastCheckedFragments.items():
        changed[f] = []
        for location, content in locations.items():
          if location in commitFragments[f]:
            index = content['index'] + 1
            if content['content'] != commitFragments[f][location]['content'] and index in clonediff[f]:
              changed[f].append(location)
              changedcount += 1
      print '  > Found %s fragments to replace'%changedcount
      if changedcount > 0:
        branchname = 'propagate_%s_%s'%(clone['title'], commit['sha'])
        print '  > Creating branch ' + branchname
        os.popen('cd ~/101results/gitdeps/101haskellclones/; git pull; git checkout -b %s; cd ~'%branchname)
        for f, locations in changed.items():
          for location in locations:
            print '   > Replacing location ' + location
            lines = getLines('101haskellclones', clone['title'], clone['clone_commit_sha'], location)
            replaceLines(clone['title'], location.split(clone['original'])[1], lines,  commitFragments[f][location]['content'])
        print '  > Pushing new branch '
        os.popen('cd ~/101results/gitdeps/101haskellclones/; git checkout %s ;git pull ; cd ~'%branchname)
        os.popen('cd ~/101results/gitdeps/101haskellclones/; git add . ; cd ~')
        commitmessage = "new branch for propagating changes to %s from commit %s"%(clone['title'], commit['sha'])
        os.popen('cd ~/101results/gitdeps/101haskellclones/; git commit -m "%s"; cd ~'%commitmessage)
        os.popen('cd ~/101results/gitdeps/101haskellclones/; git push -u origin %s; cd ~'%branchname)
        os.popen('cd ~/101results/gitdeps/101haskellclones/contributions/%s; git checkout master; git checkout .; cd ~'%clone['title']).read()
      inspection = {}
      inspection['commits'] = map(lambda c: c['sha'], newcommits)
      inspection['branch'] = branchname
      history['inspection'] = inspection
    except Error:
      pass
  return history

os.popen('cd ~/101results/gitdeps/101haskellclones/; git pull; cd ~')
historypath = "/home/worker/101web/data/dumps/clonehistory.json"
try:
  with open(historypath) as f:
    history = json.load(f)
except IOError:
 history = {}
for clone in clones:
    if clone['status'] == 'created':
      history[clone['title']] = check(clone, history)
print history
with open(historypath, 'w') as f:
    json.dump(history, f)
