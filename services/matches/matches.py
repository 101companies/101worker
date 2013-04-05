import os
import json
import sys
import commands
sys.path.append('../../libraries/101meta')
import const101
import tools101
sys.path.append('../../libraries')
from cores import *
from cores import matchesCore

path = ''
rules = json.load(open(const101.rulesDump))["results"]["rules"]
matches = {}



def matchingFunc(sFile, tFile):
    global matches
    global rules
    global path

    dirname = os.path.dirname(sFile)
    basename = os.path.basename(sFile)

    #deleting part of the dirname is necessary because of the "filename" constraint
    units = matchesCore.handleFile('basics', dirname, basename, rules)
    #units.append(matchesCore.handleFile('predicates', dirname, basename, rules))
    tmp = sFile[len(path):]
    if tmp.startswith('/'):
        tmp = sFile[len(path) + 1:]
    matches[tmp] = units

def matchFiles(username, reponame, subfolder):
    global matches
    global path

    matches = {}

    path = os.path.join(const101.results101, '101communication', username, reponame, subfolder)
    if not os.path.exists(path):
        return None

    loopOverDir(path, '', '', matchingFunc)

    matches['path'] = path

    return matches

def checkout(username, reponame):
    target = os.path.join (const101.results101, '101communication', username)
    #make sure dirs exist and save current working directory
    tools101.makedirs(target)
    cwd = os.path.abspath(os.getcwd())

    if os.path.exists(os.path.join(target,reponame)):
        os.chdir(os.path.join(target, reponame))
        cmd = 'git pull'
    else:
        os.chdir(target)
        cmd = 'git clone https://github.com/{0}/{1}'.format(username, reponame)

    status, output = commands.getstatusoutput(cmd)
    os.chdir(cwd)

    #status != 0 means an error occured
    if not status == 0:
        raise Exception('Clone failed')