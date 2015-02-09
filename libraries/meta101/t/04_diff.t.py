import os
from   StringIO       import StringIO
from   TAP.Simple     import *
from   meta101.util   import diff
import incremental101 as     inc

plan(3)

def dies_ok(code, message=None):
    try:
        code()
    except Exception as e:
        exception = e
    else:
        exception = None
    ok(exception, message)


called = []
switch = {
    "A" : lambda target, **kwargs: called.append(["A", target]),
    "M" : lambda target, **kwargs: called.append(["M", target]),
    "D" : lambda target, **kwargs: called.append(["D", target]),
}


inc.instream  = StringIO()
diff(".suffix", **switch)
eq_ok(called, [], "diff with no input doesn't call anything")


inc.instream = StringIO("A /path/repo/file\n")
dies_ok(lambda: diff(".suffix", **switch), "missing environment variables dies")


os.environ[   "repo101dir"] = "/path/repo"
os.environ["targets101dir"] = "/path/targets"

inc.instream = StringIO("""A /path/repo/added.json
A /path/targets/ignored.json
M /path/repo/somedir/modified.java
M /path/somewhere/else.java
D /path/repo/some/more/dirs/deleted
D /some/totally/different/path
""")

diff(".suffix", **switch)
eq_ok(called, [
          ["A", "/path/targets/added.json.suffix"],
          ["M", "/path/targets/somedir/modified.java.suffix"],
          ["D", "/path/targets/some/more/dirs/deleted.suffix"],
      ], "repo paths are called correctly, other paths are ignored")
