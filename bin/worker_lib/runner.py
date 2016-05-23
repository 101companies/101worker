import json
import os
import imp
import sys
import traceback
import datetime
import time
import shutil
import logging
from .logger import report_error

from .repo import *
from .env import create_module_env, env
from .executor import *

def delete_dumps_for_module(module):
    if module.config.get('behavior', None) and module.config['behavior'].get('creates', None):
        creates = module.config['behavior']['creates']
        for creation in creates:
            if creation[0] == 'dump':
                ctx = create_module_env(env, module)
                logging.debug('deleting dump %s', creation[1])
                ctx.remove_dump(creation[1])

def get_executor(module):
    value = [os.environ.get('FULL_SWEEP', 0) == 1, module.config.get('wantdiff', False), module.config.get('wantsfiles', False)]

    if os.environ.get('FULL_SWEEP', 0) == '1':
        if module.config.get('wantsfiles', False):
            return FileFullSweepExecutor(module)
        else:
            return AllFullSweepExecutor(module)

    else:
        if module.config['wantdiff']:
            return Executor(module)
        elif module.config.get('wantsfiles', False):
            return FileFullSweepExecutor(module)
        else:
            return AllFullSweepExecutor(module)


def run(modules, env):
    '''
    The worker main loop.
    '''
    if not os.environ.get('OMIT_PULL'):
        repo = create_repo(env)
        changes = pull_repo(repo)
    else:
        changes = []

    if not os.environ.get('OMIT_GITDEPS'):
        # gitdeps
        gitdeps = load_gitdeps(env)
        gitdep_changes = pull_gitdeps(env, gitdeps)
        changes.extend(gitdep_changes)

        copy_gitdeps(gitdep_changes, env)

    for module in modules:
        executor = get_executor(module)
        executor.run(changes)

def run_tests(modules):
    for module in modules:
        module.test()
