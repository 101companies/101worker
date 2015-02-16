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


def sourcetotarget(path):
    targetdir = os.environ["targets101dir"]

    if path.startswith(repodir()):
        return targetdir + path[len(repodir()):]

    raise ValueError()


def handlepath(suffix, callback, path):
    try:
        targetbase = sourcetotarget(path)

        if type(suffix) is not str:
            target = [targetbase + s for s in suffix]
        else:
            target = targetbase + suffix

        callback(target    =target,
                 targetbase=targetbase,
                 filename  =path,
                 relative  =path[len(repodir()) + 1:],
                 dirname   =os.path.dirname(path)[len(repodir()) + 1:],
                 basename  =os.path.basename(path))
    except ValueError:
        pass


def diff(suffix, **switch):
    for op, path in incremental101.eachdiff():
        if op in switch:
            handlepath(suffix, switch[op], path)


def walk(suffix, callback):
    for root, dirs, files in os.walk(repodir(), followlinks=True):
        try:
            dirs.remove(".git")
        except ValueError:
            pass

        for f in files:
            handlepath(suffix, callback, os.path.join(root, f))


def valuebykey(deriver, matches, **kwargs):
    metadata = map(lambda match: match["metadata"], matches)
    return [m[deriver.key] for m in metadata if deriver.key in m][0]
