from .env import create_module_env, env
from .logger import report_error

import os
import sys
import traceback
import shutil

class Executor(object):

    def __init__(self, module):
        self._module = module
        self._env = create_module_env(env, self._module)

    def _exec(self, change):
        try:
            self._module.run(self._env, change)
        except:
            report_error(
                'module_failed',
                traceback.format_exc()
            )

    def run(self, changes):
        for change in changes:
            self._exec(change)
        ####### added to create Image ################
        if self._module.config.get('visualization') == True :        
            print("Creating Image")
            folderName = str(self._module).replace("'","").split(" ")[1]
            path = self._env.get_env('views101dir')
            if(os.path.isdir(path + os.sep + folderName)):
                shutil.rmtree(path + os.sep + folderName)
            self._module.visualize(self._env)
        ##############################################

class FileFullSweepExecutor(Executor):

    def run(self, changes):
        for root, dirs, files in os.walk(env['repo101dir']):
            for f in files:
                if '.git' in os.path.join(root, f):
                    continue

                change = {
                    'type': 'NEW_FILE',
                    'file': os.path.join(root, f).replace(env['repo101dir'] + os.sep, '')
                }

                self._exec(change)
        ####### added to create Image ################
        if self._module.config.get('visualization') == True :        
            print("Creating Image")
            folderName = str(self._module).replace("'","").split(" ")[1]
            path = self._env.get_env('views101dir')
            if(os.path.isdir(path + os.sep + folderName)):
                shutil.rmtree(path + os.sep + folderName)
            self._module.visualize(self._env)
        ##############################################

class AllFullSweepExecutor(Executor):

    def _exec(self):
        try:
            self._module.run(self._env)
        except:
            report_error(
                'module_failed',
                traceback.format_exc()
            )

    def run(self, changes):
        self._exec()
        ####### added to create Image ################
        if self._module.config.get('visualization') == True :        
            print("Creating Image")
            folderName = str(self._module).replace("'","").split(" ")[1]
            path = self._env.get_env('views101dir')
            if(os.path.isdir(path + os.sep + folderName)):
                shutil.rmtree(path + os.sep + folderName)
            self._module.visualize(self._env)
        ##############################################
