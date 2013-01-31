#! /usr/bin/env python

import os
import sys
import json
import commands
sys.path.append('../../libraries/101meta')
import const101

def handleNormal(dump, dep):
	url = dep['sourcerepo'].replace('.git', '')
	if url.startswith('git'):
		url = url.replace('git', 'https', 1)
	if not dep['sourcedir'] == '/':
		url += '/tree/master/' + dep['sourcedir']
	dump[dep['targetdir'].split('/')[1]] = url

def handleSubdirs(dump, dep):
	parts = dep['sourcerepo'].split('/')
	contribName = parts[len(parts)-1].replace('.git', '')
	path = os.path.join(os.path.dirname(const101.sRoot), 'gitdebs', contribName)
	if not dep['sourcedir'] == '/':
		path +=  dep['sourcedir']
	url = dep['sourcerepo'].replace('.git', '')
	if url.startswith('git'):
		url = url.replace('git', 'https', 1)
	url += '/tree/master' + dep['sourcedir']
	if not url.endswith('/'):
		url += '/'
	for c in os.listdir(path):
		if os.path.isdir(os.path.join(path, c)):
			dump[c] = url + c

dump = {}
path = os.path.join(const101.sRoot, 'contributions')
for f in os.listdir(path):
	if os.path.isdir(os.path.join(path, f)):
		dump[f] = "https://github.com/101companies/101repo/tree/master/contributions/" + f

local = json.load(open('./gitdeps_local', 'r'))
for dep in local:
	if not 'mode' in dep or not dep['mode'] == 'subdirsonly':
		handleNormal(dump, dep)
	else:
		handleSubdirs(dump,dep)


json.dump(dump, open(const101.pullRepoDump, 'w'))
dumpstring = json.dumps(dump)
jsonpf = open(const101.pullRepoDump + "p", 'w')
jsonpf.write("callback(" + dumpstring + ");")
jsonpf.close()

