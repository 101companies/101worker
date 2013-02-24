#! /usr/bin/env python

import sys
import os
import commands
import json

sys.path.append('../../libraries/101meta')
import const101
import tools101

technologiesDir = os.path.join(const101.sRoot, 'technologies')
problems = list()


### BUILD SYSTEMS
def buildMakefile(path):
    command = "cd {0}; make".format(path)
    status, output = commands.getstatusoutput(command)
    if not status == 0:
        problems.append({'build-system' : 'make', 'technology' : path, 'output' : output})

def buildAnt(path):
    command = "cd {0}; ant compile".format(path)
    status, output = commands.getstatusoutput(command)
    if not status == 0:
        problems.append({'build-system' : 'ant', 'technology' : path, 'output' : output})

### HELPERS
def getDirs(dir):
    return [name for name in os.listdir(dir)
            if os.path.isdir(os.path.join(dir, name))]

def getFiles(dir):
    return [name for name in os.listdir(dir)
            if os.path.isfile(os.path.join(dir, name))]


### MAIN PROGRAM
for tech in getDirs(technologiesDir):
    techDir = os.path.join(technologiesDir, tech)
    for file in getFiles(techDir):
        if file == 'Makefile':
            buildMakefile(techDir)
            break
        if file == 'build.xml':
            buildAnt(techDir)
    tools101.tick()

print '\nFinished building technologies'
if len(problems) > 0:
    print "\nproblems:\n\t{0}".format(json.dumps(problems))