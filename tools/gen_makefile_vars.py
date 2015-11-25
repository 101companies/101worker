#!/usr/bin/python

import json
import os
from subprocess import Popen, PIPE

process = Popen([
    'tools/loadenv',
    'configs/env/production.yml'], stdout=PIPE)
(output, err) = process.communicate()
exit_code = process.wait()

output = json.loads(output)

def gen_var(name, value):
    return "{}={}".format(name, value)

def gen_makefile(vars):
    for key, value in vars.iteritems():
        yield gen_var(key, value)

with open('modules/Makefile.vars', 'w') as f:
    for line in gen_makefile(output):
        f.write(line + '\n')
    f.write('export\n')
