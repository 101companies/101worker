import os
import json

config = {
    'wantdiff': False,
    'wantsfiles': False,
    'threadsafe': True
}

def run(env):
    base = os.path.join(env.get_env('repo101dir'), 'contributions')
    output = env.get_env('targets101dir')

    for c in os.listdir(base):
        loc = 0
        for root, dirs, files in os.walk(os.path.join(base, c)):
            for f in files:
                source_file = os.path.join(root, f).replace(base + '/', 'contributions/')
                loc += (env.get_derived_resource(source_file, '.loc'))

        with open(os.path.join(output, 'contributions', c + '.module_loc.json'), 'w') as f:
            json.dump(loc, f)

def test():
    pass
