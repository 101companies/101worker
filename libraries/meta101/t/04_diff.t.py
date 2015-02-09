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
    "A" : lambda **kwargs: called.append(["A", kwargs]),
    "M" : lambda **kwargs: called.append(["M", kwargs]),
    "D" : lambda **kwargs: called.append(["D", kwargs]),
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
          ["A", {
              "target"   : "/path/targets/added.json.suffix",
              "filename" : "/path/repo/added.json",
              "dirname"  : "",
              "basename" : "added.json",
          }],
          ["M", {
              "target"   : "/path/targets/somedir/modified.java.suffix",
              "filename" : "/path/repo/somedir/modified.java",
              "dirname"  : "somedir",
              "basename" : "modified.java",
          }],
          ["D", {
              "target"   : "/path/targets/some/more/dirs/deleted.suffix",
              "filename" : "/path/repo/some/more/dirs/deleted",
              "dirname"  : "some/more/dirs",
              "basename" : "deleted",
          }],
      ], "repo paths are called correctly, other paths are ignored")
