"""
Checks if one of the given libraries appears in a ``using'' statement,
similar to javaImport.sh from 101repo.
"""
import re

def run(filename, *args):
    opts  = "|".join(map(re.escape, args))
    regex = re.compile("^\s*import\s+(" + opts + ")\.")
    with open(filename) as f:
        return any(regex.match(line) for line in f)
