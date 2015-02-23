import json
import os
import incremental101
from .Phase      import Phase
from .Matches    import Matches
from .Predicates import Predicates
from .Fragments  import Fragments
from .Deriver    import Deriver
from .util       import valuebykey


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
    args       = []

    if os.path.exists(dumpfile):
        entirerepo = os.path.getmtime(rulesfile) > os.path.getmtime(dumpfile)
        with open(dumpfile) as f:
            dump = json.load(f)
            args.append(dump["matches" ])
            args.append(dump["failures"])

    with open(rulesfile) as f:
        args.insert(0, json.load(f)["results"]["rules"])

    dump = getphase(phasekey)(*args).run(entirerepo or force)
    incremental101.writejson(dumpfile, dump)


def derive(suffix, dump, callback, oninit=None, ondump=None,
           getvalue=valuebykey, key=None, resources=None, force=False):
    return Deriver(suffix, dump, callback, oninit,
                   ondump, getvalue, key, resources).run(force)
