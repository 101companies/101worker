"""
Checks if one of the given libraries appears in a ``using'' statement,
similar to dotNetImport.sh from 101repo.
"""
import re

def run(filePath, args):
    opts  = "|".join(map(re.escape, args))
    regex = re.compile("^\s*using\s+(" + opts + ")\.")
    with open(filePath) as f:
        return any(regex.match(line) for line in f)
