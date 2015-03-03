"""
101meta library for matching and deriving resources.

Essentially only the functions of this file are the interface to the outside
world, the two main functions being matchall and derive. Look at their
respective documentation for detail. Please don't mess with the guts from the
outside, if possible.

This is a rewrite of the old 101meta library at 101worker/libraries/101meta.
That library is now depecated. Virtually all of its functionality has been
folded into matchall and derive, while the const101meta part of it has been
replaced by environment variables.
"""
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
    """
    Returns the class that matches the given phase name. Raises a RuntimeError
    if there's no matching class.
    """
    phases = {
        "matches"    : Matches,
        "predicates" : Predicates,
        "fragments"  : Fragments,
    }
    if key not in phases:
        raise RuntimeError("invalid phase: {}".format(key))
    return phases[key]



def havechanged(*files):
    """
    Checks if any of the given files have changed since the last 101worker run,
    as determined by the last101run environment variable, defaulting to 0 in
    Unix time. A missing file is treated as not having changed.


    Parameters
    ----------
    *files : string
        Varargs of file paths to be checked. You can call this like
        havechanged(file1, file2, file3) or via havechanged(*list_or_tuple).


    Returns
    -------
    bool : True if any of the given files have changed, False otherwise.
    """
    since = float(os.environ.get("last101run", 0))
    return any(os.path.exists(f) and since < os.path.getmtime(f) for f in files)



def matchall(phasekey, entirerepo=False):
    """
    Run 101meta rule matching for a given phase.

    TODO


    Parameters
    ----------
    phasekey : string
        The name of the matching phase to be run. At the time of writing, this
        may be "matches", "predicates" or "fragments".

    entirerepo : optional, bool
        Force that incrementality be ignored and walk over the entire 101repo
        instead, re-matching all files. This is useful if a module has changed
        for example. Defaults to False.


    See Also
    --------
    getphase : where the phasekey gets passed to
    havechanged : for checking if you should set entirerepo to True
    """
    dumpfile  = os.environ[phasekey + "101dump"]
    rulesfile = os.environ["rules101dump"]
    changed   = havechanged(rulesfile)
    args      = []

    if os.path.exists(dumpfile):
        with open(dumpfile) as f:
            dump = json.load(f)
            args.append(dump["matches" ])
            args.append(dump["failures"])

    with open(rulesfile) as f:
        args.insert(0, json.load(f)["results"]["rules"])

    dump = getphase(phasekey)(*args).run(changed or entirerepo)
    incremental101.writejson(dumpfile, dump)



def derive(entirerepo=False, **kwargs):
    """
    Derive resources from other resources, which in turn might have been
    derived before.

    This thing is a bit complicated, but just have a look at the modules that
    use it to see what's going on and maybe cargo-cult a bit. The parameters
    will tell you where to look for examples for each of them.

    Please only use keyword arguments (name=value) when you call this function.


    Parameters
    ----------
    suffix : string or list of string
        The suffix(es) of the files you want to generate. If you give a list
        of values here, your callback function has to return a tuple of the
        same length.

        Examples: validate101meta for a single suffix, metrics101meta for
                  multiple ones.

    dump : string
        The name of your dump file. You should pull this from an environment
        variable, not just hard-code it. This is the file that your dump will
        be loaded from and saved to. If the file doesn't exist yet, it'll
        default to this dict: {"problems" : {}}.

        Use the oninit callback to extend your dump after loading it and the
        ondump callback to prepare it before it gets saved to JSON.

        Examples: summary101meta, validate101meta.

    getvalue : optional, string or function(deriver, **kwargs)
        ...

    callback : function(deriver, value, **kwargs)
        ...

    oninit : optional, function(deriver)
        Callback that is called after the Deriver is constructed and the dump
        is loaded. You can use this to extend your dump to include more than
        just problems.

        Examples: validate101meta (adds a validators key),
                  fragmentMetrics101meta (adds geshicodes and extractors key)

    ondump : optional, function(deriver)
        Callback that is called right before the dump is converted into JSON
        and written out. You can use this if you have data in your dump that
        can't be represented in JSON, like sets or specific objects.

        Examples: validate101meta, fragmentMetrics101meta - they both convert
                  the sets in their dumps to lists.

    resources : optional, resource or list of resource
        ...

    entirerepo : optional, bool
        Force that incrementality be ignored and walk over the entire 101repo
        instead, re-deriving all files. This is useful if a module has changed
        for example. Defaults to False.

        Examples: validate101meta, summary101meta - both of them just use
                  the havechanged function.
    """
    return Deriver(**kwargs).run(entirerepo)
