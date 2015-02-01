import json
import os
from Basics     import Basics
from Predicates import Predicates
from Fragments  import Fragments


def getphase(key):
    phases = {
        "basics"     : Basics,
        "predicates" : Predicates,
        "fragments"  : Fragments,
    }
    if key not in phases:
        raise RuntimeError("invalid phase: {}".format(key))
    return phases[key]


def matchall(phasekey):
    with open(os.env['rulesDump101']) as f:
        rules = json.load(f)["results"]["rules"]
    return getphase(phasekey)(rules).run()


def tolist(thing):
    return thing if isinstance(thing, list) else [thing]


def stripregex(pattern, default=None):
    if pattern.startswith("#") and pattern.endswith("#"):
        return pattern[1:len(pattern) - 2]
    return default
