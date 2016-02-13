from shovel import task
import os
import worker_lib

@task
def new_module(name):
    path = os.path.abspath('../modules/')
    path = os.path.join(path, name)
    os.mkdir(path)

    print 'created module ' + name + ' in ' + path

@task
def run():
    import pprint
    runner = worker_lib.Runner(worker_lib.env)
    runner.checkout_commit('83d4a5664a63fddcf0a4e464165fb5c71dd17e88')
    pprint.pprint(runner.pull_repo())

@task
def test():
    pass
