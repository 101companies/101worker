from TAP.Simple import *
from StringIO   import StringIO
import os
import incremental101 as inc

plan(9)

def doline(*args):
    inc.outstream = StringIO()
    inc.writefile(*args)
    return inc.outstream.getvalue()

if not os.path.exists("TEST"): os.mkdir("TEST")
path = "TEST/writefile{}".format(os.getpid())
absp = os.path.abspath(path)


content = "file content\n"

eq_ok(doline(path, content), "\n0 A {}\n".format(absp), "add diff is printed")
with open(path) as f:
    eq_ok(f.read(), content, "file contains given content")

eq_ok(doline(path, content), "\n0 - -\n", "identical content is not rewritten")
with open(path) as f:
    eq_ok(f.read(), content, "file still contains the same content")


content = "file content\nwith more stuff added\n"

eq_ok(doline(path, content), "\n0 M {}\n".format(absp),
                             "modify diff is printed")
with open(path) as f:
    eq_ok(f.read(), content, "file content has changed")


longpath = "TEST/writefolder{}/dir/file".format(os.getpid())
longabsp = os.path.abspath(longpath)

eq_ok(doline(longpath, content), "\n0 A {}\n".format(longabsp),
      "diff with nonexistent folders runs fine")

ok(os.path.exists(longpath), "missing folders are created")

with open(longpath) as f:
    eq_ok(f.read(), content, "file contains given content")
