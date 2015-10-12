from TAP.Simple import *
from StringIO   import StringIO
import os
import incremental101 as inc

plan(4)

def doline(*args):
    inc.outstream = StringIO()
    inc.deletefile(*args)
    return inc.outstream.getvalue()

if not os.path.exists("TEST"): os.mkdir("TEST")
path = "TEST/deletefile{}".format(os.getpid())
absp = os.path.abspath(path)


with open(path, "w") as f: f.write("some content\n")
ok(os.path.exists(path),                       "file exists")
eq_ok(doline(path), "\n0 D {}\n".format(absp), "delete diff is printed")
ok(not os.path.exists(path),                   "file was deleted")
eq_ok(doline(path), "\n0 - -\n",               "deleting nothing does nothing")
