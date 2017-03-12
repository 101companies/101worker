import os
import json
import logging
from .visualiser import create_piechart as c_piechart

def abs_path(path):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', path))

env = {
    'config101': abs_path('../101worker/configs/production.json'),
    'config101schema': abs_path('../101worker/schemas/config.schema.json'),
    'data101url': 'http://data.101companies.org/',
    'diffs101dir': abs_path('../101diffs'),
    'dumps101dir': abs_path('../101web/data/dumps'),
    'data101dir': abs_path('../101web/data'),
    'endpoint101url': 'http://101companies.org/endpoint/',
    'explorer101url': 'http://101companies.org/resources/',
    'extractor101dir': abs_path('../101worker/extractors'),
    'gatheredGeshi101dir': abs_path('../101results/geshi'),
    'gitdeps101dir': abs_path('../101results/gitdeps'),
    'gitdeps101url': 'http://101companies.org/pullRepo.json',
    'last101run': '0',
    'logs101dir': abs_path('../101logs'),
    'module101schema': abs_path( '../101worker/schemas/module.schema.json'),
    'modules101dir': abs_path('../101worker/modules'),
    'ontoDir': abs_path('../101web/data/onto'),
    'output101dir': abs_path('..'),
    'predicates101deps': abs_path('../101worker/modules/predicates101meta/module.json'),
    'predicates101dir': abs_path('../101worker/predicates'),
    'repo101dir': abs_path('../101results/101repo'),
    'repo101url': 'https://github.com/101companies/101repo',
    'results101dir': abs_path('../101results'),
    'targets101dir': abs_path('../101web/data/resources'),
    'temps101dir': abs_path('../101temps'),
    'themes101dir': abs_path('../101web/data/resources/themes'),
    'validator101dir': abs_path('../101worker/validators'),
    'views101dir': abs_path('../101web/data/views'),
    'web101dir': abs_path('../101web'),
    'wiki101url': 'http://101companies.org/wiki/',
    'worker101dir': abs_path('../101worker')
}

class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

def create_module_env(env, module=None):

    def get_env(key=None):
        if key:
            return env[key]
        else:
            return env

    def write_derived_resource(primary_resource, data, key):
        target = os.path.join(get_env('targets101dir'), primary_resource + '.' + key + '.json')

        if not os.path.exists(os.path.dirname(target)):
            os.makedirs(os.path.dirname(target))

        with open(target, 'w') as f:
            json.dump(data, f)

        logging.debug('Wrote derived resource %s', target)

    def remove_derived_resource(primary_resource, key):
        target = os.path.join(get_env('targets101dir'), primary_resource + '.' + key + '.json')
        if os.path.exists(target):
            os.remove(target)
        else:
            logging.warn('cant remove missing resource ' + primary_resource + key)

    def get_primary_resource(primary_resource):
        with open(os.path.join(get_env('repo101dir'), primary_resource), 'r') as f:
            return f.read()

    def get_derived_resource(primary_resource, key):
        path = os.path.join(get_env('targets101dir'), primary_resource + '.' + key + '.json')

        with open(path, 'r') as f:
            return json.load(f)

    def remove_dump(dump_name):
        target = os.path.join(get_env('dumps101dir'), dump_name + '.json')
        if os.path.exists(target):
            os.remove(target)
        else:
            logging.warn('Trying to delete non existing dump %s', target)

    def read_dump(dump_name):
        try:
            with open(os.path.join(get_env('dumps101dir'), dump_name + '.json'), 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return None

    def write_dump(dump_name, data):
        d = os.path.join(get_env('dumps101dir'), dump_name + '.json')
        with open(d, 'w') as f:
            json.dump(data, f, indent=4)
            logging.debug('Wrote dump %s at %s', dump_name, d)

    def create_piechart(name,xName,yName,xValue,yValue):
        c_piechart(name,xName,yName,xValue,yValue,get_env('views101dir'))

    return AttrDict({
        'get_env': get_env,
        'write_derived_resource': write_derived_resource,
        'remove_derived_resource': remove_derived_resource,
        'get_primary_resource': get_primary_resource,
        'read_dump': read_dump,
        'write_dump': write_dump,
        'get_derived_resource': get_derived_resource,
        'remove_dump': remove_dump,
        'create_piechart': create_piechart
    })
