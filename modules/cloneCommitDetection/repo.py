import requests

class Repo:

  def __init__(self, owner, repo):
    self.owner = owner
    self.repo =repo
    self.urlroot = "https://api.github.com"
    self.repourl = self.urlroot + "/repos/%s/%s"%(owner, repo)

  def get(self, suffix):
    url = self.repourl + suffix
    return requests.get(url).json()

  def all_commit_shas(self):
    shas = []
    newones = self.get('/commits')
    while len(newones) > 1:
      print len(newones)
      shas.extend(map(lambda x: x['sha'], newones))
      strr = '/commits?until=' + newones[-1]['commit']['committer']['date']
      newones = self.get(strr)
    return shas

  def commits_by_path(self, path):
    return self.get('/commits?path=' + path)

  def commits_by_path_since(self, path, since):
    return self.get('/commits?path=%s&since=%s'%(path, since))

  def commit(self, sha):
    return self.get("/commits/" + sha)
