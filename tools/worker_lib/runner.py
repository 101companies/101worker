from git import Repo
import json
import os
import imp
import sys
import traceback
import datetime
import time
import shutil
import sqlite3
from attrdict import AttrDict

# --------- LOGGING ---------------------

def create_logging_tables(connection):
    c = connection.cursor()
    # c.execute('drop table log_messages')
    c.execute('create table if not exists log_messages(type text, data text, ts timestamp)')

def report_error(db_connection, error_type, error_data):
    '''
    Logs an error to an internal dump.
    :param error_type: error name
    :param error_data: data for the error, e.g. stack trace
    '''
    c = db_connection.cursor()

    print error_type
    print error_data

    c.execute('insert into log_messages values (?, ?, ?)', (error_type, json.dumps(error_data), datetime.datetime.now()))
    db_connection.commit()

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
        except ImportError, e:
            print e
            failed.append(module)
            return None

    sys.path.append(os.path.abspath('../modules'))

    return [failed, filter(lambda x: x, map(load_module, modules))]

def init_storage_system(env):
    '''
    Initializes the storage system and creates database tables.
    '''
    db_path = env['temps101dir']
    connection = sqlite3.connect(os.path.join(db_path, 'db.sqlite'))
    create_logging_tables(connection)
    return connection

def create_module_env(env, module=None):

    def get_env(key):
        return env[key]

    def write_derived_resource(primary_resource, data, key):
        target = os.path.join(get_env('targets101dir'), primary_resource + key + '.json')

        if not os.path.exists(os.path.dirname(target)):
            os.makedirs(os.path.dirname(target))

        with open(target, 'w') as f:
            json.dump(data, f)

    def remove_derived_resource(primary_resource, key):
        target = os.path.join(get_env('targets101dir'), primary_resource + key + '.json')
        os.remove(target)

    def get_primary_resource(primary_resource):
        with open(os.path.join(get_env('repo101dir'), primary_resource), 'r') as f:
            return f.read()

    def read_dump(dump_name):
        try:
            with open(get_env(dump_name), 'r') as f:
                return json.load(f)
        except IOError:
            return None

    def write_dump(dump_name, data):
        with open(get_env(dump_name), 'w') as f:
            json.dump(data, f)

    return AttrDict({
        'get_env': get_env,
        'write_derived_resource': write_derived_resource,
        'remove_derived_resource': remove_derived_resource,
        'get_primary_resource': get_primary_resource,
        'read_dump': read_dump,
        'write_dump': write_dump
    })

def run(env):
    '''
    The worker main loop.
    At startup it initializes the "storage system".
    '''
    config = load_config()
    if os.environ['MODULE']:
        failed, modules = load_modules([os.environ['MODULE']])
    else:
        failed, modules = load_modules(config)

    db_connection = init_storage_system(env)

    if failed:
        report_error(
            db_connection,
            'module_load_failed',
            failed
        )

    repo = create_repo(env)
    changes = pull_repo(repo)

    if not os.environ['OMIT_GITDEPS']:
        # gitdeps
        gitdeps = load_gitdeps(env)
        gitdep_changes = pull_gitdeps(env, gitdeps)
        changes.extend(gitdep_changes)

        copy_gitdeps(gitdep_changes, env)

    for module in modules:
        print 'Running', module
        if module.config['wantdiff'] and not os.environ['FULL_SWEEP']:
            for change in changes:
                try:
                    module.run(create_module_env(env, module), change)
                except:
                    report_error(
                        db_connection,
                        'module_failed',
                        traceback.format_exc()
                    )
        else:
            print 'manual run'
            for root, dirs, files in os.walk(env['repo101dir']):
                for f in files:
                    module.run(create_module_env(env, module), {
                        'type': 'NEW_FILE',
                        'file': os.path.join(root, f)
                    })

    db_connection.close()

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
