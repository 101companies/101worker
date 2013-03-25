#!/usr/bin/env python
#coding=utf-8

# Generates a config for all existing books

import os
import shutil


languages = get_immediate_subdirectories('../../../101results/repos/101integrate/data/languages')

baseResources = '../../../101web/data/resources/'
for lang in languages:
	shutil.copy2('../../../101results/repos/101integrate/data/languages/' + lang + '/coverage.html', base + 'languages/' + lang + )
