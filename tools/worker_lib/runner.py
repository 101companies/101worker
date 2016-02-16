from git import Repo
import json
import os
import imp
import sys
import traceback
import datetime
import time
import shutil

def report_error(error):
    print error

    path = os.path.abspath('../../101logs/worker.log')
    if os.path.exists(path):
        with open(path, 'r') as f:
            data = json.load(f)
    else:
        data = []

    ts = time.time()
    error['timestamp'] = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    data.append(error)
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)

def convert_diff(diff):
    file_1 = diff.a_path
    file_2 = diff.b_path

    if diff.a_mode == 0 and diff.a_blob is None:
        return { 'type': 'DELETED_FILE', 'file': file_2 }

    elif diff.b_mode == 0 and diff.b_blob is None:
        return { 'type': 'NEW_FILE', 'file': file_1 }

    else:
        return { 'type': 'FILE_CHANGED', 'file': file_1 }

def load_config():
    with open('../configs/production.json') as f:
        return json.load(f)

def load_modules(modules):
    failed = []
    def load_module(module):
        try:
            return __import__(module)
        except ImportError:
            failed.append(module)
            return None

    sys.path.append(os.path.abspath('../modules'))

    return [failed, filter(lambda x: x, map(load_module, modules))]

def run(env):
    config = load_config()
    failed, modules = load_modules(config)

    if failed:
        report_error({
            'type': 'module_load_failed',
            'data': failed
        })

    repo = create_repo(env)
    changes = pull_repo(repo)

    # gitdeps
    gitdeps = load_gitdeps(env)
    gitdep_changes = pull_gitdeps(env, gitdeps)
    changes.extend(gitdep_changes)

    copy_gitdeps(gitdep_changes, env)

    context = {
        'env': env
    }

    for module in modules:
        print 'Running', module
        if module.config['wantdiff']:
            for change in changes:
                try:
                    module.run(context, change)
                except:
                    report_error({
                        'type': 'module_failed',
                        'data': [traceback.format_exc()]
                    })
        else:
            module.run(context)

def run_tests(env):
    config = load_config()
    failed, modules = load_modules(config)

    context = {
        'env': env
    }

    for module in modules:
        module.test()

def copy_gitdeps(changes, env):
    for change in changes:
        if change['type'] == 'NEW_FILE':
            target_file = os.path.join(env['repo101dir'], '/'.join(change['file'].split('/')[2:]))
            dirname = os.path.dirname(target_file)
            if not os.path.exists(dirname):
                os.makedirs(dirname)

            source_file = os.path.join(env['gitdeps101dir'], change['file'])

            shutil.copyfile(source_file, target_file)

def pull_gitdeps(env, gitdeps):
    def pull_gitdep(dep):
        user = dep['sourcerepo'].split('/')[-2]
        filename = dep['sourcerepo'].split('/')[-1].replace('.git', '')
        path = os.path.join(env['gitdeps101dir'], user, filename)
        if os.path.exists(os.path.join(path, '.git')):
            repo = Repo(path)
            return pull_repo(repo)
        else:
            repo = Repo.clone_from(dep['sourcerepo'], path, branch='master')
            result = []
            for root, dirnames, filenames in os.walk(path):
                for f in filenames:
                    f = os.path.join(root, f).replace(env['gitdeps101dir'], '')[1:]
                    if '.git/' in f:
                        continue
                    result.append({ 'type': 'NEW_FILE', 'file':  f})
            return result


    return sum(map(pull_gitdep, gitdeps), [])

def load_gitdeps(env):
    with open(os.path.abspath(os.path.join(env['repo101dir'], '.gitdeps'))) as f:
        return json.load(f)

def pull_repo(repo):
    base_commit = repo.head.commit.hexsha
    info = repo.remotes.origin.pull('master')[0]
    diffs = info.commit.diff(base_commit)
    return map(lambda diff: convert_diff(diff), diffs)

def create_repo(env):
    return Repo(env['repo101dir'])

def checkout_commit(repo, commit):
    repo.git.checkout(commit)

def history(repo, commit):
    return repo.iter_commits(commit)
