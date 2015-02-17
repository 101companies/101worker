import os
from   TAP.Simple import *
import kludge101

plan(6)

repodir = os.path.abspath("t/101repo")

def path_ok(path, comment):
    result = kludge101.checkpath(path)
    eq_ok(kludge101.checkpath(path), os.path.join(repodir, path), comment)

def path_not_ok(path, comment):
    is_ok(kludge101.checkpath(path), None, comment)


os.environ["repo101dir"] = repodir

path_ok(    "contributions/regular/extractor.py",
            "regular path is fine")

path_ok(    "contributions/nonexistent/extractor.py",
            "path to nonexistent file is also fine")

path_not_ok("contributions/symlink/extractor.py",
            "symlinked path is dangerous")

path_not_ok("contributions/symlink/nonexistent/extractor.py",
            "nonexistent path with symlink is also dangerous")

path_not_ok("../gitdeps/user/malicious/extractor.py",
            "non-101repo path is dangerous")
