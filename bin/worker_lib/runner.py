import json
import os
import imp
import sys
import traceback
import datetime
import time
import shutil
from logger import report_error

from .repo import *
from .env import create_module_env
from .executor import *

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
    repo = create_repo(env)
    changes = pull_repo(repo)
    # changes = []

    if not os.environ.get('OMIT_GITDEPS'):
        # gitdeps
        gitdeps = load_gitdeps(env)
        gitdep_changes = pull_gitdeps(env, gitdeps)
        changes.extend(gitdep_changes)

        copy_gitdeps(gitdep_changes, env)

    for module in modules:
        executor = get_executor(module)
        executor.run(changes)

def run_tests(env):
    config = load_config()
    failed, modules = load_modules(config)

    context = {
        'env': env
    }

    for module in modules:
        module.test()
