#!/usr/bin/env python
#coding=utf-8

# Generates a config for all existing books

import os
import shutil

def copytree(src, dst, symlinks=False, ignore=None):
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copytree(s, d, symlinks, ignore)
        else:
            if not os.path.exists(d) or os.stat(src).st_mtime - os.stat(dst).st_mtime > 1:
                shutil.copy2(s, d)

def get_immediate_subdirectories(dir):
	return [name for name in os.listdir(dir)
            if os.path.isdir(os.path.join(dir, name))]

languages = get_immediate_subdirectories('../../../101results/repos/101integrate/data/languages')
themes = get_immediate_subdirectories('../../../101results/repos/101integrate/data/themes')


baseResources = '../../../101web/data/resources/'
for lang in languages:
	shutil.copytree('../../../101results/repos/101integrate/data/languages/' + lang.strip(), baseResources + 'languages/' + lang.strip())

for theme in themes:
	shutil.copytree('../../../101results/repos/101integrate/data/themes/' + theme.strip(), baseResources + 'themes/' + theme.strip())
