from shovel import task
import os
import worker_lib as worker

@task
def new_module(name):
    path = os.path.abspath('../modules/')
    path = os.path.join(path, name)
    os.mkdir(path)

    print 'created module ' + name + ' in ' + path

@task
def run():
    worker.runner.run(worker.env)

@task
def run_tests():
    worker.runner.run_tests(worker.env)

@task
def test():
    repo = worker.runner.create_repo(worker.env)
    worker.runner.checkout_commit(repo, '83d4a5664a63fddcf0a4e464165fb5c71dd17e88')

    worker.runner.run(worker.env)
