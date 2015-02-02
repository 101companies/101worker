import json
import os
from Phase      import Phase
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
    with open(os.environ['rulesDump101']) as f:
        rules = json.load(f)["results"]["rules"]
    return getphase(phasekey)(rules).run()
