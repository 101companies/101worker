#!/usr/bin/env python
#coding=utf-8

# Generates a config for all existing books

import os
import shutil

def copytree(root_src_dir, root_dst_dir, symlinks=False, ignore=None):
    for src_dir, dirs, files in os.walk(root_src_dir):
        dst_dir = src_dir.replace(root_src_dir, root_dst_dir)
        if not os.path.exists(dst_dir):
            os.mkdir(dst_dir)
        for file_ in files:
            src_file = os.path.join(src_dir, file_)
            dst_file = os.path.join(dst_dir, file_)
            if os.path.exists(dst_file):
                os.remove(dst_file)
            shutil.move(src_file, dst_dir)

def get_immediate_subdirectories(dir):
	return [name for name in os.listdir(dir)
            if os.path.isdir(os.path.join(dir, name))]

languages = get_immediate_subdirectories('../../../101results/repos/101integrate/data/languages')
themes = get_immediate_subdirectories('../../../101results/repos/101integrate/data/themes')


baseResources = '../../../101web/data/resources/'
for lang in languages:
	copytree('../../../101results/repos/101integrate/data/languages/' + lang.strip() + "/", baseResources + 'languages/' + lang.strip() + "/")

for theme in themes:
	copytree('../../../101results/repos/101integrate/data/themes/' + theme.strip() + "/", baseResources + 'themes/' + theme.strip() + "/")
