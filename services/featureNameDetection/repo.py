import requests

class Repo:

  def __init__(self, owner, repo):
    self.owner = owner
    self.repo =repo
    self.urlroot = "https://api.github.com"
    self.repourl = self.urlroot + "/repos/%s/%s"%(owner, repo)

  def get(self, suffix):
    return requests.get(self.repourl + suffix).json

  def all_commit_shas(self):
    shas = []
    newones = self.get('/commits')
    while len(newones) > 1:
      print len(newones)
      shas.extend(map(lambda x: x['sha'], newones))
      strr = '/commits?until=' + newones[-1]['commit']['committer']['date']
      newones = self.get(strr)
    return shas

  def commit(self, sha):
    return self.get("/commits/" + sha)
