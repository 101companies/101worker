import os
import incremental101


def stripregex(pattern, default=None):
    if pattern.startswith("#") and pattern.endswith("#"):
        return pattern[1:len(pattern) - 1]
    return default


def tolist(thing):
    return thing if isinstance(thing, list) else [thing]


def sourcetotarget(path):
    if not hasattr(sourcetotarget, "dirs"):
        sourcetotarget.dirs = (os.environ[   "repo101dir"],
                               os.environ["targets101dir"])
    repodir, targetdir = sourcetotarget.dirs

    if path.startswith(repodir):
        return targetdir + path[len(repodir):]

    raise ValueError()


def diff(suffix, **switch):
    for op, path in incremental101.gendiff():
        try:
            target = sourcetotarget(path) + suffix
            switch[op](target  =target,
                       filename=path,
                       dirname =os.path.dirname(path),
                       basename=os.path.basename(path))
        except ValueError:
            pass
