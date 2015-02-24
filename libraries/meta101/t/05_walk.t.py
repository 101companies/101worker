import os
from   TAP.Simple import *
import meta101
execfile("t/dies_ok.py")
execfile("t/tempdir.py")

plan(3)

# we don't test handlepath here
called = []
def monkeypatch(*args):
    called.append(args)

meta101.util.handlepath = monkeypatch

# dummy callback function
def dummy(*args, **kwargs):
    ok(False, "this shouldn't be called")


dies_ok(lambda: meta101.util.walk(".json", dummy),
        "missing repo101dir environment variable dies")

os.environ["repo101dir"] = "/nonexistent/path"
dies_ok(lambda: meta101.util.walk(".json", dummy), "invalid repo101dir dies")


dirs = [
    "contributions/java/src",
    "contributions/perl",
    "languages/Python",
    ".git",
    ".git/branches",
]

files = [
    "contributions/java/src/Main.java",
    "contributions/java/src/Other.java",
    "contributions/java/README.md",
    "contributions/perl/script",
    "contributions/perl/Makefile",
    "languages/Python/.101meta",
    ".git/this_shouldnt_show_up",
    ".git/branches/nor_should_this",
]

with tempdir() as tmp:
    for d in dirs:  # build a directory tree
        os.makedirs(os.path.join(tmp, d))
    for f in files: # touch files
        open(os.path.join(tmp, f), "w").close()
    os.environ["repo101dir"] = tmp

    want = [(".json", dummy, os.path.join(tmp, f)) for f in files[:-2]]
    meta101.util.walk(".json", dummy)

    keyfunc = lambda x: x[2]
    want  .sort(key=keyfunc)
    called.sort(key=keyfunc)

    eq_ok(called, want, "folder is walked with all files but the ones in .git")
