import os
import json

env = {
    'config101': os.path.abspath('../101worker/configs/production.json'),
    'config101schema': os.path.abspath('../101worker/schemas/config.schema.json'),
    'data101url': 'http://data.101companies.org/',
    'diffs101dir': os.path.abspath('../101diffs'),
    'dumps101dir': os.path.abspath('../101web/data/dumps'),
    'data101dir': os.path.abspath('../101web/data'),
    'endpoint101url': 'http://101companies.org/endpoint/',
    'explorer101url': 'http://101companies.org/resources/',
    'extractor101dir': os.path.abspath('../101worker/extractors'),
    'extractor101dump': os.path.abspath('../101web/data/dumps/extractor.json'),
    'fragmentMetrics101dump': os.path.abspath('../101web/data/dumps/fragments.metrics.json'),
    'fragments101dump': os.path.abspath('../101web/data/dumps/fragments.json'),
    'gatheredGeshi101dir': os.path.abspath('../101results/geshi'),
    'geshi101dump': os.path.abspath('../101web/data/dumps/geshi.json'),
    'gitdeps101dir': os.path.abspath('../101results/gitdeps'),
    'gitdeps101url': 'http://101companies.org/pullRepo.json',
    'imports101dump': os.path.abspath('../101web/data/dumps/imports.json'),
    'last101run': '0',
    'logs101dir': os.path.abspath('../101logs'),
    'matches101dump': os.path.abspath('../101web/data/dumps/matches.json'),
    'metrics101dump': os.path.abspath('../101web/data/dumps/metrics.json'),
    'module101schema':os.path.abspath( '../101worker/schemas/module.schema.json'),
    'moduleSummary101dump': os.path.abspath('../101web/data/dumps/ModuleSummaryDump.json'),
    'moduleSummary101temp': os.path.abspath('../101web/data/dumps/tempModuleSummaryDump.json'),
    'modules101dir': os.path.abspath('../101worker/modules'),
    'ontoDir': os.path.abspath('../101web/data/onto'),
    'output101dir': os.path.abspath('..'),
    'predicates101deps': os.path.abspath('../101worker/modules/predicates101meta/module.json'),
    'predicates101dir': os.path.abspath('../101worker/predicates'),
    'predicates101dump': os.path.abspath('../101web/data/dumps/predicates.json'),
    'pullRepo101dump': os.path.abspath('../101web/data/dumps/PullRepo.json'),
    'repo101dir': os.path.abspath('../101results/101repo'),
    'repo101url': 'https://github.com/101companies/101repo',
    'resolution101dump': os.path.abspath('../101web/data/dumps/resolution.json'),
    'results101dir': os.path.abspath('../101results'),
    'rules101dump': os.path.abspath('../101web/data/dumps/rules.json'),
    'suffixes101dump': os.path.abspath('../101web/data/dumps/suffixes.json'),
    'summary101dump': os.path.abspath('../101web/data/dumps/summary.json'),
    'targets101dir': os.path.abspath('../101web/data/resources'),
    'temps101dir': os.path.abspath('../101temps'),
    'themes101dir': os.path.abspath('../101web/data/resources/themes'),
    'validator101dir': os.path.abspath('../101worker/validators'),
    'validator101dump': os.path.abspath('../101web/data/dumps/validator.json'),
    'views101dir': os.path.abspath('../101web/data/views'),
    'web101dir': os.path.abspath('../101web'),
    'wiki101dump': os.path.abspath('../101web/data/dumps/wiki.json'),
    'wiki101url': 'http://101companies.org/wiki/',
    'worker101dir': os.path.abspath('../101worker')
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
        target = os.path.join(get_env('targets101dir'), primary_resource + key + '.json')

        if not os.path.exists(os.path.dirname(target)):
            os.makedirs(os.path.dirname(target))

        with open(target, 'w') as f:
            json.dump(data, f)

    def remove_derived_resource(primary_resource, key):
        target = os.path.join(get_env('targets101dir'), primary_resource + key + '.json')
        if os.path.exists(target):
            os.remove(target)
        else:
            print 'cant remove missing resource ' + primary_resource + key

    def get_primary_resource(primary_resource):
        with open(os.path.join(get_env('repo101dir'), primary_resource), 'r') as f:
            return f.read()

    def get_derived_resource(primary_resource, key):
        path = os.path.join(get_env('targets101dir'), primary_resource + key + '.json')

        with open(path, 'r') as f:
            return json.load(f)

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
        'write_dump': write_dump,
        'get_derived_resource': get_derived_resource
    })
