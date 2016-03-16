"""
Various utility functions that are used in various places.
"""
import os
import incremental101


def stripregex(pattern, default=None):
    """
    Strips # characters from the beginning and end of a string. This is used
    for 101meta rules, which represent their regexen that way.

    If the given pattern starts and ends with a #, the string with those two
    characters stripped off is returned. Otherwise, the given default is
    returned instead.
    """
    if pattern.startswith("#") and pattern.endswith("#"):
        return pattern[1:len(pattern) - 1]
    return default


def tolist(thing):
    """
    Returns thing if it's a list, otherwise returns a list containing the thing.
    """
    return thing if isinstance(thing, list) else [thing]


def repodir():
    """
    Returns the repo101dir environment variable. Raises a KeyError if it
    doesn't exist.
    """
    return os.environ["repo101dir"]

def targetsdir():
    """
    Returns the targets101dir environment variable. Raises a KeyError if it
    doesn't exist.
    """
    return os.environ["targets101dir"]


def sourcetotarget(path):
    """
    Turns a given path in 101repo to a path in the targets directory. Raises
    a ValueError if the path isn't in 101repo.
    """
    if path.startswith(repodir()):
        return targetsdir() + path[len(repodir()):]
    raise ValueError()


PRIMARY = 1
DERIVED = 2

def torelative(path, resources):
    """
    Turns the given path into a relative path if it's a primary resource or a
    derived resource that matches one of the given resources.


    Parameters
    ----------
    path : string
        An absolute path to a file.

    resources : list of resource


    Returns
    -------
    A pair, with the first element being the relative path and the second being
    the constant PRIMARY or DERIVED, whichever the given path represents. If
    it's neither a primary nor a relevant secondary resource, (None, None) is
    returned.
    """
    if path.startswith(repodir()):
        return (path[len(repodir()) + 1:], PRIMARY)

    if path.startswith(targetsdir()):
        for r in resources:
            if path.endswith(r.suffix):
                return (path[len(targetsdir()) + 1:-len(r.suffix)], DERIVED)

    return (None, None)


def handlepath(suffix, callback, relative):
    """
    Builds the various **kwargs that all callbacks take from the given
    suffix(es) and relative path. Then calls the given callback with all of
    them. Catches ValueErrors raised by the callback.


    Parameters
    ----------
    suffix : string or list of string
        Suffixes of resources to be derived.

    callback : function(**kwargs)
        The callback to be called, in practice this is Deriver.onfile and
        Phase.onfile.

    relative : string
        The relative file path, as obtained by torelative.
    """
    try:
        filename   = os.path.join(   repodir(), relative)
        targetbase = os.path.join(targetsdir(), relative)

        if type(suffix) is not str:
            target = [targetbase + s for s in suffix]
        else:
            target = targetbase + suffix

        callback(target    =target,
                 targetbase=targetbase,
                 filename  =filename,
                 relative  =relative,
                 dirname   =os.path.dirname(filename)[len(repodir()) + 1:],
                 basename  =os.path.basename(filename))
    except ValueError:
        pass


def diff(suffix, resources, **switch):
    """
    Iterates over 101diff input using the incremental101 library and calls the
    given callbacks when appropriate. This handles changes in primary and
    relevant derived resources incrementally.


    Parameters
    ----------
    suffix : string or list of string
        Suffix(es) of the resources to be derived.

    resources : list of resource
        Resources that the current module depends on.

    switch : dict of function(**kwargs)
        A dict with callbacks with the keys "A", "M" and "D", for added,
        modified and deleted files respecitvely. In practice, these are onfile
        and ondelete in Deriver and Phase.
    """
    raise

    primary = set()
    derived = set()

    for op, path in incremental101.eachdiff():
        relative, kind = torelative(path, resources)
        if not relative:
            continue

        todo_primary = relative not in primary
        todo_derived = relative not in derived

        if kind == PRIMARY:
            if todo_primary and (op == "D" or todo_derived):
                if op in switch:
                    handlepath(suffix, switch[op], relative)
                primary.add(relative)

        elif kind == DERIVED:
            if todo_primary and todo_derived:
                if "M" in switch:
                    handlepath(suffix, switch["M"], relative)
                derived.add(relative)


def walk(suffix, callback):
    """
    Walks the entire 101repo and re-derives all files. Ignores any directories
    called .git, because nobody cares about deriving from their contents. If
    an error occurs during the file system walk, it is propagated.


    Parameters
    ----------
    suffix : string or list of string
        Suffix(es) of the resources to be derived.

    callback : function(**kwargs)
        The function to be called on each relevant path. In practice, this is
        Deriver.onfile and Phase.onfile.
    """
    def err(e):
        raise e

    for root, dirs, files in os.walk(repodir(), onerror=err, followlinks=True):
        try:
            dirs.remove(".git")
        except ValueError:
            pass

        for f in files:
            relative = os.path.join(root, f)[len(repodir()) + 1:]
            handlepath(suffix, callback, relative)


def valuebykey(key, matches):
    """
    This is the default getvalue callback for the deriver. It returns the first
    metadata unit from the given matches that is equal to the given key. Raises
    a KeyError if there's no such unit.
    """
    metadata = [match["metadata"] for match in matches]
    return [m[key] for m in metadata if key in m][0]
