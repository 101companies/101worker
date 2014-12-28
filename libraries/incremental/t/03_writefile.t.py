from TAP.Simple import *
from StringIO   import StringIO
import os
import incremental as inc

plan(7)

def doline(*args):
    inc.outstream = StringIO()
    inc.writefile(*args)
    return inc.outstream.getvalue()

if not os.path.exists("TEST"): os.mkdir("TEST")
path = "TEST/writefile{}".format(os.getpid())
ok(not os.path.exists(path), "file doesn't exist yet")


content = "file content\n"

eq_ok(doline(path, content), "0 A {}\n".format(path), "add diff is printed")
with open(path) as f:
    eq_ok(f.read(), content, "file contains given content")

eq_ok(doline(path, content), "0 - -\n", "identical content is not rewritten")
with open(path) as f:
    eq_ok(f.read(), content, "file still contains the same content")


content = "file content\nwith more stuff added\n"

eq_ok(doline(path, content), "0 M {}\n".format(path), "modify diff is printed")
with open(path) as f:
    eq_ok(f.read(), content, "file content has changed")
