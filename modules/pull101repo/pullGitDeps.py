#! /usr/bin/env python

import os
import sys
import json
import shutil
import commands
sys.path.append('../../libraries/101meta')
import const101

# DIFFERENT FUNCTIONS
def ensureFolder(folder):
	if not os.path.exists(folder):
		os.makedirs(folder)

def getRepoName(repoUrl):
	(head, tail) = os.path.split(repoUrl)
	return tail.replace('.git', '')

def ignoredFile(dirpath, contents):
	return [filename for filename in contents if filename == '.git']

def removeContrib(dep):
	name = getRepoName(dep['sourcerepo'])
	path = os.path.join(const101.sRoot, dep['targetdir'])
	if os.path.isdir(path):
		print 'removing ' + name
		copied.remove(path)
		shutil.rmtree(path)	
		shutil.rmtree(os.path.join(gitdepsFolder, name))

def removeSubdirs(dep):
	name = getRepoName(dep['sourcerepo'])
	depsPath = os.path.join(gitdepsFolder, name)
	dirList = os.listdir(depsPath)
	for fname in dirList:
		if not '.git' in fname or 'README' in fname:
			contribPath = os.path.join(const101.sRoot, dep['targetdir'], fname)		
			if os.path.isdir(contribPath):
				print 'removing ' + contribPath
				copied.remove(contribPath)
				shutil.rmtree(contribPath)
	path = os.path.join(gitdepsFolder, name)
	print 'removing ' + path
	shutil.rmtree(path)

def copyContrib(dep):
	name = getRepoName(dep['sourcerepo'])
	if dep.get('needsUpdate') or not os.path.exists(os.path.join(const101.sRoot, dep['targetdir'])):
		#if we created the folder, then we can remove it - otherwise, we are supposed to throw an exception - which copytree does, since copytree doesn't overwrite
		if os.path.exists(os.path.join(const101.sRoot, dep['targetdir'])):
			shutil.rmtree(os.path.join(const101.sRoot, dep['targetdir']))
		print 'copying ' + name
		copied.append(os.path.join(const101.sRoot, dep['targetdir']))
		shutil.copytree(os.path.join(gitdepsFolder, name, dep['sourcedir'][1:]), os.path.join(const101.sRoot, dep['targetdir']), ignore=ignoredFile)

def copySubdirs(dep):
	name = getRepoName(dep['sourcerepo'])
	depsPath = os.path.join(gitdepsFolder, name, dep['sourcedir'][1:])
	dirList = os.listdir(depsPath)
	for fname in dirList:
		if os.path.isdir(os.path.join(depsPath, fname)) and not '.git' in fname:
			if dep.get('needsUpdate') or not os.path.exists(os.path.join(const101.sRoot, dep['targetdir'], fname)):
				#if we created the folder, then we can remove it - otherwise, we are supposed to throw an exception - which copytree does, since copytree doesn't overwrite
				if os.path.exists(os.path.join(const101.sRoot, dep['targetdir'], fname)):
						shutil.rmtree(os.path.join(const101.sRoot, dep['targetdir'], fname))			
				print 'copying ' + fname
				copied.append(os.path.join(const101.sRoot, dep['targetdir'], fname))
				shutil.copytree(os.path.join(depsPath, fname), os.path.join(const101.sRoot, dep['targetdir'], fname), ignore=ignoredFile)


#MAIN PROGRAM
basePath = os.path.dirname(const101.sRoot)
gitdepsFolder = os.path.join(basePath, "gitdebs")
gitdepsFile = '../../../101results/101repo/.gitdeps'
ensureFolder(gitdepsFolder)
gitdepsJson = json.loads(open(gitdepsFile).read())
copied = json.loads(open('./.copied').read())


if os.path.isfile('./gitdeps_local'):
	print 'removing old files, if necessary'
	localGitDeps = json.loads(open('./gitdeps_local').read())
	for dep in localGitDeps:
		if not dep in gitdepsJson:
			if not dep.get('mode') == 'subdirsonly':
				removeContrib(dep)
			else:
				removeSubdirs(dep)
				
print 'updating contributions'
for dep in gitdepsJson:
	if '@' in dep['sourcerepo']:
		print dep['sourcerepo'] + " doesn't seem to be a read only Github Url! Omitted entry..."
		continue
	status, output = commands.getstatusoutput("./pullRepo.py " + os.path.join(gitdepsFolder, getRepoName(dep['sourcerepo'])) + " " + dep["sourcerepo"])
	if not output == '':
		print output
		dep['needsUpdate'] = True
	if (status):
		print "pullGitDebs failed on " + dep['sourcerepo']
		sys.exit(status)

print "copying files, if needed"
for dep in gitdepsJson:
		name = getRepoName(dep['sourcerepo'])
		if not dep.get('mode') == 'subdirsonly':		
			copyContrib(dep)
		else:
			copySubdirs(dep)

print "saving .gitdebs file"
shutil.copy(gitdepsFile, './gitdeps_local')
f = open('./.copied', 'w')
f.write(json.dumps(copied))
