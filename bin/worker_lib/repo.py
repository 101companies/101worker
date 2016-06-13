from git import Repo
import git

import shutil
import os
import json

def convert_diff(diff):
    file_1 = diff.a_path
    file_2 = diff.b_path

    if diff.a_mode == 0 and diff.a_blob is None:
        return { 'type': 'DELETED_FILE', 'file': file_2 }

    elif diff.b_mode == 0 and diff.b_blob is None:
        return { 'type': 'NEW_FILE', 'file': file_1 }

    else:
        return { 'type': 'FILE_CHANGED', 'file': file_1 }

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
            return list(pull_repo(repo))
        else:
            try:
                print(dep['sourcerepo'])
                repo = Repo.clone_from(dep['sourcerepo'], path, branch='master')
                result = []
                for root, dirnames, filenames in os.walk(path):
                    for f in filenames:
                        f = os.path.join(root, f).replace(env['gitdeps101dir'], '')[1:]
                        if '.git/' in f:
                            continue
                        result.append({ 'type': 'NEW_FILE', 'file':  f})
                return result
            except git.exc.GitCommandError:
                return []

    return sum(list(map(pull_gitdep, gitdeps)), [])

def load_gitdeps(env):
    with open(os.path.abspath(os.path.join(env['repo101dir'], '.gitdeps'))) as f:
        return json.load(f)

def pull_repo(repo):
    base_commit = repo.head.commit.hexsha
    info = repo.remotes.origin.pull('master')[0]
    diffs = info.commit.diff(base_commit)
    return list(map(lambda diff: convert_diff(diff), diffs))

def create_repo(env):
    try:
        return Repo(env['repo101dir'])
    except git.exc.InvalidGitRepositoryError:
        return Repo.clone_from('https://github.com/101companies/101repo.git', env['repo101dir'], branch='master')

def checkout_commit(repo, commit):
    repo.git.checkout(commit)

def history(repo, commit):
    return repo.iter_commits(commit)
