import os
import incremental101


def stripregex(pattern, default=None):
    if pattern.startswith("#") and pattern.endswith("#"):
        return pattern[1:len(pattern) - 1]
    return default


def tolist(thing):
    return thing if isinstance(thing, list) else [thing]


def diff(suffix, **switch):
    repodir   = os.environ[   "repo101dir"]
    targetdir = os.environ["targets101dir"]

    for op, path in incremental101.gendiff():
        if path.startswith(repodir):
            target = path.replace(repodir, targetdir, 1) + suffix
            switch[op](target  =target,
                       filename=path,
                       dirname =os.path.dirname(path)[len(repodir):],
                       basename=os.path.basename(path))
