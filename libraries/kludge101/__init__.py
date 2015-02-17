"""
Kludge for code injection vulnerabilities until validators, extractors and
friends are fixed.
"""
import os
import warnings


warnings.warn("kludge101 is a kludge. Fix extractors, validators "
              "and friends to avoid code injection properly.")


def checkpath(relpath):
    """
    Ensures that the given path relative to 101repo is actually in 101repo and
    not actually in gitdeps or somewhere else. This is a kludge for what is a
    bad idea in the first place.

    Returns an absolute path to the given relative path if it was deemed safe.
    Otherwise returns none.

    The way this works is that it turns the relative path absolute and then
    checks if it's still in 101repo. If it's not, the path had .. in it and
    is not safe.

    Then the entire path starting from the 101repo directory is checked for
    links. If a link is found, it is assumed to be unsafe since it probably
    points to gitdeps.
    """
    repo101dir = os.environ["repo101dir"]
    path       = os.path.abspath(os.path.join(repo101dir, relpath))

    if not path.startswith(repo101dir):
        return None

    dirs = path
    while len(dirs) > len(repo101dir):
        if os.path.islink(dirs):
            return None
        dirs = os.path.dirname(dirs)

    return path
