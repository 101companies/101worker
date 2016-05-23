import os
import json

def run(env, res):
    data = env.read_dump('locPerContribution')

    if data is None:
        data = {}

    f = res['file']
    if f.startswith('contributions' + os.sep):
        contribution = f.split(os.sep)[1]

        if data.get(contribution, None) is None:
            data[contribution] = 0

        data[contribution] += env.get_derived_resource(f, 'loc')

    env.write_dump('locPerContribution', data)
