import os
import incremental101


def stripregex(pattern, default=None):
    if pattern.startswith("#") and pattern.endswith("#"):
        return pattern[1:len(pattern) - 1]
    return default


def tolist(thing):
    return thing if isinstance(thing, list) else [thing]


def repodir():
    return os.environ["repo101dir"]

def targetsdir():
    return os.environ["targets101dir"]


def sourcetotarget(path):
    if path.startswith(repodir()):
        return targetsdir() + path[len(repodir()):]
    raise ValueError()


PRIMARY = 1
DERIVED = 2

def torelative(path, resources):
    if path.startswith(repodir()):
        return (path[len(repodir()) + 1:], PRIMARY)

    if path.startswith(targetsdir()):
        for r in resources:
            if path.endswith(r.suffix):
                return (path[len(targetsdir()) + 1:-len(r.suffix)], DERIVED)

    return (None, None)


def handlepath(suffix, callback, relative):
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
    metadata = map(lambda match: match["metadata"], matches)
    return [m[key] for m in metadata if key in m][0]
