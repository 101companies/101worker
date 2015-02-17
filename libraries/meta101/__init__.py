import json
import os
import incremental101
from .Phase      import Phase
from .Matches    import Matches
from .Predicates import Predicates
from .Fragments  import Fragments
from .Deriver    import Deriver


def getphase(key):
    phases = {
        "matches"    : Matches,
        "predicates" : Predicates,
        "fragments"  : Fragments,
    }
    if key not in phases:
        raise RuntimeError("invalid phase: {}".format(key))
    return phases[key]


def matchall(phasekey, force=False):
    dumpfile   = os.environ[phasekey + "101dump"]
    rulesfile  = os.environ["rules101dump"]
    entirerepo = False
    matches    = []

    if os.path.exists(dumpfile):
        entirerepo = os.path.getmtime(rulesfile) > os.path.getmtime(dumpfile)
        with open(dumpfile) as f:
            matches = json.load(f)["matches"]

    with open(rulesfile) as f:
        rules = json.load(f)["results"]["rules"]

    dump = getphase(phasekey)(rules, matches).run(entirerepo or force)
    incremental101.writejson(dumpfile, dump)


def derive(*args, **kwargs):
    return Deriver(*args, **kwargs).derive()
