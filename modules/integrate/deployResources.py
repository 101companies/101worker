#!/usr/bin/env python
#coding=utf-8

# Generates a config for all existing books

import os
import shutil

def get_immediate_subdirectories(dir):
	return [name for name in os.listdir(dir)
            if os.path.isdir(os.path.join(dir, name))]

languages = get_immediate_subdirectories('../../../101results/repos/101integrate/data/languages')
themes = get_immediate_subdirectories('../../../101results/repos/101integrate/data/themes')


baseResources = '../../../101web/data/resources/'
for lang in languages:
	shutil.copy2('../../../101results/repos/101integrate/data/languages/' + lang.strip() + '/coverage.html', baseResources + 'languages/' + lang.strip())

for theme in themes:
	shutil.copy2('../../../101results/repos/101integrate/data/themes/' + theme.strip() + '/coverage.html', baseResources + 'themes/' + theme.strip())
