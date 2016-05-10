import os
import json

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
    'extractor101dump': abs_path('../101web/data/dumps/extractor.json'),
    'fragmentMetrics101dump': abs_path('../101web/data/dumps/fragments.metrics.json'),
    'fragments101dump': abs_path('../101web/data/dumps/fragments.json'),
    'gatheredGeshi101dir': abs_path('../101results/geshi'),
    'geshi101dump': abs_path('../101web/data/dumps/geshi.json'),
    'gitdeps101dir': abs_path('../101results/gitdeps'),
    'gitdeps101url': 'http://101companies.org/pullRepo.json',
    'imports101dump': abs_path('../101web/data/dumps/imports.json'),
    'last101run': '0',
    'logs101dir': abs_path('../101logs'),
    'matches101dump': abs_path('../101web/data/dumps/matches.json'),
    'metrics101dump': abs_path('../101web/data/dumps/metrics.json'),
    'module101schema': abs_path( '../101worker/schemas/module.schema.json'),
    'moduleSummary101dump': abs_path('../101web/data/dumps/ModuleSummaryDump.json'),
    'moduleSummary101temp': abs_path('../101web/data/dumps/tempModuleSummaryDump.json'),
    'modules101dir': abs_path('../101worker/modules'),
    'ontoDir': abs_path('../101web/data/onto'),
    'output101dir': abs_path('..'),
    'predicates101deps': abs_path('../101worker/modules/predicates101meta/module.json'),
    'predicates101dir': abs_path('../101worker/predicates'),
    'predicates101dump': abs_path('../101web/data/dumps/predicates.json'),
    'pullRepo101dump': abs_path('../101web/data/dumps/PullRepo.json'),
    'repo101dir': abs_path('../101results/101repo'),
    'repo101url': 'https://github.com/101companies/101repo',
    'resolution101dump': abs_path('../101web/data/dumps/resolution.json'),
    'results101dir': abs_path('../101results'),
    'rules101dump': abs_path('../101web/data/dumps/rules.json'),
    'suffixes101dump': abs_path('../101web/data/dumps/suffixes.json'),
    'summary101dump': abs_path('../101web/data/dumps/summary.json'),
    'targets101dir': abs_path('../101web/data/resources'),
    'temps101dir': abs_path('../101temps'),
    'themes101dir': abs_path('../101web/data/resources/themes'),
    'validator101dir': abs_path('../101worker/validators'),
    'validator101dump': abs_path('../101web/data/dumps/validator.json'),
    'views101dir': abs_path('../101web/data/views'),
    'web101dir': abs_path('../101web'),
    'wiki101dump': abs_path('../101web/data/dumps/wiki.json'),
    'wiki101url': 'http://101companies.org/wiki/',
    'worker101dir': abs_path('../101worker'),
    'locPerContribution': abs_path('../101web/data/dumps/locPerContribution.json'),
    'mostUsedLanguages': abs_path('../101web/data/dumps/mostUsedLanguages.json')
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
            print('cant remove missing resource ' + primary_resource + key)

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
        except FileNotFoundError:
            return None

    def write_dump(dump_name, data):
        with open(get_env(dump_name), 'w') as f:
            json.dump(data, f, indent=4)

    return AttrDict({
        'get_env': get_env,
        'write_derived_resource': write_derived_resource,
        'remove_derived_resource': remove_derived_resource,
        'get_primary_resource': get_primary_resource,
        'read_dump': read_dump,
        'write_dump': write_dump,
        'get_derived_resource': get_derived_resource
    })
