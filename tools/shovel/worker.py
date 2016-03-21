from shovel import task
import os
import worker_lib as worker

@task
def new_module(name):
    '''
    Creates a new module with template.
    Usage: new_module [name]
    '''
    path = os.path.abspath('../modules/')
    path = os.path.join(path, name)
    os.mkdir(path)

    with open(os.path.join(path, '__init__.py'), 'w') as f:
        f.write('''
import os
import json

config = {
    'wantdiff': True,
    'threadsafe': False
}

def update_file(context, f):
    pass

def remove_file(context, f):
    pass

def run(context, change):

    if change['type'] == 'NEW_FILE':
        update_file(context, change['file'])

    elif change['type'] == 'FILE_CHANGED':
        update_file(context, change['file'])

    else:
        remove_file(context, change['file'])

def test():
    import TAP
    import TAP.Simple
    import StringIO

    t = TAP.Simple
    t.builder._plan = None

    t.plan(2)

    # write some tests

        ''')

    print 'created module ' + name + ' in ' + path

@task
def run():
    '''
    Runs the worker.

    Modules are defined env/production.json. This can be overriden as MODULE=SineModule
    Pulling Gitdeps can be ommited with OMIT_GITDEPS=1
    '''
    worker.runner.run(worker.env)

@task
def run_tests():
    worker.runner.run_tests(worker.env)

@task
def test():
    '''
    Same as run but resets the repo a few commits (integration testing purposes).
    '''
    repo = worker.runner.create_repo(worker.env)
    worker.runner.checkout_commit(repo, '83d4a5664a63fddcf0a4e464165fb5c71dd17e88')

    worker.runner.run(worker.env)
