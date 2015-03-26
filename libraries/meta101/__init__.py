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

    This will derive all files incrementally automatically. You need to run
    rules101meta to have the rules dump available and have an environment
    variable called "phase101dump", where phase is the name of your matching
    phase. That's where the dump will be written to.


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
    Phase : the base class for all the matching phases
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
    derived before. Please only use keyword arguments (name=value) when you
    call this function.

    This library will take care of incrementality for you, and will only bother
    you with files or derived resources that have changed. If a file gets
    deleted and you derived a resource from it earlier, the resource will get
    deleted for you.

    This thing is a bit complicated, but just have a look at the modules that
    use it to see what's going on and maybe cargo-cult a bit. The parameters
    will tell you where to look for examples for each of them.


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
        Preprocess a value before your callback is called.

        If this is a string, it will get the first metadata unit from the
        .matches.json file with that key. If there's no such unit, the file
        is skipped.

        Alternatively, you can supply a callback function that does more
        complicated things. The function can return any value, which will then
        be passed to your callback. If you want to skip the file, you must
        raise any Exception. If you want to bail out totally with a fatal error,
        raise an Error that isn't an instance of Exception, such as a
        SystemExit.

        For the **kwargs parameters, see below.

        Examples: validate101meta (uses "validator" string key),
                  fragmentMetrics101meta (uses a callback function),
                  summary101meta (just always returns True)

    callback : function(deriver, value, **kwargs)
        The function that produces the derived value. The value parameter will
        be whatever is returned by the getvalue function.

        If you gave multiple suffixes, this function must return a tuple of
        values, one for each suffix. If you only have one suffix, you don't
        need to wrap the return in a tuple.

        You can return different types from this functions:

        * If you return a string, it will just be written to the derived
          resource file.

        * If you return a dict or a list, it will be JSON encoded and then
          written to the derived resource file.

        * If you return None, nothing will be derived. If an earlier derived
          resource exists, it'll be deleted.

        * If you return anything else, your module will blow up. Don't do that.

        For the **kwargs parameters, see below.

        Examples: validate101meta (returns a single value),
                  fragmentMetrics101meta (returns two values)

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
        Which resources you want to derive from. See meta101.resources for more
        info about which kinds of resources exist. Defaults to a decoded JSON
        of the 101meta matches.

        Examples: fragmentMetrics (derives from two resources), summary101meta
                  (derives from a bunch of resources).

    entirerepo : optional, bool
        Force that incrementality be ignored and walk over the entire 101repo
        instead, re-deriving all files. This is useful if a module has changed
        for example. Defaults to False.

        Examples: validate101meta, summary101meta - both of them just use
                  the havechanged function.


    **kwargs
    --------
    The getvalue and callback functions receive a bunch of keyword arguments
    when they're called. You definitely won't need all of them, so you'll want
    to put **kwargs at the end of your function signature to slurp up those
    unneeded arguments and only provide names for the ones you want to use.

    The following arguments are passed that way:

    filename
        The absolute path to the primary resource.

    relative
        The path to the primary resource, relative to repo101dir.

    basename
        The primary resource's file name without any directories.

    dirname
        The primary resource's directory name, without the basename,
        relative to repo101dir.

    resources
        Either a single loaded resource or a list of loaded resources,
        depending on what you passed as the resources parameter to derive.

    target
        Either a single absolute path to the resource to be derived or a
        list of them, depending on what you passed as the suffix parameter
        to derive.

    targetbase
        The name of the resource to be derived, without any additional
        suffix.

    Examples: validate101meta (derive uses filename),
              summary101meta (getvalue slurps everything, derive uses resources)


    See Also
    --------
    Deriver : class that handles all the actual deriving
    resource : types of resources to derive from
    """
    return Deriver(**kwargs).run(entirerepo)
